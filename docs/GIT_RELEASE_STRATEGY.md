# Git Branch and Release Strategy — Dr. Farah

**Status:** APPROVED  
**Approved:** 2026-10-29  
**Applies to:** `ben-edu/project_drfarah`

## 1. Objective

Prevent branch drift, silent omission of tested development work, and production-only history from accumulating outside the integration branch.

The normal release path is:

`feature/fix/docs branch -> dev -> main`

`dev` is the integration/staging branch. `main` is production. A normal production release must promote a coherent, validated `dev` state rather than manually copying selected files from `dev` to a branch based on `main`.

## 2. Core invariant

Before a normal `dev -> main` promotion, the current production `main` history must already be contained in `dev`.

Operationally, the intended invariant is:

`main` is an ancestor of `dev` before release.

If `main` contains commits that are not in `dev`, the next action is reconciliation/back-merge, not a new production promotion.

## 3. Standard development flow

1. Create proposed work on a feature/fix/docs branch from the current `dev` state.
2. Validate the exact branch SHA in CI.
3. Merge validated work to `dev`.
4. Allow `dev` staging CI/deployment to validate the integrated state.
5. Before production promotion, compare `main` and `dev` and confirm `dev` contains all current `main` commits.
6. Open the production promotion from `dev` to `main`.
7. Merge only when the exact promotion SHA/diff and required checks are acceptable.
8. Verify the resulting `main` production build/smoke evidence.

This makes the production release a promotion of the tested integration state, not an independently reconstructed subset.

## 4. Production hotfix exception

A direct fix based on `main` is allowed only when production recovery or another urgent production-only condition makes the normal `dev -> main` path inappropriate.

When a production hotfix is used:

1. branch from current `main`;
2. make the smallest safe production fix;
3. validate and merge it to `main`;
4. immediately back-merge/reconcile the new `main` into `dev`;
5. resolve conflicts deliberately while preserving both the production fix and valid `dev` work;
6. require CI on the reconciled `dev` state;
7. do not continue unrelated release work while `main` contains production commits absent from `dev` unless a documented emergency requires it.

A production hotfix is not complete until its history and behavior are represented in `dev`.

## 5. Selective production promotion

Copying or cherry-picking only selected files/commits from `dev` onto a branch based on `main` is an exception, not the default release method.

It is allowed only when all of the following are true:

- a specific production change is time-sensitive or independently releasable;
- the rest of `dev` is intentionally not production-ready;
- dependencies of the selected change have been checked explicitly;
- omitted `dev` work is documented and is not falsely treated as deployed;
- the release diff is minimal and reviewed;
- after the production merge, `main` is immediately reconciled back into `dev` so branch history does not continue to diverge.

Selective promotion must never be used merely because branch histories have drifted. Branch drift must be repaired.

## 6. Dependency rule

A file that passed tests on `dev` is not automatically safe to copy alone to `main`.

Before any selective promotion, verify whether it depends on:

- JavaScript/CSS/assets changed elsewhere;
- API/database/schema changes;
- environment/config changes;
- routing/redirect behavior;
- CI/deployment changes;
- measurement/analytics changes;
- other files introduced in the same integrated `dev` state.

If the dependency cannot be shown to be independent, promote the coherent integrated change rather than an isolated file.

## 7. Required pre-release checks

Before opening or merging a normal production PR:

- fetch/inspect current `dev` and `main` heads;
- inspect exact Jenkins/GitHub status for the candidate SHA;
- compare `main...dev`;
- confirm there are no production commits missing from `dev`;
- inspect the complete production diff, not just the newest feature diff;
- confirm no validated `dev` work is silently omitted unless explicitly deferred;
- record any intentional deferral in `ROADMAP.md`/`PROJECT_HANDOFF.md`.

## 8. Required post-release checks

After a production merge:

- verify the exact new `main` SHA;
- require production Jenkins/smoke result;
- if the release was a normal `dev -> main` promotion, confirm branch relationship remains expected;
- if the release was a hotfix or selective production exception, immediately create the `main -> dev` reconciliation/back-merge;
- do not call the exception complete until reconciled `dev` CI is green.

## 9. Documentation and automation rules

`PROJECT_HANDOFF.md` must record current `dev` and `main` SHAs when branch/release state materially changes, including whether reconciliation is required.

`ROADMAP.md` records any deferred production-ready work or branch-reconciliation blocker that cannot be closed immediately.

The autonomous project runner must check branch lineage before production promotion. If `main` has commits absent from `dev`, branch reconciliation takes priority over unrelated production promotion.

## 10. Current reconciliation — 2026-10-29

Historical production fixes caused `dev` and `main` to diverge. The traveler landing was then promoted through a narrow production PR as a temporary safety measure.

The approved corrective action is to create a controlled reconciliation merge whose parents include current `dev` and current `main`, preserve the valid `dev` integrated state, import the production Jenkins redirect-smoke correction, and then validate the reconciled state in CI.

After that reconciliation, normal releases return to `feature/fix/docs -> dev -> main`; production-only hotfixes must be immediately back-merged.