# Google Ads — individual review of 20 suggested Exact-match keywords

**Date:** 2026-11-23 | **Source:** operator-supplied SUCCESS console at 10:05 for `REPORT=recommendation_keywords` (Google Ads API v26), 20 rows.  
**Account:** `652-510-3588` USD; campaign Urgent Search `24414014329`; ad group Walk-In / Same-Day `199388744537`.  
**Fact:** ALL 20 proposals have `matchType=EXACT` and `recommendedCpcBidMicros=4000000` (**$4 suggested bid**). That bid is NOT the observed CPC or a newly authorized budget. **No keywords were added, bids changed, or recommendations applied/dismissed** during this analysis.  
**Approval:** the keyword dispositions below are analyst recommendations, NOT a medical/clinic-operational decision or final Ads changes. See `docs/DECISIONS.md` for owner-approved decisions.

## Executive decision

**Do not bulk-apply any of the 20.** These are closely overlapping local walk-in/urgent-care phrases. Google's Exact match can serve the same-meaning or same-intent close variants; multiple near-duplicates do not imply proportionately more unique leads. Google documentation: https://support.google.com/google-ads/answer/7478529 and https://support.google.com/google-ads/answer/9342105 .

Conservative triage: **6 potential shortlist** (subject to clinic walk-in / 'open' / geography confirmation; at most 1–2 eventual bounded pilot keywords), **9 hold for evidence/clarity**, **5 do not add now** (too vague, awkward or ambiguous). No keyword has yet been approved for action. Before any pilot, fetch current live keywords/negative keywords and existing match types to detect overlapping coverage; compare Search Terms and real completed visits.

The most relevant historical real search term was `urgent care near me`, observed in existing Walk-In traffic with **$92.13 cost / 24 clicks / 2 Google Ads conversions** for Nov 16–20. Those conversions were not verified completed visits. Thus do not blanket-negative `near me` or assume every proposed near-me keyword will produce profitable patients.

## Per-keyword evaluation

| # | Google-suggested keyword (all Exact) | Proposed status | Reason / prerequisite |
|---:|---|---|---|
| 1 | `the closest urgent care to my location` | HOLD | Strong urgent intent but "closest" and user proximity vary; no evidence this will add coverage beyond existing near-me variants; verify realistic service radius. |
| 2 | `urgent health center near me` | HOLD | "health center" can imply wider primary/other care; check real query intent and services. |
| 3 | `walk in health near me` | HOLD | Ambiguous medical intent and ungrammatical; low clarity vs higher-priority options. |
| 4 | `health care walk in clinic near me` | SHORTLIST / conditional | Walk-in clinic intent, but "health care" is broad; only test if unscheduled patients are actually accepted and ad/landing clearly state terms. |
| 5 | `closest walk in urgent care near me` | SHORTLIST / conditional | Strong urgent + walk-in intent; verify local catchment and true walk-in availability. Do not claim closest location in ad copy without support. |
| 6 | `urgent walk in near me` | SHORTLIST / conditional | Short local urgent intent; may already match existing variants. Check duplicate/coverage and qualified leads first. |
| 7 | `nearest clinic open near me` | HOLD | Too broad; "open" proximity/availability expectation may misalign with weekday-only 08:30–16:30 ad hours and clinical last-admission policy. |
| 8 | `any walk in clinic near me` | HOLD | "any" broad/general; questionable incremental fit and patient quality. |
| 9 | `urgent care near me walk in clinic` | SHORTLIST / conditional | Highest direct overlap with known urgent-care intent; attractive only if genuine walk-in policy and if current keyword coverage is missing. |
| 10 | `any clinic near me` | DO NOT ADD NOW | Broad non-specific clinic intent; avoid spending a $10/day pilot budget on unrelated services. |
| 11 | `the closest urgent care near me` | HOLD | Urgent intent but near-duplicate #1/#5/#13 and established traffic; no incremental evidence. |
| 12 | `in clinic near me` | DO NOT ADD NOW | Semantically unclear; may target general clinic inquiries and doesn't mention urgent/walk-in. |
| 13 | `the urgent care near me` | HOLD | Broad high-intent category but near-equivalent to existing `urgent care near me`; review existing keywords before adding. |
| 14 | `urgent health clinic near me` | HOLD | Clinical urgency intent diluted by "health clinic"; possible mixed primary-care searches. |
| 15 | `near urgent care near me` | DO NOT ADD NOW | Awkward redundant proximity wording; likely close-variant duplication with cleaner phrases. |
| 16 | `walk ins near me` | DO NOT ADD NOW | Could refer to nonmedical walk-ins, employment or stores, not necessarily patients. |
| 17 | `urgent clinic open near me` | SHORTLIST / conditional | Urgent and open-now intent; only if ads never serve when reception cannot accept the patient and current location/last admission is clear. |
| 18 | `open walk in clinic near me` | SHORTLIST / conditional | Strong walk-in + availability intent if actual walk-in intake is confirmed; watch end-of-day expectations. |
| 19 | `walk clinic open near me` | DO NOT ADD NOW | Awkward form and redundant to #18; weak incremental evidence. |
| 20 | `clinic appointment near me` | HOLD | Booking intent exists, but too general for Walk-In ad group; perhaps only a service/booking-specific campaign after consultation and lead evidence. |

