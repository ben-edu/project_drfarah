# PROJECT HANDOFF — Dr. Farah VIP Urgent Care

> **Live unified resume document.** A new ChatGPT context/operator must be able to continue from this file + `ROADMAP.md` without reconstructing prior chat history.

**Last updated:** 2026-10-28  
**Repository:** `ben-edu/project_drfarah`  
**Canonical branch:** `dev`  
**Production branch:** `main`  
**Canonical roadmap:** `ROADMAP.md`

---

## 1. Operating model

The project is now in **Growth Acceleration / parallel execution** mode.

Objective: operate one integrated growth system across Google Ads, Search Console, Google Business Profile, GA4, first-party attribution, the public website/landing paths, completed-visit conversion feedback, service economics, AI/ChatGPT Ads, referral/partner channels and Growth Intelligence.

Rules:

- work independent lanes in parallel;
- production is the destination for validated growth work;
- batch related development before CI/build;
- minimize build count without sacrificing correctness;
- preserve useful legacy evidence before deleting/archiving old marketing objects;
- use explicit provisional assumptions when exact clinic economics are not yet available;
- optimize toward completed visits and defensible economics, not superficial platform events;
- no unnecessary patient PII/PHI/clinical context in advertising/analytics payloads;
- update this handoff after material sessions.

---

## 2. Branch / deployment state

Production `main` remains:

`1e630b9e663b9f0ba3e3eaa1bb58c4dd714db702`

Current control-plane `dev` head after PR #99:

`039d0d29e1edb27af1b1d416d43256367c314db2`

PR #99 `Update roadmap for parallel growth acceleration` was squash-merged to `dev` on 2026-10-28.

At the last check, Jenkins status for `039d0d29...` / `dev/25` was still pending. **Do not merge the next code/docs batch to `dev` until this status is confirmed green.**

Current working branch for the next integrated batch:

`growth/google-acquisition-blueprint-20261028`

This branch is being prepared as one coherent package containing the urgent-care paid/organic landing path plus Ads/audit documentation and this handoff update.

---

## 3. Booking / first-party attribution / completed outcome

### Booking

Booking/Brevo incident is owner-confirmed resolved.

`G1-BOOKING-HEALTHY`: GREEN unless a new regression appears.

### First-party attribution

Production code already supports:

- canonical source + UTM values;
- GCLID / GBRAID / WBRAID capture;
- opaque marketing session ID;
- first-touch and useful last-touch context;
- partner/traveler markers;
- `appointment_attributions` 1:1 record;
- atomic persistence with booking;
- no page path, service, reason-for-visit, PII or clinical content in the marketing attribution record.

The public site `app.js` handles first-party attribution. `booking.js` sends the snapshot with appointment creation. The production API persists it.

### `visit_completed`

Business outcome contract:

- authoritative condition: appointment status `completed`;
- deterministic key: `visit_completed:<appointment_id>`;
- occurrence time: appointment `starts_at`;
- source selection uses non-clinical attribution;
- excludes patient name/email/phone/reason/service/registration/clinical payload.

---

## 4. Google Data Manager / completed-visit import

### Google Ads conversion action

Customer: `652-510-3588`.

Conversion action created 2026-10-28:

- name `Visit Completed`;
- goal/category `Converted leads`;
- Secondary action;
- no conversion value currently;
- source `Import from clicks`;
- count `One`;
- click-through window 30 days;
- attribution Data-driven;
- UI Conversion type ID shown: `7879009165`.

Important: the API/runtime still must establish that `7879009165` is accepted as the Data Manager `productDestinationId`. Do not treat this mapping as proven only from the UI label.

Issue #94 remains open until runtime validation + controlled import pass.

### Cloud/auth

- Data Manager API enabled in the user-owned Cloud project.
- Service account `drfarah-data-manager` exists.
- role includes `Service Usage Consumer`.
- service account is a Standard user in Google Ads customer `652-510-3588`.
- Jenkins Secret File credential ID: `drfarah-google-data-manager-sa-json`.
- Kubernetes secret `drfarah-google-data-manager-credentials` synchronized successfully to `drfarah-staging` and `drfarah` namespaces.
- **No Google Cloud billing/card is to be added.** Stop if a setup path requires enabling billing/linking a billing account.
- never request/paste/upload the JSON key in chat or commit it.

