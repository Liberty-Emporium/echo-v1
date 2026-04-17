# Multi-Tenant SaaS — Deep Dive
**Written:** 2026-04-16 | Echo's advanced reference for Jay's stack

---

## Part 1: Architecture Patterns — Choosing Your Isolation Model

There are 3 fundamental models. We use Model 2.

### Model 1: Database-per-Tenant
```
/data/
  customers/
    willies-thrift/
      database.sqlite     ← Entire DB for this tenant
    jays-antiques/
      database.sqlite
```
**Pros:** Perfect isolation, easy backup per tenant, easy delete/export
**Cons:** 100 tenants = 100 open file handles, hard to run cross-tenant queries
**Best for:** Regulated industries (HIPAA, finance), high-value enterprise clients
**Jay's stack:** Works great for small-scale (<500 tenants on Railway)

### Model 2: Schema-per-Tenant (what we use — file directories)
```
/data/
  customers/
    willies-thrift/
      inventory.csv
      config.json
      users.json
      ads/
      uploads/
    jays-antiques/
      inventory.csv
      ...
```
**Pros:** Simple, works with SQLite, easy to reason about, easy to migrate
**Cons:** More OS file handles, directory listing = tenant enumeration risk
**Best for:** Jay's current scale — simple, solid, ships fast

### Model 3: Shared DB + Tenant Column
```sql
CREATE TABLE items (
    id          INTEGER PRIMARY KEY,
    store_slug  TEXT NOT NULL,    -- the tenant filter
    title       TEXT,
    price       REAL
);
-- Every query: WHERE store_slug = ?
```
**Pros:** Easy to query across tenants, single backup, scales to millions of rows
**Cons:** Any missed WHERE clause = data leak, harder to delete/export one tenant
**Best for:** When Jay has 100+ active paying tenants and needs cross-tenant analytics

### Hybrid (best long-term for Jay)
```
SQLite (shared) for:
  - items, sales, metrics, audit_log (high-write, needs WHERE store_slug)

Files (per-tenant) for:
  - config.json (rarely changes)
  - users.json (<100 users per store)
  - uploads/ (binary files)
  - ads/ (generated content)
```

---

## Part 2: The Tenant Context Object — Never Lose Track of Who You're Serving

The biggest mistake in multi-tenant: code that doesn't know which tenant it's for.

```python
# ── The Tenant Context Pattern ─────────────────────────────────────────────

class TenantContext:
    """
    Single object that carries all per-request tenant info.
    Build it once per request. Pass it everywhere.
    Never read session directly in business logic.
    """
    def __init__(self):
        self.slug        = self._resolve_slug()
        self.config      = self._load_config()
        self.store_name  = self.config.get('store_name', 'Your Store')
        self.plan        = self.config.get('plan', 'trial')
        self.is_guest    = session.get('is_guest', False)
        self.is_admin    = session.get('role') == 'overseer'
        self.user_email  = session.get('username', '')

    def _resolve_slug(self):
        return (session.get('impersonating_slug') or
                session.get('store_slug') or None)

    def _load_config(self):
        if not self.slug:
            return {}
        path = os.path.join(CUSTOMERS_DIR, self.slug, 'config.json')
        if os.path.exists(path):
            with open(path) as f:
                return json.load(f)
        return {}

    @property
    def data_dir(self):
        return os.path.join(CUSTOMERS_DIR, self.slug)

    @property
    def is_trial_active(self):
        from datetime import datetime
        trial_end = self.config.get('trial_ends')
        if not trial_end: return False
        return datetime.utcnow() < datetime.fromisoformat(trial_end)

    @property
    def trial_days_left(self):
        from datetime import datetime
        trial_end = self.config.get('trial_ends')
        if not trial_end: return 0
        delta = datetime.fromisoformat(trial_end) - datetime.utcnow()
        return max(0, delta.days)

# Flask: build per request using g
@app.before_request
def set_tenant():
    g.tenant = TenantContext()

# Use in routes:
@app.route('/dashboard')
@login_required
def dashboard():
    tc = g.tenant
    inventory = load_inventory(tc.slug)
    return render_template('dashboard.html',
        store_name=tc.store_name,
        trial_days=tc.trial_days_left,
        **ctx())
```

---

## Part 3: Audit Log — Every Write Leaves a Trail

Critical for debugging, compliance, and knowing when a tenant's data was changed.

