#!/bin/bash
# Auto-push to GitHub using GIT_TOKEN from environment
# Usage: bash gitpush.sh "commit message"

set -e

MSG="${1:-Auto update from Replit}"

if [ -z "$GIT_TOKEN" ]; then
  echo "❌ GIT_TOKEN not set. Add it to Replit Secrets."
  exit 1
fi

REPO_URL="https://${GIT_TOKEN}@github.com/dhruvkumarray3-eng/DHRUV_X_RADHA.git"

git config user.email "bot@replit.com"
git config user.name "SHUKLA BOT"

git add -A
git commit -m "$MSG" || echo "⚠ Nothing to commit"
git push "$REPO_URL" HEAD:main

echo "✅ Pushed to GitHub successfully!"
