"""``Attempts`` table - one row per graded attempt (practice never touches this table)."""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, Unicode
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import DT, BigIntPK, Base
from app.models.assessment import Assessment
from app.models.user import User
from app.utils.time import utcnow


class Attempt(Base):
    __tablename__ = "Attempts"

    attempt_id: Mapped[int] = mapped_column("AttemptId", BigIntPK, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column("UserId", Integer, ForeignKey("Users.UserId"))
    assessment_id: Mapped[int] = mapped_column("AssessmentId", Integer, ForeignKey("Assessments.AssessmentId"))
    status: Mapped[str] = mapped_column("Status", Unicode(20), default="IN_PROGRESS")
    chosen_duration_minutes: Mapped[int] = mapped_column("ChosenDurationMinutes", Integer)
    default_duration_minutes: Mapped[int] = mapped_column("DefaultDurationMinutes", Integer)
    started_at: Mapped[datetime] = mapped_column("StartedAt", DT)
    deadline_at: Mapped[datetime] = mapped_column("DeadlineAt", DT)
    submitted_at: Mapped[Optional[datetime]] = mapped_column("SubmittedAt", DT, nullable=True)
    time_taken_sec: Mapped[Optional[int]] = mapped_column("TimeTakenSec", Integer, nullable=True)
    score: Mapped[Optional[int]] = mapped_column("Score", Integer, nullable=True)
    total: Mapped[Optional[int]] = mapped_column("Total", Integer, nullable=True)
    percentage: Mapped[Optional[Decimal]] = mapped_column("Percentage", Numeric(5, 2), nullable=True)
    malpractice_count: Mapped[int] = mapped_column("MalpracticeCount", Integer, default=0)
    extended_duration: Mapped[bool] = mapped_column("ExtendedDuration", Boolean, default=False)
    rank_position: Mapped[Optional[int]] = mapped_column("RankPosition", Integer, nullable=True)
    motivational_message: Mapped[Optional[str]] = mapped_column("MotivationalMessage", Unicode(500), nullable=True)
    is_graded: Mapped[bool] = mapped_column("IsGraded", Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column("CreatedAt", DT, default=utcnow)

    user: Mapped[User] = relationship(User)
    assessment: Mapped[Assessment] = relationship(Assessment)
