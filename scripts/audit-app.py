#!/usr/bin/env python3
"""
audit-app.py — Full pre-deploy audit of a Flask app.
Checks: secret key, CSRF, session config, health endpoint, WAL mode,
missing csrf tokens in forms, hardcoded passwords, url_for mismatches.
Usage: python3 audit-app.py <app-dir>
"""
import os, re, sys

APP_DIR = sys.argv[1] if len(sys.argv) > 1 else "."
APP_FILE = os.path.join(APP_DIR, "app.py")
if not os.path.exists(APP_FILE):
    APP_FILE = next((os.path.join(APP_DIR, f) for f in os.listdir(APP_DIR) if f.endswith('.py') and 'app' in f.lower()), None)

TEMPLATES_DIR = os.path.join(APP_DIR, "templates")
issues = []
warns  = []
passes = []

def check(cond, label, severity="issue"):
    if cond:
        passes.append(f"✅ {label}")
    else:
        (issues if severity=="issue" else warns).append(f"{'❌' if severity=='issue' else '⚠️ '} {label}")

if not APP_FILE or not os.path.exists(APP_FILE):
    print("❌ No app.py found"); sys.exit(1)

app_code = open(APP_FILE).read()
tmpl_files = {}
if os.path.isdir(TEMPLATES_DIR):
    for f in os.listdir(TEMPLATES_DIR):
        if f.endswith('.html'):
            tmpl_files[f] = open(os.path.join(TEMPLATES_DIR, f)).read()

# ── App code checks ───────────────────────────────────────────────────────
check('_get_secret_key' in app_code or "secret_key" in app_code, "secret_key set")
check('_get_secret_key' in app_code, "secret_key persists across redeploys (session-safe)")
check("journal_mode=WAL" in app_code, "SQLite WAL mode enabled")
check("@app.route('/health'" in app_code or "'/health'" in app_code, "/health endpoint exists")
check("login_required" in app_code, "login_required decorator exists")
check("SESSION_COOKIE_HTTPONLY" in app_code or "httponly" in app_code.lower(), "Session cookie httponly set")
check("SESSION_COOKIE_SAMESITE" in app_code or "samesite" in app_code.lower(), "Session cookie samesite set")
check("rate_limit" in app_code or "Rate" in app_code, "Rate limiting present")
check("add_security_headers" in app_code or "X-Frame-Options" in app_code, "Security headers present")
check("ADMIN_PASSWORD" in app_code, "Admin password from env var")

# Check for hardcoded passwords (not in env)
hardcoded = re.findall(r"ADMIN_PASS\s*=\s*['\"](?!os\.environ)[^'\"]{4,}['\"]", app_code)
check(not hardcoded, f"No hardcoded admin passwords ({hardcoded})", "issue" if hardcoded else "issue")

# ── Template checks ───────────────────────────────────────────────────────
post_forms_missing_csrf = []
for fname, content in tmpl_files.items():
    # Find POST forms without csrf_token
    forms = re.findall(r'<form[^>]+method=["\'](?:POST|post)["\'][^>]*>.*?</form>', content, re.DOTALL)
    for form in forms:
        if 'csrf_token' not in form and 'api/' not in form:
            post_forms_missing_csrf.append(fname)
            break

check(not post_forms_missing_csrf,
      f"All POST forms have csrf_token" if not post_forms_missing_csrf
      else f"POST forms missing csrf_token: {', '.join(post_forms_missing_csrf)}")

# Find all url_for() calls and check function names exist
url_for_calls = re.findall(r"url_for\(['\"](\w+)['\"]", app_code + " ".join(tmpl_files.values()))
route_functions = set(re.findall(r"^def (\w+)\(", app_code, re.MULTILINE))
bad_url_fors = [u for u in set(url_for_calls) if u not in route_functions and u not in ('static',)]
check(not bad_url_fors,
      f"All url_for() names are valid" if not bad_url_fors
      else f"Bad url_for() calls: {bad_url_fors}")

# ── Report ────────────────────────────────────────────────────────────────
print(f"\n{'='*55}")
print(f"  Audit: {os.path.basename(APP_DIR or '.')}")
print(f"{'='*55}")
for p in passes:  print(f"  {p}")
for w in warns:   print(f"  {w}")
for i in issues:  print(f"  {i}")
print(f"{'='*55}")
print(f"  ✅ {len(passes)} passed | ⚠️  {len(warns)} warnings | ❌ {len(issues)} issues")
print(f"{'='*55}\n")
sys.exit(1 if issues else 0)
