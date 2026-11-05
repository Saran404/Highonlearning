"""Password hashing and JWT helpers."""
from __future__ import annotations

import hashlib
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Literal

from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext

from app.config import settings
from app.core.exceptions import UnauthorizedError

_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Verified when the e-mail is unknown so response time does not reveal which e-mails exist.
_DUMMY_HASH = _pwd.hash(secrets.token_urlsafe(8))

TokenType = Literal["access", "refresh"]


def hash_password(plain: str) -> str:
    return _pwd.hash(plain)


def verify_password(plain: str, hashed: str | None) -> bool:
    return _pwd.verify(plain, hashed or _DUMMY_HASH) and hashed is not None


def hash_token(token: str) -> str:
    """SHA-256 of a refresh token (bcrypt truncates at 72 bytes, so it is unsuitable for JWTs)."""
    return hashlib.sha256(token.encode()).hexdigest()


def _encode(claims: dict[str, Any], expires: timedelta, token_type: TokenType) -> str:
    now = datetime.now(timezone.utc)
    payload = {**claims, "typ": token_type, "iat": int(now.timestamp()), "exp": int((now + expires).timestamp())}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def create_access_token(*, user_id: int, role: str, device_id: str, session_id: uuid.UUID) -> str:
    """JWT payload: ``{sub, role, device_id, session_id, exp, iat}`` (+ ``typ``)."""
    return _encode({"sub": str(user_id), "role": role, "device_id": device_id, "session_id": str(session_id)},
                   timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES), "access")


def create_refresh_token(*, user_id: int, role: str, device_id: str, session_id: uuid.UUID) -> str:
    expires = min(
        timedelta(hours=settings.SESSION_EXPIRE_HOURS),
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    return _encode({"sub": str(user_id), "role": role, "device_id": device_id, "session_id": str(session_id),
                    "jti": uuid.uuid4().hex},
                   expires, "refresh")


def decode_token(token: str, expected: TokenType = "access") -> dict[str, Any]:
    """Decode and validate a token; raise 401 ``TOKEN_EXPIRED`` / ``INVALID_TOKEN`` otherwise."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except ExpiredSignatureError:
        raise UnauthorizedError("Token has expired.", code="TOKEN_EXPIRED") from None
    except JWTError:
        raise UnauthorizedError("Invalid token.", code="INVALID_TOKEN") from None
    if payload.get("typ") != expected or not payload.get("session_id") or not payload.get("sub"):
        raise UnauthorizedError("Invalid token.", code="INVALID_TOKEN")
    return payload
