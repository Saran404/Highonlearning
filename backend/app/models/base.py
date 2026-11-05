"""Declarative base and shared column types."""
from __future__ import annotations

from sqlalchemy import BigInteger, DateTime, Integer
from sqlalchemy.dialects import mssql
from sqlalchemy.orm import DeclarativeBase

# DATETIME2 on SQL Server (higher precision than DATETIME); plain DateTime elsewhere (tests use SQLite).
DT = DateTime().with_variant(mssql.DATETIME2(), "mssql")

# BIGINT IDENTITY on SQL Server; SQLite only auto-increments INTEGER primary keys.
BigIntPK = BigInteger().with_variant(Integer, "sqlite")


class Base(DeclarativeBase):
    """Base class for all ORM models. Models map 1:1 onto the existing SQL Server tables."""
