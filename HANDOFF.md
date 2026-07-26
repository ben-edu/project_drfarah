# HANDOFF — 2026-07-26 (Step 03A)

## Current state

- **Branch:** `feature/api-foundation`
- **Commit:** see `SESSION_LOG.md` for the commit SHA after push.
- **Base:** `dev` (Step 02 infrastructure foundation merged).

## Work completed (Step 03A — FastAPI Application Foundation)

### API application
- FastAPI scaffold with two health endpoints:
  - `GET /api/v1/health/live` — liveness probe.
  - `GET /api/v1/health/ready` — readiness probe with database check.
- Environment-based configuration (Pydantic Settings).
- SQLAlchemy database abstraction (lazy engine, session management).
- CORS middleware with configurable origins.
- 10 passing tests (liveness, readiness, CORS, safety).
- Dockerfile (python:3.12-slim, non-root user, healthcheck).

### Kubernetes staging templates
- 9 non-secret manifests under `kubernetes/drfarah-staging/`:
  namespace, ConfigMap, secret.example.yaml, PostgreSQL StatefulSet,
  PostgreSQL Service, API Deployment, API Service, API Ingress, README.

### Environment isolation
- `drfarah` = production namespace (reserved).
- `drfarah-staging` = staging namespace (separate resources, DB, credentials).
- Documented in `docs/architecture/ENVIRONMENT_ISOLATION.md` and `docs/DECISIONS.md`.

### Jenkinsfile
- Removed bootstrap "no application code" guard.
- Added API test stage (containerized pytest).
- Added Docker build validation stage.
- Still no credentials, no image push, no deploy, no kubectl, no rsync.

### Documentation
- Updated: `api/README.md`, `kubernetes/drfarah/README.md`,
  `docs/DECISIONS.md`, `docs/architecture/README.md`, `HANDOFF.md`,
  `SESSION_LOG.md`.
- Created: `docs/architecture/ENVIRONMENT_ISOLATION.md`.

## What was NOT done (intentionally)

- No booking entities or endpoints.
- No database tables or seed data.
- No Alembic migrations.
- No PostreSQL StatefulSet applied to the cluster.
- No Docker image pushed to Harbor.
- No Kubernetes manifests applied.
- No Jenkins credential binding.
- No Keycloak, SMTP, or frontend code.

## Remaining blockers

1. **Keycloak realm** — still blocked on admin credentials.
2. **Backup destination** — blocker before production.
3. **www → apex redirect** — not yet configured.

## Files the next session must read first

1. `PROJECT.md` — approved product brief (booking scope, data model).
2. `docs/READINESS_AUDIT.md` — current infrastructure readiness.
3. `docs/architecture/ENVIRONMENT_ISOLATION.md` — staging/production design.
4. `HANDOFF.md` — this file.
5. `kubernetes/drfarah-staging/README.md` — staging manifest overview.

## Recommended Step 03B

**Staging deployment and database provisioning:**
1. Create the `drfarah-staging` namespace in K3s.
2. Copy Harbor pull secret into the namespace.
3. Create PostgreSQL credentials and apply the StatefulSet.
4. Build and push the first API image to Harbor (`drfarah-api:dev`).
5. Apply all staging Kubernetes manifests.
6. Add deployment stages to the Jenkinsfile (API build/push, K3s deploy).
7. Verify the API responds at `https://api.staging.drfarah.proxbenovh.cloud`.
