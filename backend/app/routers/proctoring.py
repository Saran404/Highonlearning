"""Snapshot upload (students) and review (admins)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.config import settings
from app.core.constants import TriggerType
from app.core.deps import get_current_user, require_admin
from app.core.exceptions import ForbiddenError
from app.database import get_db
from app.models import User
from app.schemas.proctoring import SnapshotOut, SnapshotUploadResponse
from app.services import proctoring_service
from app.utils import storage

router = APIRouter(prefix="/proctoring", tags=["proctoring"])


@router.post("/snapshot", response_model=SnapshotUploadResponse)
def upload_snapshot(attempt_id: int = Form(...), trigger_type: TriggerType = Form(...), image: UploadFile = File(...),
                    user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> SnapshotUploadResponse:
    data = image.file.read(settings.SNAPSHOT_MAX_BYTES + 1)  # bounded read: never buffer an unbounded upload
    snap = proctoring_service.save_snapshot(db, user, attempt_id=attempt_id, trigger_type=trigger_type, data=data)
    return SnapshotUploadResponse(snapshot_id=snap.snapshot_id, captured_at=snap.captured_at)


@router.get("/{attempt_id}/snapshots", response_model=list[SnapshotOut])
def list_snapshots(attempt_id: int, _: User = Depends(require_admin), db: Session = Depends(get_db)) -> list[SnapshotOut]:
    return proctoring_service.list_snapshots(db, attempt_id)


@router.get("/snapshots/{snapshot_id}/image", include_in_schema=True)
def snapshot_image(snapshot_id: int, exp: int, sig: str, db: Session = Depends(get_db)) -> FileResponse:
    """Serve one image. Authorised by the HMAC signature + expiry in the URL (so ``<img>`` tags work)."""
    if not storage.verify_snapshot_signature(snapshot_id, exp, sig):
        raise ForbiddenError("This link is invalid or has expired.", code="LINK_EXPIRED")
    return FileResponse(proctoring_service.snapshot_file(db, snapshot_id), media_type="image/jpeg",
                        headers={"Cache-Control": "private, max-age=300"})
