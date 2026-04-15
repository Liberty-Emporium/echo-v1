# saas-core

**Version:** 1.0.0
**Created:** 2026-04-14
**Author:** Echo

## Description

Drop-in multi-tenant SaaS blueprint for Flask apps. Distilled from Liberty Inventory, Dropship Shipping, and Contractor Pro AI. Add full multi-tenant architecture to any new Flask app in under 5 minutes.

## What It Provides

- Multi-tenant data isolation (per-slug directories)
- Trial signup wizard (/wizard)
- Admin overseer panel (/overseer)
- Per-tenant + admin authentication
- Persistent /data storage with fallback
- Duplicate email protection
- Lead tracking
- MRR calculation

## File Location

```
/root/.openclaw/workspace/saas_core/saas_core.py
/root/.openclaw/workspace/saas_core/README.md
/root/.openclaw/workspace/saas_core/example_app.py
```

## 🚨 HARD RULES — NEVER BREAK THESE

### SECRET_KEY — Sessions Must Survive Restarts
**NEVER do this:**
```python
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))  # ❌ BROKEN
app.secret_key = 'hardcoded-string'  # ❌ INSECURE
```
A random fallback key means every Railway restart wipes all user sessions. The nav breaks, users get logged out, and it's invisible in testing.

**ALWAYS do this:**
```python
from saas_core import SaaSCore, get_secret_key
app.secret_key = get_secret_key()  # ✅ checks env var, then persists to /data
```
`get_secret_key()` checks `SECRET_KEY` env var first. If not set, it writes a stable key to `/data/secret_key` and reuses it forever. Sessions survive restarts.

**Also tell Jay:** Add `SECRET_KEY=<random-string>` to Railway env vars as the proper production fix.

### ⚙️ Settings Gear — ALWAYS in the Nav
Every app **must** have a gear icon in the nav bar linking to `/settings`.
Users need access to their API keys and preferences from anywhere in the app.

**In base.html (or any nav template) — before Logout:**
```html
<a href="{{ url_for('settings') }}" title="Settings" 
   style="padding:6px 8px;font-size:1.1rem;line-height:1" 
   aria-label="Settings">&#9881;</a>
```
- Use `&#9881;` (⚙) — works without icon libraries
- Place it just before Logout
- Muted color, hover effect matches other nav links
- The settings page must include at minimum: OpenRouter API key field

### /data — All State Lives Here
- DB files → `/data/appname.db`
- Uploads → `/data/uploads/`
- Secret key → `/data/secret_key` (auto-managed by get_secret_key)
- **Never** write state to the app directory — Railway wipes it on deploy

### Default Admin Account
- Always create: `admin` / `admin1` on first boot
- Jay needs it to log in on fresh deploys

### Push to GitHub After Every Change
- Meaningful commit messages only (no "fix" or "updates")
- Always push to GitLab backup after GitHub push

---

## Quickstart

```python
from flask import Flask
from saas_core import SaaSCore, get_secret_key

app = Flask(__name__)
app.secret_key = get_secret_key()  # stable across Railway restarts

core = SaaSCore(
    app,
    app_name="Your App",
    monthly_price=99.00,
    trial_days=14,
    dashboard_endpoint='dashboard'  # your dashboard route name
)

@app.route('/dashboard')
@core.login_required
def dashboard():
    slug = core.active_slug()
    data = load_json(core.data_path('mydata.json', slug))
    return render_template('dashboard.html', **core.ctx())
```

## Required Templates

Create these 3 templates (forms POST to the listed endpoints):
- `login.html` → POST `/login` with `username` + `password`
- `wizard.html` → POST `/start-trial` with `store_name`, `contact_email`, `contact_name`, `extra_field`
- `overseer.html` → receives `stores`, `leads`, `active_count`, `mrr`, `monthly_price`

## Key Methods

```python
core.active_slug()                    # current tenant (impersonation-aware)
core.data_path('file.json', slug)     # scoped file path
core.load_client_config(slug)         # tenant config dict
core.list_client_stores()             # all tenants
core.ctx()                            # template context
core.login_required                   # decorator
core.admin_required                   # decorator
```

## Tested: 8/8 unit tests pass ✅

## Admin Login
- URL: /overseer
- Username: `admin` (or ADMIN_USER env var)
- Password: `admin1` (or ADMIN_PASSWORD env var)

## Pricing Reference (Jay's Apps)
- Liberty Inventory: $99 startup + $20/mo
- Dropship Shipping: $299 startup
- Consignment Solutions: $69.95 startup + $20/mo
- Contractor Pro AI: $99/mo
- Pet Vet AI: $9.99/mo
- Andy Keep Your Secrets: $14.99/mo
