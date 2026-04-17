# Multi-Tenant Web App Mastery — Echo's Deep Reference
**Written:** 2026-04-16 | Specific to Jay's Flask/SQLite/Railway stack

---

## Why This Matters for Jay's Apps
We run 7 SaaS products. 4 of them (Liberty Inventory, Consignment Solutions, Dropship Shipping, Contractor Pro AI) are **multi-tenant** — meaning one codebase, one deployment, many customer stores. Every bug I make in tenant isolation is a potential data leak between customers. This file is my cheat sheet to never get it wrong.

---

## The Core Principle: Every Query Gets the Tenant Filter

```python
# ❌ WRONG — leaks all tenants' data
def get_inventory():
    return load_json(INVENTORY_FILE)

# ✅ CORRECT — scoped to tenant
def get_inventory(slug):
    path = os.path.join(CUSTOMERS_DIR, slug, 'inventory.csv')
    return load_csv(path)
```

**The #1 rule:** Every data read/write must be scoped to the current tenant. No exceptions.

---

## Jay's Tenant Identification Pattern

Our apps use **slug-based tenancy** — each customer gets a unique slug (e.g. `willies-thrift`) that maps to:
- A directory: `/data/customers/{slug}/`
- Files: `inventory.csv`, `users.json`, `config.json`, `ads/`, `uploads/`
- Session key: `session['store_slug']` or `session['impersonating_slug']`

```python
def active_slug():
    """Always use this — never read slug from URL directly without validation."""
    return session.get('impersonating_slug') or session.get('store_slug')

def tenant_path(slug, *parts):
    """Safe path builder — prevents directory traversal attacks."""
    # Sanitize slug first
    clean = re.sub(r'[^a-z0-9\-]', '', slug.lower())
    base = os.path.join(CUSTOMERS_DIR, clean)
    return os.path.join(base, *parts)
```

### Security: Slug Validation
```python
import re

def validate_slug(slug):
    """Slugs must be alphanumeric + hyphens only. Prevents path traversal."""
    if not slug or not re.match(r'^[a-z0-9][a-z0-9\-]{0,60}[a-z0-9]$', slug):
        abort(400, 'Invalid store identifier')
    # Prevent reserved names
    reserved = {'admin', 'api', 'static', 'health', 'login', 'logout', 'overseer'}
    if slug in reserved:
        abort(400, 'Reserved name')
    return slug
```

---

## Session Architecture — Who Is Logged In?

Our apps have 3 types of session:

```python
# Type 1: Main admin (Jay)
session = {
    'logged_in': True,
    'username': 'admin',
    'role': 'overseer',
    'store_slug': None,           # no tenant — global admin
    'impersonating_slug': 'willies-thrift'  # when impersonating
}

# Type 2: Client (store owner)
session = {
    'logged_in': True,
    'username': 'williesmith@gmail.com',
    'role': 'client',
    'store_slug': 'willies-thrift',  # their tenant
    'impersonating_slug': None
}

# Type 3: Guest (demo mode)
session = {
    'logged_in': True,
    'username': 'guest',
    'is_guest': True,
    'store_slug': None
}
```

### The active_store_slug() Pattern
```python
def active_store_slug():
    """Single source of truth for current tenant context."""
    # Impersonation takes precedence (admin viewing a client store)
    if session.get('impersonating_slug'):
        return session['impersonating_slug']
    # Client's own store
    if session.get('store_slug'):
        return session['store_slug']
    return None  # admin context — no tenant filter

def require_tenant(f):
    """Decorator: ensures a tenant context exists before proceeding."""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        slug = active_store_slug()
        if not slug:
            flash('No store context. Please log in to a store.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated
```

---

## Data Isolation Patterns by Storage Type

### SQLite (single DB, tenant_id column)
```python
# Schema: always include store_slug
CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    store_slug TEXT NOT NULL,
    title TEXT,
    price REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_items_slug ON items(store_slug);

# Query: ALWAYS filter by slug
def get_items(slug):
    db = get_db()
    return db.execute(
        'SELECT * FROM items WHERE store_slug = ? ORDER BY created_at DESC',
        (slug,)
    ).fetchall()

# Never do this:
# db.execute('SELECT * FROM items').fetchall()  # ← LEAKS ALL TENANTS
```

### File System (directory-per-tenant)
```python
CUSTOMERS_DIR = os.path.join(DATA_DIR, 'customers')

def get_store_inventory(slug):
    path = os.path.join(CUSTOMERS_DIR, slug, 'inventory.csv')
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return list(csv.DictReader(f))

def save_store_inventory(slug, products):
    os.makedirs(os.path.join(CUSTOMERS_DIR, slug), exist_ok=True)
    path = os.path.join(CUSTOMERS_DIR, slug, 'inventory.csv')
    with open(path, 'w', newline='') as f:
        if products:
            writer = csv.DictWriter(f, fieldnames=products[0].keys())
            writer.writeheader()
            writer.writerows(products)
```

