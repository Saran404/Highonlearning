"""Graded attempt engine: start, autosave, malpractice, extension, submit, result, auto-submit sweeper.

Design notes
------------
* The **server clock is the only clock that matters**. ``time_taken_sec`` sent by the browser is
  ignored; time is derived from ``StartedAt`` and ``DeadlineAt``.
* Mutating operations lock the attempt row (``SELECT ... WITH (UPDLOCK)`` on SQL Server) so two
  simultaneous requests (double-click, two tabs, sweeper vs. student) cannot both finalise it.
* ``submit`` is idempotent: submitting an already-finished attempt just returns it.
* Every function that writes commits exactly once, so each request is a single transaction.
* WebSocket events are published only *after* the commit succeeded.
"""
from __future__ import annotations

import json
import logging
from datetime import timedelta
from typing import Any, Optional

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import settings
from app.core.constants import (ATTEMPT_AUTO_SUBMITTED, ATTEMPT_FLAGGED, ATTEMPT_IN_PROGRESS, ATTEMPT_SUBMITTED,
                                FINAL_STATUSES, LOCK_LOCKED, ROLE_ADMIN, TYPE_GRADED, TYPE_PRACTICE)
from app.core.exceptions import (BadRequestError, ConflictError, ForbiddenError, NotFoundError,
                                 UnprocessableError)
from app.core.websocket_manager import ws_manager
from app.models import Answer, Assessment, Attempt, Course, MalpracticeLog, ProctoringSnapshot, Question, User
from app.schemas.assessment import QuestionPublic
from app.schemas.attempt import AttemptState, SavedAnswer, StartAttemptRequest, SubmitAnswer
from app.services import catalog_service, rank_service
from app.services.motivation_service import get_motivation
from app.services.scoring_service import compute_percentage, compute_score, is_passed
from app.utils.storage import signed_snapshot_url
from app.utils.time import utcnow

logger = logging.getLogger("exampro.attempts")


# --------------------------------------------------------------------------- pure rules
def malpractice_should_terminate(count: int, max_allowed: int) -> bool:
    """``True`` once the student has reached ``max_allowed`` strikes (3 strikes => auto-submit)."""
    return count >= max_allowed


# --------------------------------------------------------------------------- loading helpers
def get_attempt(db: Session, attempt_id: int, *, user_id: Optional[int] = None, lock: bool = False) -> Attempt:
    """Load an attempt (404 when missing or owned by someone else). ``lock=True`` takes a row lock."""
    stmt = select(Attempt).where(Attempt.attempt_id == attempt_id)
    if lock:
        stmt = stmt.with_for_update().execution_options(populate_existing=True)
    attempt = db.scalar(stmt)
    if attempt is None or (user_id is not None and attempt.user_id != user_id):
        raise NotFoundError("Attempt not found.", code="ATTEMPT_NOT_FOUND")
    return attempt


def load_questions(db: Session, assessment_id: int) -> list[Question]:
    return list(db.scalars(select(Question).where(Question.assessment_id == assessment_id)
                           .order_by(Question.order_index, Question.question_id)))


def _require_active(attempt: Attempt) -> None:
    if attempt.status != ATTEMPT_IN_PROGRESS:
        raise ConflictError("This attempt is already finished.", code="ATTEMPT_NOT_ACTIVE",
                            details={"status": attempt.status})


def attempt_state(db: Session, attempt: Attempt) -> AttemptState:
    """Questions (without answers) + saved answers + timing, used for start and resume."""
    questions = load_questions(db, attempt.assessment_id)
    saved = db.scalars(select(Answer).where(Answer.attempt_id == attempt.attempt_id))
    a = attempt.assessment
    return AttemptState(
        attempt_id=attempt.attempt_id, assessment_id=attempt.assessment_id, assessment_title=a.title,
        status=attempt.status, questions=[QuestionPublic.from_model(q) for q in questions],
        saved_answers=[SavedAnswer(question_id=s.question_id, selected_index=s.selected_index,
                                   marked_for_review=s.marked_for_review) for s in saved],
        started_at=attempt.started_at, deadline_at=attempt.deadline_at, server_time=utcnow(),
        default_duration_minutes=attempt.default_duration_minutes,
        chosen_duration_minutes=attempt.chosen_duration_minutes, extended=attempt.extended_duration,
        malpractice_count=attempt.malpractice_count, max_malpractice=settings.MAX_MALPRACTICE,
        lockdown_enabled=a.lockdown_enabled, proctoring_enabled=a.proctoring_enabled,
    )


