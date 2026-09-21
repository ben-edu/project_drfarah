# Readiness Audit — Dr. Farah VIP Urgent Care

> **Historical infrastructure audit.** The hostname/TLS/Keycloak observations
> below were captured during the temporary `proxbenovh.cloud` bootstrap and
> must not be treated as current cutover state. For the September 2026 final
> domain migration, read `HANDOFF.md` and
> `docs/migration/FINAL_DOMAIN_CUTOVER.md`, then verify live infrastructure.


**Date:** 2026-07-26 (updated after Step 02 — Infrastructure Foundation)
**Performed by:** Claude Code sessions, management VM
**Scope:** Read-only inspection of all documented prerequisites

## Status legend

| Status | Meaning |
|---|---|
| READY | Verified and working — no action needed. |
| PARTIAL | Partially working — needs attention before deployment. |
| MISSING | Does not exist — must be created. |
| BLOCKED | Cannot proceed without external action. |
| NOT REQUIRED YET | Expected to be absent at this stage. |

---

## Git / Repository

| Item | Status | Evidence | Next action |
|---|---|---|---|
| Repository remote | READY | `git@github.com:ben-edu/project_drfarah.git`. Commits pushed to `main`, `dev`, `feature/bootstrap-readiness`, `feature/infrastructure-foundation`. | None. |
| Default branch | READY | `main` exists locally and remotely. | None. |
| `dev` branch | READY | `dev` exists locally and remotely. PR #1 merged (bootstrap). | None. |
| Feature branch | READY | `feature/infrastructure-foundation` created from `dev`. | Current working branch. |
| PR workflow | READY | PR #1 merged successfully. | Open new PR for infrastructure-foundation. |

## Source Documents

| Item | Status | Evidence | Next action |
|---|---|---|---|
| `PROJECT_DRFARAH.md` | READY | Copied to repo root as `PROJECT.md`. | None. |
| Supporting docs (`00`–`03`, `example-toilettage`) | READY | All present in `project-sources/`. | Reference only — kept outside repo. |

## DNS

| Hostname | Expected IP | Resolved IP | Status |
|---|---|---|---|
| `drfarah.proxbenovh.cloud` | 87.98.174.211 (BM1) | 87.98.174.211 | READY |
| `www.drfarah.proxbenovh.cloud` | 87.98.174.211 (BM1) | 87.98.174.211 | READY |
| `staging.drfarah.proxbenovh.cloud` | 87.98.174.211 (BM1) | 87.98.174.211 | READY |
| `api.drfarah.proxbenovh.cloud` | 51.75.57.153 (BM2) | 51.75.57.153 | READY |
| `api.staging.drfarah.proxbenovh.cloud` | 51.75.57.153 (BM2) | 51.75.57.153 | READY |
| `admin.drfarah.proxbenovh.cloud` | 87.98.174.211 (BM1) | 87.98.174.211 | READY |

All DNS records resolve to the correct HAProxy entry points.

## TLS

**Operator re-issued all certificates after Step 01.** Rechecked 2026-07-26.

| Hostname | Certificate CN | SAN | Expiry | Verify | Status |
|---|---|---|---|---|---|
| `drfarah.proxbenovh.cloud` | `www.drfarah.proxbenovh.cloud` | `drfarah.proxbenovh.cloud`, `www.drfarah.proxbenovh.cloud` | 2026-10-24 | 0 (ok) | READY |
| `www.drfarah.proxbenovh.cloud` | `www.drfarah.proxbenovh.cloud` | `drfarah.proxbenovh.cloud`, `www.drfarah.proxbenovh.cloud` | 2026-10-24 | 0 (ok) | READY |
| `staging.drfarah.proxbenovh.cloud` | `*.staging.drfarah.proxbenovh.cloud` | `*.staging.drfarah.proxbenovh.cloud`, `staging.drfarah.proxbenovh.cloud` | 2026-10-24 | 0 (ok) | READY |
| `api.drfarah.proxbenovh.cloud` | `api.drfarah.proxbenovh.cloud` | `api.drfarah.proxbenovh.cloud`, `drfarah.proxbenovh.cloud` | 2026-10-24 | 0 (ok) | READY |
| `api.staging.drfarah.proxbenovh.cloud` | `api.staging.drfarah.proxbenovh.cloud` | `api.staging.drfarah.proxbenovh.cloud`, `staging.drfarah.proxbenovh.cloud` | 2026-10-24 | 0 (ok) | READY |
| `admin.drfarah.proxbenovh.cloud` | `*.drfarah.proxbenovh.cloud` | `*.drfarah.proxbenovh.cloud`, `proxbenovh.cloud` | 2026-10-24 | 0 (ok) | READY |

**All certificates:** Let's Encrypt, ssl_verify=0 for all hosts, valid until Oct 24 2026.

