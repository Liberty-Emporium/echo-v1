#!/bin/bash
# Brain backup to Liberty-Emporium/echo-v1
# Runs every 20 minutes via cron

cd /root/.openclaw/workspace || exit 1

# Stage all changes
git add -A

# Only commit if there's something to commit
if ! git diff --cached --quiet; then
  git commit -m "Brain backup - $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  git push origin main
  echo "Backup pushed at $(date)"
else
  echo "No changes to backup at $(date)"
fi
