"""``Enrollments`` table."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import DT, Base
from app.utils.time import utcnow


class Enrollment(Base):
    __tablename__ = "Enrollments"

    enrollment_id: Mapped[int] = mapped_column("EnrollmentId", Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column("UserId", Integer, ForeignKey("Users.UserId"))
    course_id: Mapped[int] = mapped_column("CourseId", Integer, ForeignKey("Courses.CourseId"))
    enrolled_at: Mapped[datetime] = mapped_column("EnrolledAt", DT, default=utcnow)
    completed_at: Mapped[Optional[datetime]] = mapped_column("CompletedAt", DT, nullable=True)
