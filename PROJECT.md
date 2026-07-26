# Project — Dr. Farah VIP Urgent Care

> Per-project brief for the new Dr. Farah VIP Urgent Care website, booking
> system, and future AI-ready digital foundation.
>
> Read together with `00_START_HERE.md`, `01_INFRA_BASELINE.md`,
> `02_DELIVERY_PLAYBOOK.md`, and `03_APP_BLUEPRINT.md`.
>
> No secrets belong in this file; credentials are referenced by name only.
>
> **Project status:** planning / product design / booking definition
> **Current public website used only as a business-reference source:**
> `https://drfarahvipurgentcare.com/`
>
> **Phase 1 principle:** create a completely new, premium, conversion-focused
> website and an integrated booking workflow. The existing website is not a
> design, page-structure, or content template. Its content may be consulted to
> understand the clinic, but only selected, verified facts or assets may be
> reused.

## 1. Summary

- **What it does:** A premium, physician-led website for Dr. Farah VIP Urgent Care in Beverly Hills. It presents urgent and acute care, VIP/mobile visits, and regenerative/rejuvenation consultations through a concise, visually refined experience. Booking is a core product feature, not a secondary page: visitors must be able to understand the offer and start an appointment request within seconds.
- **Slug:** `drfarah` (repository / Kubernetes namespace / image / Keycloak realm)
- **Planned repo:** `https://github.com/ben-edu/project_drfarah` (create or confirm before implementation)
- **Language(s):** English in phase 1. Structure and content components must remain localization-ready for later approved languages.
- **Needs:** frontend **yes** · API **yes** · DB **yes** · admin **yes** · email **yes**
- **Primary timezone:** `America/Los_Angeles`
- **Clinic reference:** Beverly Hills, California. Confirm the authoritative address, hours, parking, phone, fax, and email before publication.
- **Primary audiences:**
  - Beverly Hills and greater Los Angeles residents needing prompt medical attention;
  - busy professionals seeking discreet and efficient care;
  - travelers and tourists who need a physician without navigating an unfamiliar healthcare system;
  - patients considering physician-led PRP/PRF and rejuvenation consultations;
  - patients requesting a hotel, office, home, or other approved VIP/mobile visit.
- **Primary business goal:** convert qualified visitors into calls or booked appointment requests with the least possible friction while strengthening Dr. Farah’s credibility, premium positioning, and local visibility.
- **Future direction:** use the website, booking API, operational data model, and approved content as the foundation for later AI integrations. Phase 1 does not implement clinical AI.

## 2. Temporary project domains

These domains are the active temporary development and deployment targets. The
project will later migrate to the clinic’s final production domain(s) through a
separate controlled migration plan.

| Purpose | Host |
|---|---|
| Frontend prod | `drfarah.proxbenovh.cloud` |
| Frontend canonical alias | `www.drfarah.proxbenovh.cloud` → redirect to apex |
| Frontend staging | `staging.drfarah.proxbenovh.cloud` |
| API prod | `api.drfarah.proxbenovh.cloud` |
| API staging | `api.staging.drfarah.proxbenovh.cloud` |
| Admin | `admin.drfarah.proxbenovh.cloud` |

Current infrastructure status confirmed by the operator:

- OVH DNS configuration for these temporary domains: **completed**.
- HAProxy routing configuration for these temporary domains: **completed**.
- Live state remains authoritative; verify DNS resolution, TLS, Hestia vhosts,
  Traefik routes, and backend health before deployment.

The current clinic website remains independent during design and development.
No existing URL, page, text block, visual identity, or navigation structure is
assumed to be part of the new website.

## 3. Product and experience principles

### 3.1 Booking-first, not information-first

The website must help a visitor take action quickly. It must not require the
visitor to browse many pages, read long generic texts, or repeatedly search for
a booking button.

Required experience principles:

