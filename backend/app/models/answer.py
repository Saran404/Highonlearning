"""``Answers`` table - unique on (AttemptId, QuestionId)."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import DT, BigIntPK, Base
from app.utils.time import utcnow


class Answer(Base):
    __tablename__ = "Answers"
    __table_args__ = (UniqueConstraint("AttemptId", "QuestionId", name="UQ_Answers_Attempt_Question"),)

    answer_id: Mapped[int] = mapped_column("AnswerId", BigIntPK, primary_key=True, autoincrement=True)
    attempt_id: Mapped[int] = mapped_column("AttemptId", BigIntPK, ForeignKey("Attempts.AttemptId", ondelete="CASCADE"))
    question_id: Mapped[int] = mapped_column("QuestionId", Integer, ForeignKey("Questions.QuestionId"))
    selected_index: Mapped[Optional[int]] = mapped_column("SelectedIndex", Integer, nullable=True)
    marked_for_review: Mapped[bool] = mapped_column("MarkedForReview", Boolean, default=False)
    updated_at: Mapped[datetime] = mapped_column("UpdatedAt", DT, default=utcnow, onupdate=utcnow)
