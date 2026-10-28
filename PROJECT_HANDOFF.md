# PROJECT HANDOFF — Dr. Farah VIP Urgent Care

> **Live unified resume document.** A new ChatGPT context/operator must be able to continue from this file + `ROADMAP.md` without reading old chats.

**Last updated:** 2026-10-28  
**Repository:** `ben-edu/project_drfarah`  
**Canonical branch:** `dev`  
**Production branch:** `main`  
**Canonical roadmap:** `ROADMAP.md`

---

## 1. Control-plane rule

- GitHub is durable project memory for roadmap, handoff, decisions, code, runbooks and evidence.
- `ROADMAP.md` is the single master sequencing document.
- OpenProject remains authoritative for live work-package metadata.
- Live accounts/systems are authoritative for their current state.
- `PROJECT_HANDOFF.md` is the exact resume point and must be updated after every material session.
- Execution mode is now **Growth Acceleration / parallel execution**: do not let a blocked lane stop safe, independent high-value work.
- Batch related development before CI/build. Quality remains the gate; build count is minimized, not correctness.

---

## 2. Strategic objective now

Build and operate one integrated growth system across:

`Google Ads + Search Console + Google Business Profile + GA4 + first-party attribution + website/landing paths + completed-visit feedback + economics + AI/ChatGPT Ads + partner/content channels`.

Immediate goal is not merely “finish measurement.” It is to:

1. finish/promote the current measurement stack to production;
2. extract value from the old Ads account before cleanup;
3. design the best controllable new Google Search campaign now;
4. optimize Search Console/SEO, GBP/Maps/reputation and GA4 in parallel;
5. build a defensible pilot budget from live market/account data plus provisional economics;
6. launch a small measured paid experiment;
7. prove one real click → booking → completed visit → Google Ads conversion;
8. make that conversion path operationally stable;
9. evaluate ChatGPT/OpenAI Ads as a serious paid channel where currently eligible.

---

## 3. Verified current technical state

### Production / branches

Production `main` remains:

`1e630b9e663b9f0ba3e3eaa1bb58c4dd714db702`

Current `dev` head:

`c976a56836ca4160684be2b190d6aa29e7244032`

`dev` is ahead of `main` by the current Google Data Manager measurement/import batch. Jenkins status for `c976a56...` is **SUCCESS**, target `dev/24`.

Do not claim the Data Manager transport/auth stack is production until `main` is promoted/deployed.

### Booking

Booking/Brevo incident is owner-confirmed resolved.

- `G1-BOOKING-HEALTHY`: GREEN unless a new regression appears.

### First-party attribution

Implemented and merged previously:

- canonical source/UTM values;
- GCLID/GBRAID/WBRAID capture;
- opaque marketing session ID;
- first/last-touch context;
- partner/traveler markers;
- `appointment_attributions` 1:1 record;
- booking persists attribution atomically;
- no unnecessary clinical data in the attribution object.

Production frontend/booking code already accepts click identifiers and passes the attribution snapshot to appointment creation. Production API stores the structured attribution record.

### `visit_completed`

Business outcome contract exists:

- authoritative condition: appointment status `completed`;
- deterministic key: `visit_completed:<appointment_id>`;
- occurrence time: appointment `starts_at`;
- joins non-clinical click/source attribution only;
- excludes name/email/phone/reason/service/clinical/registration payload from marketing outcome.

### Google Data Manager implementation on `dev`

PR #93 / commit `6936020375ca5a03d08a6f16cff2ab6c87cbe069`:

- privacy-safe Google Ads offline payload preparation;
- `POST https://datamanager.googleapis.com/v1/events:ingest` intent;
- Data Manager OAuth scope;
- Google Ads customer + conversion action destination;
- one click ID with preference GCLID → WBRAID → GBRAID;
- transaction ID `visit_completed:<appointment_id>`;
- timezone-aware timestamp;
- default `validateOnly=true`;
- no PII/PHI/clinical payload.

PR #95 / `8c3776aa132d835324f18d858bc1bfbe9ee5fc1b`:

- guarded Google Data Manager client;
- ADC auth via `google.auth.default`;
- explicit `allow_recording=true` required for non-validate requests;
- errors intentionally avoid payload/response-body leakage.

PR #96 / `d84fb0ed2cdb2898ca72b1412c856c68564b46d8`:

- Kubernetes credential mount and safe Jenkins secret synchronization tooling.

PR #97 / `c976a56836ca4160684be2b190d6aa29e7244032`:

- fail-closed readiness on unreadable ADC credential;
- credential mount readability corrected for the non-root API user;
- Jenkins `dev/24` SUCCESS.

### Google credential/runtime setup

- Data Manager API enabled in the user-owned Google Cloud project.
- Service account `drfarah-data-manager` exists and is a Standard user in Google Ads account `652-510-3588`.
- Jenkins Secret File credential ID: `drfarah-google-data-manager-sa-json`.
- Kubernetes secret `drfarah-google-data-manager-credentials` was synchronized to `drfarah-staging` and `drfarah` namespaces successfully.
- No Google Cloud billing/card should be added. Stop if a future setup path asks to enable billing/link a billing account.
- Never request/paste/upload the JSON key in chat or commit it to Git.

### Validation attempt status

A one-off Jenkins validation using `kubectl exec` failed **before Google was contacted** because Jenkins service account `system:serviceaccount:fastapi-platform:jenkins-project` cannot create `pods/exec` in namespace `drfarah-staging`.

Do not broaden Kubernetes `pods/exec` RBAC merely for this one-off validation unless no safer option exists.

Preferred next validation route: use the already-built green application artifact from Jenkins/runtime context or another exact-artifact execution method that does not widen Kubernetes permissions. Verify exact registry tag/credential/tool assumptions before asking the owner to run another job.

### Google Ads live account

Customer: `652-510-3588`.

Legacy paid evidence:

- campaign `Urgent Care Medical Center`;
- Smart campaign;
- paused;
- historical activity June 2025–February 2026;
- ~258,541 impressions;
- ~5,590 clicks;
- ~$4,494.86 spend;
- 16 platform-reported conversions.

Do not assume the 16 conversions equal completed visits.

Current strategy: extract forensic value before cleanup; do not simply relaunch the old Smart campaign. Design a new controllable Search architecture using historical Ads + Search Console + current market planning data + landing/economics evidence.

Auto-tagging is enabled. Google Ads destination/tag identity previously captured as `AW-17076731177`.

### New Google Ads conversion action

Created 2026-10-28:

- name: `Visit Completed`;
- customer: `652-510-3588`;
- category/goal: Converted leads;
- Secondary action;
- no value currently;
- source: Import from clicks;
- count: One;
- click-through window: 30 days;
- attribution: Data-driven;
- UI Conversion type ID shown: `7879009165`.

Important: validate through the API/runtime that `7879009165` is accepted as the Data Manager `productDestinationId`; do not treat that mapping as proven merely because the UI displays the ID.

Issue #94 remains open until runtime validation and controlled import are accepted.

### GA4

Production property:

- Property ID `489069776`;
- Web Stream `11211773871`;
- Measurement ID `G-D58FTMF05S`.

Selected-page production implementation exists for approved low-risk public pages. Sensitive booking/registration/treatment/admin surfaces are excluded under the current architecture.

Current live connector read on 2026-10-28 returned no 30-day GA4 rows. Treat live receipt/settings confirmation as still open; do not infer that the implementation is broken solely from the connector result.

### Search Console

Property: `sc-domain:drfarahvipurgentcare.com`.

Live 90-day read on 2026-10-28 returned approximately:

- 32,325 impressions;
- 308 clicks;
- 0.95% CTR;
- average position 11.80.

Useful current query evidence includes branded strength plus opportunities around urgent-care/Beverly Hills/near-me and selected service themes. `/book` and `/patient-registration` remain `noindex` and excluded from sitemap.

### Google Business Profile

Live connected profile is operational. Baseline captured earlier:

- Dr Farah VIP Urgent Care;
- primary category `Urgent care center`;
- 5.0 rating / 109 reviews at captured baseline.

Live 90-day performance read on 2026-10-28 returned approximately:

- 120 website clicks;
- 123 call clicks.

Do not bulk-delete the service catalogue. Optimize factual details/categories/services/links/content/reputation based on evidence and policy.

### AI / ChatGPT Ads

This is now an active growth lane, not a future side note. Before spend, re-check current healthcare advertiser eligibility/policy and account availability. If eligible, design a finite-budget pilot with dedicated source attribution and completed-visit measurement where supported.

---