```python
AUDIT_DB = os.path.join(DATA_DIR, 'audit.db')

def init_audit_db():
    conn = sqlite3.connect(AUDIT_DB)
    conn.execute('''CREATE TABLE IF NOT EXISTS audit_log (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        store_slug  TEXT,
        user        TEXT,
        action      TEXT,          -- 'add_product', 'delete_product', 'login', etc.
        target_id   TEXT,          -- SKU, user email, etc.
        details     TEXT,          -- JSON of what changed
        ip_address  TEXT,
        timestamp   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

def audit(action, target_id='', details=None):
    """Fire-and-forget audit entry. Never blocks the request."""
    try:
        slug  = session.get('impersonating_slug') or session.get('store_slug') or 'admin'
        user  = session.get('username', 'unknown')
        ip    = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        conn  = sqlite3.connect(AUDIT_DB)
        conn.execute(
            'INSERT INTO audit_log (store_slug,user,action,target_id,details,ip_address) VALUES (?,?,?,?,?,?)',
            (slug, user, action, target_id, json.dumps(details or {}), ip)
        )
        conn.commit()
        conn.close()
    except Exception:
        pass  # never crash a request because of audit logging

# Usage:
# audit('add_product', sku, {'name': product['Title'], 'price': product['Price']})
# audit('login', user_email)
# audit('delete_product', sku)
# audit('wizard_complete', slug, {'store_name': store_name, 'plan': 'trial'})
```

---

## Part 4: Rate Limiting Per Tenant (Not Just Per IP)

IP-based rate limiting misses multi-user tenants. Rate limit by tenant too.

```python
from collections import defaultdict
import time

_tenant_rate_store = defaultdict(list)
_TENANT_WINDOW = 60      # 1 minute
_TENANT_MAX_WRITES = 100  # max DB writes per minute per tenant

def check_tenant_rate(slug, limit=100):
    """Returns False if this tenant is hammering the API."""
    now = time.time()
    _tenant_rate_store[slug] = [
        t for t in _tenant_rate_store[slug]
        if now - t < _TENANT_WINDOW
    ]
    if len(_tenant_rate_store[slug]) >= limit:
        return False
    _tenant_rate_store[slug].append(now)
    return True

def tenant_rate_limit(limit=100):
    def decorator(f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            slug = active_store_slug()
            if slug and not check_tenant_rate(slug, limit):
                return jsonify({'error': 'Too many requests. Slow down.'}), 429
            return f(*args, **kwargs)
        return decorated
    return decorator

# Usage:
@app.route('/api/inventory', methods=['POST'])
@_require_api_key
@tenant_rate_limit(limit=60)  # 60 writes per minute per tenant
def api_add_item():
    ...
```

---

## Part 5: Tenant Metrics Dashboard (Overseer Power)

Jay needs to see health of all tenants at a glance. Build this into overseer.

```python
def get_tenant_health():
    """
    Returns health summary for all tenants.
    Sorted by: most recently active first.
    """
    from datetime import datetime
    stores = []

    if not os.path.exists(CUSTOMERS_DIR):
        return stores

    for slug in os.listdir(CUSTOMERS_DIR):
        cfg_path = os.path.join(CUSTOMERS_DIR, slug, 'config.json')
        if not os.path.isdir(os.path.join(CUSTOMERS_DIR, slug)):
            continue
        if not os.path.exists(cfg_path):
            continue

        with open(cfg_path) as f:
            cfg = json.load(f)

        # Check trial status
        trial_end = cfg.get('trial_ends')
        if cfg.get('plan') == 'paid':
            status = 'paid'
            status_color = '#22c55e'
        elif trial_end and datetime.utcnow() < datetime.fromisoformat(trial_end):
            delta = datetime.fromisoformat(trial_end) - datetime.utcnow()
            status = f'trial ({delta.days}d left)'
            status_color = '#f59e0b'
        else:
            status = 'expired'
            status_color = '#ef4444'

        # Count inventory
        inv_path = os.path.join(CUSTOMERS_DIR, slug, 'inventory.csv')
        item_count = 0
        if os.path.exists(inv_path):
            with open(inv_path) as f:
                item_count = max(0, sum(1 for _ in f) - 1)  # minus header

        # Last activity (mtime of any file in tenant dir)
        tenant_dir = os.path.join(CUSTOMERS_DIR, slug)
        last_active = max(
            (os.path.getmtime(os.path.join(tenant_dir, f))
             for f in os.listdir(tenant_dir)
             if os.path.isfile(os.path.join(tenant_dir, f))),
            default=0
        )

        stores.append({
            'slug':         slug,
            'store_name':   cfg.get('store_name', slug),
            'email':        cfg.get('contact_email', ''),
            'plan':         cfg.get('plan', 'trial'),
            'status':       status,
            'status_color': status_color,
            'item_count':   item_count,
            'created_at':   cfg.get('created_at', ''),
            'last_active':  datetime.fromtimestamp(last_active).isoformat() if last_active else '',
            'mrr':          20.00 if cfg.get('plan') == 'paid' else 0,
        })

    # Sort: paid first, then by last active
    return sorted(stores,
        key=lambda x: (x['plan'] != 'paid', x['last_active']),
        reverse=True)
```

