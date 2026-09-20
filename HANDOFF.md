# HANDOFF — 2026-09-20 — Final Domain Migration Preparation

## Read this first

This is the current operational handoff for the Dr. Farah website project.

Authoritative implementation repository:

`ben-edu/project_drfarah`

Current integration branch:

`dev`

Current final-domain migration branch:

`chore/final-domain-migration`

Detailed cutover runbook:

`docs/migration/FINAL_DOMAIN_CUTOVER.md`

For infrastructure details, use `ben-edu/infra-docs`; live infrastructure wins
when documentation and runtime disagree.

---

## Current deployed state before domain cutover

The latest website/application feature release is merged to `dev` and was
successfully deployed to the temporary staging environment.

Last known green integration commit before this migration work:

`8b3731bfd7ca736b211514b911a6758ab791463b`

That release includes:

- revised premium public website and navigation;
- PRP Treatments page;
- Weight Loss Program page;
- combined Traveler & Telehealth entry point;
- IV Therapy & Wellness page;
- Personal Injury / attorney-lien page;
- enhanced Pre-Operative Clearance lien wording;
- variable fees presented with `Starting From` where appropriate;
- public booking against real API services/availability;
- online Patient Registration with Save / Resume / Submit;
- PostgreSQL persistence;
- Alembic head `0003`;
- Keycloak-protected Admin appointment management;
- Admin Patient Registration review.

Known UI backlog:

- the Services-page IV hero image is still visually too soft/blurred and should
  be sharpened in a later focused visual fix;
- critical homepage/service imagery still uses the temporary `app-v5` runtime
  reconstruction workaround. It is stable enough for staging but should
  eventually be replaced by direct static assets.

AI Virtual Assistant / Digital Concierge is explicitly postponed.

---

## Current temporary environment

The currently deployed temporary environment uses:

- frontend staging: `https://staging.drfarah.proxbenovh.cloud`
- API staging: `https://api.staging.drfarah.proxbenovh.cloud`
- admin SPA: `https://admin.drfarah.proxbenovh.cloud`
- Keycloak: `https://keycloak.soria-academie.fr/realms/drfarah`

The temporary admin hostname is effectively a staging admin because the
`dev` Jenkins pipeline deploys to it.

---

## Approved final environment map

### Production

- frontend: `https://drfarahvipurgentcare.com`
- www: `https://www.drfarahvipurgentcare.com` → 301 to apex
- API: `https://api.drfarahvipurgentcare.com`
- admin: `https://admin.drfarahvipurgentcare.com`

### Staging

- frontend: `https://staging.drfarahvipurgentcare.com`
- API: `https://api.staging.drfarahvipurgentcare.com`
- admin: `https://admin.staging.drfarahvipurgentcare.com`

The separate staging admin is intentional. Sharing one admin hostname between
`dev` and `main` would let a staging deploy overwrite the production SPA.

Keycloak stays at `keycloak.soria-academie.fr`; only client redirect URIs and
web origins need the new admin domains.

---

## Migration branch state

Do **not** merge `chore/final-domain-migration` to `dev` until the operator
preflight below is complete.

Repository preparation already on the branch includes:

- final-domain API selection in `frontend/booking.js`;
- final-domain API selection in `frontend/registration.js`;
- environment-aware `admin/config.js`;
- final staging CORS origins;
- final staging Traefik API host while temporarily retaining the old host;
- final production canonical URLs and sitemap;
- production robots policy;
- production Apache/cutover rules;
- production Kubernetes namespace/API/PostgreSQL manifests;
- fail-closed Jenkins `main` production stages;
- final staging hostname/docroot targets in Jenkins;
- production hostname/docroot targets in Jenkins;
- domain migration runbook.

Transition support for the old temporary hosts is intentional until the new
hosts are verified.

---

## Operator-owned prerequisites before merge to dev

### 1. GoDaddy DNS

Preserve nameservers and all unrelated mail records (MX/SPF/DKIM/DMARC).

Prepare:

- apex `@` → BM1/web HAProxy;
- `www` → apex;
- `staging` → BM1/web HAProxy;
- `admin` → BM1/web HAProxy;
- `admin.staging` → BM1/web HAProxy;
- `api` → BM2/API HAProxy;
- `api.staging` → BM2/API HAProxy.

Check stale A/AAAA/CNAME conflicts. Reduce apex/www TTL before final cutover and
record the current WordPress DNS target for rollback.

### 2. Hestia domains/docroots

Create/verify, owned and writable by `benweb`:

- `/home/benweb/web/drfarahvipurgentcare.com/public_html`
- `/home/benweb/web/staging.drfarahvipurgentcare.com/public_html`
- `/home/benweb/web/admin.drfarahvipurgentcare.com/public_html`
- `/home/benweb/web/admin.staging.drfarahvipurgentcare.com/public_html`

### 3. HAProxy and TLS

Configure final frontend/admin routes on BM1 and API routes on BM2.
Install valid certificates for all final hostnames before browser testing.

### 4. Keycloak

Realm: `drfarah`  
Client: `drfarah-admin`

Add:

Valid redirect URIs:
- `https://admin.drfarahvipurgentcare.com/*`
- `https://admin.staging.drfarahvipurgentcare.com/*`

Valid post-logout redirect URIs:
- same values

