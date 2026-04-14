"""
settings_routes.py — Drop-in Settings System (Multi-Tenant)
Adds a full /settings section to any Flask multi-tenant app.

Setup:
  1. Copy this file + key_vault.py into your app
  2. Register the blueprint in app.py:
       from settings_routes import settings_bp
       app.register_blueprint(settings_bp)
  3. Add init_key_vault(db) to your init_db()
  4. Create templates/settings/ folder with the templates below
     OR use the pre-built ones from echo-v1/tools/templates/settings/

Provides these routes:
  GET  /settings              → profile + password
  POST /settings/profile      → update name/email
  POST /settings/password     → change password
  GET  /settings/integrations → API keys (BYOK)
  POST /settings/integrations → save/delete API keys
  GET  /settings/team         → team members (teams plan)
  POST /settings/team/invite  → invite team member
  POST /settings/team/remove  → remove team member
  GET  /settings/billing      → plan + usage
  GET  /settings/branding     → tenant name/logo
  POST /settings/branding     → save branding
"""

import hashlib
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, g, jsonify
from key_vault import save_api_key, get_api_key, has_own_key, mask_key, init_key_vault

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')

# ── Helpers (assumes your app has these patterns) ─────────────────────────────

def get_db():
    return g._database

def get_current_user():
    if 'user_id' not in session:
        return None
    return get_db().execute(
        "SELECT u.*, t.name as tenant_name, t.plan, t.trial_ends_at, t.ai_credits_used "
        "FROM users u LEFT JOIN tenants t ON u.tenant_id=t.id WHERE u.id=?",
        (session['user_id'],)
    ).fetchone()

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# Plan limits reference
PLANS = {
    "trial":   {"name": "Free Trial",  "listings": 50,   "ai_credits": 50,   "team_seats": 1,  "price": 0},
    "starter": {"name": "Starter",     "listings": 100,  "ai_credits": 100,  "team_seats": 1,  "price": 19.95},
    "pro":     {"name": "Pro",         "listings": 9999, "ai_credits": 9999, "team_seats": 3,  "price": 39.95},
    "teams":   {"name": "Teams",       "listings": 9999, "ai_credits": 9999, "team_seats": 10, "price": 79.95},
}

INTEGRATIONS = [
    {"service": "openrouter", "label": "OpenRouter API Key",  "placeholder": "sk-or-...",    "help": "Powers all AI features. Get yours free at openrouter.ai"},
    {"service": "stripe",     "label": "Stripe Secret Key",   "placeholder": "sk_live_...", "help": "For accepting payments in your account"},
    {"service": "square",     "label": "Square Access Token", "placeholder": "EAAAlBB...",   "help": "For Square POS integration"},
    {"service": "sendgrid",   "label": "SendGrid API Key",    "placeholder": "SG...",        "help": "For sending emails from your account"},
]

# ── Routes ────────────────────────────────────────────────────────────────────

@settings_bp.route("/")
@login_required
def settings_index():
    user = get_current_user()
    return render_template("settings/index.html", user=user, active="profile")

@settings_bp.route("/profile", methods=["POST"])
@login_required
def update_profile():
    user = get_current_user()
    db = get_db()
    name  = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    if not email:
        flash("Email is required.", "error")
        return redirect(url_for('settings.settings_index'))
    # Check email not taken by another user
    existing = db.execute("SELECT id FROM users WHERE email=? AND id!=?", (email, user['id'])).fetchone()
    if existing:
        flash("That email is already in use.", "error")
        return redirect(url_for('settings.settings_index'))
    db.execute("UPDATE users SET email=? WHERE id=?", (email, user['id']))
    if name:
        db.execute("UPDATE tenants SET name=? WHERE id=?", (name, session['tenant_id']))
    db.commit()
    session_user_email = email
    flash("Profile updated.", "success")
    return redirect(url_for('settings.settings_index'))

