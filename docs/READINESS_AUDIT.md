# Readiness Audit — Dr. Farah VIP Urgent Care

**Date:** 2026-07-26
**Performed by:** Claude Code session, management VM
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
| Repository remote | READY | `git@github.com:ben-edu/project_drfarah.git` confirmed via `git ls-remote`. Remote exists but is empty. | Push initial commits. |
| Default branch | READY | `main` created locally. | Push after first commit. |
| `dev` branch | READY | Created from `main`. | Push. |
| Feature branch | READY | `feature/bootstrap-readiness` created from `dev`. | Current working branch. |
| Uncommitted changes | N/A | Fresh repository — no user changes to preserve. | — |

## Source Documents

| Item | Status | Evidence | Next action |
|---|---|---|---|
| `PROJECT_DRFARAH.md` | READY | Found at `project-sources/PROJECT_DRFARAH.md` (33,171 bytes). Copied to repo root as `PROJECT.md`. | None. |
| `00_START_HERE.md` | READY | Found at `project-sources/00_START_HERE.md`. Infrastructure overview. | Reference only — kept outside repo. |
| `01_INFRA_BASELINE.md` | READY | Found at `project-sources/01_INFRA_BASELINE.md`. Platform facts. | Reference only. |
| `02_DELIVERY_PLAYBOOK.md` | READY | Found at `project-sources/02_DELIVERY_PLAYBOOK.md`. Setup recipe. | Reference only. |
| `03_APP_BLUEPRINT.md` | READY | Found at `project-sources/03_APP_BLUEPRINT.md`. App patterns. | Reference only. |
| `example-toilettage.md` | READY | Found at `project-sources/example-toilettage.md`. Reference project. | Reference only. |

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

| Hostname | Certificate CN | SAN | Expiry | Matches hostname? | Status |
|---|---|---|---|---|---|
| `drfarah.proxbenovh.cloud` | `*.proxbenovh.cloud` | `*.proxbenovh.cloud`, `proxbenovh.cloud` | 2026-09-07 | Yes | READY |
| `www.drfarah.proxbenovh.cloud` | `*.behnam.fr` | `*.behnam.fr`, `behnam.fr` | 2026-09-20 | **No** | BLOCKED |
| `staging.drfarah.proxbenovh.cloud` | `*.behnam.fr` | `*.behnam.fr`, `behnam.fr` | 2026-09-20 | **No** | BLOCKED |
| `api.drfarah.proxbenovh.cloud` | `*.behnam.fr` | `*.behnam.fr`, `behnam.fr` | 2026-08-25 | **No** | BLOCKED |
| `api.staging.drfarah.proxbenovh.cloud` | `*.behnam.fr` | `*.behnam.fr`, `behnam.fr` | 2026-08-25 | **No** | BLOCKED |
| `admin.drfarah.proxbenovh.cloud` | `*.behnam.fr` | `*.behnam.fr`, `behnam.fr` | 2026-09-20 | **No** | BLOCKED |

**Inferred:** The operator configured an ACME certificate for `*.proxbenovh.cloud`
which covers the apex but the HAProxy frontends for the other drfarah domains
are still serving the default `*.behnam.fr` certificate. Each drfarah subdomain
needs its SNI entry associated with the `*.proxbenovh.cloud` certificate in
HAProxy, or a separate certificate covering those names must be provisioned.

**Next action:** Update HAProxy SNI configuration so that all
`*.drfarah.proxbenovh.cloud` names present the valid `*.proxbenovh.cloud`
certificate.

## Frontend / Hestia vhosts (BM1)

| Domain | Vhost exists? | Docroot path | HTTPS response | Status |
|---|---|---|---|---|
| `drfarah.proxbenovh.cloud` | Yes | `/home/benweb/web/drfarah.proxbenovh.cloud/public_html` | 200 (Hestia default page) — cert OK | READY |
| `staging.drfarah.proxbenovh.cloud` | **No** | N/A | 200 (lands on default Hestia vhost) — cert mismatch | MISSING |
| `admin.drfarah.proxbenovh.cloud` | Yes | `/home/benweb/web/admin.drfarah.proxbenovh.cloud/public_html` | 503 — cert mismatch | PARTIAL |

**Confirmed facts:**
- Owner: `benweb` for both existing vhosts.
- `public_html/` is writable by `benweb` (owned by `benweb:www-data`, perms `drwxr-xr-x`).
- `staging.drfarah.proxbenovh.cloud` was not found under `/home/benweb/web/`.

**Inferred:** The `admin` vhost's 503 response may be because no content has been
deployed to it yet, or the HAProxy backend health check is failing. This should
resolve once the first frontend deploy lands.

**Next action:** Create the missing `staging.drfarah.proxbenovh.cloud` web domain
in Hestia (owner `benweb`).

## Jenkins

| Item | Status | Evidence | Next action |
|---|---|---|---|
| Multibranch job | READY | `project_drfarah` job exists at `https://jenkins.proxbenovh.cloud/job/project_drfarah/`. | Will index branches when Jenkinsfile is pushed. |
| `hestia-benweb-ssh` credential | READY (inferred) | Documented in `01_INFRA_BASELINE.md`; used by `project_toilettage`. | Test deploy access after vhosts are confirmed. |
| `harbor-robot-devops-project-harbor` credential | READY (inferred) | Documented; used by `project_toilettage`. | Test Docker login when API image build is added. |
| `drfarah-postgres` credential | NOT REQUIRED YET | Not yet created. | Create before API deployment. |
| `drfarah-smtp` credential | NOT REQUIRED YET | Not yet created. | Create before email testing. |
| Jenkinsfile discoverability | READY | Bootstrap Jenkinsfile added to `feature/bootstrap-readiness`. | Push. |

