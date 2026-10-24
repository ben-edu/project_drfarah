# PROJECT HANDOFF — Dr. Farah VIP Urgent Care

> **Live cross-workstream resume document.**  
> Read this first when resuming the project. Historical deployment detail remains in `HANDOFF.md`.

**Last updated:** 2026-10-24  
**Repository:** `ben-edu/project_drfarah`  
**Integration branch:** `dev`  
**Active documentation branch / PR:** `docs/unified-project-control-20261021` / PR #78  
**Roadmap:** `ROADMAP.md`

## 1. Authority model

- **GitHub:** durable project memory, roadmap, handoff, decisions, code and evidence.
- **OpenProject:** authoritative for live work-package status, owner, dates, dependencies, milestones and completion.
- **Live systems:** authoritative for their own current state.
- **ChatGPT:** analysis/execution interface; never the sole durable record.

Separate ChatGPT workstream tabs are being retired in favor of one unified project chat. The BG-00 through BG-90 workstream identities remain valid for OpenProject mapping and ownership.

## 2. Immediate project focus

Current focus is conversion infrastructure + Google marketing forensic audit + relaunch readiness.

Current sequence:

`Booking health → live Google/website baselines → measurement architecture → visit_completed attribution → high-confidence corrections → demand/landing-page work → controlled paid relaunch → ongoing optimization`

The roadmap is gate-based, not rigidly linear. Safe read-only work may continue while an unrelated hard blocker is open.

## 3. Current access state

### GitHub

`FACT:` The connected GitHub account has sufficient repository permissions to read/write files, create branches/PRs/issues and maintain the project documentation workflow for `ben-edu/project_drfarah`.

### Google Ads

`FACT:` Windsor.ai now exposes Dr. Farah's Google Ads account directly:

- Customer ID: `652-510-3588`
- currency: USD
- timezone: `America/Los_Angeles`
- account status: ENABLED
- manager/MCC: false
- auto-tagging: enabled

Read access is working. Windsor also exposes supported write actions, but material external changes require explicit approval before execution.

### Google Business Profile

`FACT:` Windsor.ai now exposes the clinic profile directly:

- location resource: `locations/6719840585856592244`
- name: Dr Farah VIP Urgent Care

Read access is working; supported profile write actions are also available subject to explicit approval.

### GA4

`DATA GAP:` The only GA4 property currently visible through this Windsor context is for `safeguardsupport.com`, not Dr. Farah. The production Dr. Farah GA4 property is not yet connected/identified here.

### Google Search Console

`DATA GAP:` The visible properties are `behnam.fr`, `soria-academie.fr` and `soria-ai.fr`. The production `drfarahvipurgentcare.com` property is not yet connected/identified here.

### OpenProject

No direct OpenProject connector surfaced in the current plugin environment. This does **not** change its authority. GitHub remains the durable evidence/handoff layer and OpenProject status must be synchronized separately when work-package state matters.

## 4. Booking / Brevo

`BLOCKER B-001:` Booking/Brevo delivery remediation is active in a separate technical workflow.

- hard dependency for meaningful paid-media launch;
- soft dependency for Google Ads/GBP audits, measurement design, local SEO, historical analysis and demand research.

Close only after controlled production booking persistence and expected delivery behavior are verified.

## 5. Website measurement baseline

Source audit evidence is in `docs/MEASUREMENT_BASELINE_2026-10-21.md`.

`FACT:` Repository/source inspection found no implemented Google tag, GTM, GA4 event stack, Google Ads website conversion tag, booking analytics events or click-to-call analytics in the current frontend source.

`FACT:` production assembly does not inject these tags.

`FACT:` current booking code preserves only a coarse `source` value derived from `partner`, `source`, or `utm_source` and stores it in `appointments.source` (`String(32)`).

`FACT:` the current privacy page says the site uses essential cookies only and no advertising/third-party tracking. That statement must be revised when the actual marketing/analytics stack changes.

`DECISION DIRECTION:` use lawful, policy-compliant measurement as fully as useful for marketing; do not impose arbitrary restrictions. Do not transmit unnecessary clinical/medical details to advertising systems.

## 6. Conversion measurement direction

`docs/CONVERSION_MEASUREMENT_SPEC.md` contains the initial specification, but the operating model is now intentionally simplified around business outcomes.

Primary hierarchy:

`traffic → booking_request_created → confirmed appointment → visit_completed → revenue/contribution`

`FACT:` The appointment model already supports `pending`, `confirmed`, `cancelled`, `completed` and `no_show` states.

`DECISION DIRECTION:`

- `booking_request_created` remains a useful secondary/lead signal;
- `visit_completed` should become the principal acquisition-quality signal once click/source attribution and return-to-Google mechanics are validated;
- diagnostic web events may still be collected for troubleshooting/UX, but should not all be primary Google Ads conversions.

## 7. Google Ads live baseline — major correction

Full evidence: `docs/GOOGLE_ADS_BASELINE_2026-10-24.md`.

### Account measurement configuration

`FACT:` Auto-tagging is enabled.

`FACT:` Google Ads has an account-side Google tag destination:

- `AW-17076731177`

The tag exists in Google Ads configuration but is not implemented in the audited website source.

### Historical campaign evidence

`CORRECTION:` Earlier project information said no campaigns had run. Live Google Ads data disproves that.

One historical campaign is visible:

- campaign: **Urgent Care Medical Center**
- type: SMART
- current status: PAUSED
- serving period in queried history: June 2025 through February 2026
- impressions: **258,541**
- clicks: **5,590**
- spend: **$4,494.8619**
- Google Ads conversions: **16**
- conversion value: **$0**

