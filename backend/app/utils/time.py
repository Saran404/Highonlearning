"""Time helpers. The database stores naive UTC in DATETIME2 columns."""
from __future__ import annotations

from datetime import datetime, timezone


def utcnow() -> datetime:
    """Current time as a *naive* UTC datetime (matches DATETIME2 columns)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def iso_utc(dt: datetime | None) -> str | None:
    """Serialise a naive-UTC datetime as ISO-8601 with a trailing ``Z``."""
    if dt is None:
        return None
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt.isoformat(timespec="seconds") + "Z"
