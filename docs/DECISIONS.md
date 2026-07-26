# Decisions — Dr. Farah VIP Urgent Care

Only approved decisions that are already known and documented in
`PROJECT.md` or the infrastructure baseline. Do not add speculative
technology or content choices.

## Project identity

- **Slug:** `drfarah` (repository, Kubernetes namespace, container image,
  Keycloak realm).
- **Language:** English — phase 1.
- **Timezone:** `America/Los_Angeles`.

## Domains

Temporary development/staging/production domains under `proxbenovh.cloud`
(see `README.md`). OVH DNS and HAProxy routing configured by the operator.

## Infrastructure placement

- **Frontend (public + admin):** static output on Hestia / BM1.
- **API:** FastAPI on K3s / BM2, Traefik ingress.
- **Database:** PostgreSQL, dedicated database and credentials for `drfarah`.
- **Admin auth:** Keycloak realm `drfarah`, client `drfarah-admin`, PKCE S256.
- **Email:** SORIA SMTP for testing; clinic-approved sender for production.
- **Registry:** `harbor.proxbenovh.cloud/devops-project-harbor/drfarah-api`.

## Product scope

- Booking-first, minimal-navigation product.
- The current `drfarahvipurgentcare.com` website is a research input — not a
  migration template.
- Phase 1 excludes clinical AI, EHR integration, lab interpretation, online
  payment (unless separately approved), and AI phone receptionist.

## CI/CD

- Jenkins-only deployment.
- No secrets in Git — `*.example` patterns only.
- Credential IDs: `hestia-benweb-ssh`, `harbor-robot-devops-project-harbor`,
  `drfarah-postgres`, `drfarah-smtp`.
