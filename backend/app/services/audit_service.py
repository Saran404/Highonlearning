"""Audit trail for admin mutations."""
from __future__ import annotations

import json
from typing import Any, Optional

from sqlalchemy.orm import Session

from app.models import AuditLog


def log_action(db: Session, *, admin_id: int, action: str, target_type: Optional[str] = None,
               target_id: Optional[str | int] = None, metadata: Optional[dict[str, Any]] = None) -> AuditLog:
    """Add an audit row to the *current transaction* (the caller commits, so the action and its audit
    entry succeed or fail together)."""
    row = AuditLog(
        admin_user_id=admin_id,
        action=action,
        target_type=target_type,
        target_id=None if target_id is None else str(target_id),
        metadata_json=json.dumps(metadata, default=str) if metadata else None,
    )
    db.add(row)
    return row
