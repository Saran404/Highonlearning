# ExamPro LMS - Backend (FastAPI + SQL Server)

Python 3.11+ · FastAPI · SQLAlchemy 2.0 (sync) · Pydantic v2 · pyodbc / ODBC Driver 17 · JWT · WebSockets.
The database already exists (see `../database/*.sql`); the API maps onto it 1:1 and never runs migrations.

## 1. Set up

```bash
cd backend
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt  # requirements.txt for production only
cp .env.example .env                 # then edit the DB_* values and JWT_SECRET
```

Generate a real secret: `python -c "import secrets; print(secrets.token_urlsafe(48))"`.

## 2. Install the SQL Server ODBC driver (once per machine)

| OS | Command |
|---|---|
| Ubuntu / Debian | follow https://learn.microsoft.com/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server then `sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev` |
| macOS | `brew tap microsoft/mssql-release && brew install msodbcsql18` |
| Windows | download "ODBC Driver 18 for SQL Server" from Microsoft and run the installer |

Check it: `python -c "import pyodbc; print(pyodbc.drivers())"` should list `ODBC Driver 17 for SQL Server`.

Connection string notes
* Configure the database with `DB_DRIVER`, `DB_SERVER`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, and `DB_TRUSTED_CONNECTION`. Set `DB_TRUSTED_CONNECTION=true` to use integrated authentication instead of user/password credentials.
* Set `DB_TRUST_SERVER_CERTIFICATE=true` only when connecting to a server with a self-signed certificate. In production, use a valid certificate.
* The Docker images lower OpenSSL's default cipher security level to match the legacy SQL Server endpoint's TLS requirements. This weakens TLS compatibility checks; remove this override when the database endpoint supports modern ciphers.
* The legacy `DATABASE_URL` setting remains supported when the `DB_*` connection settings are not provided.
* Named instance: `mssql+pyodbc://user:pw@HOST\\SQLEXPRESS/ExamProLMS?driver=...`.

## 3. Create the database and users

```bash
sqlcmd -S localhost -U sa -P "<password>" -C -i ../database/01_schema.sql
sqlcmd -S localhost -U sa -P "<password>" -C -i ../database/02_seed_demo.sql      # optional demo course
python -m scripts.create_admin --email you@example.com --name "You" --password "Str0ng!pass" --role ADMIN
python -m scripts.create_admin --demo          # DEV ONLY: admin@exampro.io / student@exampro.io
```

## 4. Run

```bash
uvicorn app.main:app --reload --port 8000
```
* Interactive API docs: http://localhost:8000/docs
* Health check: http://localhost:8000/api/health

## 5. Test

```bash
pytest
```
The tests use in-memory SQLite (no ODBC driver needed) and cover scoring, rank computation, the malpractice threshold,
the start rules, sequential unlock, autosave, submit, extension window, the expired-attempt sweeper and admin reset.

## API summary (all under `/api`)

| Area | Endpoints |
|---|---|
| Auth | `POST /auth/register` `POST /auth/login` `POST /auth/refresh` `POST /auth/logout` `GET /auth/me` `GET /auth/sessions` `DELETE /auth/sessions/{id}` |
| Student | `GET /users/me/dashboard` `PATCH /users/me` `GET /courses` `GET /courses/{slug}` `GET /courses/{slug}/assessments` `GET /assessments/{id}` `GET /assessments/{id}/questions` `GET /assessments/{id}/leaderboard` |
| Graded attempt | `POST /attempts/start` `GET /attempts/{id}` (resume) `PATCH /attempts/{id}/answer` `POST /attempts/{id}/malpractice` `POST /attempts/{id}/extend` `POST /attempts/{id}/submit` `GET /attempts/{id}/result` |
| Practice | `GET /practice/{assessment_id}/questions` `POST /practice/answer` `POST /practice/reset/{assessment_id}` |
| Proctoring | `POST /proctoring/snapshot` `GET /proctoring/{attempt_id}/snapshots` (admin) `GET /proctoring/snapshots/{id}/image?exp=&sig=` |
| Admin | `GET /admin/students` `GET /admin/attempts` `GET /admin/attempts/live` `GET /admin/attempts/{id}` `POST /admin/attempts/{id}/force-submit` `POST /admin/attempts/{id}/reset` `GET /admin/alerts` `POST /admin/sessions/{id}/revoke` `POST /admin/assessments/{id}/recompute-ranks` |
| WebSocket | `WS /ws/admin?token=JWT` `WS /ws/session/{device_id}?token=JWT` |

