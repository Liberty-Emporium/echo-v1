"""
example_app.py — Minimal working SaaS app using saas_core.py
Shows exactly how to drop saas_core into a new Flask app in under 5 minutes.
"""

from flask import Flask, render_template, session, redirect, url_for, request, flash
import os
import json
from saas_core import SaaSCore, load_json, save_json

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'example-secret-2026')

# ── 1. Initialize SaaSCore ────────────────────────────────────────────────────
core = SaaSCore(
    app,
    app_name="My SaaS App",
    monthly_price=99.00,
    trial_days=14
)

# ── 2. Your app routes — use core decorators and helpers ──────────────────────

@app.route('/')
def index():
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    return render_template('landing.html', **core.ctx())

@app.route('/dashboard')
@core.login_required
def dashboard():
    slug    = core.active_slug()
    # Load tenant-scoped data
    items   = load_json(core.data_path('items.json', slug))
    return render_template('dashboard.html', items=items, **core.ctx())

@app.route('/items/add', methods=['POST'])
@core.login_required
def add_item():
    slug  = core.active_slug()
    items = load_json(core.data_path('items.json', slug))
    items.append({
        'name':  request.form.get('name'),
        'value': request.form.get('value'),
    })
    save_json(core.data_path('items.json', slug), items)
    flash('Item added!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/healthz')
def healthz():
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