### Code on `dev`

PR #93 / `6936020375ca5a03d08a6f16cff2ab6c87cbe069`:

- privacy-safe Data Manager payload preparation;
- endpoint `https://datamanager.googleapis.com/v1/events:ingest`;
- OAuth scope `https://www.googleapis.com/auth/datamanager`;
- Google Ads customer + product destination;
- one click identifier, preference GCLID → WBRAID → GBRAID;
- transaction ID `visit_completed:<appointment_id>`;
- RFC3339/timezone-aware timestamp;
- `validateOnly=true` by default;
- no PII/PHI/clinical data.

PR #95 / `8c3776aa132d835324f18d858bc1bfbe9ee5fc1b`:

- guarded client using ADC;
- explicit `allow_recording=true` required for a non-validation request;
- errors intentionally avoid payload/response-body leakage.

PR #96 / `d84fb0ed2cdb2898ca72b1412c856c68564b46d8`:

- Kubernetes ADC credential mount + safe Jenkins sync script.

PR #97 / `c976a56836ca4160684be2b190d6aa29e7244032`:

- fail-closed readiness when configured ADC credential is unreadable;
- mounted credential made readable by non-root API user;
- Jenkins `dev/24` SUCCESS.

### Validation history

Attempt 1 failed before Google because Jenkins K8s identity lacks `pods/exec`. Do not broaden `pods/exec` RBAC merely for this validation unless no safer alternative exists.

Attempt 2 ran the exact application image and reached `google.auth.default(...)` but failed before Google because the Jenkins Secret File bind mount was unreadable by container UID 10001.

PR #97 fixed the runtime readability contract. Preferred next validation is a one-off exact-artifact execution using the known green `c976a568...` application image and a private temporary credential copy readable by the container user, while keeping `validateOnly=true`. Do not log a real click ID.

`G2-MEASUREMENT-READY` remains RED until controlled end-to-end acceptance.

---

## 5. Google Ads — live current state

Customer `652-510-3588`, USD, America/Los_Angeles. Auto-tagging is enabled.

### Legacy Smart campaign

- ID `22552983079`;
- `Urgent Care Medical Center`;
- type SMART;
- PAUSED;
- activity June 2025–February 2026;
- ~258,541 impressions;
- ~5,590 clicks;
- ~$4,494.86 spend;
- 16 platform-reported conversions.

Live forensic finding: the old conversion signal is effectively `Calls from Smart Campaign Ads`, not completed visits. Mobile dominated old activity/conversions. Geography also showed real leakage outside the intended area, including spend in Brentwood in Northern California without conversion value.

Do not relaunch this Smart campaign as the primary growth vehicle. Preserve evidence, then archive/remove obsolete objects only when safe.

### System Local Services campaign

- ID `23637947414`;
- `LocalServicesCampaign:SystemGenerated:00064c99af1b40d4`;
- account status ENABLED / primary status ELIGIBLE;
- bidding-system status PAUSED;
- no impressions/clicks/spend in the inspected recent 90-day window.

Leave unchanged until its Google-managed role is understood.

### New Search pilot — CREATED, NO SPEND

Campaign ID:

`24414014329`

Name:

`Search | Urgent Care | Beverly Hills | Pilot | 2026-10-28`

Current state:

- Search;
- PAUSED;
- Manual CPC;
- Enhanced CPC off;
- provisional budget $40/day;
- English;
- five-mile proximity around clinic lat/long 34.067 / -118.3934;
- ad schedule matches current clinic hours;
- no spend has begun.

Ad groups created, all paused:

1. `Urgent Care | Beverly Hills` — ID `196894367450`, default CPC $4.50.
2. `Urgent Care | Near Me` — ID `204328258769`, default CPC $4.50.
3. `Walk-In | Same-Day` — ID `199388744537`, default CPC $4.00.

18 initial positive keywords are Exact/Phrase only. Broad Match intentionally excluded while reliable completed-visit conversion volume is absent.