---

## Part 6: Stripe Multi-Tenant Billing Patterns

When Stripe is live, each tenant needs their own customer record.

```python
import stripe

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', '')

def get_or_create_stripe_customer(slug, email, store_name):
    """
    Get existing Stripe customer for this tenant or create one.
    Store the stripe_customer_id in tenant config.
    """
    config = load_client_config(slug)

    # Already have a customer ID
    if config.get('stripe_customer_id'):
        return config['stripe_customer_id']

    # Create new customer
    customer = stripe.Customer.create(
        email=email,
        name=store_name,
        metadata={
            'slug': slug,
            'platform': 'alexander-ai-inventory',
        }
    )
    config['stripe_customer_id'] = customer.id
    save_client_config(slug, config)
    return customer.id

def create_subscription(slug, price_id):
    """Create a Stripe subscription for this tenant."""
    config = load_client_config(slug)
    customer_id = get_or_create_stripe_customer(
        slug, config['contact_email'], config['store_name']
    )

    subscription = stripe.Subscription.create(
        customer=customer_id,
        items=[{'price': price_id}],
        payment_behavior='default_incomplete',
        payment_settings={'save_default_payment_method': 'on_subscription'},
        expand=['latest_invoice.payment_intent'],
        metadata={'slug': slug},
        idempotency_key=f'sub-{slug}-{price_id}',  # prevent duplicate charges
    )
    return subscription

# Webhook handler — keeps tenant plan in sync with Stripe
@app.route('/webhook/stripe', methods=['POST'])
def stripe_webhook():
    payload = request.data
    sig     = request.headers.get('Stripe-Signature')
    secret  = os.environ.get('STRIPE_WEBHOOK_SECRET')

    try:
        event = stripe.Webhook.construct_event(payload, sig, secret)
    except stripe.error.SignatureVerificationError:
        return '', 400

    if event['type'] == 'customer.subscription.updated':
        sub  = event['data']['object']
        slug = sub['metadata'].get('slug')
        if slug:
            cfg = load_client_config(slug)
            cfg['plan']   = 'paid' if sub['status'] == 'active' else 'trial'
            cfg['stripe_subscription_id'] = sub['id']
            save_client_config(slug, cfg)
            audit('stripe_subscription_updated', slug, {'status': sub['status']})

    elif event['type'] == 'customer.subscription.deleted':
        sub  = event['data']['object']
        slug = sub['metadata'].get('slug')
        if slug:
            cfg = load_client_config(slug)
            cfg['plan'] = 'expired'
            save_client_config(slug, cfg)

    return '', 200
```

---

## Part 7: Tenant Data Export & GDPR

Every SaaS must let tenants export or delete their data.

