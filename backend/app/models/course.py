"""``Courses`` table."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, Unicode, UnicodeText
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import DT, Base
from app.utils.time import utcnow


class Course(Base):
    __tablename__ = "Courses"

    course_id: Mapped[int] = mapped_column("CourseId", Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column("Title", Unicode(200))
    slug: Mapped[str] = mapped_column("Slug", Unicode(200), unique=True)
    description: Mapped[Optional[str]] = mapped_column("Description", UnicodeText, nullable=True)
    thumbnail_url: Mapped[Optional[str]] = mapped_column("ThumbnailUrl", Unicode(500), nullable=True)
    order_index: Mapped[int] = mapped_column("OrderIndex", Integer, default=0)
    created_at: Mapped[datetime] = mapped_column("CreatedAt", DT, default=utcnow)