def questions_for_assessment(db: Session, user: User, assessment_id: int) -> list[Question]:
    """Questions for ``GET /assessments/{id}/questions``: always for PRACTICE; for GRADED only while the
    student has a running attempt."""
    assessment = db.get(Assessment, assessment_id)
    if assessment is None:
        raise NotFoundError("Assessment not found.", code="ASSESSMENT_NOT_FOUND")
    if assessment.attempt_type == TYPE_PRACTICE:
        return load_questions(db, assessment_id)
    attempt = db.scalar(select(Attempt).where(Attempt.user_id == user.user_id, Attempt.assessment_id == assessment_id,
                                              Attempt.is_graded == True, Attempt.status == ATTEMPT_IN_PROGRESS))
    if attempt is None or utcnow() > attempt.deadline_at + timedelta(seconds=settings.SUBMIT_GRACE_SECONDS):
        raise ForbiddenError("Start the assessment to see its questions.", code="NO_ACTIVE_ATTEMPT")
    return load_questions(db, assessment_id)


# --------------------------------------------------------------------------- start
def start_attempt(db: Session, user: User, req: StartAttemptRequest) -> Attempt:
    """Validate every rule, then create the ``IN_PROGRESS`` attempt."""
    assessment = db.get(Assessment, req.assessment_id)
    if assessment is None:
        raise NotFoundError("Assessment not found.", code="ASSESSMENT_NOT_FOUND")
    if assessment.attempt_type != TYPE_GRADED:
        raise BadRequestError("Practice assessments do not use attempts.", code="NOT_GRADED")

    ack = req.acknowledgments
    if not (ack.no_minimize and ack.consent_camera and ack.single_attempt):
        raise UnprocessableError("You must accept all rules before starting.", code="ACKNOWLEDGMENT_REQUIRED")
    if not (assessment.min_duration_minutes <= req.chosen_duration_minutes <= assessment.default_duration_minutes):
        raise UnprocessableError(
            f"Duration must be between {assessment.min_duration_minutes} and {assessment.default_duration_minutes} minutes.",
            code="INVALID_DURATION",
            details={"min": assessment.min_duration_minutes, "max": assessment.default_duration_minutes})

    existing = db.scalar(select(Attempt).where(Attempt.user_id == user.user_id,
                                               Attempt.assessment_id == assessment.assessment_id,
                                               Attempt.is_graded == True))
    if existing is not None:
        raise ConflictError("You have already attempted this assessment.", code="ATTEMPT_EXISTS",
                            details={"attempt_id": existing.attempt_id, "status": existing.status})

    if user.role != ROLE_ADMIN:
        course = getattr(assessment, "course", None) or db.get(Course, assessment.course_id)
        if course is not None:
            c_status, prev_title, _ = catalog_service.course_lock_status(db, user.user_id, course)
            if c_status == LOCK_LOCKED:
                raise ForbiddenError(
                    f"Complete {prev_title or 'the previous course'} before starting this course.",
                    code="COURSE_LOCKED",
                    details={"previous_course": prev_title},
                )

    if catalog_service.lock_status_for(db, user.user_id, assessment) == LOCK_LOCKED:
        raise ForbiddenError("Complete the previous assessment to unlock this one.", code="ASSESSMENT_LOCKED")
    if not load_questions(db, assessment.assessment_id):
        raise ConflictError("This assessment has no questions yet.", code="NO_QUESTIONS")

    now = utcnow()
    attempt = Attempt(
        user_id=user.user_id, assessment_id=assessment.assessment_id, status=ATTEMPT_IN_PROGRESS,
        chosen_duration_minutes=req.chosen_duration_minutes,
        default_duration_minutes=assessment.default_duration_minutes,
        started_at=now, deadline_at=now + timedelta(minutes=req.chosen_duration_minutes),
        malpractice_count=0, extended_duration=False, is_graded=True, created_at=now,
    )
    db.add(attempt)
    catalog_service.ensure_enrolled(db, user.user_id, assessment.course_id)
    try:
        db.commit()  # the filtered unique index UX_Attempts_User_Assessment_Graded is the final guard
    except IntegrityError:
        db.rollback()
        raise ConflictError("You have already attempted this assessment.", code="ATTEMPT_EXISTS") from None
    db.refresh(attempt)

    ws_manager.publish_admin({"type": "STUDENT_STARTED", "attempt_id": attempt.attempt_id,
                              "user_email": user.email, "assessment": assessment.title})
    return attempt


