"""Assessment metadata (never includes questions)."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.core.exceptions import NotFoundError
from app.database import get_db
from app.models import Assessment, Course, User
from app.schemas.assessment import AssessmentListItem
from app.services import catalog_service

router = APIRouter(prefix="/assessments", tags=["assessments"])


@router.get("/{assessment_id}", response_model=AssessmentListItem)
def get_assessment(assessment_id: int, user: User = Depends(get_current_user),
                   db: Session = Depends(get_db)) -> AssessmentListItem:
    """Metadata plus the student's lock status / attempt id - used by the pre-start page."""
    a = db.get(Assessment, assessment_id)
    if a is None:
        raise NotFoundError("Assessment not found.", code="ASSESSMENT_NOT_FOUND")
    course = db.get(Course, a.course_id)
    items = catalog_service.list_course_assessments(db, user.user_id, course)
    return next(i for i in items if i.id == assessment_id)
