#!/bin/bash
# Dual-push script: pushes to both GitHub AND GitLab
# Usage: ./dual-push.sh "commit message"

COMMIT_MSG="${1:-Updates}"
GITLAB_TOKEN=$(cat /root/.secrets/gitlab_token 2>/dev/null)

if [ -z "$GITLAB_TOKEN" ]; then
    echo "❌ No GitLab token found"
    exit 1
fi

# Get the GitLab username
GITLAB_USER=$(curl -s --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "https://gitlab.com/api/v4/user" | python3 -c "import sys,json; print(json.load(sys.stdin).get('username',''))")

if [ -z "$GITLAB_USER" ]; then
    echo "❌ Could not get GitLab username"
    exit 1
fi

# Get current repo name from git
REPO_NAME=$(basename -s .git $(git remote get-url origin 2>/dev/null | sed 's|.*/||'))
GITLAB_REPO="$GITLAB_USER/$REPO_NAME"

# Add GitLab remote if not exists
if ! git remote get-url gitlab 2>/dev/null; then
    git remote add gitlab "https://oauth2:$GITLAB_TOKEN@gitlab.com/$GITLAB_REPO.git"
fi

# Push to both
echo "🚀 Pushing to GitHub and GitLab..."
git push origin main 2>&1
git push gitlab main 2>&1

echo "✅ Dual push complete: GitHub + GitLab"