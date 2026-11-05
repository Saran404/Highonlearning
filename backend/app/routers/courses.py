"""Course catalogue and per-course assessment list with sequential lock status."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.constants import LOCK_LOCKED, ROLE_ADMIN
from app.core.deps import get_current_user
from app.core.exceptions import ForbiddenError
from app.database import get_db
from app.models import User
from app.schemas.assessment import AssessmentListItem
from app.schemas.common import Message
from app.schemas.course import CourseOut
from app.schemas.reflection import ReflectionResponse, SubmitReflectionRequest
from app.services import catalog_service, reflection_service

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("", response_model=list[CourseOut])
def list_courses(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[CourseOut]:
    """Return all courses with sequential lock_status (LOCKED | AVAILABLE | IN_PROGRESS | COMPLETED)."""
    return catalog_service.resolve_all_courses_with_status(db, user.user_id)


@router.get("/{slug}", response_model=CourseOut)
def get_course(slug: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> CourseOut:
    courses = catalog_service.resolve_all_courses_with_status(db, user.user_id)
    for c in courses:
        if c.slug == slug:
            return c
    target = catalog_service.get_course_by_slug(db, slug)
    c_status, prev_title, prev_slug = catalog_service.course_lock_status(db, user.user_id, target)
    return CourseOut(
        id=target.course_id,
        title=target.title,
        slug=target.slug,
        description=target.description,
        thumbnail_url=target.thumbnail_url,
        order_index=target.order_index,
        lock_status=c_status,
        previous_course_title=prev_title,
        previous_course_slug=prev_slug,
        created_at=target.created_at,
    )


@router.get("/{slug}/assessments", response_model=list[AssessmentListItem])
def course_assessments(slug: str, user: User = Depends(get_current_user),
                       db: Session = Depends(get_db)) -> list[AssessmentListItem]:
    """Each assessment with ``lock_status`` = LOCKED | AVAILABLE | IN_PROGRESS | COMPLETED (+ score/rank)."""
    return catalog_service.list_course_assessments(db, user.user_id, catalog_service.get_course_by_slug(db, slug))


@router.post("/{slug}/enroll", response_model=Message)
def enroll(slug: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Message:
    course = catalog_service.get_course_by_slug(db, slug)
    if user.role != ROLE_ADMIN:
        c_status, prev_title, _ = catalog_service.course_lock_status(db, user.user_id, course)
        if c_status == LOCK_LOCKED:
            raise ForbiddenError(f"Complete {prev_title or 'the previous course'} before enrolling in this course.",
                                 code="COURSE_LOCKED", details={"previous_course": prev_title})
    catalog_service.ensure_enrolled(db, user.user_id, course.course_id)
    db.commit()
    return Message(message="Enrolled.")


@router.get("/{slug}/reflection", response_model=ReflectionResponse)
def get_reflection(slug: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ReflectionResponse:
    """Get the current user's submitted reflective activity for this course."""
    return reflection_service.get_user_course_reflection(db, user.user_id, slug)


@router.post("/{slug}/reflection", response_model=ReflectionResponse)
def submit_reflection(slug: str, body: SubmitReflectionRequest, user: User = Depends(get_current_user),
                      db: Session = Depends(get_db)) -> ReflectionResponse:
    """Submit or update the reflective activity answers for this course."""
    return reflection_service.save_user_course_reflection(db, user.user_id, slug, body.answers)