- Show a clear `Book an Appointment` action in the first viewport.
- Keep the booking action visible in the desktop header.
- Use a persistent, thumb-friendly booking/call action on mobile.
- Let service cards start the booking flow with the selected service already prefilled.
- Provide a direct, shareable `/book` route in addition to an embedded modal/drawer experience.
- Avoid sending the visitor through multiple service pages before showing availability.
- Keep the booking flow to a maximum of four understandable steps whenever possible.
- Show clear progress, preserve entered information, and allow the user to go back without restarting.
- Use plain language instead of medical or technical jargon in the booking interface.
- Treat `Call Now` as a parallel high-priority action for same-day or urgent requests.

### 3.2 Minimal navigation, strong content hierarchy

The preferred phase 1 structure uses the fewest pages that can still communicate
trust, explain the main services, support local SEO, and allow informed booking.

Recommended primary navigation:

1. `Home`
2. `Services`
3. `About Dr. Farah`
4. `Contact`
5. Persistent `Book an Appointment` CTA

Supporting routes:

- `/book` — direct booking route;
- required legal/privacy pages;
- optional focused service landing pages only when justified by conversion,
  medical clarity, paid campaigns, or local-search strategy.

A blog or large resource center is not required for the first release. It may be
added later only when there is a defined content strategy, editorial ownership,
and a clear marketing purpose.

### 3.3 One brand, two clear service journeys

The clinic combines prompt medical care with regenerative/rejuvenation services.
The new website must present both without making the practice feel fragmented.

The public experience should provide two immediately understandable paths:

- **Care Now:** urgent care, acute concerns, local patients, travelers, and VIP/mobile requests;
- **Restore & Rejuvenate:** consultation-led PRP/PRF and other approved regenerative/rejuvenation services.

Both paths share the same physician-led identity, standards of care, visual
system, and booking platform. They may use different supporting imagery and
messaging, but must not look like unrelated businesses.

### 3.4 Trust before volume

The site should communicate credibility through concise, verifiable evidence:

- Dr. Farah’s qualifications and experience;
- physician-led personalized care;
- location and practical access information;
- clearly described visit options;
- verified patient feedback when permission and source are confirmed;
- medically approved service explanations;
- transparent booking and follow-up expectations.

Avoid visual clutter, unsupported superlatives, exaggerated outcomes, generic
“cutting-edge” language, and aggressive cosmetic advertising.

## 4. Scope — phase 1

### 4.1 Public website

The public website must be designed from a clean slate. The current website is a
research input, not a page-by-page migration source.

#### Home

The homepage should function as the primary conversion page and contain only the
most useful sections, in a deliberate order:

1. **Hero:** concise physician-led value proposition, Beverly Hills context, primary booking CTA, and secondary call CTA.
2. **Choose your care path:** two or three clear cards for urgent/acute care, VIP/mobile care, and regenerative/rejuvenation consultation. Each card can start booking with a preselected category.
3. **Why Dr. Farah:** short credibility section using verified credentials and relevant experience.
4. **How booking works:** a simple three-step explanation.
5. **Featured services:** only priority services, not an exhaustive list of symptoms and procedures.
6. **VIP/mobile care:** concise explanation for professionals, travelers, hotel, office, and other approved visits.
7. **Trust signals:** verified reviews, affiliations, qualifications, or other approved proof.
8. **Location/contact:** practical information with call and booking actions.
9. **Final booking CTA:** visible and unambiguous.

The homepage must not become a long directory of every condition or treatment.

#### Services

Use one well-structured services page as the default phase 1 approach. Group
services into a small number of patient-oriented categories rather than creating
one page per symptom.

Suggested groups:

- urgent and acute care;
- VIP/mobile, hotel, office, and traveler care;
- PRP/PRF and regenerative/rejuvenation consultations;
- other active services approved by Dr. Farah.

Each service or category should provide:

- a short explanation;
- who the service is for;
- what type of appointment is offered;
- any essential preparation note;
- a direct booking action with the service preselected.

Create separate landing pages only when they serve a concrete purpose such as:

- a high-priority service with enough original content;
- a local SEO target;
- a paid advertising campaign;
- a patient journey that cannot be explained clearly on the grouped services page.

#### About Dr. Farah

- concise professional biography;
- verified education, board certification, licenses, experience, research, and memberships;
- care philosophy expressed in concrete patient terms;
- high-quality real portrait and, where available, clinic photography;
- direct booking CTA.

