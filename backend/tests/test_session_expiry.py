from __future__ import annotations

import uuid
from datetime import timedelta

import pytest

from app.core import security
from app.core.deps import authenticate_token
from app.core.exceptions import UnauthorizedError
from app.models import ActiveSession
from app.services import auth_service, session_service
from app.utils.time import utcnow
from tests.conftest import make_user


def test_authenticate_token_valid_within_10_hours(db):
    user = make_user(db)
    session_id = uuid.uuid4()
    now = utcnow()
    session = ActiveSession(
        session_id=session_id,
        user_id=user.user_id,
        device_id="dev-1",
        created_at=now - timedelta(hours=9, minutes=50),
        last_seen_at=now,
        is_revoked=False,
    )
    db.add(session)
    db.commit()

    token = security.create_access_token(
        user_id=user.user_id,
        role=user.role,
        device_id=session.device_id,
        session_id=session.session_id,
    )
    ctx = authenticate_token(db, token)
    assert ctx.user.user_id == user.user_id
    assert ctx.session.session_id == session.session_id


def test_authenticate_token_expired_after_10_hours(db):
    user = make_user(db)
    session_id = uuid.uuid4()
    now = utcnow()
    session = ActiveSession(
        session_id=session_id,
        user_id=user.user_id,
        device_id="dev-1",
        created_at=now - timedelta(hours=10, minutes=1),
        last_seen_at=now,
        is_revoked=False,
    )
    db.add(session)
    db.commit()

    token = security.create_access_token(
        user_id=user.user_id,
        role=user.role,
        device_id=session.device_id,
        session_id=session.session_id,
    )
    with pytest.raises(UnauthorizedError) as exc_info:
        authenticate_token(db, token)
    assert exc_info.value.code == "SESSION_EXPIRED"
    assert "10 hours" in exc_info.value.message

    # Verify session is marked revoked in DB
    refreshed_session = db.get(ActiveSession, session_id)
    assert refreshed_session.is_revoked is True


def test_refresh_token_expired_after_10_hours(db):
    user = make_user(db)
    session_id = uuid.uuid4()
    now = utcnow()
    session = ActiveSession(
        session_id=session_id,
        user_id=user.user_id,
        device_id="dev-1",
        created_at=now - timedelta(hours=10, minutes=5),
        last_seen_at=now,
        is_revoked=False,
    )
    db.add(session)
    db.commit()

    refresh_token = security.create_refresh_token(
        user_id=user.user_id,
        role=user.role,
        device_id=session.device_id,
        session_id=session.session_id,
    )
    session.refresh_token_hash = security.hash_token(refresh_token)
    db.commit()

    with pytest.raises(UnauthorizedError) as exc_info:
        auth_service.refresh(db, refresh_token)
    assert exc_info.value.code == "SESSION_EXPIRED"
    assert "10 hours" in exc_info.value.message


def test_user_can_login_again_after_session_expired(db):
    user = make_user(db)
    session_id = uuid.uuid4()
    now = utcnow()
    old_session = ActiveSession(
        session_id=session_id,
        user_id=user.user_id,
        device_id="dev-1",
        created_at=now - timedelta(hours=11),
        last_seen_at=now - timedelta(hours=1),
        is_revoked=False,
    )
    db.add(old_session)
    db.commit()

    # live_sessions should exclude the 11-hour-old session
    live = session_service.live_sessions(db, user.user_id)
    assert len(live) == 0

    # User logging in again should succeed without conflict
    new_session, revoked = session_service.open_session(
        db, user, device_id="dev-1", device_info="Chrome on Windows", ip="127.0.0.1"
    )
    db.commit()

    assert new_session.is_revoked is False
    # created_at should be freshly set to now
    assert (utcnow() - new_session.created_at).total_seconds() < 5
    live_after = session_service.live_sessions(db, user.user_id)
    assert len(live_after) == 1