# --------------------------------------------------------------------------- answers
def _upsert_answer(db: Session, attempt_id: int, question_id: int, selected: Optional[int],
                   marked: Optional[bool]) -> Answer:
    """Insert or update the single (attempt, question) answer row; safe under concurrent writes."""
    def fetch() -> Optional[Answer]:
        return db.scalar(select(Answer).where(Answer.attempt_id == attempt_id, Answer.question_id == question_id))

    row = fetch()
    if row is None:
        try:
            with db.begin_nested():  # SAVEPOINT so a unique-key race does not poison the transaction
                row = Answer(attempt_id=attempt_id, question_id=question_id, selected_index=selected,
                             marked_for_review=bool(marked), updated_at=utcnow())
                db.add(row)
                db.flush()
            return row
        except IntegrityError:
            row = fetch()
            if row is None:
                raise
    row.selected_index = selected
    if marked is not None:
        row.marked_for_review = marked
    row.updated_at = utcnow()
    return row


def save_answer(db: Session, user: User, attempt_id: int, *, question_id: int, selected_index: Optional[int],
                marked_for_review: bool) -> Answer:
    """Autosave one answer. Requires: owner, IN_PROGRESS, and now < deadline (+ small network grace)."""
    attempt = get_attempt(db, attempt_id, user_id=user.user_id)
    _require_active(attempt)
    if utcnow() > attempt.deadline_at + timedelta(seconds=settings.ANSWER_GRACE_SECONDS):
        raise ConflictError("Time is up for this attempt.", code="ATTEMPT_EXPIRED")
    belongs = db.scalar(select(Question.question_id).where(Question.question_id == question_id,
                                                           Question.assessment_id == attempt.assessment_id))
    if belongs is None:
        raise NotFoundError("Question does not belong to this assessment.", code="QUESTION_NOT_FOUND")
    row = _upsert_answer(db, attempt.attempt_id, question_id, selected_index, marked_for_review)
    db.commit()
    return row


# --------------------------------------------------------------------------- malpractice
def record_malpractice(db: Session, user: User, attempt_id: int, mtype: str, metadata: Optional[dict[str, Any]]
                       ) -> tuple[int, bool]:
    """Log one violation, bump the counter, and auto-submit (FLAGGED) once the strike limit is reached.

    Returns ``(malpractice_count, should_terminate)``.
    """
    attempt = get_attempt(db, attempt_id, user_id=user.user_id, lock=True)
    _require_active(attempt)

    now = utcnow()
    db.add(MalpracticeLog(attempt_id=attempt.attempt_id, type=mtype, occurred_at=now,
                          metadata_json=json.dumps(metadata, default=str) if metadata else None))
    attempt.malpractice_count = (attempt.malpractice_count or 0) + 1  # row is locked => safe read-modify-write
    count = attempt.malpractice_count
    terminate = malpractice_should_terminate(count, settings.MAX_MALPRACTICE)
    if terminate:
        finalize_attempt(db, attempt, status=ATTEMPT_FLAGGED, now=now)
    db.commit()

    ws_manager.publish_admin({"type": "MALPRACTICE_ALERT", "attempt_id": attempt.attempt_id, "user_email": user.email,
                              "count": count, "latest_type": mtype, "terminated": terminate})
    if terminate:
        _publish_submitted(attempt, user.email)
    return count, terminate


