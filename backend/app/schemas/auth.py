"""Auth request/response schemas."""
from __future__ import annotations

import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.models import User
from app.schemas.common import UTCDatetime


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72, description="bcrypt only uses the first 72 bytes")

    @field_validator("name")
    @classmethod
    def _strip(cls, v: str) -> str:
        return v.strip()


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=200)
    device_id: str = Field(min_length=8, max_length=100)
    device_info: Optional[str] = Field(default=None, max_length=500)


class RefreshRequest(BaseModel):
    refresh_token: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str
    avatar_url: Optional[str] = None
    created_at: UTCDatetime

    @classmethod
    def from_model(cls, u: User) -> "UserOut":
        return cls(id=u.user_id, name=u.name, email=u.email, role=u.role, avatar_url=u.avatar_url,
                   created_at=u.created_at)


class RegisterResponse(BaseModel):
    user: UserOut


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserOut
    device_id: str
    session_id: uuid.UUID


class RefreshResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class SessionOut(BaseModel):
    session_id: uuid.UUID
    device_id: str
    device_info: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: UTCDatetime
    last_seen_at: UTCDatetime
    is_current: bool = False


class UpdateProfileRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=150)
    avatar_url: Optional[str] = Field(default=None, max_length=500)
