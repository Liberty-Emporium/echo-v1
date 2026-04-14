# multi-tenant-upgrade

**Version:** 1.0.0
**Created:** 2026-04-14
**Author:** Echo

## Description

Step-by-step playbook for converting any single-tenant Flask SaaS app to full multi-tenant architecture. Modeled after the Liberty Emporium / Dropship Shipping pattern.

## When To Use

- Converting Contractor Pro AI, Pet Vet AI, Andy Keep Your Secrets to multi-tenant
- Building any new SaaS app from scratch
- Any time Jay says "can multiple businesses use this?"

## The Pattern (Liberty Emporium Standard)

```
/data/
  dropship.db              ← main users/auth DB
  leads.json               ← trial signups
  customers/
    store-slug-1/
      config.json          ← store name, email, plan, trial dates
      users.json           ← per-store user accounts
      orders.json          ← store data
      products.json
    store-slug-2/
      config.json
      ...
```

## Core Functions to Add to app.py

```python
import os, json, re, datetime, functools, hashlib, secrets

DATA_DIR = os.environ.get('DATA_DIR', '/data')
CUSTOMERS_DIR = os.path.join(DATA_DIR, 'customers')
os.makedirs(CUSTOMERS_DIR, exist_ok=True)

def slugify(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')[:40]

def active_slug():
    return session.get('impersonating_slug') or session.get('store_slug') or None

def tenant_dir(slug):
    d = os.path.join(CUSTOMERS_DIR, slug)
    os.makedirs(d, exist_ok=True)
    return d

def load_client_config(slug):
    p = os.path.join(CUSTOMERS_DIR, slug, 'config.json')
    return load_json(p, {})

def save_client_config(slug, cfg):
    os.makedirs(os.path.join(CUSTOMERS_DIR, slug), exist_ok=True)
    save_json(os.path.join(CUSTOMERS_DIR, slug, 'config.json'), cfg)

def list_client_stores():
    stores = []
    if not os.path.exists(CUSTOMERS_DIR): return stores
    for slug in os.listdir(CUSTOMERS_DIR):
        cfg_path = os.path.join(CUSTOMERS_DIR, slug, 'config.json')
        if os.path.exists(cfg_path):
            try:
                with open(cfg_path) as f: cfg = json.load(f)
                stores.append(cfg)
            except: pass
    return sorted(stores, key=lambda s: s.get('created_at',''), reverse=True)
```

## Routes to Add

### Trial Signup
```python
@app.route('/wizard')
def wizard(): return render_template('wizard.html', **ctx())

@app.route('/start-trial', methods=['POST'])
def start_trial():
    store_name = request.form.get('store_name','').strip()
    email = request.form.get('contact_email','').strip()
    # Check duplicate email
    for store in list_client_stores():
        users = load_json(os.path.join(CUSTOMERS_DIR, store['slug'], 'users.json'), {})
        if email in users:
            flash(f'Account with {email} already exists. Sign in instead.', 'error')
            return redirect(url_for('login'))
    slug = slugify(store_name)
    # ensure unique slug
    base = slug; counter = 1
    while os.path.exists(os.path.join(CUSTOMERS_DIR, slug)):
        slug = f'{base}-{counter}'; counter += 1
    now = datetime.datetime.now().isoformat()
    cfg = {'store_name':store_name,'slug':slug,'contact_email':email,
           'plan':'trial','status':'active',
           'trial_end':(datetime.datetime.now()+datetime.timedelta(days=14)).isoformat(),
           'created_at':now}
    save_client_config(slug, cfg)
    pw = secrets.token_urlsafe(8)
    save_json(os.path.join(CUSTOMERS_DIR, slug, 'users.json'),
              {email: {'password': hashlib.sha256(pw.encode()).hexdigest(), 'role':'client'}})
    session.clear()
    session.update({'logged_in':True,'username':email,'role':'client','store_slug':slug})
    flash(f'Welcome! Login: {email} / {pw} — save this!', 'success')
    return redirect(url_for('dashboard'))
```

### Overseer Panel
```python
@app.route('/overseer')
@admin_required
def overseer():
    return render_template('overseer.html', stores=list_client_stores(), **ctx())

@app.route('/overseer/client/<slug>/impersonate', methods=['POST'])
@admin_required
def impersonate(slug):
    session['impersonating_slug'] = slug
    return redirect(url_for('dashboard'))

@app.route('/overseer/exit')
def exit_impersonate():
    session.pop('impersonating_slug', None)
    return redirect(url_for('overseer'))
```

## Templates Needed

- `wizard.html` — trial signup form (store name, email, niche)
- `overseer.html` — admin panel: list stores, create, suspend, impersonate
- `login.html` — main login (username/password for admin OR email/password for clients)
- `store_login.html` — per-tenant login page

## Checklist

- [ ] Add slugify(), active_slug(), tenant_dir(), load_client_config() to app.py
- [ ] Add DATA_DIR fallback (try /data, fallback to ./data)
- [ ] Wrap all data load/save calls with `slug = active_slug()`
- [ ] Add /wizard and /start-trial routes
- [ ] Add /overseer routes (admin only)
- [ ] Add /login and /store/<slug>/login routes
- [ ] Create wizard.html, overseer.html, login.html templates
- [ ] Test locally before pushing (flask-local-test skill)
- [ ] Check for {# in CSS (jinja2-safe-css skill)
- [ ] Push → wait 35s → smoke test

## Pricing Context (Jay's Apps)
- Contractor Pro AI: $99/mo per client, 14-day trial
- Pet Vet AI: $9.99/mo per user, 14-day trial
- Andy Keep Your Secrets: $14.99/mo per user, 14-day trial
