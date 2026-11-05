"""Current-user profile and dashboard."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models import User
from app.schemas.auth import UpdateProfileRequest, UserOut
from app.services import catalog_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/dashboard")
def dashboard(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> dict:
    """Stats + one row per assessment (status, marks, %, time, rank) + the 'continue learning' item."""
    return catalog_service.dashboard(db, user.user_id)


@router.patch("/me", response_model=UserOut)
def update_me(body: UpdateProfileRequest, user: User = Depends(get_current_user),
              db: Session = Depends(get_db)) -> UserOut:
    if body.name is not None:
        user.name = body.name.strip()
    if body.avatar_url is not None:
        user.avatar_url = body.avatar_url or None
    db.commit()
    db.refresh(user)
    return UserOut.from_model(user)
