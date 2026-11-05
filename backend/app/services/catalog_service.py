"""Courses, assessments, lock status and the student dashboard."""
from __future__ import annotations

import logging
from typing import Optional

from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import Session

from app.core.constants import (ATTEMPT_IN_PROGRESS, FINAL_STATUSES, LOCK_AVAILABLE, LOCK_COMPLETED,
                                LOCK_IN_PROGRESS, LOCK_LOCKED, TYPE_GRADED, TYPE_PRACTICE)
from app.core.exceptions import NotFoundError
from app.models import Assessment, Attempt, Course, Enrollment, CourseReflection
from app.schemas.assessment import AssessmentListItem, AssessmentOut
from app.schemas.course import CourseOut
from app.services import rank_service
from app.utils.time import utcnow

logger = logging.getLogger("exampro")


def get_course_by_slug(db: Session, slug: str) -> Course:
    course = db.scalar(select(Course).where(Course.slug == slug))
    if course is None:
        raise NotFoundError("Course not found.", code="COURSE_NOT_FOUND")
    return course


def resolve_all_courses_with_status(db: Session, user_id: int) -> list[CourseOut]:
    """Calculate counts and sequential lock status across all courses for a user.

    Sequential unlocking rules:
    - Only the first course (order_index lowest) is unlocked initially (AVAILABLE or IN_PROGRESS).
    - A user must fully complete the current course before the next course becomes available.
    - Course (N) unlocks after completing Course (N-1), sequentially through all courses.
    - Locked courses have lock_status = LOCKED and reference previous_course_title/slug.
    """
    courses = list(db.scalars(select(Course).order_by(Course.order_index, Course.course_id)))
    if not courses:
        return []

    # 1. Counts of graded & practice per course
    counts_rows = db.execute(
        select(Assessment.course_id, Assessment.attempt_type, func.count())
        .group_by(Assessment.course_id, Assessment.attempt_type)
    ).all()
    graded_by_course: dict[int, int] = {}
    practice_by_course: dict[int, int] = {}
    for cid, atype, cnt in counts_rows:
        if atype == TYPE_GRADED:
            graded_by_course[cid] = int(cnt)
        elif atype == TYPE_PRACTICE:
            practice_by_course[cid] = int(cnt)

    # 2. Completed distinct graded assessments per course
    completed_rows = db.execute(
        select(Assessment.course_id, func.count(func.distinct(Attempt.assessment_id)))
        .select_from(Attempt)
        .join(Assessment, Assessment.assessment_id == Attempt.assessment_id)
        .where(Attempt.user_id == user_id, Attempt.is_graded == True, Attempt.status.in_(FINAL_STATUSES))
        .group_by(Assessment.course_id)
    ).all()
    completed_by_course = {cid: int(cnt) for cid, cnt in completed_rows}

    # 3. Active in-progress attempts per course
    active_rows = db.execute(
        select(Assessment.course_id, func.count())
        .select_from(Attempt)
        .join(Assessment, Assessment.assessment_id == Attempt.assessment_id)
        .where(Attempt.user_id == user_id, Attempt.status == ATTEMPT_IN_PROGRESS)
        .group_by(Assessment.course_id)
    ).all()
    active_by_course = {cid: int(cnt) > 0 for cid, cnt in active_rows}

    # 4. Enrollments
    enrollment_rows = db.execute(
        select(Enrollment.course_id, Enrollment.completed_at)
        .where(Enrollment.user_id == user_id)
    ).all()
    enrollment_by_course = {cid: comp for cid, comp in enrollment_rows}

    # 5. Reflective activity completion per course
    reflection_by_course: set[int] = set()
    try:
        reflection_rows = db.execute(
            select(CourseReflection.course_id)
            .where(CourseReflection.user_id == user_id)
        ).all()
        reflection_by_course = {cid for (cid,) in reflection_rows}
    except Exception as e:
        logger.warning("Could not query CourseReflections in resolve_all_courses_with_status: %s", e)
        db.rollback()

    # 6. Sequential unlock resolution
    results: list[CourseOut] = []
    previous_done: bool = True  # Course 1 is unlocked initially
    prev_title: Optional[str] = None
    prev_slug: Optional[str] = None

    for c in courses:
        g_cnt = graded_by_course.get(c.course_id, 0)
        p_cnt = practice_by_course.get(c.course_id, 0)
        c_cnt = completed_by_course.get(c.course_id, 0)
        has_active = active_by_course.get(c.course_id, False)
        enrolled = c.course_id in enrollment_by_course
        completed_at = enrollment_by_course.get(c.course_id)
        has_reflection = c.course_id in reflection_by_course

        # Course unlock: Course is only completed after finishing the Reflective Activity (and all graded tests if any)
        graded_done = (g_cnt == 0 or c_cnt >= g_cnt)
        is_completed = (completed_at is not None) or (graded_done and has_reflection)

        if is_completed:
            lock_status = LOCK_COMPLETED
            c_prev_title = prev_title
            c_prev_slug = prev_slug
            previous_done = True
        elif previous_done:
            lock_status = LOCK_IN_PROGRESS if (c_cnt > 0 or has_active or enrolled or has_reflection) else LOCK_AVAILABLE
            c_prev_title = prev_title
            c_prev_slug = prev_slug
            previous_done = False
        else:
            lock_status = LOCK_LOCKED
            c_prev_title = prev_title
            c_prev_slug = prev_slug
            previous_done = False

        prev_title = c.title
        prev_slug = c.slug

        results.append(
            CourseOut(
                id=c.course_id,
                title=c.title,
                slug=c.slug,
                description=c.description,
                thumbnail_url=c.thumbnail_url,
                order_index=c.order_index,
                graded_count=g_cnt,
                practice_count=p_cnt,
                completed_count=c_cnt,
                enrolled=enrolled,
                lock_status=lock_status,
                previous_course_title=c_prev_title,
                previous_course_slug=c_prev_slug,
                created_at=c.created_at,
            )
        )

    return results


