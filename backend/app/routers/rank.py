"""Leaderboard."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.core.exceptions import NotFoundError
from app.database import get_db
from app.models import Assessment, User
from app.schemas.assessment import LeaderboardResponse
from app.services import rank_service

router = APIRouter(prefix="/assessments", tags=["rank"])


@router.get("/{assessment_id}/leaderboard", response_model=LeaderboardResponse)
def leaderboard(assessment_id: int, user: User = Depends(get_current_user),
                db: Session = Depends(get_db)) -> LeaderboardResponse:
    """Top 50 by score (desc) then time (asc), plus the caller's own standing."""
    if db.get(Assessment, assessment_id) is None:
        raise NotFoundError("Assessment not found.", code="ASSESSMENT_NOT_FOUND")
    return LeaderboardResponse(**rank_service.leaderboard(db, assessment_id, limit=50, viewer_id=user.user_id))