```python
import zipfile, csv, io

@app.route('/settings/export-data')
@login_required
def export_tenant_data():
    """Package all tenant data into a downloadable zip."""
    slug = active_store_slug()
    if not slug:
        abort(403)

    audit('data_export_requested', slug)

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        tenant_dir = os.path.join(CUSTOMERS_DIR, slug)

        # Config
        cfg_path = os.path.join(tenant_dir, 'config.json')
        if os.path.exists(cfg_path):
            zf.write(cfg_path, 'config.json')

        # Inventory
        inv_path = os.path.join(tenant_dir, 'inventory.csv')
        if os.path.exists(inv_path):
            zf.write(inv_path, 'inventory.csv')

        # Ads
        ads_dir = os.path.join(tenant_dir, 'ads')
        if os.path.exists(ads_dir):
            for fname in os.listdir(ads_dir):
                zf.write(os.path.join(ads_dir, fname), f'ads/{fname}')

    buf.seek(0)
    config = load_client_config(slug)
    store_slug = config.get('store_name', slug).replace(' ', '-').lower()
    return send_file(
        buf,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f'{store_slug}-data-export.zip'
    )

@app.route('/settings/delete-account', methods=['POST'])
@login_required
def delete_tenant_account():
    """Hard delete all tenant data. Irreversible."""
    slug = active_store_slug()
    if not slug:
        abort(403)

    # Confirm with password
    password = request.form.get('confirm_password')
    users = load_store_users(slug)
    user_email = session.get('username')
    if not users.get(user_email) or not verify_password(password, users[user_email]['password']):
        flash('Incorrect password. Account not deleted.', 'error')
        return redirect(url_for('settings'))

    audit('account_deleted', slug)

    # Remove all tenant files
    import shutil
    tenant_dir = os.path.join(CUSTOMERS_DIR, slug)
    if os.path.exists(tenant_dir):
        shutil.rmtree(tenant_dir)

    # Cancel Stripe subscription if active
    config = load_client_config(slug)
    if config.get('stripe_subscription_id') and stripe.api_key:
        try:
            stripe.Subscription.delete(config['stripe_subscription_id'])
        except Exception:
            pass

    session.clear()
    flash('Your account and all data have been permanently deleted.', 'success')
    return redirect('/')
```

---

## Part 8: SaaS Pricing Psychology — What the Research Says

This directly applies to Jay's wizard and pricing pages.

### The Decoy Effect (most powerful)
```
Without decoy:          With decoy:
Starter: $20/mo         Starter:   $20/mo      ← 40% choose
                        Standard:  $35/mo      ← Decoy (bad value)
Pro: $40/mo             Pro:       $40/mo      ← 60% choose (was 34%)

Result: +26% revenue per customer, no price change
```

**Apply to Jay's apps:**
```
Current:   $99 setup + $20/mo

Better:
  Basic:   $79 setup + $14.99/mo  (5 products, no AI)
  Pro:     $99 setup + $19.99/mo  ← Most Popular ← DECOY
  Business: $149 setup + $29.99/mo (unlimited, priority support)
```

### Price Anchoring
Show the annual price first, then monthly: 
- "Save $60 — $199/year" → then show "$19.99/month"
- The $199 anchor makes $19.99 feel tiny

### Left-Digit Effect
- $19.99 vs $20 → 24% more conversions (same product)
- Always end in .99 or .95

### "Most Popular" Badge
- Placing a badge on one plan increases that plan's selection 67%
- Always put it on the plan you WANT them to choose (mid-tier)

### Loss Aversion in Trials
```
❌ "Start your free trial"  
✅ "Start free — don't lose access to AI features after 14 days"

People are 2x more motivated by avoiding loss than gaining value.
```

### CTA Button Copy That Converts
```
❌ "Get Started"       → generic, low intent
❌ "Buy Now"           → feels like a transaction, triggers resistance  
❌ "Subscribe"         → commitment aversion
✅ "Start Free Trial"  → low risk, forward motion
✅ "Get My Store Now"  → ownership language, personal
✅ "Try It Free"       → zero friction
```

### Trial Length Psychology
- 7 days: too short, causes anxiety, poor activation
- 14 days: sweet spot for most SaaS
- 30 days: too long, people forget about you
- **For Jay's apps:** 14 days is correct. Send emails at day 3, 7, 12, 14.

---

## Part 9: The Onboarding Email Sequence (Activation = Revenue)

Users who don't activate during trial never convert. The fix is email.

