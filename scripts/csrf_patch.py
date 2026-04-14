#!/usr/bin/env python3
"""
Add lightweight CSRF protection to all apps.
Uses Flask session-based tokens — no external deps.
"""
import os, ast, subprocess, re

TOKEN = open('/root/.secrets/github_token').read().strip()

APPS = [
    {"name": "Dropship-Shipping",      "path": "/tmp/Dropship-Shipping",      "branch": "main"},
    {"name": "Contractor-Pro-AI",      "path": "/tmp/Contractor-Pro-AI",      "branch": "main"},
    {"name": "pet-vet-ai",             "path": "/tmp/pet-vet-ai",             "branch": "main"},
    {"name": "jays-keep-your-secrets", "path": "/tmp/jays-keep-your-secrets", "branch": "master"},
    {"name": "Consignment-Solutions",  "path": "/tmp/Consignment-Solutions",  "branch": "master"},
    {"name": "Liberty-Emporium-Inventory-App", "path": "/tmp/Liberty-Emporium-Inventory-App", "branch": "main"},
]

CSRF_CODE = '''
import secrets as _secrets_module

def _get_csrf_token():
    """Generate or retrieve CSRF token from session."""
    if 'csrf_token' not in session:
        session['csrf_token'] = _secrets_module.token_hex(32)
    return session['csrf_token']

def _validate_csrf():
    """Validate CSRF token on POST requests. Returns True if valid."""
    if request.method != 'POST':
        return True
    # Skip API routes
    if request.path.startswith('/api/'):
        return True
    token = request.form.get('csrf_token') or request.headers.get('X-CSRF-Token')
    return token and token == session.get('csrf_token')

app.jinja_env.globals['csrf_token'] = _get_csrf_token

'''

def patch_app(app):
    name = app['name']
    app_py = os.path.join(app['path'], 'app.py')
    if not os.path.exists(app_py):
        app_py = os.path.join(app['path'], 'app_with_ai.py')
    if not os.path.exists(app_py):
        print(f"  [SKIP] {name}: no app file found")
        return False

    content = open(app_py).read()

    if '_get_csrf_token' in content:
        print(f"  [OK] {name}: CSRF already present")
        return False

    # Insert CSRF code after app.secret_key line
    pattern = r"(app\.secret_key\s*=.*\n)"
    if re.search(pattern, content):
        content = re.sub(pattern, r'\1' + CSRF_CODE, content, count=1)
    else:
        print(f"  [SKIP] {name}: can't find insertion point")
        return False

    try:
        ast.parse(content)
    except SyntaxError as e:
        print(f"  [FAIL] {name}: syntax error {e}")
        return False

    with open(app_py, 'w') as f:
        f.write(content)

    # Push
    branch = app['branch']
    fname = os.path.basename(app_py)
    cmds = [
        f"cd {app['path']} && git config user.email echo@liberty-emporium.ai && git config user.name Echo",
        f"cd {app['path']} && git remote set-url origin https://{TOKEN}@github.com/Liberty-Emporium/{name}.git",
        f"cd {app['path']} && git add {fname} && git commit -m 'security: add CSRF token protection to all forms'",
        f"cd {app['path']} && git push origin {branch}",
    ]
    for cmd in cmds:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if r.returncode != 0 and 'nothing to commit' not in r.stdout + r.stderr:
            print(f"  [ERR] {r.stderr[:150]}")
            return False
    print(f"  [PUSHED] {name}: CSRF protection added")
    return True

print("=" * 50)
print("ADDING CSRF PROTECTION")
print("=" * 50)
for app in APPS:
    print(f"\n[{app['name']}]")
    patch_app(app)
print("\nDone.")
