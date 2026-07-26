# HANDOFF — 2026-07-26 (Step 06: Immutable Staging API Image)

## Current state

- **Branch:** `fix/immutable-staging-api-image`
- **Base:** `dev` (eb728ff)
- **Commit:** see `SESSION_LOG.md` for the commit SHA after push.

## Work completed (Step 06 — Immutable Staging API Image)

### Root cause of `:dev` being deployed

The Jenkinsfile derived the image tag from `${GIT_COMMIT:-dev}`. When
`GIT_COMMIT` was empty or unset in the Jenkins environment, the fallback `dev`
was used. This resulted in the live Deployment running the `:dev` tag instead
of the immutable commit SHA.

### Fix applied

1. **All image-tag derivations** now use `git rev-parse HEAD` directly from the
   checked-out repository instead of `${GIT_COMMIT:-dev}`.
2. **POSIX validation** confirms each derived SHA is a 40-character lowercase
   hexadecimal string. The build fails immediately on empty or malformed SHAs.
3. **Deployment rendering** uses `kubectl set image -f ... --dry-run=client -o yaml
   | kubectl apply -f -` so the committed `:dev` placeholder is never applied
   to the cluster.
4. **Post-rollout verification** queries the live Deployment image via
   `kubectl get deployment -o jsonpath` and compares it with the expected
   immutable SHA. Mismatch fails the build.
5. **Both Harbor tags** (`<sha>` and `:dev`) continue to be pushed. The
   immutable SHA tag is the deployment source of truth; `:dev` is only a
   convenience alias.

### Files changed (4 files)

| File | Change |
|---|---|
| `Jenkinsfile` | Replaced all `${GIT_COMMIT:-dev}` with `git rev-parse HEAD` + validation; switched to rendered Deployment application; added post-rollout image verification |
| `kubernetes/drfarah-staging/README.md` | Documented immutable image tagging and deployment rendering |
| `HANDOFF.md` | This handoff |
| `SESSION_LOG.md` | Session entry added |

### Local `.gitignore` modification

The working tree had an uncommitted addition to `.gitignore`:
`**/.pytest_cache/`. This is appropriate Python pytest-cache exclusion and is
included in the branch commit.

### What was NOT done

- No SMTP, secret, or password changes.
- No RBAC changes (Jenkins still lacks `pods/exec` and Events access).
- No production deployment.
- No frontend redesign.
- No Keycloak, admin UI, HAProxy, DNS, or TLS changes.
- No PR merge (awaiting operator review).

## Recommended next step

1. Push the branch and open a PR into `dev`.
2. After merge, trigger a `dev` build in Jenkins.
3. Verify the Jenkins deploy stage log shows:
   - `Expected image: harbor...:<sha>`
   - `Deployed image: harbor...:<sha>`
   - `Immutable image verification passed.`
4. Confirm the live Deployment image matches the commit SHA.

Do not start admin/Keycloak until the booking flow is verified end-to-end.
