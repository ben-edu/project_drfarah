# Jenkins Google Ads reporting — SCM-backed operator runbook

**2026-11-22 | Project:** Dr. Farah VIP Urgent Care  
**Status:** operational pipeline in review branch PR #144; Jenkins operator observed successful SCM-pipeline build #4 on 2026-11-22, before latest summary-output change. Latest `OUTPUT_FORMAT` amendment requires a new Jenkins build to validate. This file is a feature-branch document until PR is merged into `dev`.

## Purpose and source of truth

Use one standalone, **read-only** pipeline in the same `ben-edu/project_drfarah` repository instead of pasting or changing Groovy code in the Jenkins web UI for every report. The normal root `Jenkinsfile` remains untouched. This job must never deploy the site, upload conversion events, or mutate Ads budgets, bids or campaigns.

- Job: `drfarah-google-ads-api-validate`
- Source: `jenkins/google-ads/Jenkinsfile`
- Repository URL: `https://github.com/ben-edu/project_drfarah.git`
- Active pre-merge branch: `*/feature/google-ads-api-readonly-reporting-20261122`
- After review and merge: point the SCM branch at `*/dev`, then run and verify again. Do not switch to `main` without a separate promotion decision.
- Jenkins configuration: **Configure → Pipeline → Definition: Pipeline script from SCM → SCM: Git → Repository URL / Branch Specifier / Script Path** as above. `checkout scm` then fetches the reporting module from the same ref.
- Keep the three original Google Data Manager Jenkins jobs unchanged.

## Credentials and execution boundary

The Jenkins job reuses *existing* protected Jenkins credentials `drfarah-google-data-manager-sa-json` (file secret) and `harbor-robot-devops-project-harbor` (registry). They are passed into an ephemeral Docker invocation of the pinned Harbor API image with report-code source bind-mounted from the SCM checkout. ADC for `google_ads_reporting.py` acquires an `adwords`-scoped token; Google Ads `SearchStream` remains read-only. Never paste tokens, service-account JSON, Docker credential files, or other secret values into GitHub or chat. Changes to this Jenkinsfile run in a credential-bearing context: accept commits only from reviewed/trusted writers and preserve branch protection/review gates.

This design allows GitHub edits without manual Groovy paste but **does not give the assistant control of Jenkins job configuration or permission to click Build**. The owner operates Jenkins unless an approved build trigger is independently verified.

## Parameters

In Jenkins → **Build with Parameters**:

| Parameter | Values | Default / meaning |
|---|---|---|
| `REPORT` | `full_audit`, `account`, `budgets`, `campaigns`, `daily`, `ad_groups`, `search_terms`, `changes` | `full_audit` performs all seven readonly reports |
| `START_DATE` | `YYYY-MM-DD` or blank | Blank: six days before `END_DATE` |
| `END_DATE` | `YYYY-MM-DD` or blank | Blank: current date in `America/Los_Angeles` |
| `OUTPUT_FORMAT` | `summary` or `raw` | `summary`: concise console; `raw`: all returned JSON |

Date range may not exceed the current LA-local date or reach 30 days (Change Events constraint). No changes to live Google Ads occur.

**`summary` behavior:** account/budgets/campaigns/daily/ad_groups remain readable as JSON; Search Terms shows totals and top 20 *paid* terms ranked by spend (other rows hidden in summary, not omitted from the API result); Change Events shows counts by type and up to eight recent entries. **`raw`** is needed to audit all term rows or exact Change Events; long raw console logs may be truncated by manual copying, so use carefully. Search-term text can reveal sensitive health interests; do not publish raw logs to public GitHub.

## Why OUTPUT_FORMAT can be missing

Jenkins displays parameters from the Job's most recently evaluated Pipeline definition. The owner-provided screenshot showed four successful builds, with #4 at approximately 21:39, **before** the `OUTPUT_FORMAT` change was committed to the feature branch. This is expected for an older parameter UI, not proof of a bad SCM configuration.