def course_lock_status(db: Session, user_id: int, course: Course) -> tuple[str, Optional[str], Optional[str]]:
    """Return (lock_status, previous_course_title, previous_course_slug) for a course."""
    courses = resolve_all_courses_with_status(db, user_id)
    for c in courses:
        if c.id == course.course_id or c.slug == course.slug:
            return c.lock_status, c.previous_course_title, c.previous_course_slug
    return LOCK_AVAILABLE, None, None


def resolve_lock_statuses(assessments: list[Assessment], attempts_by_assessment: dict[int, Attempt]) -> dict[int, str]:
    """Pure sequential-unlock logic for ONE course (``assessments`` sorted by OrderIndex).

    * PRACTICE  -> always AVAILABLE (no unlock chain, no completion state).
    * GRADED    -> COMPLETED if a finished attempt exists; IN_PROGRESS if one is running;
                   else AVAILABLE when unlock is not sequential, when it is the first graded test,
                   or when the previous graded test has a finished attempt; else LOCKED.
    """
    statuses: dict[int, str] = {}
    previous_done: Optional[bool] = None  # None => no previous graded assessment
    for a in assessments:
        if a.attempt_type == TYPE_PRACTICE:
            statuses[a.assessment_id] = LOCK_AVAILABLE
            continue
        attempt = attempts_by_assessment.get(a.assessment_id)
        if attempt is not None and attempt.status in FINAL_STATUSES:
            statuses[a.assessment_id] = LOCK_COMPLETED
            done = True
        elif attempt is not None and attempt.status == ATTEMPT_IN_PROGRESS:
            statuses[a.assessment_id] = LOCK_IN_PROGRESS
            done = False
        else:
            unlocked = (not a.sequential_unlock) or previous_done is None or previous_done
            statuses[a.assessment_id] = LOCK_AVAILABLE if unlocked else LOCK_LOCKED
            done = False
        previous_done = done
    return statuses


def _user_graded_attempts(db: Session, user_id: int, assessment_ids: list[int]) -> dict[int, Attempt]:
    if not assessment_ids:
        return {}
    rows = db.scalars(select(Attempt).where(Attempt.user_id == user_id, Attempt.is_graded == True,
                                            Attempt.assessment_id.in_(assessment_ids)))
    return {a.assessment_id: a for a in rows}


