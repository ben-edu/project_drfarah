# Google Ads auto-apply + bids + source audit — 2026-11-11

**Status: READ-ONLY audit; no Ads settings changed.** Owner's currently active Urgent and Traveler Search campaigns remain enabled. No change to spend budgets, the paused Near Me group, Tag, or first-party booking code. The connected Windsor.ai trial may return cached/late-updated reporting; native Google Ads billing and user-facing settings override connector observations.

## 1. What was verifiably checked

Account `652-510-3588` (USD / America/Los_Angeles). Google's current budget/configuration reports:
- Urgent Search `24414014329`: **ENABLED**, average daily budget **$10**, budget ID `15988400106`, budget shared **false**, 1 campaign reference; Manual CPC / Enhanced CPC off. Ad groups: Beverly Hills **ENABLED** effective ad-group Max CPC **$4.50**, Walk-In **ENABLED** **$4.00**, Near Me **PAUSED** **$4.50**.
- Traveler Search `24404901753`: **ENABLED**, average daily **$5**, separate budget ID `15989903931`, shared **false**, reference count 1; Manual CPC / ECPC off. Traveler Doctor **$3.50**, Visitor Urgent Care **$4.00**, Hotel Medical Care **$3.50** effective ad-group CPCs.
- Keyword-level CPC bids return null in the read: **they inherit ad-group bids**; no evidence of a currently higher explicit keyword-level amount from this report. Investigate actual effective bid modifiers/eligibility in native Ads UI.
- Legacy Smart `22552983079` is PAUSED; system-generated Local Services `23637947414` is ENABLED at separately reported $0.01 budget with **no sampled spend**, but its independent LSA billing must be checked.
- Campaign recommendations returned as **proposals** for Urgent: `CAMPAIGN_BUDGET`, `MAXIMIZE_CONVERSIONS_OPT_IN`, `SITELINK_ASSET`, `RESPONSIVE_SEARCH_AD`, `DYNAMIC_IMAGE_EXTENSION_OPT_IN` plus unknown items. **A recommendation's existence does not prove automatic opt-in, automatic execution or a billable change.** Recommendation objects are NOT Auto-apply subscription state.
- Connected Google Ads fields/actions do **NOT** expose the list of subscribed Auto-apply recommendation types or a direct Auto-apply toggle/automated-rule management. Change Events (Nov 1–11, with connector report row limitations) show human Google Ads web-client campaign pausing/re-enabling, and API Nov 7 budget/negative/pause changes. No observed Auto-apply execution event was demonstrated by the returned data; **this does not establish Auto-apply is disabled**. Do not fabricate setting readback.
- Nov 10 spend **revised on later connector read** from earlier reported **$3.37 / 1 click** to **$20.23 / 5 clicks** (same historical date), whereas Nov 9 remained $17.26. Thus historical API reporting is **not immutable**; use the official `Billed cost` report and adjustment/credit data to determine actual charged cost rather than alleging an overcharge merely because served cost is slightly above $20 against current $10 budget. Nov 2–6 daily rows above $20 reflected the **earlier $40/day budget** (reduced only Nov 7); data labeled with *current* budget $10 is not retroactive historical budget evidence.

## 2. Exact next operational task: Native Ads account Auto-apply readback

Account `652-510-3588`:
1. Google Ads UI → **Campaigns → Recommendations → Auto-apply settings → Manage**. Record every enabled item, its category and current checkbox state. Also **Admin → Account settings → Auto-apply** for subscribed list.
2. **Auto-apply settings → History**, check enrollment operator/date and applications in last 60–90 days. **Campaigns → Change history** (filter Automated / Google Ads system and API) to verify real actions. **Tools → Bulk actions → Rules** for enabled automated rules, triggered history, schedule, manager-level rules/scripts, budget alerts or unintended pause/enable cycles.
3. For a healthcare clinic operating Manual CPC on few leads, recommend **not delegating automatically** new keywords/dynamic search ads, aggressive targeting expansion, switch to Maximize Conversions, conversion-goal upgrades or broad ad message adjustments without evidence and prior clinic review. Keep other maintenance categories only after review of actual effect. Do not say 'turn everything off' without seeing current account's settings and History.
4. Only after exact readback: propose explicit before → after changes, affected campaigns, risk and rollback; obtain owner approval for live writes through an authorized UI/tool. Current connected Windsor actions can change budgets/bids but **cannot manage Auto-apply**; no backdoor or API workaround is appropriate.
5. Confirm genuine Google Ads ad/asset approvals, clinical claims (Urgent visit **$250** per owner, landing currently **$240**), and 'Walk-In' actual clinic practice separately; price correction of site/booking/service JSON remains a planned release and must be reviewed across all representations.

Google reference: https://support.google.com/google-ads/answer/10276359 and https://support.google.com/google-ads/answer/10279006 . Auto-apply recommendations do not automatically increase campaign budget but can change spend **allocation and type of traffic** within existing budget.

## 3. Bills and alert design

