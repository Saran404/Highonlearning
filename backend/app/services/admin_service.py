"""Admin operations. Every mutation writes an AuditLogs row in the same transaction."""
from __future__ import annotations

import json
from datetime import timedelta
from typing import Any, Optional
import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import settings
from app.core.constants import ATTEMPT_IN_PROGRESS, FINAL_STATUSES, ROLE_STUDENT
from app.core.exceptions import ConflictError, NotFoundError
from app.core.websocket_manager import ws_manager
from app.models import (ActiveSession, Answer, Assessment, Attempt, MalpracticeLog, Question, User)
from app.schemas.admin import (AdminAnswer, AlertRow, AttemptDrilldown, AttemptRow, LiveAttemptRow, MalpracticeOut,
                               StudentRow)
from app.services import attempt_service, audit_service, proctoring_service, rank_service, session_service
from app.utils import storage
from app.utils.time import utcnow


def attempt_row(a: Attempt) -> AttemptRow:
    return AttemptRow(
        attempt_id=a.attempt_id, user_id=a.user_id, user_name=a.user.name, user_email=a.user.email,
        assessment_id=a.assessment_id, assessment_title=a.assessment.title, status=a.status,
        started_at=a.started_at, deadline_at=a.deadline_at, submitted_at=a.submitted_at, score=a.score, total=a.total,
        percentage=float(a.percentage) if a.percentage is not None else None, time_taken_sec=a.time_taken_sec,
        rank_position=a.rank_position, malpractice_count=a.malpractice_count)


def list_students(db: Session, *, search: Optional[str], page: int, page_size: int) -> tuple[list[StudentRow], int]:
    where = [User.role == ROLE_STUDENT]
    if search:
        like = f"%{search.strip().lower()}%"
        where.append(func.lower(User.email).like(like) | func.lower(User.name).like(like))
    total = int(db.scalar(select(func.count()).select_from(User).where(*where)) or 0)
    users = list(db.scalars(select(User).where(*where).order_by(User.created_at.desc())
                            .offset((page - 1) * page_size).limit(page_size)))
    ids = [u.user_id for u in users]
    cutoff = utcnow() - timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    seen: dict[int, Any] = {}
    if ids:
        for uid, last in db.execute(
            select(ActiveSession.user_id, func.max(ActiveSession.last_seen_at)).where(
                ActiveSession.user_id.in_(ids), ActiveSession.is_revoked == False,
                ActiveSession.last_seen_at >= cutoff).group_by(ActiveSession.user_id)):
            seen[uid] = last
    counts = dict(db.execute(select(Attempt.user_id, func.count()).where(Attempt.user_id.in_(ids))
                             .group_by(Attempt.user_id)).all()) if ids else {}
    rows = [StudentRow(id=u.user_id, name=u.name, email=u.email, is_active=u.is_active,
                       has_active_session=u.user_id in seen, last_seen_at=seen.get(u.user_id),
                       attempts_count=int(counts.get(u.user_id, 0)), created_at=u.created_at) for u in users]
    return rows, total


def list_attempts(db: Session, *, status: Optional[str], assessment_id: Optional[int], user_id: Optional[int],
                  page: int, page_size: int) -> tuple[list[AttemptRow], int]:
    where = []
    if status:
        where.append(Attempt.status == status)
    if assessment_id:
        where.append(Attempt.assessment_id == assessment_id)
    if user_id:
        where.append(Attempt.user_id == user_id)
    total = int(db.scalar(select(func.count()).select_from(Attempt).where(*where)) or 0)
    attempts = db.scalars(select(Attempt).where(*where).order_by(Attempt.started_at.desc())
                          .offset((page - 1) * page_size).limit(page_size))
    return [attempt_row(a) for a in attempts], total


def live_attempts(db: Session) -> list[LiveAttemptRow]:
    rows = db.scalars(select(Attempt).where(Attempt.status == ATTEMPT_IN_PROGRESS).order_by(Attempt.started_at))
    return [LiveAttemptRow(attempt_id=a.attempt_id, user_name=a.user.name, user_email=a.user.email,
                           assessment_title=a.assessment.title, started_at=a.started_at, deadline_at=a.deadline_at,
                           malpractice_count=a.malpractice_count) for a in rows]


