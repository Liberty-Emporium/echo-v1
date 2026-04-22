# Security Patterns — Copy-Paste Blocks

## 1. bcrypt Password Hashing

```python
try:
    import bcrypt as _bcrypt
    BCRYPT_OK = True
except ImportError:
    BCRYPT_OK = False

def hash_pw(pw):
    if BCRYPT_OK:
        return _bcrypt.hashpw(pw.encode(), _bcrypt.gensalt(12)).decode()
    return hashlib.sha256(pw.encode()).hexdigest()

def check_pw(pw, hashed):
    if not hashed: return False
    if BCRYPT_OK and hashed.startswith('$2'):
        try: return _bcrypt.checkpw(pw.encode(), hashed.encode())
        except: return False
    return hashlib.sha256(pw.encode()).hexdigest() == hashed
```

Transparent upgrade on login (add inside login route after successful check_pw):
```python
if BCRYPT_OK and user['password'] and not user['password'].startswith('$2'):
    db.execute('UPDATE users SET password=? WHERE id=?', (hash_pw(pw), user['id']))
    db.commit()
```

## 2. Login Rate Limiting

```python
_rate_store: dict = {}

def is_rate_limited(key, max_calls=5, window=60):
    import time
    now = time.time()
    calls = [t for t in _rate_store.get(key, []) if now - t < window]
    _rate_store[key] = calls
    if len(calls) >= max_calls: return True
    _rate_store[key].append(now)
    return False

# In login route:
ip = request.remote_addr or 'unknown'
if is_rate_limited(f'login:{ip}', max_calls=5, window=60):
    flash('Too many attempts. Try again in a minute.', 'error')
    return render_template('login.html')
```

## 3. CSRF Protection

```python
import secrets as _secrets_module

def _get_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = _secrets_module.token_hex(32)
    return session['csrf_token']

def _validate_csrf():
    token = request.form.get('csrf_token') or request.headers.get('X-CSRF-Token', '')
    return bool(token and token == session.get('csrf_token', ''))

app.jinja_env.globals['csrf_token'] = _get_csrf_token

def csrf_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.method == 'POST' and not _validate_csrf():
            if request.is_json or request.headers.get('Authorization', ''):
                return f(*args, **kwargs)
            return jsonify({'error': 'CSRF validation failed'}), 403
        return f(*args, **kwargs)
    return decorated
```

In every HTML form:
```html
<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
```

## 4. Security Headers

```python
@app.after_request
def security_headers(response):
    response.headers.setdefault('X-Frame-Options', 'SAMEORIGIN')
    response.headers.setdefault('X-Content-Type-Options', 'nosniff')
    response.headers.setdefault('X-XSS-Protection', '1; mode=block')
    response.headers.setdefault('Referrer-Policy', 'strict-origin-when-cross-origin')
    response.headers.setdefault('Permissions-Policy', 'geolocation=(), microphone=(), camera=()')
    response.headers.setdefault('Content-Security-Policy',
        "default-src 'self' https: data: blob: 'unsafe-inline' 'unsafe-eval';")
    return response
```

## 5. Session Config

```python
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
app.config['SESSION_COOKIE_HTTPONLY']    = True
app.config['SESSION_COOKIE_SAMESITE']   = 'Lax'
app.config['SESSION_COOKIE_SECURE']     = False  # Railway edge handles TLS
```

## 6. Stable Secret Key

```python
import os, secrets, hashlib, pathlib
_SECRET_KEY = os.environ.get('SECRET_KEY', '')
if not _SECRET_KEY:
    _DATA_DIR = os.environ.get('RAILWAY_VOLUME_MOUNT_PATH', os.path.dirname(__file__))
    _KEY_FILE = os.path.join(_DATA_DIR, '.secret_key')
    try:
        os.makedirs(_DATA_DIR, exist_ok=True)
        if os.path.exists(_KEY_FILE):
            with open(_KEY_FILE) as f: _SECRET_KEY = f.read().strip()
        if not _SECRET_KEY:
            _SECRET_KEY = secrets.token_hex(32)
            with open(_KEY_FILE, 'w') as f: f.write(_SECRET_KEY)
    except Exception:
        _SECRET_KEY = hashlib.sha256(f'fallback-{os.environ.get("RAILWAY_SERVICE_NAME","app")}'.encode()).hexdigest()
app.secret_key = _SECRET_KEY
```

## 7. Health Endpoint

```python
@app.route('/health')
def health():
    return jsonify({'status': 'ok'})
```

## 8. Login Required Decorator

```python
from functools import wraps
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Your session expired — please log in again.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated
```
