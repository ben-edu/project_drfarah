# Fast releases for small website changes

## One PR for static content

For a change limited to public page HTML, CSS, approved image/font files,
production redirects, robots, or sitemap:

1. Create a `fix/static-*` branch from current `main`.
2. Make and review the change. Let Jenkins finish the branch build before
   opening the PR, so an old branch check cannot be left pending if Jenkins
   disables the branch job after discovering the PR.
3. Open **one PR to `main`**. Verify the exact diff and the successful branch
   SHA. A duplicate PR build is not needed if repository protection does not
   require it.
4. Merge the PR. Require Jenkins `main` success for the merge SHA and verify
   the changed behavior on the live site. A merge is not deployment evidence.

There is no automatic merge merely because a build is green. An authorized
operator or a task-specific release automation still reviews the PR and acts
on its exact head SHA.

## What Jenkins skips

`scripts/ci-change-scope.sh` compares **all changes** with the target branch
for a feature/PR build, and with the previous successful build for `dev` and
`main`. It returns `static` only if every changed path is one of:

- `frontend/*.html`, `frontend/*.css`;
- image/font files in `frontend/assets/` (`jpg`, `jpeg`, `png`, `webp`,
  `avif`, `gif`, `svg`, `ico`, `woff`, `woff2`);
- `frontend/.htaccess.production`, `frontend/robots.production.txt`,
  `frontend/sitemap.xml`.

Static builds run repository/secret/hostname checks and frontend validation.
On `main`, production preflight, frontend publication and live frontend/admin/
API smoke checks still run. API tests, PostgreSQL integration, API and backup
image builds, Kubernetes API redeployment, and the disposable restore test are
skipped **only** because no API, database, backup, CI, or deployment file changed
since the last successful `main` build. The existing backup schedule is not
changed. Production's eight legacy redirects are checked for a direct HTTPS
`301 Location`, not merely for a final page after following redirects.

A Markdown-only change (`docs/**/*.md` or a root `*.md`) is classified `docs`:
repository checks run, but no application test or deployment is repeated.
Use a `fix/docs-*` branch from `main` for one PR if it is independent of pending
development work.

Unknown history, a missing previous successful SHA, an unrecognized path,
or a change to the classifier/Jenkinsfile falls back to `full`. If an earlier
production build failed, changes since the last **successful** build remain
in scope; a later static edit cannot hide them.

## Full delivery path

Use a feature/fix branch from `dev` → PR to `dev` → staging build and review
→ release PR to `main` for API, booking JavaScript, registration, admin,
Kubernetes, CI/deployment scripts, or other changes outside the static list.
Choose this path for any static edit that needs staging review before release.
The existing production tests, image builds, deployment, backup and restore
gate stay in place for these builds.
