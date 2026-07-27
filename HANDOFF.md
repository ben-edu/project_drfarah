# HANDOFF — 2026-07-27 (Fix: Bootstrap Legacy Alembic State)

## Current state

- **Branch:** `fix/bootstrap-legacy-alembic-state`
- **Base:** `dev` (5a9aca2 — Step 07-FIX merged + Alembic-in-image fix)
- **Status:** all code, tests, and docs complete; awaiting operator review and push

## Previous state

Step 07 (Real Availability and Appointment Scheduling) was merged into `dev`
(ad8b38a) but the live `dev` staging deployment failed with 5 errors.
See SESSION_LOG.md for the full incident report.

All 5 errors from Step 07-FIX were resolved. However, a separate problem
remained: the Jenkins CI pipeline validates migrations against a clean SQLite
database, but staging PostgreSQL already had a `bookings` table created by the
application's `Base.metadata.create_all()` at startup. This legacy table
predates Alembic — there is no Alembic revision and migration 0001 tries to
CREATE the table that already exists.

## Fix: Migration bootstrap state machine

Created `api/app/migration_bootstrap.py` — a safe state machine that handles
four database states:

- **State 1 (Fresh):** No bookings table, no Alembic revision → `alembic upgrade head`
- **State 2 (Legacy):** bookings table exists, matches 0001 schema, no Alembic
  revision → validate schema, stamp 0001, upgrade head. Existing bookings are
  **preserved** — the table is never dropped or recreated.
- **State 3 (Managed):** Valid Alembic revision present → `alembic upgrade head`
- **State 4 (Unsafe):** Schema mismatch, corrupt revision table, or other
  inconsistent state → fail closed with diagnostic log. No partial changes.

The K8s init container now runs `python -m app.migration_bootstrap` instead of
`python -m alembic upgrade head`.

This is NOT a manual one-time procedure — it runs as the init container on
every pod creation and correctly handles all four states idempotently.

## Legacy schema validation

Before stamping 0001 on a legacy database, the bootstrap validates every
column in the existing `bookings` table against the expected 0001 schema:
column names, types, nullability, and primary key. If any required column is
missing or incompatible, the bootstrap fails closed — no stamp, no partial
migration, no data loss.

## Tests (13 PostgreSQL integration tests)

`api/tests/test_migration_bootstrap.py` — comprehensive integration tests
against disposable PostgreSQL databases (`sudo -u postgres createdb/dropdb`):

| Test class | State | Tests |
|---|---|---|
| `TestFreshDatabase` | State 1 | 5 — all tables created, seeds exist, head reached, idempotent |
| `TestLegacyDatabase` | State 2 | 4 — stamped 0001, upgraded, rows preserved, not recreated, idempotent |
| `TestEmptyAlembicVersion` | State 2 edge | 1 — empty version table treated as legacy |
| `TestUnsafeIncompatibleSchema` | State 4 | 1 — missing required column rejected, no stamp |
| `TestAlreadyManaged` | State 3 | 2 — upgrades from 0001, no-op at head |

Full suite: **83 passed, 1 skipped** (137s).

## CI validation

Jenkinsfile "API — migration bootstrap validation" stage validates:
- Bootstrap file and test file exist
- Module imports cleanly
- Bootstrap runs against a fresh SQLite database

## Why plain `alembic upgrade head` failed

The staging database had a `bookings` table created by
`Base.metadata.create_all()` (from the application startup before Alembic
existed). Migration 0001 tries to CREATE TABLE bookings — but the table
already exists. PostgreSQL rejects the duplicate CREATE and the migration
fails. The bootstrap detects this legacy state, validates the schema,
stamps the migration, and applies only later migrations.

## Manual stamping not required

The bootstrap state machine is the normal, automated deployment procedure.
No manual `alembic stamp` on staging or production is needed — the init
container detects the state and applies the correct action automatically.

## Recommended next steps

1. Review the changes on this branch.
2. Push and open a PR into `dev`.
3. After merge, trigger a `dev` build and verify:
   - Init container runs migration bootstrap successfully on staging PostgreSQL
   - Staging API health check passes
   - Existing bookings are preserved after bootstrap