#### Contact

- authoritative address and map/location context;
- office hours and contact channels;
- parking/access information when confirmed;
- instructions for travelers or VIP/mobile requests;
- emergency notice;
- call and booking actions;
- general inquiry form that does not invite detailed clinical disclosures.

#### Legal and required notices

- Privacy Policy;
- Terms of Use;
- Accessibility Statement;
- Notice of Privacy Practices or link to the clinic-approved version;
- online communication and booking consent language;
- emergency disclaimer;
- cookie/tracking notice only if non-essential trackers are actually used.

### 4.2 Integrated booking workflow

Booking is included in the first design and implementation cycle. It is not
postponed to a later phase.

#### Entry points

The same booking flow must be accessible from:

- hero CTA;
- desktop header;
- mobile sticky action;
- service cards;
- service sections;
- final CTA sections;
- direct `/book` URL.

Entry context should be preserved. For example, clicking `Book PRP Consultation`
opens the same booking flow with that category already selected.

#### Recommended booking steps

Keep the flow concise and adapt the exact fields to confirmed clinic rules.

1. **Choose care**
   - urgent/acute visit;
   - VIP/mobile visit request;
   - PRP/PRF or rejuvenation consultation;
   - another approved appointment category.

2. **Choose where and when**
   - clinic or approved mobile/VIP mode;
   - next available slots or preferred time request;
   - clear indication when an appointment is immediately confirmed versus pending review.

3. **Patient/contact details**
   - first and last name;
   - phone;
   - email;
   - new/existing patient only if operationally useful;
   - a short structured reason category where needed;
   - minimum necessary consent.

4. **Review and confirmation**
   - clear appointment/request summary;
   - terms and consent acknowledgement;
   - successful submission reference;
   - confirmation email;
   - instruction on what happens next.

#### Booking rules

- Display only staff-enabled appointment types and valid slots.
- Support per-service duration and before/after buffers.
- Support working hours, breaks, holidays, blocked periods, and exceptional availability.
- Prevent overlapping appointments and perform a final transactional availability check at submission.
- Return a conflict response when a slot has just been taken and let the user select another slot without losing the rest of the form.
- Support two confirmation modes:
  - `auto_confirm` for services and times approved for direct booking;
  - `request_only` for mobile/VIP visits, procedures, same-day cases, or services requiring staff review.
- Store and display all times using `America/Los_Angeles` business rules.
- Do not collect detailed symptoms, diagnosis, medications, insurance identifiers, lab results, clinical documents, or unrestricted medical narratives in phase 1.
- Date of birth, sex at birth, insurance data, or other sensitive fields are added only when a documented operational requirement exists.
- No online payment in phase 1 unless separately approved.

### 4.3 Contact and inquiry handling

- General inquiries remain separate from appointment booking.
- Use a small set of structured inquiry categories.
- Send a confirmation to the sender and a notification to the clinic.
- Apply server-side validation, rate limiting, abuse protection, and safe error handling.
- Warn users not to submit emergencies or detailed medical information through the general contact form.

### 4.4 Admin area — Keycloak protected

Minimum roles:

- `clinic-admin` — Dr. Farah / full operational access;
- `clinic-staff` — limited booking, schedule, and inquiry management.

Require MFA before production.

The admin area must provide:

- upcoming appointments;
- pending requests;
- same-day requests;
- cancellations and rescheduling needs;
- recent general inquiries;
- email notification status;
- filters by date, service, status, and visit mode.

Staff must be able to manage:

- service and appointment categories;
- booking-facing labels and summaries;
- duration and buffers;
- auto-confirm/request-only/disabled mode;
- clinic and mobile/VIP availability;
- working hours, breaks, blocked periods, holidays, and exceptional closures;
- booking status;
- rescheduling and cancellation;
- concise internal administrative notes;
- selected public operational settings.

The system must retain an audit history for important booking and configuration
changes.

No clinical chart, lab interpretation, prescription, diagnosis, medical note, or
clinical-document management is included in phase 1.

### 4.5 Editorial reset — use of the existing website

The existing website may be reviewed to understand:

