# Dr. Farah Website Design Prototype — Version 1

> **Integration note:** This design was created by the design owner and
> supplied as `project-sources/drfarah_design_prototype_v1.zip`. Claude Code
> integrated the approved prototype into the repository without redesign,
> restyle, or reinterpretation. Design ownership remains external to Claude
> Code. See `docs/architecture/README.md` for architecture context.

## Design direction

**Quiet luxury with clinical authority**

The visual system is intentionally different from both a generic urgent-care
website and a cosmetic medspa. It combines:

- deep medical navy for authority;
- warm ivory for calm and approachability;
- restrained champagne/gold for premium positioning;
- muted rose and mineral tones for rejuvenation;
- editorial serif typography balanced by a highly legible UI sans serif;
- large whitespace, controlled hierarchy, and minimal navigation.

## Conversion strategy

The homepage is designed as the principal conversion surface.

Primary actions remain visible through:

- desktop header;
- first viewport;
- care-path cards;
- service cards;
- rejuvenation section;
- location section;
- mobile sticky action bar.

The booking experience is a four-step modal/drawer and can later share the same
state model with a direct `/book` route:

1. Choose care
2. Choose location/time
3. Enter minimum contact information
4. Review and submit

## Information architecture

Phase 1 should remain lean:

- Home
- Services
- About Dr. Farah
- Contact
- Book
- Legal/privacy/accessibility pages

Additional service landing pages should be created only for real SEO or campaign
needs, not to reproduce the page count of the current site.

## Important placeholders

The following must be replaced with verified clinic information:

- telephone;
- email;
- exact address;
- hours;
- credentials wording;
- treatment/service list;
- real portrait and clinic photography;
- legal and privacy text;
- appointment availability;
- production booking API calls.

## Technical intent

This prototype is intentionally static and backend-independent. The UI can be
transferred into the selected frontend implementation and connected to the
FastAPI booking API later.

The prototype currently uses:

- semantic HTML;
- responsive CSS;
- no framework;
- original CSS/SVG graphic elements;
- no patient data storage;
- no network/API submission.

## Next design iteration

Before production implementation:

1. replace the portrait placeholder with a real approved portrait;
2. confirm logo direction;
3. confirm the three primary appointment categories;
4. test the booking flow with Dr. Farah;
5. finalize mobile hierarchy;
6. create service-page and direct `/book` route designs;
7. adapt the prototype into repository-ready components.
