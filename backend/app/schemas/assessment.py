"""Assessment and question schemas."""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from app.models import Assessment, Question


class AssessmentOut(BaseModel):
    """Assessment metadata - never includes questions."""

    id: int
    course_id: int
    title: str
    slug: str
    description: Optional[str] = None
    topic: Optional[str] = None
    difficulty: Optional[str] = None
    default_duration_minutes: int
    min_duration_minutes: int
    total_questions: int
    pass_percentage: int
    title_ta: Optional[str] = None
    description_ta: Optional[str] = None
    attempt_type: str
    sequential_unlock: bool
    lockdown_enabled: bool
    proctoring_enabled: bool
    order_index: int

    @classmethod
    def from_model(cls, a: Assessment) -> "AssessmentOut":
        return cls(id=a.assessment_id, course_id=a.course_id, title=a.title,
                   title_ta=getattr(a, "title_ta", None),
                   slug=a.slug, description=a.description,
                   description_ta=getattr(a, "description_ta", None),
                   topic=a.topic, difficulty=a.difficulty, default_duration_minutes=a.default_duration_minutes,
                   min_duration_minutes=a.min_duration_minutes, total_questions=a.total_questions,
                   pass_percentage=a.pass_percentage, attempt_type=a.attempt_type,
                   sequential_unlock=a.sequential_unlock, lockdown_enabled=a.lockdown_enabled,
                   proctoring_enabled=a.proctoring_enabled, order_index=a.order_index)


class AssessmentListItem(AssessmentOut):
    """Assessment + the current student's state (lock status, score, rank)."""

    lock_status: str
    attempt_id: Optional[int] = None
    score: Optional[int] = None
    total: Optional[int] = None
    percentage: Optional[float] = None
    time_taken_sec: Optional[int] = None
    rank_position: Optional[int] = None
    total_participants: Optional[int] = None
    course_slug: Optional[str] = None
    course_title: Optional[str] = None


class QuestionPublic(BaseModel):
    """A question as shown during an exam - the correct answer is never included."""

    id: int
    text: str
    options: list[str]
    text_ta: Optional[str] = None
    options_ta: Optional[list[str]] = None
    topic: Optional[str] = None
    difficulty: Optional[str] = None

    @classmethod
    def from_model(cls, q: Question) -> "QuestionPublic":
        return cls(id=q.question_id, text=q.question_text, options=q.options,
                   text_ta=getattr(q, "question_text_ta", None),
                   options_ta=getattr(q, "options_ta", None),
                   topic=q.topic, difficulty=q.difficulty)


class LeaderboardEntry(BaseModel):
    rank: int
    name: str
    score: int
    total: int
    percentage: float
    time_taken_sec: int
    is_me: bool = False


class LeaderboardResponse(BaseModel):
    assessment_id: int
    total_participants: int
    entries: list[LeaderboardEntry]
    me: Optional[LeaderboardEntry] = None
