# Final Domain Migration — drfarahvipurgentcare.com

**Prepared:** 2026-09-20  
**Status:** PRE-CUTOVER / DO NOT MERGE OR PROMOTE UNTIL OPERATOR PREFLIGHT IS COMPLETE

## Target environment map

| Purpose | Final host | Runtime |
|---|---|---|
| Production frontend | `drfarahvipurgentcare.com` | Hestia / BM1 |
| Production www alias | `www.drfarahvipurgentcare.com` → apex | HAProxy/Hestia redirect |
| Staging frontend | `staging.drfarahvipurgentcare.com` | Hestia / BM1 |
| Production API | `api.drfarahvipurgentcare.com` | HAProxy BM2 → Traefik → `drfarah` |
| Staging API | `api-staging.drfarahvipurgentcare.com` | HAProxy BM2 → Traefik → `drfarah-staging` |
| Production admin | `admin.drfarahvipurgentcare.com` | Hestia / BM1 |
| Staging admin | `admin-staging.drfarahvipurgentcare.com` | Hestia / BM1 |

The Keycloak issuer remains `https://keycloak.soria-academie.fr/realms/drfarah`.
The realm does not move with the website domain.

## Why staging admin is separate

The current temporary `admin.drfarah.proxbenovh.cloud` is deployed by the
`dev` pipeline and therefore behaves as a staging admin. Reusing one final
admin hostname for both `dev` and `main` would allow a staging deploy to
overwrite the production admin SPA. The final architecture therefore uses
`admin-staging.drfarahvipurgentcare.com` for `dev` and
`admin.drfarahvipurgentcare.com` for production.

## Operator-owned preflight

Complete these before the migration branch is merged to `dev`:

### DNS / GoDaddy

Do not change nameservers. Preserve all MX, SPF, DKIM, DMARC and other mail TXT
records.

Prepare or verify these records:

- apex `@` → **A 87.98.174.211** (BM1 web HAProxy)
- `www` → **CNAME @** (or equivalent apex alias/redirect strategy)
- `staging` → **A 87.98.174.211**
- `admin` → **A 87.98.174.211**
- `admin.staging` → **A 87.98.174.211**
- `api` → **A 51.75.57.153** (BM2 API HAProxy)
- `api.staging` → **A 51.75.57.153**

These are the currently documented platform edge IPs; verify the live HAProxy
addresses immediately before editing DNS.

Check for conflicting stale A/AAAA/CNAME records. In particular, remove or
replace an old AAAA record if IPv6 is not routed to the new platform.

Before the final apex cutover, reduce the relevant DNS TTL (for example to
300 seconds) and record the old production web target for rollback.

### Hestia / BM1

The following independent web domains/docroots must exist and be writable by
`benweb`:

- `/home/benweb/web/drfarahvipurgentcare.com/public_html`
- `/home/benweb/web/staging.drfarahvipurgentcare.com/public_html`
- `/home/benweb/web/admin.drfarahvipurgentcare.com/public_html`
- `/home/benweb/web/admin-staging.drfarahvipurgentcare.com/public_html`

Configure `www.drfarahvipurgentcare.com` as the production alias/redirect.
TLS terminates on HAProxy; Hestia-local ACME is not the authoritative TLS path.

### HAProxy and TLS

Clone the existing proven Dr. Farah temporary-domain routing rules.

BM1 routes:
- production frontend + www
- staging frontend
- production admin
- staging admin

BM2 routes:
- production API
- staging API

Install/verify certificates for every final hostname before browser testing.
DNS-01 certificate issuance can be done before the public A-record cutover.

Certificate coverage detail: a certificate containing
`*.drfarahvipurgentcare.com` covers every one-label subdomain used here,
including `www`, `staging`, `api`, `api-staging`, `admin`, and
`admin-staging`. It does **not** cover the apex
`drfarahvipurgentcare.com`; include the apex as an explicit SAN or use a
separate certificate for it.

### Keycloak

Realm remains `drfarah`, client remains `drfarah-admin` for this migration.

During transition, configure the public client with explicit entries for:

Valid redirect URIs:
- `https://admin.drfarahvipurgentcare.com/*`
- `https://admin-staging.drfarahvipurgentcare.com/*`
- keep `https://admin.drfarah.proxbenovh.cloud/*` temporarily until migration is verified

Valid post-logout redirect URIs:
- same three URI patterns during transition

Web origins:
- `https://admin.drfarahvipurgentcare.com`
- `https://admin-staging.drfarahvipurgentcare.com`
- keep `https://admin.drfarah.proxbenovh.cloud` temporarily during transition

Use explicit origins, not a broad wildcard.

Before production, require MFA/OTP for real clinic staff accounts as specified
by the project security requirements.

### Production Kubernetes prerequisites

Verify live `drfarah` namespace and create/verify:
- `harbor-regcred`
- `drfarah-db-secret`
- `drfarah-api-secret`

Production database credentials must be independent from staging. Do not copy
the staging database into production unless an explicit data-migration decision
is made. The normal production start is a fresh PostgreSQL database with
Alembic bootstrap to head.

No secret values belong in Git, this document, or chat.

### Production email

Confirm the real production notification setup before enabling production
booking:
- SMTP host/port
- sender identity
- staff notification recipient
- SMTP credentials in `drfarah-api-secret`

Do not silently use a test/SORIA address as the final clinic identity unless
the operator and clinic explicitly approve it.

### Production PostgreSQL backup / restore

