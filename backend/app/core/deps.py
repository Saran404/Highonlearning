"""FastAPI dependencies: database session, authenticated user, role guards."""
from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import timedelta

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.config import settings
from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.core.security import decode_token
from app.database import get_db
from app.models import ActiveSession, User
from app.utils.time import utcnow

_bearer = HTTPBearer(auto_error=False)
_LAST_SEEN_THROTTLE = timedelta(seconds=60)


@dataclass
class AuthContext:
    """The authenticated user plus the device session the token belongs to."""

    user: User
    session: ActiveSession


def authenticate_token(db: Session, token: str) -> AuthContext:
    """Validate a JWT *and* its server-side session. Shared by HTTP and WebSocket auth."""
    payload = decode_token(token, "access")
    try:
        session_id = uuid.UUID(payload["session_id"])
        user_id = int(payload["sub"])
    except (ValueError, TypeError):
        raise UnauthorizedError("Invalid token.", code="INVALID_TOKEN") from None

    session = db.get(ActiveSession, session_id)
    if session is None or session.user_id != user_id:
        raise UnauthorizedError("Session not found.", code="SESSION_REVOKED")
    if session.is_revoked:
        raise UnauthorizedError("Your session has ended.", code="SESSION_REVOKED")

    now = utcnow()
    if now - session.created_at > timedelta(hours=settings.SESSION_EXPIRE_HOURS):
        session.is_revoked = True
        session.refresh_token_hash = None
        db.commit()
        raise UnauthorizedError("Your session has expired after 10 hours. Please sign in again.", code="SESSION_EXPIRED")

    user = db.get(User, user_id)
    if user is None or not user.is_active:
        raise UnauthorizedError("Account is disabled.", code="ACCOUNT_DISABLED")

    now = utcnow()
    if now - session.last_seen_at > _LAST_SEEN_THROTTLE:
        session.last_seen_at = now
        db.commit()
    return AuthContext(user=user, session=session)


def get_auth_context(
    request: Request,
    creds: HTTPAuthorizationCredentials | None = Depends(_bearer),
    db: Session = Depends(get_db),
) -> AuthContext:
    """Authenticate the request and attach ``user``/``session`` to ``request.state``."""
    if creds is None or creds.scheme.lower() != "bearer":
        raise UnauthorizedError("Authentication required.", code="NOT_AUTHENTICATED")
    ctx = authenticate_token(db, creds.credentials)
    request.state.user = ctx.user
    request.state.session = ctx.session
    return ctx


def get_current_user(ctx: AuthContext = Depends(get_auth_context)) -> User:
    return ctx.user


def require_role(*roles: str):
    """Dependency factory: ``Depends(require_role("ADMIN"))``."""

    def _guard(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise ForbiddenError("You do not have permission to do this.", code="FORBIDDEN")
        return user

    return _guard


require_admin = require_role("ADMIN")
