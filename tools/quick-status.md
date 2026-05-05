# Tool: quick-status
**Type:** Health Check
**Use when:** Starting session, checking if anything is down, routine check
**Trigger phrases:** "Quick status", "What's down?", "Health check", "Status of services"

## What It Does
Fast health check of all Liberty-Emporium services. Returns green/yellow/red status for each app.

## How To Use

### Step 1: Check Railway Status
```bash
railway status
```

### Step 2: Check Each Known App
Based on memory, check these known services:
- EcDash (control plane)
- Echo-v1 (me/brain)
- Agent-Z (deployment agent)
- Any other Liberty-Emporium apps

### Step 3: Report Status
```
✅ EcDash — UP
✅ Echo — UP  
✅ Agent-Z — UP
⚠️ sweet-spot-cakes — DEGRADED (CSS glitch)
❌ unknown-app — DOWN
```

## Quick Commands
```bash
# Check Railway status
railway status

# Check deployment logs
railway logs --tail 20

# Check if URL responds
curl -s -o /dev/null -w "%{http_code}" https://<app>.up.railway.app
```

## Related
- `railway-pulse` — Deeper Railway diagnostics
- `deploy-rescue` — Fix issues found

---
*Tool: quick-status v1.0 — Inspired by Agent-Z by Echo (KiloClaw)*