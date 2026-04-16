#!/usr/bin/env python3
"""
new-app.py — Scaffold a new Liberty-Emporium Flask SaaS app from scratch.
Generates app.py, templates/, requirements.txt, railway.json, Dockerfile, start.sh.
Usage: python3 new-app.py <app-name> "<description>" <price>
Example: python3 new-app.py MyNewApp "AI tool for X" "$29/mo"
"""
import os, sys

APP_NAME = sys.argv[1] if len(sys.argv) > 1 else "NewApp"
DESCRIPTION = sys.argv[2] if len(sys.argv) > 2 else f"AI-powered {APP_NAME}"
PRICE = sys.argv[3] if len(sys.argv) > 3 else "$29/mo"
SLUG = APP_NAME.lower().replace(" ", "-")
OUT_DIR = f"/tmp/{SLUG}"

os.makedirs(f"{OUT_DIR}/templates", exist_ok=True)
os.makedirs(f"{OUT_DIR}/static", exist_ok=True)

# ── app.py ────────────────────────────────────────────────────────────────
open(f"{OUT_DIR}/app.py", 'w').write(f'''"""
{APP_NAME} — {DESCRIPTION}
Pricing: {PRICE}
"""
import os, sqlite3, hashlib, secrets, datetime, json
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, g

app = Flask(__name__)

# ── Secret key (persists across Railway redeploys) ─────────────────────
def _get_secret_key():
    env_key = os.environ.get("SECRET_KEY")
    if env_key: return env_key
    data_dir = os.environ.get("DATA_DIR", "/data")
    key_file = os.path.join(data_dir, "secret_key")
    try:
        os.makedirs(data_dir, exist_ok=True)
        if os.path.exists(key_file):
            with open(key_file) as f: return f.read().strip()
        key = secrets.token_hex(32)
        open(key_file, "w").write(key)
        return key
    except Exception:
        return secrets.token_hex(32)

app.secret_key = _get_secret_key()
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(hours=8)

# ── Paths ──────────────────────────────────────────────────────────────
DATA_DIR  = os.environ.get("DATA_DIR", "/data")
DB_PATH   = os.path.join(DATA_DIR, "{slug}.db")
os.makedirs(DATA_DIR, exist_ok=True)

ADMIN_USER = "admin"
ADMIN_PASS = os.environ.get("ADMIN_PASSWORD", "admin123")

# ── Database ───────────────────────────────────────────────────────────
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.execute("PRAGMA journal_mode=WAL")
        g.db.execute("PRAGMA synchronous=NORMAL")
        g.db.execute("PRAGMA foreign_keys=ON")
        g.db.execute("PRAGMA busy_timeout=5000")
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop("db", None)
    if db: db.close()

def init_db():
    db = sqlite3.connect(DB_PATH)
    db.executescript("""
        PRAGMA journal_mode=WAL;
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT DEFAULT "",
            role TEXT DEFAULT "user",
            plan TEXT DEFAULT "trial",
            status TEXT DEFAULT "active",
            joined TEXT DEFAULT (date("now"))
        );
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event TEXT, value TEXT, ts TEXT DEFAULT (datetime("now"))
        );
    """)
    db.commit()
    # Create default admin
    import hashlib
    pw = hashlib.sha256(ADMIN_PASS.encode()).hexdigest()
    try:
        db.execute("INSERT OR IGNORE INTO users (username,password,role,plan) VALUES (?,?,?,?)",
                   (ADMIN_USER, pw, "admin", "enterprise"))
        db.commit()
    except: pass
    db.close()

init_db()

# ── Auth ───────────────────────────────────────────────────────────────
def hash_pw(pw): return __import__("hashlib").sha256(pw.encode()).hexdigest()

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("username") != ADMIN_USER:
            flash("Admin access required.", "error")
            return redirect(url_for("dashboard"))
        return f(*args, **kwargs)
    return decorated

# ── CSRF ───────────────────────────────────────────────────────────────
import secrets as _sec
def _get_csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = _sec.token_hex(32)
    return session["csrf_token"]

app.jinja_env.globals["csrf_token"] = _get_csrf_token

# ── Security headers ───────────────────────────────────────────────────
@app.after_request
def add_security_headers(response):
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

# ── Context ────────────────────────────────────────────────────────────
@app.context_processor
def inject_globals():
    return dict(app_name="{APP_NAME}", app_price="{PRICE}")

# ── Routes ─────────────────────────────────────────────────────────────
@app.route("/")
def index():
    if session.get("logged_in"):
        return redirect(url_for("dashboard"))
    return render_template("landing.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if session.get("logged_in"):
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        username = request.form.get("username","").strip()
        password = request.form.get("password","")
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        if user and user["password"] == hash_pw(password):
            if user["status"] == "suspended":
                flash("Your account is suspended. Contact support.", "error")
                return render_template("login.html")
            session["logged_in"]  = True
            session["username"]   = username
            session["role"]       = user["role"]
            session.permanent     = True
            flash(f"Welcome back, {{username}}!", "success")
            return redirect(url_for("dashboard"))
        flash("Invalid username or password.", "error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/health")
def health():
    try:
        get_db().execute("SELECT 1")
        return jsonify({{"status":"ok","db":"ok"}}), 200
    except Exception as e:
        return jsonify({{"status":"degraded","error":str(e)}}), 503

@app.route("/api/status")
def api_status():
    return jsonify({{"app":"{APP_NAME}","status":"ok","version":"1.0.0"}})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
'''.format(APP_NAME=APP_NAME, DESCRIPTION=DESCRIPTION, PRICE=PRICE, slug=SLUG))

