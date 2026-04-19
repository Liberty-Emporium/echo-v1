# Session Startup Checklist & Decision Tree

## Full Decision Tree

```
START
 │
 ├─ Run check-startup-health.sh
 │   ├─ GitHub token missing? → Ask Jay for new PAT → save to /root/.secrets/github_token
 │   ├─ echo-v1 not cloned? → Clone from GitHub (or GitLab fallback)
 │   └─ All clear? → Continue
 │
 ├─ Run restore-brain.sh
 │   ├─ GitHub fetch succeeds? → Brain synced ✅
 │   ├─ GitHub fails, GitLab available? → Fallback restore from GitLab ✅
 │   └─ Both fail? → Work from local files, warn Jay, fix tokens
 │
 ├─ Read MEMORY.md (main session only)
 ├─ Read memory/YYYY-MM-DD.md (today)
 ├─ Read memory/YYYY-MM-DD.md (yesterday, if today empty)
 │
 ├─ Run todo_manager.py list --status open
 │   └─ High priority items? → Surface immediately to Jay
 │
 └─ Report readiness → Begin work
```

## What to Include in Startup Summary

**Always include:**
- Brain sync status (last commit date/time)
- Any blocking issues (missing tokens, clone failures)

**Include if present:**
- High-priority open todos
- Anything flagged in yesterday's diary as "next session" priorities
- Upcoming calendar events (if Jay has integrated calendar)

**Skip:**
- Medium/low todos unless Jay asks
- Full memory dump
- Technical details of the restore process unless something failed

## Token Rotation Workflow

When Jay provides a new GitHub token:
```bash
echo "ghp_NEWTOKEN" > /root/.secrets/github_token
chmod 600 /root/.secrets/github_token
# Update the remote URL in echo-v1
cd /root/.openclaw/workspace/echo-v1
NEW_TOKEN=$(cat /root/.secrets/github_token)
git remote set-url origin "https://$NEW_TOKEN@github.com/Liberty-Emporium/echo-v1.git"
echo "✅ Token rotated"
```

Then test it:
```bash
git ls-remote origin HEAD
```

## Never Do These

- ❌ Store raw token values in MEMORY.md, USER.md, or any file that gets committed
- ❌ Log tokens to the console in a way that might be captured
- ❌ Skip the health check and go straight to restore-brain.sh
- ❌ Force push to GitLab without unprotecting first (use the API)
- ❌ Push to GitHub with raw credentials in tracked files (secret scanning will block it)

## File Locations Reference

| File | Purpose |
|---|---|
| `/root/.secrets/github_token` | GitHub PAT — Liberty-Emporium org |
| `/root/.secrets/gitlab_token` | GitLab PAT — backup mirror |
| `/root/.secrets/kys_api_token` | Keep Your Secrets — brain encryption key |
| `/root/.openclaw/workspace/echo-v1/` | Brain repo (cloned) |
| `/root/.openclaw/workspace/memory/` | Daily diary files |
| `/root/.openclaw/workspace/MEMORY.md` | Long-term curated memory |
| `/root/.openclaw/workspace/memory/todos.json` | Structured TODO tracker |
