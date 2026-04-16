#!/bin/bash
# deploy.sh — Deploy any Jay's app to GitHub (triggers Railway)
# Usage: ./deploy.sh <repo-name> "commit message"
# Example: ./deploy.sh Liberty-Emporium-Inventory-App "Fix confirm-delete 500"

REPO="${1}"
MSG="${2:-Deploy $(date -u '+%Y-%m-%d %H:%M UTC')}"
GH_TOKEN=$(cat /root/.secrets/github_token 2>/dev/null)

if [ -z "$REPO" ] || [ -z "$GH_TOKEN" ]; then
  echo "Usage: deploy.sh <repo-name> 'commit message'"
  exit 1
fi

# Figure out branch (jay-portfolio = master, everything else = main)
BRANCH="main"
[ "$REPO" = "jay-portfolio" ] && BRANCH="master"

WORK_DIR="/tmp/deploy-$REPO-$$"
ORG="Liberty-Emporium"

echo "🚀 Deploying $REPO → $BRANCH"
echo "   Message: $MSG"

git clone --depth=1 "https://x:${GH_TOKEN}@github.com/$ORG/$REPO.git" "$WORK_DIR" 2>/dev/null
cd "$WORK_DIR"
git checkout "$BRANCH" 2>/dev/null || true
git config user.email "echo@alexander-ai.digital"
git config user.name "Echo"

# Apply any staged files from /tmp/patches/$REPO/ if they exist
if [ -d "/tmp/patches/$REPO" ]; then
  echo "  Applying patches from /tmp/patches/$REPO/"
  cp -r /tmp/patches/$REPO/. .
fi

# Bump CACHEBUST in Dockerfile if it exists
if [ -f "Dockerfile" ]; then
  TS=$(date +%s)
  sed -i "s/ARG CACHEBUST=.*/ARG CACHEBUST=$TS/" Dockerfile
  git add Dockerfile
fi

git add -A
git diff --cached --stat

if git diff --cached --quiet; then
  echo "⚠️  Nothing to commit"
else
  git commit -m "$MSG"
  git push "https://x:${GH_TOKEN}@github.com/$ORG/$REPO.git" "$BRANCH"
  echo "✅ Pushed $REPO — Railway will deploy shortly"
fi

cd / && rm -rf "$WORK_DIR"
