"""Reflective Activity service layer: submission, retrieval and admin drilldown."""
from __future__ import annotations

import json
from datetime import datetime
from typing import Optional

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models import Course, CourseReflection, User
from app.schemas.reflection import (
    AdminUserReflectionSummary,
    ReflectionAnswerItem,
    ReflectionResponse,
    UserCourseReflection,
)
from app.utils.time import utcnow


def get_course_by_slug(db: Session, slug: str) -> Course:
    course = db.scalar(select(Course).where(Course.slug == slug))
    if course is None:
        raise NotFoundError("Course not found.", code="COURSE_NOT_FOUND")
    return course


def get_user_course_reflection(db: Session, user_id: int, course_slug: str) -> ReflectionResponse:
    course = get_course_by_slug(db, course_slug)
    try:
        row = db.scalar(
            select(CourseReflection).where(
                CourseReflection.user_id == user_id,
                CourseReflection.course_id == course.course_id,
            )
        )
    except Exception:
        db.rollback()
        row = None
    if row is None:
        return ReflectionResponse(
            course_id=course.course_id,
            course_slug=course.slug,
            course_title=course.title,
            submitted=False,
            submitted_at=None,
            answers=[],
        )

    answers_raw = json.loads(row.answers_json) if row.answers_json else []
    answers = [ReflectionAnswerItem(**a) for a in answers_raw]
    return ReflectionResponse(
        course_id=course.course_id,
        course_slug=course.slug,
        course_title=course.title,
        submitted=True,
        submitted_at=row.created_at,
        answers=answers,
    )


def save_user_course_reflection(
    db: Session, user_id: int, course_slug: str, answers: list[ReflectionAnswerItem]
) -> ReflectionResponse:
    course = get_course_by_slug(db, course_slug)
    now = utcnow()
    dumped_json = json.dumps([a.model_dump() for a in answers], ensure_ascii=False)

    row = db.scalar(
        select(CourseReflection).where(
            CourseReflection.user_id == user_id,
            CourseReflection.course_id == course.course_id,
        )
    )
    if row is not None:
        row.answers_json = dumped_json
        row.updated_at = now
    else:
        row = CourseReflection(
            user_id=user_id,
            course_id=course.course_id,
            answers_json=dumped_json,
            created_at=now,
            updated_at=now,
        )
        db.add(row)
        db.flush()

    # Automatically check and mark course completion if all graded tests + reflection are done
    from app.services import catalog_service
    catalog_service.mark_course_completed_if_done(db, user_id, course.course_id)

    db.commit()
    db.refresh(row)

    return ReflectionResponse(
        course_id=course.course_id,
        course_slug=course.slug,
        course_title=course.title,
        submitted=True,
        submitted_at=row.created_at,
        answers=answers,
    )


def list_admin_reflections(db: Session, search: Optional[str] = None) -> list[AdminUserReflectionSummary]:
    stmt = (
        select(CourseReflection, User, Course)
        .join(User, User.user_id == CourseReflection.user_id)
        .join(Course, Course.course_id == CourseReflection.course_id)
        .order_by(desc(CourseReflection.updated_at))
    )
    if search:
        s = f"%{search.strip().lower()}%"
        stmt = stmt.where(User.name.ilike(s) | User.email.ilike(s))

    rows = db.execute(stmt).all()

    # Group by user_id
    users_map: dict[int, dict] = {}
    for refl, user, course in rows:
        uid = user.user_id
        if uid not in users_map:
            users_map[uid] = {
                "user_id": uid,
                "name": user.name,
                "email": user.email,
                "courses": [],
                "latest_submitted_at": refl.updated_at or refl.created_at,
            }
        answers_raw = json.loads(refl.answers_json) if refl.answers_json else []
        answers = [ReflectionAnswerItem(**a) for a in answers_raw]
        users_map[uid]["courses"].append(
            UserCourseReflection(
                course_id=course.course_id,
                course_slug=course.slug,
                course_title=course.title,
                submitted_at=refl.created_at,
                updated_at=refl.updated_at,
                answers=answers,
            )
        )

    result = []
    for uid, data in users_map.items():
        result.append(
            AdminUserReflectionSummary(
                user_id=data["user_id"],
                name=data["name"],
                email=data["email"],
                total_reflections=len(data["courses"]),
                latest_submitted_at=data["latest_submitted_at"],
                courses=data["courses"],
            )
        )

    # Sort users by latest submission
    result.sort(key=lambda u: u.latest_submitted_at or datetime.min, reverse=True)
    return result
