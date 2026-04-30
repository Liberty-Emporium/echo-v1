#!/bin/bash
# sync-all-to-gitlab.sh — Mirror all Liberty-Emporium repos GitHub → GitLab
set -e

GH_TOKEN=$(cat /root/.secrets/github_token)
GL_TOKEN=$(cat /root/.secrets/gitlab_token)

REPOS=(
  "echo-v1"
  "alexander-ai-dashboard"
  "alexander-ai-floodclaim"
  "alexander-ai-agent-widget"
  "alexander-ai-inventory"
  "alexander-ai-petvet"
  "alexander-ai-contractor"
  "alexander-ai-consignment"
  "liberty-oil-website"
  "Drop-Shipping-by-alexander-ai-solutions"
)

TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT

echo "[$(date '+%Y-%m-%d %H:%M')] Starting GitLab sync..."
SUCCESS=0; FAILED=0

for repo in "${REPOS[@]}"; do
  echo "  Syncing $repo..."

  # Ensure GitLab repo exists
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Authorization: Bearer $GL_TOKEN" \
    "https://gitlab.com/api/v4/projects/Liberty-Emporium%2F$(python3 -c "import urllib.parse; print(urllib.parse.quote('${repo}', safe=''))")")

  if [ "$STATUS" = "404" ]; then
    echo "    Creating GitLab repo for $repo..."
    curl -s -X POST -H "Authorization: Bearer $GL_TOKEN" \
      -H "Content-Type: application/json" \
      "https://gitlab.com/api/v4/projects" \
      -d "{\"name\":\"${repo}\",\"namespace_id\":130241649,\"visibility\":\"private\",\"initialize_with_readme\":false}" > /dev/null
    sleep 2
  fi

  REPO_DIR="$TMPDIR/$repo"
  git clone --mirror "https://x-access-token:${GH_TOKEN}@github.com/Liberty-Emporium/${repo}.git" "$REPO_DIR" 2>/dev/null || {
    echo "    ⚠️  Skipping $repo (not found on GitHub)"
    FAILED=$((FAILED+1))
    continue
  }

  cd "$REPO_DIR"
  git push --mirror "https://oauth2:${GL_TOKEN}@gitlab.com/Liberty-Emporium/${repo}.git" 2>&1 | grep -E "branch|error|Done|->|everything" || true
  cd /
  SUCCESS=$((SUCCESS+1))
  echo "    ✅ $repo synced"
done

echo ""
echo "[$(date '+%Y-%m-%d %H:%M')] GitLab sync complete — $SUCCESS synced, $FAILED skipped ✅"
