"""Ranking and leaderboard queries.

Ordering rule: higher score first; on equal score, less time taken first. Attempts that tie on both
share the same rank (competition ranking: 1, 2, 2, 4).
"""
from __future__ import annotations

from typing import Optional, Sequence

from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import Session

from app.core.constants import FINAL_STATUSES
from app.models import Attempt, User

_NO_TIME = 2**31 - 1  # treat a missing TimeTakenSec as "slowest"


def compute_rank(db: Session, assessment_id: int, score: int, time_taken_sec: Optional[int]) -> int:
    """``SELECT COUNT(*) + 1`` of finished attempts that beat ``(score, time)``."""
    my_time = _NO_TIME if time_taken_sec is None else time_taken_sec
    better = db.scalar(
        select(func.count()).select_from(Attempt).where(
            Attempt.assessment_id == assessment_id,
            Attempt.status.in_(FINAL_STATUSES),
            or_(Attempt.score > score, and_(Attempt.score == score, Attempt.time_taken_sec < my_time)),
        )
    )
    return int(better or 0) + 1


def total_participants(db: Session, assessment_id: int) -> int:
    return int(db.scalar(
        select(func.count()).select_from(Attempt).where(
            Attempt.assessment_id == assessment_id, Attempt.status.in_(FINAL_STATUSES))
    ) or 0)


def rank_rows(rows: Sequence[tuple[int, int]]) -> list[int]:
    """Competition-rank an already sorted list of ``(score, time)`` pairs. Pure helper."""
    ranks: list[int] = []
    for i, row in enumerate(rows):
        ranks.append(ranks[-1] if i and rows[i - 1] == row else i + 1)
    return ranks


def leaderboard(db: Session, assessment_id: int, *, limit: int = 50, viewer_id: Optional[int] = None) -> dict:
    """Top ``limit`` finished attempts plus the viewer's own standing (if they finished)."""
    stmt = (
        select(Attempt, User.name)
        .join(User, User.user_id == Attempt.user_id)
        .where(Attempt.assessment_id == assessment_id, Attempt.status.in_(FINAL_STATUSES))
        .order_by(Attempt.score.desc(), Attempt.time_taken_sec.asc(), Attempt.attempt_id.asc())
        .limit(limit)
    )
    rows = db.execute(stmt).all()
    ranks = rank_rows([(a.score or 0, a.time_taken_sec or 0) for a, _ in rows])

    def entry(a: Attempt, name: str, rank: int) -> dict:
        return {"rank": rank, "name": name, "score": a.score or 0, "total": a.total or 0,
                "percentage": float(a.percentage or 0), "time_taken_sec": a.time_taken_sec or 0,
                "is_me": viewer_id is not None and a.user_id == viewer_id}

    entries = [entry(a, n, r) for (a, n), r in zip(rows, ranks)]
    me = next((e for e in entries if e["is_me"]), None)
    if me is None and viewer_id is not None:
        mine = db.execute(
            select(Attempt, User.name).join(User, User.user_id == Attempt.user_id).where(
                Attempt.assessment_id == assessment_id, Attempt.user_id == viewer_id,
                Attempt.status.in_(FINAL_STATUSES))
        ).first()
        if mine:
            a, n = mine
            me = entry(a, n, compute_rank(db, assessment_id, a.score or 0, a.time_taken_sec))
    return {"assessment_id": assessment_id, "total_participants": total_participants(db, assessment_id),
            "entries": entries, "me": me}


def refresh_stored_ranks(db: Session, assessment_id: int) -> int:
    """Recompute ``Attempts.RankPosition`` for every finished attempt (stored ranks go stale as
    other students finish). Returns the number of rows updated. Caller commits."""
    attempts = list(db.scalars(
        select(Attempt).where(Attempt.assessment_id == assessment_id, Attempt.status.in_(FINAL_STATUSES))
        .order_by(Attempt.score.desc(), Attempt.time_taken_sec.asc(), Attempt.attempt_id.asc())
    ))
    ranks = rank_rows([(a.score or 0, a.time_taken_sec or 0) for a in attempts])
    for a, r in zip(attempts, ranks):
        a.rank_position = r
    return len(attempts)