Web origins:
- `https://admin.drfarahvipurgentcare.com`
- `https://admin.staging.drfarahvipurgentcare.com`

Keep the old temporary admin URI/origin during the transition, then remove it
after stable cutover. Do not use a broad wildcard. Enable/require MFA for real
staff before production.

### 5. Production Kubernetes secrets

In namespace `drfarah`, verify/create:

- `harbor-regcred`
- `drfarah-db-secret`
- `drfarah-api-secret`

Production DB credentials must be independent from staging.

### 6. Production SMTP identity

Confirm the non-secret production values:

- SMTP host;
- SMTP from address;
- clinic notification recipient.

Real SMTP username/password remain out of Git and belong in
`drfarah-api-secret`.

The production ConfigMap intentionally contains
`REPLACE_BEFORE_PRODUCTION` markers until these values are confirmed.

### 7. Legacy WordPress preservation

Before apex DNS cutover:

- back up/export the old WordPress files and database;
- export/crawl the complete legacy URL inventory / XML sitemap;
- retain old DNS target and hosting for rollback;
- prepare 301 mappings for valuable legacy URLs.

The production Apache file intentionally contains a `CUTOVER_BLOCKER` marker
until the full redirect inventory is reviewed.

---

## Repository-side cutover blockers

Production deployment is intentionally fail-closed until all of these are resolved:

1. `REPLACE_BEFORE_PRODUCTION` values in
   `kubernetes/drfarah/configmap.yaml` — production SMTP host/from/to;
2. `CUTOVER_BLOCKER` in `frontend/.htaccess.production` — full legacy URL
   inventory / redirect decisions;
3. legacy insurer images are still hotlinked from
   `drfarahvipurgentcare.com/wp-content/...` in `app.js` / `app-v5.js`.
   The six approved artwork files must be copied into `frontend/assets/` and
   referenced locally before apex cutover;
4. `BACKUP_READINESS_BLOCKER` in `kubernetes/drfarah/README.md` — production
   PostgreSQL backup destination, retention, restore procedure and a restore
   test are not yet verified.

Do not remove a blocker merely to make Jenkins green. Clear each one only after
its prerequisite is actually satisfied.

---

## Required migration sequence

1. Finish operator DNS/Hestia/HAProxy/TLS/Keycloak prerequisites for the **new
   staging hosts**.
2. Run CI on `chore/final-domain-migration`.
3. Review PR and merge to `dev`.
4. Jenkins `dev` deploys to:
   - `staging.drfarahvipurgentcare.com`
   - `api.staging.drfarahvipurgentcare.com`
   - `admin.staging.drfarahvipurgentcare.com`
5. Verify staging end to end:
   - public pages;
   - booking;
   - availability;
   - Patient Registration Save/Resume/Submit;
   - admin Keycloak login;
   - appointment and registration admin views;
   - CORS;
   - noindex + robots Disallow.
6. Complete production SMTP, secrets and legacy redirect inventory.
7. Back up legacy WordPress and record rollback DNS.
8. With explicit human approval, fast-forward `main` to the exact approved
   green `dev` SHA.
9. Jenkins `main` deploys isolated production API/DB/frontend/admin.
10. Validate production routing with `curl --resolve` before apex DNS switch.
11. Switch apex/www DNS.
12. Verify canonical, robots, sitemap, redirects, booking, API, admin and
    Keycloak after public cutover.
13. Submit the new sitemap in Google Search Console.
14. Keep old WordPress hosting and temporary Dr. Farah routes available during
    the stabilization/rollback window.

---

## SEO / legacy URL warning

The current production domain already has indexed WordPress content. The domain
itself staying the same does not protect rankings for old paths that disappear.

Known examples that require redirect decisions include:

- `/about-us/`
- `/contact-us/`
- `/prp-prf-exosomes-center/`
- `/urgent-care-near-you/`
- `/vip-urgent-care/`
- `/faq/`
- `/blog/`
- multiple indexed article URLs.

Some obvious structural redirects are already drafted, but the list is not
complete. Do not declare production cutover ready until the full legacy URL
inventory has been captured.

---

## Security / privacy boundaries

- Never expose Keycloak, database, Harbor, SMTP or Jenkins secrets.
- Staging and production databases/secrets remain separate.
- Browser traffic uses public API hostnames, never private cluster IPs.
- Patient Registration currently collects demographic/contact data only; do not
  casually extend it to clinical documents/history.
- Admin tokens stay in memory through `keycloak-js`.
- Production deployment must go through Jenkins; do not manually rsync the final
  site as a normal deployment method.

---

## New-session startup protocol

A new AI/tab should:

1. read this `HANDOFF.md`;
2. read `docs/migration/FINAL_DOMAIN_CUTOVER.md`;
3. inspect current `dev`, `main`, and open PRs;
4. inspect current Jenkins status;
5. inspect live DNS/HAProxy/Hestia/Kubernetes/Keycloak state when relevant;
6. never assume this migration branch has been merged;
7. preserve all fail-closed blockers until their prerequisites are actually met.


## 2026-09-20 — Migration CI retrigger

- Jenkins HTTPS/reachability issue was corrected by the operator.
- PR #40 remains the authoritative final-domain migration PR.
- Re-trigger CI on this branch after the Jenkins recovery; do not merge to `dev` until the final staging DNS/Hestia/HAProxy/TLS/Keycloak prerequisites in this handoff are complete.
