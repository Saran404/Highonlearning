"""Admin schemas."""
from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel

from app.schemas.common import UTCDatetime
from app.schemas.proctoring import SnapshotOut


class StudentRow(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool
    has_active_session: bool
    last_seen_at: Optional[UTCDatetime] = None
    attempts_count: int = 0
    created_at: UTCDatetime


class AttemptRow(BaseModel):
    attempt_id: int
    user_id: int
    user_name: str
    user_email: str
    assessment_id: int
    assessment_title: str
    status: str
    started_at: UTCDatetime
    deadline_at: UTCDatetime
    submitted_at: Optional[UTCDatetime] = None
    score: Optional[int] = None
    total: Optional[int] = None
    percentage: Optional[float] = None
    time_taken_sec: Optional[int] = None
    rank_position: Optional[int] = None
    malpractice_count: int


class AdminAnswer(BaseModel):
    question_id: int
    question_text: str
    selected_index: Optional[int] = None
    correct_index: int
    is_correct: bool
    marked_for_review: bool


class MalpracticeOut(BaseModel):
    log_id: int
    type: str
    occurred_at: UTCDatetime
    metadata: Optional[Any] = None


class AttemptDrilldown(BaseModel):
    attempt: AttemptRow
    answers: list[AdminAnswer]
    malpractice_logs: list[MalpracticeOut]
    snapshots: list[SnapshotOut]


class AlertRow(BaseModel):
    log_id: int
    attempt_id: int
    user_email: str
    user_name: str
    assessment_title: str
    type: str
    occurred_at: UTCDatetime
    malpractice_count: int
    attempt_status: str


class LiveAttemptRow(BaseModel):
    attempt_id: int
    user_name: str
    user_email: str
    assessment_title: str
    started_at: UTCDatetime
    deadline_at: UTCDatetime
    malpractice_count: int