- Dr. Farah’s background;
- the clinic’s current service claims;
- current audiences and positioning;
- existing contact information;
- available photos, logos, testimonials, or articles;
- inconsistencies that must not be repeated.

It is not necessary to reproduce its:

- page structure;
- navigation;
- visual identity;
- long service lists;
- duplicate text;
- current copywriting;
- blog archive;
- forms;
- external links;
- graphic style.

Reuse only facts, claims, images, and assets that are verified, legally usable,
medically approved, and useful to the new product strategy.

A future migration to the clinic’s final domain will require its own URL and
redirect plan. That future plan does not require the new temporary-domain site
to mirror the current website.

### 4.6 Explicitly out of scope for phase 1

- AI phone receptionist;
- AI lab-result interpretation;
- upload or storage of lab reports or clinical documents;
- EHR integration;
- automated clinical messaging;
- patient portal or full medical-record management;
- insurance eligibility or claims automation;
- online payment unless separately approved;
- autonomous publication of AI-generated medical or marketing content.

These remain later workstreams. The phase 1 product must create clean extension
points without pretending that future AI requirements are already resolved.

## 5. Data model

### 5.1 Core entities

#### `ServiceCategory`

- `id`
- `name`
- `slug`
- `short_description`
- `audience_path` (`care_now`, `restore_rejuvenate`, or another approved value)
- `display_order`
- `is_active`

#### `Service`

- `id`
- `category_id`
- `name`
- `slug`
- `public_summary`
- `duration_minutes`
- `buffer_before_minutes`
- `buffer_after_minutes`
- `booking_mode` (`auto_confirm`, `request_only`, `disabled`)
- `visit_modes` (clinic/mobile as approved)
- `price_display` (optional text)
- `is_featured`
- `is_active`
- `display_order`

The API manages concise booking-facing service data. Long-form medical and
marketing content remains source-controlled in phase 1 unless a later content
management requirement is approved.

#### `WorkingHours`

- `id`
- `weekday`
- `start_time`
- `end_time`
- `visit_mode`
- `is_active`

#### `BlockedPeriod`

- `id`
- `starts_at`
- `ends_at`
- `reason_internal`
- `applies_to_service_id` (optional)
- `applies_to_visit_mode` (optional)

#### `Booking`

- `id`
- `public_reference`
- `service_id`
- `visit_mode`
- `patient_status` (`new`, `existing`, optional if retained)
- `starts_at`
- `ends_at`
- `status` (`pending`, `confirmed`, `rescheduled`, `cancelled`, `completed`, `no_show`)
- `first_name`
- `last_name`
- `email`
- `phone`
- `reason_category` (optional and structured)
- `mobile_location_summary` (optional; minimum necessary for a mobile request)
- `patient_note` (disabled by default; if enabled, length-limited and clearly discouraged for sensitive medical details)
- `consent_version`
- `consent_recorded_at`
- `created_at`
- `updated_at`
- `source` (`website`, `admin`, later another approved channel)

Scheduling information is sensitive. Access, exports, logs, backups, and
retention must be controlled even though phase 1 excludes clinical records.

#### `ContactRequest`

- `id`
- `category`
- `name`
- `email`
- `phone` (optional)
- `message`
- `status`
- `created_at`
- `handled_at`

#### `Notification`

- `id`
- `booking_id` or `contact_request_id`
- `channel` (`email`; other channels reserved for later approved providers)
- `template_key`
- `recipient`
- `delivery_status`
- `provider_message_id`
- `sent_at`
- `error_summary`

#### `SiteSetting`

- `key`
- `value`
- `updated_at`
- `updated_by`

Only approved operational values belong here. Secrets remain in Kubernetes or
Jenkins-managed secret stores.

#### `AuditEvent`

- `id`
- `actor_subject`
- `action`
- `entity_type`
- `entity_id`
- `timestamp`
- `metadata` (minimal and non-secret)

### 5.2 Main business rules