Initial campaign negatives include 24-hour/24-7, emergency-room-specific, hospital-emergency, free-clinic, job/career/training, veterinary and dental intent.

Assets linked:

- call asset `310-467-0101`;
- callouts `Physician-Led Care`, `Beverly Hills Clinic`, `Same-Day When Available`;
- sitelinks to `/about` and `/services`.

Responsive Search Ads are intentionally not created yet because the new final landing page must be live first.

### Critical geo blocker before enable

Read-back after setting the five-mile proximity shows Google Ads positive geo option is still default:

`PRESENCE_OR_INTEREST`

This is unacceptable for launch because people outside the service area can qualify by showing interest in the area, and the old campaign already demonstrated geographic leakage.

Before enable, change the campaign target-location option to **Presence: people in or regularly in the targeted locations**. The connected Windsor write action can set the radius but does not expose this positive-geo-type switch, so use a supported Google Ads UI/API path before spend.

### Keyword Planner live account evidence

Examples captured 2026-10-28:

- `urgent care beverly hills`: ~590 avg monthly, top-of-page roughly $1.47–$6.37;
- `urgent care near me`: ~49,500 avg monthly in the selected planner geography, roughly $1.51–$7.06;
- `private urgent care`: ~10, competition 69, roughly $3.01–$8.39;
- `private urgent care near me`: ~10, competition 79, roughly $1.49–$7.65;
- medical-clearance/pre-op variants in this planning slice are much lower volume.

First pilot therefore prioritizes core urgent-care/local intent. Pre-op/private/VIP can be separate hypotheses rather than diluting the first search campaign.

Detailed pilot spec: `docs/GOOGLE_ADS_PILOT_2026-10-28.md`.

---

## 6. New paid + organic landing path

Current working branch adds:

`frontend/urgent-care-beverly-hills.html`

Canonical production URL:

`https://drfarahvipurgentcare.com/urgent-care-beverly-hills`

Design intent:

- indexable public page;
- aligned to Beverly Hills urgent-care search intent;
- actual phone/address/hours;
- same-day wording only `when available`;
- urgent visit starting price from current service content;
- book + call CTAs;
- explicit 911 / not-an-emergency-department language;
- `MedicalClinic` structured data;
- no 24/7 claim;
- existing first-party attribution via `app.js`;
- no GA4 injection under current health/privacy allowlist.

Prepared routing/SEO updates:

- add page to `sitemap.xml`;
- `/urgent-care-near-you` → new canonical page;
- `/vip-urgent-care` → new canonical page.

Do not create/enable responsive ads against this URL until it is deployed and smoke-tested on production.

---

## 7. Search Console

Property:

`sc-domain:drfarahvipurgentcare.com`

Recent live 90-day read on 2026-10-28:

- ~32,325 impressions;
- 308 clicks;
- CTR ~0.95%;
- average position ~11.8.

Useful local opportunity examples:

- `urgent care near me`: meaningful impressions around position ~15;
- `urgent care beverly hills`: meaningful impressions around ~10.5;
- `beverly hills urgent care`: meaningful impressions around ~15.8;
- branded terms generally rank much stronger.

Old WordPress URLs still appear historically. Production Apache already has several 301 redirects. Verify live redirect/canonical behavior rather than recreating obsolete pages.

`/book` and `/patient-registration` remain noindex and excluded from sitemap.

---

## 8. Google Business Profile

Connected location:

`locations/6719840585856592244`

Baseline:

- Dr Farah VIP Urgent Care;
- primary category `Urgent care center`;
- captured baseline rating 5.0 / 109 reviews.

Recent 90-day live actions:

- ~120 website clicks;
- ~123 call clicks.

Live coordinates:

- 34.067, -118.3934.

Live regular hours:

- Mon–Thu 08:30–17:30;
- Fri 08:30–16:30;
- weekends closed.

Audit findings:

- `has_google_updated=true` — inspect Google update(s);
- stale special-hours entries from 2025 need review;
- service catalogue has duplicates and some overly aggressive wording; clean item-by-item, not bulk-delete;
- Ads schedule/copy must match actual hours.

