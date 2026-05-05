# Skill: rollback-ready
**Type:** Recovery
**Use when:** Production is broken and you need to revert FAST
**Trigger phrases:** "Undo last push", "Rollback to working version", "Site is broken", "Revert now", "Emergency rollback"

## What It Does
Revert broken deployments in under 60 seconds. Speed beats elegance in downtime.

## How To Use

### Step 1: Tag Current State (Never Lose Broken State)
```bash
cd /a0/usr/workdir/<project>
git tag broken-$(date +%Y%m%d-%H%M%S)
```

### Step 2: Revert Fast
```bash
# Option A: Revert last commit (keeps history, safer)
git revert --no-edit HEAD
git push origin main

# Option B: Hard reset to known good commit (nuclear)
git reset --hard <commit-hash>
git push --force-with-lease origin main
```

### Step 3: Verify Recovery
```bash
railway status
curl -I https://<app>.up.railway.app | head -1
```

### Step 4: Fix Forward Safely
```bash
# Create feature branch from last good commit
git checkout -b fix-broken-feature <commit-hash>
# Fix locally, test, then merge to main
```

## Rules
1. **Revert first, investigate second** — Speed beats elegance in downtime
2. **Always git tag before hard reset** — Never lose the broken state
3. **Never force-push shared branches** — Use force-with-lease
4. **Test on Railway preview if possible** — Before merging to main
5. **Log what happened** — In memory/YYYY-MM-DD.md for later analysis

## Quick Commands
```bash
# One-liner revert
git revert --no-edit HEAD && git push origin main

# Tag, reset, push (with tag for debugging)
git tag broken-$(date +%Y%m%d-%H%M%S) && git reset --hard HEAD~1 && git push --force-with-lease origin main
```

## Related
- `deploy-rescue` — Debug why deployment broke
- `db-migrate` — Safe schema changes prevent rollbacks

---
*Skill: rollback-ready v1.0 — Absorbed from Agent-Z, enhanced by Echo (KiloClaw)*