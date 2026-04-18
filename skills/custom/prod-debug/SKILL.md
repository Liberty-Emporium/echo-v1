---
name: prod-debug
description: Debug issues in production Railway-deployed Flask apps. Use when you need to fix live broken apps, read logs, diagnose 502/500 errors, check env vars, or rollback.
---

# prod-debug

**Version:** 2.0.0
**Updated:** 2026-04-18
**Author:** Echo

## Jay's App URLs (Quick Reference)

| App | URL |
|-----|-----|
| Liberty Inventory | https://liberty-emporium-and-thrift-inventory-app-production.up.railway.app |
| Dropship Shipping | https://dropship-shipping-production.up.railway.app |
| Consignment Solutions | https://web-production-43ce4.up.railway.app |
| Jay Portfolio | https://jay-portfolio-production.up.railway.app |
| Contractor Pro AI | https://contractor-pro-ai-production.up.railway.app |
| Pet Vet AI | https://pet-vet-ai-production.up.railway.app |
| Keep Your Secrets | https://ai-api-tracker-production.up.railway.app |

## Step 1 — Health Check First (Always)

```bash
URL=https://your-app.up.railway.app
curl -s -o /dev/null -w "%{http_code}" $URL/health
curl -s $URL/health
curl -s -o /dev/null -w "%{http_code}" $URL/login
```

## Step 2 — Diagnose by Status Code

| Code | Meaning | First Action |
|------|---------|--------------|
| 200 | OK | Check content for errors |
| 302 | Redirect | Check redirect target |
| 404 | Route missing | Check route names + registration |
| 429 | Rate limited | Reduce request rate |
| 500 | App crash | Read Railway logs immediately |
| 502 | App not running | Check Railway deploy status + Procfile |
| 503 | Overloaded | Check Railway usage |

## 502 Bad Gateway — Most Common Railway Issue

**Causes (in order of frequency):**
1. Missing `Procfile` → Railway doesn't know how to start app
2. Missing `requirements.txt` → Python not detected
3. App crashes on startup (import error, missing env var)
4. Wrong port — must bind to `0.0.0.0:$PORT`
5. Build failed — check Railway build logs

**Fix checklist:**
```bash
# 1. Verify these 3 files exist
cat Procfile         # must be: web: python3 app.py (or gunicorn)
cat requirements.txt # must exist with dependencies
head -5 app.py       # check PORT binding

# 2. Check PORT binding in app.py
# CORRECT:
# port = int(os.environ.get('PORT', 5000))
# app.run(host='0.0.0.0', port=port)

# 3. Push and wait 60s
git push origin main
sleep 60
curl -s -o /dev/null -w "%{http_code}" $URL/health
```

## Railway-Specific Debugging

```bash
# Check Railway env vars (via API)
RAILWAY_TOKEN=$(cat /root/.secrets/railway_token)
curl -s -H "Authorization: Bearer $RAILWAY_TOKEN" \
  https://backboard.railway.app/graphql/v2 \
  -H "Content-Type: application/json" \
  -d '{"query":"{ me { projects { edges { node { id name } } } } }"}' | python3 -m json.tool

# Health check with retries
for i in $(seq 1 8); do
  CODE=$(curl -s -o /dev/null -w "%{http_code}" $URL/health)
  echo "Attempt $i: HTTP $CODE"
  [ "$CODE" = "200" ] && echo "✅ UP" && break
  sleep 15
done
```

## 500 Internal Server Error

```bash
# 1. Check health endpoint for DB status
curl -s $URL/health | python3 -m json.tool

# 2. Test login page (usually reveals template errors)
curl -s $URL/login | grep -i "error\|traceback\|exception" | head -5

# 3. Common causes:
# - Missing env var (SECRET_KEY, DATABASE_URL, etc.)
# - DB migration not run
# - Import error in a route file
# - Jinja2 template variable undefined
```

## Common Jinja2 Template Errors

```python
# WRONG - crashes if user is None
{{ user.email }}

# RIGHT - safe access
{{ user.email if user else '' }}
{{ user.get('email', '') }}  # for dicts

# WRONG - undefined filter
{{ price | currency }}

# RIGHT - use built-in filters
{{ "%.2f" | format(price) }}
```

## DB Issues

```bash
# Check if /data is mounted (SQLite)
curl -s $URL/health
# {"status":"ok","db":"ok"} = good
# {"status":"ok","db":"error"} = DB problem

# SQLite WAL mode (add at every connection)
# conn.execute("PRAGMA journal_mode=WAL")
# conn.execute("PRAGMA foreign_keys=ON")
```

## Quick Fix → Deploy → Verify Pattern

```bash
# 1. Fix the code
# 2. Commit with meaningful message
git add -A && git commit -m "fix: describe what was broken and what was fixed"

# 3. Push (CI/CD auto-deploys)
# Note: jay-portfolio uses 'master' NOT 'main'
BRANCH=$(git branch --show-current)
git push origin $BRANCH

# 4. Wait for Railway build (60-90s)
sleep 75

# 5. Verify
curl -s -o /dev/null -w "%{http_code}" $URL/health
```

## Nuclear Option — Something Is Very Broken

```bash
# Roll back to last known good commit
git log --oneline -10
git revert HEAD  # creates new commit undoing last change
git push origin main
```