- Slots are calculated from working hours, service duration, buffers, blocked periods, existing bookings, visit mode, and booking mode.
- Slot calculation and conflict validation occur server-side.
- Booking creation performs a final transactional availability check.
- Auto-confirmation is allowed only for explicitly enabled services and rules.
- Mobile/hotel/office requests default to `pending` unless Dr. Farah later approves reliable automatic rules.
- Booking changes retain an audit trail.
- Staff permissions follow least privilege.
- Public responses never expose internal notes, database identifiers, another patient’s information, or infrastructure details.
- Validation, rate limiting, safe error handling, and appropriate browser security controls are mandatory.
- Logs must avoid or redact patient contact details and free-text content unless a specific protected logging requirement is approved.
- Retention and deletion rules must be approved before production.
- Seeds and deployments must never overwrite values modified by clinic staff.

### 5.3 Reserved future extension points

Keep the application modular enough to later add, only after separate study and
approval:

- `AIInteraction` for approved phone or website assistant exchanges;
- `ReviewTask` for mandatory human/physician approval;
- `KnowledgeDocument` for approved clinic knowledge retrieval;
- a separately secured clinical boundary for future `ClinicalDocument` and `LabInterpretationDraft` data;
- adapters for approved calendar, EHR, phone, SMS, and AI providers;
- channel-neutral notification and conversation orchestration.

Do not create clinical tables or collect clinical data “for later.”

## 6. Stack choices

| Layer | Tech | Host |
|---|---|---|
| Public frontend | Static-first, component-based, minimal multi-page site | Hestia / BM1 |
| Frontend implementation baseline | Astro static output or an equivalent maintainable static-first approach; confirm before coding | Build in Jenkins, serve from Hestia / BM1 |
| Booking experience | Embedded modal/drawer plus direct `/book` route using the same API and state model | Frontend / Hestia |
| Public/admin API | FastAPI, versioned routes under `/api/v1` | K3s / BM2 |
| DB | PostgreSQL, dedicated database and credentials for `drfarah` | cluster / BM2 |
| Admin frontend | Static SPA on the separate admin domain | Hestia / BM1 |
| Admin auth | Keycloak realm `drfarah`, client `drfarah-admin`, Authorization Code + PKCE S256 | Keycloak / BM2 |
| Email | SORIA SMTP for testing; clinic-approved sender for production | shared/external service |
| Container registry | `harbor.proxbenovh.cloud/devops-project-harbor/drfarah-api` | Harbor / BM1 |
| Ingress | Traefik and ClusterIP service only | K3s / BM2 |
| Observability | Structured logs, health/readiness endpoints, and integration with the existing monitoring platform where available | BM2 |
| Backup | Automated PostgreSQL backup outside the pod/node, plus a documented restore test before production | to confirm |

The current infrastructure is the selected baseline for the website, booking API,
database, and administration layer. This does not predetermine the hosting or
vendor choice for every future AI capability.

## 7. CI/CD

- **GitHub repo:** planned `https://github.com/ben-edu/project_drfarah`
- **Branch model:** `feature/*` → `dev` (staging) → `main` (temporary production environment)
- **Deployment:** Jenkins only; no manual frontend copy or manual cluster deployment.
- **Frontend build:** use a pinned Node container if the selected static framework requires a build; deploy only generated static output.
- **API tests:** run in a pinned Python container because the Jenkins agent does not provide `python3-venv`.
- **API image:** `harbor.proxbenovh.cloud/devops-project-harbor/drfarah-api:<immutable-tag>` plus controlled `dev` and `prod` aliases.
- **Kubeconfig:** use the existing Jenkins agent kubeconfig documented in the infrastructure baseline.
- **Frontend/admin deploy credential:** `hestia-benweb-ssh`.
- **Harbor credential:** `harbor-robot-devops-project-harbor`.
- **Per-project credentials to create or confirm:**
  - `drfarah-postgres`;
  - `drfarah-smtp`;
  - `drfarah-backup` only if required by the chosen backup target.
- **Secrets:** create runtime secrets from protected values; commit only `*.example` files.
- **CORS origins:** include temporary prod, temporary staging, and admin origins exactly as configured.
- **Quality gates before temporary production deployment:**
  - API tests;
  - frontend build;
  - link checks;
  - accessibility smoke checks;
  - responsive/mobile acceptance;
  - complete booking end-to-end test;
  - double-booking conflict test;
  - admin authentication and role test;
  - email-delivery test;
  - backup and restore evidence;
  - smoke tests for all temporary domains.
