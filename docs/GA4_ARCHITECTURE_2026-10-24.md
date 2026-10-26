# GA4 Discovery & Target Architecture — updated 2026-10-26

**Project:** Dr. Farah VIP Urgent Care  
**Roadmap item:** P2.2 Resolve GA4 access / property architecture  
**Status:** IMPLEMENTATION IN VALIDATION — property/access/stream metadata are resolved; selected-page production GA4 implementation is now proposed on `feature/ga4-public-measurement-20261026` and must pass Jenkins/staging validation before merge/deploy.

## 1. Verified current state

### Clinic GA4 property

- Property ID: `489069776`
- Property name: `drfarahvipurgentcare.com`
- Web Stream ID: `11211773871`
- Measurement ID: `G-D58FTMF05S`
- Windsor.ai access works.

The unrelated property `483894121` (`safeguardsupport.com`) is not part of this project.

### Google Ads relationship

- Google Ads account: `652-510-3588`
- Google Ads tag destination: `AW-17076731177`
- Auto-tagging: enabled
- A hidden legacy GA4-origin conversion named `drfarahvipurgentcare.com (web) purchase` exists but is not the new business-outcome model.

## 2. Measurement strategy

GA4 is a supplemental analytics layer, not the source of truth for acquisition-to-patient outcome attribution.

Primary durable path:

`source / click ID → first-party attribution → appointment → status=completed → visit_completed → controlled Ads/reporting import`

First-party attribution remains active across the marketing/booking journey and preserves non-clinical UTM/click/referral identifiers. `visit_completed` remains the intended primary optimization outcome.

## 3. Current public-page Google measurement boundary

Google Analytics is not being deployed site-wide.

The production assembly injects `frontend/analytics.js` only into this explicit allowlist:

- `/about`
- `/contact`
- `/privacy`
- `/terms`
- `/accessibility`
- `/notice-of-privacy-practices`

The wrapper itself independently verifies the production hostname and the same path allowlist before loading Google code.

Explicitly excluded from Google measurement include:

- `/book`
- `/patient-registration`
- admin/authenticated workflows
- homepage
- general services page
- pre-op, IV, PRP, weight-loss, traveler/telehealth and other service/treatment/condition-oriented pages
- detailed health educational/content pages unless they are separately reviewed and added later.

This boundary is intentionally easy to expand if later evidence/legal review supports a broader set. The project is not treating every public healthcare page as categorically forbidden; it is avoiding unnecessary disclosure while preserving first-party measurement everywhere.

## 4. Consent and Google tag behavior

Selected public pages use Google Consent Mode with these defaults:

- `analytics_storage`: denied until explicit acceptance;
- `ad_storage`: denied;
- `ad_user_data`: denied;
- `ad_personalization`: denied;
- functionality/security storage: granted.

The Google tag is allowed to load on the selected low-risk pages under consent-denied state so Consent Mode can provide limited cookieless aggregate/modeling signals. Analytics cookies are enabled only after the user accepts the updated measurement notice.

A prior site preference that existed before Google Analytics disclosure is not treated as Analytics consent. The wrapper uses a separate `drfarah_google_measurement_choice_v1` key and forces a fresh choice on an allowlisted page.

## 5. Data minimization in GA4

The implementation suppresses automatic page-view collection and sends a controlled manual `page_view` only.

Controls:

- no query string or fragment in page location;
- no document title; a controlled page-class label is sent instead;
- no detailed referrer value;
- Google signals disabled in the wrapper;
- ad-personalization signals disabled;
- Enhanced Measurement should remain off unless a specific feature is separately approved;
- no form values, booking values, registration values, service selections, reason-for-visit, symptoms, diagnoses, medications, treatment details, names, email addresses or phone numbers are intentionally sent to GA4.

## 6. Production / staging separation

`analytics.js` exists in source but is not referenced by staging HTML.

`scripts/prepare-production-frontend.sh` injects the measurement wrapper only into the approved production HTML files. The production assembly fails if measurement appears on known excluded healthcare/booking pages.

The runtime wrapper also refuses to load Google code unless the hostname is `drfarahvipurgentcare.com` or `www.drfarahvipurgentcare.com`.

## 7. Privacy disclosure

`frontend/privacy.html` is updated in the same implementation branch to describe:

- first-party attribution;
- the selected-page GA4 implementation;
- Consent Mode / analytics storage choice;
- limited cookieless measurement when analytics storage is denied;
- exclusion of booking, registration and treatment/service-intent pages;
- separation of patient/clinical data from advertising/analytics use.

## 8. Business-outcome model

### Secondary signal

`booking_request_created` remains a first-party lead event and is not automatically sent to Google.

### Primary outcome

`visit_completed` is derived from `Appointment.status == completed` and has a deterministic deduplication key. It joins only non-clinical attribution metadata.

PR #86 implementing the privacy-safe `visit_completed` read model was Jenkins-validated by the owner and merged on 2026-10-26.

## 9. Offline Ads import

Windsor.ai's connected Google Ads write-action set does not provide offline click-conversion upload. Therefore the eventual completed-visit import must use another controlled mechanism, most likely Google Ads API/Data Manager or another supported import path.

No `visit_completed` rows are sent to Google yet.

## 10. Current completion gate

Before P2.2 / G2 can be considered complete:

1. Jenkins must pass `feature/ga4-public-measurement-20261026`;
2. production/staging assembly behavior must be validated;
3. selected pages must show the expected consent behavior and no Google tag on excluded pages;
4. GA4 Realtime/DebugView must receive one controlled safe page-view after deployment;
5. timezone/currency/Enhanced Measurement live settings should be confirmed;
6. Google Ads ↔ GA4 linking/destination configuration should be reviewed;
7. first-party attribution and `visit_completed` end-to-end staging tests must pass;
8. Ads offline completed-visit import must be designed and tested before paid relaunch.
