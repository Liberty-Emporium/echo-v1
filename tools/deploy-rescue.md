# Tool: deploy-rescue
**Type:** Diagnostic & Recovery
**Use when:** Railway deployment fails, app crashes on boot, worker won't start
**Trigger phrases:** "Railway is down", "App crashed on deploy", "Fix deployment", "Deploy rescue"

## What It Does
Systematically diagnose and fix Railway deployment issues for Flask/SQLite apps.

## How To Use

### Step 1: Capture Error
Get full error from Railway logs (`railway logs`) or user description.

Watch for patterns:
- `NameError` → undefined function/variable
- `sqlite3.OperationalError: no such column` → missing migration
- `HaltServer 'Worker failed to boot'` → fatal startup error
- Template/CSS issues → class spacing problems

### Step 2: Identify Root Cause
| Error | Fix |
|-------|-----|
| NameError on boot | Move `_run_migrations()` definition BEFORE `init_db()` calls it |
| No such column | Add `ALTER TABLE ADD COLUMN` in `_run_migrations()`, wrapped in try/except |
| No such table | Check query uses correct table name |
| Worker boot failed | Check imports, DB init, syntax errors |

### Step 3: Apply Fix
```bash
cd /a0/usr/workdir/<project>
# Edit the file
git add -A && git commit -m "Fix: <description>"
git push origin main
```

### Step 4: Verify
```bash
railway status
curl -I https://<app>.up.railway.app | head -1
```

### Step 5: Log
Document the fix in memory/deploy-recovery.md

## Quick Commands
```bash
# Check recent commits
git log --oneline -5

# View Railway logs
railway logs

# Check what's modified
git status --short
```

## Related
- `railway-pulse` — Check deployment health
- `debug-trace` — Systematic debugging
- `rollback-ready` — Revert to last good version

---
*Tool: deploy-rescue v1.0 — Built from Agent-Z/skills by Echo (KiloClaw)*