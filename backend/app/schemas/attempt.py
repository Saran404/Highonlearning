"""Attempt engine schemas."""
from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field

from app.core.constants import MalpracticeType
from app.schemas.assessment import QuestionPublic
from app.schemas.common import UTCDatetime


class Acknowledgments(BaseModel):
    no_minimize: bool = False
    consent_camera: bool = False
    single_attempt: bool = False


class StartAttemptRequest(BaseModel):
    assessment_id: int
    chosen_duration_minutes: int = Field(gt=0)
    acknowledgments: Acknowledgments


class SavedAnswer(BaseModel):
    question_id: int
    selected_index: Optional[int] = None
    marked_for_review: bool = False


class AttemptState(BaseModel):
    """Returned when an attempt starts and when it is resumed."""

    attempt_id: int
    assessment_id: int
    assessment_title: str
    status: str
    questions: list[QuestionPublic]
    saved_answers: list[SavedAnswer] = []
    started_at: UTCDatetime
    deadline_at: UTCDatetime
    server_time: UTCDatetime
    default_duration_minutes: int
    chosen_duration_minutes: int
    extended: bool = False
    malpractice_count: int = 0
    max_malpractice: int
    lockdown_enabled: bool = True
    proctoring_enabled: bool = True


class AnswerRequest(BaseModel):
    question_id: int
    selected_index: Optional[int] = Field(default=None, ge=0, le=3)
    marked_for_review: bool = False


class AnswerResponse(BaseModel):
    ok: bool = True
    saved_at: UTCDatetime


class MalpracticeRequest(BaseModel):
    type: MalpracticeType
    metadata: Optional[dict[str, Any]] = None


class MalpracticeResponse(BaseModel):
    malpractice_count: int
    should_terminate: bool
    max_malpractice: int


class ExtendResponse(BaseModel):
    deadline_at: UTCDatetime
    extended: bool = True


class SubmitAnswer(BaseModel):
    question_id: int
    selected_index: Optional[int] = Field(default=None, ge=0, le=3)


class SubmitRequest(BaseModel):
    answers: list[SubmitAnswer] = []
    time_taken_sec: Optional[int] = Field(default=None, ge=0, description="Informational only; the server measures time itself.")
    auto: bool = False


class ResultAttempt(BaseModel):
    attempt_id: int
    assessment_id: int
    assessment_title: str
    course_id: Optional[int] = None
    course_slug: Optional[str] = None
    course_title: Optional[str] = None
    status: str
    score: int
    total: int
    percentage: float
    passed: bool
    pass_percentage: int
    time_taken_sec: int
    rank_position: Optional[int] = None
    total_participants: int = 0
    malpractice_count: int
    chosen_duration_minutes: int
    submitted_at: Optional[UTCDatetime] = None


class ResultQuestion(BaseModel):
    question_id: int
    question_text: str
    options: list[str]
    question_text_ta: Optional[str] = None
    options_ta: Optional[list[str]] = None
    correct_index: int
    selected_index: Optional[int] = None
    explanation: Optional[str] = None
    explanation_ta: Optional[str] = None
    is_correct: bool
    topic: Optional[str] = None


class ResultSnapshot(BaseModel):
    snapshot_id: int
    image_url: str
    captured_at: UTCDatetime
    trigger_type: str


class ResultResponse(BaseModel):
    attempt: ResultAttempt
    motivational_message: str
    questions: list[ResultQuestion]
    snapshots: list[ResultSnapshot]