# ── railway.json ────────────────────────────────────────────────────────
open(f"{OUT_DIR}/railway.json", 'w').write(f'''{{"$schema":"https://railway.app/railway.schema.json","build":{{}},"deploy":{{"numReplicas":1,"restartPolicyType":"ON_FAILURE","restartPolicyMaxRetries":10,"startCommand":"gunicorn app:app --bind 0.0.0.0:$PORT","numWorkers":1,"volume":"/data"}}}}''')

# ── requirements.txt ────────────────────────────────────────────────────
open(f"{OUT_DIR}/requirements.txt", 'w').write("flask\ngunicorn\nrequests\nbcrypt\npython-dotenv\n")

# ── README ─────────────────────────────────────────────────────────────
open(f"{OUT_DIR}/README.md", 'w').write(f"# {APP_NAME}\n\n{DESCRIPTION}\n\n## Pricing\n{PRICE}\n\n## Deploy\nPush to GitHub → Railway auto-deploys.\n\n## Default Login\n- Username: `admin`\n- Password: `admin123` (or set `ADMIN_PASSWORD` env var)\n")

# ── Minimal templates ───────────────────────────────────────────────────
open(f"{OUT_DIR}/templates/login.html", 'w').write(f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Login | {APP_NAME}</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:Inter,sans-serif;min-height:100vh;background:linear-gradient(135deg,#0f172a,#1e293b);display:flex;align-items:center;justify-content:center;padding:1rem}}
.card{{background:white;border-radius:16px;padding:2.5rem 2rem;width:100%;max-width:400px;box-shadow:0 20px 60px rgba(0,0,0,0.3)}}
h1{{font-size:1.5rem;font-weight:800;color:#0f172a;margin-bottom:0.25rem}}.sub{{color:#64748b;font-size:0.9rem;margin-bottom:1.75rem}}
label{{display:block;font-size:0.85rem;font-weight:600;color:#374151;margin-bottom:0.3rem;margin-top:1rem}}
input{{width:100%;padding:0.65rem 0.9rem;border:1.5px solid #e2e8f0;border-radius:8px;font-size:0.95rem;outline:none;transition:border-color .2s}}
input:focus{{border-color:#6366f1}}.btn{{display:block;width:100%;margin-top:1.5rem;padding:0.85rem;background:#6366f1;color:white;border:none;border-radius:10px;font-size:1rem;font-weight:700;cursor:pointer;transition:background .2s}}
.btn:hover{{background:#4f46e5}}.flash{{padding:0.65rem 1rem;border-radius:8px;font-size:0.88rem;margin-bottom:1rem}}
.flash.success{{background:#d1fae5;color:#065f46}}.flash.error{{background:#fee2e2;color:#b91c1c}}
</style></head><body>
<div class="card">
  <h1>🔐 {APP_NAME}</h1><p class="sub">Sign in to your account</p>
  {{% for cat,msg in get_flashed_messages(with_categories=true) %}}<div class="flash {{{{cat}}}}">{{{{msg}}}}</div>{{% endfor %}}
  <form method="POST" action="{{{{url_for('login')}}}}">
    <input type="hidden" name="csrf_token" value="{{{{csrf_token()}}}}">
    <label>Username</label><input type="text" name="username" required autofocus placeholder="admin">
    <label>Password</label><input type="password" name="password" required placeholder="••••••••">
    <button type="submit" class="btn">Sign In →</button>
  </form>
</div></body></html>''')

open(f"{OUT_DIR}/templates/dashboard.html", 'w').write(f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Dashboard | {APP_NAME}</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:Inter,sans-serif;background:#f8fafc;color:#0f172a}}
.nav{{background:#0f172a;padding:0 1.5rem;height:60px;display:flex;align-items:center;justify-content:space-between}}
.nav-brand{{color:white;font-weight:800;font-size:1rem}}.nav-user{{color:#94a3b8;font-size:0.85rem}}
.nav a{{color:#94a3b8;text-decoration:none;font-size:0.85rem;margin-left:1rem}}.nav a:hover{{color:white}}
.main{{max-width:1100px;margin:2rem auto;padding:0 1.5rem}}
.page-title{{font-size:1.5rem;font-weight:800;margin-bottom:1.5rem}}
.card{{background:white;border-radius:14px;padding:1.5rem;box-shadow:0 2px 12px rgba(0,0,0,0.07)}}
</style></head><body>
<nav class="nav">
  <span class="nav-brand">⚡ {APP_NAME}</span>
  <div><span class="nav-user">{{{{session.username}}}}</span><a href="{{{{url_for('logout')}}}}">Logout</a></div>
</nav>
<div class="main">
  {{% for cat,msg in get_flashed_messages(with_categories=true) %}}
  <div style="padding:.65rem 1rem;border-radius:8px;margin-bottom:1rem;background:{{% if cat=='success' %}}#d1fae5;color:#065f46{{% elif cat=='error' %}}#fee2e2;color:#b91c1c{{% else %}}#e0e7ff;color:#3730a3{{% endif %}}">{{{{msg}}}}</div>
  {{% endfor %}}
  <h1 class="page-title">Dashboard</h1>
  <div class="card"><p>Welcome to {APP_NAME}. Build your features here.</p></div>
</div></body></html>''')

open(f"{OUT_DIR}/templates/landing.html", 'w').write(f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{APP_NAME} — {DESCRIPTION}</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://unpkg.com/aos@2.3.1/dist/aos.css">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:Inter,sans-serif;color:#0f172a;background:#fff}}
.hero{{background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);padding:5rem 1.5rem 4rem;text-align:center;position:relative;overflow:hidden}}
.hero::before{{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 80% 50% at 50% -20%,rgba(99,102,241,.3),transparent),radial-gradient(ellipse 60% 40% at 80% 50%,rgba(168,85,247,.15),transparent)}}
.hero-inner{{position:relative;max-width:760px;margin:0 auto}}
.badge{{display:inline-block;background:rgba(99,102,241,.2);color:#a5b4fc;border:1px solid rgba(99,102,241,.3);border-radius:20px;padding:.3rem .9rem;font-size:.8rem;font-weight:700;margin-bottom:1.25rem;letter-spacing:.05em}}
h1{{font-size:clamp(2rem,5vw,3.25rem);font-weight:900;color:white;line-height:1.15;margin-bottom:1rem}}
.hero p{{color:#94a3b8;font-size:1.1rem;margin-bottom:2rem;line-height:1.6}}
.cta-btn{{display:inline-block;background:#6366f1;color:white;padding:.9rem 2.25rem;border-radius:12px;font-weight:800;font-size:1rem;text-decoration:none;box-shadow:0 4px 20px rgba(99,102,241,.4);transition:all .2s}}
.cta-btn:hover{{background:#4f46e5;transform:translateY(-2px);box-shadow:0 8px 30px rgba(99,102,241,.5)}}
.price-note{{color:#64748b;font-size:.85rem;margin-top:.75rem}}
.features{{max-width:1100px;margin:4rem auto;padding:0 1.5rem;display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1.5rem}}
.feature-card{{background:#f8fafc;border-radius:14px;padding:1.75rem;border:1px solid #e2e8f0;transition:box-shadow .2s}}
.feature-card:hover{{box-shadow:0 8px 24px rgba(0,0,0,.08)}}
.feature-icon{{font-size:2rem;margin-bottom:.75rem}}
.feature-card h3{{font-size:1rem;font-weight:700;margin-bottom:.4rem}}
.feature-card p{{font-size:.88rem;color:#64748b;line-height:1.5}}
.cta-section{{background:#0f172a;padding:4rem 1.5rem;text-align:center}}
.cta-section h2{{color:white;font-size:1.75rem;font-weight:800;margin-bottom:.75rem}}
.cta-section p{{color:#94a3b8;margin-bottom:2rem}}
</style></head>
<body>
<section class="hero">
  <div class="hero-inner">
    <div class="badge">✨ Now Available</div>
    <h1>{APP_NAME}</h1>
    <p>{DESCRIPTION}</p>
    <a href="{{{{url_for('login')}}}}" class="cta-btn">Start Free Trial →</a>
    <p class="price-note">{PRICE} · 14-day free trial · No credit card required</p>
  </div>
</section>
<div class="features">
  <div class="feature-card" data-aos="fade-up"><div class="feature-icon">🤖</div><h3>AI-Powered</h3><p>Smart automation handles the heavy lifting so you can focus on what matters.</p></div>
  <div class="feature-card" data-aos="fade-up" data-aos-delay="100"><div class="feature-icon">⚡</div><h3>Fast Setup</h3><p>Get started in minutes. No technical knowledge required.</p></div>
  <div class="feature-card" data-aos="fade-up" data-aos-delay="200"><div class="feature-icon">📊</div><h3>Real Insights</h3><p>Track everything that matters with clear dashboards and reports.</p></div>
</div>
<section class="cta-section">
  <h2>Ready to get started?</h2>
  <p>Join hundreds of businesses using {APP_NAME} today.</p>
  <a href="{{{{url_for('login')}}}}" class="cta-btn">Get Started Free →</a>
</section>
<script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
<script>AOS.init({{duration:600,once:true}});</script>
</body></html>''')

print(f"\n✅ Scaffolded {APP_NAME} at {OUT_DIR}")
print(f"   Files: app.py, templates/, railway.json, requirements.txt, README.md")
print(f"\n   Next steps:")
print(f"   1. cd {OUT_DIR}")
print(f"   2. Add your features to app.py")
print(f"   3. Push to GitHub → Railway deploys automatically")
print(f"   4. Default login: admin / admin123")
