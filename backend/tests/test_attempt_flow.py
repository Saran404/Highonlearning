"""Start rules, lock status, autosave, submit and extension."""
from datetime import timedelta

import pytest
from sqlalchemy import select

from app.core.constants import ATTEMPT_AUTO_SUBMITTED, ATTEMPT_SUBMITTED
from app.core.exceptions import ConflictError, ForbiddenError, UnprocessableError
from app.models import Answer, Question
from app.schemas.attempt import SubmitAnswer
from app.services import attempt_service, catalog_service
from app.utils.time import utcnow
from tests.conftest import make_assessment, make_course, make_finished_attempt, make_user, start_request


def _questions(db, attempt):
    return list(db.scalars(select(Question).where(Question.assessment_id == attempt.assessment_id)
                           .order_by(Question.order_index)))


# ------------------------------------------------------------------ start rules
def test_start_creates_in_progress_attempt_with_deadline(db):
    user, a = make_user(db), make_assessment(db, make_course(db))
    attempt = attempt_service.start_attempt(db, user, start_request(a, minutes=20))
    assert attempt.status == "IN_PROGRESS" and attempt.is_graded is True
    assert attempt.deadline_at - attempt.started_at == timedelta(minutes=20)
    assert attempt.default_duration_minutes == a.default_duration_minutes


def test_start_requires_all_acknowledgments(db):
    user, a = make_user(db), make_assessment(db, make_course(db))
    with pytest.raises(UnprocessableError) as e:
        attempt_service.start_attempt(db, user, start_request(a, consent_camera=False))
    assert e.value.code == "ACKNOWLEDGMENT_REQUIRED"


@pytest.mark.parametrize("minutes", [9, 31])
def test_start_rejects_duration_outside_range(db, minutes):
    user, a = make_user(db), make_assessment(db, make_course(db), default=30, minimum=10)
    with pytest.raises(UnprocessableError) as e:
        attempt_service.start_attempt(db, user, start_request(a, minutes=minutes))
    assert e.value.code == "INVALID_DURATION"


def test_single_attempt_rule(db):
    user, a = make_user(db), make_assessment(db, make_course(db))
    attempt_service.start_attempt(db, user, start_request(a))
    with pytest.raises(ConflictError) as e:
        attempt_service.start_attempt(db, user, start_request(a))
    assert e.value.code == "ATTEMPT_EXISTS"


def test_practice_assessment_cannot_be_started_as_attempt(db):
    user, a = make_user(db), make_assessment(db, make_course(db), kind="PRACTICE")
    with pytest.raises(Exception) as e:
        attempt_service.start_attempt(db, user, start_request(a))
    assert getattr(e.value, "code", "") == "NOT_GRADED"


def test_locked_assessment_cannot_start_until_previous_is_done(db):
    course = make_course(db)
    a1, a2 = make_assessment(db, course, 1), make_assessment(db, course, 2)
    user = make_user(db)
    with pytest.raises(ForbiddenError) as e:
        attempt_service.start_attempt(db, user, start_request(a2))
    assert e.value.code == "ASSESSMENT_LOCKED"
    make_finished_attempt(db, user, a1, score=2, time_taken=100)
    assert attempt_service.start_attempt(db, user, start_request(a2)).status == "IN_PROGRESS"


# ------------------------------------------------------------------ lock status
def test_lock_status_matrix(db):
    course = make_course(db)
    a1, a2, a3 = (make_assessment(db, course, i) for i in (1, 2, 3))
    practice = make_assessment(db, course, 4, kind="PRACTICE")
    user = make_user(db)
    make_finished_attempt(db, user, a1, score=1, time_taken=50)
    attempt_service.start_attempt(db, user, start_request(a2))
    items = {i.id: i for i in catalog_service.list_course_assessments(db, user.user_id, course)}
    assert items[a1.assessment_id].lock_status == "COMPLETED" and items[a1.assessment_id].rank_position == 1
    assert items[a2.assessment_id].lock_status == "IN_PROGRESS" and items[a2.assessment_id].attempt_id
    assert items[a3.assessment_id].lock_status == "LOCKED"
    assert items[practice.assessment_id].lock_status == "AVAILABLE"


def test_first_graded_is_available_and_non_sequential_is_never_locked(db):
    course = make_course(db)
    a1 = make_assessment(db, course, 1)
    a2 = make_assessment(db, course, 2, sequential=False)
    statuses = catalog_service.resolve_lock_statuses([a1, a2], {})
    assert statuses == {a1.assessment_id: "AVAILABLE", a2.assessment_id: "AVAILABLE"}


