"""Authentication routes: register, login (single-device), refresh, logout, sessions."""
from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.core.deps import AuthContext, get_auth_context
from app.database import get_db
from app.schemas.auth import (LoginRequest, RefreshRequest, RefreshResponse, RegisterRequest, RegisterResponse,
                              SessionOut, TokenResponse, UserOut)
from app.schemas.common import Message
from app.services import auth_service, session_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(body: RegisterRequest, db: Session = Depends(get_db)) -> RegisterResponse:
    user = auth_service.register_user(db, name=body.name, email=body.email, password=body.password)
    return RegisterResponse(user=UserOut.from_model(user))


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, request: Request, db: Session = Depends(get_db)) -> TokenResponse:
    """409 ``ALREADY_LOGGED_IN`` in strict mode when another device holds a live session."""
    info = body.device_info or request.headers.get("user-agent", "")[:500] or None
    ip = request.client.host if request.client else None
    user, session, access, refresh = auth_service.login(
        db, email=body.email, password=body.password, device_id=body.device_id, device_info=info, ip=ip)
    return TokenResponse(access_token=access, refresh_token=refresh, user=UserOut.from_model(user),
                         device_id=session.device_id, session_id=session.session_id)


@router.post("/refresh", response_model=RefreshResponse)
def refresh(body: RefreshRequest, db: Session = Depends(get_db)) -> RefreshResponse:
    access, new_refresh = auth_service.refresh(db, body.refresh_token)
    return RefreshResponse(access_token=access, refresh_token=new_refresh)


@router.post("/logout", response_model=Message)
def logout(ctx: AuthContext = Depends(get_auth_context), db: Session = Depends(get_db)) -> Message:
    auth_service.logout(db, ctx.session)
    return Message(message="Logged out.")


@router.get("/me", response_model=UserOut)
def me(ctx: AuthContext = Depends(get_auth_context)) -> UserOut:
    return UserOut.from_model(ctx.user)


@router.get("/sessions", response_model=list[SessionOut])
def list_sessions(ctx: AuthContext = Depends(get_auth_context), db: Session = Depends(get_db)) -> list[SessionOut]:
    return [SessionOut(session_id=s.session_id, device_id=s.device_id, device_info=s.device_info,
                       ip_address=s.ip_address, created_at=s.created_at, last_seen_at=s.last_seen_at,
                       is_current=s.session_id == ctx.session.session_id)
            for s in session_service.live_sessions(db, ctx.user.user_id)]


@router.delete("/sessions/{session_id}", response_model=Message)
def revoke_my_session(session_id: uuid.UUID, ctx: AuthContext = Depends(get_auth_context),
                      db: Session = Depends(get_db)) -> Message:
    target = session_service.get_owned_session(db, ctx.user.user_id, session_id)
    session_service.revoke(db, target)
    db.commit()
    if target.session_id != ctx.session.session_id:
        session_service.notify_revoked([target.device_id], "This device was logged out from another device")
    return Message(message="Session revoked.")
