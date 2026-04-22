# Tenant Isolation Patterns

## Canonical get_slug() Implementation

```python
import re, os
from flask import session, abort

RESERVED_SLUGS = {"admin","api","static","health","login","logout","overseer","guest","demo","system"}

def _sanitize_slug(slug: str) -> str:
    """Lowercase, alphanumeric + hyphens only, max 40 chars."""
    slug = re.sub(r'[^a-z0-9-]', '', slug.lower())[:40]
    if not slug or slug in RESERVED_SLUGS:
        raise ValueError(f"Invalid or reserved slug: {slug!r}")
    return slug

def get_slug(slug=None) -> str:
    """
    Get the current tenant slug — always from session, never from user input.
    Priority: impersonating_slug (Overseer) > store_slug (logged-in user) > param
    """
    raw = (session.get('impersonating_slug')
           or session.get('store_slug')
           or slug
           or 'system')
    return _sanitize_slug(raw)
```

## Silo Model (file-based, our standard)

```python
DATA_DIR      = os.environ.get('RAILWAY_VOLUME_MOUNT_PATH', '/data')
CUSTOMERS_DIR = os.path.join(DATA_DIR, 'customers')
os.makedirs(CUSTOMERS_DIR, exist_ok=True)

def tenant_dir(slug=None):
    s = get_slug(slug)
    d = os.path.join(CUSTOMERS_DIR, s)
    os.makedirs(d, exist_ok=True)
    return d

def tenant_file(filename, slug=None):
    """Safe path to a file inside the current tenant's directory."""
    return os.path.join(tenant_dir(slug), filename)

def get_tenant_db(slug=None):
    """Get SQLite connection for this tenant's database."""
    import sqlite3
    db_path = tenant_file('data.db', slug)
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    return db

def get_tenant_config(slug=None):
    import json
    cfg_path = tenant_file('config.json', slug)
    if os.path.exists(cfg_path):
        try:
            with open(cfg_path) as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_tenant_config(cfg, slug=None):
    import json
    cfg_path = tenant_file('config.json', slug)
    os.makedirs(os.path.dirname(cfg_path), exist_ok=True)
    with open(cfg_path, 'w') as f:
        json.dump(cfg, f, indent=2)
```

## Pool Model (shared DB + store_slug column)

```python
# Every table needs store_slug:
db.executescript("""
    CREATE TABLE IF NOT EXISTS items (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        store_slug TEXT NOT NULL,
        name       TEXT NOT NULL,
        price      REAL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_items_slug ON items(store_slug);
""")

# Every query scoped to tenant:
def get_items():
    slug = get_slug()
    return get_db().execute(
        'SELECT * FROM items WHERE store_slug=? ORDER BY created_at DESC',
        (slug,)
    ).fetchall()

def add_item(name, price):
    slug = get_slug()
    db = get_db()
    db.execute('INSERT INTO items(store_slug,name,price) VALUES(?,?,?)', (slug,name,price))
    db.commit()
```

## Tenant Rate Limiting

```python
from collections import defaultdict
import time

_tenant_calls = defaultdict(list)

def tenant_rate_ok(slug, max_calls=120, window=60):
    now = time.time()
    _tenant_calls[slug] = [t for t in _tenant_calls[slug] if now - t < window]
    if len(_tenant_calls[slug]) >= max_calls:
        return False
    _tenant_calls[slug].append(now)
    return True

def tenant_rate_limit(max_calls=120):
    """Decorator: per-tenant rate limiting."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            slug = session.get('impersonating_slug') or session.get('store_slug')
            if slug and not tenant_rate_ok(slug, max_calls):
                return jsonify({'error': 'Rate limit exceeded. Slow down.'}), 429
            return f(*args, **kwargs)
        return decorated
    return decorator
```

## Tenant Isolation Audit Checklist

Before shipping any multi-tenant route, verify:
- [ ] `get_slug()` used — never `request.args.get('slug')` or `request.form.get('slug')`
- [ ] Every DB query has `WHERE store_slug=?` or uses `tenant_dir()`/`tenant_file()`
- [ ] File paths use `tenant_file()` — never `os.path.join(DATA_DIR, user_input)`
- [ ] Slug is validated before use (via `_sanitize_slug`)
- [ ] Overseer impersonation uses `session['impersonating_slug']`, cleared on exit
- [ ] `@login_required` on every tenant route
- [ ] `@trial_gate` on every feature route
