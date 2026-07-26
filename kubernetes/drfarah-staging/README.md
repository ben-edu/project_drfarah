# Kubernetes — drfarah-staging namespace

Staging environment for the Dr. Farah VIP Urgent Care API.

## Manifests

| File | Purpose |
|---|---|
| `namespace.yaml` | `drfarah-staging` namespace with labels |
| `configmap.yaml` | Non-secret API configuration (CORS, DB host, SMTP settings) |
| `secret.example.yaml` | Secret template — commit-only example, never real values |
| `postgres-statefulset.yaml` | PostgreSQL StatefulSet + PVC (`local-path`) |
| `postgres-service.yaml` | PostgreSQL ClusterIP Service |
| `api-deployment.yaml` | FastAPI Deployment (1 replica) |
| `api-service.yaml` | API ClusterIP Service |
| `api-ingress.yaml` | Traefik Ingress for `api.staging.drfarah.proxbenovh.cloud` |

## Environment isolation

- `drfarah` namespace → production (reserved, not yet provisioned).
- `drfarah-staging` namespace → staging (these manifests).
- Separate Deployments, Services, Secrets, PVCs, and databases per
  environment.
- See `docs/architecture/ENVIRONMENT_ISOLATION.md`.

## Current state (Step 05)

Namespace and all resources are deployed and running:

| Resource | Name | Status |
|---|---|---|
| Namespace | `drfarah-staging` | Active |
| Secret | `harbor-regcred` | Present (copied from toilettage) |
| Secret | `drfarah-staging-db-secret` | Present |
| Secret | `drfarah-staging-api-secret` | Present (includes SMTP) |
| ConfigMap | `drfarah-staging-api-config` | Present |
| StatefulSet | `drfarah-staging-postgres` | 1/1 Ready |
| Service | `drfarah-staging-postgres` | ClusterIP:5432 |
| Deployment | `drfarah-staging-api` | 1/1 Ready |
| Service | `drfarah-staging-api` | ClusterIP:80 |
| Ingress | `drfarah-staging-api` | `api.staging.drfarah.proxbenovh.cloud` |

## Secrets (created via kubectl, never committed)

- `drfarah-staging-db-secret` — `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`
- `drfarah-staging-api-secret` — `DATABASE_URL`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `SMTP_*`
- `harbor-regcred` — Docker registry pull secret (copied from `toilettage`)
- SMTP credentials copied from toilettage SMTP pattern

## Image tagging

The Jenkins pipeline derives the image tag from `git rev-parse HEAD` (full
40-character commit SHA). The SHA is validated before every use. Two Harbor
tags are pushed:

- `<full-commit-sha>` — immutable deployment source of truth
- `:dev` — convenience alias only, never deployed directly

The committed `api-deployment.yaml` contains a placeholder image (`:dev`).
At deploy time, Jenkins renders the Deployment with the exact immutable image
using `kubectl set image --dry-run=client` and applies the rendered result.
The `:dev` placeholder is never applied to the cluster.

After rollout, Jenkins verifies that the deployed image matches the expected
commit SHA and fails the build if they differ.

## Migration init container

The API Deployment includes a `db-migrate` init container that runs
`python -m alembic upgrade head` before the main API container starts.
This ensures database migrations execute exactly once, before the API
begins serving traffic.

- If the migration succeeds: the main container starts, readiness probe
  passes, old pod terminates.
- If the migration fails: the init container exits non-zero, pod stays in
  Init phase, old pod keeps running. Rollout times out and Jenkins fails.

The init container uses the same immutable image as the main container.
Both are set by Jenkins at deploy time via `kubectl set image`.

## CI cleanup token

The ConfigMap includes `CLEANUP_TOKEN`, a pre-shared operational token
used by the CI smoke test to call `POST /api/v1/internal/cleanup-ci`
and remove CI-created appointments from previous builds. This token is
not a secret — it protects a CI-only cleanup endpoint, not sensitive data.

## Jenkins deployment (dev branch)

On `dev` builds, Jenkins:
1. Builds the API Docker image
2. Pushes to Harbor (`harbor.proxbenovh.cloud/devops-project-harbor/drfarah-api`)
   with both commit SHA and `:dev` tags
3. Applies K8s manifests (Deployment rendered with immutable SHA for both
   `api` and `db-migrate` containers)
4. Rolls out and verifies API health, CI cleanup, services/availability
   endpoints, booking endpoint (legacy), and appointment endpoint
5. Verifies the deployed image matches the immutable commit SHA

Feature branches run validation only. No deployment.
