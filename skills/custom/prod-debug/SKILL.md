---
name: prod-debug
description: Debug issues in production environments. Use when you need to: fix live broken apps, read production logs, diagnose deployed issues.
---

# Prod Debug

## Quick Diagnosis

1. **Check logs first**
```bash
railway logs --num 50
heroku logs --tail
```

2. **Check recent deploys**
```bash
git log --oneline -10
heroku releases
```

3. **Check environment**
```bash
railway variables
heroku config
```

## Common Errors

| Error | Fix |
|-------|-----|
| 500 | Check logs for traceback |
| 404 | Route missing or typo |
| Timeout | Slow query or external API |
| CORS | Add CORS headers |

## Debug Flow

1. Get status code
2. Read error from logs
3. Find relevant code
4. Add logging
5. Deploy test fix
6. Verify

## Safe Changes

- Add logging (safe)
- Check env vars (safe)
- Rollback version (safe)

## Emergency Rollback

```bash
heroku releases:rollback v123
railway status
```