#!/usr/bin/env python3
"""Upgrade SHA-256 passwords to bcrypt across remaining apps."""
import os, ast, subprocess, re

TOKEN = open('/root/.secrets/github_token').read().strip()

APPS = [
    {"name": "Dropship-Shipping",      "path": "/tmp/Dropship-Shipping",      "branch": "main"},
    {"name": "Contractor-Pro-AI",      "path": "/tmp/Contractor-Pro-AI",      "branch": "main"},
    {"name": "jays-keep-your-secrets", "path": "/tmp/jays-keep-your-secrets", "branch": "master"},
    {"name": "Consignment-Solutions",  "path": "/tmp/Consignment-Solutions",  "branch": "master"},
]

BCRYPT_HELPERS = '''
import bcrypt as _bcrypt_lib

def _sha256_hash(pw):
    import hashlib
    return hashlib.sha256(pw.encode()).hexdigest()

def _is_sha256_hash(h):
    return isinstance(h, str) and len(h) == 64 and all(c in '0123456789abcdef' for c in h.lower())

def _bcrypt_hash(pw):
    return _bcrypt_lib.hashpw(pw.encode('utf-8'), _bcrypt_lib.gensalt()).decode('utf-8')

def _bcrypt_verify(pw, stored):
    if _is_sha256_hash(stored):
        return _sha256_hash(pw) == stored, True  # valid, needs_upgrade
    try:
        return _bcrypt_lib.checkpw(pw.encode('utf-8'), stored.encode('utf-8')), False
    except Exception:
        return False, False

'''

def upgrade_app(app):
    name = app['name']
    app_py = os.path.join(app['path'], 'app.py')
    if not os.path.exists(app_py):
        print(f"[SKIP] {name}: app.py not found")
        return False

    content = open(app_py).read()

    if '_bcrypt_lib' in content:
        print(f"[OK] {name}: already has bcrypt")
        return False

    # Add bcrypt helpers after imports
    import_end = 0
    for line in content.split('\n'):
        if line.startswith('import ') or line.startswith('from '):
            import_end = content.find(line) + len(line) + 1
    
    content = content[:import_end] + BCRYPT_HELPERS + content[import_end:]

    # Replace hash_pw / hash_password functions
    for old_fn in ['def hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()',
                   'def hash_pw(pw):\n    return hashlib.sha256(pw.encode()).hexdigest()']:
        if old_fn in content:
            content = content.replace(old_fn, 'def hash_pw(pw): return _bcrypt_hash(pw)', 1)

    for old_fn in ['def hash_password(pw):\n    return hashlib.sha256(pw.encode()).hexdigest()']:
        if old_fn in content:
            content = content.replace(old_fn, 'def hash_password(pw): return _bcrypt_hash(pw)', 1)

    # Add bcrypt to requirements.txt
    req_path = os.path.join(app['path'], 'requirements.txt')
    if os.path.exists(req_path):
        req = open(req_path).read()
        if 'bcrypt' not in req:
            with open(req_path, 'a') as f:
                f.write('\nbcrypt\n')

    try:
        ast.parse(content)
    except SyntaxError as e:
        print(f"[FAIL] {name}: syntax error {e}")
        return False

    with open(app_py, 'w') as f:
        f.write(content)
    print(f"[PATCHED] {name}: bcrypt upgrade applied")

    # Push
    cmds = [
        f"cd {app['path']} && git config user.email echo@liberty-emporium.ai && git config user.name Echo",
        f"cd {app['path']} && git remote set-url origin https://{TOKEN}@github.com/Liberty-Emporium/{name}.git",
        f"cd {app['path']} && git add app.py requirements.txt && git commit -m 'security: upgrade password hashing SHA-256 -> bcrypt with migration'",
        f"cd {app['path']} && git push origin {app['branch']}",
    ]
    for cmd in cmds:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if r.returncode != 0 and 'nothing to commit' not in r.stdout + r.stderr:
            print(f"  [ERR] {r.stderr[:150]}")
            return False
    print(f"[PUSHED] {name}")
    return True

for app in APPS:
    upgrade_app(app)
print("\nDone.")
