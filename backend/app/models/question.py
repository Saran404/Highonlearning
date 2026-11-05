"""``Questions`` table."""
from __future__ import annotations

import json
from typing import Optional

from sqlalchemy import ForeignKey, Integer, Unicode, UnicodeText
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Question(Base):
    __tablename__ = "Questions"

    question_id: Mapped[int] = mapped_column("QuestionId", Integer, primary_key=True, autoincrement=True)
    assessment_id: Mapped[int] = mapped_column("AssessmentId", Integer, ForeignKey("Assessments.AssessmentId"))
    question_text: Mapped[str] = mapped_column("QuestionText", UnicodeText)
    options_json: Mapped[str] = mapped_column("OptionsJson", UnicodeText)
    correct_index: Mapped[int] = mapped_column("CorrectIndex", Integer)
    explanation: Mapped[Optional[str]] = mapped_column("Explanation", UnicodeText, nullable=True)
    question_text_ta: Mapped[Optional[str]] = mapped_column("QuestionTextTa", UnicodeText, nullable=True)
    options_json_ta: Mapped[Optional[str]] = mapped_column("OptionsJsonTa", UnicodeText, nullable=True)
    explanation_ta: Mapped[Optional[str]] = mapped_column("ExplanationTa", UnicodeText, nullable=True)
    topic: Mapped[Optional[str]] = mapped_column("Topic", Unicode(100), nullable=True)
    difficulty: Mapped[Optional[str]] = mapped_column("Difficulty", Unicode(20), nullable=True)
    order_index: Mapped[int] = mapped_column("OrderIndex", Integer, default=0)

    @property
    def options(self) -> list[str]:
        """Decoded ``OptionsJson`` (a JSON array of 4 strings)."""
        return [str(o) for o in json.loads(self.options_json)]

    @property
    def options_ta(self) -> list[str] | None:
        """Decoded ``OptionsJsonTa`` (a JSON array of 4 strings)."""
        if not self.options_json_ta:
            return None
        try:
            return [str(o) for o in json.loads(self.options_json_ta)]
        except Exception:
            return None
