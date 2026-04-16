#!/usr/bin/env python3
"""
add-secret-key-persist.py — Fix session invalidation on Railway redeploy.
Replaces app.secret_key = static_string with list-it-everywhere's
persistent key pattern (saves to /data/secret_key file).
Usage: python3 add-secret-key-persist.py <app.py path>
"""
import sys, re, os

APP_FILE = sys.argv[1] if len(sys.argv) > 1 else "app.py"

SECRET_KEY_PATTERN = r"app\.secret_key\s*=\s*os\.environ\.get\(['\"]SECRET_KEY['\"][^)]*\)"

NEW_SECRET_KEY_CODE = """def _get_secret_key():
    env_key = os.environ.get('SECRET_KEY')
    if env_key:
        return env_key
    # Persist key to /data so sessions survive Railway redeploys
    data_dir = os.environ.get('RAILWAY_DATA_DIR') or os.environ.get('DATA_DIR') or '/data'
    key_file = os.path.join(data_dir, 'secret_key')
    try:
        os.makedirs(data_dir, exist_ok=True)
        if os.path.exists(key_file):
            with open(key_file) as f:
                key = f.read().strip()
            if key:
                return key
        import secrets as _sec
        key = _sec.token_hex(32)
        with open(key_file, 'w') as f:
            f.write(key)
        return key
    except Exception:
        import secrets as _sec
        return _sec.token_hex(32)

app.secret_key = _get_secret_key()
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'"""

content = open(APP_FILE).read()

if '_get_secret_key' in content:
    print(f"  ⏭  {APP_FILE} already has persistent secret key")
    sys.exit(0)

new = re.sub(SECRET_KEY_PATTERN, NEW_SECRET_KEY_CODE, content)
if new == content:
    # Try simpler fallback patterns
    for pat in [
        r"app\.secret_key\s*=\s*['\"][^'\"]+['\"]",
        r"app\.secret_key\s*=\s*os\.environ\.get\(['\"]SECRET_KEY['\"][^)]*\)[^\n]*",
    ]:
        new = re.sub(pat, NEW_SECRET_KEY_CODE, content)
        if new != content:
            break

if new == content:
    print(f"  ❌ Could not find app.secret_key pattern in {APP_FILE}")
    print("  Manual fix: replace app.secret_key line with _get_secret_key() pattern")
    sys.exit(1)

open(APP_FILE, 'w').write(new)
print(f"  ✅ {APP_FILE} — persistent secret key added")
