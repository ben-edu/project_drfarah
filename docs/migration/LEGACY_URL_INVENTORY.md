# Legacy WordPress URL inventory — partial, 2026-10-08

## Sources and limits

- The previous WordPress [blog index](https://drfarahvipurgentcare.com/blog/) remains in a search snapshot crawled before cutover; it lists the 20 article paths below. Opening those links through the search service on 2026-10-08 returned 404. The index itself is a historical snapshot, not a live WordPress sitemap.
- Additional old URLs are visible in search results. This is **not** a complete historical crawl. Do not call the migration inventory complete until the retained WordPress site/export and Google Search Console data have been compared.
- The production Apache policy is `frontend/.htaccess.production`. Its six existing structural redirects remain in force. The two extra mappings in this PR cover clear same-intent routes only.

## Unambiguous page mappings

| Old path | New path | Decision |
| --- | --- | --- |
| `/booking` and `/booking/` | `/book` | Add 301; new booking page is the replacement flow. |
| `/services/` | `/services` | Add 301 to the canonical extensionless services URL; match only the trailing-slash path to avoid a redirect loop. |

Existing source-controlled 301s: `/about-us/` → `/about`, `/contact-us/` → `/contact`, `/prp-prf-exosomes-center/` → `/prp-treatments`, `/urgent-care-near-you/` → `/services`, `/vip-urgent-care/` → `/services`, `/faq/` → `/services`. Their live HTTP responses still need verification.

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

Other search-visible old routes to investigate: `/blog/`, `/category/blog/`, `/guide-to-urgent-care-visits/`, `/private-urgent-care-appointments/`, `/urgent-care-vs-emergency-room/`, `/urgent-care-for-cough-los-angeles/`, `/concierge-urgent-care-clinic/`, `/walk-in-clinic-vs-appointment-your-options-at-dr-farahs-la-urgent-care/`. The archive/category paths have no current equivalent and must not be sent to the homepage by a blanket rule.

## To complete the migration

1. Export the old WordPress published URL list or XML sitemap from the retained GoDaddy installation, plus Search Console indexed/traffic URLs. Compare and de-duplicate against this partial list, including query-string and pagination variants.
2. For each article, choose one of: preserve a clinically reviewed article at its old slug; consolidate into a truly equivalent new page with a 301; or retire it with a real 404/410. The clinic must review current medical and service claims before republishing old copy.
3. After branch CI and staging review, verify production HTTP status and `Location` for the redirects, representative unmapped articles, canonical tags, `/robots.txt`, and `/sitemap.xml`. Keep staging noindexed and do not publish by hand outside Jenkins.

Google Search Central guidance: [site moves](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes), [crawl errors](https://developers.google.com/search/docs/crawling-indexing/troubleshoot-crawling-errors).
