"""``ActiveSessions`` table - one row per logged-in device."""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, ForeignKey, Integer, Unicode, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import DT, Base
from app.utils.time import utcnow


class ActiveSession(Base):
    __tablename__ = "ActiveSessions"

    session_id: Mapped[uuid.UUID] = mapped_column("SessionId", Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[int] = mapped_column("UserId", Integer, ForeignKey("Users.UserId"))
    device_id: Mapped[str] = mapped_column("DeviceId", Unicode(100))
    device_info: Mapped[Optional[str]] = mapped_column("DeviceInfo", Unicode(500), nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column("IpAddress", Unicode(45), nullable=True)
    refresh_token_hash: Mapped[Optional[str]] = mapped_column("RefreshTokenHash", Unicode(255), nullable=True)
    is_revoked: Mapped[bool] = mapped_column("IsRevoked", Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column("CreatedAt", DT, default=utcnow)
    last_seen_at: Mapped[datetime] = mapped_column("LastSeenAt", DT, default=utcnow)
