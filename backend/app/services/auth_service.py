"""Registration, login, refresh and logout."""
from __future__ import annotations

from datetime import timedelta
from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import settings
from app.core import security
from app.core.constants import ROLE_STUDENT
from app.core.exceptions import ConflictError, UnauthorizedError
from app.models import ActiveSession, User
from app.services import session_service
from app.utils.time import utcnow


def register_user(db: Session, *, name: str, email: str, password: str) -> User:
    """Create a STUDENT account. Admins/instructors are created out-of-band (see scripts/create_admin.py)."""
    email = email.strip().lower()
    if db.scalar(select(User.user_id).where(User.email == email)) is not None:
        raise ConflictError("An account with this e-mail already exists.", code="EMAIL_EXISTS")
    user = User(name=name.strip(), email=email, hashed_password=security.hash_password(password),
                role=ROLE_STUDENT, is_active=True)
    db.add(user)
    try:
        db.commit()
    except IntegrityError:  # two simultaneous registrations
        db.rollback()
        raise ConflictError("An account with this e-mail already exists.", code="EMAIL_EXISTS") from None
    db.refresh(user)
    return user


def _issue_tokens(db: Session, user: User, session: ActiveSession) -> tuple[str, str]:
    access = security.create_access_token(user_id=user.user_id, role=user.role, device_id=session.device_id,
                                          session_id=session.session_id)
    refresh = security.create_refresh_token(user_id=user.user_id, role=user.role, device_id=session.device_id,
                                            session_id=session.session_id)
    session.refresh_token_hash = security.hash_token(refresh)
    return access, refresh


def login(db: Session, *, email: str, password: str, device_id: str, device_info: Optional[str], ip: Optional[str]
          ) -> tuple[User, ActiveSession, str, str]:
    """Verify credentials, apply the single-device rule, and mint tokens."""
    user = db.scalar(select(User).where(User.email == email.strip().lower()))
    if not security.verify_password(password, user.hashed_password if user else None) or user is None:
        raise UnauthorizedError("Incorrect e-mail or password.", code="INVALID_CREDENTIALS")
    if not user.is_active:
        raise UnauthorizedError("This account is disabled.", code="ACCOUNT_DISABLED")

    session, revoked = session_service.open_session(db, user, device_id=device_id, device_info=device_info, ip=ip)
    db.flush()  # assigns session_id
    access, refresh = _issue_tokens(db, user, session)
    db.commit()
    session_service.notify_revoked(revoked)  # only after the revocation is durable
    return user, session, access, refresh


def refresh(db: Session, refresh_token: str) -> tuple[str, str]:
    """Rotate the refresh token. Reuse of an old token revokes the session (theft signal)."""
    import uuid

    payload = security.decode_token(refresh_token, "refresh")
    session = db.get(ActiveSession, uuid.UUID(payload["session_id"]))
    if session is None or session.is_revoked:
        raise UnauthorizedError("Your session has ended.", code="SESSION_REVOKED")
    if utcnow() - session.created_at > timedelta(hours=settings.SESSION_EXPIRE_HOURS):
        session_service.revoke(db, session)
        db.commit()
        raise UnauthorizedError("Your session has expired after 10 hours. Please sign in again.", code="SESSION_EXPIRED")
    if session.refresh_token_hash != security.hash_token(refresh_token):
        session_service.revoke(db, session)
        db.commit()
        session_service.notify_revoked([session.device_id], "Security check failed. Please sign in again.")
        raise UnauthorizedError("Your session has ended.", code="SESSION_REVOKED")
    user = db.get(User, session.user_id)
    if user is None or not user.is_active:
        raise UnauthorizedError("This account is disabled.", code="ACCOUNT_DISABLED")
    session.last_seen_at = utcnow()
    access, new_refresh = _issue_tokens(db, user, session)
    db.commit()
    return access, new_refresh


def logout(db: Session, session: ActiveSession) -> None:
    session_service.revoke(db, session)
    db.commit()
