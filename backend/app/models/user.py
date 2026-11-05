"""``Users`` table."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Integer, Unicode
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import DT, Base
from app.utils.time import utcnow


class User(Base):
    __tablename__ = "Users"

    user_id: Mapped[int] = mapped_column("UserId", Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column("Name", Unicode(150))
    email: Mapped[str] = mapped_column("Email", Unicode(200), unique=True)
    hashed_password: Mapped[str] = mapped_column("HashedPassword", Unicode(255))
    role: Mapped[str] = mapped_column("Role", Unicode(20), default="STUDENT")
    avatar_url: Mapped[Optional[str]] = mapped_column("AvatarUrl", Unicode(500), nullable=True)
    is_active: Mapped[bool] = mapped_column("IsActive", Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column("CreatedAt", DT, default=utcnow)
    updated_at: Mapped[datetime] = mapped_column("UpdatedAt", DT, default=utcnow, onupdate=utcnow)
