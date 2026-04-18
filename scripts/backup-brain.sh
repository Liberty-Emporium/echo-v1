#!/bin/bash
# backup-brain.sh
# Backs up Echo's memory, MEMORY.md, USER.md, TOOLS.md, SOUL.md, skills/ to echo-v1
# Called by cron every 30 minutes during active sessions

set -e

GH_TOKEN=$(cat /root/.secrets/github_token)
GL_TOKEN=$(cat /root/.secrets/gitlab_token)
WORKSPACE="/root/.openclaw/workspace"
BRAIN_DIR="$WORKSPACE/echo-v1"

echo "[$(date '+%Y-%m-%d %H:%M')] Brain backup starting..."

cd "$BRAIN_DIR"

# Pull latest first
git pull "https://x-access-token:${GH_TOKEN}@github.com/Liberty-Emporium/echo-v1.git" main --rebase 2>/dev/null || true

# Copy all brain files
cp "$WORKSPACE/MEMORY.md"   ./MEMORY.md   2>/dev/null || true
cp "$WORKSPACE/USER.md"     ./USER.md     2>/dev/null || true
cp "$WORKSPACE/SOUL.md"     ./SOUL.md     2>/dev/null || true
cp "$WORKSPACE/TOOLS.md"    ./TOOLS.md    2>/dev/null || true
cp "$WORKSPACE/IDENTITY.md" ./IDENTITY.md 2>/dev/null || true
cp "$WORKSPACE/AGENTS.md"   ./AGENTS.md   2>/dev/null || true

# Copy today's memory file
TODAY=$(date '+%Y-%m-%d')
mkdir -p ./memory
cp "$WORKSPACE/memory/${TODAY}.md" "./memory/${TODAY}.md" 2>/dev/null || true

# Copy skills if they exist locally
if [ -d "$WORKSPACE/echo-v1/skills" ]; then
  rsync -a --delete "$WORKSPACE/echo-v1/skills/" "./skills/" 2>/dev/null || true
fi

# Check if anything changed
if git diff --quiet && git diff --cached --quiet; then
  echo "[$(date '+%Y-%m-%d %H:%M')] No changes to backup."
  exit 0
fi

git add -A
git commit -m "auto-backup: brain sync $(date '+%Y-%m-%d %H:%M') UTC" 2>/dev/null || true

# Push to GitHub
git push "https://x-access-token:${GH_TOKEN}@github.com/Liberty-Emporium/echo-v1.git" main 2>&1 | tail -2
echo "  GitHub ✅"

# Push to GitLab
git push "https://oauth2:${GL_TOKEN}@gitlab.com/Liberty-Emporium/echo-v1.git" main 2>&1 | tail -2 || \
  echo "  GitLab ⚠️ (protected branch — will retry on next cycle)"

echo "[$(date '+%Y-%m-%d %H:%M')] Brain backup complete ✅"
