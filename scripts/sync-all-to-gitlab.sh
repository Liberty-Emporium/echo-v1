#!/bin/bash
# sync-all-to-gitlab.sh
# Pushes all Liberty-Emporium app repos from GitHub -> GitLab
# Run after any GitHub push to keep GitLab in sync

set -e

GH_TOKEN=$(cat /root/.secrets/github_token)
GL_TOKEN=$(cat /root/.secrets/gitlab_token)

REPOS=(
  "AI-Agent-Widget"
  "ai-widget-test-site"
  "luxury-rentals-demo"
  "Contractor-Pro-AI"
  "jays-keep-your-secrets"
  "Liberty-Emporium-Inventory-App"
  "pet-vet-ai"
  "Dropship-Shipping"
  "jay-portfolio"
  "Consignment-Solutions"
)

TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT

echo "[$(date '+%Y-%m-%d %H:%M')] Starting GitLab sync..."

for repo in "${REPOS[@]}"; do
  echo "  Syncing $repo..."
  
  # Check if GitLab repo exists, create if not
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Authorization: Bearer $GL_TOKEN" \
    "https://gitlab.com/api/v4/projects/Liberty-Emporium%2F$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote('${repo}', safe=''))")")
  
  if [ "$STATUS" = "404" ]; then
    echo "    Creating GitLab repo for $repo..."
    curl -s -X POST -H "Authorization: Bearer $GL_TOKEN" \
      -H "Content-Type: application/json" \
      "https://gitlab.com/api/v4/projects" \
      -d "{\"name\":\"${repo}\",\"namespace_id\":130241649,\"visibility\":\"private\",\"initialize_with_readme\":false}" > /dev/null
    sleep 1
  fi

  # Clone from GitHub and push to GitLab
  REPO_DIR="$TMPDIR/$repo"
  git clone --mirror "https://x-access-token:${GH_TOKEN}@github.com/Liberty-Emporium/${repo}.git" "$REPO_DIR" 2>/dev/null || {
    echo "    Skipping $repo (not found on GitHub)"
    continue
  }
  
  cd "$REPO_DIR"
  git push --mirror "https://oauth2:${GL_TOKEN}@gitlab.com/Liberty-Emporium/${repo}.git" 2>&1 | grep -E "branch|error|Done" || true
  cd /
done

echo "[$(date '+%Y-%m-%d %H:%M')] GitLab sync complete ✅"