# --------------------------------------------------------------------------- extension
def extend_attempt(db: Session, user: User, attempt_id: int) -> Attempt:
    """One-time extension from the chosen duration up to the assessment's default duration."""
    attempt = get_attempt(db, attempt_id, user_id=user.user_id, lock=True)
    _require_active(attempt)
    if attempt.extended_duration:
        raise ConflictError("The extension has already been used.", code="EXTENSION_ALREADY_USED")

    now = utcnow()
    chosen_end = attempt.started_at + timedelta(minutes=attempt.chosen_duration_minutes)
    default_end = attempt.started_at + timedelta(minutes=attempt.default_duration_minutes)
    if now + timedelta(seconds=settings.EXTEND_TOLERANCE_SECONDS) < chosen_end:
        raise ConflictError("Your chosen time has not ended yet.", code="EXTENSION_TOO_EARLY")
    if attempt.chosen_duration_minutes >= attempt.default_duration_minutes or now >= default_end:
        raise ConflictError("No extra time is available.", code="EXTENSION_NOT_AVAILABLE")

    attempt.extended_duration = True
    attempt.deadline_at = default_end
    db.commit()
    return attempt


# --------------------------------------------------------------------------- finalise
def finalize_attempt(db: Session, attempt: Attempt, *, status: str, now=None,
                     answers: Optional[list[SubmitAnswer]] = None) -> Attempt:
    """Score, rank and close an attempt. Does **not** commit (the caller owns the transaction).

    1. persist any last answers (only if within the submit grace window)
    2. score = number of correct answers; percentage = score / total * 100
    3. time taken is measured server-side and capped at the deadline
    4. rank = COUNT(*)+1 of finished attempts with a higher score (or equal score and less time)
    5. motivational message from the percentage
    """
    now = now or utcnow()
    questions = load_questions(db, attempt.assessment_id)
    valid_ids = {q.question_id for q in questions}

    if answers and now <= attempt.deadline_at + timedelta(seconds=settings.SUBMIT_GRACE_SECONDS):
        for a in answers:
            if a.question_id in valid_ids:
                _upsert_answer(db, attempt.attempt_id, a.question_id, a.selected_index, None)
        db.flush()

    saved = {row.question_id: row.selected_index
             for row in db.scalars(select(Answer).where(Answer.attempt_id == attempt.attempt_id))}
    score, total = compute_score({q.question_id: q.correct_index for q in questions}, saved)
    pct = compute_percentage(score, total)

    end = min(now, attempt.deadline_at)
    time_taken = max(0, int((end - attempt.started_at).total_seconds()))

    attempt.status = status
    attempt.submitted_at = end
    attempt.time_taken_sec = time_taken
    attempt.score, attempt.total, attempt.percentage = score, total, pct
    attempt.rank_position = rank_service.compute_rank(db, attempt.assessment_id, score, time_taken)
    attempt.motivational_message = get_motivation(float(pct))
    db.flush()
    catalog_service.mark_course_completed_if_done(db, attempt.user_id, attempt.assessment.course_id)
    return attempt


def _publish_submitted(attempt: Attempt, user_email: str) -> None:
    ws_manager.publish_admin({"type": "ATTEMPT_SUBMITTED", "attempt_id": attempt.attempt_id, "user_email": user_email,
                              "score": attempt.score, "percentage": float(attempt.percentage or 0),
                              "status": attempt.status})


def submit_attempt(db: Session, user: User, attempt_id: int, answers: list[SubmitAnswer], auto: bool) -> Attempt:
    """Finish an attempt. Idempotent - a finished attempt is returned unchanged."""
    attempt = get_attempt(db, attempt_id, user_id=user.user_id, lock=True)
    if attempt.status != ATTEMPT_IN_PROGRESS:
        db.rollback()  # release the row lock
        return attempt
    finalize_attempt(db, attempt, status=ATTEMPT_AUTO_SUBMITTED if auto else ATTEMPT_SUBMITTED, answers=answers)
    db.commit()
    _publish_submitted(attempt, user.email)
    return attempt


def force_submit(db: Session, attempt_id: int) -> Attempt:
    """Admin action: close a running attempt using the answers saved so far. Does not commit."""
    attempt = get_attempt(db, attempt_id, lock=True)
    _require_active(attempt)
    return finalize_attempt(db, attempt, status=ATTEMPT_AUTO_SUBMITTED)