**Counts:** 6 SHORTLIST, 9 HOLD, 5 DO NOT ADD NOW = 20. The SHORTLIST category is an *internal evaluation*, not authorization to add six keywords. Preferred final bounded trial (only after acceptance and duplicate check): 1–2 from #9 and #18/#17, not all six, within existing owner-approved $10/day average Urgent Search budget and without increasing ad group CPC. Record pre/post search-term spend, answered qualified calls and completed clinic visits. Any test is a new owner-approved Ads write.

## Business and clinical questions Dr. Farah must resolve

1. **True walk-in acceptance:** Are patients admitted without advance appointment? What conditions/services are suitable? Is calling first preferred? Is same-day booking guaranteed or subject to capacity? Some currently indexed clinic pages emphasize appointments. Answer this **before** any new Walk-In keywords, RSA copy, or Sitelinks are published.
2. **Operating cutoffs and geography:** Regular hours Mon–Fri 08:30–17:30 PT; Ads are scheduled Mon–Fri **08:30–16:30** and last patient is currently noted as accepted before 17:00. Confirm these are still accurate and whether the clinic wants to attract urgent walk-ins from each nearby city, not all of Greater LA.
3. **Weekly outcome counts:** For the most recent closed week, how many calls came from Google Ads (reception source, not platform guess), answered calls, genuinely qualified inquiries, appointments booked, patients actually seen, and the number of the reported two visits reliably identified as Ads-origin?
4. **Patient economics:** Approximate collected revenue per completed Google-origin visit (or aggregated total), typical services, availability/capacity and any practical maximum acquisition cost. Do not collect patient names, phone numbers, diagnosis, or notes in marketing audit.
5. **Ad claim and price truth:** Urgent evaluation from $250 is owner-confirmed in project planning; verify actual payable price/insurance handling and ensure published landing/booking/service prices agree before launching new ad claims or creative.
6. **Attribution distinction:** Separately count Google Ads, Google Business Profile/Maps, organic Google search, direct calls and hotel/referral sources when known; unknown stays unknown.

## Related recommendation categories and current decision

| Type/count | Analyst recommendation | Decision owner |
|---|---|---|
| CAMPAIGN_BUDGET (1) | **Decline for now**: Google suggested **$110/day**, vs owner-authorized/live API-verified Urgent $10/day. Cost forecast ≠ collected revenue or verified visits. | Dr. Farah / project owner for any future budget increase |
| MAXIMIZE_CONVERSIONS_OPT_IN (1) | **Defer** pending reliable completed-visit conversion attribution; don't optimize only toward call/click proxies. | Owner + Ads analyst |
| PERFORMANCE_MAX_OPT_IN (1) | **Defer**; would broaden acquisition channels and asset/healthcare claims under weak measurement. | Dr. Farah + owner |
| KEYWORD (20) | Per-keyword triage as above; **no bulk add**. | Dr. Farah decides clinical walk-in fit; Ads analyst checks duplicate coverage and economics |
| RESPONSIVE_SEARCH_AD (1) | Possible quality improvement: review actual suggested headline/description and service/price/capacity claims before writing. | Dr. Farah clinical claim approval |
| SITELINK_ASSET (1) | **Candidate** after target-link verification: Urgent Care information, Book a Visit, contact/hours. Do not claim 24/7, guaranteed same-day or walk-in unless supported. | Dr. Farah/owner content approval |
| DYNAMIC_IMAGE_EXTENSION_OPT_IN (1) | **Hold** until approved source images, consent, clinic brand/policy check; automatic selection can be risky. | Dr. Farah |
 
## Verified Ads controls / CI release gate

- Urgent Search **$10/day**, Traveler Search **$5/day**, independent live API budget readback; all three enabled Search/Local Services campaigns had **15 enabled Mon–Fri 08:30–16:30** schedule windows; `SCHEDULE_COMPLIANCE=PASS`.
- Live `auto_apply` returned **zero subscription rows** on 2026-11-23; separately configured automated Rules/scripts remain unverified.
- SCM standalone reporting pipeline passed 8 Python regression tests; operator-supplied `recommendation_keywords` console returned **ROWS=20 / Finished: SUCCESS**.
- Root Jenkins `PR-144/17` operator console finished **SUCCESS** and GitHub status for exact PR head `5a7a1ce02a4b72ec469aa74f617e95b83d98fd74` returned **success**. The earlier CI failure is no longer current for this exact feature SHA; its historical root cause is not established from the supplied tail alone.
- **Still NOT released:** GitHub PR #144 is DRAFT, and GitHub `mergeable_state=dirty` against newer `dev` after independent canonical docs/roadmap updates. Resolve conflicts preserving new canonical dev docs and feature code, revalidate exact new SHA/CI before merging. Production `main` has not been changed by this review.

## Ongoing work, not a one-time signoff

Repeat Recommendation review each Monday (next 2026-11-30 PT) via `docs/OPERATIONS_RECURRING_CADENCE.md` / Issue #146, with immediate checks after major changes. Detailed Keyword proposals may change/expire between reviews. Record exact evidence date, allowed/declined/conditional status, clinic question, owner authorization, next due. Do NOT apply or dismiss directly from this report.
