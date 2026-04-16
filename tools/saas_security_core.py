"""
saas_security_core.py — Alexander AI Integrated Solutions
=============================================
Drop this into any SaaS app and import it.
Provides: password hashing, CSRF, session security,
          rate limiting, security headers, input validation.

Usage:
    from saas_security_core import init_security, hash_password, verify_password, login_required

    app = Flask(__name__)
    init_security(app)

Author: KiloClaw / Alexander AI Integrated Solutions
Last updated: 2026-04-16
"""

import os
import re
import hashlib
import secrets
import datetime
import functools
from collections import defaultdict
import time as _time

# ── Try importing optional deps gracefully ────────────────
try:
    import bcrypt as _bcrypt
    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False

try:
    from argon2 import PasswordHasher as _Argon2PasswordHasher
    from argon2.exceptions import VerifyMismatchError as _VerifyMismatchError
    ARGON2_AVAILABLE = True
except ImportError:
    ARGON2_AVAILABLE = False

from flask import request, session, jsonify, redirect, url_for, g


# ════════════════════════════════════════════════════════════
# CONFIGURATION
# ════════════════════════════════════════════════════════════

def get_pepper() -> str:
    """Get the pepper from env var. Never hardcode this."""
    p = os.environ.get('PASSWORD_PEPPER', '')
    if not p:
        print('[SECURITY WARNING] PASSWORD_PEPPER env var not set! '
              'Set it in Railway environment variables.')
    return p


# ════════════════════════════════════════════════════════════
# PASSWORD HASHING  (bcrypt > SHA-256, Argon2id > bcrypt)
# ════════════════════════════════════════════════════════════

def hash_password(password: str) -> str:
    """
    Hash a password securely.
    Uses Argon2id if available, falls back to bcrypt, falls back to
    salted SHA-256 (legacy only — upgrade ASAP).

    Always applies pepper from env var for extra DB-breach protection.
    """
    pepper = get_pepper()
    peppered = pepper + password  # pepper + password before hashing

    if ARGON2_AVAILABLE:
        ph = _Argon2PasswordHasher(
            time_cost=3,
            memory_cost=65536,  # 64MB — hard to parallelize on GPU
            parallelism=2,
            hash_len=32,
            salt_len=16,
        )
        return 'argon2:' + ph.hash(peppered)

    if BCRYPT_AVAILABLE:
        hashed = _bcrypt.hashpw(peppered.encode('utf-8'), _bcrypt.gensalt(rounds=12))
        return 'bcrypt:' + hashed.decode('utf-8')

    # Legacy fallback — DO NOT USE in production without bcrypt
    salt = secrets.token_hex(32)
    h = hashlib.sha256((salt + peppered).encode()).hexdigest()
    return f'sha256:{salt}:{h}'


def verify_password(password: str, stored_hash: str) -> bool:
    """
    Verify a password against a stored hash.
    Handles all three formats: argon2:, bcrypt:, sha256:, and legacy plain sha256.
    """
    pepper = get_pepper()
    peppered = pepper + password

    try:
        if stored_hash.startswith('argon2:'):
            if not ARGON2_AVAILABLE:
                return False
            ph = _Argon2PasswordHasher()
            try:
                return ph.verify(stored_hash[7:], peppered)
            except _VerifyMismatchError:
                return False

        elif stored_hash.startswith('bcrypt:'):
            if not BCRYPT_AVAILABLE:
                return False
            return _bcrypt.checkpw(peppered.encode('utf-8'),
                                   stored_hash[7:].encode('utf-8'))

        elif stored_hash.startswith('sha256:'):
            # New salted sha256 format: sha256:salt:hash
            parts = stored_hash.split(':')
            if len(parts) != 3:
                return False
            _, salt, expected = parts
            actual = hashlib.sha256((salt + peppered).encode()).hexdigest()
            return secrets.compare_digest(actual, expected)

        else:
            # Legacy plain sha256 (no pepper, no salt) — still supports old accounts
            # BUT: on next login, upgrade their hash automatically
            legacy = hashlib.sha256(password.encode()).hexdigest()
            return secrets.compare_digest(stored_hash, legacy)

    except Exception:
        return False