def auto_submit_expired(db: Session, *, limit: int = 200) -> int:
    """Close attempts whose student vanished (closed the tab, lost power). Runs from a background task.

    The cut-off is ``StartedAt + DefaultDuration + grace`` so nobody is closed while the extension
    dialog could still be open. Score uses the answers autosaved so far; time taken is capped at the deadline.
    """
    now = utcnow()
    grace = timedelta(seconds=settings.SWEEPER_GRACE_SECONDS)
    candidates = list(db.scalars(
        select(Attempt).where(Attempt.status == ATTEMPT_IN_PROGRESS, Attempt.deadline_at < now - grace).limit(limit)))
    closed = 0
    for cand in candidates:
        if cand.started_at + timedelta(minutes=cand.default_duration_minutes) + grace >= now:
            continue
        try:
            attempt = get_attempt(db, cand.attempt_id, lock=True)
            if attempt.status != ATTEMPT_IN_PROGRESS:
                db.rollback()
                continue
            finalize_attempt(db, attempt, status=ATTEMPT_AUTO_SUBMITTED, now=now)
            db.commit()
            closed += 1
            _publish_submitted(attempt, attempt.user.email)
        except Exception:  # noqa: BLE001 - one bad row must not stop the sweep
            db.rollback()
            logger.exception("Auto-submit failed for attempt %s", cand.attempt_id)
    return closed


# --------------------------------------------------------------------------- result
def build_result(db: Session, attempt: Attempt, *, is_admin: bool = False) -> dict[str, Any]:
    """Full result payload: score, live rank, solutions and proctoring snapshots (admin only)."""
    if attempt.status not in FINAL_STATUSES:
        raise ForbiddenError("Results are available after you submit.", code="RESULT_NOT_AVAILABLE")

    assessment = attempt.assessment
    course = db.get(Course, assessment.course_id) if assessment and assessment.course_id else None
    questions = load_questions(db, attempt.assessment_id)
    answers = {a.question_id: a for a in db.scalars(select(Answer).where(Answer.attempt_id == attempt.attempt_id))}
    snapshots_list = []
    if is_admin:
        snapshots = list(db.scalars(select(ProctoringSnapshot).where(ProctoringSnapshot.attempt_id == attempt.attempt_id)
                                    .order_by(ProctoringSnapshot.captured_at)))
        snapshots_list = [{"snapshot_id": s.snapshot_id, "image_url": signed_snapshot_url(s.snapshot_id),
                           "captured_at": s.captured_at, "trigger_type": s.trigger_type} for s in snapshots]
    pct = float(attempt.percentage or 0)
    live_rank = rank_service.compute_rank(db, attempt.assessment_id, attempt.score or 0, attempt.time_taken_sec)

    result_questions = []
    for q in questions:
        sel = answers[q.question_id].selected_index if q.question_id in answers else None
        result_questions.append({
            "question_id": q.question_id, "question_text": q.question_text, "options": q.options,
            "question_text_ta": getattr(q, "question_text_ta", None),
            "options_ta": getattr(q, "options_ta", None),
            "correct_index": q.correct_index, "selected_index": sel, "explanation": q.explanation,
            "explanation_ta": getattr(q, "explanation_ta", None),
            "is_correct": sel is not None and sel == q.correct_index, "topic": q.topic,
        })
    return {
        "attempt": {
            "attempt_id": attempt.attempt_id, "assessment_id": attempt.assessment_id,
            "assessment_title": assessment.title,
            "course_id": assessment.course_id if assessment else None,
            "course_slug": course.slug if course else None,
            "course_title": course.title if course else None,
            "status": attempt.status, "score": attempt.score or 0,
            "total": attempt.total or 0, "percentage": pct, "passed": is_passed(pct, assessment.pass_percentage),
            "pass_percentage": assessment.pass_percentage, "time_taken_sec": attempt.time_taken_sec or 0,
            "rank_position": live_rank, "total_participants": rank_service.total_participants(db, attempt.assessment_id),
            "malpractice_count": attempt.malpractice_count, "chosen_duration_minutes": attempt.chosen_duration_minutes,
            "submitted_at": attempt.submitted_at,
        },
        "motivational_message": attempt.motivational_message or get_motivation(pct),
        "questions": result_questions,
        "snapshots": snapshots_list,
    }


def delete_attempt_cascade(db: Session, attempt: Attempt) -> None:
    """Delete an attempt and everything hanging off it (admin reset). Does not commit."""
    aid = attempt.attempt_id
    db.execute(delete(Answer).where(Answer.attempt_id == aid))
    db.execute(delete(MalpracticeLog).where(MalpracticeLog.attempt_id == aid))
    db.execute(delete(ProctoringSnapshot).where(ProctoringSnapshot.attempt_id == aid))
    db.delete(attempt)