**Kubeconfig path** (`/var/lib/jenkins/.kube/config-afpa-k3s`) was confirmed from
documentation but is on the Jenkins agent, not this management VM. The local
management VM uses `~/.kube/config` which also connects successfully to
`afpa-k3s`.

## K3s / BM2

| Item | Status | Evidence | Next action |
|---|---|---|---|
| Cluster connectivity | READY | `kubectl cluster-info` succeeds. 3 nodes Ready (`v1.34.5+k3s1`). | None. |
| `drfarah` namespace | MISSING | `kubectl get namespace drfarah` returns NotFound. | Create namespace. |
| Harbor pull secret pattern | READY | `harbor-regcred` (type `kubernetes.io/dockerconfigjson`) exists in `toilettage` namespace. | Copy pattern to `drfarah` namespace when created. |
| Traefik ingress class | READY | `traefik` ingress class available (controller: `traefik.io/ingress-controller`). | Use for drfarah API ingresses. |
| API deployments/services/ingresses | NOT REQUIRED YET | No resources exist in `drfarah` namespace. | Create during implementation. |
| PostgreSQL StatefulSet | NOT REQUIRED YET | Not created. Reference pattern exists in `toilettage` namespace. | Create during implementation. |
| ConfigMaps / Secrets | NOT REQUIRED YET | None exist. | Create during implementation; commit only `*.example`. |

**Confirmed:** Traefik ingress uses entrypoints `web` and `websecure` as observed
from existing ingresses.

## Keycloak

| Item | Status | Evidence | Next action |
|---|---|---|---|
| Endpoint availability | READY | `https://keycloak.soria-academie.fr` returns 302 to `/admin/`. | None. |
| `drfarah` realm | MISSING | `GET /realms/drfarah` returns `{"error":"Realm does not exist"}`. | Create realm, admin client (`drfarah-admin`), PKCE S256, roles. |

## PostgreSQL

| Item | Status | Evidence | Next action |
|---|---|---|---|
| Database `drfarah` | NOT REQUIRED YET | No StatefulSet, Service, or PVC in `drfarah` namespace. | Create during API implementation. |
| Credentials | NOT REQUIRED YET | `drfarah-postgres` credential not yet created. | Create Jenkins credential + K3s Secret. |

**Not verifiable from current environment:** The shared PostgreSQL instance
running in the cluster. Assumed available based on the `toilettage-postgres`
StatefulSet pattern in the `toilettage` namespace.

## Harbor

| Item | Status | Evidence | Next action |
|---|---|---|---|
| Endpoint availability | READY | `https://harbor.proxbenovh.cloud` returns 200. | None. |
| Project path | READY | Expected path: `devops-project-harbor/drfarah-api` (per naming convention). | Create project/image repo when API is ready. |
| Robot account | READY (inferred) | Credential `harbor-robot-devops-project-harbor` documented and used by `project_toilettage`. | Verify pull+push access for `drfarah-api` repo. |

## SMTP

| Item | Status | Evidence | Next action |
|---|---|---|---|
| SORIA SMTP | NOT VERIFIABLE | No credential or configuration inspected. Documented in infrastructure baseline. | Create `drfarah-smtp` credential before email testing. |
| Clinic sender | NOT REQUIRED YET | Production sender address to be confirmed by Dr. Farah. | Define before production deployment. |

## Backups

| Item | Status | Evidence | Next action |
|---|---|---|---|
| PostgreSQL backup | NOT REQUIRED YET | No CronJob, backup target, or retention policy defined for `drfarah`. | Define before production. |
| Restore test | NOT REQUIRED YET | — | Perform before production acceptance. |

## Unresolved Prerequisites

1. **TLS certificate mismatch** (BLOCKED): 5 of 6 domains serve `*.behnam.fr`
   instead of `*.proxbenovh.cloud`. HAProxy SNI configuration needs updating
   before browsers can connect without certificate warnings.
2. **Missing Hestia staging vhost** (MISSING): `staging.drfarah.proxbenovh.cloud`
   needs to be created before the `dev` branch can deploy to staging.
3. **Missing K3s namespace** (MISSING): `drfarah` namespace needs creation
   before any API resources can be deployed.
4. **Missing Keycloak realm** (MISSING): `drfarah` realm needs creation before
   admin authentication can work.

## Classification Summary

| Status | Count | Items |
|---|---|---|
| READY | 15 | Git remote, branches, 6 DNS records, apex TLS, 2 Hestia vhosts, Jenkins, K3s cluster, Traefik, Harbor endpoint, Keycloak endpoint |
| PARTIAL | 1 | Admin vhost (exists, returns 503 — needs content deploy) |
| MISSING | 4 | Staging Hestia vhost, K3s namespace, Keycloak realm, Harbor image repo |
| BLOCKED | 5 | TLS cert mismatch for www/staging/api/api-staging/admin |
| NOT REQUIRED YET | 6 | K3s resources, PostgreSQL DB, SMTP credential, backup, drfarah-postgres credential, drfarah-smtp credential |
| NOT VERIFIABLE | 1 | SMTP (no access path from management VM) |
