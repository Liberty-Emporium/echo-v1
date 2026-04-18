# HEARTBEAT.md — Echo Active Checks

## 🔁 Cron Guard (CRITICAL — check every heartbeat)

These two cron jobs MUST always be running. If either is missing, recreate it immediately.

### Required Cron Jobs:
1. **Brain Backup** (ID: `39e5109c-73a9-4840-8477-4b3e35a97d13`)
   - Schedule: every 30 minutes
   - Task: `bash /root/.openclaw/workspace/echo-v1/scripts/backup-brain.sh`

2. **GitLab App Sync** (ID: `87985897-7926-4e1b-a58a-1ce1bfd5639c`)
   - Schedule: every 2 hours
   - Task: `bash /root/.openclaw/workspace/echo-v1/scripts/sync-all-to-gitlab.sh`

### On every heartbeat:
- Call `cron list` and verify both jobs exist and are enabled
- If either is missing or disabled → recreate/re-enable it immediately
- If both present and enabled → HEARTBEAT_OK

> Rule #7: These crons must be alive every session, no exceptions.