Errors always look like `{"code": "...", "message": "...", "details": ...}`.
Common codes: `ALREADY_LOGGED_IN` (409), `SESSION_REVOKED` (401), `TOKEN_EXPIRED` (401), `ATTEMPT_EXISTS` (409),
`ASSESSMENT_LOCKED` (403), `NO_ACTIVE_ATTEMPT` (403), `ATTEMPT_EXPIRED` (409), `INVALID_DURATION` (422).

## Files

| File | What it does |
|---|---|
| `app/main.py` | App factory: CORS, routers under `/api`, exception handlers, optional static mount, background sweeper |
| `app/config.py` | Typed settings from `.env`; refuses the default JWT secret in production |
| `app/database.py` | Engine (`pool_pre_ping`, pool 10 / overflow 20), `SessionLocal`, `get_db` |
| `app/models/*` | One SQLAlchemy model per table, column names identical to the DBA schema |
| `app/schemas/*` | Pydantic v2 request/response models; datetimes are emitted as UTC with a `Z` |
| `app/core/security.py` | bcrypt hashing, JWT create/decode (`TOKEN_EXPIRED` vs `INVALID_TOKEN`) |
| `app/core/deps.py` | `get_current_user`, `require_role`; validates the JWT *and* its `ActiveSessions` row on every request |
| `app/core/exceptions.py` | `AppError` family + handlers producing `{code, message, details}` |
| `app/core/websocket_manager.py` | Admin and per-device socket registry, thread-safe publish helpers |
| `app/services/auth_service.py` | Register / login / refresh-token rotation / logout |
| `app/services/session_service.py` | Single-device rule (`strict` vs `replace`), session revocation |
| `app/services/catalog_service.py` | Courses, sequential unlock (`LOCKED/AVAILABLE/IN_PROGRESS/COMPLETED`), dashboard |
| `app/services/attempt_service.py` | Start, autosave, malpractice, extension, submit, result, expired-attempt sweeper |
| `app/services/scoring_service.py` | Pure score / percentage functions |
| `app/services/rank_service.py` | `COUNT(*)+1` rank, top-50 leaderboard, stored-rank refresh |
| `app/services/proctoring_service.py` | Validates and re-encodes snapshot images, stores files + rows |
| `app/services/practice_service.py` | Stateless practice feedback (restricted to PRACTICE assessments) |
| `app/services/motivation_service.py` | Score-banded messages |
| `app/services/admin_service.py`, `audit_service.py` | Admin operations; each mutation writes `AuditLogs` in the same transaction |
| `app/utils/storage.py` | Upload paths, path-traversal guard, HMAC-signed snapshot URLs |
| `scripts/create_admin.py` | Create/reset a user from the command line |
| `tests/*` | pytest suite (SQLite) |

## Design decisions worth knowing

* **Server clock is authoritative.** `time_taken_sec` from the browser is accepted but ignored; time is computed from `StartedAt` and capped at `DeadlineAt`.
* **Strikes.** `MAX_MALPRACTICE=3` means the 3rd violation auto-submits (status `FLAGGED`). The original spec said `count > MAX`, which would allow 4;
  the frontend brief says "3 strikes". To use the literal rule change `malpractice_should_terminate` to `count > max_allowed`.
* **Abandoned attempts.** A background task (every 30 s) auto-submits attempts whose deadline plus grace has passed, using the answers autosaved so far.
* **Idempotent submit.** Double-clicks, two tabs, or the sweeper racing the student cannot double-score an attempt (row lock + status check).
* **Practice cannot leak graded answers.** `/practice/*` only works for `AttemptType = 'PRACTICE'` assessments.
* **Snapshots are private.** They are served through short-lived HMAC-signed URLs. `SERVE_UPLOADS_STATIC=true` mounts `/uploads` publicly - dev only.
* **Idle sessions expire.** A session unseen for `REFRESH_TOKEN_EXPIRE_DAYS` no longer blocks a login in `strict` mode (a student who closed the browser without logging out is not locked out forever).
* **Refresh tokens rotate.** Reusing an old refresh token revokes the session.
* **WebSocket state is in-process.** Run a single Uvicorn worker, or add Redis pub/sub inside `WebSocketManager` before scaling out.
