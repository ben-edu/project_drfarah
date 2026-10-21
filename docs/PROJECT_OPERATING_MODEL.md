# Project Operating Model — Dr. Farah VIP Urgent Care

## 1. Why this document exists

This repository now serves as the durable operational memory for the Dr. Farah
project across website, booking, marketing, reputation, growth and analytics.

The previous operating model used many specialized ChatGPT tabs. That created
useful focused work, but it also fragmented context, duplicated decisions and
made continuity dependent on chat context windows.

The new model consolidates active reasoning into one ChatGPT workspace while
preserving workstream identity through GitHub documentation and OpenProject work
packages.

## 2. System roles

### GitHub — durable project memory and technical source

GitHub is the primary durable reference for:

- project charter and stable facts;
- cross-workstream roadmap;
- current handoff/resume point;
- approved decisions;
- technical implementation;
- deployment evidence;
- durable runbooks;
- session history;
- code and configuration.

No material project fact, decision, blocker or next-step dependency should exist
only in chat.

### OpenProject — live execution control

OpenProject remains authoritative for:

- work-package status;
- assignee;
- dates;
- dependencies;
- milestones;
- completion;
- evidence links;
- formal execution tracking.

GitHub may summarize or reference OpenProject but must not invent live statuses.

### ChatGPT — reasoning and action interface

The single active project chat is used for:

- analysis;
- research;
- planning;
- synthesis;
- drafting;
- account audits;
- technical review;
- execution through connected tools;
- converting decisions into GitHub/OpenProject-ready outputs.

Chat is not the durable source of truth.

### Live external systems — configuration/performance authority

Examples:

- Google Ads for current ad-account state;
- Google Business Profile for current profile state;
- Google Search Console for Google organic search reporting;
- GA4 for configured analytics reporting;
- booking/admin platform for appointment state;
- Jenkins for accepted deployment pipeline evidence;
- live production endpoints for current public behavior.

## 3. Minimum durable files

The project intentionally keeps a small set of core files.

### `README.md`
Entry point and reading order.

### `PROJECT.md`
Stable project charter, product/business context and technical architecture.
Update only when durable facts, scope or architecture change.

### `ROADMAP.md`
Cross-workstream sequencing, dependencies, gates, parallelization and phase
logic. Update when execution strategy changes.

### `HANDOFF.md`
Current state and exact resume point. This is the first operational file to
update after a material session.

### `docs/DECISIONS.md`
Approved decisions only. Do not store hypotheses as decisions.

### `SESSION_LOG.md`
Short append-only historical record of meaningful sessions/releases/decisions.
It is not the current-state document.

Other documentation may exist for technical runbooks or architecture, but the
six files above are the control plane.

## 4. Evidence labels

Use the following labels in analysis and durable documentation when a statement
could materially affect a decision:

- `FACT` — directly verified.
- `HYPOTHESIS` — plausible but unproven.
- `DECISION` — explicitly approved.
- `DATA_GAP` — evidence is missing or unavailable.
- `RISK` — downside requiring active control.
- `BLOCKER` — dependency that prevents a required downstream action.

## 5. Workstream consolidation

The separate ChatGPT tabs previously aligned to OpenProject workstreams are now
consolidated into one active chat. Their logical identities remain:

- BG-00 Governance, Decisions & Measurement
- BG-10 Website & Conversion
- BG-20 Google Ads & Paid Acquisition
- BG-30 Google Business, Local SEO & Reputation
- BG-40 Hotel / Traveler / VIP Growth
- BG-50 Pre-Op Referral Engine
- BG-60 Video, Social & Creative
- BG-70 Service Priority & Economics
- BG-80 Analytics & Growth Intelligence
- BG-90 Operations / Compliance Readiness

The active chat should name the relevant workstream/work package when performing
substantive work, but a separate chat tab is no longer required.

## 6. Session start protocol

At the start of a new substantial session:

1. Read `HANDOFF.md`.
2. Read the current-priority section of `ROADMAP.md`.
3. Read `docs/DECISIONS.md` if the task may change strategy, scope or approval.
4. Read the relevant implementation/runbook file only when needed.
5. Check live systems or OpenProject when the task depends on current state.