Production data protection is a launch requirement, not a post-cutover task.

Before promotion to `main`:
- choose a backup destination outside the production PVC/node;
- define an automated schedule and retention period;
- encrypt/protect backup credentials outside Git;
- document restore commands;
- perform and record at least one restore test to a disposable database.

`kubernetes/drfarah/README.md` contains `BACKUP_READINESS_BLOCKER` until this
is complete.

## Repository-owned migration work

The migration branch must prepare:

1. final canonical URLs and sitemap on `drfarahvipurgentcare.com`;
2. staging and production API hostname selection in public JS;
3. staging and production admin/API hostname selection in `admin/config.js`;
4. staging CORS and Ingress for the final staging origins/host;
5. production Kubernetes manifests in `kubernetes/drfarah/`;
6. `dev` deployment to the final staging frontend/admin/API hosts;
7. production deployment assets/manifests are prepared now; activation of `main` deployment stages happens in a focused follow-up only after final staging is accepted and all production blockers are cleared;
8. production-only indexing behavior:
   - staging keeps `noindex,nofollow,noarchive` and `Disallow: /`;
   - production removes staging noindex and publishes a crawlable robots file;
9. production smoke checks that are read-only wherever possible;
10. updated project handoff and environment documentation.

## Legacy insurer artwork dependency

The current frontend still references six insurance images from the legacy
WordPress host:

- `/wp-content/uploads/2025/02/6.png`
- `/wp-content/uploads/2025/02/14.png`
- `/wp-content/uploads/2025/02/3.png`
- `/wp-content/uploads/2025/02/21.png`
- `/wp-content/uploads/2025/02/aetna.jpg`
- `/wp-content/uploads/2025/02/22.png`

This is safe only while the legacy WordPress origin still serves those files.
After the apex domain points at the new Hestia site, those hotlinks are not a
stable dependency. Copy the approved originals into `frontend/assets/`, keep
their insurer identity/alt text accurate, and replace both `app.js` and
`app-v5.js` references before production promotion. Jenkins deliberately
blocks `main` while these legacy hotlinks remain.

## Legacy WordPress / SEO cutover

The existing `drfarahvipurgentcare.com` is currently a WordPress site and has
indexed pages and blog content. The domain staying the same preserves domain
authority, but paths that disappear can still lose search equity.

Before DNS cutover:

1. take a full backup/export of the old WordPress site and database;
2. export or crawl the complete old URL list / XML sitemap;
3. build a source-controlled 301 redirect map from valuable old paths to the
   closest new page;
4. never redirect every removed URL blindly to the homepage;
5. retain a list of intentionally retired URLs that should return 410/404;
6. verify high-value examples such as old urgent-care, PRP, services, about,
   contact and indexed blog paths.

Known publicly indexed examples include:
- `/urgent-care-near-you/`
- `/vip-urgent-care/`
- `/services/`
- `/blog/`
- multiple PRP / urgent-care blog article slugs

The complete redirect map remains a cutover blocker until the old sitemap/URL
inventory is captured.

## Pre-DNS validation with --resolve

After Hestia/HAProxy/TLS and production Kubernetes are prepared, validate the
new platform before changing public DNS:

```bash
curl --resolve drfarahvipurgentcare.com:443:87.98.174.211 \
  -I https://drfarahvipurgentcare.com/

curl --resolve api.drfarahvipurgentcare.com:443:51.75.57.153 \
  -I https://api.drfarahvipurgentcare.com/api/v1/health/live
```

Use the actual live HAProxy IPs if infrastructure has changed.

Also test:
- production booking service list and availability;
- one explicitly controlled production booking only if approved, otherwise use
  read-only health/services checks;
- production admin Keycloak login;
- staging admin remains isolated from production API;
- patient-registration save/resume/submit on staging before production;
- all final TLS certificates and redirect behavior.

## Cutover order

1. Back up legacy WordPress and record rollback DNS.
2. Complete new DNS records for non-apex hosts first (staging/admin/API).
3. Validate final staging end to end.
4. Create/verify production K8s secrets and production database.
5. After final staging acceptance and production blocker clearance, activate the production Jenkins stages in a focused follow-up PR.
6. Promote the exact approved production-ready SHA to `main` and require a successful production deployment.
7. Validate production with `--resolve` before apex DNS switch.
8. Switch apex/www DNS to BM1.
9. Verify HTTPS, canonical, robots, sitemap, booking, API, admin and Keycloak.
10. Submit the new sitemap in Google Search Console.
11. Monitor 404/5xx/auth/CORS/booking errors.
12. Keep the old hosting target and temporary domains available for rollback
    during the stabilization window.

## Rollback

A domain migration is not complete without rollback evidence.

Record before cutover:
- old apex/www DNS target;
- WordPress backup location;
- last green `dev` SHA;
- production `main` SHA;
- database backup/snapshot strategy.

If the new production frontend is unhealthy immediately after DNS cutover,
restore the old apex/www target while the issue is corrected. Do not destroy
the old WordPress hosting on cutover day.

## Post-cutover cleanup

Only after stable verification:
- remove temporary Keycloak redirect URI/web-origin entries;
- remove temporary staging CORS origins;
- retire temporary `proxbenovh.cloud` Dr. Farah routes when no longer needed;
- restore normal DNS TTL;
- update all long-lived project/infrastructure documentation;
- keep staging noindexed;
- keep production indexable;
- review redirect/404 logs and fix missed legacy URLs.
