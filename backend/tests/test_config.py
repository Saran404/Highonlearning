from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.config import Settings


def test_database_url_is_built_from_individual_environment_settings():
    settings = Settings(
        _env_file=None,
        DB_DRIVER="ODBC Driver 17 for SQL Server",
        DB_SERVER="db.example.com",
        DB_NAME="exam-db",
        DB_USER="exam-user",
        DB_PASSWORD="password@with/slashes",
        DB_TRUSTED_CONNECTION=False,
    )

    url = settings.database_url

    assert url.drivername == "mssql+pyodbc"
    assert url.host == "db.example.com"
    assert url.database == "exam-db"
    assert url.username == "exam-user"
    assert url.password == "password@with/slashes"
    assert url.query == {"driver": "ODBC Driver 17 for SQL Server"}


def test_database_url_uses_integrated_authentication_when_configured():
    settings = Settings(
        _env_file=None,
        DB_DRIVER="ODBC Driver 17 for SQL Server",
        DB_SERVER="db.example.com",
        DB_NAME="exam-db",
        DB_TRUSTED_CONNECTION=True,
    )

    url = settings.database_url

    assert url.username is None
    assert url.password is None
    assert url.query["trusted_connection"] == "yes"


def test_legacy_database_url_is_used_when_individual_settings_are_absent():
    legacy_url = "mssql+pyodbc://user:password@db.example.com/exam-db?driver=ODBC+Driver+17+for+SQL+Server"
    settings = Settings(_env_file=None, DATABASE_URL=legacy_url)

    assert settings.database_url == legacy_url


def test_partial_database_settings_are_rejected():
    with pytest.raises(ValidationError, match="DB_DRIVER, DB_SERVER, and DB_NAME"):
        Settings(_env_file=None, DB_SERVER="db.example.com")
