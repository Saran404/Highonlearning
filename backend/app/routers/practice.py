"""Practice mode - stateless, instant feedback, no proctoring."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models import User
from app.schemas.assessment import QuestionPublic
from app.schemas.common import Message
from app.schemas.practice import PracticeAnswerRequest, PracticeAnswerResponse
from app.services import practice_service

router = APIRouter(prefix="/practice", tags=["practice"])


@router.get("/{assessment_id}/questions", response_model=list[QuestionPublic])
def questions(assessment_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[QuestionPublic]:
    return [QuestionPublic.from_model(q) for q in practice_service.practice_questions(db, user.user_id, assessment_id)]


@router.post("/answer", response_model=PracticeAnswerResponse)
def answer(body: PracticeAnswerRequest, user: User = Depends(get_current_user),
           db: Session = Depends(get_db)) -> PracticeAnswerResponse:
    return practice_service.check_answer(db, body.question_id, body.selected_index)


@router.post("/reset/{assessment_id}", response_model=Message)
def reset(assessment_id: int, user: User = Depends(get_current_user)) -> Message:
    """Practice is stateless on the server; the client clears its own state."""
    return Message(message="Practice reset. Nothing is stored on the server.")