1. Leave current `REPORT=full_audit` and date fields blank, click **Build** once. A pipeline run loads the newer Jenkinsfile (assuming SCM ref is still correct); select a report choice on that first run if the new parameter has not yet appeared.
2. After that build, refresh the job page and reopen **Build with Parameters**. Confirm the new `OUTPUT_FORMAT=summary/raw` control.
3. If missing, inspect build Console Output for `REPORT_SOURCE_COMMIT=` and compare it with the expected feature branch HEAD; inspect Jenkins **Configure → Pipeline → Branch Specifier / Script Path**. Do not paste a second inline script.
4. Check the build actually runs the new summary logic and ends SUCCESS; the summary formatter had **not** been live-validated at the time of the 2026-11-22 documentation update.

## GitHub hook trigger for GITScm polling

The owner reported enabling **Triggers → GitHub hook trigger for GITScm polling** in Jenkins. This is **not** confirmation that a GitHub webhook is configured or delivering. The GitHub Plugin accepts a GitHub push webhook, matches a configured repository, and polls the selected Git SCM branch for changes. It is event-driven polling, **not** a periodic report schedule and not a guaranteed auto-build for every GitHub change.

- Review the repository's GitHub **Settings → Webhooks** for a GitHub push hook to the Jenkins GitHub Plugin endpoint (typically `https://jenkins.proxbenovh.cloud/github-webhook/`, provided this is actually configured by Jenkins). Examine **Recent Deliveries** for successful HTTP delivery, and Jenkins **GitHub Hook Log** for receipt; do not create duplicate webhooks.
- Verify a permitted, reviewed change on the selected branch triggers a new Jenkins build. Do not count successful manual builds as webhook delivery evidence.
- Since code on this branch can run with Jenkins credentials, disable the trigger if code-review/branch access is not sufficiently controlled. The default is an operator-started build. There is no schedule/cron trigger in the new Jenkinsfile.
- The hook triggers on SCM changes, not automatically once per week for business reporting. That would require a separate approved schedule.

## Successful milestones / remaining checks

- 2026-11-22: existing service account authenticated against production Ads account `6525103588`; direct `account` read returned USD and `America/Los_Angeles`.
- Subsequent `budgets`, `campaigns`, `daily` read-only job succeeded; operator-supplied metrics saved as evidence in PR #144 and `PROJECT_HANDOFF.md`.
- Owner later supplied a successful SCM Pipeline console tail with 21 `change_event` results auditing API budget/schedule mutations (one budget resource and 20 campaign-criterion events). Tail of Search Terms showed only some zero-click/zero-cost terms, not full paid terms.
- Direct Google Ads write successes previously reported: Urgent Search daily budget $36 → $10; Urgent and Traveler Search scheduled Monday–Friday 08:30–16:30 LA account time. These writes were from a separate approved action connector, **not** from the reporting Jenkinsfile.
- Remaining: first live validation of revised `OUTPUT_FORMAT=summary`; post-write budget readback `campaignBudgets/15988400106 amountMicros=10000000`; assess full paid search terms; cross-check native Ads billed spend and Auto-apply settings independently. Platform conversions/calls are not confirmed patient visits.
- Draft PR #144 must be reviewed and merged into `dev` under the normal branch policy; publishing this documentation is not deployment.

## Authoritative references

- Jenkins Pipeline syntax: https://www.jenkins.io/doc/book/pipeline/syntax/
- Jenkins using a Jenkinsfile: https://www.jenkins.io/doc/book/pipeline/jenkinsfile/
- Jenkins GitHub Plugin webhook trigger: https://plugins.jenkins.io/github/
- Google Ads client operator notes: `docs/GOOGLE_ADS_DIRECT_API_READONLY_2026-11-22.md`
- Current resume and live evidence: `PROJECT_HANDOFF.md` and PR #144
