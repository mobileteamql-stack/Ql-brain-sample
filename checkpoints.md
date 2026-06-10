 # Dashboard Implementation Plan With Module Checkpoints  
  
## Summary  
Implement the dashboard in staged modules under `dashboard/`, verifying each module before moving to the next. Each checkpoint must pass its own build/type/lint/manual checks, and no later module should begin until the current one is working.  
  
## Checkpoint 1: Frontend Foundation  
- Scaffold `dashboard/` as a Vite + React + TypeScript app.  
- Add Tailwind, routing, TanStack Query, Zustand, React Hook Form, Zod, toast notifications, and base error boundary.  
- Add `.env.example` with `VITE_API_BASE_URL=http://localhost:8000`.  
- Update `.gitignore` for frontend build/dependency artifacts.  
- Verification:  
  - `npm install`  
  - `npm run type-check`  
  - `npm run lint`  
  - `npm run build`  
  - Start dev server and confirm the app shell renders.  
  
## Checkpoint 2: Backend Dashboard APIs  
- Add minimal read-only backend endpoints:  
  - `GET /api/dashboard/stats`  
  - `GET /api/dashboard/query-history?limit=20`  
- Register the dashboard router in `main.py`.  
- Keep existing Gmail, ingest, and query APIs unchanged.  
- Verification:  
  - Add pytest coverage for stats and query history.  
  - Run relevant backend tests.  
  - Confirm `/health`, `/api/connect/gmail/status`, and new dashboard endpoints respond correctly.  
  
## Checkpoint 3: App Shell And Navigation  
- Build enterprise SaaS layout with sidebar, header, responsive mobile navigation, and route-level pages:  
  - `/setup`  
  - `/dashboard`  
  - `/dashboard/search`  
  - `/dashboard/processing`  
  - `/dashboard/analytics`  
  - `/dashboard/settings`  
- `/` redirects based on Gmail connection state.  
- Verification:  
  - Browser-check desktop and mobile layouts.  
  - Confirm navigation works without broken routes.  
  - Confirm unavailable backend shows a clear recoverable error state.  
  
## Checkpoint 4: Gmail Setup And Overview  
- Wire Gmail connection state using `GET /api/connect/gmail/status`.  
- Build setup flow using `GET /api/connect/gmail` and returned `auth_url`.  
- Build Overview cards for backend health, Gmail state, scope, processed emails, chunks, queries, latency, and latest activity.  
- Verification:  
  - Connected and disconnected states render correctly.  
  - Overview refreshes after query invalidation.  
  - Browser-check empty/loading/error states.  
  
## Checkpoint 5: Processing Module  
- Build Processing page with batch size control.  
- Call `POST /api/ingest/gmail` with `{ max_emails }`.  
- Show synchronous in-flight state and completion counts: fetched, stored, skipped, failed.  
- Refresh dashboard stats and Gmail status after completion.  
- Verification:  
  - Invalid batch sizes are blocked by form validation.  
  - Success and failure responses render clearly.  
  - No fake queue or real-time status is shown beyond current backend capability.  
  
## Checkpoint 6: Search Module  
- Build natural language Search page.  
- Call `POST /api/query`.  
- Show answer, latency, sources, similarity scores, subject/date attribution, loading state, empty validation, and errors.  
- Add local recent searches plus persisted query history from `GET /api/dashboard/query-history`.  
- Verification:  
  - Empty questions are blocked.  
  - Successful answers show source attribution.  
  - Backend failure and no-results states are useful.  
  - Type-check and build pass.  
  
## Checkpoint 7: Analytics And Settings  
- Analytics:  
  - Use dashboard stats and query history for activity, latency, and usage summaries.  
  - Add lightweight charts without inventing unavailable production metrics.  
- Settings:  
  - Scope form for labels, days back, and domain filter.  
  - Call `PUT /api/connect/gmail/scope`.  
  - Refresh status after save.  
- Verification:  
  - Settings validation works.  
  - Scope saves and refetches.  
  - Analytics handles empty query history cleanly.  
  
## Checkpoint 8: Final Hardening  
- Replace real-looking secrets in `.env.example` with safe placeholders.  
- Run full frontend checks:  
  - `npm run type-check`  
  - `npm run lint`  
  - `npm run build`  
- Run backend tests added for dashboard APIs.  
- Start backend and frontend together.  
- Browser-verify:  
  - Desktop layout  
  - Mobile layout  
  - Setup  
  - Overview  
  - Search  
  - Processing  
  - Analytics  
  - Settings  
- Final status should include changed files, tests run, any skipped checks, and the local dashboard URL.  
  
## Assumptions  
- Use `npm` for the dashboard.  
- Keep current POC tenant behavior; no JWT/user-auth implementation.  
- Add only minimal backend endpoints needed for stats/history.  
- Do not implement Celery queue UI, WebSockets, PWA, Docker, Sentry, or CI/CD in this pass.  