At unchanged current $10/day Urgent + $5/day Traveler, each STANDARD search campaign has its own average daily budget; for most campaigns Google may serve/spend **up to 2×** average on a day and limit normal monthly billed cost under applicable rules (often **30.4× average**, with budget-change and start/stop adjustments). Reference steady monthly amount = $304 + $152 = $456 in a continuously-running full month **at unchanged budgets**, not a guaranteed total account hard cap or current month bill. Google official https://support.google.com/google-ads/answer/10486637.

Check **Billed cost** versus served cost, overdelivery credits, invalid interaction credits, taxes, Local Services and any manager-run campaigns. Agree on clinic's actual maximum monthly cost and alert/stop criteria; if using automated rules note execution delays and do not call them real-time hard spending ceilings. Avoid auto-applying the explicit `CAMPAIGN_BUDGET` / `MAXIMIZE_CONVERSIONS_OPT_IN` recommendations without qualified completed-visit economics.

## 4. First-party source taxonomy forensic review

`frontend/app.js` `canonicalSource` prioritizes GCLID/GBRAID/WBRAID as `google_ads`; explicit `source=google_ads`, Google UTM with medium `cpc|ppc|paid|paidsearch` as paid; Google referral/UTM without paid evidence as `google_organic`; Google Business/Maps labels as `google_business`; unknown explicit sources/referrers as `other`. `frontend/booking.js` normally takes full first/last-touch attribution, but its fallback directly reads arbitrary `source` and may label `utm_source=google` as `google_organic` when full attribution object is missing. `api/app/routers/appointments.py` prefers nested last/first touch when present, otherwise accepts the top-level submitted source; reserved `ci` source has special authorized smoke handling.

| Source seen in Reserve Admin | Interpretation and evidence confidence |
|---|---|
| `google_ads` | Strong paid-origin **classification**, subject to validation of real click-ID/UTM ingestion; not a completed patient |
| `google_organic` | Intended non-paid Google search referral, but **possible misclassification** when paid tag/ID is lost |
| `google_business` | Explicit Google Business/Maps source markers; Maps and organic search should not be combined blindly |
| `web` | Legacy/generic source value accepted by API; exists in attribution tests as top-level source and overridden by structured Google Ads attribution. **Not evidence of Google paid or organic** |
| `other` | Generic bucket for unknown explicit source / non-Google referrer / unresolved UTM; review first/last touch and metadata |
| `production-verification` | **Not found as a canonical channel or marker in current repository source**. It could come from external QA/test or a manually submitted API `source`; this origin is **NOT PROVEN**. Investigate specific record audit/system logs or external client before labeling it a test or patient. Mark as unverified / exclude from attributable marketing conversion reporting pending provenance |

**Precise operational step:** read only non-sensitive appointment attribution metadata (source, first/last touch, created timestamp, campaign ID/UTM present, anonymous internal record) for a small sample of these statuses; do not access/export patient identity or reason for visit. Add tests for `web`, `other`, `production-verification`, paid click IDs lost through redirect, `utm_source=google&utm_medium=cpc`, and first/last-touch consistency. Fix only evidence-based source parser defects in normal CI/Staging→Production flow.

## 5. Full Matomo implementation is committed as a project deliverable

**Owner's `https://matomo.soria-ai.fr/` is an existing self-hosted service; it is not yet integrated or authenticated in this session.** GitHub Issue **#142** tracks the **complete** implementation: actual Matomo admin/site access and IDs, Tag Manager/JS or approved server integration, acquisition/campaign tagging (Google paid vs organic/GBP/partners), source first/last-touch taxonomy, useful page and CTA events, calls as *click* vs answered call from reception, booking stages, accepted vs completed bookings, qualified leads, aggregate funnel and real cost/visit dashboards, per-service/per-channel reports, controlled goals, cross-domain source handling and validation on staging/production, monitoring/privacy and operational runbook.

Avoid false trade-off 'full measurement vs all-purpose sensitive-data tracking': Matomo supports comprehensive event, goal, campaign and server-side reporting while allowing context-specific protections against clinical notes, names, form values, raw medical query strings and uncontrolled recordings. Assess actual legal/consent/data security before enabling tracking on health-intent flows. Do NOT automatically turn existing GA4 or Ads conversions off, or double-count a booking; keep first-party appointments as authoritative for confirmed/actual completed outcomes.

References:
- https://matomo.org/faq/general/how-to-track-google-ads-campaigns-with-matomo/
- https://matomo.org/guide/reports/event-tracking/
- https://matomo.org/guide/reports/goals-and-conversions/
- https://developer.matomo.org/api-reference/tracking-api

## 6. Execution status / outstanding dependencies

**Completed**: current budget/CPC/recommendation/Change Event account read, source code forensic, issue #142 for full Matomo, exact-owner `$250` price decision, documented audit and roadmap priorities. **Not completed**: viewing the actual subscribed Auto-apply settings/automated rules, toggling anything in Google Ads, changing ad copy or landing price, Matomo installation and production dashboard, verifying `production-verification` record origin. User's already-active campaigns were not modified.