def lock_status_for(db: Session, user_id: int, assessment: Assessment) -> str:
    """Lock status of a single assessment for a student (used by the start-attempt guard)."""
    siblings = list(db.scalars(select(Assessment).where(Assessment.course_id == assessment.course_id)
                               .order_by(Assessment.order_index, Assessment.assessment_id)))
    attempts = _user_graded_attempts(db, user_id, [a.assessment_id for a in siblings])
    return resolve_lock_statuses(siblings, attempts)[assessment.assessment_id]


def list_course_assessments(db: Session, user_id: int, course: Course,
                            course_lock: Optional[str] = None) -> list[AssessmentListItem]:
    """Every assessment of a course with the student's lock status, score and live rank."""
    if course_lock is not None:
        c_status = course_lock
    else:
        c_status, _, _ = course_lock_status(db, user_id, course)
    assessments = list(db.scalars(select(Assessment).where(Assessment.course_id == course.course_id)
                                  .order_by(Assessment.order_index, Assessment.assessment_id)))
    attempts = _user_graded_attempts(db, user_id, [a.assessment_id for a in assessments])
    statuses = resolve_lock_statuses(assessments, attempts)
    items: list[AssessmentListItem] = []
    for a in assessments:
        base = AssessmentOut.from_model(a).model_dump()
        assigned_status = LOCK_LOCKED if c_status == LOCK_LOCKED else statuses[a.assessment_id]
        item = AssessmentListItem(**{**base, "lock_status": assigned_status,
                                     "course_slug": course.slug, "course_title": course.title})
        att = attempts.get(a.assessment_id)
        if att is not None:
            item.attempt_id = att.attempt_id
            if att.status in FINAL_STATUSES:
                item.score, item.total = att.score, att.total
                item.percentage = float(att.percentage or 0)
                item.time_taken_sec = att.time_taken_sec
                item.rank_position = rank_service.compute_rank(db, a.assessment_id, att.score or 0, att.time_taken_sec)
                item.total_participants = rank_service.total_participants(db, a.assessment_id)
        items.append(item)
    return items


def ensure_enrolled(db: Session, user_id: int, course_id: int) -> None:
    """Idempotently enrol a student. Caller commits."""
    exists = db.scalar(select(Enrollment.enrollment_id).where(Enrollment.user_id == user_id,
                                                              Enrollment.course_id == course_id))
    if exists is None:
        db.add(Enrollment(user_id=user_id, course_id=course_id, enrolled_at=utcnow()))


def mark_course_completed_if_done(db: Session, user_id: int, course_id: int) -> None:
    """Set ``Enrollments.CompletedAt`` once every graded assessment AND the reflective activity of the course is finished. Caller commits."""
    graded_ids = list(db.scalars(select(Assessment.assessment_id).where(
        Assessment.course_id == course_id, Assessment.attempt_type == TYPE_GRADED)))
    if graded_ids:
        done = db.scalar(select(func.count(func.distinct(Attempt.assessment_id))).where(
            Attempt.user_id == user_id, Attempt.assessment_id.in_(graded_ids), Attempt.status.in_(FINAL_STATUSES)))
        if int(done or 0) < len(graded_ids):
            return

    # Must also complete Reflective Activity
    has_reflection = False
    try:
        has_reflection = db.scalar(
            select(CourseReflection.reflection_id).where(
                CourseReflection.user_id == user_id,
                CourseReflection.course_id == course_id,
            )
        ) is not None
    except Exception as e:
        logger.warning("Could not query CourseReflection in mark_course_completed_if_done: %s", e)
        db.rollback()

    if not has_reflection:
        return

    enrollment = db.scalar(select(Enrollment).where(Enrollment.user_id == user_id, Enrollment.course_id == course_id))
    if enrollment is None:
        enrollment = Enrollment(user_id=user_id, course_id=course_id, enrolled_at=utcnow(), completed_at=utcnow())
        db.add(enrollment)
    elif enrollment.completed_at is None:
        enrollment.completed_at = utcnow()


