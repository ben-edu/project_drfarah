# Environment Isolation — Dr. Farah VIP Urgent Care

**Decision date:** 2026-07-26
**Status:** Approved

## Summary

The project uses **separate Kubernetes namespaces** for staging and production
environments. They do not share Deployments, Services, Ingresses, Secrets, PVCs,
or databases.

## Namespace mapping

| Environment | Namespace | Frontend domain | API domain | Admin domain | DB hostname |
|---|---|---|---|---|---|
| Staging | `drfarah-staging` | `staging.drfarahvipurgentcare.com` | `api-staging.drfarahvipurgentcare.com` | `admin-staging.drfarahvipurgentcare.com` | `drfarah-staging-postgres` |
| Production | `drfarah` | `drfarahvipurgentcare.com` | `api.drfarahvipurgentcare.com` | `admin.drfarahvipurgentcare.com` | `drfarah-postgres` |

Target Hestia docroots:
- Staging frontend: `/home/benweb/web/staging.drfarahvipurgentcare.com/public_html`
- Staging admin: `/home/benweb/web/admin-staging.drfarahvipurgentcare.com/public_html`
- Production frontend: `/home/benweb/web/drfarahvipurgentcare.com/public_html`
- Production admin: `/home/benweb/web/admin.drfarahvipurgentcare.com/public_html`

The old `proxbenovh.cloud` hosts are temporary compatibility routes during
migration and must not be treated as the final environment map.

## Why isolation matters

### 1. No cross-contamination

A single Deployment overwritten by both `dev` and `main` branches would cause:
- Staging deploys from `dev` overwriting production pods from `main`.
- Staging database test data appearing in production.
- Configuration leaks (staging CORS origins in production, etc.).

### 2. Independent scaling

Production may need more replicas or different resource limits than staging.
Separate Deployments allow per-environment tuning without affecting the other.

### 3. Safe database separation

Staging and production each have their own PostgreSQL StatefulSet, PVC, and
credentials. A staging database migration, seed change, or data wipe cannot
affect production bookings.

### 4. Predictable rollback

Rolling back production does not affect staging, and vice versa.

## Jenkins branch mapping (future)

| Branch | Action |
|---|---|
| `feature/*` | API tests + Docker build validation only. No deploy. |
| `dev` | Build, push `:dev` image tag, deploy to `drfarah-staging` namespace. |
| `main` | Build, push `:prod` image tag, deploy to `drfarah` namespace (added only after production readiness). |

## Staging-specific Kubernetes resources

All staging resources carry a `staging` suffix in their names:
- `drfarah-staging-api` (Deployment, Service, Ingress)
- `drfarah-staging-postgres` (StatefulSet, Service)
- `drfarah-staging-api-config` (ConfigMap)
- `drfarah-staging-api-secret`, `drfarah-staging-db-secret` (Secrets)

Production resources (in `drfarah` namespace) will use production-prefixed names:
- `drfarah-api`, `drfarah-postgres`, etc.

## CORS origins

- Staging ConfigMap: final staging frontend/admin origins, with temporary old origins retained only during cutover.
- Production ConfigMap: `https://drfarahvipurgentcare.com,https://www.drfarahvipurgentcare.com,https://admin.drfarahvipurgentcare.com`

Production origins must not appear in staging configuration.

## Database credentials

Each environment uses a separate PostgreSQL instance with its own `POSTGRES_USER`,
`POSTGRES_PASSWORD`, and `POSTGRES_DB`. Credentials must never be reused across
environments.