### JSON Config (per-tenant config files)
```python
def load_client_config(slug):
    path = os.path.join(CUSTOMERS_DIR, slug, 'config.json')
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}

def save_client_config(slug, config):
    os.makedirs(os.path.join(CUSTOMERS_DIR, slug), exist_ok=True)
    path = os.path.join(CUSTOMERS_DIR, slug, 'config.json')
    with open(path, 'w') as f:
        json.dump(config, f, indent=2)
```

---

## Tenant Provisioning — The Wizard Pattern

When a new customer signs up via wizard, we need to:

```python
def provision_store(slug, store_name, contact_email, password, config_data):
    """
    Create a complete tenant environment.
    Idempotent — safe to call twice.
    """
    from datetime import datetime
    import secrets, hashlib

    store_dir = os.path.join(CUSTOMERS_DIR, slug)
    os.makedirs(store_dir, exist_ok=True)
    os.makedirs(os.path.join(store_dir, 'uploads'), exist_ok=True)
    os.makedirs(os.path.join(store_dir, 'ads'), exist_ok=True)

    # 1. Save config
    config = {
        'store_name': store_name,
        'slug': slug,
        'primary_color': config_data.get('color', '#7c3aed'),
        'industry': config_data.get('industry', 'general'),
        'tagline': config_data.get('tagline', ''),
        'contact_name': config_data.get('contact_name', ''),
        'contact_email': contact_email,
        'contact_phone': config_data.get('contact_phone', ''),
        'plan': 'trial',
        'trial_ends': (datetime.utcnow() + timedelta(days=14)).isoformat(),
        'created_at': datetime.utcnow().isoformat(),
    }
    save_client_config(slug, config)

    # 2. Create user account
    if contact_email and password:
        users = {
            contact_email: {
                'password': hashlib.sha256(password.encode()).hexdigest(),
                'role': 'client',
                'name': config_data.get('contact_name', ''),
                'email': contact_email,
                'created': datetime.utcnow().isoformat(),
            }
        }
        with open(os.path.join(store_dir, 'users.json'), 'w') as f:
            json.dump(users, f, indent=2)

    # 3. Seed sample inventory
    sample = load_sample_products(config_data.get('industry', 'general'))
    save_store_inventory(slug, sample)

    # 4. Register in master store list (for overseer)
    add_to_leads_list(config)

    return config
```

---

## The Impersonation Pattern (Overseer Admin)

Jay needs to "enter" any client store to debug or demo it:

```python
@app.route('/overseer/impersonate/<slug>')
@login_required
@overseer_required
def impersonate_store(slug):
    """Enter a client store as admin."""
    validate_slug(slug)
    config = load_client_config(slug)
    if not config:
        flash('Store not found.', 'error')
        return redirect(url_for('overseer_dashboard'))

    session['impersonating_slug'] = slug
    session['impersonating_store_name'] = config.get('store_name', slug)
    flash(f'Now managing {config["store_name"]} — changes are real.', 'warning')
    return redirect(url_for('dashboard'))

@app.route('/overseer/exit-impersonate')
def exit_impersonate():
    """Return to overseer context."""
    session.pop('impersonating_slug', None)
    session.pop('impersonating_store_name', None)
    return redirect(url_for('overseer_dashboard'))
```

---

## Trial → Paid Conversion Flow

```python
def check_trial_status(slug):
    """Returns: 'active', 'expired', 'paid'"""
    config = load_client_config(slug)
    if config.get('plan') == 'paid':
        return 'paid'
    trial_end = config.get('trial_ends')
    if not trial_end:
        return 'expired'
    if datetime.utcnow() < datetime.fromisoformat(trial_end):
        return 'active'
    return 'expired'

def trial_gate(f):
    """Block expired trials from accessing the app."""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        slug = active_store_slug()
        if slug:
            status = check_trial_status(slug)
            if status == 'expired':
                return redirect(url_for('upgrade'))
        return f(*args, **kwargs)
    return decorated
```

---

## Demo Mode vs Guest Mode vs Trial

| Mode | Who | Can modify data? | Sees real data? | Gets to wizard? |
|------|-----|-----------------|-----------------|-----------------|
| **Guest** | Anonymous visitor | ❌ | Sample only | ✅ |
| **Trial** | Signed-up customer | ✅ | Their own | ✅ |
| **Paid** | Paying customer | ✅ | Their own | N/A |
| **Impersonation** | Jay (admin) | ✅ | Client's real data | N/A |

### Guest demo best practices
```python
# Guest sees sample data, not real customer data
@app.route('/dashboard')
@login_required
def dashboard():
    if session.get('is_guest'):
        # Load demo/sample data — never real customer data
        products = load_sample_products('thrift')  
        stats = {'total': len(products), 'available': len(products), 'sold': 0, 'total_value': 1250.00}
        return render_template('dashboard.html', products=products, stats=stats, **ctx())
    
    # Real tenant data
    slug = active_store_slug()
    products = get_store_inventory(slug)
    stats = calculate_stats(products)
    return render_template('dashboard.html', products=products, stats=stats, **ctx())
```

---

## URL Design for Multi-Tenant

