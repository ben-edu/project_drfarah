#!/bin/sh
set -eu

script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
fixture="$(mktemp -d)"
trap 'rm -rf "$fixture"' EXIT HUP INT TERM

git init -q --bare "$fixture/origin.git"
git init -q "$fixture/work"
cd "$fixture/work"
git config user.name CI
git config user.email ci@example.invalid
git remote add origin "$fixture/origin.git"
git checkout -q -b main
mkdir -p frontend/assets docs api
printf 'Home\n' > frontend/index.html
printf 'Instructions\n' > docs/guide.md
printf 'API\n' > api/app.py
git add .
git commit -qm baseline
baseline="$(git rev-parse HEAD)"
git push -q origin main
git branch dev
git push -q origin dev

assert_scope() {
  expected="$1"
  shift
  actual="$(env "$@" sh "$script_dir/ci-change-scope.sh")"
  if [ "$actual" != "$expected" ]; then
    echo "FAIL: expected $expected, got $actual at $(git rev-parse --short HEAD)" >&2
    exit 1
  fi
}

git checkout -q -b static/page
printf 'Updated\n' >> frontend/index.html
git commit -qam 'static copy'
assert_scope static BRANCH_NAME=static/page
assert_scope full BRANCH_NAME=main
assert_scope static BRANCH_NAME=main GIT_PREVIOUS_SUCCESSFUL_COMMIT="$baseline"
assert_scope full BRANCH_NAME=main GIT_PREVIOUS_SUCCESSFUL_COMMIT=missing

git checkout -q main
git checkout -q -b docs/guide
printf 'More guidance\n' >> docs/guide.md
git commit -qam 'docs edit'
assert_scope docs BRANCH_NAME=docs/guide

git checkout -q main
git checkout -q -b static/booking-js
printf 'code\n' > frontend/booking.js
git add .
git commit -qm 'booking code'
assert_scope full BRANCH_NAME=static/booking-js

git checkout -q main
git checkout -q -b static/accumulated
printf 'API change\n' >> api/app.py
git commit -qam 'failed API build'
printf 'Another page change\n' >> frontend/index.html
git commit -qam 'static follow-up'
assert_scope full BRANCH_NAME=main GIT_PREVIOUS_SUCCESSFUL_COMMIT="$baseline"

git checkout -q main
git checkout -q -b static/rename
git mv api/app.py frontend/assets/app.svg
git commit -qam 'rename API into static assets'
assert_scope full BRANCH_NAME=static/rename

git checkout -q main
git checkout -q -b static/ci
printf 'change\n' > Jenkinsfile
git add .
git commit -qm 'change pipeline'
assert_scope full BRANCH_NAME=static/ci

git checkout -q main
assert_scope full BRANCH_NAME=main GIT_PREVIOUS_SUCCESSFUL_COMMIT="$baseline"

echo 'CI change scope checks passed.'
