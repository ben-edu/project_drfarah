# Architecture

Architecture decisions and diagrams for the Dr. Farah VIP Urgent Care project.

## Documents

| File | Purpose |
|---|---|
| `ENVIRONMENT_ISOLATION.md` | Staging/production namespace separation rationale and mapping |
| `INFRASTRUCTURE_FOUNDATION.md` | Step 02 provisioning record — domains, TLS, Hestia, K3s, Keycloak |

## Design

| File | Purpose |
|---|---|
| `../design/DESIGN_SYSTEM_V2.md` | **Current** — approved frontend design prototype v2 — richer visuals, assets, cookie notice, SEO, fuller slot UI |
| `../design/DESIGN_SYSTEM_V1.md` | Approved frontend design prototype v1 — visual system, IA, placeholders (superseded by v2) |

## Deployment

| File | Purpose |
|---|---|
| `../deployment/FRONTEND_STAGING.md` | Staging frontend deployment — branch mapping, mechanism, rollback |

## Status

Phase 1: website + booking foundation. Frontend prototype integrated; staging deployment configured; API scaffold complete.

## Reference documents (outside repository)

- `~/projects/drfarah-project/project-sources/01_INFRA_BASELINE.md` — platform
  infrastructure facts (hosts, networks, credentials, hard rules).
- `~/projects/drfarah-project/project-sources/02_DELIVERY_PLAYBOOK.md` —
  end-to-end setup recipe and Jenkinsfile template.
- `~/projects/drfarah-project/project-sources/03_APP_BLUEPRINT.md` —
  application patterns and reference snippets.
