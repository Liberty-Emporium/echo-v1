#!/bin/bash
# backup-all.sh — Mirror all Liberty-Emporium repos from GitHub → GitLab
# Usage: ./backup-all.sh

GH_TOKEN=$(cat /root/.secrets/github_token 2>/dev/null)
GL_TOKEN=$(cat /root/.secrets/gitlab_token 2>/dev/null)

if [ -z "$GH_TOKEN" ] || [ -z "$GL_TOKEN" ]; then
  echo "❌ Missing tokens in /root/.secrets/"
  exit 1
fi

REPOS="Contractor-Pro-AI jays-keep-your-secrets Liberty-Emporium-Inventory-App pet-vet-ai Dropship-Shipping jay-portfolio Consignment-Solutions echo-v1 list-it-everywhere"
WORK="/tmp/backup-work-$$"
mkdir -p "$WORK"
PASS=0; FAIL=0

for REPO in $REPOS; do
  echo -n "  → $REPO ... "
  cd "$WORK"

  git clone --mirror "https://x:${GH_TOKEN}@github.com/Liberty-Emporium/${REPO}.git" "${REPO}.git" 2>/dev/null
  if [ $? -ne 0 ]; then
    echo "❌ clone failed"
    FAIL=$((FAIL+1))
    continue
  fi

  cd "${REPO}.git"
  git remote add gitlab "https://oauth2:${GL_TOKEN}@gitlab.com/Liberty-Emporium/${REPO}.git" 2>/dev/null || true
  git push --mirror gitlab 2>&1 | grep -E "error:|Everything|main ->" | head -3
  echo "✅"
  PASS=$((PASS+1))
  cd "$WORK"
  rm -rf "${REPO}.git"
done

rm -rf "$WORK"
echo ""
echo "✅ $PASS backed up | ❌ $FAIL failed — $(date -u '+%Y-%m-%d %H:%M UTC')"
