# Git branch audit — Dr. Farah — 2026-11-08

**Repository:** `ben-edu/project_drfarah`  
**Canonical strategy:** `docs/GIT_RELEASE_STRATEGY.md`  
**Operator checklist:** https://github.com/ben-edu/project_drfarah/issues/141  
**Method:** GitHub `compare` with exact branch heads against both `dev` and `main` before cleaning. Re-check the ancestry at deletion time.

## A. Core branches — never delete

- `dev`: default branch, source for integration and staging deploys.
- `main`: production deploy branch.
- GitHub `delete_branch_on_merge=true`. Release PR #140 merged the owner-approved medical Hero into `main`; main release SHA `37794a7490ff338e1648fd788b0c38527fef838a`.

## B. Fully merged branches — safe ref deletion candidates, pending tool/admin access

Each of these head commits was verified to be an ancestor of BOTH main and dev (0 unique commits compared with each), so deleting only the ref does not discard the historical changes:

| Old ref | Audited head SHA | Action |
|---|---|---|
| `chore/git-release-strategy-reconcile-20261029` | `085df28a6488587bae94bd1400553b8750091555` | Prune after fresh ancestry check |
| `ci/fast-static-docs-delivery-20261016` | `1dfbaaa3fbb1274415b1a2284870c178fa9d4fad` | Prune after fresh ancestry check |
| `feat/authentic-image-refresh-20261031` | `591a825b074137822fbb91ba20bee6f12a5b1db6` | Prune after fresh ancestry check |
| `fix/ci-urgent-care-redirect-smoke-20261029-check` | `46a551683402d99d896652788e35d7fe606472f1` | Prune after fresh ancestry check |
| `fix/visual-polish-mobile-v4-20261031` | `d8354d62d7574916743f1efbecede44de0da8d1d` | Prune after fresh ancestry check |
| `__noop__` | `47e3cd4b36e38f15822bf270cca88c030e4d7901` | Prune after fresh ancestry check |
| `__noop2__` | `47e3cd4b36e38f15822bf270cca88c030e4d7901` | Prune after fresh ancestry check |

**Status:** These refs have **not** been deleted. The installed GitHub connector has no delete-ref action. Do not mark pruning complete on the strength of this audit.

## C. Distinct / unmerged commit histories — retain until reviewed

| Ref | SHA | Unique commits at audit | Reason not to delete |
|---|---|---:|---|
| `docs/independent-ads-audit-handoff-20261107` | `93be361d748503de9230cbe0ff5d0da0149950ff` | 2 | PR #131 closed without merge; overlapping newer audits do not preserve these exact commit IDs |
| `fix/restore-physician-visuals-20261108` | `98d397b4d1066b2661a4bfa9febf6894c06a5114` | 1 | PR #138 closed without merge; superseded by approved owner image PR #139, but unique commit still exists |
| `fix/static-urgent-care-landing-20261028` | `7e5fcad95f4ad97bda375f02cc0112f433698dc3` | 3 | Unmerged changes to urgent-care HTML, production .htaccess and sitemap |
| `release/booking-email-guard-20261018` | `9bb741427ac6073d6a479620395186e298a3a2b0` | 2 | PR #76 closed without merge; involves API/booking email/security, needs deliberate functional review |

**Status:** Retained intentionally; review actual unique commits and archive/tag if retirement is approved. Do not discard potentially relevant clinical booking safeguards without review.

## D. Precise operator cleanup commands (never force)

Run from an authenticated local checkout, **only for the seven refs in section B**, once `origin/dev` contains `origin/main` and no corresponding open PR exists. Example safe guard:

```sh
git fetch origin --prune
branch='__noop__'
git merge-base --is-ancestor "refs/remotes/origin/$branch" refs/remotes/origin/dev &&
git merge-base --is-ancestor "refs/remotes/origin/$branch" refs/remotes/origin/main &&
git push origin --delete "$branch"
```

Repeat for each explicitly listed branch, checking protection and job discovery. Use no wildcard and no `--force`. Preserve the main/dev merge history; verify the remote branch list afterwards.

## E. Outstanding controls

- Review GitHub protection rules for `main` and `dev` in an administrator UI (branch-protection API read was 403); require suitable PR review, exact CI and no force-push.
- Tune Jenkins Multibranch branch/PR discovery to avoid duplicate builds; prune orphaned jobs after old refs are deleted; do not confuse Jenkins job cleanup with Git ref deletion.
- Keep issue #141 OPEN until remote refs truly disappear or an administrator confirms cleanup; update this audit/handoff after actual deletion.
- Production release CI success does not itself prove real-device Hero crop/clarity; operator production QA remains a separate gate.