```python
# Trigger this immediately after wizard completes
def queue_trial_onboarding(slug, email, store_name):
    """14-day sequence — gets them to aha moment fast."""
    emails = [
        # Day 0 — immediately
        {
            'day': 0,
            'subject': f'🎉 Your {store_name} store is live',
            'preview': 'Your store is ready. Here\'s how to get the most out of it.',
            'body_template': 'onboarding_welcome',
        },
        # Day 1 — first feature push
        {
            'day': 1,
            'subject': f'Try this first: AI picture ads for {store_name}',
            'preview': 'Upload a photo → AI writes the ad. Takes 30 seconds.',
            'body_template': 'onboarding_ai_ads',
        },
        # Day 3 — usage check
        {
            'day': 3,
            'subject': 'How\'s it going so far?',
            'preview': 'You\'ve had 3 days with Alexander AI. Here\'s what most stores do next.',
            'body_template': 'onboarding_day3',
        },
        # Day 7 — social proof
        {
            'day': 7,
            'subject': 'What stores like yours are doing with AI',
            'preview': 'Real results from Alexander AI stores in your first week.',
            'body_template': 'onboarding_social_proof',
        },
        # Day 12 — urgency
        {
            'day': 12,
            'subject': f'2 days left on your {store_name} trial',
            'preview': 'Your AI features go dark in 2 days. Keep them for $20/mo.',
            'body_template': 'onboarding_urgency',
        },
        # Day 14 — last chance
        {
            'day': 14,
            'subject': 'Your trial ends today',
            'preview': 'Upgrade now to keep your store and all your data.',
            'body_template': 'onboarding_final',
        },
    ]

    for email_def in emails:
        queue_email(
            user_email=email,
            template=email_def['body_template'],
            context_dict={'store_name': store_name, 'slug': slug},
            delay_days=email_def['day']
        )
```

---

## Part 10: Background Jobs Per Tenant (No External Deps)

For fire-and-forget tasks (email, AI generation, backups) without Celery:

```python
import threading, queue, time

class TenantJobQueue:
    """
    Simple background job queue.
    No Redis, no Celery. Pure Python.
    Good for <1000 tenants and <100 jobs/minute.
    """
    def __init__(self):
        self._q = queue.Queue()
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()

    def enqueue(self, fn, *args, **kwargs):
        """Add a job. Returns immediately."""
        self._q.put((fn, args, kwargs))

    def _worker(self):
        while True:
            try:
                fn, args, kwargs = self._q.get(timeout=1)
                fn(*args, **kwargs)
                self._q.task_done()
            except queue.Empty:
                pass
            except Exception as e:
                app.logger.error(f'Background job failed: {e}')

# Initialize once at startup
job_queue = TenantJobQueue()

# Usage:
# job_queue.enqueue(send_email, to=email, subject='Welcome', body=body)
# job_queue.enqueue(generate_ai_ad, slug=slug, sku=sku)
# job_queue.enqueue(backup_tenant_data, slug=slug)
```

---

## Part 11: Tenant Security Checklist

```
BEFORE SHIPPING ANY MULTI-TENANT FEATURE:

Authentication & Authorization:
□ Route has @login_required
□ Admin routes have @admin_required  
□ Tenant data only accessible to that tenant
□ Slug in URL validated against session slug (not just URL)
□ Admin can impersonate but exit is always available

Data Isolation:
□ All DB queries have WHERE store_slug = ?
□ File paths use validated slug (no traversal possible)
□ Upload filenames sanitized (secure_filename())
□ No global state shared between tenants
□ Guest sees only sample data, never real tenant data

Session Security:
□ SESSION_COOKIE_HTTPONLY = True
□ SESSION_COOKIE_SAMESITE = 'Lax'
□ Session secret is long random string from env var
□ Impersonation stored in session, not URL

API Security:
□ API keys scoped to tenant
□ API key stored as hash in DB, not plaintext
□ Rate limiting per tenant + per IP
□ All API writes go through audit log

Outputs:
□ No tenant-specific info in error messages (reveals tenant exists)
□ 404 for non-existent slugs (not 403 — don't reveal it exists)
□ Stripe webhooks verified with signature
```

---

## Part 12: What Makes the Difference at Scale

**Things that feel fine at 10 tenants but break at 100:**

1. **`os.listdir(CUSTOMERS_DIR)` in every request** → Cache the store list in memory, invalidate on write
2. **Loading full inventory.csv to count items** → Store item_count in config.json, update on write
3. **All tenants share one SQLite DB** → With WAL mode, handles ~100 concurrent writes. At 500+ tenants, migrate to per-tenant DB or Postgres
4. **Email sends in request thread** → Always use background queue. Never block a web request on SMTP
5. **No pagination on inventory** → Load 200 items max. Add `?page=2` for the rest
6. **Backup runs synchronously** → Queue it. Never block the request thread for a backup

---
*Echo's deep reference — researched + written 2026-04-16*
*Sources: OWASP, Stripe docs, Dan Ariely pricing research, ProfitWell, ConversionXL*
