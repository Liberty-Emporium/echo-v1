---
name: flask-app-builder
description: >-
  Build, audit, secure, test, and improve Flask web apps in the Liberty-Emporium portfolio.
  Use when creating a new Flask SaaS app from scratch, adding a feature to an existing app
  (orders, auth, payments, AI chat, reports), running a security audit, fixing bugs, making
  an app mobile-friendly, writing Playwright tests, or deploying to Railway. Triggers on
  phrases like "build a new app", "add a feature to", "fix a bug in", "run tests on",
  "audit", "secure", "make mobile", "deploy to Railway", or any reference to a specific
  Liberty-Emporium app such as FloodClaim, AI Widget, EcDash, Pet Vet, Contractor Pro,
  Sweet Spot, Dropship, Consignment, Inventory, or Liberty Oil.
---

# Flask App Builder

Echo's primary skill for building and maintaining Liberty-Emporium Flask apps.

## Stack

All apps share the same pattern:
- **Backend:** Python 3.11 + Flask + SQLite (via Railway volume at `/data`)
- **Auth:** bcrypt passwords + Flask sessions + CSRF protection
- **Frontend:** Jinja2 templates, Inter font, dark navy/indigo color system
- **Hosting:** Railway (auto-deploy on `git push`)
- **AI:** OpenRouter API (model picker in settings)
- **Payments:** Stripe (optional, in requirements)

## App Registry

See `references/app-registry.md` for all app URLs, credentials, repo names, and Railway deployment IDs.

## Creating a New App

1. Clone the template pattern from `references/app-template.md`
2. Replace placeholder names, colors, routes
3. Add app-specific DB tables and routes
4. Push to GitHub → Railway auto-deploys
5. Add to EcDash dashboard (projects + daily summary)
6. Write Playwright tests with `scripts/gen_playwright_test.py`

## Standard App Structure

Every app must have:
```
app.py          — single-file Flask app
requirements.txt — flask, gunicorn, bcrypt, requests (+ app-specific)
Procfile        — web: gunicorn app:app
railway.json    — healthcheckPath: /health
templates/
  base.html     — sidebar layout, mobile-first CSS, security headers
  login.html    — bcrypt login with rate limiting + CSRF
```

## Security Checklist (apply to every app)

Run `scripts/security_audit.py <app_path>` to auto-check. Manual checklist:

- [ ] `debug=False` in `app.run()`
- [ ] `bcrypt` for password hashing (not SHA-256/MD5)
- [ ] Login rate limiting: `is_rate_limited(f'login:{ip}', 5, 60)`
- [ ] CSRF: `_get_csrf_token()` + `_validate_csrf()` + `@csrf_required` on POST routes
- [ ] Security headers `@app.after_request`: X-Frame-Options, X-Content-Type-Options, CSP, Referrer-Policy, Permissions-Policy
- [ ] `SESSION_COOKIE_HTTPONLY = True`, `SESSION_COOKIE_SAMESITE = 'Lax'`
- [ ] No secrets in code — all via `os.environ.get()`
- [ ] Parameterized SQL — never f-strings in queries

See `references/security-patterns.md` for copy-paste code blocks for all of the above.

## Mobile-First Checklist (apply to every template)

- [ ] `html,body { overflow-x: hidden; max-width: 100%; }` — no horizontal scroll
- [ ] `<meta name="viewport" content="width=device-width,initial-scale=1">`
- [ ] `input, select, textarea { font-size: 16px !important; }` — prevents iOS zoom
- [ ] `img { max-width: 100%; height: auto; }`
- [ ] Tables: `@media(max-width:768px){ table { display:block; overflow-x:auto; } }`
- [ ] `form-row` grids collapse to `1fr` at ≤768px
- [ ] Touch targets ≥ 44×44px

## Running Playwright Tests

```bash
# Run existing Sweet Spot test
python3 echo-v1/scripts/test_sweet_spot.py

# Generate a new test for any app
python3 echo-v1/scripts/gen_playwright_test.py <app_name> <base_url> <email> <password>
```

See `references/playwright-patterns.md` for test patterns (login, form submit, mobile overflow check, health check).

## Deploying to Railway

```bash
cd /root/.openclaw/workspace/<repo>
git add -A && git commit -m "feat: <description>"
git push origin main      # triggers Railway auto-deploy
git push gitlab main      # GitLab backup

# Check deploy status
railway status
```

Railway reads `Procfile` for the start command. Health check hits `/health` — always keep that route returning `{"status":"ok"}`.

## Adding Features — Common Patterns

See `references/feature-patterns.md` for copy-paste patterns:
- AI chat endpoint (OpenRouter)
- Stripe checkout + webhook
- File upload with validation
- Email via SendGrid
- Willie AI widget integration
- KYS API key fetching
- EcDash bridge task posting
- Cron job / scheduled task

## After Any Session

1. Update `echo-v1/memory/YYYY-MM-DD.md`
2. Add card to EcDash Daily Summary (`jay-portfolio/templates/dashboard.html` → `#panel-daily`)
3. Push echo-v1 brain: `git push origin main && git push gitlab main`
