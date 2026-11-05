"""Snapshot upload/validation and lookups."""
from __future__ import annotations

from io import BytesIO
from typing import Optional

from PIL import Image, UnidentifiedImageError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.core.constants import ATTEMPT_IN_PROGRESS
from app.core.exceptions import AppError, NotFoundError, UnprocessableError
from app.models import Attempt, ProctoringSnapshot, User
from app.schemas.proctoring import SnapshotOut
from app.services import attempt_service
from app.utils import storage
from app.utils.time import utcnow

_ALLOWED_FORMATS = {"JPEG", "PNG", "WEBP"}


def normalise_image(data: bytes) -> bytes:
    """Validate that ``data`` is a real image and re-encode it as a bounded JPEG.

    Re-encoding strips metadata and any payload hidden inside the file, and caps storage per snapshot.
    """
    if not data:
        raise UnprocessableError("Empty image.", code="INVALID_IMAGE")
    if len(data) > settings.SNAPSHOT_MAX_BYTES:
        raise AppError("Image is too large.", code="IMAGE_TOO_LARGE", status_code=413)
    try:
        with Image.open(BytesIO(data)) as probe:
            fmt = probe.format
            probe.verify()
        if fmt not in _ALLOWED_FORMATS:
            raise UnprocessableError("Unsupported image type.", code="INVALID_IMAGE")
        with Image.open(BytesIO(data)) as img:
            img = img.convert("RGB")
            img.thumbnail((1280, 1280))
            out = BytesIO()
            img.save(out, format="JPEG", quality=80, optimize=True)
            return out.getvalue()
    except (UnidentifiedImageError, OSError, SyntaxError, ValueError):
        raise UnprocessableError("The file is not a valid image.", code="INVALID_IMAGE") from None


def save_snapshot(db: Session, user: User, *, attempt_id: int, trigger_type: str, data: bytes) -> ProctoringSnapshot:
    """Store ``UPLOAD_DIR/{attempt_id}/{utc_timestamp}.jpg`` and insert the ``ProctoringSnapshots`` row."""
    attempt = attempt_service.get_attempt(db, attempt_id, user_id=user.user_id)
    if attempt.status != ATTEMPT_IN_PROGRESS:
        raise AppError("This attempt is no longer active.", code="ATTEMPT_NOT_ACTIVE", status_code=409)

    jpeg = normalise_image(data)
    now = utcnow()
    folder = storage.attempt_dir(attempt.attempt_id)
    folder.mkdir(parents=True, exist_ok=True)
    filename = now.strftime("%Y%m%dT%H%M%S%f") + ".jpg"
    (folder / filename).write_bytes(jpeg)

    snap = ProctoringSnapshot(attempt_id=attempt.attempt_id, image_path=f"{attempt.attempt_id}/{filename}",
                              captured_at=now, trigger_type=trigger_type)
    db.add(snap)
    try:
        db.commit()
    except Exception:
        db.rollback()
        (folder / filename).unlink(missing_ok=True)  # do not leave orphan files
        raise
    db.refresh(snap)
    return snap


def list_snapshots(db: Session, attempt_id: int) -> list[SnapshotOut]:
    rows = db.scalars(select(ProctoringSnapshot).where(ProctoringSnapshot.attempt_id == attempt_id)
                      .order_by(ProctoringSnapshot.captured_at))
    return [SnapshotOut(snapshot_id=s.snapshot_id, image_url=storage.signed_snapshot_url(s.snapshot_id),
                        captured_at=s.captured_at, trigger_type=s.trigger_type, face_detected=s.face_detected,
                        face_match_score=float(s.face_match_score) if s.face_match_score is not None else None)
            for s in rows]


def snapshot_file(db: Session, snapshot_id: int):
    snap: Optional[ProctoringSnapshot] = db.get(ProctoringSnapshot, snapshot_id)
    if snap is None:
        raise NotFoundError("Snapshot not found.", code="SNAPSHOT_NOT_FOUND")
    path = storage.resolve(snap.image_path)
    if not path.is_file():
        raise NotFoundError("Snapshot file is missing.", code="SNAPSHOT_NOT_FOUND")
    return path