```python
# Pattern 1: Path prefix /store/{slug}/ — for public-facing store pages
/store/willies-thrift/            # store landing
/store/willies-thrift/login       # store login
/store/willies-thrift/catalog     # public catalog (future)

# Pattern 2: Session-based — for authenticated admin dashboard
/dashboard      # uses session['store_slug'] — no slug in URL
/inventory      # same
/settings       # same

# Pattern 3: Subdomain (future upgrade)
# willies-thrift.yoursaas.com → extract slug from request.host
def slug_from_subdomain():
    host = request.host  # willies-thrift.yoursaas.com
    subdomain = host.split('.')[0]
    if subdomain not in ('www', 'app', 'api'):
        return validate_slug(subdomain)
    return None
```

---

## Slug Generation — Always Unique, Always Safe

```python
import re, os

def slugify(name):
    """Convert store name to URL-safe slug."""
    slug = name.lower().strip()
    slug = re.sub(r'[^\w\s\-]', '', slug)    # remove special chars
    slug = re.sub(r'[\s_]+', '-', slug)       # spaces to hyphens
    slug = re.sub(r'-+', '-', slug)           # collapse multiple hyphens
    slug = slug.strip('-')                     # remove leading/trailing
    slug = slug[:50]                           # max 50 chars
    return slug or 'store'

def unique_slug(name):
    """Guarantee uniqueness by appending counter if needed."""
    base = slugify(name)
    slug = base
    counter = 2
    while os.path.exists(os.path.join(CUSTOMERS_DIR, slug)):
        slug = f'{base}-{counter}'
        counter += 1
    return slug
```

---

## Common Multi-Tenant Bugs I Must Avoid

### Bug 1: Missing tenant filter
```python
# ❌ Returns ALL tenants' data
items = db.execute('SELECT * FROM items').fetchall()

# ✅ Scoped to tenant
items = db.execute('SELECT * FROM items WHERE store_slug=?', (slug,)).fetchall()
```

### Bug 2: Using wrong slug source
```python
# ❌ Trusting URL param without validation — attacker can access any store
slug = request.args.get('slug')  

# ✅ Always use session-derived slug
slug = active_store_slug()
```

### Bug 3: File path traversal
```python
# ❌ Allows ../../etc/passwd style attacks
path = os.path.join(CUSTOMERS_DIR, user_input, 'data.json')

# ✅ Validate and sanitize first
slug = validate_slug(user_input)
path = os.path.join(CUSTOMERS_DIR, slug, 'data.json')
```

### Bug 4: Shared global state between tenants
```python
# ❌ Module-level dict shared across all requests/tenants
_cache = {}  # DANGER: leaks between tenants

# ✅ Always scope cache by tenant
_cache = {}
def get_cached(slug, key):
    return _cache.get(f'{slug}:{key}')
def set_cached(slug, key, val):
    _cache[f'{slug}:{key}'] = val
```

### Bug 5: Sending wrong tenant's emails
```python
# ❌ Hardcoded sender name
send_email(to=user_email, subject='Welcome', from_name='Liberty Emporium')

# ✅ Use tenant's store name
config = load_client_config(slug)
send_email(to=user_email, subject=f'Welcome to {config["store_name"]}', 
           from_name=config['store_name'])
```

---

## Overseer Dashboard — What Jay Needs to See

The overseer dashboard should show per-tenant:
- Store name + slug
- Plan status (trial/paid/expired) + days left
- Item count
- Last login
- Quick actions: impersonate, suspend, reset password

```python
def get_all_stores():
    """Load all provisioned stores for overseer view."""
    stores = []
    if not os.path.exists(CUSTOMERS_DIR):
        return stores
    for entry in os.listdir(CUSTOMERS_DIR):
        cfg_path = os.path.join(CUSTOMERS_DIR, entry, 'config.json')
        if os.path.isdir(os.path.join(CUSTOMERS_DIR, entry)) and os.path.exists(cfg_path):
            with open(cfg_path) as f:
                cfg = json.load(f)
            cfg['slug'] = entry
            cfg['status'] = check_trial_status(entry)
            cfg['item_count'] = len(get_store_inventory(entry))
            stores.append(cfg)
    return sorted(stores, key=lambda x: x.get('created_at', ''), reverse=True)
```

---

## Scaling Path for Jay's Stack

**Now (0-100 customers):** File-per-tenant works fine. SQLite WAL handles concurrency.

**100-1000 customers:** 
- Switch inventory to SQLite with tenant_id columns
- Add Redis/Valkey for session storage (avoid file-based sessions)
- Nginx with upstream routing

**1000+ customers:**
- PostgreSQL with Row Level Security
- Separate read replica
- Background job queue (Celery or RQ)
- Subdomain routing per tenant

**For now: stick with the file system pattern. It works, it's simple, and it's what we know.**

---

## Quick Reference Card

```
TENANT CHECKLIST — use this before shipping any feature:

□ All queries scoped to slug/tenant_id?
□ Slug validated before use in file paths?
□ Impersonation exits correctly?
□ Guest sees sample data only?
□ Trial expiry checked on protected routes?
□ Config/users loaded from tenant dir not global?
□ Emails send from tenant's store name?
□ Audit log entry created for mutations?
```

---
*Written by Echo for Echo — 2026-04-16 | Jay's multi-tenant SaaS stack*