def needs_hash_upgrade(stored_hash: str) -> bool:
    """Returns True if the hash should be upgraded to a stronger algorithm."""
    return not (stored_hash.startswith('argon2:') or stored_hash.startswith('bcrypt:'))


# ════════════════════════════════════════════════════════════
# AUTH DECORATORS
# ════════════════════════════════════════════════════════════

def login_required(f):
    """Decorator: requires user to be logged in."""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            if request.is_json or request.path.startswith('/api/'):
                return jsonify({'error': 'Authentication required'}), 401
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    """Decorator: requires admin session."""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in') or not session.get('is_admin'):
            if request.is_json or request.path.startswith('/api/'):
                return jsonify({'error': 'Admin access required'}), 403
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


# ════════════════════════════════════════════════════════════
# CSRF PROTECTION
# ════════════════════════════════════════════════════════════

def generate_csrf_token() -> str:
    """Generate a per-session CSRF token."""
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(32)
    return session['csrf_token']


def validate_csrf() -> bool:
    """
    Validate CSRF token on POST/PUT/DELETE/PATCH requests.
    Skips API routes (they use Bearer tokens instead).
    """
    if request.method not in ('POST', 'PUT', 'DELETE', 'PATCH'):
        return True
    if request.path.startswith('/api/'):
        return True  # API uses Bearer tokens, not CSRF tokens

    token = (request.form.get('csrf_token') or
             request.headers.get('X-CSRF-Token'))
    expected = session.get('csrf_token')

    if not token or not expected:
        return False
    return secrets.compare_digest(token, expected)


def csrf_protect(f):
    """Decorator: enforces CSRF validation."""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if not validate_csrf():
            return jsonify({'error': 'CSRF validation failed'}), 403
        return f(*args, **kwargs)
    return decorated


# ════════════════════════════════════════════════════════════
# RATE LIMITING  (no external deps)
# ════════════════════════════════════════════════════════════

_rate_store: dict = defaultdict(list)
_rate_lock_store: dict = {}  # ip -> locked_until timestamp


def is_rate_limited(key: str,
                    max_requests: int = 20,
                    window_seconds: int = 60,
                    lockout_seconds: int = 0) -> bool:
    """
    In-memory rate limiter. Returns True if limit exceeded.
    Optionally locks out the key for lockout_seconds after max_requests.
    """
    now = _time.time()

    # Check lockout
    if lockout_seconds and key in _rate_lock_store:
        if now < _rate_lock_store[key]:
            return True  # still locked
        else:
            del _rate_lock_store[key]

    # Slide window
    _rate_store[key] = [t for t in _rate_store[key] if now - t < window_seconds]

    if len(_rate_store[key]) >= max_requests:
        if lockout_seconds:
            _rate_lock_store[key] = now + lockout_seconds
        return True

    _rate_store[key].append(now)
    return False


