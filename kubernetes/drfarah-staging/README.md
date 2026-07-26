# Kubernetes — drfarah-staging namespace

Staging environment for the Dr. Farah VIP Urgent Care API.

## Manifests

| File | Purpose |
|---|---|
| `namespace.yaml` | `drfarah-staging` namespace with labels |
| `configmap.yaml` | Non-secret API configuration (CORS, DB host, etc.) |
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

## Status

Templates only — not yet applied to the cluster. Provisioning is Step 03B.

## Applying (future)

```bash
kubectl apply -f namespace.yaml
# Copy Harbor pull secret into the namespace:
kubectl -n drfarah-staging create secret docker-registry harbor-regcred \
  --from-literal=.dockerconfigjson='...'
# Create runtime secrets (use real values, not the example):
kubectl -n drfarah-staging create secret generic drfarah-staging-db-secret \
  --from-literal=POSTGRES_USER=drfarah \
  --from-literal=POSTGRES_PASSWORD='<strong-password>' \
  --from-literal=POSTGRES_DB=drfarah
kubectl -n drfarah-staging create secret generic drfarah-staging-api-secret \
  --from-literal=DATABASE_URL='postgresql+psycopg://drfarah:<password>@drfarah-staging-postgres:5432/drfarah'
kubectl apply -f configmap.yaml
kubectl apply -f postgres-statefulset.yaml
kubectl apply -f postgres-service.yaml
kubectl apply -f api-deployment.yaml
kubectl apply -f api-service.yaml
kubectl apply -f api-ingress.yaml
```