- **Future final-domain migration:** prepare separately after temporary production is accepted. It must include final DNS/HAProxy/TLS, canonical URLs, analytics/SEO decisions, redirects where useful, smoke tests, and rollback readiness.

## 8. Design and content direction

### 8.1 Brand position

The new visual identity must represent a physician-led Beverly Hills clinic that
combines medical credibility, personalized access, discretion, and high-quality
rejuvenation care.

It must not resemble:

- a generic hospital template;
- a crowded discount urgent-care website;
- an aggressive cosmetic medspa;
- a wellness blog with weak medical authority;
- the current site’s visual structure.

The intended impression is **quiet luxury with clinical authority**.

### 8.2 Visual direction

- generous whitespace and disciplined composition;
- refined, high-resolution real photography;
- elegant editorial typography for selected headings;
- highly readable modern sans-serif for navigation, forms, and body text;
- restrained surfaces and transitions rather than decorative effects;
- visual distinction between `Care Now` and `Restore & Rejuvenate` without splitting the brand;
- strong contrast and accessible interactive states;
- mobile-first booking and call actions.

Suggested palette direction, to be validated visually:

- warm ivory or soft mineral backgrounds;
- deep ink, navy, or charcoal for authority;
- muted warm taupe or stone neutrals;
- restrained champagne, soft rose, or desaturated gold accents for premium/rejuvenation cues;
- no excessive pink, bright medical blue, neon color, or metallic effect.

### 8.3 Photography and assets

Preferred real assets:

- professional portraits of Dr. Farah;
- clinic exterior and interior;
- consultation setting;
- tasteful, medically appropriate treatment imagery;
- Beverly Hills/location context where useful.

Do not use stock images that imply staff, facilities, outcomes, equipment, or
services that are not real. Existing site assets may be reused only after
checking ownership, quality, and relevance.

The logo may be retained, refined, or redesigned after source files and brand
fit are reviewed. Do not force the current logo or visual identity into the new
design if it weakens the result.

### 8.4 Content principles

- Write new copy for the new product strategy rather than rewriting every current paragraph.
- Put patient questions and decisions before exhaustive service descriptions.
- Explain “VIP urgent care” in practical terms.
- Use short, specific, evidence-oriented sections.
- Keep the homepage focused on action and trust.
- Use medically reviewed language for services and treatment expectations.
- Do not publish guarantees, cures, superiority claims, regulatory claims, or outcome promises without explicit approval.
- Show medical reviewer and review date on detailed medical content where appropriate.
- Use testimonials or review excerpts only when their source and permission/display requirements are confirmed.
- Do not create content merely to increase page count.

### 8.5 Marketing and conversion requirements

The design must support both organic and paid acquisition without becoming an
advertising-heavy site.

Required foundations:

- clear Beverly Hills/local intent in headings and metadata where natural;
- strong service-to-booking links;
- fast mobile performance;
- accurate physician and medical-clinic structured data;
- event hooks for future privacy-approved conversion measurement;
- campaign-ready focused landing-page capability;
- verified social proof and trust signals;
- clear distinction between direct booking and request-for-confirmation;
- no unnecessary third-party scripts or trackers by default.

## 9. Items to resolve progressively during design

These items should be answered through the design and booking-model process,
using Dr. Farah’s validation where necessary. They are not reasons to stop the
project before wireframing.

### Business and booking

- authoritative list of active appointment categories;
- which services are shown publicly and which are bookable;
- services eligible for direct confirmation;
- services requiring manual review;
- appointment duration and buffers;
- working hours and exceptional availability;
- same-day rules and minimum lead time;
- VIP/mobile geography and travel rules;
- cancellation, rescheduling, late-arrival, and no-show rules;
- whether pricing or insurance information is shown;
- minimum patient/contact data required to create a booking;
- authoritative phone, email, address, parking, and office-hour details.

### Access and operations

