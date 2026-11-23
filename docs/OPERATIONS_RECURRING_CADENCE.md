# Recurring Business & Growth Operations — Dr. Farah

**Established:** 2026-11-23  
**Status:** ACTIVE OPERATING CADENCE / not an automated promise  
**Project:** `ben-edu/project_drfarah`  
**Review queue:** [GitHub Issue #146](https://github.com/ben-edu/project_drfarah/issues/146)  
**Canonical plan:** `ROADMAP.md`; **resume state:** `PROJECT_HANDOFF.md`; **approved decisions:** `docs/DECISIONS.md`  
**Timezone for clinic/Google Ads reviews:** `America/Los_Angeles` (Pacific; local DST observed). GitHub commit timestamps may be UTC.

## Operating principles

1. **Recurring checks are never "done forever".** Mark an individual review date as completed, maintain the task as recurring, and set its **next due**. A passing Jenkins report proves that snapshot only, not continuous compliance.
2. **Source-of-truth precedence:** clinic-confirmed patients / revenue; Google Ads native account for current ad settings and billed ledger; booking/first-party sources for visit outcome; Jenkins output for reporting execution; GitHub docs for audit decisions. OpenProject remains authoritative for live work-package ownership/status. A Google Ads conversion or call click is not a completed patient.
3. **Read-first and least privilege:** Review runs are read-only. Do not auto-apply or automatically dismiss Google Ads recommendations, change budget/bids/keywords, send clinical data to ad vendors, or activate new marketing campaigns without explicit owner authorization and current-state readback.
4. **Evidence format for each cycle:** `checked_at`, `data_window`, `timezone`, source/tool and commit/build, current values, exceptions, proposed decision + owner approval if needed, `next_due`, GitHub/issue link. Keep only aggregate/non-identifying counts and redacted GAQL terms in durable public logs.
5. **Trigger rules:** Any budget > approved value, unexpected schedule, campaign status change, Ads/booking outage, billing anomaly, policy disapproval, tracking failure, or material claim change triggers an immediate out-of-cycle review. Never rely solely on time-based checks.
6. **Do not confuse schedules:** Jenkins `GitHub hook trigger for GITScm polling` is for Git pushes **only**. It is not the recurring Ads/Business review scheduler. Unless a trigger is separately configured and proven, the owner/operator starts Jenkins jobs. The ChatGPT assistant can modify source via GitHub, but cannot assert that it automatically executed Jenkins.

## Recurring runbook

| ID | Activity | Cadence / recommended due (Pacific) | Owner / execution path | Minimum check, evidence, decision gate |
|---|---|---|---|---|
| R01 | Ads budget, campaign status, schedule and API connectivity | **Every clinic business day**, before 08:30 (target 08:00) and after any Ads mutation | Growth operator; Jenkins `REPORT=budgets`, `campaigns`, `schedules`, `OUTPUT_FORMAT=summary` | Urgent $10/day, Traveler $5/day, three enabled campaigns have 15 Mon–Fri 08:30–16:30 windows; Legacy Smart paused, Near Me ad group paused. Investigate drift immediately; no automatic restorative write. Check Local Services costs separately. |
| R02 | Google Ads Recommendations | **Weekly Monday** (target 09:00) and immediately after material Google Ads changes | Growth operator/analyst; Jenkins `REPORT=recommendations` read-only | Count/types and campaign, detailed suggested keywords/ads/assets, current approved budget, historical decisions, owner approval status. Categorize ACCEPT CANDIDATE / DEFER / REJECT FOR NOW; **no automatic Apply/Dismiss**. Save dated evidence and next due. |
| R03 | Ads served performance and term quality | **Weekly Monday**, previous closed Mon–Sun local week; quick anomaly scan each workday | Growth operator; `daily`, `ad_groups`, `search_terms` | Spend/clicks/impressions/CPC, search-term covered cost vs campaign spend, top paid irrelevant/competitor/insurance queries, near-me conversion evidence; draft *specific* negative keyword candidates only after service/patient-quality review. |
| R04 | Calls → leads → bookings → completed visits | **Weekly Friday** after reception reconciliation, and monthly finalization | Clinic reception/owner supplies non-PII aggregates; growth analyst checks booking source | Calls answered, qualified, no-answer, appointments, completed visits, source confidence and cost per confirmed visit. Dr. Farah's "2 patients last week" is a report, not proven Ads-attribution. Never store patient identity/clinical details in GitHub or Ads. |
| R05 | Billing, pacing, credits and independent Local Services charges | **Weekly Monday** provisional; **monthly** on available invoice/statement, plus immediate spend anomaly | Owner/finance + Ads operator; **native Google Ads Billing** mandatory | Served vs billed charges, overdelivery/invalid-click credits, taxes, LSA charges and monthly limit. A daily average budget is not necessarily a hard daily billed ceiling. Reconcile any discrepancy before budget increase. |
| R06 | Auto-apply, account Rules, Change History, bidding/asset policy | **Weekly Monday** quick check; **monthly** full native-UI review and after unexpected change | Ads account Admin + operator; Google Ads native UI; Change Events via Jenkins | Direct `REPORT=auto_apply` subscription type/status readback (when validated) PLUS native UI Auto-apply History, activated Rules/scripts, recommendation acceptance actor, Manual CPC status, image/asset/healthcare claims and disapprovals. Record screenshot/export of current settings; recommendations alone do not prove auto-apply. |
| R07 | Website price, booking path and production health | **Weekly**, and **on every deploy/incident** | Engineering + owner/staging/production acceptance | Owner-confirmed urgent starting price $250 across public pages, booking/API consistency, Call/Book links, mobile response, emergency-scope statements, status endpoint, smoke tests. Record production SHA and staging/production acceptance. |
| R08 | GBP, local SEO and reputation | **Weekly**, with monthly trends | Growth/local SEO operator; Google Business Profile and native Search/Maps data | Correct hours/prices/address/phone, reviews needing compliant responses, unusual suspension/visibility drops, prohibited unverified medical claims. Never reveal patient details in public replies. |
| R09 | Search Console, organic search and technical index health | **Every 2 weeks**, and after a major site release | SEO/engineering; GSC direct first-party data | Query/page trends, clicks/impressions/CTR, indexation, structured data, canonical/redirect errors, competition with paid terms; use historical baseline and note lag. |
| R10 | GA4 / Matomo / first-party attribution and privacy | **Weekly instrumentation QA**, **monthly** channel funnel / source taxonomy | Measurement/engineering; Matomo issue #142 until deployed; clinic data source | No PII/PHI leakage, critical allowed event reception, source first/last touch, Google paid vs organic/GBP, unknown `web`/`other`/`production-verification`; dedupe and conversion truth. Mark Matomo not yet deployed until verified. |
| R11 | Product / marketing economics and experiment review | **Monthly** and after 2–4 weeks of statistically interpretable pilot data | Owner + analyst | Confirm visit price/service scope, cost per qualified lead/confirmed completed visit, realistic profit and capacity, stop/scale decisions. Don't equate forecast optimization score with realized ROI. |
| R12 | CI, branch integrity, deployments and durable documentation | **After every material change / release**, plus **weekly Friday** backlog review | Engineering/operator; GitHub + Jenkins + OpenProject | Exact-head PR CI, `feature→dev→main`, staging QA, main smoke, main ancestry, open PRs/incidents; update `PROJECT_HANDOFF.md` **during every material work session**, `ROADMAP.md` if priority changes, `docs/DECISIONS.md` for approved choices, runbook for new processes; issue work-package provenance and next due. |

## Current approved bounds and action policy (as of 2026-11-23)

- Google Ads customer `652-510-3588` (USD, `America/Los_Angeles`), Urgent Search `24414014329` at **$10/day**, Traveler Search `24404901753` at **$5/day**. Separate system Local Services `23637947414` billing is not proved by its campaign budget query. Legacy Smart PAUSED; Near Me ad group PAUSED.
- Ads schedules for **all three enabled campaigns** read back exactly 15 enabled criteria: Mon–Fri 08:30–16:30; `SCHEDULE_COMPLIANCE=PASS` from operator-supplied Jenkins console on Nov 23.
- Most recent owner-supplied direct recommendations: **26 undismissed** (20 KEYWORD, 1 CAMPAIGN_BUDGET, 1 MAXIMIZE_CONVERSIONS_OPT_IN, 1 PERFORMANCE_MAX_OPT_IN, 1 RESPONSIVE_SEARCH_AD, 1 SITELINK_ASSET, 1 DYNAMIC_IMAGE_EXTENSION_OPT_IN). Budget suggestion **$110/day** is **not approved**; review at every R02 cycle. No action applied/dismissed as part of the read.
- Do not automatically enact weekly decisions or new spending. Direct Google Ads reporting code is in **draft PR #144** until release gates close. Opening an automated Jenkins cron/notification is a *separate implementation step requiring configured credentials, timezone, recipients and a verified owner*.


## Current cycle ledger — 2026-11-23 (evidence vs outstanding)

This is the operating status at the stated snapshot, not proof that a scheduler is active. Dates refer to the clinic's Pacific day unless noted; Jenkins console display time may be in the operator's own locale.

| Control | Last proven check | Next due / follow-up | Current exception |
|---|---|---|---|
| R01 Budget and schedules | 2026-11-22 budget readback; 2026-11-23 15-rule schedule `PASS` | Each following clinic weekday before 08:30 LA | Future drift monitoring not automatically scheduled |
| R02 Google Ads Recommendations | 2026-11-23 `ROWS=26`, 26 undismissed; dated review saved | **Mon 2026-11-30 LA** | 20 KEYWORD proposals lack detail; on-demand detail report awaiting live test |
| R03 Spend/search terms | 2026-11-22 read for Nov 16–20: $216.17 Urgent served, 58 clicks, 6 platform conversions | Mon 2026-11-30 LA | No post-change week yet; paid terms incomplete vs campaign ledger |
| R04 Clinic patient outcomes | Clinic owner reported 2 visits and ~2–3 calls/day for prior week, source unverified | Fri 2026-11-27 LA | Booking/source/actual paid attribution not yet reconciled |
| R05 Billing | **NOT verified** against official billed-cost ledger | Initial native Billing review required; monthly after invoice | Google Ads served cost is not billed cost; Local Services separate |
| R06 Auto-apply and account rules | 2026-11-23 direct `auto_apply`: 0 returned subscriptions/0 ENABLED, Jenkins SUCCESS, 8 runner tests PASS | Mondays + monthly native Rules/scripts review | No Auto-apply subscription returned, but Rules/scripts and history still require native verification |
| R07 Site release and booking | PR #143 $250 frontend edit tested at PR head, but integrated staging acceptance not documented | Before dev→main PR #145 merge, then weekly/after deploy | No production price release or smoke claim |
| R08 GBP/reviews | No fresh same-cycle readback | Next business-week review | Do not fabricate rating/review facts |
| R09 GSC organic | No fresh same-cycle readback | By 2026-12-07 LA | No current data snapshot |
| R10 Matomo/GA4 first-party | Matomo full implementation remains Issue #142 | Weekly measurement QA / implementation gate | Installation and dashboard not verified |
| R11 Economics | Owner price $250; clinic visit counts unlinked to Ads | Next monthly economic checkpoint | CAC per confirmed paid patient unknown |
| R12 CI and documentation | Canonical Handoff/Roadmap/Decisions updated Nov 23; PR #144/#145 drafted | Every Git write/CI status change and Fridays | PR #144 root CI not green; main production not released |

Always keep `next_due` after checking each line. No automatic recovery, dismissals, bid, budget or keyword writes are authorized by a recurring read-only check.

## Review cycle record template

```text
cycle_id: BG-ADS-YYYYMMDD-recommendations (or R01...R12)
checked_at: YYYY-MM-DDTHH:MM (America/Los_Angeles)
period: start..end (if applicable)
source: Google Ads v26 API / native Ads / reception / GSC / Jenkins (include run URL + SHA)
observed: exact counts and material deltas; omit patient data and secrets
assessment: ACCEPT_CANDIDATE | DEFER | REJECT_FOR_NOW | NEEDS_EVIDENCE
actions_taken: read-only / explicit owner-approved write + link (never silently change)
exceptions: billing drift / scheduling / policy / unknown outcome
next_due: YYYY-MM-DDTHH:MM (America/Los_Angeles)
owner: role, not patient identity
links: Issue/PR/doc/verified logs
```

## Current next due (planned cadence, not a scheduled system task)

- **R01:** next clinic business-day budget/schedule check (Mon 2026-11-23 LA, before 08:30; missed checks must be explicitly labeled rather than backdated). Then every weekday.
- **R02/R03/R05/R06:** weekly Monday 2026-11-23 LA, then Monday 2026-11-30 LA. This initial R02 report was received 2026-11-23; detailed KEYWORD terms remain pending.
- **R04/R12:** Friday 2026-11-27 LA, then following Fridays.
- **R09:** by Monday 2026-12-07 LA (biweekly after baseline).
- **Monthly:** after November invoice is available; do not invent its publication date.

The owner can ask for a specific cycle any time. The assistant must distinguish completed checks from scheduled work and not promise unattended execution without an actual configured and validated scheduler.

## Newly implemented read-only control surfaces (2026-11-23)

The in-review Google Ads v26 connector in PR #144 now includes `REPORT=auto_apply` (recommendation subscriptions ENABLED/PAUSED by type) and `REPORT=recommendation_keywords` (the literal text, match type and recommended CPC for each Google-suggested keyword). Google documents the subscription GAQL resource at https://developers.google.com/google-ads/api/fields/v26/recommendation_subscription and the keyword detail at https://developers.google.com/google-ads/api/fields/v26/recommendation .

These new reports are **not yet live Jenkins-validated**. Only after they pass do we use the subscription report as the R06 weekly evidence and keyword-detail report as R02 deep-review evidence. The subscription resource does not expose all separately configured account/manager Rules and scripts; a native UI/manual control remains necessary. No auto-apply subscription, keyword, campaign or budget change was made by coding these report options.

A standalone credential-free Python runner test stage has been added to the SCM Jenkins Job to isolate script tests from the root API Docker's limited `api/` mount, but it too requires Jenkins acceptance. A passing one-time code test does not replace recurring future Ads checks.

## 2026-11-23 R02 deep-review closure (cycle only)

Direct Google Ads `recommendation_keywords` retrieved the full 20 proposed Exact-match keyword texts/bids and Jenkins SUCCESS; each suggestion reviewed in `docs/GOOGLE_ADS_KEYWORD_RECOMMENDATIONS_REVIEW_2026-11-23.md`. Six conditional shortlist, nine hold, five do not add, with zero mutations. This **closes the individual-keyword evidence gap for the Nov 23 review only**; eligibility, duplicated existing exact/phrase coverage and verified patient ROI are not yet established. The recurring R02 task remains ACTIVE, with next regular date Monday Nov 30 LA. Doctor reporting draft lives at `docs/DR_FARAH_BUSINESS_UPDATE_2026-11-23.md`. CI PR #144/17 success is separate from ongoing staging/production release gates.
