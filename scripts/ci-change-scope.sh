#!/bin/sh
# Print exactly one of: full, static, docs. Unknown history always means full.
set -eu

full() {
  echo full
  exit 0
}

head="$(git rev-parse --verify HEAD 2>/dev/null)" || full

case "${BRANCH_NAME:-}" in
  dev|main)
    # Compare deployments with the last *successful* build of this branch.
    # A failed deployment must not hide its changes behind a later static edit.
    base="${GIT_PREVIOUS_SUCCESSFUL_COMMIT:-}"
    printf '%s\n' "$base" | grep -Eq '^[0-9a-fA-F]{40}$' || full
    if ! git cat-file -e "$base^{commit}" 2>/dev/null; then
      git fetch --no-tags --quiet origin "$base" 1>&2 || full
    fi
    ;;
  *)
    # static/* and docs/* branches start at main and can use one PR to main.
    # Other branches continue to compare with dev. PR targets take precedence.
    target="${CHANGE_TARGET:-}"
    if [ -z "$target" ]; then
      case "${BRANCH_NAME:-}" in
        static/*|docs/*) target=main ;;
        *) target=dev ;;
      esac
    fi
    case "$target" in main|dev) ;; *) full ;; esac
    ref="refs/remotes/origin/$target"
    git fetch --no-tags --quiet origin "refs/heads/$target:$ref" 1>&2 || full
    base="$(git merge-base "$ref" "$head" 2>/dev/null)" || full
    ;;
esac

git merge-base --is-ancestor "$base" "$head" 2>/dev/null || full
[ "$base" != "$head" ] || full

changed="$(mktemp)" || full
trap 'rm -f "$changed"' EXIT HUP INT TERM
# Disable rename detection so moving API/CI files into an allowed directory
# cannot hide the old path. Git quotes unusual filenames, which fail closed.
git diff --no-renames --name-only "$base" "$head" > "$changed" || full
[ -s "$changed" ] || full

scope=docs
while IFS= read -r path; do
  case "$path" in
    *.md)
      case "$path" in
        */*) case "$path" in docs/*) ;; *) full ;; esac ;;
      esac
      ;;
    frontend/*.html|frontend/*.css|frontend/.htaccess.production|frontend/robots.production.txt|frontend/sitemap.xml|\
    frontend/assets/*.jpg|frontend/assets/*.jpeg|frontend/assets/*.png|frontend/assets/*.webp|\
    frontend/assets/*.avif|frontend/assets/*.gif|frontend/assets/*.svg|frontend/assets/*.ico|\
    frontend/assets/*.woff|frontend/assets/*.woff2)
      scope=static
      ;;
    *) full ;;
  esac
done < "$changed"

echo "$scope"
