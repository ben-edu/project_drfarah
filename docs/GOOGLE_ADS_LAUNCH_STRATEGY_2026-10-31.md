# Google Ads launch strategy — 2026-10-31

## Status

This document records the approved operating strategy after Dr. Farah declined to prioritize LegitScript and Behnam explicitly authorized a controlled launch of the current Google Search pilots.

Live Google Ads remains authoritative for current delivery/policy state. `ROADMAP.md` remains the single master roadmap; `PROJECT_HANDOFF.md` remains the live resume point. This document is durable strategy/evidence, not a competing roadmap.

## Approved decision

- LegitScript / Google telemedicine-prescription certification is **deferred**, not declared unnecessary. Issue #106 is closed `not_planned` with explicit reopen triggers.
- Current paid acquisition is limited to two policy-isolated Search pilots:
  1. Local Beverly Hills in-person urgent care — campaign `24414014329`.
  2. Traveler / pre-arrival Beverly Hills medical care — campaign `24404901753`.
- Paid prescription-refill, virtual-prescribing and certification-sensitive telemedicine acquisition is out of current launch scope.
- The public clinic may continue to describe legitimate virtual/prescription services. The strategy is to keep those services outside the current Google Ads destinations/assets rather than deleting legitimate services to bypass policy.
- Do not use `/services`, `/virtual-urgent-care`, prescription/refill copy, or certification-sensitive booking/refill destinations in the current paid campaigns.
- `HEALTH_IN_PERSONALIZED_ADS` limitations are accepted policy constraints. Do not use health-sensitive Customer Match, remarketing or other workarounds.

## Dr. Farah's current position

Dr. Farah's priority is measurable patient acquisition and appointments rather than paying for LegitScript now. She prefers to proceed with everything that does not require certification and revisit certification only if Google confirms it is necessary for a strategically valuable paid service.

She separately proposed a future California `Virtual Medical Consultations` Search campaign focused on consultations, common illnesses, follow-ups and lab-result reviews with transparent pricing. She explicitly acknowledged that merely removing prescription language may not guarantee exemption from Google certification requirements.

**Decision:** do not build or launch that proposed virtual campaign yet. Behnam will first meet with Dr. Farah, explain the current Google policy boundary and the strategy executed here, then provide her final service definition/decision. Only after that meeting may the virtual-paid lane be reconsidered.

## Policy boundary confirmed

Current Google policy evidence supports treating telemedicine that can facilitate prescribing as certification-sensitive even when ad copy itself avoids prescription wording. Therefore the project must not present a prescription-capable virtual service as consultation-only merely to obtain ad approval.

Known certification-sensitive assets remain historical/live evidence:
- asset `434419668405` — `Clinic Services` -> `/services`: `DISAPPROVED`, `PRESCRIPTION_DRUG_SALE`, US certificate missing; also limited by `HEALTH_IN_PERSONALIZED_ADS`.
- asset `434523647907` — `Book Traveler Care` -> `/book?service=traveler-care`: `DISAPPROVED`, `PRESCRIPTION_DRUG_SALE`.

These assets are intentionally **not launch dependencies**. They may be cleaned up later in Google Ads UI if desired; current connector actions do not expose detach/remove for an existing asset association.

## Launch configuration executed

### Local urgent-care pilot

Campaign `24414014329` — `Search | Urgent Care | Beverly Hills | Pilot | 2026-10-28`

- Status command accepted: `ENABLED`.
- Configured daily budget: **$40/day**; no increase made.
- Manual CPC.
- Five-mile Beverly Hills proximity targeting; positive location mode previously confirmed `PRESENCE`.
- Schedule: Monday–Thursday 08:30–17:30; Friday 08:30–16:30, account time zone.
- 3 ad groups enabled.
- 18 Exact/Phrase positive keywords enabled.
- 3 RSAs enabled; all three read back `APPROVED / REVIEWED`.
- Additional campaign negatives added to isolate certification-sensitive intent: `prescription`, `refill`, `telemedicine`, `telehealth`, `virtual`, `online doctor`, `pharmacy`, `medication`.
- Dedicated paid destination: `https://drfarahvipurgentcare.com/urgent-care-beverly-hills`.

Current direct child readback shows all three ad groups `ENABLED / ELIGIBLE`, all positives enabled, and all RSAs enabled/approved. Campaign-level aggregate status temporarily retained stale paused-child reasons after enable; treat this as propagation/cache lag unless a later fresh read shows a real blocker. On Saturday the campaign cannot serve because of its Mon–Fri schedule.

### Traveler / pre-arrival pilot

