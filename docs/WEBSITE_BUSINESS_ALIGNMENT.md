# Website Business & Marketing Alignment — August 2026

## Scope

This iteration aligns the public website with Dr. Farah's requested changes and the current business-growth direction without redesigning the established quiet-luxury / clinical-authority visual system.

## Implemented

- Homepage business hierarchy updated from two care paths to three: urgent/private care, pre-operative clearance, and restore/rejuvenate.
- Homepage hero messaging sharpened around same-day, pre-op, traveler/hotel/mobile care.
- Absolute wait-time language removed.
- Insurance & Medicare section added using current clinic insurance language. Temporary text marks are used until approved local insurer-logo files are available.
- `No concierge membership fee` wording added. This avoids implying that every hotel/mobile visit has no service-related charge.
- Homepage location/map switched to map-left on desktop while preserving content-first order on narrow screens.
- Services page expanded with a visual hero, pre-op pricing, Personal Injury/MVA, virtual urgent care/travel refill information, and supporting services.
- Dedicated `/hotel-traveler-care`, `/pre-op-clearance`, and `/virtual-urgent-care` landing pages added.
- Traveler and pre-op pages are designed as future organic, paid-search, and referral destinations.
- Virtual refill copy is deliberately framed as a clinical evaluation rather than guaranteed prescribing.
- Public virtual-refill copy states the clinic's stricter policy not to prescribe controlled substances through this service while acknowledging that legal eligibility also depends on patient location, licensure, federal/state rules, pharmacy rules, and clinical judgment.
- Public booking remains minimum-necessary and does not accept medication images, prescription labels, or medical-document uploads.
- Booking reason categories and first-party acquisition-context support are added without collecting a clinical narrative for marketing attribution.
- Browser-generated acquisition markers are constrained to the real `appointments.source` VARCHAR(32) database boundary, and the API validation now matches that boundary.
- Primary navigation is normalized across the static pages at runtime during this incremental rollout.
- The existing general contact form no longer displays a false success message: until a real ContactRequest backend exists, it clearly states that the message was not transmitted and directs the user to phone/booking.

## Deliberately not implemented yet

### New API bookable service records

No new scheduling service rows were invented for:
- pre-operative clearance;
- Personal Injury/MVA;
- virtual refill care.

Their duration, buffers, booking mode, and availability have not yet been confirmed by the clinic. Existing API-configured appointment types remain authoritative. Specialized CTAs therefore use phone/request flows or an existing traveler-care slot with a structured reason where appropriate.

### Real photography

The current staging image files remain placeholders until approved real photography is available to the repository as file assets. Replace them before production publication and update alt text to describe the actual image truthfully.

### Insurance logo binaries

Approved insurer logo files are still required. The homepage currently uses styled textual carrier marks so the information architecture can be reviewed without hotlinking third-party assets. Replace these with approved local assets after verifying current clinic participation/acceptance status.

### Reviews

Review excerpts must be checked against the current Google Business Profile before production cutover.

## Required clinic confirmations before production

1. Verify every publicly displayed insurance carrier/network and the exact public wording.
2. Confirm that `No concierge membership fee` reflects Dr. Farah's intended meaning.
3. Confirm pre-op pricing and current target turnaround wording.
4. Confirm Personal Injury/MVA starting price and public scope.
5. Confirm virtual-care/refill clinical policy, patient-location restrictions, secure medication-verification workflow, and final legal/compliance wording.
6. Confirm service durations, buffers, booking modes, and availability before adding new services to the scheduling API.
7. Supply and approve real physician/clinic photography as repository-ready files.
8. Verify patient review excerpts and display permissions/source.

## Production boundary

Staging remains `noindex,nofollow`. Production cutover, canonical-domain replacement, redirects, sitemap/indexing, and any non-essential advertising/tracking technology remain separate controlled steps.


## September 2026 service-navigation and registration update

The current implementation now also includes:

- dedicated public pages for `/prp-treatments`, `/weight-loss-program`, `/traveler-telehealth`, `/iv-therapy`, and `/personal-injury-care`;
- the expanded primary navigation requested by the clinic;
- variable-fee wording presented as `Starting From` where the final charge can vary by treatment, testing, medication, or individual plan;
- attorney/law-firm lien language for qualifying Personal Injury and Pre-Op cases, expressly subject to a formal written agreement and case eligibility;
- an IV Therapy & Wellness page that reuses the existing approved IV visual rather than introducing another unrelated image;
- a first-phase Online Patient Registration flow with server-side persistence, Save Draft, Resume, and Submit;
- a Keycloak-protected admin registration queue and detail view for clinic staff.

The first registration phase is intentionally limited to demographic/contact information. It does not collect medical-history narratives, medication lists, insurance member identifiers, SSNs, identity documents, or medical uploads. The patient receives a registration reference and private resume token; only a hash of the resume token is stored.

AI/chat assistance remains outside this implementation.

CI rerun note: validation re-triggered after Jenkins HTTPS endpoint recovery on 2026-09-19.