## 4. Current blockers

### B-001 Booking/Brevo
CLOSED.

### B-002 End-to-end completed-visit measurement
**State:** IN_PROGRESS / HARD for material scale.

Remaining:

- safe runtime `validateOnly` call to Google Data Manager using the actual current implementation;
- verify destination/customer/conversion-action acceptance;
- promote coherent Data Manager batch to `main` after validation;
- production smoke test;
- first legitimate paid click→booking→completed visit→recorded conversion;
- dedupe/reconciliation evidence.

### B-003 GA4 live receipt/settings
**State:** IN_PROGRESS / SOFT for most parallel growth research, HARD only where a specific decision depends on GA4 behavioral data.

### B-004 Exact clinic economics
**State:** SOFT.

Do not block strategy. Use explicit provisional assumptions from market/account evidence until authoritative revenue/margin/capacity values are supplied.

### B-005 ChatGPT/OpenAI Ads eligibility
**State:** WAITING_EXTERNAL / SOFT.

Verify current eligibility/policy; continue campaign hypothesis/measurement planning in parallel.

---

## 5. Exact next actions — parallel queue

### Lane 1 — Production measurement

1. inspect exact current Jenkins/registry/deployment behavior before another validation run;
2. choose the lowest-risk exact-artifact validation route that avoids broad `pods/exec` RBAC;
3. send one `validateOnly=true` Data Manager request without logging click IDs/patient data;
4. if accepted, prepare one coherent `dev`→`main` promotion of the current Google Data Manager batch;
5. deploy through Jenkins and run production smoke validation;
6. keep real recording guarded until one legitimate eligible event exists.

### Lane 2 — Google Ads campaign rebuild

1. preserve/extract legacy Smart campaign evidence;
2. inventory old conversion goals/assets/landing destinations/settings;
3. build keyword/query opportunity set from Ads history + Search Console + current planning data;
4. create negative-keyword taxonomy;
5. design new Search campaign/ad-group/geo/schedule/bidding/ad/asset structure;
6. map each intent cluster to the correct landing path;
7. produce provisional learning-budget model and stop/scale rules;
8. build the new campaign paused/ready before spend where account tooling permits.

Do not delete useful legacy evidence until extraction is complete.

### Lane 3 — Search Console / website

1. prioritize position 4–20 high-intent local/commercial queries;
2. identify page/query mismatches;
3. map pages to paid/organic intent;
4. implement high-confidence SEO/landing corrections in batched website changes;
5. promote qualified website changes to production promptly after normal validation.

### Lane 4 — GBP / Maps / reputation

1. re-verify hours/contact/location/categories/links;
2. optimize service catalogue based on factual availability + demand + economics + clarity + policy;
3. establish review request/response workflow;
4. perform Beverly Hills local competitor baseline;
5. feed findings back into Ads/site/content.

### Lane 5 — GA4

1. verify production Realtime/DebugView safe event;
2. confirm timezone/currency/Enhanced Measurement;
3. confirm allowlist/consent/exclusion behavior;
4. close or document connector/data gap.

### Lane 6 — Economics/budget

Build provisional service priority and pilot budget without waiting for owner input. Clearly label assumptions; replace with clinic facts later.

### Lane 7 — AI Ads

Verify current ChatGPT/OpenAI Ads eligibility/policy/account path and design the first measurable pilot if eligible.

### Lane 8 — Operations automation

After the first controlled real import succeeds, implement durable import ledger/scheduler/retry/monitoring so clinic staff only need to maintain correct appointment outcome status.

---

## 6. Production rule

The owner explicitly wants growth work moved forward on the real site rather than left indefinitely on `dev`.

Operational interpretation:

- do not bypass staging/CI/Jenkins quality controls;
- do not accumulate validated growth code on `dev` without a production plan;
- batch coherent changes;
- promote to `main` promptly once the relevant acceptance evidence is green;
- production is the environment where final measurement/business behavior must be verified.

---

## 7. Resume protocol

A future chat/operator should:

1. read this file;
2. read the current parallel priority queue in `ROADMAP.md`;
3. check `dev` and `main` heads + Jenkins status;
4. re-check B-002 first;
5. continue Lane 1 and at least one independent growth lane in parallel;
6. never ask again for information already recorded here unless live state changed;
7. record material evidence/results in GitHub;
8. update this handoff before ending.
