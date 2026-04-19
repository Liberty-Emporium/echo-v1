# railway-deploy

Deploy any Liberty-Emporium app to Railway and verify it's live.

## When to use
- Any time Jay says "deploy this", "push to Railway", "get it live"
- After pushing code to GitHub and needing Railway to pick it up
- Verifying a Railway app is healthy after deploy

## Steps

### 1. Verify GitHub is up to date
```bash
cd /root/.openclaw/workspace/<REPO>
git status
git push origin main
```

### 2. Trigger Railway deploy (via GitHub push)
Railway auto-deploys on push to main. Wait ~60-90 seconds.

### 3. Verify health
```bash
curl -s https://<APP_URL>/health
```
Expected: `{"status":"ok","db":"ok"}`

### 4. Check key routes
```bash
curl -s -o /dev/null -w "%{http_code}" https://<APP_URL>/
curl -s -o /dev/null -w "%{http_code}" https://<APP_URL>/login
```

## Railway env vars required for new apps
- `SECRET_KEY` — random hex string
- `RAILWAY_VOLUME_MOUNT_PATH` — set to `/data` (add volume in Railway UI first)
- App-specific vars (OPENROUTER_API_KEY, STRIPE_*, etc.)

## Grace App specific
- Repo: https://github.com/Liberty-Emporium/grace-app
- Required env vars: USER_NAME, CAREGIVER_PIN, OPENROUTER_API_KEY, SECRET_KEY
- Volume mount: /data
- URL: (set after Railway creates it)

## Known Railway URLs
| App | URL |
|-----|-----|
| AI Agent Widget | https://ai-agent-widget-production.up.railway.app |
| Contractor Pro AI | https://contractor-pro-ai-production.up.railway.app |
| Pet Vet AI | https://pet-vet-ai-production.up.railway.app |
| Keep Your Secrets | https://ai-api-tracker-production.up.railway.app |
| Liberty Inventory | https://liberty-emporium-inventory-demo-app-production.up.railway.app |
| Dropship Shipping | https://dropship-shipping-production.up.railway.app |
| Jay Portfolio | https://jay-portfolio-production.up.railway.app |
| Consignment Solutions | https://web-production-43ce4.up.railway.app |
| Grace App | https://moms-ai-helper.up.railway.app |

## Critical Rules
1. Always check branch — jay-portfolio uses `master`, all others use `main`
2. Always verify /health returns 200 before declaring done
3. If health fails after 90s, check Railway logs
4. Never push without syntax check: `python3 -c "import ast; ast.parse(open('app.py').read())"`
