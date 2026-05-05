# Skill: railway-deploy-fix

## Purpose
Diagnose and fix Railway deployment failures and hangs.

## Trigger Phrases
- "Railway is hanging", "App won't start on Railway"
- "Railway build stuck", "Container won't start"
- "Fix Railway deployment", "Debug Railway"
- "Dockerfile VOLUME error", "Railway volume issue"

## When to Use
- Railway deployment shows "Processing" for too long (>5 min)
- App starts but hangs (never responds)
- Build succeeds but app doesn't work
- "VOLUME instruction not supported" error

## Steps

### Step 1: Check Basic Connectivity
```bash
# Can you reach the Railway API?
curl -s "https://railway.app/api/v2/projects" -H "Authorization: Bearer $RAILWAY_TOKEN"
```

### Step 2: Common Dockerfile Fixes

**Problem: `VOLUME at Line X is not supported`**
```dockerfile
# BEFORE (breaks Railway)
VOLUME ["/data"]

# AFTER (Railway uses managed volumes)
# Remove the VOLUME instruction entirely
EXPOSE 3000
```

**Problem: Missing build step**
```dockerfile
# BEFORE
RUN bun install
# App bundle may not exist!

# AFTER — ensure build step exists
RUN bun install && bun run build:server
```

**Problem: Wrong start command**
```dockerfile
# Confirm the server bundle exists
RUN ls dist-server/server.mjs  # should exist after build
```

### Step 3: Add Startup Diagnostics
Add step-by-step logging to `server.ts`:
```typescript
console.log('[Alexander AI] Step 1/5: initStorage()...');
await initStorage();
console.log('[Alexander AI] Step 1/5: DONE');

console.log('[Alexander AI] Step 2/5: ExtensionRegistry.initialize()...');
// ... continue for each step
```

This tells you exactly where startup hangs on Railway.

### Step 4: Trigger Redeploy
```bash
# Push an empty commit to trigger GitHub webhook rebuild
git commit --allow-empty -m "chore: trigger Railway redeploy"
git push origin main

# OR use Railway CLI
railway up

# OR disable/enable the service in Railway dashboard
```

### Step 5: Check Railway Logs
```bash
railway logs --project=PROJECT_ID --service=SERVICE_ID
```

### Step 6: Check GitHub Actions (if using GitHub integration)
```bash
gh run list --repo OWNER/REPO --limit=5
gh run view RUN_ID --log  # to see build output
```

## Common Railway Fixes

| Problem | Fix |
|---------|-----|
| `VOLUME not supported` | Remove `VOLUME` instruction from Dockerfile |
| Hangs during startup | Add `DATA_DIR=/data` env var + step logging |
| Missing env vars | Add `ADMIN_PASSWORD`, `ALLOW_REMOTE=true` etc. |
| Database wiped on redeploy | Add Railway Volume at `/data` |
| Build not triggering | Push empty commit or use `railway up` |
| Port mismatch | Ensure `ENV PORT=3000` and app listens on `PORT` env var |

## Key Environment Variables for Bun/Web Apps
```bash
PORT=3000                    # Railway port
NODE_ENV=production         # Enable production mode
ALLOW_REMOTE=true           # Allow external access
DATA_DIR=/data              # Persistent storage (if volume added)
ADMIN_PASSWORD=YourPass123  # Set fixed admin password
```

## When All Else Fails
1. Check Railway status page: https://railway.statuspage.io
2. Check GitHub Actions for upstream repo issues
3. Try `railway doctor` to diagnose CLI issues
4. Delete the project and redeploy fresh

## Related Skills
- `branding-rebrand-app` — for applying branding before deployment
- `github-actions-build` — for building desktop installers