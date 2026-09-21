# HANDOFF — 2026-09-21 — Production activation

## Authoritative project state

Repository: `ben-edu/project_drfarah`

Integration branch: `dev`

Final-domain migration merge on `dev`:
`9e5c70e52e0f27435c0c5f32c5b48fa52bbff6c5`

Jenkins `dev` build 5 completed successfully and deployed the final staging
hosts.

Detailed runbook: `docs/migration/FINAL_DOMAIN_CUTOVER.md`

## Environment map

### Production

- public site: `https://drfarahvipurgentcare.com`
- canonical alias: `https://www.drfarahvipurgentcare.com` → apex
- API: `https://api.drfarahvipurgentcare.com`
- admin: `https://admin.drfarahvipurgentcare.com`
- Kubernetes namespace: `drfarah`

### Staging

- public site: `https://staging.drfarahvipurgentcare.com`
- API: `https://api-staging.drfarahvipurgentcare.com`
- admin: `https://admin-staging.drfarahvipurgentcare.com`
- Kubernetes namespace: `drfarah-staging`

Do not use the obsolete nested `.staging.` hostname form; both final staging
service names use a hyphen.

Keycloak remains at
`https://keycloak.soria-academie.fr/realms/drfarah`, client
`drfarah-admin`.

## Verified infrastructure

- authoritative GoDaddy DNS points BM1 web/admin hosts to `87.98.174.211`;
- authoritative GoDaddy DNS points BM2 API hosts to `51.75.57.153`;
- `www` is a CNAME to the apex;
- obsolete dotted staging names do not resolve;
- no unsupported AAAA records are present;
- HAProxy HTTP/HTTPS frontend rules are attached on both bare metals;
- HTTP-01 ACME routing and final-host certificates are valid;
- Hestia production/staging public and admin docroots exist and are writable;
- final staging Keycloak redirect, logout and Web Origin entries are present.

## Accepted staging evidence

External checks returned:

- staging frontend: HTTP 200, valid TLS;
- staging admin: HTTP 200, valid TLS;
- staging API liveness: HTTP 200, valid TLS;
- staging API readiness: HTTP 200, valid TLS.

The staging API HAProxy backend sends the correct `Host` and
`X-Forwarded-Host`: `api-staging.drfarahvipurgentcare.com`.

## Explicit launch decisions

The operator approved the following temporary launch decisions on 2026-09-21:

1. Keep the existing GoDaddy WordPress hosting intact as the recovery source;
   a separate WordPress export is not required before this immediate launch.
2. Use the Soria SMTP relay temporarily in production:
   - host `mail.soria-academie.fr`;
   - port `587` with STARTTLS;
   - sender `contact@soria-academie.fr`;
   - clinic recipient `appointment@soria-academie.fr`.
3. Finish the complete historical WordPress URL/SEO inventory after launch.
   Confirmed high-value redirects ship now and the old hosting must remain
   available during stabilization.
4. Remove runtime insurer-image hotlinks to WordPress. Launch uses the named,
   accessible insurance text cards already present in the HTML; approved local
   artwork can be added later.

GoDaddy/Microsoft 365 SMTP migration is a separate post-launch task. Do not
change MX/SPF/DKIM/DMARC records as part of the website deployment.

## Production delivery now implemented

The Jenkins `main` path is fail-closed and performs, in order:

1. repository, Kubernetes secret and Hestia preflight;
2. immutable API and PostgreSQL-backup image build/push to Harbor;
3. isolated production PostgreSQL/API deployment in namespace `drfarah`;
4. external production API liveness, readiness, environment and CORS checks;
5. immediate PostgreSQL backup to Hestia and restore into disposable
   PostgreSQL 16;
6. crawlable production frontend assembly and publication;
7. production admin SPA publication;
8. final frontend/admin/API HTTPS checks.

The daily database backup CronJob:

- runs at `09:17 UTC`;
- sends a custom-format `pg_dump` over SSH to
  `/home/benweb/backups/drfarah-postgres` on Hestia;
- uses directory mode `0700`, archive mode `0600`, and 30-day retention;
- stores data outside the production PVC and cluster nodes.

Frontend/admin publication does not happen unless the immediate off-cluster
archive passes the disposable restore test.

## Production secret bootstrap

On the first `main` deployment, Jenkins automatically runs the safe bootstrap
when both production DB/API secrets are absent:

```bash
sh scripts/bootstrap-production-secrets.sh
```

The same script can be run manually from a trusted Kubernetes management shell
if an operator intentionally prepares the namespace before promotion. It:

- prints no secret values;
- generates a new independent production database password;
- refuses to overwrite existing production DB/API secrets;
- creates `harbor-regcred`, `drfarah-db-secret`, and
  `drfarah-api-secret` in namespace `drfarah`.

Do not paste credential values into chat, Git, or Jenkins logs.

If exactly one of the DB/API secrets exists, Jenkins fails closed instead of
guessing or overwriting a partial production state.

## Promotion order

1. Validate the production-activation branch in Jenkins.
2. Merge its PR into `dev` and require a green final staging deployment.
3. Open/merge the exact approved `dev` state into `main`.
4. Require the complete green `main` production pipeline; on a fresh namespace
   it performs the one-time secret bootstrap automatically.
5. Verify public booking/services, admin Keycloak login, redirects, robots and
   sitemap from an external host.

Do not manually rsync production content around Jenkins; Jenkins is the
authoritative deployment path.

## Post-launch follow-up

- test a controlled real booking and confirm both patient and clinic email;
- complete the old WordPress URL/blog inventory and add missing targeted 301s;
- retain GoDaddy hosting and temporary `proxbenovh.cloud` routes during the
  stabilization window;
- replace the shared Hestia deployment key used by the backup CronJob with a
  dedicated restricted backup-only key;
- evaluate GoDaddy/Microsoft 365 SMTP AUTH and sender policy before replacing
  Soria SMTP;
- submit the final sitemap and review 404/5xx/auth/CORS logs;
- remove temporary Keycloak/CORS/HAProxy compatibility entries only after
  stable verification;
- improve the remaining reconstructed/placeholder imagery in a separate visual
  release.
