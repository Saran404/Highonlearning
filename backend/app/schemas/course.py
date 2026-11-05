"""Course schemas."""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from app.schemas.common import UTCDatetime


class CourseOut(BaseModel):
    id: int
    title: str
    slug: str
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    order_index: int
    graded_count: int = 0
    practice_count: int = 0
    completed_count: int = 0
    enrolled: bool = False
    lock_status: str = "AVAILABLE"
    previous_course_title: Optional[str] = None
    previous_course_slug: Optional[str] = None
    created_at: UTCDatetime