---

## 9. GA4

Production property `489069776`.
Web Stream `11211773871`.
Measurement ID `G-D58FTMF05S`.

Selected-page production architecture remains intentionally limited to approved low-risk public pages. Sensitive booking/registration/service/treatment/admin surfaces are excluded under the current design.

Recent Windsor reads returned no rows. Treat live receipt/settings as still open; do not conclude the implementation is broken solely from the connector result.

Pending:

- safe Realtime/DebugView test on an allowlisted page;
- timezone/currency;
- Enhanced Measurement state;
- consent behavior;
- excluded-page verification.

The new urgent-care landing page remains outside the GA4 allowlist. Paid attribution is first-party + completed-visit feedback.

---

## 10. AI / ChatGPT Ads

This is an active growth lane.

Current policy research indicates US hospitals/urgent-care advertising is limited to a small set of approved advertisers; outside the US it is not broadly allowed. Verify current account eligibility before spend.

The connected ChatGPT Ads Manager currently returned no accessible ad accounts. Do not claim the clinic is eligible or onboarded yet.

Issue #92 remains the durable evaluation thread. Continue eligibility/onboarding investigation in parallel; any pilot must have finite budget, dedicated source attribution and explicit stop/scale rules.

---

## 11. Current blockers

### B-001 Booking/Brevo
CLOSED.

### B-002 Data Manager completed-visit path
IN_PROGRESS / HARD for meaningful paid scale.

Need:

1. `validateOnly` runtime request using current green application artifact;
2. destination/customer/productDestinationId acceptance;
3. coherent Data Manager batch promotion to `main`;
4. production smoke validation;
5. first legitimate paid click → booking → completed visit → recorded conversion;
6. dedupe/reconciliation evidence.

### B-003 New Search pilot destination
IN_PROGRESS.

Need production deploy + smoke of `/urgent-care-beverly-hills`, then create/approve RSAs.

### B-004 Google Ads geo location option
HARD for campaign enable.

Need positive geo target type = `PRESENCE`, not `PRESENCE_OR_INTEREST`.

### B-005 GA4 live receipt/settings
SOFT for most growth work; open validation.

### B-006 Exact clinic economics
SOFT.

Use explicit provisional assumptions; replace with authoritative economics later.

### B-007 ChatGPT Ads eligibility
SOFT / WAITING_EXTERNAL.

---

## 12. Exact next actions

### Repository / production

1. finish current integrated landing/audit/handoff branch;
2. re-check Jenkins `dev/25` and merge only after green;
3. run one Jenkins build for the integrated website batch;
4. if staging acceptance is clean, promote promptly to `main` and deploy production;
5. smoke-test new canonical URL, redirects, book/call CTAs and first-party attribution.

### Google Ads

1. keep campaign `24414014329` PAUSED;
2. set positive location option to Presence-only through supported UI/API;
3. after landing page is live, create at least one RSA per ad group using the production URL;
4. read back policy/eligibility/status;
5. do not enable until measurement/landing/geo blockers are green;
6. once enabled, review search terms early and add negatives aggressively.

### Data Manager

1. use the known green `c976a568...` app artifact for one-off `validateOnly` auth/destination testing rather than waiting on docs-only builds;
2. do not log real click IDs;
3. if accepted, promote the four Data Manager commits to production as one coherent batch;
4. use the first legitimate paid completed visit for the controlled real recording.

### GBP/Search/GA4

- inspect GBP Google updates and stale special hours;
- clean service duplicates/claims selectively;
- verify live Search Console redirects/canonicals after deployment;
- verify GA4 Realtime/settings on allowlisted pages.

---

## 13. Resume protocol

A future chat/operator should:

1. read this file;
2. read current parallel queue in `ROADMAP.md`;
3. check `dev`, `main` and Jenkins status;
4. check campaign `24414014329` remains PAUSED before doing anything else in Ads;
5. re-check B-002, B-003 and B-004;
6. continue production measurement + at least one independent growth lane in parallel;
7. never ask for information already recorded here unless live state changed;
8. record material live changes/evidence in GitHub and update this handoff before ending.
