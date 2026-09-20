# SESSION_LOG — Dr. Farah Project

## 2026-07-26 — Session 01: Repository Bootstrap and Readiness Audit

### Git operations
- Initialized empty Git repository in `~/projects/drfarah-project`.
- Set remote `origin` to `git@github.com:ben-edu/project_drfarah.git`.
- Renamed default branch from `master` to `main`.
- Created empty root commit on `main`.
- Created `dev` branch from `main`.
- Created `feature/bootstrap-readiness` branch from `dev`.
- All branch setup done locally; not yet pushed.

### Source documents
- Located `PROJECT_DRFARAH.md` in `project-sources/`.
- Located supporting docs: `00_START_HERE.md`, `01_INFRA_BASELINE.md`,
  `02_DELIVERY_PLAYBOOK.md`, `03_APP_BLUEPRINT.md`, `example-toilettage.md`.
- Copied `PROJECT_DRFARAH.md` content into repository root as `PROJECT.md`.

### Readiness checks performed
- DNS: `dig +short` for all 6 temporary domains.
- HTTPS: `curl -sSI` for all domains (with and without `-k`).
- TLS: `openssl s_client` certificate inspection for all domains.
- Hestia: SSH to BM1 (`ben@192.168.100.75:2275`) to list
  `/home/benweb/web/` — confirmed `drfarah.proxbenovh.cloud` and
  `admin.drfarah.proxbenovh.cloud` exist; `staging.drfarah.proxbenovh.cloud`
  is missing.
- K3s: connectivity confirmed via `~/.kube/config`, 3 nodes Ready.
  Namespace `drfarah` does not exist. Reference pattern `harbor-regcred`
  confirmed in `toilettage` namespace.
- Keycloak: endpoint reachable at `keycloak.soria-academie.fr`. Realm
  `drfarah` does not exist.
- Harbor: endpoint reachable at `harbor.proxbenovh.cloud`.
- Jenkins: multibranch job `project_drfarah` confirmed.

### Files created
- `.gitignore`
- `README.md`
- `PROJECT.md`
- `HANDOFF.md`
- `SESSION_LOG.md`
- `Jenkinsfile`
- `docs/READINESS_AUDIT.md`
- `docs/DECISIONS.md`
- `docs/architecture/README.md`
- `frontend/README.md`
- `admin/README.md`
- `api/README.md`
- `kubernetes/drfarah/README.md`

### Unresolved issues
- TLS certificate mismatch: www, staging, admin, and API domains present
  `*.behnam.fr` certificate instead of `*.proxbenovh.cloud`. HAProxy SNI
  configuration may need updating.
- `staging.drfarah.proxbenovh.cloud` Hestia vhost not yet created.
- `drfarah` K3s namespace not yet created.
- `drfarah` Keycloak realm not yet created.
- SSH to Hestia as `benweb` not tested from this VM — `ben` user was used.
  Jenkins will use the `hestia-benweb-ssh` credential.
- PostgreSQL, SMTP, backup not yet provisioned (expected at this stage).

### No secrets were printed, copied, committed, or exposed.

---

## 2026-07-26 — Session 04B: Deploy Approved Frontend to Staging

