# HANDOFF — 2026-07-26 (Step 07-FIX: Repair Staging Deployment)

## Current state

- **Branch:** `fix/scheduling-staging-deployment`
- **Base:** `dev` (ad8b38a — Step 07 merged)
- **Status:** fixes applied, awaiting operator review and push

## Previous state (Step 07)

Step 07 (Real Availability and Appointment Scheduling) was merged into `dev`
(ad8b38a) but the live `dev` staging deployment failed with 5 errors.
See SESSION_LOG.md for the full incident report.

## Fixes applied on `fix/scheduling-staging-deployment`

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
