# Dr. Farah VIP Urgent Care — Project Repository

This repository is the durable source for the Dr. Farah VIP Urgent Care website, booking platform, Google marketing, local SEO/reputation, growth workstreams, measurement and future Growth Intelligence work.

The project uses **one active ChatGPT project workspace: the existing BG-20 tab**. The former specialized tabs are represented as logical/OpenProject workstreams inside the single master roadmap.

## Start here

Read in this order for a new substantial session:

1. [`PROJECT_HANDOFF.md`](PROJECT_HANDOFF.md) — current state, blockers and exact next actions.
2. [`ROADMAP.md`](ROADMAP.md) — the **only master roadmap**: phases, gates, dependencies, workstream inventory and safe parallelization.
3. [`docs/DECISIONS.md`](docs/DECISIONS.md) — approved decisions only.
4. [`docs/BUSINESS_GROWTH_SOURCE.md`](docs/BUSINESS_GROWTH_SOURCE.md) — compact durable business/growth context.
5. [`docs/PROJECT_OPERATING_MODEL.md`](docs/PROJECT_OPERATING_MODEL.md) — how GitHub, OpenProject, the single ChatGPT workspace and live systems interact.
6. [`PROJECT.md`](PROJECT.md) — stable website/product/technical charter.
7. Only the relevant baseline/spec/runbook/code for the task at hand.

`HANDOFF.md` is detailed/historical website/deployment evidence. It is **not** the current unified resume file.

## Authority model

- **GitHub:** durable roadmap, current handoff, decisions, stable facts, code, runbooks and evidence.
- **OpenProject:** live work-package status, assignee, dates, dependencies, milestones and completion.
- **Single ChatGPT workspace (BG-20):** reasoning, research and execution interface; not durable truth.
- **Live systems:** authority for their own current state (Google Ads, GBP, Search Console, GA4, booking/admin, Jenkins, production endpoints).

No material project result should exist only in chat.

## Consolidated workstreams

- BG-00 — Governance, Decisions & Measurement
- BG-10 — Website & Conversion
- BG-20 — Google Ads & Paid Acquisition
- BG-30 — Google Business, Local SEO & Reputation
- BG-40 — Hotel / Traveler / VIP Growth
- BG-50 — Pre-Op Referral Engine
- BG-60 — Video, Social & Creative
- BG-70 — Service Priority & Economics
- BG-80 — Analytics & Growth Intelligence
- BG-90 — Operations / Compliance Readiness

Separate ChatGPT tabs are not required. OpenProject workstream identities remain valid.

## Current project principle

Do not launch meaningful paid traffic into an unhealthy booking path or unvalidated measurement system.

Use the current queue in `PROJECT_HANDOFF.md`; do not infer current priority from this README.

## Environment domains

| Purpose | Host |
|---|---|
| Frontend production | `drfarahvipurgentcare.com` |
| Frontend canonical alias | `www.drfarahvipurgentcare.com` → apex |
| Frontend staging | `staging.drfarahvipurgentcare.com` |
| API production | `api.drfarahvipurgentcare.com` |
| API staging | `api-staging.drfarahvipurgentcare.com` |
| Admin production | `admin.drfarahvipurgentcare.com` |
| Admin staging | `admin-staging.drfarahvipurgentcare.com` |

## Core control-plane layout

```text
.
├── README.md
├── PROJECT_HANDOFF.md             # Live unified resume point
├── ROADMAP.md                     # Only master project roadmap
├── PROJECT.md                     # Stable website/product/technical charter
├── HANDOFF.md                     # Historical/detailed website deployment handoff
├── SESSION_LOG.md
├── docs/
│   ├── DECISIONS.md
│   ├── BUSINESS_GROWTH_SOURCE.md
│   ├── PROJECT_OPERATING_MODEL.md
│   ├── CONVERSION_MEASUREMENT_SPEC.md
│   ├── MEASUREMENT_BASELINE_*.md
│   ├── GOOGLE_ADS_BASELINE_*.md
│   ├── GBP_BASELINE_*.md
│   └── ... detailed runbooks/baselines/specifications
├── frontend/
├── admin/
├── api/
└── kubernetes/drfarah/
```

Detailed runbooks/specifications may describe implementation, but they do not become competing roadmaps.

## Branch and deployment rules

- proposed work uses a dedicated feature/fix/docs branch;
- `dev` is integration/staging;
- `main` is production;
- Jenkins is deployment authority;
- no routine direct commits to `main`;
- no secrets in Git.

## Resume rule

A new session should not need old ChatGPT history. It should:

`read PROJECT_HANDOFF → read relevant ROADMAP phase → verify live state → execute → validate → update PROJECT_HANDOFF`

If a blocker appears, record hard/soft status, unblock evidence, prohibited downstream work, safe parallel work and exact restart point.
