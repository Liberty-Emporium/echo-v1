#!/bin/bash
# ensure-crons.sh
# Verifies the two critical cron jobs exist via the OpenClaw API.
# Call this from session startup or heartbeat checks.
# The cron jobs are managed by KiloClaw and persist across restarts,
# but this script serves as documentation of what must exist.

echo "Critical cron jobs that must always be running:"
echo ""
echo "1. Brain Backup (every 30 min)"
echo "   ID: 39e5109c-73a9-4840-8477-4b3e35a97d13"
echo "   Task: bash /root/.openclaw/workspace/echo-v1/scripts/backup-brain.sh"
echo ""
echo "2. GitLab App Sync (every 2 hours)"
echo "   ID: 87985897-7926-4e1b-a58a-1ce1bfd5639c"
echo "   Task: bash /root/.openclaw/workspace/echo-v1/scripts/sync-all-to-gitlab.sh"
echo ""
echo "If either is missing, Echo will recreate it via the cron tool during heartbeat."
echo "Per Rule #7: GitLab must always stay in sync."