Do not reconstruct current state from old chat history when GitHub contains a
newer handoff.

## 7. Session close protocol

A material session is not complete until its durable state is recorded.

At minimum:

1. Update `HANDOFF.md` with:
   - what changed;
   - evidence;
   - unresolved blockers;
   - exact next step;
   - restart condition for paused/blocked work.
2. Update `ROADMAP.md` only if ordering, phase state or gates changed.
3. Update `docs/DECISIONS.md` only for approved decisions.
4. Update `PROJECT.md` only for stable facts/scope/architecture.
5. Append a concise entry to `SESSION_LOG.md`.
6. Preserve or link evidence in OpenProject when relevant.

## 8. Handoff state template

Use this structure inside `HANDOFF.md`:

```markdown
## Current focus

**Workstream/WP:** ...
**State:** IN_PROGRESS / BLOCKED / ...
**Started/updated:** YYYY-MM-DD

### Verified facts
- ...

### Work completed
- ...

### Evidence
- commit / PR / account snapshot / OpenProject link / live check

### Blockers / risks
- BLOCKER: ...
  - hard/soft: ...
  - unblock evidence: ...

### Exact next action
1. ...
2. ...

### Safe parallel work
- ...

### Do not do yet
- ...
```

## 9. Paused and blocked work

When work is paused or blocked, never remove it from the roadmap.

Record:

- owner/workstream;
- current state;
- reason;
- hard vs soft dependency;
- exact evidence/action needed to restart;
- what downstream work is prohibited;
- what independent work may continue.

A later session must check blocked work before creating lower-priority new work.

## 10. Decision protocol

A recommendation is not a decision.

For significant changes, document:

1. evidence;
2. uncertainty;
3. expected business/technical effect;
4. alternative(s) considered;
5. approval required;
6. approved decision;
7. implementation owner/work package;
8. validation plan.

For external write actions such as Google Ads, GBP, production configuration or
customer-facing publication, preserve the before-state and get explicit approval
when required by the operating boundary.

## 11. Website/marketing handoff protocol

When marketing analysis identifies a website need, create a structured handoff:

```markdown
### HANDOFF — Marketing → Website

**Source workstream:** BG-20 / BG-30 / BG-40 / BG-50 / BG-60
**Target workstream:** BG-10
**Evidence:** ...
**Affected page/path:** ...
**Required change:** ...
**Business reason:** ...
**Tracking requirement:** ...
**Primary KPI:** ...
**Dr. Farah approval needed:** ...
**Acceptance evidence:** ...
```

When the website creates a measurement capability required by marketing, record
the reverse handoff and validation result.

## 12. Marketing/account write-control protocol

Default mode for connected accounts:

`read → analyze → recommend → approve → change → validate → measure`

Do not make broad Google Ads, GBP or production changes solely because a tool
supports write access.

For every material account write:

- capture current state;
- identify exact object/setting;
- explain reason;
- obtain approval when required;
- perform one bounded change;
- record date/time;
- define validation/measurement window;
- record outcome.

## 13. Privacy and clinical boundary

This repository and marketing stack are not an EHR or clinical decision system.

Do not store unnecessary:

- patient names;
- emails/phones in analytics documentation;
- diagnoses;
- symptoms/free-text reasons;
- medications;
- clinical notes;
- lab results;
- insurance/member identifiers;
- medical documents.

Use opaque identifiers and business-level outcomes where linkage is necessary.

## 14. Release and branch discipline

The current repository policy remains:

- feature/fix/documentation branches for proposed work;
- `dev` is the integration/staging branch;
- `main` is production;
- Jenkins is the deployment authority;
- no direct routine commits to `main`;
- no secrets in Git.

Documentation that changes execution strategy should normally arrive through a
reviewable PR into `dev`.

## 15. Definition of a healthy project control plane

The control plane is healthy when a new operator can determine, without reading
old chat threads:

- current production state;
- current business/growth priorities;
- what is in progress;
- what is blocked and why;
- what can proceed in parallel;
- exact next actions;
- required approvals;
- relevant OpenProject work package;
- where acceptance evidence belongs.

If that cannot be answered, update the GitHub control files before adding more
work.
