"""``MalpracticeLogs`` table."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, Unicode, UnicodeText
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import DT, BigIntPK, Base
from app.utils.time import utcnow


class MalpracticeLog(Base):
    __tablename__ = "MalpracticeLogs"

    log_id: Mapped[int] = mapped_column("LogId", BigIntPK, primary_key=True, autoincrement=True)
    attempt_id: Mapped[int] = mapped_column("AttemptId", BigIntPK, ForeignKey("Attempts.AttemptId", ondelete="CASCADE"))
    type: Mapped[str] = mapped_column("Type", Unicode(30))
    occurred_at: Mapped[datetime] = mapped_column("OccurredAt", DT, default=utcnow)
    metadata_json: Mapped[Optional[str]] = mapped_column("MetadataJson", UnicodeText, nullable=True)
