# Dashboard Implementation Plan  
  
## Summary  
Build a production-style React 18 + TypeScript dashboard inside `dashboard/`, using the existing FastAPI backend as the source of truth and adding only minimal read-only backend endpoints for dashboard stats/history. The dashboard will use an enterprise SaaS design: dense, calm, responsive, and built for repeated operational use.  
  
The first usable screen will be `/dashboard`, not a marketing landing page. `/` will redirect based on Gmail connection state: connected users go to `/dashboard`; unconnected users go to `/setup`.  
  
## Key Changes  
- Scaffold `dashboard/` as a Vite + React + TypeScript app with strict TypeScript, Tailwind, React Router, TanStack Query, Zustand, React Hook Form, Zod, toast notifications, and an error boundary.  
- Build the main app shell with sidebar navigation, top status bar, and tabs/pages for Overview, Search, Processing, Analytics, and Settings.  
- Wire frontend API calls to existing backend endpoints:  
  - `GET /health`  
  - `GET /api/connect/gmail/status`  
  - `GET /api/connect/gmail`  
  - `PUT /api/connect/gmail/scope`  
  - `POST /api/ingest/gmail`  
  - `POST /api/query`  
- Add minimal backend dashboard support in a new route module, without changing the core ingestion pipeline:  
  - `GET /api/dashboard/stats`: connection summary, email summary count, chunk count, query count, average query latency, latest processed email timestamp, latest query timestamp.  
  - `GET /api/dashboard/query-history?limit=20`: recent query logs for Search history and Analytics.  
- Keep processing real-time behavior simple for now: show an in-flight ingestion state while `POST /api/ingest/gmail` runs, then refresh stats. No Celery queue, WebSocket, or scheduling implementation in this pass.  
- Add dashboard-specific environment config:  
  - `VITE_API_BASE_URL=http://localhost:8000`  
  - Update `.gitignore` for `dashboard/node_modules`, `dashboard/dist`, and frontend env files.  
- Treat the current `.env.example` secrets as a security cleanup item: replace apparent real-looking API keys/secrets with safe placeholders before committing dashboard-related changes.  
  
## Dashboard Behavior  
- Overview:  
  - Shows Gmail connection status, connected email, selected labels, days back, backend health, total processed emails, chunks, queries, average latency, and latest activity.  
  - Provides primary actions for Connect Gmail, Start Ingestion, and Ask a Question.  
- Setup:  
  - Calls `GET /api/connect/gmail`, shows a Connect Gmail action, and opens/redirects to the returned Google OAuth URL.  
  - After callback completes on the backend, the user returns to the dashboard and status refreshes.  
- Search:  
  - Natural language query input with validation.  
  - Calls `POST /api/query`.  
  - Shows answer, latency, source subjects/dates/similarity scores, loading/error/empty states, and local recent searches.  
  - Uses `GET /api/dashboard/query-history` for persisted query history when available.  
- Processing:  
  - Batch size control for `max_emails`.  
  - Calls `POST /api/ingest/gmail`.  
  - Displays fetched/stored/skipped/failed counts after completion and refreshes stats.  
  - Shows clear messaging that processing is synchronous in the current backend.  
- Analytics:  
  - Uses dashboard stats and query history to show summary cards and lightweight charts for query latency/activity.  
  - Avoids fake production metrics that the backend cannot support yet.  
- Settings:  
  - Scope form for labels, days back, and domain filter.  
  - Calls `PUT /api/connect/gmail/scope`.  
  - Validates inputs with Zod and refreshes connection status after save.  
  
## Test Plan  
- Frontend:  
  - Run `npm run type-check`, `npm run lint`, and `npm run build` inside `dashboard/`.  
  - Add focused Vitest tests for API client behavior, form validation, and key render states.  
  - Use Playwright/browser verification for desktop and mobile layouts after the dev server starts.  
- Backend:  
  - Add pytest coverage for the new dashboard stats/history endpoints using mocked or test DB data.  
  - Confirm existing Gmail, ingest, and query route imports still work.  
- Manual acceptance:  
  - Dashboard loads with backend unavailable and shows recoverable errors.  
  - Connected and disconnected Gmail states render correctly.  
  - Ingestion action shows loading, result counts, and refreshed stats.  
  - Search shows answer, sources, latency, empty question validation, and failure state.  
  
## Assumptions  
- Use `npm` as the frontend package manager unless the repo later introduces another standard.  
- Keep auth as the current hardcoded POC tenant flow; do not add user accounts/JWT auth in this dashboard pass.  
- Do not add Celery queue UI beyond honest synchronous processing status.  
- Do not add Sentry, CI/CD, Docker, PWA, or offline support in the first implementation unless requested later; structure the app so these can be added cleanly.  
  
