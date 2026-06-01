# FloodClaims Pro — App Operations & Monitoring Skill

> Complete reference for maintaining all Liberty Emporium Railway apps, deployment, monitoring, and incident response.

## All Deployed Apps (Railway)

### Active (200 OK)
| App | URL | Repo |
|-----|-----|------|
| FloodClaims Pro | billy-floods.up.railway.app | alexander-ai-floodclaim |
| Portfolio (EcDash) | jay-portfolio-production.up.railway.app | jay-portfolio |
| AI Agent Widget | ai-agent-widget-production.up.railway.app | ai-agent-widget |
| Liberty Thrift | liberty-thrift-store.up.railway.app | liberty-thrift-store |
| Pet Vet AI | pet-vet-ai-production.up.railway.app | pet-vet-ai |
| Sweet Spot Cakes | sweet-spot-cakes.up.railway.app | sweet-spot-cakes |
| Contractor Pro | contractor-pro-production.up.railway.app | contractor-pro |
| Inventory | inventory-production.up.railway.app | inventory-app |
| Drop Shipping | drop-shipping-production.up.railway.app | drop-shipping |
| Remote Repair | remote-repair-services-production.up.railway.app | remote-repair-services |
| Luxury Rentals | luxury-rentals-production.up.railway.app | luxury-rentals |
| Agents | agents-production.up.railway.app | agents |

### Down (Need Fixing)
| App | URL | Issue |
|-----|-----|-------|
| GymForge | gymforge.up.railway.app | CRASHING |
| My-AI | my-ai-production.up.railway.app | FAILED |
| Course | course-production.up.railway.app | 404 |
| Extra Mile Photography | extra-mile-photography-production.up.railway.app | 404 |
| Consignment Solutions | consignment-solutions-production.up.railway.app | 404 |
| Liberty Oil | liberty-oil-propane.up.railway.app | 404 |
| KYS | ai-api-tracker-production.up.railway.app | 404 |

## Deployment Pattern

### Every Code Change MUST:
1. Test locally: `cd /home/mingo/workspace/<repo> && python3 -c "import app; app.app"`
2. Commit: `git add -A && git commit -m "description"`
3. Push to GitHub: `git push origin main`
4. Push to GitLab: `git push gitlab main`
5. Verify Railway auto-deploy (2-3 minutes)
6. Check live site: `curl -s -o /dev/null -w "%{http_code}" <url>`

### Git Remotes
- **GitHub**: `git@github.com:Liberty-Emporium/<repo>.git` (SSH — no token needed)
- **GitLab**: `https://oauth2:<PAT>@gitlab.com/Liberty-Emporium/<repo>.git`

## Database Pattern (SQLite)

### Migration Style
All migrations use `_migrate_<feature>()` functions called at app startup:
```python
def _migrate_feature_x():
    db = sqlite3.connect(DB_PATH)
    try:
        db.executescript('''
            CREATE TABLE IF NOT EXISTS new_table (...);
        ''')
        # Add columns to existing tables
        cols = [row[1] for row in db.execute('PRAGMA table_info(existing_table)').fetchall()]
        if 'new_col' not in cols:
            db.execute('ALTER TABLE existing_table ADD COLUMN new_col TEXT DEFAULT ""')
        db.commit()
    except Exception as e:
        print(f'Migration error: {e}')
    finally:
        db.close()

_migrate_feature_x()  # Call at module level
```

### Key Rules
- Always use `IF NOT EXISTS` for tables
- Check `PRAGMA table_info` before adding columns
- Use `try/except` — never let migrations crash the app
- Close DB connections in `finally` block
- Store all monetary values in cents (integers)

## Security Checklist (Every Deploy)

1. **Session cookies**: Secure flag ✅, HttpOnly ✅, SameSite=Lax
2. **CSP headers**: No `unsafe-inline` or `unsafe-eval` in production
3. **HSTS**: Strict-Transport-Security header
4. **CSRF**: `@csrf_required` on all POST routes
5. **Rate limiting**: On login (5 attempts/min), API endpoints
6. **Input validation**: All user input sanitized before DB
7. **No secrets in code**: Use environment variables only
8. **SQL injection**: Use parameterized queries only (never f-strings)
9. **XSS**: Escape all user-generated content in templates

## Incident Response

### App Down (502/503/CRASHING)
1. Check Railway dashboard → deploy logs
2. If build failed → check requirements.txt, Procfile, Dockerfile
3. If runtime crash → check error logs for Python traceback
4. Common fixes:
   - `ModuleNotFoundError` → add to requirements.txt
   - `Address already in use` → check PORT env var
   - `sqlite3.OperationalError` → run migration manually
5. Railway deploy logs: `railway logs --env production`

### Database Corruption
1. Download DB from Railway
2. Fix locally with sqlite3 CLI
3. Re-upload (careful — only for schema changes, not data loss)

### Secret Rotation
1. Update in Railway dashboard → Variables
2. No code change needed if using `os.environ.get()`

## Monitoring

### Health Check Endpoint
Every app should have:
```python
@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'timestamp': datetime.utcnow().isoformat()})
```

### Cron Jobs (Echo-v1-brain)
- Brain backup: every 40 min → GitLab
- Uptime monitor: ping all apps
- Comms health: check message bus
- Archive manager: clean old messages

## Key Environment Variables
| Variable | Purpose | Set In |
|----------|---------|--------|
| ADMIN_EMAIL | Admin login email | Railway |
| ADMIN_PASSWORD | Admin login password | Railway |
| STRIPE_SECRET_KEY | Stripe API | Railway |
| STRIPE_PUBLISHABLE_KEY | Stripe frontend | Railway |
| SENDGRID_API_KEY | Email sending | Railway |
| OPENROUTER_API_KEY | AI chat/vision | Railway |
| RAILWAY_TOKEN | Railway API | Bull's local |

## Git Workflow
1. All changes go to `/home/mingo/workspace/<repo>/`
2. Work on `main` branch only (no feature branches)
3. Commit messages:Verb + description (e.g., "Fix emoji grid CSS")
4. Push to both remotes immediately
5. Never force push to GitHub (branch protection)
6. GitLab is backup — can force push if needed