- final repository URL and ownership;
- Hestia vhosts and docroots for temporary frontend, staging, and admin domains;
- live TLS status for each temporary hostname;
- K3s namespace, PostgreSQL database/secret, API resources, and Harbor pull secret;
- Keycloak realm, client, roles, MFA, and staff accounts;
- production sender and clinic notification addresses;
- backup target, retention, restore ownership, and alerts;
- data-retention, deletion, logging, and incident-response responsibilities.

### Content and compliance

- verified credentials, biography, memberships, and licenses;
- approved service descriptions and claims;
- usable photographs, logo sources, testimonials, and review sources;
- Privacy Policy, Notice of Privacy Practices, booking consent, accessibility language, and other required U.S./California content;
- approved emergency guidance;
- analytics, advertising, cookies, call tracking, and consent decisions.

## 10. Status and open items

- [x] Review the shared infrastructure documentation and reference project.
- [x] Select the phase 1 platform shape: frontend + FastAPI booking API + PostgreSQL + Keycloak admin + email.
- [x] Confirm that booking is part of the first design and implementation cycle.
- [x] Define temporary project domains.
- [x] Configure OVH DNS for the temporary domains.
- [x] Configure HAProxy routing for the temporary domains.
- [x] Confirm that the current website is a research reference, not a design/content migration template.
- [x] Establish a minimal-navigation, booking-first product direction.
- [x] Separate phase 1 scheduling from future clinical AI workflows.
- [ ] Create or confirm the GitHub repository.
- [ ] Verify live DNS resolution, TLS, Hestia vhosts/docroots, HAProxy backends, and Traefik/API routing before deployment.
- [ ] Confirm final slug/naming consistency across repository, namespace, image, DB, and Keycloak.
- [ ] Create a concise source-of-truth sheet for Dr. Farah’s verified business and medical information.
- [ ] Define the final service groups and initial bookable appointment categories.
- [ ] Create the booking state diagram and business-rule matrix.
- [ ] Produce the final lean sitemap and conversion journey.
- [ ] Produce homepage and integrated-booking wireframes.
- [ ] Produce two or three premium visual directions and select one.
- [ ] Confirm real photos, brand assets, and temporary placeholders.
- [ ] Create Hestia domains/docroots for frontend, staging, and admin if not already present.
- [ ] Create the K3s namespace, PostgreSQL database/secret, API resources, and Harbor pull secret.
- [ ] Create Keycloak realm, client, roles, MFA policy, and initial staff users.
- [ ] Configure test SMTP and booking templates.
- [ ] Implement frontend, booking flow, API, admin, tests, and Jenkins pipeline.
- [ ] Add automated external database backup and perform a documented restore test.
- [ ] Complete accessibility, security, mobile, booking, content, and temporary-domain acceptance checks.
- [ ] Deploy the accepted temporary production version to `drfarah.proxbenovh.cloud`.
- [ ] Plan final-domain migration only after the new site and booking system are accepted.
- [ ] Reopen the AI workstreams after phase 1 provides real operational evidence.

## 11. Future AI integration readiness

The new website and booking platform are the operational foundation for later AI
integration, not the AI solution itself.

Phase 1 must provide:

- stable and versioned API boundaries;
- explicit service and scheduling rules in the backend;
- a channel/source field for future approved phone or web assistants;
- auditable status changes and clear human ownership;
- reusable notification abstractions;
- separation between public content, scheduling data, internal administrative notes, and future clinical data;
- clean, approved content that can later feed a clinic knowledge base;
- no hard dependency on a single AI vendor.

Possible later workstreams:

1. AI phone receptionist and appointment assistant;
2. approved website concierge and patient navigation;
3. staff-assisted patient communication drafting;
4. AI-supported marketing and content governance;
5. physician-reviewed lab-result interpretation;
6. internal clinic knowledge retrieval.

Each later workstream requires its own validated requirements, data-flow study,
human-review rules, provider assessment, security controls, and acceptance tests.
The technical study may select existing agents or skills, healthcare-compatible
services, lightweight custom orchestration, the existing infrastructure, or a
hybrid approach. No AI hosting or vendor decision is made in this phase.
