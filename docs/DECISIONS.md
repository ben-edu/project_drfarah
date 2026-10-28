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

## Growth Acceleration operating model — approved 2026-10-28

- **DECISION:** the project objective is an integrated growth/marketing system across Google Ads, Search Console, Google Business Profile, GA4, first-party attribution, the website/landing paths, completed-visit measurement, service economics, AI/ChatGPT Ads, partner/referral channels and Growth Intelligence.
- **DECISION:** execution is parallel by default. A blocker in one lane must not stall safe independent work in another lane.
- **DECISION:** production is the destination for validated growth infrastructure. Coherent changes should be promoted from `dev` to `main` promptly after normal quality/staging gates rather than left indefinitely in development.
- **DECISION:** related changes should be batched before CI/build to reduce unnecessary build cycles; quality/correctness is not to be sacrificed to reduce build count.
- **DECISION:** historical Google Ads campaigns/settings must be mined for useful evidence before cleanup or deletion. Obsolete objects may then be archived/removed when safe.
- **DECISION:** the paused legacy Smart campaign is not the default relaunch vehicle. The first new paid experiment should use a more controllable architecture, expected to be Search unless current evidence demonstrates a better alternative.
- **DECISION:** missing exact clinic economics must not block campaign research/design. Explicit provisional assumptions may be used from live market/account evidence and must be replaced when authoritative revenue/margin/capacity figures become available.
- **DECISION:** AI/ChatGPT advertising is a serious paid-channel workstream. Current eligibility/policy must be verified before spend, and any pilot must use finite budget, measurement and stop/scale rules.
- **DECISION:** `PROJECT_HANDOFF.md` must be updated after material sessions so a new tab/operator can resume without reconstructing the project from chat history.

## Google marketing control — updated 2026-10-28

- **DECISION:** Behnam has administrative access to Google Ads and Google Business Profile and will directly coordinate their operational work from the unified project workspace.
- **DECISION:** Google Ads, Google Business / Local SEO / Reputation, Search Console, GA4 and the website are operated as one integrated acquisition system because their measurement, landing-page, local-search and conversion dependencies overlap.
- **DECISION:** live Google Ads is authoritative for current Ads configuration/performance; live verified GBP is authoritative for current profile configuration; Search Console is authoritative for organic Google Search data it reports; GA4 is authoritative for its configured analytics reporting.
- **DECISION:** the prior assumption that Google Ads had never run is superseded by live account evidence. BG20-01 is a historical forensic audit + relaunch-readiness audit.
- **DECISION:** do not materially scale paid traffic until booking and completed-visit measurement hard gates are validated. Small controlled learning spend may begin only when the experiment-specific minimum booking/landing/measurement dependencies are satisfied.
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
