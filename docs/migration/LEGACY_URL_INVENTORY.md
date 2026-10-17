# Legacy WordPress URL inventory — partial, updated 2026-10-17

## Sources and limits

- The previous WordPress [blog index](https://drfarahvipurgentcare.com/blog/) remains in a pre-cutover search snapshot. The original 20 article paths below came from that snapshot. Search results from October 2026 exposed 20 more article paths; search indexes can be stale and are **not** a WordPress export.
- This document now lists 46 distinct article paths (the original 20, the 20 newly found paths, and six previously noted search-visible paths), plus two archive paths and eight structural redirects. A further article title has no verified URL.
- This is **not** a complete historical crawl. The retained WordPress published-URL export and Google Search Console page data have not been supplied or compared. Do not mark the migration complete based on search results alone.
- On 2026-10-17, direct production HTTP checks returned `301` with an immediate `https://drfarahvipurgentcare.com/...` Location for all eight redirects in `frontend/.htaccess.production`. Representative old article paths and `/blog/` returned `404`; the full article list was not individually checked.

## Unambiguous page mappings

| Old path | New path | Decision |
| --- | --- | --- |
| `/booking` and `/booking/` | `/book` | Live 301; new booking page is the replacement flow. |
| `/services/` | `/services` | Live 301 to the canonical extensionless URL; match only the trailing-slash path to avoid a redirect loop. |

The other six live 301s are `/about-us/` → `/about`, `/contact-us/` → `/contact`, `/prp-prf-exosomes-center/` → `/prp-treatments`, `/urgent-care-near-you/` → `/services`, `/vip-urgent-care/` → `/services`, and `/faq/` → `/services`. The check above verified their first response and direct HTTPS Location.

## Blog articles needing a content decision

Each path below appeared on the old blog index. The 2026-10-08 fetch returned 404. Do not redirect these to a broad service or home page without confirming that the destination contains the corresponding content. Keep their status under review while clinical claims and original copy are checked.

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

These 20 exact paths were visible as old-site results or as a link from an old article. They are candidates for recovery or content review, **not** approved redirect targets. Live spot checks on `/why-physician-led-urgent-care-feels-better/`, `/how-tirzepatide-supports-metabolic-health/`, and `/bronchitis-treatment-without-er-visits/` returned 404 on 2026-10-17.

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

The archived blog index also mentions an article titled “Semaglutide vs Tirzepatide: Which Fits Best?”, but its exact URL has not been verified and is **not** counted among the paths above.

## Other previously found paths

- Articles: `/guide-to-urgent-care-visits/`, `/private-urgent-care-appointments/`, `/urgent-care-vs-emergency-room/`, `/urgent-care-for-cough-los-angeles/`, `/concierge-urgent-care-clinic/`, `/walk-in-clinic-vs-appointment-your-options-at-dr-farahs-la-urgent-care/`.
- Archives: `/blog/` (live 404 on 2026-10-17) and `/category/blog/` (not rechecked).

The archives have no current equivalent and must not be sent to the homepage by a blanket rule. For articles, a service landing page that merely mentions the topic is not automatically equivalent to the original educational article.

## To complete the migration

1. Obtain the published post/page URL list or XML export from the retained GoDaddy WordPress site, including the exact slug and publication status. Obtain a pre-cutover Search Console **Pages** export with clicks and impressions, plus not-found URLs if available. Neither source was accessible for this audit.
2. Compare and de-duplicate against the 46 article paths, eight structural routes and two archives here. Include pagination and query-string variants; prioritize paths that actually had search traffic or links.
3. For each article, choose one of: preserve a clinically reviewed article at its old slug; consolidate into a truly equivalent new page with a 301; or retire it with a real 404/410. The clinic must review current medical and service claims before republishing old copy, especially treatment, medication and outcome claims. Do not treat a current 404 as an approved permanent-retirement decision.
4. After any approved redirect or article change, verify production HTTP status and first `Location`, canonical tags, `/robots.txt`, and `/sitemap.xml`. Keep staging noindexed and deploy only through Jenkins.

Google Search Central guidance: [site moves](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes), [crawl errors](https://developers.google.com/search/docs/crawling-indexing/troubleshoot-crawling-errors).
