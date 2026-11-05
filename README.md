# ExamPro LMS

Proctored assessment platform for government-exam students (TNPSC, SSC, Banking, UPSC, RRB, IBPS).

```
exampro-lms/
├── database/    01_schema.sql · 02_seed_demo.sql · 03_useful_queries.sql   (SQL Server / T-SQL)
├── backend/     FastAPI + SQLAlchemy 2.0 + pyodbc                         (see backend/README.md)
├── frontend/    React 18 + TypeScript + Vite + Tailwind                    (see frontend/README.md)
└── docker-compose.yml   SQL Server + schema init + backend + frontend
```

## How to run

**Option A - Docker (fastest)**
```bash
docker compose up --build
docker compose exec backend python -m scripts.create_admin --demo
# app: http://localhost:8080   api docs: http://localhost:8000/docs
```
Demo logins (development only): `admin@exampro.io / Admin@12345`, `student@exampro.io / Student@12345`.

**Option B - local**
1. Run `database/01_schema.sql`, then `database/02_seed_demo.sql` on your SQL Server.
2. Backend: follow `backend/README.md` (venv, `.env`, ODBC driver, `uvicorn app.main:app --reload --port 8000`).
3. Create users: `python -m scripts.create_admin ...`
4. Frontend: `cd frontend && npm install && npm run dev`.

## The SQL

* `01_schema.sql` - all 11 tables exactly as specified, plus constraints (roles, statuses, `ISJSON`, duration/pass ranges), the **filtered unique index that enforces one graded attempt per student per assessment**, rank/leaderboard indexes and the `vw_AssessmentRanking` view.
* `02_seed_demo.sql` - one course, four sequential graded tests and one practice set with worked explanations.
* `03_useful_queries.sql` - the rank query, top-50 leaderboard, student dashboard, sequential-unlock query, live monitor, malpractice alerts, item analysis and maintenance queries.

## Verification status

The sandbox this was written in had no network access, so nothing could be installed or executed against a real SQL Server.
What was checked: every Python file compiles, the pure scoring/motivation functions were run, and the frontend passes a TypeScript syntax check.
**Not yet run:** `pytest`, `npm install && npm run build`, the SQL scripts against SQL Server, and the browser proctoring flow.
Expect to fix a few small type or version issues on first run, and test on the real browsers your students use (camera and fullscreen behave differently across them).