Derived diagnostic values:

- CTR ≈ 2.16%
- average CPC ≈ $0.80
- platform conversion rate ≈ 0.29%
- cost per platform-reported conversion ≈ $280.93

These are not completed-visit CAC metrics.

### Existing Google Ads conversion actions

Live data shows seven actions in the audited view, including:

- Clicks to call — primary
- Smart campaign map directions — primary
- Calls from Smart Campaign Ads — primary; last conversion 2026-01-23
- Smart campaign ad clicks to call — primary
- Smart campaign map clicks to call — primary
- Local actions - Directions — primary
- `drfarahvipurgentcare.com (web) purchase` — hidden, secondary, GA4-origin

`RISK:` The current primary-goal mix is dominated by local/call/direction interactions rather than verified completed visits. Do not relaunch conversion-based bidding until the goal architecture is cleaned and validated.

BG-20 is therefore **historical forensic audit + measurement repair + controlled relaunch readiness**, not a pure pre-launch audit.

## 8. Google Business Profile live baseline

Full evidence: `docs/GBP_BASELINE_2026-10-24.md`.

### Current identity

- name: Dr Farah VIP Urgent Care
- status: OPEN
- primary category: Urgent care center
- additional categories: Medical clinic, Walk-in clinic, IV therapy service, Weight loss service, Physical examination center
- phone: (310) 467-0101
- website: https://drfarahvipurgentcare.com/
- address: 9229 Wilshire Blvd, Beverly Hills, CA 90210
- Voice of Merchant: true
- duplicate-location resource returned: none

### Hours discrepancy

Live GBP regular hours:

- Monday–Thursday: 8:30 AM–5:30 PM
- Friday: **8:30 AM–4:30 PM**

Project-confirmed clinic hours are Monday–Friday 8:30 AM–5:30 PM, with last patient before 5:00 PM.

`HIGH-PRIORITY CORRECTION CANDIDATE:` Friday closing time is inconsistent. Preserve baseline first; then correct after final operating confirmation.

### Reputation

`FACT:` current rating = **5.0**.

`FACT:` current review count = **109**. This supersedes the previous 108-review screenshot baseline.

### Recent 90-day GBP performance

- impressions: 3,860
- desktop Maps: 387
- desktop Search: 631
- mobile Maps: 1,608
- mobile Search: 1,234
- website clicks: 130
- call clicks: 120
- direction requests: 205

These are profile interactions, not completed visits.

### Service-catalog risk

The profile contains a very large free-form service catalog with many prices, treatment descriptions, medical claims, emergency-like wording and sensitive service categories.

`RISK:` Do not edit piecemeal. Audit the catalog systematically against current service availability, approved pricing, website positioning, Google policies and business priority.

## 9. Current priority queue

| Priority | Work | State | Acceptance / dependency |
|---:|---|---|---|
| 0 | Resolve booking/Brevo production delivery | IN_PROGRESS | controlled production booking + expected delivery evidence |
| 1 | Google Ads historical forensic/configuration audit | IN_PROGRESS | campaign, goals, geo, search/query, rules, changes, landing paths documented |
| 2 | GBP baseline and high-confidence corrections | IN_PROGRESS | full before-state captured; hours/service/category/description findings classified |
| 3 | Production measurement/tag implementation design | IN_PROGRESS | exact Google/GA4 IDs + consent/privacy architecture + attribution contract |
| 4 | `visit_completed` attribution implementation | READY | preserve click/source identifiers and map completed appointment outcome back to acquisition |
| 5 | Connect/verify Dr. Farah GA4 | WAITING_EXTERNAL | correct production property/data stream visible |
| 6 | Connect/verify Dr. Farah Search Console | WAITING_EXTERNAL | correct production property visible |
| 7 | Implement/validate Google tag + analytics/conversions | WAITING | architecture/IDs/privacy changes ready; deploy through Jenkins |
| 8 | Correct verified Ads/GBP/site foundation issues | READY as findings mature | before-state + exact approved change + validation |
| 9 | Demand/keyword/local competitor/service-priority research | READY | can proceed in parallel |
| 10 | Evidence-backed landing-page improvements | NOT_STARTED | formal BG-10 handoff |
| 11 | First controlled paid relaunch | BLOCKED | booking + measurement + goal cleanup + landing readiness |
| 12 | Ongoing review/reputation system | READY after GBP baseline acceptance | neutral compliant workflow + measurement |
| 13+ | Traveler, Pre-Op, Content, Growth Intelligence | NOT_STARTED | see roadmap gates |

## 10. Immediate next actions

Proceed without waiting for GA4/Search Console on work that does not depend on them:

1. finish Google Ads forensic audit: geo, targeting, campaign settings, historical search/query evidence, automated rules and change history;
2. finish GBP baseline: search keywords, reviews/replies, categories/services, description, links and current performance trends;
3. design the shortest robust attribution path to `visit_completed`;
4. define exact production Google tag / GA4 architecture and environment isolation;
5. revise privacy/cookie language in the same implementation cycle as the new tracking behavior;
6. correct only high-confidence factual GBP problems after explicit approval;
7. connect Dr. Farah GA4 and Search Console when available;
8. do not relaunch meaningful paid traffic until the booking and measurement gates are green.

## 11. Change-control rules

For material external changes:

1. preserve before-state/evidence;
2. classify FACT / HYPOTHESIS / DATA GAP / DECISION;
3. state exact proposed change and business reason;
4. obtain explicit approval where required;
5. execute one bounded change set;
6. validate result;
7. update GitHub evidence/handoff;
8. synchronize relevant OpenProject status/evidence separately.

Never leave a material result only in chat.
