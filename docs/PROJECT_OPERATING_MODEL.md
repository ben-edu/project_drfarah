# Project Operating Model — Dr. Farah VIP Urgent Care

## 1. Purpose

This repository is the durable operational memory for the Dr. Farah project across website, booking, Google marketing, local SEO, reputation, growth experiments, analytics and operational readiness.

The project uses **one active ChatGPT project workspace: the existing BG-20 tab**. Former specialized tabs may be retired because their workstreams and work packages are preserved in `ROADMAP.md` and OpenProject.

Chat context is disposable. GitHub continuity is not.

## 2. System roles

### GitHub — durable project memory

GitHub is authoritative for:

- single master roadmap;
- current handoff/resume state;
- approved decisions;
- stable project/business facts;
- technical implementation;
- runbooks/specifications;
- durable evidence and session history.

No material project fact, decision, blocker or restart condition should exist only in chat.

### OpenProject — live execution control

OpenProject remains authoritative for:

- work-package status;
- assignee;
- dates;
- dependencies;
- milestones;
- completion;
- formal execution evidence/links.

GitHub may map/summarize OpenProject work, but must not invent a live status.

### Single ChatGPT workspace — reasoning/action interface

The existing BG-20 tab is now the unified workspace for all BG-00 through BG-90 workstreams.

Use it for:

- analysis/research;
- account audits;
- technical review;
- planning and decision support;
- execution through connected tools;
- cross-workstream handoffs;
- updating GitHub/OpenProject-ready outputs.

Do not require separate tabs for each workstream.

### Live systems — state authority

Examples:

- Google Ads;
- Google Business Profile;
- Google Search Console;
- GA4;
- booking/admin platform;
- Jenkins;
- production/staging endpoints.

When live state can change, verify it instead of relying on an older document.

## 3. Core control files

### `README.md`
Entry point and reading order.

### `PROJECT_HANDOFF.md`
**Live current-state and exact resume file.** Update after every material session.

### `ROADMAP.md`
**Only master sequencing document.** Contains phases, dependencies, gates, parallelization and workstream inventory.

### `docs/DECISIONS.md`
Approved decisions only.

### `docs/GIT_RELEASE_STRATEGY.md`
Approved detailed branch/release procedure. Defines the normal `feature/fix/docs -> dev -> main` flow, production-hotfix exception, immediate back-merge requirement and branch-lineage checks.

### `docs/BUSINESS_GROWTH_SOURCE.md`
Compact durable business/growth context; not a live-account substitute.

### `PROJECT.md`
Stable website/product/technical charter; not a competing roadmap.

### `HANDOFF.md`
Detailed/historical website/deployment evidence; not the current cross-workstream resume file.

### `SESSION_LOG.md`
Historical session/release log.

Technical runbooks/specifications may exist under `docs/`, but do not replace `ROADMAP.md` for sequence or `PROJECT_HANDOFF.md` for current state.

## 4. Evidence labels

Use:

- `FACT` — directly verified;
- `HYPOTHESIS` — plausible but unproven;
- `DECISION` — explicitly approved;
- `DATA_GAP` — evidence missing;
- `RISK` — downside requiring control;
- `BLOCKER` — dependency preventing required downstream action.

## 5. Workstream consolidation

Logical/OpenProject workstreams remain:

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

The single chat should name the relevant workstream/work package when performing substantive work.

## 6. Session start protocol

For a substantive session:

1. read `README.md` if orientation is needed;
2. read `PROJECT_HANDOFF.md`;
3. read the current-priority/relevant phase in `ROADMAP.md`;
4. read `docs/DECISIONS.md` if strategy/approval is involved;
5. read only the relevant specification/runbook/baseline/code;
6. verify live system state when it may have changed;
7. query OpenProject when live execution metadata matters;
8. before production/release work, inspect current `dev` and `main` heads and branch lineage per `docs/GIT_RELEASE_STRATEGY.md`.

Do not reconstruct current state from old chat history when GitHub has newer evidence.

## 7. Task-selection and blocker protocol

Use the roadmap state model.

When blocked:

