# Tool: backup-verify
**Type:** Disaster Recovery
**Use when:** After significant changes, periodic verification, pre-deployment check
**Trigger phrases:** "Verify backups", "Check backup integrity", "Backup status", "GitLab sync"

## What It Does
Confirm GitLab mirrors are up to date. Check backup integrity for all Liberty-Emporium projects.

## How To Use

### Step 1: Check GitHub Primary
```bash
# For each major repo:
curl -s "https://api.github.com/repos/Liberty-Emporium/echo-v1" | grep -E '"updated_at"|"pushed_at"'
curl -s "https://api.github.com/repos/Liberty-Emporium/Agent-Z" | grep -E '"updated_at"|"pushed_at"'
```

### Step 2: Check GitLab Backup
```bash
# Check GitLab mirror status
# Use GLAB_TOKEN environment variable or token from EcDash credentials

curl -s "https://gitlab.com/api/v4/projects?private_token=$GLAB_TOKEN" | grep -E '"name"|"last_activity_at"'
```

### Step 3: Verify Sync
- Compare GitHub push timestamp vs GitLab last activity
- Look for repos that haven't synced
- Check for any backup failures in logs

### Step 4: Report
```
🔄 BACKUP STATUS

GitHub Primary:
  ✅ echo-v1 — Last push: 2026-05-04T12:30:00Z
  ✅ Agent-Z — Last push: 2026-05-03T18:45:00Z

GitLab Mirror:
  ✅ echo-v1 — Last activity: 2026-05-04T12:32:00Z (synced)
  ⚠️ Agent-Z — Last activity: 2026-05-01T (7 days old, needs sync)
  ❌ unknown-repo — Not found in GitLab

Action Required:
  - Push Agent-Z to GitLab
  - Verify sweet-spot-cakes backup
```

## Quick Commands
```bash
# Sync a repo to GitLab (from repo directory)
git push gitlab main

# Check GitHub repos
gh repo list Liberty-Emporium --json name,pushedAt --limit 10
```

## Related
- `memory-sync` — Sync memory files to backup
- `rollback-ready` — Restore from backup if needed

---
*Tool: backup-verify v1.0 — Built for Liberty-Emporium by Echo (KiloClaw)*