@settings_bp.route("/password", methods=["POST"])
@login_required
def change_password():
    user = get_current_user()
    db = get_db()
    current = request.form.get("current_password", "")
    new_pw  = request.form.get("new_password", "")
    confirm = request.form.get("confirm_password", "")
    # Verify current password
    row = db.execute("SELECT password_hash FROM users WHERE id=?", (user['id'],)).fetchone()
    if row['password_hash'] != hash_pw(current):
        flash("Current password is incorrect.", "error")
        return redirect(url_for('settings.settings_index'))
    if len(new_pw) < 6:
        flash("New password must be at least 6 characters.", "error")
        return redirect(url_for('settings.settings_index'))
    if new_pw != confirm:
        flash("Passwords don't match.", "error")
        return redirect(url_for('settings.settings_index'))
    db.execute("UPDATE users SET password_hash=? WHERE id=?", (hash_pw(new_pw), user['id']))
    db.commit()
    flash("Password changed successfully.", "success")
    return redirect(url_for('settings.settings_index'))

@settings_bp.route("/integrations")
@login_required
def integrations():
    user = get_current_user()
    db = get_db()
    tid = session['tenant_id']
    # Build integration status list
    integration_status = []
    for integ in INTEGRATIONS:
        integration_status.append({
            **integ,
            "has_key": has_own_key(db, tid, integ['service']),
            "masked":  mask_key(db, tid, integ['service']),
        })
    return render_template("settings/integrations.html", user=user,
                           integrations=integration_status, active="integrations")

@settings_bp.route("/integrations", methods=["POST"])
@login_required
def save_integrations():
    db = get_db()
    tid = session['tenant_id']
    uid = session['user_id']
    saved = []
    cleared = []
    for integ in INTEGRATIONS:
        key_val = request.form.get(f"key_{integ['service']}", "").strip()
        if key_val == "":
            continue  # Don't touch keys not submitted
        if key_val == "CLEAR":
            save_api_key(db, tid, integ['service'], "", user_id=uid)
            cleared.append(integ['label'])
        else:
            save_api_key(db, tid, integ['service'], key_val, label=integ['label'], user_id=uid)
            saved.append(integ['label'])
    if saved:
        flash(f"Saved: {', '.join(saved)}", "success")
    if cleared:
        flash(f"Cleared: {', '.join(cleared)}", "success")
    if not saved and not cleared:
        flash("No changes made.", "success")
    return redirect(url_for('settings.integrations'))

@settings_bp.route("/team")
@login_required
def team():
    user = get_current_user()
    db = get_db()
    tid = session['tenant_id']
    plan = PLANS.get(user['plan'] or 'trial', PLANS['trial'])
    members = db.execute(
        "SELECT id, email, role, created_at FROM users WHERE tenant_id=? ORDER BY created_at",
        (tid,)
    ).fetchall()
    return render_template("settings/team.html", user=user, members=members,
                           plan=plan, active="team")

@settings_bp.route("/team/remove", methods=["POST"])
@login_required
def remove_member():
    user = get_current_user()
    db = get_db()
    tid = session['tenant_id']
    member_id = request.form.get("member_id")
    if str(member_id) == str(user['id']):
        flash("You can't remove yourself.", "error")
        return redirect(url_for('settings.team'))
    db.execute("DELETE FROM users WHERE id=? AND tenant_id=? AND role!='owner'", (member_id, tid))
    db.commit()
    flash("Team member removed.", "success")
    return redirect(url_for('settings.team'))

@settings_bp.route("/billing")
@login_required
def billing():
    user = get_current_user()
    db = get_db()
    tid = session['tenant_id']
    plan = PLANS.get(user['plan'] or 'trial', PLANS['trial'])
    listing_count = db.execute("SELECT COUNT(*) as c FROM listings WHERE tenant_id=?", (tid,)).fetchone()['c']
    return render_template("settings/billing.html", user=user, plan=plan,
                           listing_count=listing_count, plans=PLANS, active="billing")

@settings_bp.route("/branding", methods=["GET", "POST"])
@login_required
def branding():
    user = get_current_user()
    db = get_db()
    tid = session['tenant_id']
    if request.method == "POST":
        name = request.form.get("tenant_name", "").strip()
        if name:
            db.execute("UPDATE tenants SET name=? WHERE id=?", (name, tid))
            db.commit()
            flash("Branding updated.", "success")
        return redirect(url_for('settings.branding'))
    tenant = db.execute("SELECT * FROM tenants WHERE id=?", (tid,)).fetchone()
    return render_template("settings/branding.html", user=user, tenant=tenant, active="branding")
