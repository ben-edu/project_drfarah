# HANDOFF — 2026-07-26 (Step 02)

## Current state

- **Branch:** `feature/infrastructure-foundation`
- **Commit:** see `SESSION_LOG.md` for the commit SHA after push.
- **Base:** `dev`

## Work completed (Step 02 — Infrastructure Foundation)

### TLS
- Operator re-issued all certificates. All 6 hosts verified: ssl_verify=0,
  matching SANs, valid until Oct 24 2026.
- www → apex redirect NOT configured (both serve 200 — needs HAProxy/Hestia fix).

### Hestia / BM1
- Created `staging.drfarah.proxbenovh.cloud` vhost (was missing).
- All 3 vhosts confirmed: `drfarah`, `staging`, `admin` — owner `benweb`,
  `public_html/` writable.
- Admin 503 resolved (now 200).

### K3s / BM2
- Created `drfarah` namespace with labels.
- Copied Harbor pull secret (`harbor-regcred`) from `toilettage` namespace.

### Keycloak
- Realm `drfarah` NOT created — blocked on admin credentials (bootstrap
  password was rotated).
- Admin username confirmed: `admin`.
- Configuration spec documented in `docs/architecture/INFRASTRUCTURE_FOUNDATION.md`.

### Harbor
- Classified `drfarah-api` as NOT REQUIRED YET — auto-creates on first push.

### PostgreSQL / SMTP / Backup
- PostgreSQL pattern documented (follow `toilettage-postgres`).
- SMTP pattern documented.
- Backup identified as BLOCKER before production (no destination defined).

### Documentation
- Updated `docs/READINESS_AUDIT.md` with all Step 02 results.
- Created `docs/architecture/INFRASTRUCTURE_FOUNDATION.md`.
- Updated `HANDOFF.md` and `SESSION_LOG.md`.

## Remaining blockers

1. **Keycloak realm** — requires admin credentials. See config spec in
   `docs/architecture/INFRASTRUCTURE_FOUNDATION.md`.
2. **www → apex redirect** — configure in HAProxy or Hestia.
3. **Backup destination** — define before production.

## Files the next session must read first

1. `PROJECT.md`
2. `docs/READINESS_AUDIT.md` (updated)
3. `docs/architecture/INFRASTRUCTURE_FOUNDATION.md`
4. `docs/DECISIONS.md`
5. `HANDOFF.md` (this file)

## Recommended Step 03

**Application skeleton and database provisioning.** With infrastructure ready:
1. Create the Keycloak realm (requires admin — coordinate with operator).
2. Create PostgreSQL StatefulSet, Service, PVC, and `drfarah-postgres-secret`
   in the `drfarah` namespace.
3. Create the `drfarah-postgres` Jenkins credential.
4. Scaffold the FastAPI application (`api/`) with health endpoint, CORS, and
   database connection.
5. Scaffold the frontend (`frontend/`) with placeholder pages and booking
   entry points.
6. Update the Jenkinsfile with build/test stages (still no deployment to prod).
7. Push first API image to Harbor.
