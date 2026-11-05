"""Proctoring schemas."""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from app.schemas.common import UTCDatetime


class SnapshotUploadResponse(BaseModel):
    snapshot_id: int
    captured_at: UTCDatetime


class SnapshotOut(BaseModel):
    snapshot_id: int
    image_url: str
    captured_at: UTCDatetime
    trigger_type: str
    face_detected: Optional[bool] = None
    face_match_score: Optional[float] = None