def drilldown(db: Session, attempt_id: int) -> AttemptDrilldown:
    attempt = attempt_service.get_attempt(db, attempt_id)
    questions = {q.question_id: q for q in attempt_service.load_questions(db, attempt.assessment_id)}
    answers = {a.question_id: a for a in db.scalars(select(Answer).where(Answer.attempt_id == attempt_id))}
    admin_answers = []
    for qid, q in questions.items():
        ans = answers.get(qid)
        sel = ans.selected_index if ans else None
        admin_answers.append(AdminAnswer(question_id=qid, question_text=q.question_text, selected_index=sel,
                                         correct_index=q.correct_index, is_correct=sel is not None and sel == q.correct_index,
                                         marked_for_review=bool(ans and ans.marked_for_review)))
    logs = db.scalars(select(MalpracticeLog).where(MalpracticeLog.attempt_id == attempt_id).order_by(MalpracticeLog.occurred_at))
    return AttemptDrilldown(
        attempt=attempt_row(attempt), answers=admin_answers,
        malpractice_logs=[MalpracticeOut(log_id=l.log_id, type=l.type, occurred_at=l.occurred_at,
                                         metadata=json.loads(l.metadata_json) if l.metadata_json else None) for l in logs],
        snapshots=proctoring_service.list_snapshots(db, attempt_id))


def force_submit(db: Session, admin: User, attempt_id: int) -> AttemptRow:
    attempt = attempt_service.force_submit(db, attempt_id)
    audit_service.log_action(db, admin_id=admin.user_id, action="ATTEMPT_FORCE_SUBMIT", target_type="Attempt",
                             target_id=attempt_id, metadata={"user_id": attempt.user_id, "score": attempt.score})
    db.commit()
    attempt_service._publish_submitted(attempt, attempt.user.email)  # noqa: SLF001
    return attempt_row(attempt)


def reset_attempt(db: Session, admin: User, attempt_id: int) -> None:
    """Delete the attempt with its answers, malpractice logs and snapshots so the student can retake."""
    attempt = attempt_service.get_attempt(db, attempt_id, lock=True)
    meta = {"user_id": attempt.user_id, "assessment_id": attempt.assessment_id, "status": attempt.status,
            "score": attempt.score, "malpractice_count": attempt.malpractice_count}
    audit_service.log_action(db, admin_id=admin.user_id, action="ATTEMPT_RESET", target_type="Attempt",
                             target_id=attempt_id, metadata=meta)
    attempt_service.delete_attempt_cascade(db, attempt)
    db.commit()
    storage.delete_attempt_files(attempt_id)


def recent_alerts(db: Session, limit: int = 100) -> list[AlertRow]:
    stmt = (select(MalpracticeLog, Attempt, User, Assessment.title)
            .join(Attempt, Attempt.attempt_id == MalpracticeLog.attempt_id)
            .join(User, User.user_id == Attempt.user_id)
            .join(Assessment, Assessment.assessment_id == Attempt.assessment_id)
            .order_by(MalpracticeLog.occurred_at.desc()).limit(limit))
    return [AlertRow(log_id=l.log_id, attempt_id=a.attempt_id, user_email=u.email, user_name=u.name,
                     assessment_title=title, type=l.type, occurred_at=l.occurred_at,
                     malpractice_count=a.malpractice_count, attempt_status=a.status)
            for l, a, u, title in db.execute(stmt)]


def revoke_session(db: Session, admin: User, session_id: uuid.UUID) -> None:
    s = db.get(ActiveSession, session_id)
    if s is None:
        raise NotFoundError("Session not found.", code="SESSION_NOT_FOUND")
    if s.is_revoked:
        raise ConflictError("Session is already revoked.", code="ALREADY_REVOKED")
    session_service.revoke(db, s)
    audit_service.log_action(db, admin_id=admin.user_id, action="SESSION_REVOKE", target_type="Session",
                             target_id=str(session_id), metadata={"user_id": s.user_id, "device_id": s.device_id})
    db.commit()
    session_service.notify_revoked([s.device_id], "Your session was ended by an administrator")


def recompute_ranks(db: Session, admin: User, assessment_id: int) -> int:
    if db.get(Assessment, assessment_id) is None:
        raise NotFoundError("Assessment not found.", code="ASSESSMENT_NOT_FOUND")
    n = rank_service.refresh_stored_ranks(db, assessment_id)
    audit_service.log_action(db, admin_id=admin.user_id, action="RANKS_RECOMPUTE", target_type="Assessment",
                             target_id=assessment_id, metadata={"attempts": n})
    db.commit()
    return n
