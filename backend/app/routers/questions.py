"""Questions for an assessment (no correct answers)."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models import User
from app.schemas.assessment import QuestionPublic
from app.services import attempt_service

router = APIRouter(prefix="/assessments", tags=["questions"])


@router.get("/{assessment_id}/questions", response_model=list[QuestionPublic])
def assessment_questions(assessment_id: int, user: User = Depends(get_current_user),
                         db: Session = Depends(get_db)) -> list[QuestionPublic]:
    """403 for GRADED unless the student has an IN_PROGRESS attempt; always allowed for PRACTICE."""
    return [QuestionPublic.from_model(q) for q in attempt_service.questions_for_assessment(db, user, assessment_id)]