# ------------------------------------------------------------------ questions endpoint rule
def test_graded_questions_require_running_attempt(db):
    user, a = make_user(db), make_assessment(db, make_course(db))
    with pytest.raises(ForbiddenError):
        attempt_service.questions_for_assessment(db, user, a.assessment_id)
    attempt_service.start_attempt(db, user, start_request(a))
    assert len(attempt_service.questions_for_assessment(db, user, a.assessment_id)) == 4


def test_practice_questions_always_allowed(db):
    user, a = make_user(db), make_assessment(db, make_course(db), kind="PRACTICE")
    assert len(attempt_service.questions_for_assessment(db, user, a.assessment_id)) == 4


# ------------------------------------------------------------------ answers + submit
def test_autosave_upserts_a_single_row(db):
    user, a = make_user(db), make_assessment(db, make_course(db))
    attempt = attempt_service.start_attempt(db, user, start_request(a))
    q = _questions(db, attempt)[0]
    for sel in (0, 2, 1):
        attempt_service.save_answer(db, user, attempt.attempt_id, question_id=q.question_id, selected_index=sel,
                                    marked_for_review=sel == 2)
    rows = db.scalars(select(Answer).where(Answer.attempt_id == attempt.attempt_id)).all()
    assert len(rows) == 1 and rows[0].selected_index == 1


def test_answer_rejected_after_deadline(db):
    user, a = make_user(db), make_assessment(db, make_course(db))
    attempt = attempt_service.start_attempt(db, user, start_request(a))
    attempt.deadline_at = utcnow() - timedelta(minutes=5)
    db.commit()
    with pytest.raises(ConflictError) as e:
        attempt_service.save_answer(db, user, attempt.attempt_id, question_id=_questions(db, attempt)[0].question_id,
                                    selected_index=1, marked_for_review=False)
    assert e.value.code == "ATTEMPT_EXPIRED"


def test_submit_scores_ranks_and_is_idempotent(db):
    user, a = make_user(db), make_assessment(db, make_course(db))
    attempt = attempt_service.start_attempt(db, user, start_request(a))
    qs = _questions(db, attempt)  # correct_index is 1 for every seeded question
    answers = [SubmitAnswer(question_id=qs[0].question_id, selected_index=1),
               SubmitAnswer(question_id=qs[1].question_id, selected_index=1),
               SubmitAnswer(question_id=qs[2].question_id, selected_index=0)]
    done = attempt_service.submit_attempt(db, user, attempt.attempt_id, answers, auto=False)
    assert done.status == ATTEMPT_SUBMITTED
    assert (done.score, done.total, float(done.percentage)) == (2, 4, 50.0)
    assert done.rank_position == 1 and done.motivational_message
    again = attempt_service.submit_attempt(db, user, attempt.attempt_id, [], auto=True)
    assert again.status == ATTEMPT_SUBMITTED and again.score == 2      # unchanged


def test_auto_flag_and_time_is_measured_by_the_server(db):
    user, a = make_user(db), make_assessment(db, make_course(db))
    attempt = attempt_service.start_attempt(db, user, start_request(a, minutes=10))
    attempt.started_at = utcnow() - timedelta(minutes=10, seconds=20)   # deadline passed 20 s ago
    attempt.deadline_at = attempt.started_at + timedelta(minutes=10)
    db.commit()
    done = attempt_service.submit_attempt(db, user, attempt.attempt_id, [], auto=True)
    assert done.status == ATTEMPT_AUTO_SUBMITTED and done.time_taken_sec == 600   # capped at the deadline


def test_result_hidden_until_finished_then_contains_solutions(db):
    user, a = make_user(db), make_assessment(db, make_course(db))
    attempt = attempt_service.start_attempt(db, user, start_request(a))
    with pytest.raises(ForbiddenError):
        attempt_service.build_result(db, attempt)
    attempt_service.submit_attempt(db, user, attempt.attempt_id, [], auto=False)
    result = attempt_service.build_result(db, attempt_service.get_attempt(db, attempt.attempt_id))
    assert len(result["questions"]) == 4 and result["questions"][0]["correct_index"] == 1
    assert result["attempt"]["total_participants"] == 1


