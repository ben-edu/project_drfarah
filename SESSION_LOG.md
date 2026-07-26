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
