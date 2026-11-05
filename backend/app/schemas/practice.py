from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class PracticeAnswerRequest(BaseModel):
    question_id: int
    selected_index: int = Field(ge=0, le=3)


class PracticeAnswerResponse(BaseModel):
    correct: bool
    correct_index: int
    explanation: str
    explanation_ta: Optional[str] = None
    selected_index: int
