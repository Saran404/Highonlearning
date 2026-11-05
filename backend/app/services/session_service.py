"""Device-session management and the single-device rule."""
from __future__ import annotations

import uuid
from datetime import timedelta
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.core.exceptions import ConflictError, NotFoundError
from app.core.websocket_manager import ws_manager
from app.models import ActiveSession, User
from app.utils.time import iso_utc, utcnow


def _session_cutoff():
    """Sessions created longer than SESSION_EXPIRE_HOURS (10h) ago are expired."""
    return utcnow() - timedelta(hours=settings.SESSION_EXPIRE_HOURS)


def _idle_cutoff():
    """Sessions unseen for longer than the refresh-token lifetime can no longer refresh, so they are dead."""
    return utcnow() - timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)


def live_sessions(db: Session, user_id: int) -> list[ActiveSession]:
    """Sessions that are not revoked, within the 10h duration, and not idle-expired."""
    return list(db.scalars(
        select(ActiveSession).where(
            ActiveSession.user_id == user_id,
            ActiveSession.is_revoked == False,
            ActiveSession.created_at >= _session_cutoff(),
            ActiveSession.last_seen_at >= _idle_cutoff(),
        ).order_by(ActiveSession.created_at)
    ))


def open_session(db: Session, user: User, *, device_id: str, device_info: Optional[str], ip: Optional[str]
                 ) -> tuple[ActiveSession, list[str]]:
    """Create or reuse the session for ``device_id``, enforcing ``SINGLE_DEVICE_MODE``.

    Returns ``(session, revoked_device_ids)``. The caller commits and then notifies the revoked
    devices. The commit-then-notify order matters: a device must never be told it was logged out
    unless the revocation was really stored.
    """
    now = utcnow()
    # Revoke any expired sessions on this device for the user
    expired_on_device = list(db.scalars(
        select(ActiveSession).where(
            ActiveSession.user_id == user.user_id,
            ActiveSession.device_id == device_id,
            ActiveSession.is_revoked == False,
            ActiveSession.created_at < _session_cutoff(),
        )
    ))
    for s in expired_on_device:
        s.is_revoked = True

    existing = live_sessions(db, user.user_id)
    others = [s for s in existing if s.device_id != device_id]
    same = next((s for s in existing if s.device_id == device_id), None)

    revoked_devices: list[str] = []
    if others:
        if settings.SINGLE_DEVICE_MODE == "strict":
            raise ConflictError(
                "You are already logged in on another device. Log out there first.",
                code="ALREADY_LOGGED_IN",
                details={"device_info": others[0].device_info, "last_seen_at": iso_utc(others[0].last_seen_at)},
            )
        for s in others:  # "replace" mode
            s.is_revoked = True
            revoked_devices.append(s.device_id)

    if same is not None:
        same.device_info = device_info or same.device_info
        same.ip_address = ip or same.ip_address
        same.last_seen_at = now
        same.created_at = now  # Reset session start time to now so a new 10-hour window starts
        return same, revoked_devices

    session = ActiveSession(user_id=user.user_id, device_id=device_id, device_info=device_info, ip_address=ip,
                            is_revoked=False, created_at=now, last_seen_at=now)
    db.add(session)
    return session, revoked_devices


def notify_revoked(device_ids: list[str], reason: str = "Logged in from another device") -> None:
    for d in device_ids:
        ws_manager.publish_device(d, {"type": "SESSION_REVOKED", "reason": reason})


def revoke(db: Session, session: ActiveSession) -> None:
    session.is_revoked = True
    session.refresh_token_hash = None


def get_owned_session(db: Session, user_id: int, session_id: uuid.UUID) -> ActiveSession:
    s = db.get(ActiveSession, session_id)
    if s is None or s.user_id != user_id:
        raise NotFoundError("Session not found.", code="SESSION_NOT_FOUND")
    return s