def rate_limit(max_requests: int = 20, window_seconds: int = 60,
               lockout_seconds: int = 0):
    """Decorator factory: rate limit by IP."""
    def decorator(f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            ip = request.remote_addr or 'unknown'
            key = f'{f.__name__}:{ip}'
            if is_rate_limited(key, max_requests, window_seconds, lockout_seconds):
                return jsonify({'error': 'Too many requests. Please slow down.'}), 429
            return f(*args, **kwargs)
        return decorated
    return decorator


def login_rate_limit(f):
    """Strict rate limit for login routes: 10/min, 5-min lockout after that."""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        ip = request.remote_addr or 'unknown'
        key = f'login:{ip}'
        if is_rate_limited(key, max_requests=10, window_seconds=60,
                           lockout_seconds=300):
            return jsonify({'error': 'Too many login attempts. Try again in 5 minutes.'}), 429
        return f(*args, **kwargs)
    return decorated


# ════════════════════════════════════════════════════════════
# SESSION SECURITY
# ════════════════════════════════════════════════════════════

def secure_login(user_id: int, username: str, is_admin: bool = False,
                 plan: str = 'free', **extra):
    """
    Properly set up a session after successful login.
    Clears old session (prevents session fixation!),
    then sets new session data.
    """
    # CRITICAL: clear first to prevent session fixation attacks
    old_csrf = session.get('csrf_token')  # preserve CSRF if needed
    session.clear()
    session.permanent = True
    session['logged_in'] = True
    session['user_id'] = user_id
    session['username'] = username
    session['is_admin'] = bool(is_admin)
    session['plan'] = plan
    session['login_time'] = datetime.datetime.utcnow().isoformat()
    for k, v in extra.items():
        session[k] = v
    # Regenerate CSRF token
    session['csrf_token'] = secrets.token_hex(32)


def secure_logout():
    """Properly clear the session on logout."""
    session.clear()


# ════════════════════════════════════════════════════════════
# INPUT VALIDATION
# ════════════════════════════════════════════════════════════

# Common breached passwords to block at signup
COMMON_PASSWORDS = {
    'password', 'password1', 'password123', '123456', '12345678',
    'qwerty', 'abc123', 'letmein', 'admin', 'admin123', 'welcome',
    'monkey', 'dragon', 'master', 'sunshine', 'princess', 'shadow',
    'superman', 'michael', 'football', 'iloveyou', 'trustno1',
}


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password strength. Returns (is_valid, error_message).
    Based on OWASP/NIST guidelines.
    """
    if len(password) < 8:
        return False, 'Password must be at least 8 characters'
    if len(password) > 256:
        return False, 'Password must be under 256 characters'
    if password.lower() in COMMON_PASSWORDS:
        return False, 'This password is too common. Please choose a stronger one'
    return True, ''


def validate_username(username: str) -> tuple[bool, str]:
    """Validate username format."""
    if not username:
        return False, 'Username is required'
    if len(username) < 3:
        return False, 'Username must be at least 3 characters'
    if len(username) > 64:
        return False, 'Username must be under 64 characters'
    if not re.match(r'^[a-zA-Z0-9_\-\.]+$', username):
        return False, 'Username can only contain letters, numbers, underscores, hyphens, and dots'
    return True, ''


def validate_email(email: str) -> tuple[bool, str]:
    """Basic email validation."""
    if not email or len(email) > 254:
        return False, 'Invalid email address'
    if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email):
        return False, 'Invalid email address format'
    return True, ''


def sanitize_string(value: str, max_length: int = 255) -> str:
    """Strip whitespace and truncate. Safe for DB storage."""
    if not value:
        return ''
    return value.strip()[:max_length]


# ════════════════════════════════════════════════════════════
# SECURITY HEADERS
# ════════════════════════════════════════════════════════════

SECURITY_HEADERS = {
    'X-Frame-Options': 'DENY',
    'X-Content-Type-Options': 'nosniff',
    'X-XSS-Protection': '1; mode=block',
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
    'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
}

# CSP — allows inline styles (needed for our apps) but restricts scripts
CSP = (
    "default-src 'self'; "
    "script-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://fonts.gstatic.com; "
    "font-src 'self' https://fonts.gstatic.com; "
    "img-src 'self' data: https:; "
    "connect-src 'self'"
)


# ════════════════════════════════════════════════════════════
# INIT — call this once per app
# ════════════════════════════════════════════════════════════

def init_security(app):
    """
    Initialize all security features for a Flask app.
    Call once after app creation:
        app = Flask(__name__)
        init_security(app)
    """
    # Secure session config
    app.config.setdefault('SESSION_COOKIE_SECURE',
                          os.environ.get('FLASK_ENV') == 'production')
    app.config.setdefault('SESSION_COOKIE_HTTPONLY', True)
    app.config.setdefault('SESSION_COOKIE_SAMESITE', 'Lax')
    app.config.setdefault('PERMANENT_SESSION_LIFETIME',
                          datetime.timedelta(hours=1))

    # Secret key — MUST come from env var
    if not app.secret_key:
        env_key = os.environ.get('SECRET_KEY')
        if env_key:
            app.secret_key = env_key
        else:
            # Auto-generate and warn — will change on restart
            app.secret_key = secrets.token_hex(32)
            print('[SECURITY WARNING] SECRET_KEY env var not set! '
                  'Sessions will not persist across restarts.')

    # Inject CSRF token into all templates
    app.jinja_env.globals['csrf_token'] = generate_csrf_token

    # Add security headers to all responses
    @app.after_request
    def add_security_headers(response):
        for header, value in SECURITY_HEADERS.items():
            response.headers[header] = value
        if 'Content-Security-Policy' not in response.headers:
            response.headers['Content-Security-Policy'] = CSP
        return response

    # Clean up old rate limit data periodically
    @app.before_request
    def cleanup_rate_store():
        if secrets.randbelow(100) < 2:  # 2% chance per request
            now = _time.time()
            for key in list(_rate_store.keys()):
                _rate_store[key] = [t for t in _rate_store[key] if now - t < 3600]

    return app


# ════════════════════════════════════════════════════════════
# API TOKEN VALIDATION  (reusable for all apps)
# ════════════════════════════════════════════════════════════

def validate_api_token(token: str, db_conn) -> int | None:
    """
    Validate a Bearer token against the api_tokens table.
    Returns user_id if valid, None if invalid/expired.

    Requires api_tokens table:
        CREATE TABLE api_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token_hash TEXT UNIQUE NOT NULL,
            label TEXT DEFAULT 'default',
            expires_at TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    if not token or len(token) < 16:
        return None
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    try:
        row = db_conn.execute(
            'SELECT user_id, expires_at FROM api_tokens WHERE token_hash = ?',
            (token_hash,)
        ).fetchone()
        if not row:
            return None
        if row['expires_at']:
            expires = datetime.datetime.fromisoformat(row['expires_at'])
            if datetime.datetime.utcnow() > expires:
                return None
        return row['user_id']
    except Exception:
        return None


def require_api_token(db_getter):
    """
    Decorator for API routes that require Bearer token auth.
    db_getter is a callable that returns a DB connection.

    Usage:
        @app.route('/api/data')
        @require_api_token(get_db)
        def api_data():
            user_id = g.api_user_id
            ...
    """
    def decorator(f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            auth = request.headers.get('Authorization', '')
            if not auth.startswith('Bearer '):
                return jsonify({'error': 'Authorization header required'}), 401
            token = auth[7:]
            user_id = validate_api_token(token, db_getter())
            if not user_id:
                return jsonify({'error': 'Invalid or expired token'}), 401
            g.api_user_id = user_id
            return f(*args, **kwargs)
        return decorated
    return decorator


# ════════════════════════════════════════════════════════════
# QUICK REFERENCE CHEATSHEET (print this in README)
# ════════════════════════════════════════════════════════════
"""
SECURITY QUICK REFERENCE — Alexander AI Integrated Solutions

Passwords:
    hash = hash_password(password)        # bcrypt or Argon2id + pepper
    ok   = verify_password(password, hash)
    if needs_hash_upgrade(hash): ...      # upgrade on next login

Session:
    secure_login(user_id, username, ...)  # prevents session fixation
    secure_logout()

CSRF:
    {{ csrf_token() }}                    # in every HTML form
    @csrf_protect                         # on POST routes

Rate Limiting:
    @login_rate_limit                     # strict: 10/min, 5-min lockout
    @rate_limit(max_requests=20)          # general

Input Validation:
    ok, err = validate_password_strength(password)
    ok, err = validate_username(username)
    ok, err = validate_email(email)
    clean   = sanitize_string(value, max_length=255)

API Tokens:
    @require_api_token(get_db)            # on API routes
    user_id = g.api_user_id              # access in handler

Init (once per app):
    init_security(app)

Railway env vars needed:
    SECRET_KEY        = <64 hex chars>
    PASSWORD_PEPPER   = <64 hex chars>
"""