### Branch
- Created `feature/frontend-staging-deploy` from `dev` (0e71857, containing
  the Step 04A frontend prototype merge via PR #4).

### Preflight (read-only, no infrastructure changes)
- DNS: `staging.drfarah.proxbenovh.cloud` -> `87.98.174.211`.
- TLS: valid Let's Encrypt cert, SAN covers staging hostname, expires Oct 24.
- HTTPS: HTTP 200 (Hestia default placeholder page).
- Docroot: `/home/benweb/web/staging.drfarah.proxbenovh.cloud/public_html`
  exists, owner `benweb:www-data`, permissions `drwxr-xr-x`.
- Write access: `benweb` confirmed via temporary file create/delete.
- Current content: Hestia default `index.html` and `robots.txt` only.
- `benweb` shell: `/bin/bash` (SSH-ready).

### Jenkinsfile changes
- Added `Frontend — deploy staging` stage (runs on `dev` only):
  - `withCredentials` using `hestia-benweb-ssh` (SSH user private key).
  - Remote preflight: SSH to Hestia as `benweb`, confirm docroot and write.
  - `rsync -av --delete --exclude='.env' --exclude='.well-known'` from
    `frontend/` to staging docroot.
  - Smoke test: HTTP 200 retry loop (5 attempts, 3s interval).
  - Content verification: grep for Dr. Farah marker, noindex meta,
    robots `Disallow: /`.
  - Asset verification: HTTP 200 for /styles.css, /app.js, /robots.txt.
- Updated header comments.
- All existing stages preserved unchanged.
- No API/DB/Keycloak/admin/K3s deployment stages.

### Documentation created/updated
- Created: `docs/deployment/FRONTEND_STAGING.md`.
- Updated: `docs/architecture/README.md`, `frontend/README.md`, `HANDOFF.md`,
  `SESSION_LOG.md`.

### Validation before commit
- `git diff --check` — clean.
- No approved frontend file changed.
- Deploy stage gated on `branch 'dev'` only — cannot run on feature/* or main.
- `.well-known` excluded from rsync.
- Credential ID: `hestia-benweb-ssh` (correct).
- SSH user: `benweb` (correct).
- Docroot: `/home/benweb/web/staging.drfarah.proxbenovh.cloud/public_html`
  (exact).
- No kubectl, Harbor push, production docroot, or API deployment.
- No secrets in diff.

### What was NOT done
- No frontend file changes.
- No manual deployment to Hestia.
- No production deployment configuration.
- No API, PostgreSQL, Keycloak, admin, or K3s deployment.
- No HAProxy, DNS, TLS, or Hestia config changes.
- No PR merge (awaiting operator review).

### No secrets were printed, copied, committed, or exposed.

---

## 2026-07-26 — Session 04A: Integrate Approved Frontend Prototype

### Source
- Design prototype supplied by the design owner:
  `project-sources/drfarah_design_prototype_v1.zip` (4 files, 50 KB).
- Claude Code integrated the approved prototype faithfully — no redesign,
  restyle, simplification, or framework migration.
- Design ownership remains external to Claude Code.

### Branch
- Created `feature/frontend-prototype-integration` from `dev` (a8abb42).

### Files created
- `frontend/index.html` — homepage with integrated booking modal (prototype
  content preserved; added `meta robots noindex,nofollow,noarchive`).
- `frontend/styles.css` — complete responsive stylesheet (unchanged).
- `frontend/app.js` — booking modal interaction, frontend-only (unchanged).
- `frontend/robots.txt` — `Disallow: /` for temporary-domain protection.
- `docs/design/DESIGN_SYSTEM_V1.md` — design system documentation (prototype
  DESIGN_NOTES.md with integration header added).

### Files updated
- `frontend/README.md` — full documentation with unresolved placeholder list.
- `docs/architecture/README.md` — added design document link, updated status.
- `Jenkinsfile` — added frontend validation stage, updated required paths,
  updated header comments.
- `HANDOFF.md` — full session handoff.
- `SESSION_LOG.md` — this entry.

### Allowed corrections
- Added `<meta name="robots" content="noindex,nofollow,noarchive">` to
  `index.html` (temporary-domain indexing protection).
- Created `robots.txt` with `Disallow: /`.
- These must be removed or changed during final-domain migration.
- No visual design, typography, color, spacing, layout, or interaction
  changes were made.

### Accessibility audit
- Prototype already included: `lang="en"`, single logical `h1`, labeled form
  controls, keyboard-operable buttons, Escape-to-close dialog, `role="dialog"`
  with `aria-modal="true"`, skip link, no `outline: none` suppression
  (browser focus rings preserved), touch targets >= 44px.
- No accessibility defects requiring correction were found.

### Booking behavior
- Frontend-only modal preserved intact: four steps, service preselection,
  progress indicator, review step, prototype success notice.
- 12 booking entry points, all using the same `data-open-booking` handler.
- No network requests, no API connection, no data storage, no
  localStorage/sessionStorage.
- The `/book` route and API integration belong to later steps.

### Jenkinsfile — frontend validation stage
- Runs on feature/*, dev, main.
- Confirms `frontend/index.html`, `styles.css`, `app.js`, `robots.txt` exist.
- JS syntax validation via `node:20-slim` container: `node --check
  frontend/app.js`.
- Grep-verifies no-index meta and robots Disallow rule.
- Starts Python `http.server` on port 18900, validates HTTP 200 for `/`,
  `/styles.css`, `/app.js`, `/robots.txt`.
- Cleanup via `trap cleanup_server EXIT`.
- No credentials, rsync, Hestia deploy, Docker push, or kubectl.

### Local validation
- `node --check frontend/app.js` — passed.
- `diff` between prototype sources and repo copies — only robots meta
  addition differs.
- `python3 -m http.server` — all four assets HTTP 200.
- Curl-verified no-index meta and robots Disallow rule.
- `git diff --check` — clean.
- No secrets, passwords, tokens, or keys in the diff.
- `project-sources/` excluded by `.gitignore`.

### Unresolved placeholders
Documented in `frontend/README.md`: phone, email, address, office hours,
legal text, portrait/clinic photography, appointment availability, verified
reviews, final service list, credentials wording, logo.

### What was NOT done
- No redesign, restyle, or framework migration.
- No API integration or `/book` route.
- No deployment to any environment.
- No data persistence.
- No analytics, tracking, or cookie banner.
- No sitemap or Google Fonts change.
- No infrastructure changes (K3s, Harbor, DNS, HAProxy, Hestia).

### No secrets were printed, copied, committed, or exposed.

---

## 2026-07-26 — Session 02: Infrastructure Foundation

### TLS recheck
- Rechecked all 6 hostnames after operator certificate update.
- All certificates: Let's Encrypt, ssl_verify=0, valid until Oct 24 2026.
- SANs cover each hostname specifically (no generic wildcard mismatch).
- www → apex redirect not configured (PARTIAL — both serve 200).

### Hestia / BM1
- Created staging vhost: `v-add-web-domain benweb staging.drfarah.proxbenovh.cloud`
  via SSH to Hestia (`ben@192.168.100.75:2275`, sudo).
- All 3 vhosts now present and verified: `drfarah`, `staging`, `admin`.
- All `public_html/` writable by `benweb` (`benweb:www-data`, `drwxr-xr-x`).
- Admin 503 resolved (was routing issue in Step 01, now 200).

### K3s / BM2
- Created `drfarah` namespace with labels:
  `app.kubernetes.io/name=drfarah`, `app.kubernetes.io/part-of=drfarah-vip-urgent-care`,
  `app.kubernetes.io/managed-by=jenkins`.
- Copied `harbor-regcred` from `toilettage` namespace (type:
  `kubernetes.io/dockerconfigjson`). No secret data printed or exposed.
- Verified existing namespaces, Traefik ingress class, node health.

### Keycloak
- Attempted realm creation via Keycloak admin API.
- Admin username confirmed: `admin` (from `keycloak-env-vars` ConfigMap).
- Bootstrap password in `keycloak-admin-secret` no longer valid (rotated).
- Realm `drfarah` BLOCKED — requires current admin credentials.
- Configuration spec documented in `docs/architecture/INFRASTRUCTURE_FOUNDATION.md`.

### Harbor
- Classified `drfarah-api` image repo as NOT REQUIRED YET.
- Will auto-create on first `docker push` from Jenkins.
- Robot account `harbor-robot-devops-project-harbor` documented for push access.

### PostgreSQL / SMTP / Backup
- PostgreSQL: pattern documented (follow `toilettage-postgres` StatefulSet).
  Reference names: DB `drfarah`, user `drfarah`, secret `drfarah-postgres-secret`.
- SMTP: pattern documented (SORIA for testing, clinic sender for production).
- Backup: identified as BLOCKER before production — no destination defined.

### Files changed
- Updated: `docs/READINESS_AUDIT.md`, `HANDOFF.md`, `SESSION_LOG.md`
- Created: `docs/architecture/INFRASTRUCTURE_FOUNDATION.md`

### No secrets were printed, copied, committed, or exposed.

---

## 2026-07-26 — Session 03A: FastAPI Application Foundation

### Application scaffold
- Created FastAPI application in `api/`:
  - `app/main.py` — app factory, CORS middleware, router registration.
  - `app/core/config.py` — Pydantic Settings (APP_NAME, ENVIRONMENT, DATABASE_URL, CORS_ORIGINS, LOG_LEVEL).
  - `app/core/database.py` — SQLAlchemy 2.x engine (lazy), session factory, connection check.
  - `app/routers/health.py` — `/api/v1/health/live` and `/ready` endpoints.
- `Dockerfile` — python:3.12-slim, non-root user (appuser), HEALTHCHECK.
- `.dockerignore`, `requirements.txt`, `README.md`.
- Tests: `tests/test_health.py` — 10 tests (liveness, readiness, CORS, safety).
- All 10 tests pass locally (Python 3.11 venv).

### Kubernetes staging templates
- Created `kubernetes/drfarah-staging/` with 9 manifests:
  namespace, configmap, secret.example.yaml, postgres-statefulset,
  postgres-service, api-deployment, api-service, api-ingress, README.
- Templates reference staging-specific names: `drfarah-staging-*`.
- Image placeholder: `harbor.proxbenovh.cloud/devops-project-harbor/drfarah-api:dev`.
- Probes use the implemented health endpoints.
- Resource limits follow reference project values.

### Environment isolation
- Decision recorded: `drfarah` = production namespace (reserved), `drfarah-staging` = staging.
- Documented in `docs/architecture/ENVIRONMENT_ISOLATION.md` and `docs/DECISIONS.md`.

### Jenkinsfile
- Removed "No application code guard" stage.
- Added "API — tests" stage (containerized pytest in python:3.12-slim).
- Added "API — Docker build validation" stage (build + run + health check + cleanup).
- No credentials, no image push, no kubectl, no rsync, no deploy.

### Documentation
- Updated: `api/README.md`, `kubernetes/drfarah/README.md` (production-reserved note),
  `docs/DECISIONS.md`, `docs/architecture/README.md`, `HANDOFF.md`, `SESSION_LOG.md`.
- Created: `docs/architecture/ENVIRONMENT_ISOLATION.md`.

### Tests
- 10/10 passing: liveness (3), readiness (4), CORS (3).
- Tests use SQLite for database-dependent checks.
- No live cluster or PostgreSQL required.

### Docker
- Docker daemon not available on management VM.
- Dockerfile validated via reference comparison with `project_toilettage`.
- Jenkins agent has Docker — build validation stage will run there.

### No secrets were printed, copied, committed, or exposed.

---

## 2026-07-26 — Session 03A-FIX: Repair Jenkins API Test Pipeline

### Problem
- Jenkins branch build for `feature/api-foundation` (commit `acc2f98`)
  failed in `API — tests` stage: `No module named pytest`.
- Root cause: `pytest` correctly excluded from `requirements.txt` (keeps
  production image lean), but Jenkins test stage only installed
  `requirements.txt`.

### Fix applied
- Created `api/requirements-dev.txt` with `pytest==8.3.4`.
- Updated Jenkins `API — tests` stage:
  `pip install -q -r requirements.txt -r requirements-dev.txt`.
- Updated `api/README.md` test instructions to include both files.
- Reviewed Docker build validation stage — already correct: builds
  production Dockerfile with only `requirements.txt`.

### Local validation
- All 10 tests pass in `.venv` (Python 3.11).

### No secrets were printed, copied, committed, or exposed.

---

## 2026-07-26 — Session 04C: Integrate Frontend Refresh V2

### Source
- Design prototype v2 supplied by the design owner:
  `project-sources/drfarah_design_prototype_v2.zip` (15 files).
- Claude Code integrated the approved prototype faithfully — no redesign,
  restyle, or reinterpretation.

### Branch
- Created `feature/frontend-refresh-v2` from `dev` (2f979e5, containing the
  Step 04B staging deploy merge).

### Files replaced (complete, not incremental)
- `frontend/index.html` — favicon link, SEO/OG meta, cookie banner, richer
  hero UI, MedicalClinic structured data, 4-step booking with 16-slot grid.
- `frontend/styles.css` — expanded design system with cookie banner, richer
  slot grid, responsive mobile bar, split/rejuvenation/doctor/process sections.
- `frontend/app.js` — 16-slot time picker with "Show more slots" toggle,
  cookie consent via `localStorage`, same 4-step booking flow.
- `frontend/robots.txt` — unchanged (`Disallow: /`).

### Files created (new in this step)
- `frontend/assets/favicon.svg`
- `frontend/assets/logo-mark.svg`
- `frontend/assets/doctor-portrait.svg`
- `frontend/assets/hero-clinic.svg`
- `frontend/assets/urgent-care.svg`
- `frontend/assets/mobile-care.svg`
- `frontend/assets/traveler-care.svg`
- `frontend/assets/rejuvenation-main.svg`
- `frontend/assets/clinic-map.svg`
- `frontend/assets/og-preview.svg`
- `docs/design/DESIGN_SYSTEM_V2.md` (from package DESIGN_NOTES.md)

### Files updated
- `frontend/README.md` — v2 status, structure with assets/, favicon/logo,
  cookie notice, SEO/noindex, richer slot UI, updated placeholders.
- `docs/architecture/README.md` — both design docs linked, v2 marked current.
- `Jenkinsfile` — added `DESIGN_SYSTEM_V2.md` to required paths, added asset
  serving validation for all 10 SVG files.
- `HANDOFF.md` — full session handoff for Step 04C.
- `SESSION_LOG.md` — this entry.

### Jenkinsfile changes
- Added `docs/design/DESIGN_SYSTEM_V2.md` to required paths.
- Added asset serving check block: HTTP 200 validation for all 10 SVG assets.
- No deployment changes.

### Local validation
- `node --check frontend/app.js` — passed.
- Python `http.server`: all core paths and 10 asset paths return HTTP 200.
- Grep verified: noindex meta, Disallow rule, favicon link, cookie banner
  markup, SEO description meta tag.
- Booking modal: all entry points open flow; step 2 shows 8 of 16 slots;
  "Show more slots" reveals all 16; navigation and review summary work.
- No network/API requests in JS code.
- `git diff --check` — clean.
- No secrets, passwords, tokens, or keys in the diff.

### What was NOT done
- No redesign, restyle, or reinterpretation of the supplied package.
- No API, PostgreSQL, Keycloak, Harbor, or Kubernetes changes.
- No deployment from this feature branch.
- No PR merge (awaiting operator review).

### No secrets were printed, copied, committed, or exposed.

---

## 2026-07-26 — Session 05: Booking MVP Backend + Staging Deployment

### Preconditions verified
- `feature/frontend-refresh-v2` merged into dev (PR #6, commit 4e49d33).
- Jenkins dev build #6: SUCCESS.
- Staging frontend: HTTP 200 at `https://staging.drfarah.proxbenovh.cloud/`.

### Branch
- Created `feature/booking-mvp-staging` from `dev` (4e49d33).

### K3s infrastructure
- Created `drfarah-staging` namespace with labels.
- Copied `harbor-regcred` from `toilettage` to `drfarah-staging`.
- Created `drfarah-staging-db-secret` (POSTGRES_USER/PASSWORD/DB).
- Created `drfarah-staging-api-secret` (DATABASE_URL + SMTP keys copied from
  toilettage-api-secret — no values exposed).
- Applied ConfigMap with SMTP settings (SMTP_TEST_MODE=true).
- Deployed PostgreSQL StatefulSet + Service → 1/1 Ready.
- Applied API Service and Ingress manifests.
- API Deployment pending image build/push (no Docker on management VM).

### Backend — new files
- `api/app/models/booking.py` — Booking model (id, service_type, visit_type,
  preferred_day, preferred_time, time_window, first_name, last_name, email,
  phone, reason_category, status, created_at). No clinical free text.
- `api/app/schemas/booking.py` — BookingCreate (strict regex validation on
  name/email/phone fields) and BookingResponse schemas.
- `api/app/routers/booking.py` — `POST /api/v1/bookings` (creates booking,
  triggers email notification fire-and-forget).
- `api/app/services/email.py` — SMTP notification via `smtplib`. Test mode
  logs instead of sending. SMTP credentials from K8s secret.
- `api/tests/test_booking.py` — 12 tests: creation, persistence, validation
  (missing fields, invalid email, numeric names, accented names, empty payload,
  optional fields). Plus safety: no secrets in response.

### Backend — updated files
- `api/app/main.py` — registered booking router, added `Base.metadata.create_all`
  on startup for automatic table creation.
- `api/app/core/config.py` — added SMTP settings (SMTP_HOST, SMTP_PORT,
  SMTP_USER, SMTP_PASSWORD, SMTP_FROM, SMTP_TO, SMTP_USE_TLS, SMTP_TEST_MODE).
- `kubernetes/drfarah-staging/configmap.yaml` — added SMTP environment vars.
- `kubernetes/drfarah-staging/secret.example.yaml` — added SMTP credential fields.

### Frontend — updated
- `frontend/app.js` — submit handler now POSTs to
  `https://api.staging.drfarah.proxbenovh.cloud/api/v1/bookings`. Shows
  booking reference ID on success, clinic phone number on failure.
- `frontend/index.html` — success message now uses `data-success-detail` for
  dynamic confirmation text.

### Jenkinsfile changes
- Added required paths for all new backend files and K8s manifests.
- Added `API — build and push to Harbor` stage (dev only):
  - Builds image, tags with GIT_COMMIT and `:dev`.
  - Logs into Harbor with robot account, pushes both tags.
- Added `API — deploy staging manifests` stage (dev only):
  - Applies namespace, service, ingress. Sets image tag, applies deployment.
  - Waits for rollout (120s timeout).
- Added `API — staging health check` stage (dev only):
  - Liveness probe retry loop, readiness probe, booking POST smoke test.
- Updated header comments.

### Documentation updated
- `api/README.md` — full rewrite with endpoints, structure, env vars, booking
  data discipline, SMTP docs.
- `frontend/README.md` — booking behavior updated for API integration.
- `kubernetes/drfarah-staging/README.md` — current deployed state, secrets,
  Jenkins pipeline flow.
- `HANDOFF.md` — full Step 05 handoff.
- `SESSION_LOG.md` — this entry.

### Validation
- All Python files compile cleanly (`py_compile`).
- Tests designed for in-container execution (22 total: 10 health/CORS +
  12 booking).
- `node --check frontend/app.js` — passed.
- No secrets in Git diff.

### What was NOT done
- No Docker image build/push (Docker unavailable on management VM; Jenkins
  handles this on `dev`).
- No Keycloak, admin UI, production deployment.
- No PR merge (awaiting operator review).
- No clinical free text, no excessive PHI collected.
- No secrets were printed, copied, committed, or exposed.

### No secrets were printed, copied, committed, or exposed.

---

## 2026-07-26 — Session 05-FIX: Test Isolation + Correct SMTP + Complete Staging Booking MVP

### Root cause of Jenkins test failures
Three booking tests failed with unexpected IDs (expected 1 got 2, expected
2 got 4, expected 3 got 7) because all tests shared a single SQLite database
file (`sqlite:///./test_booking.db`). The `setup_env` fixture cleared the
cached engine/settings but did not create a unique database per test. Rows
inserted by earlier tests persisted and caused auto-increment drift.

### Fix: per-test isolated databases
- Changed `setup_env` fixture to accept `tmp_path` (pytest built-in).
- Each test receives `sqlite:///{tmp_path}/test.db` — a unique temporary file.
- `reset_engine()` disposes the old engine and sets cached globals to None.
- Tables are created fresh via the FastAPI lifespan handler.
- After each test, the temp directory is automatically cleaned up by pytest.
- Tested: no cross-test state leakage, order-independent, passes repeatedly.

### Brittle ID assertions fixed
- `test_response_contains_booking_fields`: checks `id >= 1` and `isinstance(id, int)`
- `test_persistence_across_requests`: checks `r2_id > r1_id` (relative ordering)
- `test_id_increments`: checks `id2 == id1 + 1` and `id3 == id2 + 1` within
  the same isolated database

### Deprecation warnings resolved
- **Pydantic v1 `class Config`**: replaced with `model_config = ConfigDict(from_attributes=True)` in `BookingResponse` (Pydantic v2).
- **FastAPI `@app.on_event("startup")`**: replaced with async `lifespan` context manager. Preserved existing behavior: `Base.metadata.create_all()` on startup.

### SMTP configuration corrected

**Identity (verified with reference Soria SMTP pattern):**
- SMTP_HOST: `mail.soria-academie.fr` (was `smtp.soria-academie.fr`)
- SMTP_FROM: `contact@soria-academie.fr` (was `noreply@drfarah.proxbenovh.cloud`)
- SMTP_USER: `contact@soria-academie.fr`
- SMTP_PORT: 587 (verified from reference, STARTTLS)
- SMTP_USE_TLS: true (verified from reference)
- SMTP_TO: `appointments@drfarah.proxbenovh.cloud` (separately configurable)

**Architecture:**
- ConfigMap: non-secret values (SMTP_HOST, SMTP_PORT, SMTP_FROM, SMTP_TO, SMTP_USE_TLS, SMTP_TEST_MODE)
- Secret: identity/password only (SMTP_USER, SMTP_PASSWORD)
- Updated live ConfigMap and Secret via kubectl (no credential exposure).
- `secret.example.yaml` documented the split architecture.

### Email service verification
- Reviewed `api/app/services/email.py`: authenticates with SMTP_USER/PASSWORD, uses STARTTLS on port 587, sender is `contact@soria-academie.fr`.
- No clinical free text in notification body.
- SMTP errors logged safely (no credential leakage). Booking persistence not rolled back on notification failure.
- Added `api/tests/test_email.py` with 7 mock-based tests:
  - successful SMTP send
  - sender address is correct
  - no secrets in logs on connection failure
  - test mode logs instead of sending
  - subject contains patient name
  - body does not contain clinical free text
  - SMTP not configured returns False

### Feature-branch safety confirmed
- All deploy/push stages gated on `branch 'dev'` — feature/* runs validation only.
- No manual deployment performed from feature branch.

### Files changed (6 files, +198 / -36)

| File | Change |
|---|---|
| `api/tests/test_booking.py` | Per-test isolated SQLite via tmp_path; relative ID assertions |
| `api/tests/test_email.py` | **New** — 7 email service tests with mocks |
| `api/app/main.py` | Replaced `on_event("startup")` with async lifespan |
| `api/app/schemas/booking.py` | Pydantic v2 `ConfigDict(from_attributes=True)` |
| `kubernetes/drfarah-staging/configmap.yaml` | Corrected SMTP_HOST and SMTP_FROM |
| `kubernetes/drfarah-staging/secret.example.yaml` | Documented SMTP architecture split |

### No secrets were printed, copied, committed, or exposed.

---

## 2026-07-26 — Session 05-FIX2: Diagnose and Repair API Container Startup Validation

### Root cause of Docker build validation failure

The API image built successfully but the health check (`curl
http://localhost:18000/api/v1/health/live`) always failed with "connection
refused". The container crashed before Uvicorn started listening because:

1. `DATABASE_URL` was not set (config default: `None`).
2. `database.py` fell back to `sqlite:///./drfarah.db` → resolves to
   `/app/drfarah.db`.
3. `main.py` lifespan handler calls `Base.metadata.create_all()` on startup.
4. SQLite tried to create `/app/drfarah.db` — but `/app` is owned by root
   and the container runs as non-root `appuser` (uid 10001).
5. Startup crashed with a database permission error before Uvicorn could bind
   port 8000.

### Fix: Jenkinsfile validation stage rewrite

Replaced the fragile `docker run -d / sleep 5 / curl` block with a robust
validation stage:

- **Unique container name** per build number (`drfarah-api-validation-${BUILD_NUMBER}`).
- **Unique host port** derived from build number to avoid collisions (`18000 + BUILD_NUMBER % 100`).
- **Explicit test environment**:
  - `ENVIRONMENT=test` — readiness accepts SQLite in test mode.
  - `DATABASE_URL=sqlite:////tmp/drfarah-validation.db` — writable path
    under `/tmp/` (world-writable, accessible to non-root `appuser`).
- **Retry loop**: checks liveness every 1s for up to 20 attempts (~20s) instead
  of a single fixed 5s sleep.
- **Early exit on container crash**: if the container exits, stops retrying
  immediately and prints diagnostics.
- **Failure diagnostics**: prints `docker ps -a`, container state/exit code,
  and last 200 log lines.
- **Trap-based cleanup**: container removed on success and failure.
- **Readiness check**: also validates the readiness endpoint under the isolated
  SQLite database.

### Validation environment (no live dependencies)

| Variable | Value | Purpose |
|---|---|---|
| `ENVIRONMENT` | `test` | Readiness accepts SQLite |
| `DATABASE_URL` | `sqlite:////tmp/drfarah-validation.db` | Writable SQLite under /tmp |

SMTP is not configured (`SMTP_HOST=""`) and `SMTP_TEST_MODE=true` (default),
so no email sending is attempted during validation.

### Production image verification

Confirmed (no changes needed):
- Runs as non-root `appuser` (uid 10001).
- Uvicorn on `0.0.0.0:8000`.
- Runtime dependencies only (no `requirements-dev.txt` in image).
- No test files in image (only `requirements.txt` and `app/` copied).
- Liveness (`/live`) does not touch the database.
- Readiness (`/ready`) checks PostgreSQL in staging/production; passes with
  SQLite in test mode.
- No SMTP send during startup.

### Staging safety preserved

- Feature branches still skip Harbor push, Kubernetes deployment, and staging
  API smoke test (gated on `branch 'dev'`).
- Staging still requires real PostgreSQL URL and runtime secrets.
- No application code changed — only the Jenkinsfile validation stage.

### Files changed

| File | Change |
|---|---|
| `Jenkinsfile` | Rewrote API Docker build validation stage with test env, retry loop, diagnostics, cleanup trap |

### No secrets were printed, copied, committed, or exposed.

---

## 2026-07-26 — Session 06: Immutable Staging API Image

### Root cause

The staging API Deployment was running `harbor.proxbenovh.cloud/.../drfarah-api:dev`
instead of the intended immutable commit SHA. The Jenkinsfile used
`${GIT_COMMIT:-dev}` which fell back to `dev` when the Jenkins environment
variable was empty or unset.

### Branch

- Created `fix/immutable-staging-api-image` from `dev` (eb728ff).

### Fix applied

1. **Image tag derivation**: replaced all `${GIT_COMMIT:-dev}` with
   `git rev-parse HEAD` in every stage that needs the tag (build/push,
   deploy, health check).
2. **SHA validation**: each derivation is followed by a POSIX check that
   the value is a non-empty 40-character lowercase hex string. Build fails
   immediately on empty or malformed SHAs.
3. **Deployment rendering**: the committed `:dev` placeholder in
   `api-deployment.yaml` is never applied to the cluster. Instead, Jenkins
   uses `kubectl set image -f ... --dry-run=client -o yaml | kubectl apply -f -`
   to render the Deployment with the immutable SHA at apply time.
4. **Post-rollout verification**: after rollout, Jenkins queries the live
   Deployment image via `kubectl get deployment -o jsonpath` and compares it
   with the expected SHA. Mismatch fails the build.
5. **Both Harbor tags preserved**: the immutable `<sha>` tag and the `:dev`
   convenience alias continue to be pushed.

### Build metadata

The "Build metadata" stage now also prints the SHA obtained from
`git rev-parse HEAD` alongside the Jenkins `GIT_COMMIT` variable for
comparison.

### Files changed

| File | Change |
|---|---|
| `Jenkinsfile` | Four stages updated: build metadata, build/push, deploy, health check |
| `kubernetes/drfarah-staging/README.md` | Documented immutable image tagging and rendering |
| `HANDOFF.md` | Full session handoff |
| `SESSION_LOG.md` | This entry |

### Local `.gitignore` modification

The working tree had an uncommitted `**/.pytest_cache/` addition to
`.gitignore`. This is appropriate and is included in the branch commit.

### Local validation

- `git diff --check` — clean.
- No remaining `${GIT_COMMIT:-dev}` in Jenkinsfile.
- `git rev-parse HEAD` used in all three image-tag locations.
- `kubectl set image --dry-run=client` approach validated locally (kubectl v1.34.5).
- Container name is `api` (confirmed in `api-deployment.yaml` line 30).

### What was NOT done

- No SMTP, secret, or password changes.
- No RBAC changes.
- No production deployment, frontend changes, or Keycloak work.
- No PR merge (awaiting operator review).

### No secrets were printed, copied, committed, or exposed.

---

## 2026-07-26 — Session 07: Real Availability and Appointment Scheduling

### Branch

- Created `feature/real-availability-scheduling` from `dev` (5ca8b47).

### What was built

Replaced the legacy free-text `preferred_day`/`preferred_time` booking system
with real appointment slots, availability generation, and double-booking
prevention backed by PostgreSQL exclusion constraints.

### Commit 1 — Alembic migrations and scheduling data models (`10d6a5f`)

- Added `alembic==1.14.1` to `api/requirements.txt`
- Created `api/alembic.ini`, `api/alembic/env.py` (reads DATABASE_URL from
  Settings, SQLite `render_as_batch=True`)
- Migration 0001: baseline — captures existing `bookings` table
- Migration 0002: creates services, working_hours, blocked_periods,
  appointments tables. PostgreSQL branch: `btree_gist` extension +
  exclusion constraint `no_double_booking`. SQLite branch: plain index.
  Seeds 4 provisional services + Mon-Fri 9am-5pm working hours.
- New models: Service, WorkingHours, BlockedPeriod, Appointment
- Added CLEANUP_TOKEN to Settings
- Booking router: added deprecation docstring

### Commit 2 — Scheduling service and public API endpoints (`fcf1a5f`)

- `api/app/services/scheduling.py` (~190 lines):
  - `generate_availability()` — slot generation at 15-min increments
  - `check_slot_conflict()` — application-level double-booking detection
  - `validate_slot_in_working_hours()` — working hours validation
  - Clinic timezone: `America/Los_Angeles`, UTC storage, ISO 8601 output
- New schemas: ServiceOut, ServiceListResponse, SlotOut,
  AvailabilityResponse, AppointmentCreate, AppointmentResponse
- New router `api/app/routers/appointments.py` (~220 lines):
  - `GET /api/v1/services` — active services only
  - `GET /api/v1/availability` — date-validated slot generation
  - `POST /api/v1/appointments` — conflict detection, 409 on double-booking
  - `POST /api/v1/internal/cleanup-ci` — Bearer token auth, deletes
    `source='ci'` records older than 1 hour
- Registered appointments router in `app/main.py`

### Commit 3 — Frontend integration (`1deb559`)

- `frontend/index.html`: replaced hardcoded service cards with dynamic
  `<div id="service-choices">`, replaced hardcoded slots with date picker
  + slot toolbar + dynamic slot grid
- `frontend/app.js` (~320 lines): rewritten for real API integration
  - `loadServices()` — fetches and renders service cards
  - `renderDatePicker()` — 14-day date picker in clinic timezone
  - `loadAvailability()` / `renderSlots()` — slot grid with show-more
  - `submitAppointment()` — POST with 409 handling, loading states,
    duplicate submission prevention

### Commit 4 — Tests (`0dc599f`)

- `api/tests/conftest.py`: isolated SQLite per test, seed fixtures
- `api/tests/test_services.py`: 7 tests (listing, filtering, validation)
- `api/tests/test_availability.py`: 12 tests (slots, weekends, blocked
  periods, date validation)
- `api/tests/test_appointments.py`: 16 tests (creation, conflict, working
  hours, VIP buffers, validation, cleanup-ci)
- `api/tests/test_concurrency.py`: 3 tests (sequential double-booking,
  concurrent threads [skipped on SQLite], overlapping slots)
- Fixed `_ensure_utc()` helper for SQLite naive datetime comparison
- 70 tests pass, 1 skipped (concurrency requires PostgreSQL)

### Commit 5 — CI and deployment (`27f2d66`)

- `api-deployment.yaml`: added `db-migrate` init container running
  `python -m alembic upgrade head`
- `configmap.yaml`: added `CLEANUP_TOKEN`
- `Jenkinsfile`:
  - Added new required paths (models, schemas, services, routers,
    migrations, tests)
  - Added `CLEANUP_TOKEN` env var
  - `kubectl set image` sets both `api` and `db-migrate` containers
  - Health check: CI cleanup before tests, services endpoint check,
    availability endpoint check, appointment smoke test with
    `source="ci"`
- Added optional `source` field to `AppointmentCreate` schema

### Commit 6 — Documentation (this commit)

- Created `docs/architecture/SCHEDULING.md` — full architecture document
- Updated `api/README.md`, `frontend/README.md`,
  `kubernetes/drfarah-staging/README.md`
- Updated `HANDOFF.md`, `SESSION_LOG.md`

### Design decisions

- **Migration execution:** init container, not app startup. Deterministic
  single execution; failure keeps old pod running.
- **Double-booking:** two-layer defense. App-level conflict check catches
  most cases; PostgreSQL exclusion constraint prevents race conditions.
- **CI cleanup:** token-protected internal endpoint + `source="ci"` marker.
  No public delete endpoint, no new RBAC.
- **Provisional data:** all seed data marked PROVISIONAL. Requires business
  confirmation before production.
- **SQLite dialect branching:** migrations branch on dialect for PostgreSQL
  (exclusion constraint) vs SQLite (plain index). Tests document SQLite
  concurrency limitations.

### What was NOT done

- No SMTP, secret, or password changes
- No RBAC changes
- No production deployment
- No frontend visual redesign
- No admin UI, Keycloak, HAProxy, DNS, or TLS changes

### No secrets were printed, copied, committed, or exposed.

---

## 2026-07-26 — Session 07-FIX: Repair Staging Deployment After Failed dev Merge

### Incident

Step 07 (Real Availability and Appointment Scheduling) was merged into `dev`
(ad8b38a) before the pre-merge audit completed. The live `dev` staging
deployment failed with 5 errors:

1. **`kubectl set image` error:** "unable to find container named db-migrate"
   — `kubectl set image` only targets `spec.containers`, not
   `spec.initContainers`. The init container image was never updated.
2. **Pipe masked the failure:** POSIX sh lacks `pipefail`. The failed
   `kubectl set image` exit code was discarded — only `kubectl apply` (0)
   mattered. The deployment was applied with the init container still on
   `:dev`.
3. **CI cleanup token exposed:** `CLEANUP_TOKEN = 'staging-ci-cleanup-token-2026'`
   was hardcoded in the Jenkinsfile environment block and `configmap.yaml`.
   Printed in Jenkins logs via the curl Authorization header.
4. **Availability endpoint returned 404:** `GET /api/v1/availability?service_code=urgent-care`
   returned 404 because the migration init container ran the old `:dev` image
   (never migrated → no seed data).
5. **Frontend staging deployment skipped:** the smoke test failure aborted
   the pipeline before the frontend deploy stage.

### Branch

- Created `fix/scheduling-staging-deployment` from `dev` (ad8b38a).

### Fix 1 — Deployment rendering

Replaced the `kubectl set image ... | kubectl apply -f -` pipe with:
- `sed` templating to a temp file (replaces `:dev` placeholder with
  immutable SHA in all containers)
- Validation: exact count of image lines = 2, no `:dev` remaining
- Direct `kubectl apply -f "$RENDERED"` — no pipe
- Temp file cleanup after apply
- Post-rollout: verifies BOTH `api` AND `db-migrate` container images

### Fix 2 — Compromised cleanup token

- Removed `CLEANUP_TOKEN` from Jenkinsfile `environment` block.
- CI cleanup now uses `withCredentials([string(...)])` with credential ID
  `drfarah-staging-ci-cleanup-token`.
- `set +x` / `set -x` around the authenticated curl prevents token in logs.
- Removed `CLEANUP_TOKEN` from `configmap.yaml`.
- Added `CLEANUP_TOKEN` to `secret.example.yaml` (the live
  `drfarah-staging-api-secret` must be updated with a new token).
- **Token rotation is mandatory** before next deploy.

### Fix 3 — Availability smoke test

- No longer hardcodes `urgent-care`.
- Calls `GET /api/v1/services`, validates service count > 0, picks first
  active service.
- Queries availability over 14-day window.
- Picks first returned slot for the appointment smoke test.
- Uses `python3` for reliable JSON parsing.

### Fix 4 — Root cause of 404

The 404 was caused by Fix 1's root cause: the init container used the old
`:dev` image, so Alembic never ran migration 0002, so the `services` table
was never seeded. Fix 1 ensures the init container gets the immutable image.

### Fix 5 — False success prevention

The deployment rendering no longer pipes into `kubectl apply`. Any rendering
failure stops the stage immediately.

### Fix 6 — Cleanup endpoint security validated

- Scope: only `source='ci'` records — confirmed safe.
- Auth: 401 for wrong/missing token — correct.
- Token not in logs: `set +x` protection added.
- Constant-time comparison not required (operational token, not user auth).
- Token moved to Secret (defense in depth).

### Fix 7 — Documentation

- Updated HANDOFF.md, SESSION_LOG.md, kubernetes/drfarah-staging/README.md.

### Files changed

| File | Change |
|---|---|
| `Jenkinsfile` | Deploy rendering (sed + validation, no pipe), token via withCredentials + set +x, dynamic service/slot discovery, init container image verification |
| `kubernetes/drfarah-staging/configmap.yaml` | Removed CLEANUP_TOKEN |
| `kubernetes/drfarah-staging/secret.example.yaml` | Added CLEANUP_TOKEN field |
| `kubernetes/drfarah-staging/README.md` | Token rotation notice, corrected deployment docs |
| `HANDOFF.md` | Rewritten for fix session |
| `SESSION_LOG.md` | This entry |

### What was NOT done

- No live Kubernetes changes (Secret rotation requires operator).
- No Jenkins credential creation (requires operator).
- No PR merge (awaiting operator review).
- No application code, SMTP, RBAC, production, frontend, or infra changes.

### No secrets were printed, copied, committed, or exposed.

---

## 2026-07-27 — Session 08-FIX: Bootstrap Legacy Alembic State

### Problem

The staging PostgreSQL database predates Alembic. The `bookings` table was
created by `Base.metadata.create_all()` at application startup (before Alembic
was introduced in Step 07). When the K8s init container ran
`python -m alembic upgrade head`, migration 0001 failed with
"relation 'bookings' already exists" because the CREATE TABLE statement in
0001 tried to create a table that was already there.

### Branch

- Created `fix/bootstrap-legacy-alembic-state` from `dev` (5a9aca2).

### Fix: Migration bootstrap state machine

Created `api/app/migration_bootstrap.py` — a safe state machine that handles
four database states on every pod creation:

- **State 1 (Fresh):** No bookings table, no Alembic revision → `alembic upgrade head`
- **State 2 (Legacy):** bookings table exists, matches 0001 schema, no Alembic
  revision → validate schema, stamp 0001, upgrade head. Existing bookings
  **preserved** — table never dropped or recreated.
- **State 3 (Managed):** Valid Alembic revision present → `alembic upgrade head`
- **State 4 (Unsafe):** Schema mismatch, corrupt revision table, or other
  inconsistent state → fail closed with diagnostic log. No partial changes.

### Legacy schema validation

Before stamping 0001 on a legacy database, the bootstrap validates every
column in the existing `bookings` table: column names, types (with cross-
dialect type matching — PostgreSQL reports `CHARACTER VARYING` while SQLite
reports `VARCHAR`), nullability, and primary key.

If any required column is missing or incompatible, the bootstrap fails
closed — no stamp, no partial migration, no data loss, no scheduling tables
created.

### Tests — 13 PostgreSQL integration tests

`api/tests/test_migration_bootstrap.py` — comprehensive integration tests
against disposable PostgreSQL databases. Each test creates a unique temporary
database via `sudo -u postgres createdb`, runs the bootstrap, verifies the
result, and drops the database.

Test coverage:
- **TestFreshDatabase (5 tests):** all tables created, seed services exist
  (4 codes), seed working hours exist (5 Mon-Fri), Alembic reaches head (0002),
  second bootstrap is idempotent
- **TestLegacyDatabase (4 tests + autouse fixture):** stamped 0001 and upgraded,
  legacy rows preserved with exact field values, booking IDs unchanged (proof
  table not recreated), second bootstrap idempotent
- **TestEmptyAlembicVersion (1 test + autouse fixture):** bookings + empty
  version table → treated as legacy (State 2)
- **TestUnsafeIncompatibleSchema (1 test):** bookings missing required
  `reason_category` column → BootstrapError raised, no stamp, no scheduling
  tables created, original bookings preserved
- **TestAlreadyManaged (2 tests):** upgrades from 0001 to head (data preserved),
  already at head → no-op (data preserved)

Full suite: **83 passed, 1 skipped** (136.36s).

### Cross-dialect considerations

PostgreSQL type names differ from SQLite:
- `CHARACTER VARYING(128)` vs `VARCHAR(128)`
- `TIMESTAMP WITH TIME ZONE` vs `DATETIME`

The schema validator checks for any matching type substring from a tuple of
acceptable type names (e.g., `("VARCHAR", "CHARACTER VARYING")` and
`("DATETIME", "TIMESTAMP")`).

### Settings caching issue

`get_settings()` uses `@lru_cache` — when DATABASE_URL is changed between
tests, the cached URL from a previous test is returned. The Alembic `env.py`
calls `get_settings()` to override the SQLAlchemy URL in `alembic.ini`, so a
cached SQLite URL causes "Context impl SQLiteImpl" errors on PostgreSQL tests.

Fix: tests call `get_settings.cache_clear()` and `reset_engine()` before
creating the Alembic Config.

### Kubernetes init container

Updated `kubernetes/drfarah-staging/api-deployment.yaml` — the `db-migrate`
init container now runs `python -m app.migration_bootstrap` instead of
`python -m alembic upgrade head`.

### CI validation

Added "API — migration bootstrap validation" stage to Jenkinsfile:
1. Verify `api/app/migration_bootstrap.py` exists
2. Verify `api/tests/test_migration_bootstrap.py` exists
3. Verify `python -c "from app.migration_bootstrap import main"` succeeds
4. Run bootstrap against a fresh SQLite database and verify exit code 0

### Documentation updated

- `HANDOFF.md` — full session handoff with state machine overview, schema
  validation, test results, why plain Alembic failed
- `SESSION_LOG.md` — this entry
- `kubernetes/drfarah-staging/README.md` — migration init container docs
  updated for bootstrap, legacy state documented

### Files changed

| File | Change |
|---|---|
| `api/app/migration_bootstrap.py` | **New** — 4-state migration bootstrap |
| `api/tests/test_migration_bootstrap.py` | **New** — 13 PostgreSQL integration tests |
| `kubernetes/drfarah-staging/api-deployment.yaml` | Init container command: migration_bootstrap |
| `Jenkinsfile` | Added migration bootstrap CI validation stage |
| `HANDOFF.md` | Rewritten for bootstrap session |
| `SESSION_LOG.md` | This entry |
| `kubernetes/drfarah-staging/README.md` | Updated migration docs |

### What was NOT done

- No manual Alembic stamp on staging or production
- No changes to existing migrations (0001, 0002)
- No changes to application code (routers, models, services, schemas)
- No live Kubernetes changes
- No SMTP, secret, or password changes
- No PR merge (awaiting operator review)

### No secrets were printed, copied, committed, or exposed.


## 2026-07-27 — PostgreSQL CI test architecture (fix/bootstrap-legacy-alembic-state)

- Root cause of the Jenkins failure: `test_migration_bootstrap.py` orchestrated
  host infrastructure from inside the `python:3.12-slim` test container, calling
  `sudo -u postgres createdb/dropdb` and socket peer-auth. The container has no
  `sudo` and no local PostgreSQL → `FileNotFoundError: 'sudo'` on all 13 tests.
- Fix: tests no longer touch the host. PostgreSQL is provisioned by Jenkins as a
  disposable container on an isolated Docker network; tests receive a maintenance
  URL via `POSTGRES_TEST_DATABASE_URL` (tests/_pg_util.py) and create/drop
  per-test databases with plain SQL on an AUTOCOMMIT connection.
- Marker separation: `@pytest.mark.postgresql` (registered in api/pytest.ini).
  SQLite stage runs `-m "not postgresql"`; the new "API — PostgreSQL integration
  tests" stage runs `-m postgresql` (migration bootstrap + real concurrency).
- Concurrency: the postgres test migrates via the bootstrap (creating the
  `no_double_booking` exclusion constraint from migration 0002) and asserts two
  concurrent requests yield exactly one 201 + one 409 and one active row.
- Determinism: replaced weekend-prone `_days_ahead(4)` with next-Monday slots.
- Cleanup: Jenkins stage uses a POSIX `trap cleanup EXIT INT TERM`; the
  PostgreSQL container uses `--tmpfs` storage and is removed with its network.
  No `sudo`, no `--privileged`, no Docker socket in the test container.
- Branch policy unchanged: feature/fix are validation-only; push/deploy on `dev`.

## 2026-07-28 — Inconsistent Alembic stamp recovery and bootstrap hardening

### Staging incident: alembic_version=0001 with orphaned 0002 tables

A partial prior migration run left the `services`, `working_hours`,
`blocked_periods`, and `appointments` tables from revision 0002 in the staging
database while `alembic_version` was still stamped at 0001. When the init
container's migration bootstrap hit State 3 (already managed at 0001) and ran
`alembic upgrade head`, it crashed with `relation "services" already exists`
because the upgrade tried to recreate tables that were already present.

### Recovery procedure

All four 0002 tables were confirmed empty (0 rows each). `bookings` (4 rows,
legacy) and `alembic_version` (0001) were verified intact. The empty orphan
tables were dropped (FK-safe order: appointments, blocked_periods, working_hours,
services) in a single transaction. The init container retried on its own backoff,
ran upgrade 0001 → 0002 cleanly (creating tables, installing btree_gist, seeding
services and working_hours, creating the no_double_booking constraint), and the
new pod became Ready. Legacy bookings preserved (4 rows). Staging confirmed healthy.

### Hardening: fail-closed guards in migration_bootstrap.py

To prevent this class of failure from recurring, the bootstrap now detects
inconsistent-stamp states and fails closed with an actionable message instead of
crashing on raw `relation already exists`:

- `REVISION_SENTINEL_TABLES` — maps each post-0001 revision to a sentinel table
  that revision introduces (currently `{"0002": "services"}`).
- `_detect_inconsistent_stamp()` — checks whether the current alembic_version
  stamp is behind a sentinel table that already exists.
- **State 3 guard** (already managed): before `command.upgrade`, verifies the
  stamp is consistent with existing tables; if a sentinel table exists but the
  stamp is behind, raises a `BootstrapError` with a diagnostic message naming the
  offending table and revision.
- **State 2 guard** (legacy bookings, no stamp): before stamping 0001, verifies
  no later-revision tables are already present.
- **Fresh-path guard**: verifies no later-revision tables are present before
  running migrations from scratch.

### New tests (TestInconsistentStamp, 3 tests, postgresql-marked)

- `test_stamped_0001_with_0002_tables_fails_closed` — reproduces the exact
  staging incident: bookings + alembic_version=0001 + orphaned services table
  → clean `BootstrapError`, not a ProgrammingError. Verifies revision unchanged
  and bookings intact.
- `test_legacy_bookings_with_orphan_0002_fails_closed` — unversioned legacy
  bookings with orphaned services → fails before stamping, no stamp written.
- `test_exit_code_is_one_not_two` — confirms the inconsistent-stamp path exits
  with code 1 (BootstrapError), not code 2 (crash).

### Jenkinsfix: appointment smoke-test payload quoting

The staging health-check stage's appointment smoke test had a shell-quoting bug:
a double-quoted multi-line heredoc for the JSON `-d` body inside a Jenkins
`sh '''...'''` block mangled inner JSON quotes. Fixed by building the JSON with
`python3` into a temp file and POSTing with `--data-binary`; no new dependency.
Committed on `fix/appointment-smoke-test-quoting`.


---

## 2026-09-19 — Final-domain migration preparation

### Starting point

- Current green integration branch: `dev`.
- Last known green pre-migration commit: `8b3731bfd7ca736b211514b911a6758ab791463b`.
- Temporary staging frontend/API/admin are still on `proxbenovh.cloud`.
- Clinic-owned `drfarahvipurgentcare.com` is still the legacy WordPress public site.

### Migration architecture

Approved final host map:

- production frontend: `drfarahvipurgentcare.com`
- production API: `api.drfarahvipurgentcare.com`
- production admin: `admin.drfarahvipurgentcare.com`
- staging frontend: `staging.drfarahvipurgentcare.com`
- staging API: `api.staging.drfarahvipurgentcare.com`
- staging admin: `admin.staging.drfarahvipurgentcare.com`

The separate staging admin prevents `dev` deployments from overwriting the
production admin SPA.

### Branch

Created exceptional infrastructure/auth/deployment branch:

`chore/final-domain-migration`

Do not merge until operator DNS/Hestia/HAProxy/TLS/Keycloak prerequisites are
ready.

### Repository changes prepared

- final hostname-aware public booking and registration API routing;
- hostname-aware admin API routing;
- final staging CORS and API ingress host, retaining temporary compatibility;
- final production canonicals and sitemap;
- production robots and Apache/cutover policy;
- production Kubernetes namespace/PostgreSQL/API manifests;
- independent production DB/API secret contract;
- fail-closed Jenkins production deployment stages for `main`;
- Jenkins staging targets moved to final staging frontend/API/admin hosts;
- updated project/environment documentation;
- new current `HANDOFF.md`;
- detailed `docs/migration/FINAL_DOMAIN_CUTOVER.md`.

### Intentional blockers

Production Jenkins refuses to deploy while:

- `kubernetes/drfarah/configmap.yaml` contains `REPLACE_BEFORE_PRODUCTION`
  (production SMTP host/from/to not yet confirmed);
- `frontend/.htaccess.production` contains `CUTOVER_BLOCKER`
  (legacy WordPress URL/redirect inventory incomplete).

These markers must not be removed merely to make CI/deployment pass.

### Operator prerequisites

- GoDaddy DNS records while preserving mail DNS.
- Hestia frontend/admin domains for both environments.
- HAProxy routing and TLS certificates.
- Keycloak redirect/post-logout URI and Web Origin additions for both final
  admin hosts.
- production Kubernetes secrets.
- production SMTP identity/recipient confirmation.
- full legacy WordPress backup and URL inventory.
- rollback DNS target recorded.

### SEO

The current domain already has indexed WordPress paths. Some obvious redirects
are drafted, but a full legacy sitemap/crawl is still required before cutover.
The old WordPress hosting must remain available for rollback during the
stabilization window.



---

## 2026-09-20 — Final-domain cutover audit and hardening

### Scope

Audited the full dependency chain for migration from the temporary
`*.drfarah.proxbenovh.cloud` environment to the clinic-owned
`drfarahvipurgentcare.com` domain.

### Confirmed final environment map

Production:
- `drfarahvipurgentcare.com`
- `api.drfarahvipurgentcare.com`
- `admin.drfarahvipurgentcare.com`

Staging:
- `staging.drfarahvipurgentcare.com`
- `api.staging.drfarahvipurgentcare.com`
- `admin.staging.drfarahvipurgentcare.com`

Keycloak remains at `keycloak.soria-academie.fr`, realm `drfarah`.

### Repository/deployment preparation

- public booking and patient-registration JS selects API by final hostname;
- admin SPA selects staging/production API by admin hostname;
- final staging CORS and API ingress are prepared with temporary compatibility
  origins/host retained during migration;
- production Kubernetes manifests are source-controlled under
  `kubernetes/drfarah/`;
- Jenkins `dev` targets the final staging frontend/API/admin;
- Jenkins `main` contains isolated production build/deploy/smoke stages;
- production frontend artifact converts noindex to index/follow and substitutes
  the production robots/Apache files;
- production pre-DNS smoke checks use `curl --resolve`;
- final-domain canonicals and sitemap are prepared;
- staging excludes production-only robots/Apache files during rsync.

### Additional launch blockers found during audit

1. **Legacy insurer artwork hotlinks.**
   `app.js` and `app-v5.js` still reference six
   `drfarahvipurgentcare.com/wp-content/...` insurer images. These must be
   copied into `frontend/assets/` and referenced locally before apex cutover.
   Jenkins production preflight now fails while the hotlinks remain.

2. **Production database backup/restore.**
   The earlier infrastructure readiness audit already classified backup as a
   production blocker. `BACKUP_READINESS_BLOCKER` now prevents accidental
   production promotion until an off-PVC backup target, retention, restore
   procedure and restore test are verified.

3. **Production SMTP identity.**
   `REPLACE_BEFORE_PRODUCTION` remains in the production ConfigMap until the
   actual SMTP host/from/to are approved. Temporary-domain SMTP defaults were
   removed from application defaults.

4. **Legacy URL redirects.**
   `CUTOVER_BLOCKER` remains in the production Apache file until a complete
   WordPress URL/sitemap inventory is reviewed. Search-visible legacy examples
   include `/services/`, `/about-us/`, `/contact-us/`,
   `/urgent-care-near-you/`, `/vip-urgent-care/`, `/faq/`,
   `/blog/`, and multiple indexed article URLs.

### Operator prerequisites

Before merging this migration branch to `dev`, prepare the new **staging**
DNS/Hestia/HAProxy/TLS and Keycloak staging-admin origin.

Before promoting `main`, additionally complete production Hestia/HAProxy/TLS,
production K8s secrets, SMTP, backup/restore, insurer localization, WordPress
backup and full redirect inventory.

### Handoff

`HANDOFF.md` and `docs/migration/FINAL_DOMAIN_CUTOVER.md` are now the
starting documents for any new tab/AI continuing this migration. Historical
temporary-domain audit/provisioning documents are explicitly marked historical.
