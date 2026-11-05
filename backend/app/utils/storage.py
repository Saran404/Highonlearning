"""Snapshot file storage and signed URLs."""
from __future__ import annotations

import hashlib
import hmac
import shutil
import time
from pathlib import Path

from app.config import settings
from app.core.exceptions import NotFoundError


def upload_root() -> Path:
    root = Path(settings.UPLOAD_DIR).resolve()
    root.mkdir(parents=True, exist_ok=True)
    return root


def attempt_dir(attempt_id: int) -> Path:
    return upload_root() / str(int(attempt_id))


def resolve(relative_path: str) -> Path:
    """Resolve a stored relative path, refusing anything that escapes the upload root."""
    root = upload_root()
    path = (root / relative_path).resolve()
    if root != path and root not in path.parents:
        raise NotFoundError("File not found.", code="FILE_NOT_FOUND")
    return path


def delete_attempt_files(attempt_id: int) -> None:
    shutil.rmtree(attempt_dir(attempt_id), ignore_errors=True)


def _sig(snapshot_id: int, expires: int) -> str:
    msg = f"snapshot:{snapshot_id}:{expires}".encode()
    return hmac.new(settings.JWT_SECRET.encode(), msg, hashlib.sha256).hexdigest()


def signed_snapshot_url(snapshot_id: int, ttl: int | None = None) -> str:
    """Time-limited URL for one snapshot image. Works in ``<img src>`` (no auth header needed)."""
    expires = int(time.time()) + (ttl or settings.SIGNED_URL_TTL_SECONDS)
    return f"/api/proctoring/snapshots/{snapshot_id}/image?exp={expires}&sig={_sig(snapshot_id, expires)}"


def verify_snapshot_signature(snapshot_id: int, expires: int, sig: str) -> bool:
    if expires < int(time.time()):
        return False
    return hmac.compare_digest(_sig(snapshot_id, expires), sig)
