"""Schemas for student course reflections and admin review."""
from __future__ import annotations

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ReflectionAnswerItem(BaseModel):
    question_number: int
    question: str
    selected_option: str


class SubmitReflectionRequest(BaseModel):
    answers: list[ReflectionAnswerItem]


class ReflectionResponse(BaseModel):
    course_id: int
    course_slug: str
    course_title: str
    submitted: bool
    submitted_at: Optional[datetime] = None
    answers: list[ReflectionAnswerItem] = []


class UserCourseReflection(BaseModel):
    course_id: int
    course_slug: str
    course_title: str
    submitted_at: datetime
    updated_at: datetime
    answers: list[ReflectionAnswerItem]


class AdminUserReflectionSummary(BaseModel):
    user_id: int
    name: str
    email: str
    total_reflections: int
    latest_submitted_at: Optional[datetime] = None
    courses: list[UserCourseReflection]
