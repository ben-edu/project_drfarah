# Infrastructure Foundation — Dr. Farah VIP Urgent Care

> **Historical provisioning record.** This file records the original
> `proxbenovh.cloud` foundation and is useful for provenance, but it is not the
> current final-domain runbook. Use `HANDOFF.md` and
> `docs/migration/FINAL_DOMAIN_CUTOVER.md` for
> `drfarahvipurgentcare.com`, and verify live infrastructure before changes.


**Date:** 2026-07-26
**Step:** 02 — Infrastructure Foundation
**Branch:** `feature/infrastructure-foundation`

## Domain Mapping and TLS

All six temporary domains are operational with valid Let's Encrypt certificates
(re-issued by the operator after Step 01).

| Hostname | HAProxy | Backend | TLS CN | SAN | Expiry |
|---|---|---|---|---|---|
| `drfarah.proxbenovh.cloud` | BM1 (87.98.174.211) | Hestia | `www.drfarah.proxbenovh.cloud` | `drfarah`, `www.drfarah` | 2026-10-24 |
| `www.drfarah.proxbenovh.cloud` | BM1 | Hestia | `www.drfarah.proxbenovh.cloud` | `drfarah`, `www.drfarah` | 2026-10-24 |
| `staging.drfarah.proxbenovh.cloud` | BM1 | Hestia | `*.staging.drfarah.proxbenovh.cloud` | `*.staging`, `staging` | 2026-10-24 |
| `api.drfarah.proxbenovh.cloud` | BM2 (51.75.57.153) | Traefik | `api.drfarah.proxbenovh.cloud` | `api`, `drfarah` | 2026-10-24 |
| `api.staging.drfarah.proxbenovh.cloud` | BM2 | Traefik | `api.staging.drfarah.proxbenovh.cloud` | `api.staging`, `staging` | 2026-10-24 |
| `admin.drfarah.proxbenovh.cloud` | BM1 | Hestia | `*.drfarah.proxbenovh.cloud` | `*.drfarah`, `proxbenovh` | 2026-10-24 |

**Pending:** `www` → apex redirect not yet configured (serves same content as
apex). Should be implemented in HAProxy or Hestia before production.

## Hestia / BM1

### Vhosts

| Domain | Docroot | Owner | Created |
|---|---|---|---|
| `drfarah.proxbenovh.cloud` | `/home/benweb/web/drfarah.proxbenovh.cloud/public_html` | `benweb` | 2026-07-26 (operator) |
| `staging.drfarah.proxbenovh.cloud` | `/home/benweb/web/staging.drfarah.proxbenovh.cloud/public_html` | `benweb` | 2026-07-26 (Step 02) |
| `admin.drfarah.proxbenovh.cloud` | `/home/benweb/web/admin.drfarah.proxbenovh.cloud/public_html` | `benweb` | 2026-07-26 (operator) |

### Mechanism

- Staging vhost created via: `sudo /usr/local/hestia/bin/v-add-web-domain benweb staging.drfarah.proxbenovh.cloud`
- Executed as `ben` user with `sudo` on Hestia host (192.168.100.75:2275).
- All `public_html/` directories confirmed writable by `benweb` (`benweb:www-data`, `drwxr-xr-x`).
- Jenkins deploys will use `hestia-benweb-ssh` credential (ssh as `benweb`).

### Admin 503 resolution

Admin vhost returned 503 in Step 01, now returns 200. Likely resolved by a
Hestia `v-rebuild-web-domain` or HAProxy reload after the operator's TLS update.
No manual fix was applied in this step.

## Kubernetes / BM2

### Namespace

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: drfarah
  labels:
    app.kubernetes.io/name: drfarah
    app.kubernetes.io/part-of: drfarah-vip-urgent-care
    app.kubernetes.io/managed-by: jenkins
