#!/bin/sh

# Assemble the crawlable production frontend without modifying the staging
# source tree. The destination must be a dedicated temporary directory.

set -eu

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 SOURCE_DIR DESTINATION_DIR" >&2
  exit 2
fi

source_dir="$1"
destination_dir="$2"

[ -d "$source_dir" ] || {
  echo "FAIL: frontend source directory is missing: $source_dir" >&2
  exit 1
}

[ -f "$source_dir/.htaccess.production" ] || {
  echo "FAIL: production Apache policy is missing." >&2
  exit 1
}

[ -f "$source_dir/robots.production.txt" ] || {
  echo "FAIL: production robots policy is missing." >&2
  exit 1
}

mkdir -p "$destination_dir"

if find "$destination_dir" -mindepth 1 -print -quit | grep -q .; then
  echo "FAIL: production assembly destination is not empty: $destination_dir" >&2
  exit 1
fi

cp -a "$source_dir/." "$destination_dir/"
cp "$source_dir/.htaccess.production" "$destination_dir/.htaccess"
cp "$source_dir/robots.production.txt" "$destination_dir/robots.txt"
rm -f \
  "$destination_dir/.htaccess.production" \
  "$destination_dir/robots.production.txt"

FRONTEND_PRODUCTION_ROOT="$destination_dir" python3 - <<'PY'
import os
from pathlib import Path

root = Path(os.environ["FRONTEND_PRODUCTION_ROOT"])
staging_tag = '<meta name="robots" content="noindex,nofollow,noarchive">'

html_files = sorted(root.rglob("*.html"))
if not html_files:
    raise SystemExit("FAIL: no HTML files found in production assembly")

for path in html_files:
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace(staging_tag, ""), encoding="utf-8")
PY

if grep -R -nF 'noindex,nofollow,noarchive' "$destination_dir" --include='*.html'; then
  echo "FAIL: staging noindex metadata remains in production HTML." >&2
  exit 1
fi

if grep -R -nF '/wp-content/uploads/' "$destination_dir" --include='*.js' --include='*.html'; then
  echo "FAIL: a production asset still depends on legacy WordPress." >&2
  exit 1
fi

if grep -qF 'CUTOVER_BLOCKER' "$destination_dir/.htaccess"; then
  echo "FAIL: legacy redirect blocker remains in production Apache policy." >&2
  exit 1
fi

grep -qF 'LEGACY_REDIRECT_RISK_ACCEPTED: 2026-09-21' "$destination_dir/.htaccess" || {
  echo "FAIL: documented legacy redirect decision is missing." >&2
  exit 1
}

grep -qF 'Allow: /' "$destination_dir/robots.txt" || {
  echo "FAIL: production robots policy is not crawlable." >&2
  exit 1
}

if grep -qF 'Disallow: /' "$destination_dir/robots.txt"; then
  echo "FAIL: staging robots policy leaked into production assembly." >&2
  exit 1
fi

grep -qF 'https://drfarahvipurgentcare.com/sitemap.xml' "$destination_dir/robots.txt" || {
  echo "FAIL: production robots policy has the wrong sitemap." >&2
  exit 1
}

echo "Production frontend assembly passed."
