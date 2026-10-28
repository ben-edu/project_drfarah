# Google Ads Pilot — Beverly Hills Urgent Care

**Date:** 2026-10-28  
**Account:** `652-510-3588`  
**Campaign ID:** `24414014329`  
**Campaign:** `Search | Urgent Care | Beverly Hills | Pilot | 2026-10-28`  
**Current state:** PAUSED — no spend authorized or started.

## Objective

Build the first controllable paid-search experiment around high-intent Beverly Hills urgent-care demand and optimize toward the business outcome `Visit Completed`, not legacy call-only platform conversions.

## Evidence used

Historical Smart campaign `Urgent Care Medical Center` (`22552983079`) ran June 2025–February 2026 and produced approximately 258,541 impressions, 5,590 clicks, $4,494.86 spend and 16 platform conversions. Live conversion breakdown shows those conversions were effectively `Calls from Smart Campaign Ads`, not completed visits. Device performance was heavily mobile-weighted. Historical geography also showed leakage outside the intended Beverly Hills service area, including spend in Brentwood in Northern California with no conversion value.

A system-generated Local Services campaign also exists (`23637947414`). It is account-status ENABLED/ELIGIBLE but its bidding system is PAUSED and it recorded no impressions, clicks or spend in the inspected 90-day window. Do not delete it without understanding its platform role.

Search Console shows meaningful local opportunity around urgent-care queries, with several high-intent terms around positions 10–16 rather than strong page-one coverage.

Keyword Planner account data on 2026-10-28 includes:

- `urgent care beverly hills`: about 590 average monthly searches; estimated top-of-page range about $1.47–$6.37.
- `urgent care near me`: about 49,500 average monthly searches in the selected planning geography; estimated top-of-page range about $1.51–$7.06.
- `private urgent care`: about 10 average monthly searches; competition index 69; top-of-page about $3.01–$8.39.
- `private urgent care near me`: about 10; competition 79; about $1.49–$7.65.
- pre-op / medical-clearance variants are low-volume in this planning slice and should not dilute the first urgent-care pilot.

## Campaign configuration

Created paused with:

- Search channel;
- Manual CPC;
- Enhanced CPC off;
- provisional daily budget: $40/day;
- English;
- five-mile proximity around the clinic coordinates 34.067, -118.3934;
- schedule matching current GBP hours: Mon–Thu 08:30–17:30, Fri 08:30–16:30;
- weekends off.

### Ad groups

1. `Urgent Care | Beverly Hills` — ID `196894367450`, paused, default CPC $4.50.
2. `Urgent Care | Near Me` — ID `204328258769`, paused, default CPC $4.50.
3. `Walk-In | Same-Day` — ID `199388744537`, paused, default CPC $4.00.

Initial positive keywords are Exact and Phrase only. Broad Match is intentionally excluded while reliable completed-visit conversion volume is absent.

### Campaign negatives

Initial waste-control negatives include 24-hour/24-7, emergency-room/ER-specific intent, hospital-emergency intent, free clinic, employment/training terms, veterinary and dental terms. Negatives should be expanded aggressively from live search-term evidence after launch.

Do not use a broad negative that could unintentionally suppress legitimate urgent-care searches.

### Assets already linked

- call asset: 310-467-0101;
- callouts: `Physician-Led Care`, `Beverly Hills Clinic`, `Same-Day When Available`;
- sitelinks to physician/about and clinic services.

Responsive Search Ads are deliberately not created yet. The intended primary final URL is the new production landing page `/urgent-care-beverly-hills`; creating ads before that destination is live would invite avoidable destination/policy failures.

## Critical geo issue before enable

Read-back shows the campaign positive geo setting is currently Google Ads default `PRESENCE_OR_INTEREST`, despite the five-mile proximity criterion. Given historical geographic leakage, this is not acceptable for launch.

Before enabling, set the campaign Location option for Target to people **in or regularly in** the targeted locations (`PRESENCE`), not people who merely show interest in them. The currently connected write action can set the radius but does not expose this specific geo-presence switch, so it must be changed through a supported account UI/API path before spend begins.

## Landing page

Primary destination: `https://drfarahvipurgentcare.com/urgent-care-beverly-hills`.

Requirements implemented/planned:

- public, indexable Beverly Hills urgent-care page;
- actual clinic hours and phone;
- same-day wording only `when available`;
- explicit non-emergency/911 language;
- no 24/7 claim;
- book and call CTAs;
- first-party click/source attribution via existing `app.js` mechanism;
- no GA4 injection under the current health/privacy allowlist architecture;
- old `urgent-care-near-you` and `vip-urgent-care` aliases redirect to the new canonical page.

## Bidding and budget hypothesis

The $40/day budget is a provisional learning ceiling, not a scale budget. With top-of-page CPC ranges commonly around $1.5–$7 for core intent, it should produce enough search interactions to inspect query quality without exposing the account to large uncontrolled spend.

Initial Manual CPC is intentional because completed-visit conversion history is not yet available. Smart bidding should be reconsidered only after reliable conversion feedback and sufficient signal volume exist. Do not optimize toward legacy call conversions.

## Conversion hierarchy

- Primary business outcome target: `Visit Completed` after Data Manager import is fully validated.
- `Visit Completed` remains Secondary in Google Ads until the controlled end-to-end import is proven.
- Booking/call signals are diagnostic/secondary and must not be mistaken for completed visits.

## Launch blockers

Do not enable campaign until all are true:

1. `/urgent-care-beverly-hills` is live on production and smoke-tested.
2. Target location mode is `PRESENCE`, not `PRESENCE_OR_INTEREST`.
3. at least one responsive search ad per active ad group is approved/eligible.
4. first-party click attribution works through landing → booking in production.
5. booking path is healthy.
6. current Data Manager production path has passed validation sufficiently to support the controlled completed-visit test.
7. budget ceiling is still acceptable after final CPC/landing review.

## First review after launch

Review search terms early, before scaling. Decisions should prioritize:

- irrelevant-query rate;
- actual CPC versus plan;
- mobile experience;
- booking creation from paid-click sessions;
- completed visits once available;
- geographic leakage;
- clinic capacity.

Scale only on business-outcome evidence, not CTR or call counts alone.
