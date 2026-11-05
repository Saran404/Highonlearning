# ExamPro LMS - Frontend (React + TypeScript + Vite)

Mobile-first (works from 360 px). React 18 · TypeScript strict · Tailwind · Zustand · React Router 6 · Axios · Framer Motion · Recharts · react-webcam.

## Run

```bash
cd frontend
cp .env.example .env         # VITE_API_URL=http://localhost:8000/api
npm install
npm run dev                  # http://localhost:5173
npm run build                # type-checks, then builds to dist/
```
The backend must allow this origin in `CORS_ORIGINS`. Camera access needs `localhost` or HTTPS.

## Routes

| Path | Page |
|---|---|
| `/` `/login` `/register` | Landing, sign in (409 → "Already logged in on another device."), register |
| `/dashboard` | Stats, progress ring, assessments table (desktop) / cards (mobile), score chart, continue-learning |
| `/courses` `/courses/:slug` | Catalogue; graded tests with lock state + practice sets |
| `/assessments/:id` | Pre-start: duration picker, system check (connection, fullscreen, camera), three rule acknowledgements |
| `/attempts/:attemptId` | Proctored exam screen (also used to resume) |
| `/practice/:id` | Practice: instant feedback after every answer, unlimited repeats |
| `/results/:attemptId` | Score, rank, motivational message, leaderboard, full solutions, snapshots |
| `/admin` | Live feed (WebSocket), attempts with drill-down (force-submit / reset), students |

## How the exam screen works

* **Deadline comes from the server.** The countdown is computed from the wall clock plus the server/client offset measured when the attempt loaded, so refreshing or throttled tabs cannot drift.
* **Autosave.** Every tap is `PATCH`ed immediately; failures are retried every 8 s and *all* answers are sent again on submit.
* **Lockdown** (`useLockdown`): fullscreen exit, tab switch, window blur, right-click, copy/cut/paste, view-source/print/save/reload shortcuts, developer-tools shortcuts and a window-size heuristic. One physical action (Alt+Tab) counts once. The server holds the authoritative strike count.
* **Proctoring** (`useProctoring`): snapshot on start, every 30 s, on each violation and at submit. Upload failures never interrupt the test.
* **Extension:** when the chosen duration ends and time remains, a modal offers the remaining minutes once; no answer in 30 s submits automatically.
* **Session guard** (`useSessionGuard`): a WebSocket per device. `SESSION_REVOKED` ends the local session and shows a modal.

## Honest limits

A web page cannot fully lock a browser. These checks deter and create an audit trail; they cannot stop a second device, a phone camera, or a virtual machine.
Fullscreen is unavailable on iPhone Safari, so the pre-start check blocks graded tests there (practice works).
Tokens are kept in `localStorage` as specified; an XSS bug would expose them, so keep the CSP tight in production.
