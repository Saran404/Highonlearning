"""``Assessments`` table."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, ForeignKey, Integer, Unicode, UnicodeText
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import DT, Base
from app.utils.time import utcnow


class Assessment(Base):
    __tablename__ = "Assessments"

    assessment_id: Mapped[int] = mapped_column("AssessmentId", Integer, primary_key=True, autoincrement=True)
    course_id: Mapped[int] = mapped_column("CourseId", Integer, ForeignKey("Courses.CourseId"))
    title: Mapped[str] = mapped_column("Title", Unicode(200))
    title_ta: Mapped[Optional[str]] = mapped_column("TitleTa", Unicode(200), nullable=True)
    slug: Mapped[str] = mapped_column("Slug", Unicode(200), unique=True)
    description: Mapped[Optional[str]] = mapped_column("Description", UnicodeText, nullable=True)
    description_ta: Mapped[Optional[str]] = mapped_column("DescriptionTa", UnicodeText, nullable=True)
    topic: Mapped[Optional[str]] = mapped_column("Topic", Unicode(100), nullable=True)
    difficulty: Mapped[Optional[str]] = mapped_column("Difficulty", Unicode(20), nullable=True)
    default_duration_minutes: Mapped[int] = mapped_column("DefaultDurationMinutes", Integer, default=60)
    min_duration_minutes: Mapped[int] = mapped_column("MinDurationMinutes", Integer, default=20)
    total_questions: Mapped[int] = mapped_column("TotalQuestions", Integer, default=30)
    pass_percentage: Mapped[int] = mapped_column("PassPercentage", Integer, default=60)
    attempt_type: Mapped[str] = mapped_column("AttemptType", Unicode(20), default="GRADED")
    sequential_unlock: Mapped[bool] = mapped_column("SequentialUnlock", Boolean, default=True)
    lockdown_enabled: Mapped[bool] = mapped_column("LockdownEnabled", Boolean, default=True)
    proctoring_enabled: Mapped[bool] = mapped_column("ProctoringEnabled", Boolean, default=True)
    order_index: Mapped[int] = mapped_column("OrderIndex", Integer, default=0)
    created_at: Mapped[datetime] = mapped_column("CreatedAt", DT, default=utcnow)
