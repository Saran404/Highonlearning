"""Application settings, loaded from environment variables / a ``.env`` file."""
from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    """All runtime configuration. Field names match the environment variable keys 1:1."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    ENVIRONMENT: Literal["development", "production", "test"] = "development"

    DB_DRIVER: str | None = None
    DB_SERVER: str | None = None
    DB_NAME: str | None = None
    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    DB_TRUSTED_CONNECTION: bool = False
    DB_TRUST_SERVER_CERTIFICATE: bool = False

    DATABASE_URL: str = (
        "mssql+pyodbc://@DESKTOP-NCVOO5I/ExamProLMS"
        "?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes&trusted_connection=yes"
    )

    JWT_SECRET: str = "change-me-in-prod"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    SESSION_EXPIRE_HOURS: int = 10
    SINGLE_DEVICE_MODE: Literal["strict", "replace"] = "strict"

    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000"
    CORS_ORIGIN_REGEX: str = (
        r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$|"
        r"^https://.*\.netlify\.app$|"
        r"^https://.*\.vercel\.app$|"
        r"^https://.*\.onrender\.com$"
    )

    UPLOAD_DIR: str = "./uploads"
    SERVE_UPLOADS_STATIC: bool = False
    SNAPSHOT_MAX_BYTES: int = 2_000_000
    SIGNED_URL_TTL_SECONDS: int = 600

    MAX_MALPRACTICE: int = 3

    # Timer fairness / robustness (seconds)
    ANSWER_GRACE_SECONDS: int = 5        # answers accepted this long after the deadline (network latency)
    SUBMIT_GRACE_SECONDS: int = 30       # final answer batch accepted this long after the deadline
    EXTEND_TOLERANCE_SECONDS: int = 2    # client/server clock skew allowance for the extension popup
    SWEEPER_INTERVAL_SECONDS: int = 30   # how often abandoned attempts are auto-submitted
    SWEEPER_GRACE_SECONDS: int = 60

    @model_validator(mode="after")
    def _validate_database_settings(self) -> "Settings":
        database_parts = (self.DB_DRIVER, self.DB_SERVER, self.DB_NAME)
        database_configured = any((
            *database_parts,
            self.DB_USER,
            self.DB_PASSWORD,
            self.DB_TRUSTED_CONNECTION,
        ))
        if not database_configured:
            return self

        if not all(database_parts):
            raise ValueError("DB_DRIVER, DB_SERVER, and DB_NAME must all be set together")
        if not self.DB_TRUSTED_CONNECTION and (not self.DB_USER or not self.DB_PASSWORD):
            raise ValueError("DB_USER and DB_PASSWORD are required unless DB_TRUSTED_CONNECTION=true")
        return self

    @property
    def database_url(self) -> str | URL:
        """Build a SQLAlchemy URL from DB_* settings, or use DATABASE_URL for legacy configs."""
        if not (self.DB_DRIVER and self.DB_SERVER and self.DB_NAME):
            return self.DATABASE_URL

        query = {
            "driver": self.DB_DRIVER,
        }
        if self.DB_TRUST_SERVER_CERTIFICATE:
            query["TrustServerCertificate"] = "yes"
        if self.DB_TRUSTED_CONNECTION:
            query["trusted_connection"] = "yes"

        return URL.create(
            "mssql+pyodbc",
            username=None if self.DB_TRUSTED_CONNECTION else self.DB_USER,
            password=None if self.DB_TRUSTED_CONNECTION else self.DB_PASSWORD,
            host=self.DB_SERVER,
            database=self.DB_NAME,
            query=query,
        )

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

    @model_validator(mode="after")
    def _forbid_default_secret_in_production(self) -> "Settings":
        if self.ENVIRONMENT == "production" and self.JWT_SECRET == "change-me-in-prod":
            raise ValueError("JWT_SECRET must be changed when ENVIRONMENT=production")
        return self


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance (also usable as a FastAPI dependency)."""
    return Settings()


settings = get_settings()
