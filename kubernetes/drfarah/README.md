# Kubernetes — drfarah namespace (PRODUCTION — reserved)

Production namespace for the Dr. Farah VIP Urgent Care project.

**Important:** This namespace is reserved for production deployment only.
Staging uses a separate `drfarah-staging` namespace with independent
Deployments, Services, Secrets, PVCs, and databases.

See `docs/architecture/ENVIRONMENT_ISOLATION.md` for the full rationale.

## Current state

- Namespace created and labeled (Step 02).
- Harbor pull secret (`harbor-regcred`) present.
- No application workloads deployed yet.

## Planned resources

- `drfarah-postgres` StatefulSet + Service + PVC
- `drfarah-api` Deployment + ClusterIP Service
- `drfarah-api` Traefik Ingress for `api.drfarah.proxbenovh.cloud`

## Notes

- Production resources must only be deployed from the `main` branch via Jenkins.
- Do not overwrite or reuse production database credentials in staging.
- Commit only `*.example` files for secrets.
