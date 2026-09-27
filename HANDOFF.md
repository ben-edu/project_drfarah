# HANDOFF — 2026-09-27 — Production live; public-copy cleanup accepted on staging

## Authoritative project state

Repository: `ben-edu/project_drfarah`. Integration/default branch: `dev`.

Snapshot verified through GitHub on 2026-09-27, before this documentation PR:

| Environment | Branch / commit | Accepted build evidence |
|---|---|---|
| Production | `main` / `cf4d470a90403641b2dd81be69b903da83649a69` | [Jenkins main/6](https://jenkins.proxbenovh.cloud/job/project_drfarah/job/main/6/display/redirect), success recorded 2026-09-26 22:05 UTC |
| Staging | `dev` / `410ad992851feb952f8ce5839ff7a5ade406179d` | [Jenkins dev/3](https://jenkins.proxbenovh.cloud/job/project_drfarah/job/dev/3/display/redirect), success recorded 2026-09-27 13:34 UTC |

[PR #53](https://github.com/ben-edu/project_drfarah/pull/53) is merged to `dev`
and accepted on staging. Its homepage/Contact cleanup is **not yet in main**.
Do not describe this cleanup as published on the public production site.

The earlier bulk branch cleanup is complete: only `dev` and `main` remained
and there were no open PRs at this snapshot. GitHub automatic deletion of
merged branches is enabled. New work still uses a separate branch and PR.

Match Jenkins evidence to the target branch and SHA. The same commit can have
both `dev` and `main` builds; its latest combined GitHub status alone does not
identify a production deployment.

Current code, branch state and dated deployment evidence override old
cutover-preparation notes in Project Sources and historical documentation.
Do not restart the completed DNS, initial production, email-transport or
backup implementation work because an older checklist is still unchecked.

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

## Previously verified infrastructure — 2026-09-21

These are the recorded migration checks, not a fresh infrastructure audit:

- authoritative GoDaddy DNS points BM1 web/admin hosts to `87.98.174.211`;
- authoritative GoDaddy DNS points BM2 API hosts to `51.75.57.153`;
- `www` is a CNAME to the apex;
- obsolete dotted staging names do not resolve;
- no unsupported AAAA records are present;
- HAProxy HTTP/HTTPS frontend rules are attached on both bare metals;
- HTTP-01 ACME routing and final-host certificates are valid;
- Hestia production/staging public and admin docroots exist and are writable;
- final staging Keycloak redirect, logout and Web Origin entries are present.

## Accepted staging evidence — PR #53

On 2026-09-27 the operator reported successful branch CI and `dev` deployment,
then explicitly confirmed `Home: OK`, `Contact: OK`, and `Book: OK` after the
following requested manual checks:

- Home: the internal review-recheck instruction is replaced by
  `Google review excerpts. Individual experiences may vary.`
- Contact: the pending-contact-confirmation note and non-functional message
  form are removed; phone and online-booking actions are displayed.
- Book: the booking page and services open from the Contact action.

The confirmation is operator-provided UI evidence. The assistant's direct
staging requests timed out, so no independent HTTP/TLS, mobile, accessibility
or full booking-submission test is claimed for this check.

PR #53 also removes the unused Contact handler from `app.js` and `app-v5.js`
and aligns frontend/business documentation. It does not add a ContactRequest
backend or verify the quoted reviews, contact facts or legal text.

Earlier final-domain staging acceptance recorded HTTP 200 and valid TLS for
frontend, admin, API liveness and API readiness, with the API forwarding
`Host` and `X-Forwarded-Host` as `api-staging.drfarahvipurgentcare.com`.

## Explicit launch decisions

The initial launch decisions were approved on 2026-09-21. Email configuration
has since advanced as described below:

1. Keep the existing GoDaddy WordPress hosting intact as the recovery source;
   a separate WordPress export is not required before this immediate launch.
2. The temporary Soria outbound relay was superseded by Brevo. Current
   production configuration selects the **Brevo HTTPS API**:
   - `EMAIL_TRANSPORT=brevo_api`;
   - endpoint `https://api.brevo.com/v3/smtp/email`;
   - sender `notifications@drfarahvipurgentcare.com`;
   - two clinic recipients are configured in
     `kubernetes/drfarah/configmap.yaml` as a comma-separated `SMTP_TO` value;
   - one separate message per clinic recipient;
   - API key and retained SMTP rollback credentials stay in
     `drfarah-api-secret`; do not print their values.
   The retained `SMTP_*` names do not mean SMTP is the active transport.
3. Finish the complete historical WordPress URL/SEO inventory after launch.
   Confirmed high-value redirects ship now and the old hosting must remain
   available during stabilization.
4. Remove runtime insurer-image hotlinks to WordPress. Launch uses the named,
   accessible insurance text cards already present in the HTML; approved local
   artwork can be added later.

The Microsoft 365 mailbox remains the inbound service for the clinic domain.
Brevo is only the website's outbound transactional service; this change does not
require replacing the Microsoft MX records.

## Production delivery and recovery

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

The successful `main/6` build above is the accepted pipeline evidence for
these gates. It is not a fresh check of the most recent daily CronJob archive.
The current pipeline includes the disposable-restore startup-race fix and
bounded retries for transient production API readiness failures (PR #52).

## Production secret bootstrap

On the first `main` deployment, Jenkins automatically runs the safe bootstrap
when both production DB/API secrets are absent:

```bash
sh scripts/bootstrap-production-secrets.sh
```

The script:

- prints no secret values;
- generates a new independent production database password;
- refuses to overwrite existing production DB/API secrets;
- creates `harbor-regcred`, `drfarah-db-secret`, and
  `drfarah-api-secret` in namespace `drfarah`.

Do not paste credential values into chat, Git, or Jenkins logs.

If exactly one of the DB/API secrets exists, Jenkins fails closed instead of
guessing or overwriting a partial production state.

Production is already initialized. Do not rerun bootstrap as a routine
follow-up to this documentation or frontend cleanup.

## Immediate delivery order

1. Finish this documentation PR: require successful branch/PR CI, merge to
   `dev`, then require its Jenkins staging build to succeed.
2. Prepare a release PR for the exact tested `dev` state into `main` to publish
   PR #53's cleanup. Production promotion still requires explicit operator
   approval; this handoff does not grant it.
3. After approval and the successful `main` pipeline, verify Home, Contact and
   Book on the production domain and record the release SHA/build result.
4. Proceed through the remaining work below without repeating accepted work.

Jenkins discovers branches/PRs automatically; no routine manual Scan is
required. Feature/chore branches validate, `dev` deploys staging, and approved
`main` changes deploy production. Source HTML remains noindexed for staging;
`scripts/prepare-production-frontend.sh` assembles the crawlable production
artifact without changing those source controls.

Do not manually rsync production content around Jenkins; Jenkins is the
authoritative deployment path.

## Ordered remaining work

This list starts after the immediate documentation/release steps above.
Operator-supplied content and existing operational evidence can be collected
while CI runs, without opening another implementation change.

| Order | Work and completion criterion | Owner / required input |
|---|---|---|
| 1 | Consolidate clinic-approved facts and copy: contact details/hours, credentials, prices, insurance, service claims, review sources/display permission, Privacy, Terms, Notice of Privacy Practices and accessibility wording. Replace pending/draft copy with approved content; removing a warning does not verify a claim. | Clinic/operator supplies one approved pack; developer implements it. |
| 2 | Decide whether a real ContactRequest backend is needed. Until then, retain working Call/Book paths. If approved, scope recipient ownership, validation, rate limiting, privacy/retention and delivery confirmation before implementation. | Operator decision; developer prepares a separate change. |
| 3 | Complete technical SEO migration: old WordPress URL/article inventory, targeted 301 map, deliberate 404/410 decisions, production canonical/robots/sitemap checks, then Search Console sitemap/indexing review. Preserve staging noindex. | Operator supplies legacy export/sitemap and Search Console results; developer implements and checks routing. |
| 4 | Record existing production booking/email evidence: patient confirmation plus both clinic recipients, authenticated admin behavior and staff MFA/OTP enforcement. Reuse accepted evidence; perform one controlled test only if evidence is missing. | Operator confirms receipts and staff login behavior; developer investigates only concrete failures. |
| 5 | Finish visual/media and accessibility/performance cleanup: replace temporary Base64/runtime image reconstruction with approved static assets, retire the `app-v5` workaround and correct the soft Services/IV hero. Preserve approved visual choices; verify mobile and critical images. | Developer; operator supplies original approved files if needed. |
| 6 | Improve local/AI-search content using approved clinic facts: structured data, useful question/answer copy and internal links, after technical SEO is verified. | Developer implements approved content. |
| 7 | Replace the shared backup deployment key with a dedicated restricted backup-only key. Retest the backup path and restore gate. Remove temporary Keycloak/CORS/HAProxy origins/routes only after stable final-domain verification and an agreed recovery decision. | Operator/infrastructure owner, with a scoped implementation plan. |
| 8 | Create and integrate website-first marketing videos after page copy, claims and visual assets are stable. External-channel publishing remains a separate decision. | Operator approves content; developer integrates it. |

MFA enforcement and backup failures take priority if a concrete gap is found;
they should not wait for content or video work. Keep GoDaddy recovery hosting
and temporary routes until the stabilization/recovery decision is made.

Generic non-clinical mobile notifications remain optional after provider
setup. AI Digital Concierge remains postponed. New bookable service records
still need clinic-approved durations, buffers, modes and availability.

## Continuation and low-overhead reporting

- Work on one bounded change at a time. Check current `dev`, open PRs and the
  relevant files; do not reload or retest the whole project without a reason.
- After triggering Jenkins, stop polling and ask the operator for the final
  result. Report branch/PR/build identity plus `Finished: SUCCESS`, or the
  first actual error; full logs are unnecessary unless diagnosis requires them.
- UI reports can be `URL | OK/FAIL | first problem`, with a screenshot only
  for a failure. PR #53's staging checks above are already accepted.
- Collect facts/legal text/review sources in one pack and legacy URLs in one
  file. Never include passwords, API keys, private resume tokens or MFA codes.
- Older `PROJECT.md`, alignment and migration notes include historical
  cutover/SMTP/insurance-hotlink wording. Use this handoff and current runtime
  configuration for present status; reconcile those passages when their
  specific workstream is next edited.
