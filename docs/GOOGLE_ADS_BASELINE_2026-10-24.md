# Google Ads Live Baseline — 2026-10-24

> Account: Dr Farah VIP Urgent Care  
> Customer ID: `652-510-3588`  
> Source: live Google Ads connector via Windsor.ai  
> Purpose: replace earlier owner-reported assumptions with direct account evidence before any material account change.

## 1. Account identity and measurement configuration

`FACT:` The connected account is enabled, denominated in USD, and uses `America/Los_Angeles` timezone.

`FACT:` The account is not a manager/MCC account.

`FACT:` Auto-tagging is enabled.

`FACT:` Google Ads reports conversion tracking as self-managed.

`FACT:` The account has a Google tag configuration for:

- Google Ads destination ID: `AW-17076731177`

The Google Ads account provides the standard `gtag.js` snippet for this destination, but repository/source inspection found that this tag is **not currently implemented in the website source** and the production build does not inject it.

`DATA GAP:` Runtime/browser validation of production remains required to exclude any out-of-repository injection.

## 2. Historical campaign evidence — prior assumption corrected

Earlier project material treated the account as having no campaign history. Live account data disproves that assumption.

`FACT:` One campaign is present in the queried two-year window:

| Campaign | Type | Current status | Impressions | Clicks | Spend | Google Ads conversions | Conversion value |
|---|---|---|---:|---:|---:|---:|---:|
| Urgent Care Medical Center | SMART | PAUSED | 258,541 | 5,590 | $4,494.8619 | 16 | $0 |

Derived diagnostic metrics from the platform totals:

- CTR: approximately 2.16%
- average CPC: approximately $0.80
- platform-reported conversion rate from clicks: approximately 0.29%
- cost per platform-reported conversion: approximately $280.93

These are **not** completed-patient CAC metrics. The quality and downstream business value of the 16 platform conversions are not yet reconciled.

### Monthly serving history

| Month | Impressions | Clicks | Spend | Platform conversions |
|---|---:|---:|---:|---:|
| 2025-06 | 40,698 | 910 | $387.8903 | 1 |
| 2025-07 | 69,922 | 1,270 | $811.0709 | 2 |
| 2025-08 | 53,253 | 1,097 | $850.7764 | 4 |
| 2025-09 | 10,403 | 344 | $508.5179 | 3 |
| 2025-10 | 7,813 | 382 | $492.6690 | 2 |
| 2025-11 | 25,824 | 609 | $398.7246 | 0 |
| 2025-12 | 17,545 | 508 | $490.2797 | 1 |
| 2026-01 | 18,856 | 198 | $395.9279 | 3 |
| 2026-02 | 14,227 | 272 | $159.0053 | 0 |

`DECISION IMPACT:` BG-20 is no longer purely a pre-launch audit. It is now a **historical forensic audit + measurement repair + controlled relaunch readiness** workstream.

## 3. Existing conversion actions

Live Google Ads currently returns the following conversion actions in the audited view:

| Conversion action | Category | Origin/type | Status | Primary | Counting | Last conversion |
|---|---|---|---|---|---|---|
| Clicks to call | CONTACT | GOOGLE_HOSTED | ENABLED | Yes | Many per click | none returned |
| Smart campaign map directions | GET_DIRECTIONS | GOOGLE_HOSTED / SMART_CAMPAIGN_MAP_DIRECTIONS | ENABLED | Yes | Many per click | none returned |
| Calls from Smart Campaign Ads | PHONE_CALL_LEAD | CALL_FROM_ADS / SMART_CAMPAIGN_TRACKED_CALLS | ENABLED | Yes | One per click | 2026-01-23 |
| drfarahvipurgentcare.com (web) purchase | PURCHASE | WEBSITE / GA4 PURCHASE | HIDDEN | No | Many per click | none returned |
| Smart campaign ad clicks to call | CONTACT | CALL_FROM_ADS | ENABLED | Yes | Many per click | none returned |
| Smart campaign map clicks to call | CONTACT | GOOGLE_HOSTED | ENABLED | Yes | Many per click | none returned |
| Local actions - Directions | GET_DIRECTIONS | GOOGLE_HOSTED | ENABLED | Yes | Many per click | none returned |

### Immediate interpretation

`FACT:` Several low-/mid-funnel local actions are marked primary.

`RISK:` If a future campaign uses conversion-based bidding without cleaning the goal architecture, Google may optimize toward directions/click-to-call/local actions rather than verified completed visits.

`FACT:` The GA4-labelled website purchase action is hidden and not primary. The current repository has no implemented GA4/Google tag instrumentation, so its historical origin/configuration requires investigation.

`FACT:` `Calls from Smart Campaign Ads` shows a last conversion on 2026-01-23, consistent with the now-confirmed historical Smart campaign activity.

## 4. Measurement direction

The intended business outcome hierarchy is:

`Traffic → booking_request_created → confirmed appointment → visit_completed → revenue/contribution`

For acquisition optimization:

- diagnostic website interactions may be measured but should not all become primary Ads conversions;
- `booking_request_created` is a useful secondary/lead signal;
- `visit_completed` is the intended primary business-outcome signal once the attribution pipeline is technically validated;
- clinical details must not be sent to advertising systems.

The existing appointment model already supports a `completed` status, making `visit_completed` technically feasible without inventing a separate clinical outcome model.

## 5. Next Google Ads audit work

Before any campaign relaunch or material restructure:

1. inspect campaign configuration, targeting, geo settings and schedule;
2. inspect Smart campaign search/query/location evidence that is available;
3. inspect historical change history and automated rules;
4. classify every conversion action as diagnostic, lead, or business outcome;
5. reconcile historical platform conversions to bookings/completed visits if clinic data permits;
6. implement website attribution capture, including Google click identifiers where technically/policy appropriate;
7. establish `visit_completed` return-to-Google architecture;
8. validate landing-page/booking health;
9. only then design the controlled relaunch.

## 6. Current launch gate

`BLOCKED:` Do not relaunch meaningful paid traffic yet.

Hard requirements still include:

- booking/Brevo health;
- production measurement implementation and validation;
- conversion-goal cleanup;
- completed-visit attribution design;
- campaign/geo/search-intent forensic audit;
- landing-path readiness.
