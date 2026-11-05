"""Admin routes (role = ADMIN). Every mutation is audit-logged by the service layer."""
from __future__ import annotations

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import require_admin
from app.database import get_db
from app.models import User
from app.schemas.admin import AlertRow, AttemptDrilldown, AttemptRow, LiveAttemptRow, StudentRow
from app.schemas.common import Message, Page
from app.schemas.reflection import AdminUserReflectionSummary
from app.services import admin_service, reflection_service

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/students", response_model=Page[StudentRow])
def students(search: Optional[str] = None, page: int = Query(1, ge=1), page_size: int = Query(25, ge=1, le=100),
             _: User = Depends(require_admin), db: Session = Depends(get_db)) -> Page[StudentRow]:
    items, total = admin_service.list_students(db, search=search, page=page, page_size=page_size)
    return Page[StudentRow](items=items, total=total, page=page, page_size=page_size)


@router.get("/attempts", response_model=Page[AttemptRow])
def attempts(status: Optional[str] = None, assessment_id: Optional[int] = None, user_id: Optional[int] = None,
             page: int = Query(1, ge=1), page_size: int = Query(25, ge=1, le=100),
             _: User = Depends(require_admin), db: Session = Depends(get_db)) -> Page[AttemptRow]:
    items, total = admin_service.list_attempts(db, status=status, assessment_id=assessment_id, user_id=user_id,
                                               page=page, page_size=page_size)
    return Page[AttemptRow](items=items, total=total, page=page, page_size=page_size)


@router.get("/attempts/live", response_model=list[LiveAttemptRow])
def live(_: User = Depends(require_admin), db: Session = Depends(get_db)) -> list[LiveAttemptRow]:
    return admin_service.live_attempts(db)


@router.get("/attempts/{attempt_id}", response_model=AttemptDrilldown)
def attempt_detail(attempt_id: int, _: User = Depends(require_admin), db: Session = Depends(get_db)) -> AttemptDrilldown:
    return admin_service.drilldown(db, attempt_id)


@router.post("/attempts/{attempt_id}/force-submit", response_model=AttemptRow)
def force_submit(attempt_id: int, admin: User = Depends(require_admin), db: Session = Depends(get_db)) -> AttemptRow:
    return admin_service.force_submit(db, admin, attempt_id)


@router.post("/attempts/{attempt_id}/reset", response_model=Message)
def reset(attempt_id: int, admin: User = Depends(require_admin), db: Session = Depends(get_db)) -> Message:
    admin_service.reset_attempt(db, admin, attempt_id)
    return Message(message="Attempt deleted. The student can start again.")


@router.get("/alerts", response_model=list[AlertRow])
def alerts(_: User = Depends(require_admin), db: Session = Depends(get_db)) -> list[AlertRow]:
    return admin_service.recent_alerts(db, 100)


@router.post("/sessions/{session_id}/revoke", response_model=Message)
def revoke(session_id: uuid.UUID, admin: User = Depends(require_admin), db: Session = Depends(get_db)) -> Message:
    admin_service.revoke_session(db, admin, session_id)
    return Message(message="Session revoked.")


@router.post("/assessments/{assessment_id}/recompute-ranks", response_model=Message)
def recompute(assessment_id: int, admin: User = Depends(require_admin), db: Session = Depends(get_db)) -> Message:
    n = admin_service.recompute_ranks(db, admin, assessment_id)
    return Message(message=f"Updated {n} ranks.")


@router.get("/reflections", response_model=list[AdminUserReflectionSummary])
def list_reflections(search: Optional[str] = None, _: User = Depends(require_admin),
                     db: Session = Depends(get_db)) -> list[AdminUserReflectionSummary]:
    """List all student reflection activities grouped by user and course."""
    return reflection_service.list_admin_reflections(db, search=search)