**Note — www redirect:** `www.drfarah.proxbenovh.cloud` resolves and serves
HTTPS correctly but does **not** redirect to the apex. The project brief calls for
a redirect. This needs to be configured in HAProxy or Hestia (PARTIAL).

## HTTPS Responses

| Hostname | HTTP | Notes |
|---|---|---|
| `drfarah.proxbenovh.cloud` | 200 | Hestia default page (expected — no app deployed yet). |
| `www.drfarah.proxbenovh.cloud` | 200 | Serves same as apex (should redirect). |
| `staging.drfarah.proxbenovh.cloud` | 200 | Hestia default page (expected). |
| `api.drfarah.proxbenovh.cloud` | 404 | Traefik responding, no backend (expected). |
| `api.staging.drfarah.proxbenovh.cloud` | 404 | Traefik responding, no backend (expected). |
| `admin.drfarah.proxbenovh.cloud` | 200 | Hestia default page (was 503 in Step 01, now resolved). |

## Frontend / Hestia vhosts (BM1)

| Domain | Vhost exists? | Docroot path | HTTPS response | Status |
|---|---|---|---|---|
| `drfarah.proxbenovh.cloud` | Yes | `/home/benweb/web/drfarah.proxbenovh.cloud/public_html` | 200 | READY |
| `staging.drfarah.proxbenovh.cloud` | **Yes** (created 2026-07-26) | `/home/benweb/web/staging.drfarah.proxbenovh.cloud/public_html` | 200 | READY |
| `admin.drfarah.proxbenovh.cloud` | Yes | `/home/benweb/web/admin.drfarah.proxbenovh.cloud/public_html` | 200 | READY |

**Confirmed facts:**
- All three vhosts exist, owned by `benweb`.
- All `public_html/` directories are writable by `benweb` (`benweb:www-data`, `drwxr-xr-x`).
- Staging vhost created via `v-add-web-domain benweb staging.drfarah.proxbenovh.cloud`.
- Admin 503 resolved (was a routing/vhost issue in Step 01, now serves 200).

**Next action:** None for Hestia. All vhosts ready for Jenkins deployment.

## Jenkins

| Item | Status | Evidence | Next action |
|---|---|---|---|
| Multibranch job | READY | `project_drfarah` job exists. | Index branches after push. |
| `hestia-benweb-ssh` credential | READY (inferred) | Documented; used by `project_toilettage`. | Test deploy access when first frontend build runs. |
| `harbor-robot-devops-project-harbor` credential | READY (inferred) | Documented; used by `project_toilettage`. | Test when API image build is added. |
| `drfarah-postgres` credential | NOT REQUIRED YET | Not yet created. | Create before API deployment. |
| `drfarah-smtp` credential | NOT REQUIRED YET | Not yet created. | Create before email testing. |
| Jenkinsfile discoverability | READY | Bootstrap Jenkinsfile present on feature branches. | Jenkins will detect on next scan. |

## K3s / BM2

| Item | Status | Evidence | Next action |
|---|---|---|---|
| Cluster connectivity | READY | `kubectl cluster-info` succeeds. 3 nodes Ready (`v1.34.5+k3s1`). | None. |
| `drfarah` namespace | **READY** (created 2026-07-26) | `kubectl get namespace drfarah` returns Active. Labels: `app.kubernetes.io/name=drfarah`, `app.kubernetes.io/part-of=drfarah-vip-urgent-care`, `app.kubernetes.io/managed-by=jenkins`. | None. |
| Harbor pull secret | **READY** (copied 2026-07-26) | `harbor-regcred` (type `kubernetes.io/dockerconfigjson`) exists in `drfarah` namespace. Copied from `toilettage` namespace. | None. |
| Traefik ingress class | READY | `traefik` ingress class available. | Use for drfarah API ingresses. |
| API deployments/services/ingresses | NOT REQUIRED YET | No resources created yet. | Create during implementation. |
| PostgreSQL StatefulSet | NOT REQUIRED YET | Not created. Reference pattern exists in `toilettage` namespace. | Create during implementation. |
| ConfigMaps / Secrets | NOT REQUIRED YET | Only `harbor-regcred` exists. | Create application secrets during implementation. |

## Keycloak

| Item | Status | Evidence | Next action |
|---|---|---|---|
| Endpoint availability | READY | `https://keycloak.soria-academie.fr` returns 302 to `/admin/`. | None. |
| `drfarah` realm | **BLOCKED** | `GET /realms/drfarah` returns `{"error":"Realm does not exist"}`. Admin credentials changed after bootstrap — cannot create programmatically. | Requires Keycloak admin access. Create realm `drfarah`, client `drfarah-admin` (public, PKCE S256), roles `clinic-admin` and `clinic-staff`. |
| Admin credentials | PARTIAL | `keycloak-admin-secret` exists in K3s but password was rotated after Helm chart deployment. | Operator or admin must provide current credentials or create the realm manually. |