# ------------------------------------------------------------------ extension
def test_extension_window(db):
    user, a = make_user(db), make_assessment(db, make_course(db), default=30, minimum=10)
    attempt = attempt_service.start_attempt(db, user, start_request(a, minutes=10))
    with pytest.raises(ConflictError) as e:                       # too early
        attempt_service.extend_attempt(db, user, attempt.attempt_id)
    assert e.value.code == "EXTENSION_TOO_EARLY"

    attempt.started_at = utcnow() - timedelta(minutes=11)         # chosen time is over, default not yet
    attempt.deadline_at = attempt.started_at + timedelta(minutes=10)
    db.commit()
    extended = attempt_service.extend_attempt(db, user, attempt.attempt_id)
    assert extended.extended_duration is True
    assert extended.deadline_at == extended.started_at + timedelta(minutes=30)

    with pytest.raises(ConflictError) as e:                       # only once
        attempt_service.extend_attempt(db, user, attempt.attempt_id)
    assert e.value.code == "EXTENSION_ALREADY_USED"


def test_no_extension_when_chosen_equals_default(db):
    user, a = make_user(db), make_assessment(db, make_course(db), default=30)
    attempt = attempt_service.start_attempt(db, user, start_request(a, minutes=30))
    attempt.started_at = utcnow() - timedelta(minutes=31)
    attempt.deadline_at = attempt.started_at + timedelta(minutes=30)
    db.commit()
    with pytest.raises(ConflictError) as e:
        attempt_service.extend_attempt(db, user, attempt.attempt_id)
    assert e.value.code == "EXTENSION_NOT_AVAILABLE"


# ------------------------------------------------------------------ sweeper + admin reset
def test_sweeper_closes_only_abandoned_attempts(db):
    course = make_course(db)
    a1, a2 = make_assessment(db, course, 1, sequential=False), make_assessment(db, course, 2, sequential=False)
    gone, active = make_user(db), make_user(db)
    stale = attempt_service.start_attempt(db, gone, start_request(a1, minutes=10))
    fresh = attempt_service.start_attempt(db, active, start_request(a2, minutes=10))
    stale.started_at = utcnow() - timedelta(hours=2)
    stale.deadline_at = stale.started_at + timedelta(minutes=10)
    db.commit()
    assert attempt_service.auto_submit_expired(db) == 1
    db.refresh(stale), db.refresh(fresh)
    assert stale.status == ATTEMPT_AUTO_SUBMITTED and stale.time_taken_sec == 600
    assert fresh.status == "IN_PROGRESS"


def test_admin_reset_allows_a_fresh_attempt(db):
    user, a = make_user(db), make_assessment(db, make_course(db))
    admin = make_user(db, role="ADMIN")
    from app.services import admin_service
    attempt = attempt_service.start_attempt(db, user, start_request(a))
    q = _questions(db, attempt)[0]
    attempt_service.save_answer(db, user, attempt.attempt_id, question_id=q.question_id, selected_index=1, marked_for_review=False)
    admin_service.reset_attempt(db, admin, attempt.attempt_id)
    assert db.scalars(select(Answer)).all() == []
    assert attempt_service.start_attempt(db, user, start_request(a)).status == "IN_PROGRESS"


