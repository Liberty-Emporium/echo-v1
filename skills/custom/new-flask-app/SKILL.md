# new-flask-app

Scaffold a full Liberty-Emporium Flask app with all standard building blocks in one shot.

## When to use
- Jay says "build a new app for X"
- Starting any new SaaS product

## Standard stack (always included)
From TOOL_LIBRARY.md — use trigger phrases to activate each:

### Always included (no need to ask):
- Dark theme base template (#21)
- Toast notifications (#22)
- Health endpoint (#18)
- WAL mode SQLite (#15)
- Persistent volume at /data (#16)
- Railway deploy config (#25)
- Security headers (#28)
- bcrypt password hashing (#29)
- Global error handlers (#30)
- Structured logging (#20)
- SEO package (#26)
- Rate limiter (#10)

### Add when specified:
- Multi-tenant auth (#7) — "Make it multi-tenant" / "SaaS auth"
- Single-tenant auth (#6) — "basic auth" / "single user login"
- Trial system (#9) — "free trial" / "14-day trial"
- Stripe billing (#13) — "add Stripe" / "add payments"
- Overseer panel (#11) — "admin dashboard for all customers"
- AI chat widget (#3) — "add AI chat" / "add a chat assistant"
- Image analyzer (#2) — "Photo to listing" / "Add Image AI"
- Plan enforcement (#14) — "Add plan limits"
- Stats dashboard (#23) — "Add stat boxes"
- Landing page with pricing (#24) — "Add a landing page"
- Email onboarding (#27) — "Add email drip"

## File structure
```
app-name/
  app.py          — main Flask app
  requirements.txt
  Procfile
  railway.json
  templates/
    base.html
    landing.html
    dashboard.html
    login.html
    signup.html
    ...
```

## Railway deployment checklist
1. Create GitHub repo under Liberty-Emporium
2. Push code
3. Create Railway project from GitHub repo
4. Add volume → mount at /data
5. Set env vars: SECRET_KEY, OPENROUTER_API_KEY (if AI), STRIPE_* (if billing)
6. Verify /health returns {"status":"ok","db":"ok"}
7. Push to GitLab backup

## Critical: Password fields
EVERY password field needs eye toggle (👁️/🙈). Non-negotiable per Jay's rules.
