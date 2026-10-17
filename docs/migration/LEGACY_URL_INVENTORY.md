# Legacy WordPress URL inventory — partial, updated 2026-10-17

## Sources and limits

- The previous WordPress [blog index](https://drfarahvipurgentcare.com/blog/) remains in a pre-cutover search snapshot. The original 20 article paths below came from that snapshot. Search results from October 2026 exposed 20 more article paths; search indexes can be stale and are **not** a WordPress export.
- This document now lists 46 distinct article paths (the original 20, the 20 newly found paths, and six previously noted search-visible paths), plus two archive paths and eight structural redirects. A further article title has no verified URL.
- This is **not** a complete historical crawl. The retained WordPress post list
  has not been inspected, so these search results cannot prove that every old
  article has been identified. Search Console data may help discover missed
  URLs, but is not needed to decide the content policy below.
- On 2026-10-17, direct production HTTP checks returned `301` with an immediate `https://drfarahvipurgentcare.com/...` Location for all eight redirects in `frontend/.htaccess.production`. Representative old article paths and `/blog/` returned `404`; the full article list was not individually checked.

## Content ownership decision — 2026-10-17

The site owner decided to retire the old WordPress articles. Public content is
maintained only in the Dr. Farah GitHub repository. Do not import, rewrite or
republish a WordPress-only article as part of this migration. Do not redirect
retired articles to a loosely related service page or the homepage.

The old article paths already checked on the new site return genuine `404`.
That is an appropriate permanent response for removed content with no equivalent
replacement; an explicit `410` rule is not required. The old WordPress **post
records** must still be removed from the retained WordPress installation when
administrative access is available. A `404` from the new site does not prove
that the old installation's database has been cleaned. Keep the rollback backup
and avoid deleting WordPress pages or shared media as part of a post-only purge.

## Unambiguous page mappings

| Old path | New path | Decision |
| --- | --- | --- |
| `/booking` and `/booking/` | `/book` | Live 301; new booking page is the replacement flow. |
| `/services/` | `/services` | Live 301 to the canonical extensionless URL; match only the trailing-slash path to avoid a redirect loop. |

The other six live 301s are `/about-us/` → `/about`, `/contact-us/` → `/contact`, `/prp-prf-exosomes-center/` → `/prp-treatments`, `/urgent-care-near-you/` → `/services`, `/vip-urgent-care/` → `/services`, and `/faq/` → `/services`. The check above verified their first response and direct HTTPS Location.

## Retired WordPress articles found in the old blog index

Each path below appeared on the old blog index. The 2026-10-08 fetch returned
404. These articles are retired by the content ownership decision above.

- `/what-to-expect-your-regenerative-treatment-journey-at-dr-farahs-la-clinic/`
- `/how-prp-and-prf-and-exosomes-work/`
- `/which-regenerative-treatment-is-right-for-you/`
- `/understanding-the-cost-of-prp-prf-and-exosomes-in-los-angeles/`
- `/guide-to-candidacy-in-los-angeles/`
- `/platelet-rich-fibrin-prf-therapy/`
- `/prp-injections-for-joint-pain-relief-and-orthopedic-healing-in-los-angeles/`
- `/prp-hair-restoration-in-los-angeles/`
- `/prp-for-skin-rejuvenation-in-los-angeles/`
- `/platelet-rich-plasma-prp-therapy-what-it-is-and-how-it-works/`
- `/experience-premium-urgent-care-in-los-angeles/`
- `/regenerative-medicine-in-los-angeles/`
- `/preventing-common-urgent-care-visits-tips-for-la-residents/`
- `/pediatric-urgent-care-in-los-angeles/`
- `/fast-relief-for-sprains-and-strains-urgent-care-la/`
- `/school-and-sports-physicals-at-your-local-la-urgent-care/`
- `/travel-health-and-vaccinations-your-la-urgent-care-resource/`
- `/urgent-care-costs-and-insurance-in-los-angeles/`
- `/urgent-care-for-allergies-la/`
- `/urgent-care-for-minor-burns-and-wound-care-in-los-angeles/`

## Additional article paths found in 2026 search snapshots

These 20 exact paths were visible as old-site results or as a link from an old
article. They are retired WordPress-only content, **not** approved redirect
targets. Live spot checks on `/why-physician-led-urgent-care-feels-better/`,
`/how-tirzepatide-supports-metabolic-health/`, and
`/bronchitis-treatment-without-er-visits/` returned 404 on 2026-10-17.

Urgent care, wounds and infections:

- `/why-physician-led-urgent-care-feels-better/`
- `/when-do-you-need-stitches-for-a-cut/`
- `/when-do-stitches-need-removal/`
- `/how-to-treat-bronchitis/`
- `/same-day-laceration-repair-when-to-go/`
- `/same-day-stitches-appointment/`
- `/allergic-reaction-treatment-options/`
- `/doctor-for-bladder-infection/`
- `/minor-injury-urgent-care-treatment/`
- `/bronchitis-treatment-without-er-visits/`
- `/rapid-asthma-flare-treatment/`
- `/medical-glue-vs-stitches/`

IV care and dehydration:

- `/iv-hydration-vs-oral-rehydration/`
- `/how-to-treat-dehydration/`
- `/how-nad-iv-therapy-works/`
- `/myers-cocktail-iv-review/`
- `/best-treatments-for-dehydration-recovery/`

Weight management:

- `/is-semaglutide-safe-for-obesity/`
- `/who-qualifies-for-tirzepatide-treatment/`
- `/how-tirzepatide-supports-metabolic-health/`

The archived blog index also mentions an article titled “Semaglutide vs
Tirzepatide: Which Fits Best?”, but its exact URL has not been verified and is
**not** counted among the paths above. It is covered by the same retirement
decision.

## Other previously found paths

- Articles: `/guide-to-urgent-care-visits/`, `/private-urgent-care-appointments/`, `/urgent-care-vs-emergency-room/`, `/urgent-care-for-cough-los-angeles/`, `/concierge-urgent-care-clinic/`, `/walk-in-clinic-vs-appointment-your-options-at-dr-farahs-la-urgent-care/`.
- Archives: `/blog/` (live 404 on 2026-10-17) and `/category/blog/` (not rechecked).

The archives have no current equivalent and must not be sent to the homepage by
a blanket rule. The six article paths above are retired too.

## To complete the migration

1. With authorized access to the retained WordPress installation, list its
   `post` records across all statuses and verify which are WordPress-only.
   Remove those posts there, including the Trash, and confirm the post count
   afterwards. Do not purge `page` records, shared media, or the rollback
   backup as part of this operation. The GitHub repository contains no copies
   of the 46 listed article pages.
2. Compare the WordPress post list with these 46 known paths and the unverified
   article title to catch additional old posts. A WordPress export or Search
   Console report can help with completeness, but traffic data is no longer
   needed to decide whether to keep the old articles.
3. Keep the eight verified structural 301s. On the new site, leave retired
   article and archive URLs as genuine 404s unless the owner later approves a
   specific new equivalent in the GitHub repository. Do not blanket-redirect
   unknown old URLs.
4. After WordPress deletion, verify a sample of retired article URLs, canonical
   tags, `/robots.txt`, and `/sitemap.xml`. Keep staging noindexed and
   deploy repository changes only through Jenkins.

Google Search Central guidance: [site moves](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes), [crawl errors](https://developers.google.com/search/docs/crawling-indexing/troubleshoot-crawling-errors).
