"""``CourseReflections`` table."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey, Integer, UnicodeText, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import DT, Base
from app.utils.time import utcnow


class CourseReflection(Base):
    __tablename__ = "CourseReflections"
    __table_args__ = (
        UniqueConstraint("UserId", "CourseId", name="UQ_CourseReflections_User_Course"),
    )

    reflection_id: Mapped[int] = mapped_column("ReflectionId", Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column("UserId", Integer, ForeignKey("Users.UserId", ondelete="CASCADE"))
    course_id: Mapped[int] = mapped_column("CourseId", Integer, ForeignKey("Courses.CourseId", ondelete="CASCADE"))
    answers_json: Mapped[str] = mapped_column("AnswersJson", UnicodeText)
    created_at: Mapped[datetime] = mapped_column("CreatedAt", DT, default=utcnow)
    updated_at: Mapped[datetime] = mapped_column("UpdatedAt", DT, default=utcnow, onupdate=utcnow)

    user = relationship("User", backref="course_reflections")
    course = relationship("Course", backref="reflections")
