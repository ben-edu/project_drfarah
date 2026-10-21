# Decisions — Dr. Farah VIP Urgent Care

Only approved decisions belong in this file. Do not add hypotheses or proposed
technology/content choices as decisions.

## Project identity

- **Slug:** `drfarah` (repository, Kubernetes namespace, container image, Keycloak realm).
- **Language:** English — phase 1.
- **Timezone:** `America/Los_Angeles`.

## Project control model — 2026-10-21

- **DECISION:** GitHub is the durable project memory for roadmap, current handoff,
  approved decisions, stable project facts, code, runbooks and technical evidence.
- **DECISION:** OpenProject remains authoritative for live work-package status,
  assignee, dates, dependencies, milestones and completion.
- **DECISION:** the project will use one active ChatGPT workspace instead of
  maintaining separate chat tabs for each BG workstream.
- **DECISION:** workstream identities BG-00 through BG-90 remain valid and are
  referenced in GitHub/OpenProject even though separate chat tabs may be retired.
- **DECISION:** `PROJECT_HANDOFF.md` is the live cross-workstream resume point;
  `HANDOFF.md` remains the detailed historical website/deployment handoff.
- **DECISION:** a blocked roadmap item may be bypassed only when its dependency,
  restart condition and hard/soft blocker status are documented and the next
  task is safe to execute independently.
- **DECISION:** no material project decision, blocker or next-step dependency
  should exist only in chat.

## Google marketing control — 2026-10-21

- **DECISION:** Behnam has been granted administrative access to Google Ads and
  Google Business Profile and will directly coordinate their operational work.
- **DECISION:** Google Ads and Google Business / Local SEO / Reputation are
  operated from the same active ChatGPT workspace because their measurement,
  landing-page, local-search and conversion dependencies overlap.
- **DECISION:** live Google Ads is authoritative for current Ads configuration;
  live verified GBP is authoritative for current profile configuration;
  Search Console is authoritative for the organic Search data it reports.
- **DECISION:** the current Google Ads phase is a pre-launch configuration and
  measurement-readiness audit because no campaign history/spend has yet been
  confirmed.
- **DECISION:** do not launch meaningful paid traffic until the booking path and
  measurement foundation have been validated.
- **DECISION:** default connected-account operating mode is
  `read → analyze → recommend → approve → change → validate → measure`.

## Domains

The final clinic-domain migration is approved as a controlled cutover.

Production:
- `drfarahvipurgentcare.com`
- `api.drfarahvipurgentcare.com`
- `admin.drfarahvipurgentcare.com`

Staging:
- `staging.drfarahvipurgentcare.com`
- `api-staging.drfarahvipurgentcare.com`
- `admin-staging.drfarahvipurgentcare.com`

The old `*.drfarah.proxbenovh.cloud` hosts are transition/rollback compatibility
hosts only. Keycloak remains on `keycloak.soria-academie.fr`.

Staging and production admin hostnames are deliberately separate so a `dev`
deployment cannot overwrite the production admin SPA. See
`docs/migration/FINAL_DOMAIN_CUTOVER.md` for the cutover sequence and gates.

## Infrastructure placement

- **Frontend (public + admin):** static output on Hestia / BM1.
- **API:** FastAPI on K3s / BM2, Traefik ingress.
- **Database:** PostgreSQL, dedicated database and credentials for `drfarah`.
- **Admin auth:** Keycloak realm `drfarah`, client `drfarah-admin`, PKCE S256.
- **Registry:** `harbor.proxbenovh.cloud/devops-project-harbor/drfarah-api`.

Current email transport and production evidence are maintained in the live
technical handoff/runbook; do not use older transport wording in this file as a
substitute for current configuration evidence.

## Product scope

- Booking-first, minimal-navigation product.
- The legacy website is a research input, not a migration template.
- Phase 1 excludes clinical AI, EHR integration, lab interpretation, online
  payment unless separately approved, and AI phone receptionist.

## CI/CD

- Jenkins-only deployment.
- No secrets in Git — safe examples/references only.
- Proposed changes use separate branches/PRs; `dev` integrates/stages and `main`
  represents production.

## Environment isolation

- Separate Kubernetes namespaces for staging and production:
  - `drfarah` — production.
  - `drfarah-staging` — staging.
- Separate Deployments, Services, Ingresses, Secrets, PVCs and PostgreSQL
  instances per environment.
- Frontend staging and production have separate Hestia docroots.
- Jenkins mapping: feature/fix/docs branches validate, `dev` deploys staging,
  `main` deploys production after approval.
- See `docs/architecture/ENVIRONMENT_ISOLATION.md` for full rationale.
