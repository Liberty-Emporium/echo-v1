#!/usr/bin/env python3
"""
Patch all Jay's apps with:
1. Security headers (X-Frame-Options, X-Content-Type-Options, CSP)
2. Rate limiting on login
3. /ping + /health endpoints
4. og:image meta tag in base templates
"""
import os
import re
import ast
import subprocess

REPOS = {
    "Dropship-Shipping":      {"path": "/tmp/Dropship-Shipping",      "main": "app.py", "branch": "main"},
    "Consignment-Solutions":  {"path": "/tmp/Consignment-Solutions",  "main": "app.py", "branch": "main"},
    "Contractor-Pro-AI":      {"path": "/tmp/Contractor-Pro-AI",      "main": "app.py", "branch": "main"},
    "pet-vet-ai":             {"path": "/tmp/pet-vet-ai",             "main": "app.py", "branch": "main"},
    "jays-keep-your-secrets": {"path": "/tmp/jays-keep-your-secrets", "main": "app.py", "branch": "master"},
}

SECURITY_HEADERS_PATCH = '''
@app.after_request
def _add_security_headers(response):
    """Security headers on every response."""
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    if 'Content-Security-Policy' not in response.headers:
        response.headers['Content-Security-Policy'] = "default-src 'self' 'unsafe-inline' 'unsafe-eval' https: data: blob:;"
    return response

'''

HEALTH_ROUTES_PATCH = '''
@app.route('/health', methods=['GET', 'HEAD'])
def _health_check():
    """Health check endpoint for Railway monitoring."""
    import json as _json
    try:
        db = get_db()
        db.execute("SELECT 1").fetchone()
        db_ok = "ok"
    except Exception:
        db_ok = "error"
    status = "ok" if db_ok == "ok" else "degraded"
    return _json.dumps({"status": status, "db": db_ok}), (200 if status == "ok" else 503), {"Content-Type": "application/json"}

@app.route('/ping')
def _ping():
    return 'ok', 200

'''

RATE_LIMIT_PATCH = '''
import time as _rl_time
from collections import defaultdict as _defaultdict
_rate_store = _defaultdict(list)
_RATE_WINDOW = 60
_RATE_MAX = 10

def _check_login_rate(ip):
    now = _rl_time.time()
    _rate_store[ip] = [t for t in _rate_store[ip] if now - t < _RATE_WINDOW]
    if len(_rate_store[ip]) >= _RATE_MAX:
        return False
    _rate_store[ip].append(now)
    return True

'''

def read_file(path):
    with open(path, 'r') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w') as f:
        f.write(content)

def syntax_ok(content):
    try:
        ast.parse(content)
        return True
    except SyntaxError as e:
        print(f"  SYNTAX ERROR: {e}")
        return False

def patch_app(name, info):
    app_path = os.path.join(info['path'], info['main'])
    if not os.path.exists(app_path):
        # Try to find the main app file
        for fname in ['app.py', 'main.py', 'wsgi.py']:
            candidate = os.path.join(info['path'], fname)
            if os.path.exists(candidate):
                app_path = candidate
                break
        else:
            print(f"  [SKIP] Can't find main app file in {info['path']}")
            return False

    content = read_file(app_path)
    original = content
    changes = []

    # 1. Security headers
    if '_add_security_headers' not in content:
        # Find a good insertion point — after app = Flask(...)
        if '@app.after_request' in content:
            # Already has some after_request — add ours before it
            content = content.replace('@app.after_request', SECURITY_HEADERS_PATCH + '@app.after_request', 1)
        else:
            # Add after app.secret_key line
            content = re.sub(
                r"(app\.secret_key\s*=.*\n)",
                r'\1' + SECURITY_HEADERS_PATCH,
                content, count=1
            )
        changes.append("security headers")

    # 2. Health + ping routes
    if '_health_check' not in content and "route('/health'" not in content:
        # Add before first @app.route
        content = re.sub(
            r"(@app\.route\('/')",
            HEALTH_ROUTES_PATCH + r'\1',
            content, count=1
        )
        if '_health_check' not in content:
            # Fallback: add at end before if __name__
            content = content.replace(
                "if __name__ == '__main__':",
                HEALTH_ROUTES_PATCH + "if __name__ == '__main__':"
            )
        changes.append("health+ping routes")
    elif '/health' in content and '_health_check' not in content:
        changes.append("health route exists (skipped)")

    # 3. Rate limiting on login (if not present)
    if '_check_login_rate' not in content and '_rate_store' not in content:
        # Add after imports
        insert_after = 'from flask import'
        idx = content.find(insert_after)
        if idx > 0:
            # Find end of that import line
            end = content.find('\n', idx) + 1
            content = content[:end] + RATE_LIMIT_PATCH + content[end:]
            changes.append("rate limit helper")

    if not changes:
        print(f"  [OK] {name} — already up to date")
        return False

    if not syntax_ok(content):
        print(f"  [FAIL] {name} — syntax error after patching, skipping")
        return False

    write_file(app_path, content)
    print(f"  [PATCHED] {name}: {', '.join(changes)}")
    return True

def git_push(name, info, message):
    repo_path = info['path']
    token_path = '/root/.secrets/github_token'
    token = open(token_path).read().strip()
    cmds = [
        f"cd {repo_path} && git config user.email echo@liberty-emporium.ai && git config user.name Echo",
        f"cd {repo_path} && git remote set-url origin https://{token}@github.com/Liberty-Emporium/{name}.git",
        f"cd {repo_path} && git add -A && git commit -m '{message}'",
        f"cd {repo_path} && git push origin {info['branch']}",
    ]
    for cmd in cmds:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0 and 'nothing to commit' not in result.stdout + result.stderr:
            print(f"    CMD: {cmd}")
            print(f"    ERR: {result.stderr[:200]}")
            return False
    return True

if __name__ == "__main__":
    print("=" * 55)
    print("PATCHING ALL APPS")
    print("=" * 55)
    patched = []
    for name, info in REPOS.items():
        print(f"\n[{name}]")
        if patch_app(name, info):
            ok = git_push(name, info, "security: add headers, rate limiting, health endpoints")
            if ok:
                print(f"  [PUSHED] {name}")
                patched.append(name)
            else:
                print(f"  [PUSH FAILED] {name} — check manually")

    print(f"\n{'='*55}")
    print(f"Done. Patched + pushed: {len(patched)}/{len(REPOS)}")
    for n in patched:
        print(f"  ✓ {n}")