```

Created via `kubectl create namespace drfarah` and labeled.

### Harbor pull secret

- **Name:** `harbor-regcred`
- **Type:** `kubernetes.io/dockerconfigjson`
- **Source:** Copied from `toilettage` namespace.
- **Method:** `kubectl get secret -n toilettage harbor-regcred -o yaml | sed 's/namespace: toilettage/namespace: drfarah/' | kubectl apply -f -`
- **No secret data was printed, copied to Git, or exposed.**

### Rollback

- Delete namespace: `kubectl delete namespace drfarah` (destroys all resources within).
- Recreate: follow the same steps above.

## Keycloak

### Realm: drfarah (BLOCKED)

**Status:** NOT CREATED. Admin credentials were rotated after Helm chart
deployment. Current bootstrap password in `keycloak-admin-secret` is no longer
valid for the admin user.

**Required configuration (when access is available):**

```text
Realm:             drfarah
Client ID:         drfarah-admin
Client type:       public (client authentication OFF)
Standard flow:     ON
Direct access:     OFF
PKCE:              S256
Redirect URIs:     https://admin.drfarah.proxbenovh.cloud/*
Post-logout URIs:  https://admin.drfarah.proxbenovh.cloud/*
Web origins:       https://admin.drfarah.proxbenovh.cloud
Roles:             clinic-admin, clinic-staff
```

**MFA:** Enable only if safe (do not lock out existing administrators).

### Keycloak admin credentials

- **Secret name in K3s:** `keycloak-admin-secret` (namespace `keycloak`)
- **Admin username:** `admin` (confirmed via `KC_BOOTSTRAP_ADMIN_USERNAME` in `keycloak-env-vars` ConfigMap)
- **Password:** Rotated. Current value unknown. The Helm bootstrap value is
  stored but no longer accepted for authentication.

**Next action:** Obtain current Keycloak admin credentials from the operator,
or have the operator create the `drfarah` realm through the admin console.

## Harbor

### Classification: NOT REQUIRED YET

The `drfarah-api` image repository does not exist. Harbor auto-creates
repositories on first `docker push` if the pushing account has write permission.

**Expected path:** `harbor.proxbenovh.cloud/devops-project-harbor/drfarah-api`

**Robot account:** `harbor-robot-devops-project-harbor` (Jenkins credential,
used by `project_toilettage` for push/pull to `devops-project-harbor`).

**First-push behavior:** When Jenkins runs the API build stage for the first time
on `dev` or `main`, the `docker push` will auto-create the repository. No manual
pre-creation is needed unless Harbor project policy requires it.

## Deferred Items

### PostgreSQL

**Not created yet.** Will follow the `toilettage-postgres` pattern:

```text
StatefulSet:  drfarah-postgres
Service:      drfarah-postgres (ClusterIP)
PVC:          drfarah-postgres-pvc (local-path)
DB name:      drfarah
User:         drfarah
K8s Secret:   drfarah-postgres-secret
Jenkins cred: drfarah-postgres
```

Create during API implementation. Commit only `secret.example.yaml`.

### SMTP

**Not verified.** Reference project uses SORIA SMTP for testing. Pattern:

```text
Jenkins credential: drfarah-smtp
K8s Secret:         drfarah-smtp-secret
Environment vars:   SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_FROM
```

Create before email testing. Clinic production sender address must be confirmed
by Dr. Farah before production deployment.

### Backups

**BLOCKER before production.** No backup destination is defined for any project.
The `toilettage` reference project also lists this as pending work.

Requirements:
- Automated `pg_dump` CronJob in the `drfarah` namespace or cluster-wide backup.
- External storage target (S3-compatible, NFS, or external host).
- Retention policy.
- Documented restore procedure and a verified restore test before production.

## Applied Mechanisms

| Action | Command/Tool | Host |
|---|---|---|
| TLS recheck | `openssl s_client -verify_hostname`, `curl --resolve` | Management VM |
| Hestia staging vhost | `v-add-web-domain benweb staging.drfarah.proxbenovh.cloud` | Hestia (BM1) via SSH |
| K3s namespace | `kubectl create namespace drfarah` | K3s (BM2) via kubeconfig |
| Harbor pull secret | `kubectl get -n toilettage ... | sed ... | kubectl apply -f -` | K3s (BM2) via kubeconfig |
| Keycloak inspection | `kubectl get secret/configmap -n keycloak`, `curl` auth attempt | K3s + Keycloak endpoint |

## Validation Checklist

- [x] All 6 TLS names: ssl_verify=0, matching SANs, valid expiry.
- [ ] www → apex redirect (not configured).
- [x] Hestia vhosts: all 3 exist, `benweb` owner, `public_html/` writable.
- [x] Admin 200 (503 resolved).
- [x] K3s namespace `drfarah`: Active with correct labels.
- [x] Harbor pull secret: present in `drfarah` namespace, correct type.
- [ ] Keycloak realm `drfarah`: NOT CREATED (blocked on admin credentials).
- [x] No secrets in Git diff.
- [x] Bootstrap Jenkinsfile remains non-deploying.
- [x] No application code, Dockerfiles, or K8s app manifests committed.
