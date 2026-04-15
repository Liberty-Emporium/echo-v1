"""
saas_core.py — Liberty Emporium Multi-Tenant SaaS Blueprint
============================================================
Drop this file into ANY Flask app and get:
  - Multi-tenant data isolation (per-slug directories)
  - Trial signup wizard
  - Admin overseer panel (CRUD, impersonate, suspend, delete)
  - Per-tenant user auth (email/password)
  - Admin auth (separate from tenant users)
  - Persistent /data storage with fallback
  - Duplicate email protection
  - Lead tracking

USAGE:
  1. Copy saas_core.py into your Flask app directory
  2. In app.py: from saas_core import SaaSCore
  3. core = SaaSCore(app, app_name="My App", monthly_price=99.00)
  4. Register blueprints: app.register_blueprint(core.blueprint)
  5. In your routes, use: core.active_slug(), core.tenant_dir(slug), etc.

ROUTES ADDED AUTOMATICALLY:
  GET/POST /login                          — admin + tenant user login
  GET      /logout                         — clear session
  GET      /wizard                         — trial signup form
  POST     /start-trial                    — create new tenant
  GET/POST /account                        — change username + password
  GET/POST /forgot-password               — request password reset by email
  GET/POST /reset-password/<token>        — set new password via token
  GET      /overseer                       — admin panel (admin only)
  POST     /overseer/client/create        — create client manually
  POST     /overseer/client/<slug>/impersonate
  GET      /overseer/exit                 — exit impersonation
  POST     /overseer/client/<slug>/suspend
  POST     /overseer/client/<slug>/delete

TEMPLATES REQUIRED (create these in your templates/ dir):
  login.html              — login form (username/email + password)
  wizard.html             — trial signup form
  overseer.html           — admin panel
  account.html            — change username + password form
  forgot_password.html    — email input for password reset
  reset_password.html     — new password input (receives token + email)

Author: Echo (AI CEO, Liberty Emporium)
Version: 1.0.0
Created: 2026-04-14
"""

import os
import json
import re
import hashlib
import secrets
import datetime
import functools
import sqlite3

from flask import (Blueprint, render_template, request, redirect,
                   url_for, session, flash, g)


# ─────────────────────────────────────────────────────────────────────────────
# DATA DIRECTORY SETUP
# ─────────────────────────────────────────────────────────────────────────────

def setup_data_dir(preferred='/data'):
    """
    Returns a writable data directory.
    Tries preferred (/data) first — Railway persistent volume.
    Falls back to ./data in the app directory.
    """
    try:
        os.makedirs(preferred, exist_ok=True)
        test = os.path.join(preferred, '.write_test')
        open(test, 'w').close()
        os.remove(test)
        return preferred
    except Exception:
        fallback = os.path.join(os.path.dirname(__file__), 'data')
        os.makedirs(fallback, exist_ok=True)
        return fallback


# ─────────────────────────────────────────────────────────────────────────────
# SECRET KEY — STABLE ACROSS RESTARTS
# ─────────────────────────────────────────────────────────────────────────────

def get_secret_key(data_dir=None):
    """
    Returns a stable Flask SECRET_KEY that survives Railway restarts.

    Priority:
      1. SECRET_KEY env var (set this in Railway for production)
      2. Persisted key in /data/secret_key (auto-created on first boot)
      3. Random fallback (last resort — sessions won't survive restarts)

    NEVER use secrets.token_hex() as a default — it generates a new key
    on every restart, which invalidates all user sessions and breaks the nav.
    """
    env_key = os.environ.get('SECRET_KEY')
    if env_key:
        return env_key
    base = data_dir or os.environ.get('DATA_DIR', '/data')
    key_file = os.path.join(base, 'secret_key')
    try:
        os.makedirs(base, exist_ok=True)
        if os.path.exists(key_file):
            with open(key_file) as f:
                key = f.read().strip()
                if key:
                    return key
        key = secrets.token_hex(32)
        with open(key_file, 'w') as f:
            f.write(key)
        return key
    except Exception:
        # Can't write to disk — return random key as last resort
        return secrets.token_hex(32)


