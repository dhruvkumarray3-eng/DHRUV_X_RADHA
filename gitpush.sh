#!/bin/bash
# Auto-push to GitHub using GIT_TOKEN from environment
# Usage: bash gitpush.sh "commit message"

set -e

MSG="${1:-Auto update from Replit}"

TOKEN="${GIT_TOKEN:-${GITHUB_PERSONAL_ACCESS_TOKEN:-${GITHUB_TOKEN:-}}}"

if [ -z "$TOKEN" ]; then
  echo "❌ No GitHub token found. Add GIT_TOKEN or GITHUB_PERSONAL_ACCESS_TOKEN to Replit Secrets."
  exit 1
fi

REPO_URL="https://github.com/dhruvkumarray3-eng/DHRUV_X_RADHA.git"
AUTH_HEADER=$(printf 'x-access-token:%s' "$TOKEN" | base64 -w0)

git config user.email "bot@replit.com"
git config user.name "SHUKLA BOT"

git add -A
git commit -m "$MSG" || echo "⚠ Nothing to commit"
git -c http.extraHeader="Authorization: Basic ${AUTH_HEADER}" push "$REPO_URL" HEAD:main

echo "✅ Pushed to GitHub successfully!"
