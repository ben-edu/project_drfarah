# Dr. Farah VIP Urgent Care — Project Repository

This repository is the durable project memory and technical source for the Dr.
Farah VIP Urgent Care website, booking system, Google marketing, local SEO,
reputation, growth experiments and future analytics/growth-intelligence work.

The project now uses **one active ChatGPT workspace** instead of separate chat
tabs for every OpenProject workstream. GitHub preserves the durable context so
work can continue safely when chat context windows end.

## Start here

For a new session or operator, read in this order:

1. [`PROJECT_HANDOFF.md`](PROJECT_HANDOFF.md) — current state, blockers and exact next action.
2. [`ROADMAP.md`](ROADMAP.md) — cross-workstream phases, dependencies, gates and safe parallelization.
3. [`docs/DECISIONS.md`](docs/DECISIONS.md) — approved decisions only.
4. [`docs/BUSINESS_GROWTH_SOURCE.md`](docs/BUSINESS_GROWTH_SOURCE.md) — consolidated business/growth context.
5. [`docs/PROJECT_OPERATING_MODEL.md`](docs/PROJECT_OPERATING_MODEL.md) — how GitHub, OpenProject, ChatGPT and live systems interact.
6. [`PROJECT.md`](PROJECT.md) — deeper stable product/technical charter.

`HANDOFF.md` remains the detailed historical website/deployment handoff. Use
`PROJECT_HANDOFF.md` for the current unified cross-workstream resume point.

## Authority model

- **GitHub:** durable roadmap, current handoff, decisions, code, runbooks and technical evidence.
- **OpenProject:** live work-package status, assignment, dates, dependencies, milestones and completion.
- **ChatGPT:** reasoning, research and execution interface; not durable source of truth.
- **Live systems:** authority for their own current state (Google Ads, GBP, Search Console, GA4, booking/admin, Jenkins, production endpoints).

No material decision, blocker or project fact should exist only in chat.

## Consolidated workstreams

The former specialized chat tabs remain as logical OpenProject workstreams but
are handled from one active project chat:

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

## Current top-level priority

Do not launch meaningful paid Google Ads traffic until the booking path and
measurement foundation are validated.

Current high-level sequence:

`Booking health → Measurement inventory → Conversion specification → Google account baselines → Measurement validation → Foundation corrections → Demand/landing pages → First controlled paid experiment`

Read `PROJECT_HANDOFF.md` for the live queue and blockers.

## Environment domains

| Purpose | Host |
|---|---|
| Frontend prod | `drfarahvipurgentcare.com` |
| Frontend canonical alias | `www.drfarahvipurgentcare.com` → redirect to apex |
| Frontend staging | `staging.drfarahvipurgentcare.com` |
| API prod | `api.drfarahvipurgentcare.com` |
| API staging | `api-staging.drfarahvipurgentcare.com` |
| Admin prod | `admin.drfarahvipurgentcare.com` |
| Admin staging | `admin-staging.drfarahvipurgentcare.com` |

## Repository layout

```text
.
├── README.md
├── PROJECT_HANDOFF.md             # Live unified resume point
├── ROADMAP.md                     # Unified phased roadmap and gates
├── PROJECT.md                     # Stable product/technical charter
├── HANDOFF.md                     # Historical/detailed website deployment handoff
├── SESSION_LOG.md                 # Historical session log
├── Jenkinsfile
├── docs/
│   ├── BUSINESS_GROWTH_SOURCE.md  # Consolidated business/growth source
│   ├── PROJECT_OPERATING_MODEL.md # Control-plane rules
│   ├── DECISIONS.md               # Approved decisions
│   ├── READINESS_AUDIT.md
│   ├── EMAIL_DELIVERY_RUNBOOK.md
│   └── ... technical runbooks
├── frontend/
├── admin/
├── api/
└── kubernetes/drfarah/
```

## Branch and deployment rules

- proposed work uses a dedicated feature/fix/docs branch;
- `dev` is the integration/staging branch;
- `main` is production;
- do not commit directly to `main` as a routine workflow;
- deployment is performed only by Jenkins;
- no secrets in Git — commit only safe examples/references.

## Session close rule

After a material session:

1. update `PROJECT_HANDOFF.md`;
2. update `ROADMAP.md` only if sequence/gates changed;
3. update `docs/DECISIONS.md` only for approved decisions;
4. update `PROJECT.md` only for durable scope/fact/architecture changes;
5. preserve relevant execution evidence in OpenProject;
6. never leave an important result only in chat.
