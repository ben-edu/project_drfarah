# Dr. Farah VIP Urgent Care — Project Repository

Premium, physician-led website and booking system for Dr. Farah VIP Urgent Care
in Beverly Hills. Phase 1 delivers a conversion-focused public website and an
integrated appointment booking workflow. The current website
(`drfarahvipurgentcare.com`) is a research reference only — this is a clean-slate
build.

**Phase 1 explicitly excludes clinical AI.**

## Temporary domains

| Purpose | Host |
|---|---|
| Frontend prod | `drfarah.proxbenovh.cloud` |
| Frontend canonical alias | `www.drfarah.proxbenovh.cloud` → redirect to apex |
| Frontend staging | `staging.drfarah.proxbenovh.cloud` |
| API prod | `api.drfarah.proxbenovh.cloud` |
| API staging | `api.staging.drfarah.proxbenovh.cloud` |
| Admin | `admin.drfarah.proxbenovh.cloud` |

## Repository layout

```
.
├── README.md
├── PROJECT.md                    # Approved project brief
├── HANDOFF.md                    # Session handoff notes
├── SESSION_LOG.md                # Dated session log
├── .gitignore
├── Jenkinsfile
├── docs/
│   ├── READINESS_AUDIT.md        # Infrastructure readiness
│   ├── DECISIONS.md              # Approved decisions
│   └── architecture/
├── frontend/                     # Public website (Hestia / BM1)
├── admin/                        # Admin SPA (Hestia / BM1)
├── api/                          # FastAPI booking API (K3s / BM2)
└── kubernetes/drfarah/           # K8s manifests
```

## Branch and deployment rules

- `feature/*` → `dev` (staging) → `main` (temporary production).
- Do not commit directly to `main`.
- Deployment is performed only by Jenkins.
- No secrets in Git — commit only `*.example` files.

## Key documents

- [PROJECT.md](PROJECT.md) — approved product brief, scope, data model, stack.
- [docs/READINESS_AUDIT.md](docs/READINESS_AUDIT.md) — infrastructure readiness
  with evidence and next actions.
- [HANDOFF.md](HANDOFF.md) — current branch, work completed, next step.

## Infrastructure reference (outside repository)

- `~/projects/drfarah-project/project-sources/01_INFRA_BASELINE.md`
- `~/projects/drfarah-project/project-sources/02_DELIVERY_PLAYBOOK.md`
- `~/projects/drfarah-project/project-sources/03_APP_BLUEPRINT.md`
- `~/projects/drfarah-project/project-sources/example-toilettage.md`
