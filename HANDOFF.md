# HANDOFF — 2026-07-26 (Step 05)

## Current state

- **Branch:** `feature/booking-mvp-staging`
- **Base:** `dev` (4e49d33, containing merged frontend v2 refresh via PR #6)
- **Commit:** see `SESSION_LOG.md` for the commit SHA after push.

## Work completed (Step 05 — Booking MVP Backend + Staging Deployment)

### K3s infrastructure provisioned

| Resource | Status |
|---|---|
| `drfarah-staging` namespace | Created with labels |
| `harbor-regcred` pull secret | Copied from `toilettage` |
| `drfarah-staging-db-secret` | Created (POSTGRES_USER/PASSWORD/DB) |
| `drfarah-staging-api-secret` | Created (DATABASE_URL + SMTP credentials) |
| `drfarah-staging-api-config` ConfigMap | Applied (CORS, DB host, SMTP settings) |
| `drfarah-staging-postgres` StatefulSet | 1/1 Ready |
| `drfarah-staging-postgres` Service | ClusterIP:5432 |
| `drfarah-staging-api` Deployment | Pending image push |
| `drfarah-staging-api` Service | ClusterIP:80 |
| `drfarah-staging-api` Ingress | `api.staging.drfarah.proxbenovh.cloud` |

### Backend — new files

| File | Purpose |
|---|---|
| `api/app/models/booking.py` | Booking SQLAlchemy model (minimal fields, no clinical free text) |
| `api/app/schemas/booking.py` | BookingCreate + BookingResponse Pydantic schemas with safe validation |
| `api/app/routers/booking.py` | `POST /api/v1/bookings` endpoint |
| `api/app/services/email.py` | SMTP notification service (test mode by default) |
| `api/tests/test_booking.py` | 12 booking tests (CRUD, validation, persistence, safety) |

### Backend — updated files

| File | Change |
|---|---|
| `api/app/main.py` | Registered booking router, added table creation on startup |
| `api/app/core/config.py` | Added SMTP settings (host, port, user, password, from, to, TLS, test mode) |
| `kubernetes/drfarah-staging/configmap.yaml` | Added SMTP_HOST, SMTP_PORT, SMTP_FROM, SMTP_TO, SMTP_USE_TLS, SMTP_TEST_MODE |
| `kubernetes/drfarah-staging/secret.example.yaml` | Added SMTP credential fields |

### Frontend — updated

| File | Change |
|---|---|
| `frontend/app.js` | Submit handler now POSTs to staging API; success shows booking reference; error shows fallback message |
| `frontend/index.html` | Success message paragraph now has `data-success-detail` for dynamic content |

### Jenkinsfile changes

- Added required paths for new backend files and K8s manifests.
- Added `API — build and push to Harbor` stage (dev only):
  - Builds Docker image, tags with GIT_COMMIT and `:dev`.
  - Logs into Harbor with `harbor-robot-devops-project-harbor` credential.
  - Pushes both tags.
- Added `API — deploy staging manifests` stage (dev only):
  - Applies namespace, service, ingress manifests.
  - Sets image tag from GIT_COMMIT.
  - Applies deployment and waits for rollout (120s timeout).
- Added `API — staging health check` stage (dev only):
  - Liveness probe retry loop.
  - Readiness probe.
  - Booking endpoint smoke test (POST, expects 201).
- Updated header comments.

### Documentation created/updated

- Updated: `api/README.md` — full endpoint list, structure, env vars, booking data discipline, SMTP docs.
- Updated: `frontend/README.md` — booking behavior updated for API integration.
- Updated: `kubernetes/drfarah-staging/README.md` — current state, secrets, Jenkins deployment flow.
- Updated: `HANDOFF.md` — this file.
- Updated: `SESSION_LOG.md` — session record appended.

### SMTP status

- SMTP credentials (`SMTP_USER`, `SMTP_PASSWORD`, `SMTP_HOST`, etc.) were
  copied from the `toilettage-api-secret` into `drfarah-staging-api-secret`.
  No credential values were printed or exposed.
- `SMTP_TEST_MODE=true` is set in the ConfigMap — emails are logged, not sent.
  This is the safe default for staging. Set to `false` when ready to send.

### Booking data discipline

- No clinical free text in any field.
- Name fields validated via regex (letters, hyphens, apostrophes, spaces only).
- Email and phone validated via patterns.
- Reason category is constrained (not free text).
- Request body never logged.
- No insurance, ID, SSN, medical history, or documents collected.

### What was NOT done (intentionally)

- No Keycloak/admin UI.
- No production deployment.
- No lab interpretation, AI agents, phone AI, admin dashboard, payment, EHR.
- Docker image not yet built/pushed (Docker unavailable on management VM;
  Jenkins handles this on dev branch).
- No PR merge (awaiting operator review).

## Deployment behavior summary

| Branch | Validation | Build+Push | K8s Deploy | Frontend Deploy |
|---|---|---|---|---|
| `feature/*` | Yes | No | No | No |
| `dev` | Yes | Yes | Yes | Yes |
| `main` | Yes | No | No | No (prod not configured) |

## Files the next session must read first

1. `HANDOFF.md` — this file.
2. `SESSION_LOG.md` — latest session entry.
3. `api/README.md` — booking endpoint and SMTP docs.
4. `kubernetes/drfarah-staging/README.md` — deployed resource state.
5. `docs/deployment/FRONTEND_STAGING.md` — frontend deployment details.

## Recommended next step

**Review the full booking flow on staging** — merge this PR into `dev`, let
Jenkins build and deploy, then test the full flow:
1. Open `https://staging.drfarah.proxbenovh.cloud/`
2. Click "Book an appointment"
3. Fill in all 4 steps and submit
4. Verify the success message with booking reference ID
5. Confirm the email notification was logged/sent

Do not start admin/Keycloak until this flow is verified end-to-end.