def test_course_sequential_unlock_progression(db):
    from app.models import Course
    from app.services import practice_service
    user = make_user(db)
    c1 = Course(title="Course 1", slug="course-1", order_index=1)
    c2 = Course(title="Course 2", slug="course-2", order_index=2)
    c3 = Course(title="Course 3", slug="course-3", order_index=3)
    db.add_all([c1, c2, c3])
    db.commit()

    a1 = make_assessment(db, c1, 1, kind="GRADED")
    p1 = make_assessment(db, c1, 2, kind="PRACTICE")
    a2 = make_assessment(db, c2, 1, kind="GRADED")
    p2 = make_assessment(db, c2, 2, kind="PRACTICE")
    a3 = make_assessment(db, c3, 1, kind="GRADED")

    # Initial state: only Course 1 is unlocked
    courses = catalog_service.resolve_all_courses_with_status(db, user.user_id)
    by_slug = {c.slug: c for c in courses}
    assert by_slug["course-1"].lock_status == "AVAILABLE"
    assert by_slug["course-2"].lock_status == "LOCKED"
    assert by_slug["course-2"].previous_course_title == "Course 1"
    assert by_slug["course-3"].lock_status == "LOCKED"
    assert by_slug["course-3"].previous_course_title == "Course 2"

    # Attempting to start attempt or practice in Course 2 raises COURSE_LOCKED
    with pytest.raises(ForbiddenError) as e:
        attempt_service.start_attempt(db, user, start_request(a2))
    assert e.value.code == "COURSE_LOCKED"

    with pytest.raises(ForbiddenError) as e:
        practice_service.practice_questions(db, user.user_id, p2.assessment_id)
    assert e.value.code == "COURSE_LOCKED"

    # User starts Course 1: Course 1 becomes IN_PROGRESS
    attempt = attempt_service.start_attempt(db, user, start_request(a1))
    c1_stat = {c.slug: c for c in catalog_service.resolve_all_courses_with_status(db, user.user_id)}
    assert c1_stat["course-1"].lock_status == "IN_PROGRESS"

    # User finishes graded test for Course 1
    attempt_service.submit_attempt(db, user, attempt.attempt_id, answers=[], auto=False)
    courses_after_graded1 = {c.slug: c for c in catalog_service.resolve_all_courses_with_status(db, user.user_id)}
    # Course 1 is still IN_PROGRESS and Course 2 is still LOCKED because Reflective Activity is required!
    assert courses_after_graded1["course-1"].lock_status == "IN_PROGRESS"
    assert courses_after_graded1["course-2"].lock_status == "LOCKED"

    # User completes Reflective Activity for Course 1
    from app.services import reflection_service
    from app.schemas.reflection import ReflectionAnswerItem
    reflection_service.save_user_course_reflection(
        db, user.user_id, c1.slug,
        [ReflectionAnswerItem(question_number=1, question="Q1", selected_option="Opt1")]
    )
    courses_after_c1 = {c.slug: c for c in catalog_service.resolve_all_courses_with_status(db, user.user_id)}
    assert courses_after_c1["course-1"].lock_status == "COMPLETED"
    assert courses_after_c1["course-2"].lock_status == "AVAILABLE"
    assert courses_after_c1["course-3"].lock_status == "LOCKED"

    # Now Course 2 practice and graded tests can be accessed!
    p_qs = practice_service.practice_questions(db, user.user_id, p2.assessment_id)
    assert len(p_qs) > 0

    att2 = attempt_service.start_attempt(db, user, start_request(a2))
    assert att2.status == "IN_PROGRESS"

    # User finishes graded test for Course 2: Course 2 is IN_PROGRESS until reflection is submitted
    attempt_service.submit_attempt(db, user, att2.attempt_id, answers=[], auto=False)
    courses_after_graded2 = {c.slug: c for c in catalog_service.resolve_all_courses_with_status(db, user.user_id)}
    assert courses_after_graded2["course-2"].lock_status == "IN_PROGRESS"
    assert courses_after_graded2["course-3"].lock_status == "LOCKED"

    # User completes Reflective Activity for Course 2 -> unlocks Course 3!
    reflection_service.save_user_course_reflection(
        db, user.user_id, c2.slug,
        [ReflectionAnswerItem(question_number=1, question="Q1", selected_option="Opt1")]
    )
    courses_after_c2 = {c.slug: c for c in catalog_service.resolve_all_courses_with_status(db, user.user_id)}
    assert courses_after_c2["course-1"].lock_status == "COMPLETED"
    assert courses_after_c2["course-2"].lock_status == "COMPLETED"
    assert courses_after_c2["course-3"].lock_status == "AVAILABLE"


def test_snapshots_hidden_from_regular_users_in_result(db):
    from app.models import ProctoringSnapshot
    user, a = make_user(db), make_assessment(db, make_course(db))
    attempt = attempt_service.start_attempt(db, user, start_request(a))
    now = utcnow()
    snap = ProctoringSnapshot(attempt_id=attempt.attempt_id, image_path="dummy.jpg", captured_at=now, trigger_type="interval")
    db.add(snap)
    db.commit()

    attempt_service.submit_attempt(db, user, attempt.attempt_id, answers=[], auto=False)

    # For regular user (is_admin=False), snapshots should be empty
    res_user = attempt_service.build_result(db, attempt, is_admin=False)
    assert res_user["snapshots"] == []

    # For admin (is_admin=True), snapshots should be included
    res_admin = attempt_service.build_result(db, attempt, is_admin=True)
    assert len(res_admin["snapshots"]) == 1
    assert res_admin["snapshots"][0]["snapshot_id"] == snap.snapshot_id

