"""Shared schema types."""
from __future__ import annotations

from datetime import datetime
from typing import Annotated, Any, Generic, Optional, TypeVar

from pydantic import BaseModel, PlainSerializer

from app.utils.time import iso_utc

# Naive-UTC datetimes from the DB are emitted as ISO-8601 with a "Z" so browsers parse them as UTC.
UTCDatetime = Annotated[datetime, PlainSerializer(lambda d: iso_utc(d), return_type=str, when_used="json-unless-none")]

T = TypeVar("T")


class ErrorResponse(BaseModel):
    code: str
    message: str
    details: Optional[Any] = None


class Message(BaseModel):
    ok: bool = True
    message: str = ""


class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