# ─────────────────────────────────────────────────────────────────────────────
# JSON HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def load_json(path, default=None):
    if default is None:
        default = []
    if os.path.exists(path):
        try:
            with open(path) as f:
                return json.load(f)
        except Exception:
            pass
    return default


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


# ─────────────────────────────────────────────────────────────────────────────
# UTILITY
# ─────────────────────────────────────────────────────────────────────────────

def hash_pw(password):
    return hashlib.sha256(password.encode()).hexdigest()


def slugify(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')[:40]


# ─────────────────────────────────────────────────────────────────────────────
# SAAS CORE CLASS
# ─────────────────────────────────────────────────────────────────────────────

class SaaSCore:
    """
    Drop-in multi-tenant SaaS core for Flask apps.

    Example:
        from saas_core import SaaSCore
        core = SaaSCore(app, app_name="Contractor Pro AI", monthly_price=99.00)
        app.register_blueprint(core.blueprint)
    """

    def __init__(self, app=None, app_name="My SaaS App", monthly_price=99.00,
                 admin_user=None, admin_pass=None, trial_days=14,
                 dashboard_endpoint='dashboard'):
        self.app_name      = app_name
        self.monthly_price = monthly_price
        self.trial_days           = trial_days
        self.dashboard_endpoint  = dashboard_endpoint

        # Data directories
        self.data_dir       = setup_data_dir(os.environ.get('DATA_DIR', '/data'))
        self.customers_dir  = os.path.join(self.data_dir, 'customers')
        os.makedirs(self.customers_dir, exist_ok=True)

        # Secret key — set on app if not already set
        # This ensures sessions survive Railway restarts automatically
        if app is not None and not app.secret_key:
            app.secret_key = get_secret_key(self.data_dir)

        # Admin credentials
        self.admin_user = admin_user or os.environ.get('ADMIN_USER', 'admin')
        self.admin_pass = admin_pass or os.environ.get('ADMIN_PASSWORD', 'admin1')

        # SQLite for admin auth
        self.db_file = os.path.join(self.data_dir, 'saas_core.db')
        self._init_db()

        # Flask blueprint
        self.blueprint = Blueprint('saas_core', __name__)
        self._register_routes()

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Register with a Flask app (supports app factory pattern)."""
        # Ensure stable secret key before registering (fixes Railway restart session wipe)
        if not app.secret_key:
            app.secret_key = get_secret_key(self.data_dir)
        app.register_blueprint(self.blueprint)
        app.extensions = getattr(app, 'extensions', {})
        app.extensions['saas_core'] = self

    # ── Database ──────────────────────────────────────────────────────────────

    def _init_db(self):
        db = sqlite3.connect(self.db_file)
        db.execute('''CREATE TABLE IF NOT EXISTS admin_users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'admin',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        pw = hash_pw(self.admin_pass)
        db.execute('INSERT OR IGNORE INTO admin_users (username, password) VALUES (?, ?)',
                   (self.admin_user, pw))
        db.commit()
        db.close()

    # ── Tenant Helpers ────────────────────────────────────────────────────────

    def active_slug(self):
        """Returns the current active tenant slug (impersonation-aware)."""
        return session.get('impersonating_slug') or session.get('store_slug') or None

    def tenant_dir(self, slug):
        """Returns (and creates) the data directory for a tenant."""
        d = os.path.join(self.customers_dir, slug)
        os.makedirs(d, exist_ok=True)
        return d

    def data_path(self, filename, slug=None):
        """Returns the full path to a data file, optionally scoped to a tenant."""
        if slug:
            return os.path.join(self.tenant_dir(slug), filename)
        return os.path.join(self.data_dir, filename)

    def load_client_config(self, slug):
        return load_json(os.path.join(self.customers_dir, slug, 'config.json'), {})

    def save_client_config(self, slug, cfg):
        os.makedirs(os.path.join(self.customers_dir, slug), exist_ok=True)
        save_json(os.path.join(self.customers_dir, slug, 'config.json'), cfg)

    def list_client_stores(self):
        stores = []
        if not os.path.exists(self.customers_dir):
            return stores
        for slug in os.listdir(self.customers_dir):
            cfg_path = os.path.join(self.customers_dir, slug, 'config.json')
            if os.path.exists(cfg_path):
                try:
                    with open(cfg_path) as f:
                        stores.append(json.load(f))
                except Exception:
                    pass
        return sorted(stores, key=lambda s: s.get('created_at', ''), reverse=True)

    def load_leads(self):
        return load_json(os.path.join(self.data_dir, 'leads.json'))

    def save_leads(self, data):
        save_json(os.path.join(self.data_dir, 'leads.json'), data)

    # ── Auth Decorators ───────────────────────────────────────────────────────

    def login_required(self, f):
        """Decorator: redirect to /login if not logged in."""
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            if not session.get('logged_in'):
                return redirect(url_for('saas_core.login'))
            return f(*args, **kwargs)
        return decorated

    def admin_required(self, f):
        """Decorator: redirect to /login if not admin."""
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            if not session.get('logged_in') or session.get('role') != 'admin':
                flash('Admin access required.', 'error')
                return redirect(url_for('saas_core.login'))
            return f(*args, **kwargs)
        return decorated

    # ── Context ───────────────────────────────────────────────────────────────

    def ctx(self):
        """Returns template context dict. Merge with your own context."""
        slug = self.active_slug()
        store_name = self.app_name
        if slug:
            cfg = self.load_client_config(slug)
            store_name = cfg.get('store_name', self.app_name)
        return {
            'app_name':     self.app_name,
            'store_name':   store_name,
            'store_slug':   slug,
            'current_user': session.get('username'),
            'current_role': session.get('role'),
            'impersonating': bool(session.get('impersonating_slug')),
        }

    # ── Route Registration ────────────────────────────────────────────────────

    def _register_routes(self):
        bp = self.blueprint

        # ── Login ─────────────────────────────────────────────────────────────
        @bp.route('/login', methods=['GET', 'POST'])
        def login():
            if session.get('logged_in'):
                return redirect(url_for('dashboard'))

            if request.method == 'POST':
                username = request.form.get('username', '').strip()
                password = request.form.get('password', '').strip()

                # Check admin
                db = sqlite3.connect(self.db_file)
                db.row_factory = sqlite3.Row
                admin = db.execute('SELECT * FROM admin_users WHERE username=?',
                                   (username,)).fetchone()
                db.close()
                if admin and admin['password'] == hash_pw(password):
                    session.clear()
                    session.update({'logged_in': True, 'username': username, 'role': 'admin'})
                    return redirect(url_for(self.dashboard_endpoint))

                # Check tenant users
                for store in self.list_client_stores():
                    upath = os.path.join(self.customers_dir, store['slug'], 'users.json')
                    users = load_json(upath, {})
                    u = users.get(username)
                    if u and u.get('password') == hash_pw(password):
                        session.clear()
                        session.update({
                            'logged_in': True, 'username': username,
                            'role': u.get('role', 'client'),
                            'store_slug': store['slug']
                        })
                        return redirect(url_for(self.dashboard_endpoint))

                flash('Invalid credentials.', 'error')
            return render_template('login.html', **self.ctx())

        # ── Logout ────────────────────────────────────────────────────────────
        @bp.route('/logout')
        def logout():
            session.clear()
            return redirect(url_for('saas_core.login'))

        # ── Trial Wizard ──────────────────────────────────────────────────────
        @bp.route('/wizard')
        def wizard():
            return render_template('wizard.html', **self.ctx())

        @bp.route('/start-trial', methods=['POST'])
        def start_trial():
            store_name    = request.form.get('store_name', '').strip()
            contact_email = request.form.get('contact_email', '').strip()
            contact_name  = request.form.get('contact_name', '').strip()
            extra_field   = request.form.get('extra_field', '').strip()  # niche/specialty/etc.

            if not store_name or not contact_email:
                flash('Business name and email are required.', 'error')
                return redirect(url_for('saas_core.wizard'))

            # Block duplicate email
            for store in self.list_client_stores():
                upath = os.path.join(self.customers_dir, store['slug'], 'users.json')
                users = load_json(upath, {})
                if contact_email in users:
                    flash(f'Account with {contact_email} already exists. Sign in instead.', 'error')
                    return redirect(url_for('saas_core.login'))

            # Create unique slug
            slug = slugify(store_name)
            base = slug; counter = 1
            while os.path.exists(os.path.join(self.customers_dir, slug)):
                slug = f'{base}-{counter}'; counter += 1

            now = datetime.datetime.now().isoformat()
            trial_end = (datetime.datetime.now() +
                         datetime.timedelta(days=self.trial_days)).isoformat()

            cfg = {
                'store_name':    store_name,
                'slug':          slug,
                'contact_name':  contact_name,
                'contact_email': contact_email,
                'extra_field':   extra_field,
                'plan':          'trial',
                'status':        'active',
                'trial_start':   now,
                'trial_end':     trial_end,
                'created_at':    now,
            }
            self.save_client_config(slug, cfg)

            temp_pw = secrets.token_urlsafe(8)
            save_json(os.path.join(self.customers_dir, slug, 'users.json'), {
                contact_email: {
                    'password':   hash_pw(temp_pw),
                    'role':       'client',
                    'store_slug': slug,
                    'created_at': now,
                }
            })

            leads = self.load_leads()
            leads.append({'store_name': store_name, 'contact_email': contact_email,
                          'slug': slug, 'created_at': now, 'type': 'trial'})
            self.save_leads(leads)

            session.clear()
            session.update({'logged_in': True, 'username': contact_email,
                            'role': 'client', 'store_slug': slug})
            flash(f'Welcome! Your login: {contact_email} / {temp_pw} — save this!', 'success')
            return redirect(url_for(self.dashboard_endpoint))

        # ── Overseer ──────────────────────────────────────────────────────────
        @bp.route('/overseer')
        def overseer():
            if not session.get('logged_in') or session.get('role') != 'admin':
                return redirect(url_for('saas_core.login'))
            stores = self.list_client_stores()
            active = sum(1 for s in stores if s.get('status') == 'active')
            mrr    = active * self.monthly_price
            return render_template('overseer.html',
                stores=stores, leads=self.load_leads(),
                active_count=active,
                suspended_count=sum(1 for s in stores if s.get('status') == 'suspended'),
                mrr=mrr, monthly_price=self.monthly_price,
                **self.ctx())

        @bp.route('/overseer/client/create', methods=['POST'])
        def overseer_create():
            if session.get('role') != 'admin':
                return redirect(url_for('saas_core.login'))
            store_name = request.form.get('store_name', '').strip()
            email      = request.form.get('contact_email', '').strip()
            temp_pw    = request.form.get('temp_password', '').strip()
            extra      = request.form.get('extra_field', '').strip()
            if not all([store_name, email, temp_pw]):
                flash('All fields required.', 'error')
                return redirect(url_for('saas_core.overseer'))
            slug = slugify(store_name); base = slug; counter = 1
            while os.path.exists(os.path.join(self.customers_dir, slug)):
                slug = f'{base}-{counter}'; counter += 1
            now = datetime.datetime.now().isoformat()
            self.save_client_config(slug, {
                'store_name': store_name, 'slug': slug, 'contact_email': email,
                'extra_field': extra, 'plan': 'starter', 'status': 'active', 'created_at': now
            })
            save_json(os.path.join(self.customers_dir, slug, 'users.json'), {
                email: {'password': hash_pw(temp_pw), 'role': 'client',
                        'store_slug': slug, 'created_at': now}
            })
            flash(f'Client "{store_name}" created! Login: {email} / {temp_pw}', 'success')
            return redirect(url_for('saas_core.overseer'))

        @bp.route('/overseer/client/<slug>/impersonate', methods=['POST'])
        def overseer_impersonate(slug):
            if session.get('role') != 'admin':
                return redirect(url_for('saas_core.login'))
            cfg = self.load_client_config(slug)
            if not cfg:
                flash('Store not found.', 'error')
                return redirect(url_for('saas_core.overseer'))
            session['impersonating_slug'] = slug
            flash(f'Managing {cfg["store_name"]}.', 'success')
            return redirect(url_for(self.dashboard_endpoint))

        @bp.route('/overseer/exit')
        def overseer_exit():
            session.pop('impersonating_slug', None)
            return redirect(url_for('saas_core.overseer'))

        @bp.route('/overseer/client/<slug>/suspend', methods=['POST'])
        def overseer_suspend(slug):
            if session.get('role') != 'admin':
                return redirect(url_for('saas_core.login'))
            cfg = self.load_client_config(slug)
            if cfg:
                cfg['status'] = 'suspended' if cfg.get('status') == 'active' else 'active'
                self.save_client_config(slug, cfg)
                flash(f'Store {cfg["status"]}.', 'success')
            return redirect(url_for('saas_core.overseer'))

        @bp.route('/overseer/client/<slug>/delete', methods=['POST'])
        def overseer_delete(slug):
            if session.get('role') != 'admin':
                return redirect(url_for('saas_core.login'))
            import shutil
            d = os.path.join(self.customers_dir, slug)
            if os.path.exists(d):
                shutil.rmtree(d)
            flash('Store deleted.', 'success')
            return redirect(url_for('saas_core.overseer'))

        # ── Account: change username + password ───────────────────────────────────────
        @bp.route('/account', methods=['GET', 'POST'])
        def account():
            if not session.get('logged_in'):
                return redirect(url_for('saas_core.login'))

            slug     = self.active_slug()
            username = session.get('username', '')
            is_admin = session.get('role') == 'admin'

            if request.method == 'POST':
                action       = request.form.get('action', '')
                current_pass = request.form.get('current_password', '').strip()
                new_pass     = request.form.get('new_password', '').strip()
                new_user     = request.form.get('new_username', '').strip()

                # --- Verify current password first ---
                verified = False
                if is_admin:
                    db = sqlite3.connect(self.db_file)
                    db.row_factory = sqlite3.Row
                    row = db.execute('SELECT * FROM admin_users WHERE username=?', (username,)).fetchone()
                    db.close()
                    verified = row and row['password'] == hash_pw(current_pass)
                elif slug:
                    upath = os.path.join(self.customers_dir, slug, 'users.json')
                    users = load_json(upath, {})
                    u = users.get(username, {})
                    verified = u.get('password') == hash_pw(current_pass)

                if not verified:
                    flash('Current password is incorrect.', 'error')
                    return render_template('account.html', username=username, **self.ctx())

                # --- Change password ---
                if action == 'change_password':
                    if len(new_pass) < 6:
                        flash('New password must be at least 6 characters.', 'error')
                        return render_template('account.html', username=username, **self.ctx())
                    if is_admin:
                        db = sqlite3.connect(self.db_file)
                        db.execute('UPDATE admin_users SET password=? WHERE username=?',
                                   (hash_pw(new_pass), username))
                        db.commit(); db.close()
                    elif slug:
                        upath = os.path.join(self.customers_dir, slug, 'users.json')
                        users = load_json(upath, {})
                        if username in users:
                            users[username]['password'] = hash_pw(new_pass)
                            save_json(upath, users)
                    flash('Password updated successfully!', 'success')

                # --- Change username / email ---
                elif action == 'change_username':
                    if not new_user:
                        flash('New username cannot be empty.', 'error')
                        return render_template('account.html', username=username, **self.ctx())
                    if is_admin:
                        db = sqlite3.connect(self.db_file)
                        # Check not taken
                        existing = db.execute('SELECT * FROM admin_users WHERE username=?', (new_user,)).fetchone()
                        if existing and existing['username'] != username:
                            db.close()
                            flash('That username is already taken.', 'error')
                            return render_template('account.html', username=username, **self.ctx())
                        db.execute('UPDATE admin_users SET username=? WHERE username=?', (new_user, username))
                        db.commit(); db.close()
                    elif slug:
                        upath = os.path.join(self.customers_dir, slug, 'users.json')
                        users = load_json(upath, {})
                        if username in users and new_user not in users:
                            users[new_user] = users.pop(username)
                            save_json(upath, users)
                        elif new_user in users:
                            flash('That email/username is already in use.', 'error')
                            return render_template('account.html', username=username, **self.ctx())
                    session['username'] = new_user
                    flash(f'Username updated to {new_user}!', 'success')

                return redirect(url_for('saas_core.account'))

            return render_template('account.html', username=username, **self.ctx())

        # ── Forgot password ────────────────────────────────────────────────
        @bp.route('/forgot-password', methods=['GET', 'POST'])
        def forgot_password():
            if request.method == 'POST':
                email = request.form.get('email', '').strip().lower()
                token = secrets.token_urlsafe(24)
                found = False
                resets_path = os.path.join(self.data_dir, 'password_resets.json')
                resets = load_json(resets_path, [])

                for store in self.list_client_stores():
                    upath = os.path.join(self.customers_dir, store['slug'], 'users.json')
                    users = load_json(upath, {})
                    if email in users:
                        found = True
                        resets = [r for r in resets if r.get('email') != email]
                        resets.append({
                            'email':   email,
                            'token':   token,
                            'slug':    store['slug'],
                            'expires': (datetime.datetime.now() + datetime.timedelta(hours=2)).isoformat(),
                            'created': datetime.datetime.now().isoformat()
                        })
                        break

                if found:
                    save_json(resets_path, resets)
                    flash(
                        f'Reset token generated. Visit: /reset-password/{token} '
                        f'(or copy the token: {token})', 'success'
                    )
                else:
                    flash('If that email is registered, a reset link has been generated.', 'info')
                return redirect(url_for('saas_core.forgot_password'))

            return render_template('forgot_password.html', **self.ctx())

        # ── Reset password ────────────────────────────────────────────────
        @bp.route('/reset-password/<token>', methods=['GET', 'POST'])
        def reset_password(token):
            resets_path = os.path.join(self.data_dir, 'password_resets.json')
            resets = load_json(resets_path, [])
            reset  = next((r for r in resets if r.get('token') == token), None)

            if not reset:
                flash('Invalid or expired reset link.', 'error')
                return redirect(url_for('saas_core.login'))

            if datetime.datetime.fromisoformat(reset['expires']) < datetime.datetime.now():
                flash('Reset link has expired. Please request a new one.', 'error')
                return redirect(url_for('saas_core.forgot_password'))

            if request.method == 'POST':
                new_pass = request.form.get('password', '').strip()
                if len(new_pass) < 6:
                    flash('Password must be at least 6 characters.', 'error')
                    return render_template('reset_password.html',
                                          token=token, email=reset.get('email',''),
                                          **self.ctx())
                slug  = reset['slug']
                email = reset['email']
                upath = os.path.join(self.customers_dir, slug, 'users.json')
                users = load_json(upath, {})
                if email in users:
                    users[email]['password'] = hash_pw(new_pass)
                    save_json(upath, users)
                resets = [r for r in resets if r.get('token') != token]
                save_json(resets_path, resets)
                flash('Password updated! You can now sign in.', 'success')
                return redirect(url_for('saas_core.login'))

            return render_template('reset_password.html',
                                   token=token, email=reset.get('email',''),
                                   **self.ctx())
