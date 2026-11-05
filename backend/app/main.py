"""FastAPI application: CORS, routers, WebSockets, static files and the auto-submit sweeper."""
from __future__ import annotations

import asyncio
import logging
import socket
import urllib.request
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.concurrency import run_in_threadpool

from app.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.websocket_manager import ws_manager
from app.database import SessionLocal
from app.routers import (admin, assessments, attempts, auth, courses, practice, proctoring, questions, rank, users, ws)
from app.services import attempt_service
from app.utils.storage import upload_root

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("exampro")


def _sweep_once() -> int:
    with SessionLocal() as db:
        return attempt_service.auto_submit_expired(db)


async def _sweeper() -> None:
    """Every ``SWEEPER_INTERVAL_SECONDS``, auto-submit attempts whose student disappeared."""
    while True:
        await asyncio.sleep(settings.SWEEPER_INTERVAL_SECONDS)
        try:
            closed = await run_in_threadpool(_sweep_once)
            if closed:
                logger.info("Auto-submitted %s abandoned attempt(s)", closed)
        except Exception:  # noqa: BLE001
            logger.exception("Sweeper iteration failed")


@asynccontextmanager
async def lifespan(_: FastAPI):
    ws_manager.bind_loop(asyncio.get_running_loop())
    upload_root()
    db_target = settings.database_url
    safe_target = db_target.render_as_string(hide_password=True) if hasattr(db_target, "render_as_string") else str(db_target)
    logger.info("Initializing database connection with target: %s", safe_target)
    logger.info("DB_TRUST_SERVER_CERTIFICATE is set to: %s", settings.DB_TRUST_SERVER_CERTIFICATE)

    # Check container outbound IP
    try:
        public_ip = await asyncio.to_thread(lambda: urllib.request.urlopen("https://api.ipify.org", timeout=5).read().decode("utf8"))
        logger.info("Render service outbound public IP: %s", public_ip)
    except Exception as e:
        logger.warning("Could not determine outbound public IP: %s", e)

    # Check TCP socket connectivity to SQL Server host
    db_host = settings.DB_SERVER or (getattr(db_target, "host", None) if hasattr(db_target, "host") else None)
    if db_host:
        try:
            def _check_socket():
                with socket.create_connection((db_host, 1433), timeout=5):
                    pass
            await asyncio.to_thread(_check_socket)
            logger.info("TCP socket connection to %s:1433 SUCCEEDED", db_host)
        except Exception as e:
            logger.error("TCP socket connection to %s:1433 FAILED: %s", db_host, e)

    # Ensure CourseReflections table exists
    try:
        from app.database import engine
        from app.models.course_reflection import CourseReflection
        from sqlalchemy import text
        def _ensure_tables():
            if engine.dialect.name == "mssql":
                with engine.connect() as conn:
                    conn.execute(text("""
                        IF OBJECT_ID(N'dbo.CourseReflections', N'U') IS NULL
                        BEGIN
                            CREATE TABLE dbo.CourseReflections (
                                ReflectionId INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_CourseReflections PRIMARY KEY,
                                UserId INT NOT NULL,
                                CourseId INT NOT NULL,
                                AnswersJson NVARCHAR(MAX) NOT NULL,
                                CreatedAt DATETIME2 NOT NULL CONSTRAINT DF_CourseReflections_CreatedAt DEFAULT SYSUTCDATETIME(),
                                UpdatedAt DATETIME2 NOT NULL CONSTRAINT DF_CourseReflections_UpdatedAt DEFAULT SYSUTCDATETIME(),
                                CONSTRAINT FK_CourseReflections_Users FOREIGN KEY (UserId) REFERENCES dbo.Users(UserId) ON DELETE CASCADE,
                                CONSTRAINT FK_CourseReflections_Courses FOREIGN KEY (CourseId) REFERENCES dbo.Courses(CourseId) ON DELETE CASCADE,
                                CONSTRAINT UQ_CourseReflections_User_Course UNIQUE (UserId, CourseId)
                            );
                            CREATE INDEX IX_CourseReflections_User ON dbo.CourseReflections (UserId);
                            CREATE INDEX IX_CourseReflections_Course ON dbo.CourseReflections (CourseId);
                        END
                    """))
                    conn.commit()
            else:
                CourseReflection.__table__.create(bind=engine, checkfirst=True)
        await asyncio.to_thread(_ensure_tables)
        logger.info("Database tables verified (CourseReflections ensured)")
    except Exception as e:
        logger.warning("Could not auto-create tables: %s", e)

    task = asyncio.create_task(_sweeper())
    try:
        yield
    finally:
        task.cancel()


app = FastAPI(title="HighonLearning LMS API", version="1.0.0", lifespan=lifespan,
              description="Proctored assessment platform for government exam students.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_origin_regex=settings.CORS_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
register_exception_handlers(app)

api = APIRouter(prefix="/api")
for module in (auth, users, courses, assessments, questions, rank, attempts, practice, proctoring, admin, ws):
    api.include_router(module.router)


@api.get("/health", tags=["meta"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", tags=["meta"])
def root() -> dict[str, str]:
    return {
        "message": "HighonLearning LMS API is running",
        "docs": "/docs",
        "health": "/api/health",
    }


app.include_router(api)

if settings.SERVE_UPLOADS_STATIC:  # dev convenience only - snapshots are otherwise served via signed URLs
    app.mount("/uploads", StaticFiles(directory=str(upload_root())), name="uploads")
