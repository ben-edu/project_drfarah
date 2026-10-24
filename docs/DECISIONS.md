# Decisions — Dr. Farah VIP Urgent Care

Only approved decisions belong in this file. Do not add hypotheses or proposed technology/content choices as decisions.

## Project identity

- **Slug:** `drfarah` (repository, Kubernetes namespace, container image, Keycloak realm).
- **Language:** English — phase 1.
- **Timezone:** `America/Los_Angeles`.

## Project control model — 2026-10-21, refined 2026-10-24

- **DECISION:** GitHub is the durable project memory for roadmap, current handoff, approved decisions, stable project facts, code, runbooks and technical evidence.
- **DECISION:** `ROADMAP.md` is the single master sequencing document for website, marketing, growth, analytics, operations and related workstreams. Detailed runbooks/specs may exist, but no competing roadmap should be maintained.
- **DECISION:** OpenProject remains authoritative for live work-package status, assignee, dates, dependencies, milestones and completion.
- **DECISION:** the existing `BG-20` ChatGPT project tab will remain as the single active project workspace; the other specialized tabs may be retired after the unified GitHub control plane and Project Source routers are verified.
- **DECISION:** workstream identities BG-00 through BG-90 remain valid and are referenced in GitHub/OpenProject even though separate chat tabs are retired.
- **DECISION:** `PROJECT_HANDOFF.md` is the live cross-workstream resume point; `HANDOFF.md` remains detailed historical website/deployment evidence.
- **DECISION:** a blocked roadmap item may be bypassed only when its dependency, restart condition and hard/soft blocker status are documented and the next task is safe to execute independently.
- **DECISION:** no material project decision, blocker or next-step dependency should exist only in chat.
- **DECISION:** ChatGPT Project Source `.md` files should be minimal bootstrap/router documents; they must not become a parallel source of business/project truth. GitHub and current live systems supersede them according to the authority hierarchy.

## Google marketing control — updated 2026-10-24

- **DECISION:** Behnam has administrative access to Google Ads and Google Business Profile and will directly coordinate their operational work from the unified project workspace.
- **DECISION:** Google Ads and Google Business / Local SEO / Reputation are operated from the same active workspace because measurement, landing-page, local-search and conversion dependencies overlap.
- **DECISION:** live Google Ads is authoritative for current Ads configuration/performance; live verified GBP is authoritative for current profile configuration; Search Console is authoritative for organic Google Search data it reports; GA4 is authoritative for its configured analytics reporting.
- **DECISION:** the prior assumption that Google Ads had never run is superseded by live account evidence. BG20-01 is a **historical forensic audit + relaunch-readiness audit**.
- **DECISION:** do not launch or materially scale paid traffic until booking and measurement hard gates are validated.
- **DECISION:** default connected-account operating mode is `read → analyze → recommend/act within authorization → validate → measure → record evidence`.
- **DECISION:** platform-reported conversions are not assumed to equal completed patient visits.
- **DECISION:** `visit_completed` is the intended primary business-outcome conversion once reliable source/appointment linkage and Google Ads import are validated; `booking_request_created` remains a lead/secondary signal rather than a completed visit.
- **DECISION:** the project should use useful lawful/platform-compliant marketing measurement and attribution without arbitrary self-imposed restrictions, while excluding unnecessary medical-record detail and respecting applicable privacy/consent/platform requirements.
- **DECISION:** the Google Business service catalogue will not be bulk-reduced merely because it is extensive. Services will be evaluated for factual availability, demand, economics, clarity, duplication, conversion usefulness, claims/pricing accuracy and platform policy before change.

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

The old `*.drfarah.proxbenovh.cloud` hosts are transition/rollback compatibility hosts only. Keycloak remains on `keycloak.soria-academie.fr`.

Staging and production admin hostnames are deliberately separate so a `dev` deployment cannot overwrite the production admin SPA. See `docs/migration/FINAL_DOMAIN_CUTOVER.md` for the detailed historical cutover procedure and gates where still relevant.

## Infrastructure placement

- **Frontend (public + admin):** static output on Hestia / BM1.
- **API:** FastAPI on K3s / BM2, Traefik ingress.
- **Database:** PostgreSQL, dedicated database and credentials for `drfarah`.
- **Admin auth:** Keycloak realm `drfarah`, client `drfarah-admin`, PKCE S256.
- **Registry:** `harbor.proxbenovh.cloud/devops-project-harbor/drfarah-api`.

Current email transport and production evidence are maintained in the live technical handoff/runbook; do not use older transport wording in this file as a substitute for current configuration evidence.

## Product scope

- Booking-first, minimal-navigation product.
- The legacy website is a research input, not a migration template.
- Phase 1 excludes clinical AI, EHR integration, lab interpretation, online payment unless separately approved, and AI phone receptionist.
- Growth/marketing work may create evidence-backed landing pages and tracking requirements, but changes follow repository/Jenkins controls.

## CI/CD

- Jenkins-only deployment.
- No secrets in Git — safe examples/references only.
- Proposed changes use separate branches/PRs; `dev` integrates/stages and `main` represents production.

## Environment isolation

- Separate Kubernetes namespaces for staging and production:
  - `drfarah` — production.
  - `drfarah-staging` — staging.
- Separate Deployments, Services, Ingresses, Secrets, PVCs and PostgreSQL instances per environment.
- Frontend staging and production have separate Hestia docroots.
- Jenkins mapping: feature/fix/docs branches validate, `dev` deploys staging, `main` deploys production after approval.
- Measurement implementation must preserve staging/production analytics isolation.
- See `docs/architecture/ENVIRONMENT_ISOLATION.md` for full rationale.
