"""Malpractice strikes: logging, counter, threshold auto-submit."""
import pytest

from app.config import settings
from app.core.constants import ATTEMPT_FLAGGED, ATTEMPT_IN_PROGRESS
from app.core.exceptions import ConflictError, NotFoundError
from app.models import MalpracticeLog
from app.services import attempt_service
from sqlalchemy import select
from tests.conftest import make_assessment, make_course, make_user, start_request


@pytest.mark.parametrize("count,limit,expected", [(0, 3, False), (1, 3, False), (2, 3, False), (3, 3, True), (4, 3, True)])
def test_threshold_rule(count, limit, expected):
    assert attempt_service.malpractice_should_terminate(count, limit) is expected


def _start(db, monkeypatch, limit=3):
    monkeypatch.setattr(settings, "MAX_MALPRACTICE", limit)
    user = make_user(db)
    a = make_assessment(db, make_course(db))
    attempt = attempt_service.start_attempt(db, user, start_request(a))
    return user, attempt


def test_strikes_are_counted_and_logged(db, monkeypatch):
    user, attempt = _start(db, monkeypatch)
    assert attempt_service.record_malpractice(db, user, attempt.attempt_id, "TAB_SWITCH", {"n": 1}) == (1, False)
    assert attempt_service.record_malpractice(db, user, attempt.attempt_id, "FULLSCREEN_EXIT", None) == (2, False)
    db.refresh(attempt)
    assert attempt.status == ATTEMPT_IN_PROGRESS and attempt.malpractice_count == 2
    logs = db.scalars(select(MalpracticeLog).where(MalpracticeLog.attempt_id == attempt.attempt_id)).all()
    assert [l.type for l in logs] == ["TAB_SWITCH", "FULLSCREEN_EXIT"]


def test_reaching_the_limit_flags_and_scores_the_attempt(db, monkeypatch):
    user, attempt = _start(db, monkeypatch, limit=3)
    for _ in range(2):
        attempt_service.record_malpractice(db, user, attempt.attempt_id, "TAB_SWITCH", None)
    count, terminate = attempt_service.record_malpractice(db, user, attempt.attempt_id, "MINIMIZE", None)
    assert (count, terminate) == (3, True)
    db.refresh(attempt)
    assert attempt.status == ATTEMPT_FLAGGED
    assert attempt.score == 0 and attempt.total == 4          # nothing answered => 0/4
    assert attempt.rank_position == 1 and attempt.submitted_at is not None
    assert attempt.motivational_message


def test_flagged_attempt_keeps_answers_saved_before_termination(db, monkeypatch):
    user, attempt = _start(db, monkeypatch, limit=1)
    from app.models import Question
    q = db.scalars(select(Question).where(Question.assessment_id == attempt.assessment_id)).first()
    attempt_service.save_answer(db, user, attempt.attempt_id, question_id=q.question_id, selected_index=1, marked_for_review=False)
    attempt_service.record_malpractice(db, user, attempt.attempt_id, "DEVTOOLS", None)
    db.refresh(attempt)
    assert attempt.status == ATTEMPT_FLAGGED and attempt.score == 1


def test_no_more_strikes_after_termination(db, monkeypatch):
    user, attempt = _start(db, monkeypatch, limit=1)
    attempt_service.record_malpractice(db, user, attempt.attempt_id, "TAB_SWITCH", None)
    with pytest.raises(ConflictError):
        attempt_service.record_malpractice(db, user, attempt.attempt_id, "TAB_SWITCH", None)


def test_cannot_report_malpractice_on_someone_elses_attempt(db, monkeypatch):
    _, attempt = _start(db, monkeypatch)
    with pytest.raises(NotFoundError):
        attempt_service.record_malpractice(db, make_user(db), attempt.attempt_id, "TAB_SWITCH", None)
