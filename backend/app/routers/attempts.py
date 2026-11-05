"""Graded attempt engine routes."""
from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.config import settings
from app.core.deps import get_current_user
from app.database import get_db
from app.models import User
from app.schemas.attempt import (AnswerRequest, AnswerResponse, AttemptState, ExtendResponse, MalpracticeRequest,
                                 MalpracticeResponse, ResultResponse, StartAttemptRequest, SubmitRequest)
from app.services import attempt_service

router = APIRouter(prefix="/attempts", tags=["attempts"])


@router.post("/start", response_model=AttemptState, status_code=status.HTTP_201_CREATED)
def start(body: StartAttemptRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> AttemptState:
    attempt = attempt_service.start_attempt(db, user, body)
    return attempt_service.attempt_state(db, attempt)


@router.get("/{attempt_id}", response_model=AttemptState)
def resume(attempt_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> AttemptState:
    """Reload a running attempt (page refresh / resume): questions, saved answers and the deadline."""
    attempt = attempt_service.get_attempt(db, attempt_id, user_id=user.user_id)
    return attempt_service.attempt_state(db, attempt)


@router.patch("/{attempt_id}/answer", response_model=AnswerResponse)
def answer(attempt_id: int, body: AnswerRequest, user: User = Depends(get_current_user),
           db: Session = Depends(get_db)) -> AnswerResponse:
    row = attempt_service.save_answer(db, user, attempt_id, question_id=body.question_id,
                                      selected_index=body.selected_index, marked_for_review=body.marked_for_review)
    return AnswerResponse(saved_at=row.updated_at)


@router.post("/{attempt_id}/malpractice", response_model=MalpracticeResponse)
def malpractice(attempt_id: int, body: MalpracticeRequest, user: User = Depends(get_current_user),
                db: Session = Depends(get_db)) -> MalpracticeResponse:
    count, terminate = attempt_service.record_malpractice(db, user, attempt_id, body.type, body.metadata)
    return MalpracticeResponse(malpractice_count=count, should_terminate=terminate, max_malpractice=settings.MAX_MALPRACTICE)


@router.post("/{attempt_id}/extend", response_model=ExtendResponse)
def extend(attempt_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ExtendResponse:
    attempt = attempt_service.extend_attempt(db, user, attempt_id)
    return ExtendResponse(deadline_at=attempt.deadline_at)


@router.post("/{attempt_id}/submit", response_model=ResultResponse)
def submit(attempt_id: int, body: SubmitRequest, user: User = Depends(get_current_user),
           db: Session = Depends(get_db)) -> ResultResponse:
    attempt = attempt_service.submit_attempt(db, user, attempt_id, body.answers, body.auto)
    return ResultResponse(**attempt_service.build_result(db, attempt, is_admin=user.role == "ADMIN"))


@router.get("/{attempt_id}/result", response_model=ResultResponse)
def result(attempt_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ResultResponse:
    attempt = attempt_service.get_attempt(db, attempt_id, user_id=user.user_id)
    return ResultResponse(**attempt_service.build_result(db, attempt, is_admin=user.role == "ADMIN"))
