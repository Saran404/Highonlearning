"""``ProctoringSnapshots`` table."""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, ForeignKey, Numeric, Unicode
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import DT, BigIntPK, Base
from app.utils.time import utcnow


class ProctoringSnapshot(Base):
    __tablename__ = "ProctoringSnapshots"

    snapshot_id: Mapped[int] = mapped_column("SnapshotId", BigIntPK, primary_key=True, autoincrement=True)
    attempt_id: Mapped[int] = mapped_column("AttemptId", BigIntPK, ForeignKey("Attempts.AttemptId", ondelete="CASCADE"))
    image_path: Mapped[str] = mapped_column("ImagePath", Unicode(500))
    captured_at: Mapped[datetime] = mapped_column("CapturedAt", DT, default=utcnow)
    trigger_type: Mapped[str] = mapped_column("TriggerType", Unicode(20))
    face_detected: Mapped[Optional[bool]] = mapped_column("FaceDetected", Boolean, nullable=True)
    face_match_score: Mapped[Optional[Decimal]] = mapped_column("FaceMatchScore", Numeric(5, 2), nullable=True)
