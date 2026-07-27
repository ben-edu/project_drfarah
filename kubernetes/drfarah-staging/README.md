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

The `CLEANUP_TOKEN` is stored in `drfarah-staging-api-secret` (not the
ConfigMap). It is injected into the API pod via `envFrom.secretRef` alongside
other secrets.

- **Kubernetes:** the token lives in `drfarah-staging-api-secret` with key
  `CLEANUP_TOKEN`. Created via `kubectl create secret generic` — never
  committed.
- **Jenkins:** a matching String credential
  (`drfarah-staging-ci-cleanup-token`) is bound through `withCredentials`
  in the health-check stage. Shell tracing is disabled (`set +x`) around
  the authenticated curl so the token never appears in build logs.
- The token is operational (not a user authentication secret) but must not
  appear in committed code, ConfigMaps, or logs.

> **Token rotation mandatory:** the previous token
> (`staging-ci-cleanup-token-2026`) was committed in the ConfigMap and
> Jenkinsfile. It was removed in commit `<TBD>` on branch
> `fix/scheduling-staging-deployment`. Rotate the token before the next
> deploy.

## Jenkins deployment (dev branch)

On `dev` builds, Jenkins:
1. Builds the API Docker image
2. Pushes to Harbor (`harbor.proxbenovh.cloud/devops-project-harbor/drfarah-api`)
   with both commit SHA and `:dev` tags
3. Renders the Deployment manifest to a temp file with both the `api` and
   `db-migrate` container images set to the immutable SHA. Validates that
   both image fields match before applying. Does NOT pipe into `kubectl
   apply` (POSIX sh without `pipefail` masks rendering failures).
4. Applies the validated rendered manifest
5. Rolls out and verifies API health, CI cleanup, services/availability
   endpoints, booking endpoint (legacy), and appointment endpoint
6. Verifies the deployed image for BOTH the `api` container and the
   `db-migrate` init container match the immutable commit SHA

Feature branches run validation only. No deployment.