def dashboard(db: Session, user_id: int) -> dict:
    """Everything the student dashboard needs in one round trip with batched queries."""
    course_outs = resolve_all_courses_with_status(db, user_id)
    course_status_by_id = {c.id: c.lock_status for c in course_outs}
    courses = list(db.scalars(select(Course).order_by(Course.order_index, Course.course_id)))

    # 1. Batch fetch all assessments across all courses
    all_assessments = list(db.scalars(select(Assessment).order_by(Assessment.course_id, Assessment.order_index, Assessment.assessment_id)))
    assessments_by_course: dict[int, list[Assessment]] = {}
    for a in all_assessments:
        assessments_by_course.setdefault(a.course_id, []).append(a)

    # 2. Batch fetch user's attempts across all assessments
    all_attempts = list(db.scalars(select(Attempt).where(Attempt.user_id == user_id, Attempt.is_graded == True)))
    attempts_by_assessment = {att.assessment_id: att for att in all_attempts}

    # 3. Batch fetch total participants for all assessments
    part_counts = dict(
        db.execute(
            select(Attempt.assessment_id, func.count())
            .where(Attempt.status.in_(FINAL_STATUSES))
            .group_by(Attempt.assessment_id)
        ).all()
    )

    # 4. Batch compute ranks for completed attempts
    completed_atts = [att for att in all_attempts if att.status in FINAL_STATUSES and att.score is not None]
    rank_conditions = []
    for att in completed_atts:
        t_sec = 2**31 - 1 if att.time_taken_sec is None else att.time_taken_sec
        rank_conditions.append(
            and_(
                Attempt.assessment_id == att.assessment_id,
                or_(Attempt.score > att.score, and_(Attempt.score == att.score, Attempt.time_taken_sec < t_sec)),
            )
        )

    better_counts: dict[int, int] = {}
    if rank_conditions:
        better_rows = db.execute(
            select(Attempt.assessment_id, func.count())
            .where(Attempt.status.in_(FINAL_STATUSES), or_(*rank_conditions))
            .group_by(Attempt.assessment_id)
        ).all()
        better_counts = {aid: int(cnt) for aid, cnt in better_rows}

    rows: list[AssessmentListItem] = []
    for c in courses:
        c_status = course_status_by_id.get(c.course_id, LOCK_AVAILABLE)
        course_ass = assessments_by_course.get(c.course_id, [])
        statuses = resolve_lock_statuses(course_ass, attempts_by_assessment)
        for a in course_ass:
            base = AssessmentOut.from_model(a).model_dump()
            assigned_status = LOCK_LOCKED if c_status == LOCK_LOCKED else statuses[a.assessment_id]
            item = AssessmentListItem(**{**base, "lock_status": assigned_status,
                                         "course_slug": c.slug, "course_title": c.title})
            att = attempts_by_assessment.get(a.assessment_id)
            if att is not None:
                item.attempt_id = att.attempt_id
                if att.status in FINAL_STATUSES:
                    item.score, item.total = att.score, att.total
                    item.percentage = float(att.percentage or 0)
                    item.time_taken_sec = att.time_taken_sec
                    item.rank_position = better_counts.get(a.assessment_id, 0) + 1
                    item.total_participants = part_counts.get(a.assessment_id, 0)
            rows.append(item)

    graded = [r for r in rows if r.attempt_type == TYPE_GRADED]
    completed = [r for r in graded if r.lock_status == LOCK_COMPLETED]
    ranks = [r.rank_position for r in completed if r.rank_position]
    enrolled = int(db.scalar(select(func.count()).select_from(Enrollment).where(Enrollment.user_id == user_id)) or 0)
    completed_courses = sum(1 for c in course_outs if c.lock_status == LOCK_COMPLETED)

    continue_item = next((r for r in graded if r.lock_status == LOCK_IN_PROGRESS), None) or \
        next((r for r in graded if r.lock_status == LOCK_AVAILABLE), None)
    return {
        "stats": {
            "courses_enrolled": enrolled,
            "courses_completed": completed_courses,
            "courses_total": len(course_outs),
            "assessments_completed": len(completed),
            "assessments_total": len(graded),
            "avg_percentage": round(sum(r.percentage or 0 for r in completed) / len(completed), 2) if completed else 0.0,
            "best_rank": min(ranks) if ranks else None,
            "completion_percentage": round(100 * len(completed) / len(graded), 1) if graded else 0.0,
        },
        "assessments": rows,
        "continue_item": continue_item,
    }

