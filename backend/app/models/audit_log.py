"""``AuditLogs`` table - every admin mutation writes a row."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, Integer, Unicode, UnicodeText
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import DT, BigIntPK, Base
from app.utils.time import utcnow


class AuditLog(Base):
    __tablename__ = "AuditLogs"

    audit_id: Mapped[int] = mapped_column("AuditId", BigIntPK, primary_key=True, autoincrement=True)
    admin_user_id: Mapped[int] = mapped_column("AdminUserId", Integer, ForeignKey("Users.UserId"))
    action: Mapped[str] = mapped_column("Action", Unicode(100))
    target_type: Mapped[Optional[str]] = mapped_column("TargetType", Unicode(50), nullable=True)
    target_id: Mapped[Optional[str]] = mapped_column("TargetId", Unicode(50), nullable=True)
    metadata_json: Mapped[Optional[str]] = mapped_column("MetadataJson", UnicodeText, nullable=True)
    created_at: Mapped[datetime] = mapped_column("CreatedAt", DT, default=utcnow)
