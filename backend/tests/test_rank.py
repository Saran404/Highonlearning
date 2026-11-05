"""Rank = COUNT(*)+1 of finished attempts with a higher score, or equal score and less time."""
from app.core.constants import ATTEMPT_AUTO_SUBMITTED, ATTEMPT_FLAGGED, ATTEMPT_IN_PROGRESS
from app.services import rank_service
from tests.conftest import make_assessment, make_course, make_finished_attempt, make_user


def _setup(db):
    course = make_course(db)
    return make_assessment(db, course)


def test_first_attempt_is_rank_one(db):
    a = _setup(db)
    assert rank_service.compute_rank(db, a.assessment_id, score=3, time_taken_sec=600) == 1


def test_higher_score_wins_then_faster_time(db):
    a = _setup(db)
    make_finished_attempt(db, make_user(db), a, score=4, time_taken=900)
    make_finished_attempt(db, make_user(db), a, score=3, time_taken=300)
    make_finished_attempt(db, make_user(db), a, score=3, time_taken=500)
    assert rank_service.compute_rank(db, a.assessment_id, 4, 800) == 1    # beats the only 4/4 on time
    assert rank_service.compute_rank(db, a.assessment_id, 4, 950) == 2    # slower than the 4/4
    assert rank_service.compute_rank(db, a.assessment_id, 3, 400) == 3    # behind 4/4 and 3/4@300
    assert rank_service.compute_rank(db, a.assessment_id, 3, 600) == 4
    assert rank_service.compute_rank(db, a.assessment_id, 1, 10) == 4   # nobody scored lower


def test_ties_share_a_rank(db):
    a = _setup(db)
    make_finished_attempt(db, make_user(db), a, score=3, time_taken=500)
    make_finished_attempt(db, make_user(db), a, score=3, time_taken=500)
    assert rank_service.compute_rank(db, a.assessment_id, 3, 500) == 1   # equal time => nobody is better
    assert rank_service.compute_rank(db, a.assessment_id, 2, 100) == 3


def test_in_progress_attempts_do_not_count(db):
    a = _setup(db)
    make_finished_attempt(db, make_user(db), a, score=4, time_taken=100, status=ATTEMPT_IN_PROGRESS)
    assert rank_service.compute_rank(db, a.assessment_id, 0, 1000) == 1
    assert rank_service.total_participants(db, a.assessment_id) == 0


def test_flagged_and_auto_submitted_count(db):
    a = _setup(db)
    make_finished_attempt(db, make_user(db), a, score=4, time_taken=100, status=ATTEMPT_FLAGGED)
    make_finished_attempt(db, make_user(db), a, score=4, time_taken=200, status=ATTEMPT_AUTO_SUBMITTED)
    assert rank_service.compute_rank(db, a.assessment_id, 4, 150) == 2
    assert rank_service.total_participants(db, a.assessment_id) == 2


def test_other_assessments_do_not_interfere(db):
    course = make_course(db)
    a1, a2 = make_assessment(db, course, 1), make_assessment(db, course, 2)
    make_finished_attempt(db, make_user(db), a2, score=4, time_taken=10)
    assert rank_service.compute_rank(db, a1.assessment_id, 1, 999) == 1


def test_rank_rows_competition_ranking():
    assert rank_service.rank_rows([(4, 10), (3, 5), (3, 5), (3, 9), (1, 1)]) == [1, 2, 2, 4, 5]


def test_leaderboard_orders_and_reports_me(db):
    a = _setup(db)
    slow, fast, me = make_user(db), make_user(db), make_user(db)
    make_finished_attempt(db, slow, a, score=3, time_taken=900)
    make_finished_attempt(db, fast, a, score=3, time_taken=300)
    make_finished_attempt(db, me, a, score=4, time_taken=1200)
    board = rank_service.leaderboard(db, a.assessment_id, viewer_id=me.user_id)
    assert [e["rank"] for e in board["entries"]] == [1, 2, 3]
    assert board["entries"][0]["is_me"] is True
    assert board["me"]["rank"] == 1 and board["total_participants"] == 3


def test_refresh_stored_ranks(db):
    a = _setup(db)
    x = make_finished_attempt(db, make_user(db), a, score=2, time_taken=100)
    y = make_finished_attempt(db, make_user(db), a, score=4, time_taken=100)
    assert rank_service.refresh_stored_ranks(db, a.assessment_id) == 2
    db.commit()
    db.refresh(x), db.refresh(y)
    assert (y.rank_position, x.rank_position) == (1, 2)
