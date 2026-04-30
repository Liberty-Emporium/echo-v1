#!/bin/bash
# auto-save.sh — Lightweight brain save for cron (no KYS encryption)
set -e
WORKSPACE="/root/.openclaw/workspace"
ECHO_REPO="$WORKSPACE/echo-v1"
TOKEN=$(cat /root/.secrets/github_token 2>/dev/null) || exit 0

cd "$ECHO_REPO"
git remote set-url origin "https://$TOKEN@github.com/Liberty-Emporium/echo-v1.git" 2>/dev/null

# Copy key brain files
for f in MEMORY.md SOUL.md AGENTS.md TOOLS.md USER.md IDENTITY.md HEARTBEAT.md; do
  [ -f "$WORKSPACE/$f" ] && cp "$WORKSPACE/$f" "$ECHO_REPO/$f"
done
[ -d "$WORKSPACE/memory" ] && cp -r "$WORKSPACE/memory/." "$ECHO_REPO/memory/" 2>/dev/null || true

# Only push if changes exist
git add -A
CHANGED=$(git diff --cached --name-only | wc -l)
if [ "$CHANGED" -gt 0 ]; then
  git config user.email "echo@liberty-emporium.ai"
  git config user.name "Echo"
  git commit -m "🧠 Auto brain-save $(date -u '+%Y-%m-%d %H:%M UTC')"
  git push origin main 2>/dev/null
  # Mirror to GitLab
  GL_TOKEN=$(cat /root/.secrets/gitlab_token 2>/dev/null) || true
  [ -n "$GL_TOKEN" ] && git push "https://oauth2:${GL_TOKEN}@gitlab.com/Liberty-Emporium/echo-v1.git" main 2>/dev/null || true
fi