Campaign `24404901753` — `Search | Traveler Care | Beverly Hills | Pre-Arrival | Pilot | 2026-10-29`

- Status command accepted and read back: `ENABLED / ELIGIBLE`.
- Configured daily budget: **$20/day**; no increase made.
- Manual CPC.
- United States targeting; positive location mode previously confirmed `PRESENCE`.
- Schedule: 06:00–22:00 daily, account time zone.
- 3 ad groups enabled.
- 36 Exact/Phrase positive keywords enabled.
- 3 RSAs enabled; all three read back `APPROVED / REVIEWED`.
- Existing campaign negatives already isolate refill/prescription/virtual/telemedicine/telehealth/online-doctor/pharmacy/medication intent plus waste and local-overlap terms.
- Dedicated paid destination: `https://drfarahvipurgentcare.com/traveler-medical-care-beverly-hills`.

## Safe replacement sitelinks

Eight campaign-level replacements were created using only in-person/traveler-safe destinations. All eight subsequently read back `APPROVED` or `APPROVED_LIMITED`; none carries `PRESCRIPTION_DRUG_SALE`.

Local:
- `434950381736` — Urgent Care Details -> `/urgent-care-beverly-hills` — APPROVED_LIMITED.
- `434950412969` — Meet Dr. Farah -> `/about` — APPROVED_LIMITED.
- `435057993841` — Contact the Clinic -> `/contact` — APPROVED_LIMITED.
- `435058066408` — Pre-Op Clearance -> `/pre-op-clearance` — APPROVED.

Traveler:
- `435138299394` — Traveler Medical Care -> `/traveler-medical-care-beverly-hills` — APPROVED.
- `435138324555` — Beverly Hills Urgent Care -> `/urgent-care-beverly-hills` — APPROVED_LIMITED.
- `435058121053` — Meet Dr. Farah -> `/about` — APPROVED_LIMITED.
- `435058140682` — Contact the Clinic -> `/contact` — APPROVED_LIMITED.

`APPROVED_LIMITED` here reflects the separate health-personalization limitation and is not treated as a reason to bypass policy.

## Billing / payment state

- Google Ads customer reads `ENABLED`, non-test, non-manager.
- Campaign budget resources are enabled.
- Traveler reads `ENABLED / ELIGIBLE` after launch and exposes no billing primary-status reason.
- No current evidence indicates that Dr. Farah must take a billing action now.
- If Google Ads later displays a payments/billing alert, Dr. Farah or an authorized account owner must confirm the payment method in Google's secure billing UI. Never request card/payment credentials in chat or GitHub.

## Measurement and scale controls

- `Visit Completed` remains the intended primary business outcome but stays Secondary until first legitimate paid click -> booking -> completed visit -> live Data Manager import -> same-transaction replay/dedupe -> Google Ads reconciliation succeeds.
- Booking/call signals remain secondary/diagnostic.
- Review search terms early and control waste/overlap.
- Do not increase budgets or materially scale based on CTR alone; require completed visits, defensible economics, capacity and measurement confidence.
- No health-sensitive Customer Match/remarketing workaround.

## Open items that do not block this launch

1. Call asset: issue #110 remains open. The account has not completed the healthcare/HIPAA-safe Communication Features path; call recording stays off. Site phone CTAs remain available.
2. Legacy/disapproved assets: `434419668405` and `434523647907` remain recorded and isolated. UI cleanup can follow later.
3. Future virtual medical-consultation campaign: deferred until Dr. Farah meeting and policy/service-definition decision.
4. Website: real service imagery is accepted for now, but development is **not complete**. Mobile/tablet primary navigation/menu visibility, responsive polish, accessibility and further visual/performance work remain roadmap items.
5. Production CI: production branch promotion commit `8c1a1673fb9b557b79647044f4dc37dfe9f4234d` was created from the validated release tree; Jenkins `main/6` status must still be recorded when final.
6. Local aggregate primary-status propagation must be re-read; direct child objects are enabled/eligible and policy-approved.

## Immediate operating loop

1. Confirm final production CI status and reconcile `dev` to production ancestry.
2. Re-read Local aggregate serving status after propagation.
3. Watch spend, impressions, clicks, search terms and booking attribution during the controlled pilot.
4. Surface any billing/policy/serving blocker immediately; pause the affected campaign if material.
5. Complete the first legitimate paid completed-visit Data Manager acceptance when it occurs.
6. Review patient/appointment/economic results before any budget increase.
7. At the Dr. Farah meeting, explain why prescription-capable telemedicine remains certification-sensitive and review her proposed virtual-consultation service definition before any future paid virtual build.