### Fix 1 — Deployment rendering (CRITICAL)

**Problem:** `kubectl set image` cannot target init containers — it only
updates `spec.containers`. The db-migrate init container was left at `:dev`.
The pipe `| kubectl apply -f -` masked the rendering failure because POSIX sh
lacks `pipefail`.

**Fix:** Render the Deployment to a temp file via `sed` (replacing the `:dev`
placeholder with the immutable SHA globally). Validate 2 image lines contain
the immutable image. Validate no `:dev` placeholder remains. Apply the
validated temp file directly — no pipe. Clean up the temp file after apply.

### Fix 2 — Compromised cleanup token

**Problem:** `CLEANUP_TOKEN = 'staging-ci-cleanup-token-2026'` was committed
in `Jenkinsfile` (environment block) and `configmap.yaml`. Printed in Jenkins
logs via the curl Authorization header.

**Fix:**
- Removed from `Jenkinsfile` environment block. Now uses `withCredentials`
  with a String credential (`drfarah-staging-ci-cleanup-token`).
- `set +x` / `set -x` around the authenticated curl prevents token in logs.
- Removed from `configmap.yaml`. Moved to `drfarah-staging-api-secret`
  (injected via existing `envFrom.secretRef`).
- Updated `secret.example.yaml` with CLEANUP_TOKEN field.
- **Token rotation is mandatory** before next deploy.

### Fix 3 — Availability smoke test

**Problem:** Hardcoded `service_code=urgent-care` on a single date. If
`urgent-care` isn't seeded or the date has no slots, the test fails
incorrectly.

**Fix:** Smoke test now calls `GET /api/v1/services`, validates at least one
active service exists, picks the first one. Queries availability over a
14-day window. Picks the first returned slot for the appointment smoke test.
Uses `python3` for JSON parsing (available on Jenkins agent).

### Fix 4 — Root cause of 404

**Diagnosis:** The init container ran the old `:dev` image (kubectl set image
couldn't update it), so Alembic migrations never ran. The `services` table
was never seeded → `GET /api/v1/availability?service_code=urgent-care`
returned 404 because no service with code `urgent-care` existed.

**Fix:** Fix 1 ensures the init container gets the immutable image with the
migration code. Fix 3 makes the test resilient in case any individual service
is missing.

### Fix 5 — False success from piped commands

**Problem:** Without `pipefail`, the `kubectl set image` failure (exit code 1)
was discarded — only `kubectl apply` exit code (0) mattered.

**Fix:** The deployment rendering no longer uses a pipe. See Fix 1.

### Fix 6 — Cleanup endpoint security

**Validated:**
- Only deletes records where `source='ci'` — never touches real appointments.
- 1-hour grace period prevents race conditions.
- Returns 401 for wrong/missing token (not 403 — avoids user enumeration).
- Token is operational (not a user authentication secret). Constant-time
  comparison is not required for this use case.

**Applied:**
- `set +x` / `set -x` around the authenticated curl in Jenkins.
- Token moved from ConfigMap to Secret (defense in depth).

### Fix 7 — Documentation

- Updated this HANDOFF.md.
- Updated SESSION_LOG.md with incident report and fix summary.
- Updated `kubernetes/drfarah-staging/README.md` with token rotation notice
  and corrected deployment rendering description.

## Recommended next steps

1. **Rotate the cleanup token before any deploy.** The old token
   (`staging-ci-cleanup-token-2026`) was committed in two files and must be
   replaced in both the live Kubernetes Secret and the Jenkins credential.
2. Review the changes on this branch.
3. Push and open a PR into `dev`.
4. After merge, trigger a `dev` build and verify:
   - Deployment renders with both containers set to the immutable SHA.
   - Init container runs migrations successfully.
   - Services and availability endpoints return real data.
   - CI cleanup + dynamic appointment smoke test pass.
5. Do not start Keycloak/admin UI until scheduling is verified end-to-end.

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