1. record the item in `PROJECT_HANDOFF.md`;
2. classify HARD or SOFT;
3. record exact unblock evidence;
4. record prohibited downstream work;
5. identify safe parallel work;
6. continue with the highest-priority eligible READY item;
7. re-check blocked higher-priority items at the next session.

Never silently abandon blocked work.

## 8. Material-session close protocol

Before ending material work:

1. update `PROJECT_HANDOFF.md` with what changed, evidence, blockers and exact next action;
2. update `ROADMAP.md` only if sequencing/gates/scope changed;
3. update `docs/DECISIONS.md` only for an approved decision;
4. update stable business/project docs only when durable facts changed;
5. append concise history to `SESSION_LOG.md` where appropriate;
6. update OpenProject separately when live work-package state/evidence changes.

## 9. Website/marketing handoff protocol

When acquisition/local/content analysis identifies website work, record:

- source workstream;
- target BG-10 requirement;
- evidence;
- affected path/page;
- exact change;
- business/search reason;
- tracking requirement;
- KPI;
- claim/approval requirement;
- acceptance evidence.

When website implementation creates marketing measurement capability, record the reverse handoff and validation result.

## 10. External-account write protocol

Default mode:

`read → preserve before-state → analyze → decide/approve → bounded change → validate → measure → record evidence`

Do not make broad Google Ads/GBP/production changes merely because a tool supports write access.

High-confidence factual corrections may be executed when authorized, but still preserve evidence and validation.

## 11. Marketing data/privacy principle

Use the strongest useful lawful and platform-compliant measurement/marketing capability; do not add arbitrary restrictions that reduce business learning without a legal/policy reason.

At the same time:

- this project is not an EHR;
- do not send/store unnecessary diagnoses, free-text symptoms, medications, clinical notes, lab results, medical documents or insurance/member identifiers in marketing/analytics systems;
- use opaque/internal linkage where practical;
- keep marketing identifiers and business outcomes separate from clinical-record content;
- align public privacy/cookie disclosures with actual implemented behavior and applicable requirements.

## 12. Branch/release discipline

Detailed procedure: `docs/GIT_RELEASE_STRATEGY.md`.

Core rules:

- feature/fix/docs branches are based on the current integration state and are proposed through PRs;
- `dev` = integration/staging;
- `main` = production;
- normal flow is `feature/fix/docs -> dev -> main`;
- before a normal production promotion, current `main` must already be contained in `dev`; if not, reconcile `main -> dev` first;
- normal production releases promote the coherent validated `dev` state, not a manually reconstructed subset;
- direct `main` hotfixes are exceptional and only for urgent production recovery/production-only needs;
- every direct `main` hotfix or selective production release requires immediate back-merge/reconciliation into `dev` and CI validation there;
- selective promotion/cherry-picking from `dev` is an exception only when the rest of `dev` is intentionally not production-ready and independence/dependencies are explicitly verified;
- do not treat a file tested on `dev` as independently production-safe without checking its code/config/runtime dependencies;
- before production merge, inspect exact `dev`/`main` heads, complete diff and CI status;
- `PROJECT_HANDOFF.md` records any material branch divergence/reconciliation state;
- unresolved branch drift is a release-control issue and must not be silently carried forward;
- Jenkins is deployment authority;
- no routine direct commits to `main`;
- no secrets in Git.

Once the unified control PR is merged, Project Sources should point to `dev` and should not need a special control-branch fallback.

## 13. Project Source policy

ChatGPT Project Source `.md` files are bootstrap/router files only.

They should tell AI:

- repository identity;
- reading order;
- authority hierarchy;
- single-tab operating model;
- source/workstream routing;
- durable-update rule.

They should not duplicate live strategy, current KPI values, service lists or task status.

## 14. Definition of a healthy control plane

A new context/operator can answer without old chats:

- what is the current focus?
- what is blocked and why?
- what can proceed safely?
- what is the next exact action?
- which roadmap phase/workstream owns it?
- what evidence proves completion?
- which live system/OpenProject source must be checked?
- are `dev` and `main` in a valid release relationship, or is reconciliation required first?

If those answers cannot be found from `PROJECT_HANDOFF.md` + `ROADMAP.md` + targeted evidence, the control plane needs repair before more complexity is added.
