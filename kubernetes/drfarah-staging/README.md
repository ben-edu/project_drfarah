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

## Jenkins deployment (dev branch)

On `dev` builds, Jenkins:
1. Builds the API Docker image
2. Pushes to Harbor (`harbor.proxbenovh.cloud/devops-project-harbor/drfarah-api`)
3. Applies K8s manifests
4. Updates deployment image tag
5. Rolls out and verifies API health + booking endpoint

Feature branches run validation only. No deployment.