## PostgreSQL

| Item | Status | Evidence | Next action |
|---|---|---|---|
| Pattern confirmation | READY | `toilettage-postgres` StatefulSet exists in `toilettage` namespace (1/1 ready). Pattern: StatefulSet + Service + PVC `local-path`. | Follow same pattern for drfarah. |
| Database `drfarah` | NOT REQUIRED YET | Not yet created. | Create during API implementation (StatefulSet + PVC in `drfarah` namespace). |
| Credentials | NOT REQUIRED YET | `drfarah-postgres` credential not yet created. | Create Jenkins credential + K8s Secret before API deployment. |
| Future reference names | Defined | DB name: `drfarah`, User: `drfarah`, K8s Secret: `drfarah-postgres-secret`, Jenkins credential: `drfarah-postgres`. | Apply these names in manifests. |

## Harbor

| Item | Status | Evidence | Next action |
|---|---|---|---|
| Endpoint availability | READY | `https://harbor.proxbenovh.cloud` returns 200. | None. |
| Project `devops-project-harbor` | READY (inferred) | Used by `project_toilettage`. API requires auth. | None. |
| Image repo `drfarah-api` | **NOT REQUIRED YET** | Not created. Harbor will auto-create on first `docker push` if the robot account has push permission. | Verify robot account push access. Do not manually create. |
| Robot account | READY (inferred) | Credential `harbor-robot-devops-project-harbor` documented and used by `project_toilettage`. | Test `docker push` with the credential when API image is built. |

**Classification:** Harbor image repository is NOT REQUIRED YET. The first
`docker push` from Jenkins (using the Harbor robot account) will auto-create the
`drfarah-api` repository within `devops-project-harbor` if it does not exist.
If Harbor policy requires pre-creation, do it at that time.

## SMTP

| Item | Status | Evidence | Next action |
|---|---|---|---|
| SORIA SMTP pattern | NOT VERIFIABLE | Credential not inspected. Reference project (`toilettage`) uses SORIA SMTP for testing. | Create `drfarah-smtp` Jenkins credential before email testing. Copy pattern from `toilettage` without exposing values. |
| Clinic sender | NOT REQUIRED YET | Production sender address to be confirmed by Dr. Farah. | Define before production deployment. |

## Backups

| Item | Status | Evidence | Next action |
|---|---|---|---|
| PostgreSQL backup target | **NOT DEFINED** | No backup destination, CronJob, or retention policy defined for any project. `toilettage` also lists this as pending. | Define backup target (e.g. S3-compatible, NFS, or external host) before production. |
| Restore test | NOT REQUIRED YET | — | Perform before production acceptance. |
| Blocker classification | **BLOCKER before production** | No automated backup means data loss risk for booking data. | Define and implement before production deployment. |

## Unresolved Prerequisites

1. **Keycloak realm** (BLOCKED): `drfarah` realm not created. Requires current
   Keycloak admin credentials — the bootstrap password was rotated. Realm, client,
   roles must be created before admin authentication works.
2. **www → apex redirect** (PARTIAL): `www.drfarah.proxbenovh.cloud` serves HTTPS
   correctly but does not redirect to `drfarah.proxbenovh.cloud`. Configure in
   HAProxy or Hestia.
3. **Backup destination** (NOT DEFINED): No backup target configured for any
   project. Must be resolved before production to protect booking data.

### Resolved from Step 01

1. ~~TLS certificate mismatch~~ — all 6 hosts now have valid, matching Let's Encrypt certificates.
2. ~~Missing Hestia staging vhost~~ — created via `v-add-web-domain`.
3. ~~Missing K3s namespace~~ — created with labels.
4. ~~Missing Harbor pull secret~~ — copied from `toilettage` namespace.
5. ~~Admin 503~~ — now returns 200 (routing fixed or Hestia rebuilt).

## Classification Summary

| Status | Count | Items |
|---|---|---|
| READY | 20 | Git remote, branches, PR workflow, 6 DNS records, 6 TLS certs (ssl_verify=0), 3 Hestia vhosts, K3s namespace + pull secret, Traefik, Jenkins, Harbor endpoint, Keycloak endpoint |
| PARTIAL | 2 | www → apex redirect (not configured), Keycloak admin credential rotated |
| BLOCKED | 1 | Keycloak realm creation (requires admin credentials) |
| NOT REQUIRED YET | 7 | K3s app resources, PostgreSQL DB/credential, Harbor image repo, SMTP credential, backup config, app ConfigMaps/Secrets |
| BLOCKER before production | 1 | Backup destination and automated backup |
