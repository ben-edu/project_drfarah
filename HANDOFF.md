# HANDOFF — 2026-07-26

## Current state

- **Branch:** `feature/bootstrap-readiness`
- **Commit:** see `SESSION_LOG.md` for the commit SHA after push.
- **Base:** `dev` (created from `main`).

## Work completed

1. Repository initialized and connected to `git@github.com:ben-edu/project_drfarah.git`.
2. Branches created: `main`, `dev`, `feature/bootstrap-readiness`.
3. Full read-only readiness audit performed:
   - DNS resolution for all 6 temporary domains.
   - TLS certificate inspection for all domains.
   - Hestia vhost/docroot check via SSH.
   - K3s cluster connectivity and namespace/resource inspection.
   - Keycloak and Harbor endpoint availability.
   - Jenkins multibranch job confirmed.
4. Repository skeleton created with all required directories and files.
5. Bootstrap Jenkinsfile added (safe, non-deploying).
6. Source document `PROJECT_DRFARAH.md` copied into repository root as
   `PROJECT.md`.

## Audit findings summary

### Ready
- Git repository, branches, remote.
- DNS for all 6 domains.
- TLS for apex domain `drfarah.proxbenovh.cloud`.
- Hestia vhosts: `drfarah.proxbenovh.cloud` and `admin.drfarah.proxbenovh.cloud`.
- K3s cluster connectivity.
- Jenkins multibranch pipeline.
- Keycloak and Harbor endpoints.

### Blocked / Needs action before deployment
- **staging.drfarah.proxbenovh.cloud Hestia vhost:** not created.
- **drfarah K3s namespace:** not created.
- **drfarah Keycloak realm:** not created.
- **TLS cert mismatch:** domains other than the apex present `*.behnam.fr`
  instead of `*.proxbenovh.cloud`.

### NOT REQUIRED YET
- PostgreSQL database, K3s resources, Harbor image repo, SMTP credentials,
  backup configuration — all expected to be missing at this stage.

See `docs/READINESS_AUDIT.md` for the full table with evidence.

## Files the next session must read first

1. `PROJECT.md` — approved product brief.
2. `docs/READINESS_AUDIT.md` — current infrastructure readiness.
3. `HANDOFF.md` — this file.

## Recommended Step 02

**Infrastructure provisioning and TLS fix.** Before any application code:
1. Create the missing `staging.drfarah.proxbenovh.cloud` Hestia vhost (owner:
   `benweb`).
2. Create the `drfarah` K3s namespace and copy the Harbor pull secret.
3. Create the `drfarah` Keycloak realm with the admin client.
4. Resolve TLS certificate mismatch for www, staging, admin, and API domains.
5. Create the `drfarah-postgres` database, credentials, and Jenkins credential.
6. Verify API endpoints respond (404 from Traefik is expected — confirms routing).
