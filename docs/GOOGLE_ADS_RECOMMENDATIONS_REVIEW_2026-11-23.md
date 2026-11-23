# Google Ads Recommendations — Review of 2026-11-23 live operator output

**Account:** `652-510-3588` | Currency USD | Timezone `America/Los_Angeles`  
**Evidence:** Owner-supplied Jenkins `REPORT=recommendations` output at displayed 09:16:22–09:16:24 on 2026-11-23; `Google Ads API read-only reports SUCCESS`, `Finished: SUCCESS`.  
**Execution:** Direct Google Ads API v26 `SearchStream` report on feature PR #144, read-only. No Apply, Dismiss, bid or budget mutation.  
**Recurring review:** R02 weekly Monday in `docs/OPERATIONS_RECURRING_CADENCE.md` and tracked in [Issue #146](https://github.com/ben-edu/project_drfarah/issues/146).  
**Data limitation:** summary output reports recommendation type, account/campaign, impact and budget options, but **does not include actual 20 suggested keyword texts**, their match types, or the proposed sitelink/ad copy. Do not invent them or claim each individual keyword was substantively approved.

## Actual observed recommendations

`ROWS=26`, `undismissed=26`. All shown recommendation categories and the targeted campaign (where one was supplied):

| Recommendation | Count | Target | Assessment and next step | State |
|---|---:|---|---|---|
| CAMPAIGN_BUDGET | 1 | Urgent Search `24414014329` | **REJECT_FOR_NOW / DO NOT APPLY**. Google suggests **$110/day** vs owner-approved and API-verified **$10/day** (11×). Other hypothetical options included $36, $61 and $159/day. Projections are not verified patient/revenue outcomes. Compare billed costs and confirmed visits before reopening budget. | Read only, not dismissed |
| KEYWORD | 20 | Urgent Search, recommended ad-group context in resource names | **NEEDS_EVIDENCE**. Text/match type/bids omitted in report. Enrich read-only recommendation report first; check intent, clinic service eligibility, location, search term history, negatives, and post-visit source before any additions. No automatic broadened targeting. | Read only |
| MAXIMIZE_CONVERSIONS_OPT_IN | 1 | Urgent Search | **DEFER**. Report projects the same 44 clicks / 4.25 platform conversions and cost $171.92 in base and potential estimates, not guaranteed completed patient results. Keep approved Manual CPC until call/booking/visit outcomes and measured CPA are reconciled. | Read only |
| PERFORMANCE_MAX_OPT_IN | 1 | Account (no single campaign supplied) | **DEFER**. Would broaden spend/channel/asset governance outside present pilot and may bring healthcare-policy/measurement risks; requires separate written experiment decision and budget cap. | Read only |
| RESPONSIVE_SEARCH_AD | 1 | Urgent Search `24414014329` | **CANDIDATE_FOR_CONTENT_REVIEW ONLY**. Google model shows clicks 31→33 and served cost ~$114.91→$122.49 in projection, no verified patient revenue. Need inspect suggested text, service claims, $250 price truth, walk-in rules, and landing page before approval. | Read only |
| SITELINK_ASSET | 1 | Urgent Search | **CANDIDATE_FOR_REVIEW ONLY**. Verify proposed destination URL resolves to a relevant available clinic service/booking path; never lead to unapproved care/health-data tracking. | Read only |
| DYNAMIC_IMAGE_EXTENSION_OPT_IN | 1 | Account (no single campaign supplied) | **DEFER / CLINICAL MEDIA REVIEW**. Automatically selected landing-page images can be inappropriate or violate clinic consent/brand/policy expectations; need exact image control and owner approval. | Read only |

**High-spend warning:** Google's budget forecast lists `recommendedBudgetAmountMicros=110000000` ($110/day), `currentBudgetAmountMicros=10000000` ($10/day). Its `potentialMetrics.costMicros=533587487` and `baseMetrics.costMicros=71999999` are **estimates in Google's recommendation response, not billed costs or a guaranteed time-period ROI**. The $110 proposal conflicts with the owner's cost-containment direction. Do not take action solely to improve Google Optimization Score.

**Context from last full performance audit:** Nov 16–20 Urgent Search $216.17 served cost / 58 clicks / 15 phoneCalls / 6 platform conversions; this predates budget/hour restrictions on Nov 22. Dr. Farah separately reported 2 visits last week, source/individual campaign attribution unverified. Previous paid `urgent care near me` term appeared in Walk-In, $92.13/24 clicks/2 platform conversions. A blanket "near me" negative would be unjustified; candidate negatives for competitor, insurance or out-of-service queries require medical/service review.

## Evidence-gated next actions

1. Add a bounded read-only **keyword recommendation detail** query (e.g. `recommendation.keyword_recommendation`, verified selectable in Google Ads API v26 schema), and inspect recommended text/match/bid without calling Apply/Dismiss. Review all 20 suggested keywords individually; maintain same approved $10 budget during this analysis.
2. Extract proposal text/destination details for `RESPONSIVE_SEARCH_AD` and `SITELINK_ASSET` using selectable v26 recommendation fields if the source permits; obtain clinic content/policy signoff before creating any asset.
3. Verify current native Auto-apply **subscribed types**, History and automated rules, since recommendations existing or their suggested impacts do not prove enrollment.
4. On next Monday review: re-fetch recommendations, compare by type/resource/campaign against this 26-item baseline; report added, disappeared or changed proposals without assuming they were applied.
5. No automated broad targeting, budget or Smart Bidding changes; any proposed write needs exact current-state readback, owner authorization, rollback plan and evidence log.

## Decision and repeat status

- **Cycle:** `BG-ADS-20261123-recommendations`.
- **Completed this cycle:** obtained current 26-item count/type list, evaluated 7 proposal categories; no mutation.
- **Unresolved:** actual 20 keyword texts, proposed RSA/Sitelink specifics, Auto-apply native settings and actual patient ROI.
- **Next due:** Monday **2026-11-30**, Pacific; recheck earlier if budgets/schedules/rules change.
- **Persistent status:** R02 **RECURRING — ACTIVE**, not done after one pass.

## 2026-11-23 engineering follow-up (not live tested)

The new `REPORT=recommendation_keywords` option will query `recommendation.keyword_recommendation` and return the actual suggested text, match type, optional recommended CPC, campaign and ad-group resource for each KEYWORD recommendation. Do not treat the prior 20 resource identifiers as proof of individual keyword suitability. The new `REPORT=auto_apply` option will query `recommendation_subscription.status/type` for actual subscribed recommendation types, while still distinguishing separate Rules/scripts. Official v26 field documentation confirms these are selectable. Both features are in feature PR #144 and **Jenkins production acceptance is pending**; no Ads mutation.

## New direct auto-apply readback — 2026-11-23

Live owner-supplied Jenkins `REPORT=auto_apply` (09:41) PASSED after **8/8 Python regression tests**. API yielded `ROWS=0`, `total=0 enabled=0 paused=0`. **No auto-apply recommendation subscriptions returned** in this snapshot; does **not** prove independently configured automated Rules/scripts are absent. Do not confuse the earlier `GOOGLE_ADS_RECOMMENDATIONS` budget change with evidence of active Auto-apply subscription. Keyword-detail review remains unverified until live `REPORT=recommendation_keywords` output is available. No Google Ads changes were made by the report.
