# saas_core.py — Liberty Emporium Multi-Tenant SaaS Blueprint

Drop this one file into any Flask app and instantly get full multi-tenant SaaS architecture.

## What You Get

- ✅ Multi-tenant data isolation (per-slug directories under /data/customers/)
- ✅ Trial signup wizard (/wizard + /start-trial)
- ✅ Admin overseer panel (/overseer — CRUD, impersonate, suspend, delete)
- ✅ Per-tenant user authentication
- ✅ Admin auth (separate from tenant users)
- ✅ Persistent /data storage with local fallback
- ✅ Duplicate email protection
- ✅ Lead tracking (leads.json)
- ✅ MRR calculation in overseer

## Setup (5 minutes)

### 1. Copy the file
```bash
cp saas_core.py /path/to/your/app/saas_core.py
```

### 2. Update app.py
```python
from flask import Flask, render_template, session, redirect, url_for
from saas_core import SaaSCore

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Initialize SaaSCore
core = SaaSCore(
    app,
    app_name="Your App Name",
    monthly_price=99.00,      # your monthly price
    trial_days=14             # trial length
)

# Use core decorators on your routes
@app.route('/dashboard')
@core.login_required
def dashboard():
    slug = core.active_slug()
    # load tenant-scoped data:
    # data = load_json(core.data_path('mydata.json', slug))
    return render_template('dashboard.html', **core.ctx())
```

### 3. Create 3 templates

**templates/login.html** — login form with `username` + `password` fields, POST to `/login`

**templates/wizard.html** — trial signup with:
- `store_name` (required)
- `contact_email` (required)  
- `contact_name` (optional)
- `extra_field` (optional — niche/specialty/city/etc.)
POST to `/start-trial`

**templates/overseer.html** — admin panel with access to:
- `stores` list (all tenants)
- `leads` list
- `active_count`, `suspended_count`, `mrr`, `monthly_price`

**templates/account.html** — account settings with two forms:
- Change password: `current_password`, `new_password`, `action=change_password`
- Change username: `current_password`, `new_username`, `action=change_username`
- Both POST to `/account`

**templates/forgot_password.html** — email input, POST to `/forgot-password`

**templates/reset_password.html** — receives `token` + `email` context, `password` field POST to `/reset-password/<token>`

## Data Structure

```
/data/
  saas_core.db          ← admin auth
  leads.json            ← trial signups
  customers/
    store-slug-1/
      config.json       ← store name, email, plan, trial dates
      users.json        ← per-store user accounts  
      orders.json       ← your app's data (any files you want)
      products.json
    store-slug-2/
      ...
```

## Core Methods

```python
core.active_slug()              # current tenant slug (impersonation-aware)
core.tenant_dir(slug)           # /data/customers/slug/ (creates if needed)
core.data_path('file.json', slug)  # full path to tenant data file
core.load_client_config(slug)   # dict with store_name, plan, status, etc.
core.save_client_config(slug, cfg)
core.list_client_stores()       # list of all tenant configs
core.ctx()                      # template context dict
core.login_required             # decorator
core.admin_required             # decorator
```

## Routes Added Automatically

| Method | Path | Description |
|--------|------|-------------|
| GET/POST | `/login` | Login (admin + tenant) |
| GET | `/logout` | Clear session |
| GET | `/wizard` | Trial signup form |
| POST | `/start-trial` | Create new tenant |
| GET/POST | `/account` | Change username + password |
| GET/POST | `/forgot-password` | Request password reset by email |
| GET/POST | `/reset-password/<token>` | Set new password via token |
| GET | `/overseer` | Admin panel |
| POST | `/overseer/client/create` | Create client manually |
| POST | `/overseer/client/<slug>/impersonate` | Manage as client |
| GET | `/overseer/exit` | Exit impersonation |
| POST | `/overseer/client/<slug>/suspend` | Toggle suspend |
| POST | `/overseer/client/<slug>/delete` | Delete client |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATA_DIR` | `/data` | Data directory (Railway volume mount) |
| `ADMIN_USER` | `admin` | Admin username |
| `ADMIN_PASSWORD` | `admin1` | Admin password |
| `SECRET_KEY` | (required) | Flask secret key |

## Full Example App

See `example_app.py` for a complete working app using saas_core.

---
*Built by Echo · Liberty Emporium · April 2026*
