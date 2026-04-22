# Echo Mobile & Security Knowledge Base
_Built 2026-04-22 — Deep study of Liberty-Emporium apps + OWASP + Flask 2025 best practices_

---

## 📱 What "Mobile Programming" Means for Our Stack

Our apps are **Flask web apps** served over HTTPS on Railway. "Mobile" for us means:
1. **Responsive design** — works beautifully on phones (we already have `viewport` meta tags ✅)
2. **PWA capability** — installable on home screen, offline-capable, push notifications
3. **Capacitor wrapper** — pet-vet-ai already has `capacitor.config.json` — can be wrapped as native iOS/Android app
4. **Mobile UX patterns** — touch targets ≥44px, thumb-friendly nav, no hover-only interactions
5. **API-first backends** — so a native app (React Native, Flutter, Capacitor) can consume the same endpoints

---

## 🔐 Security Audit: Current State of Our Apps

### FloodClaim Pro
| Check | Status | Notes |
|-------|--------|-------|
| Security headers | ❌ MISSING | No X-Frame-Options, no CSP, no X-Content-Type |
| Password hashing | ⚠️ WEAK | Uses `hashlib.sha256` — NOT bcrypt. Must fix. |
| CSRF protection | ❌ MISSING | No CSRF tokens on forms |
| Rate limiting | ❌ MISSING | Login has no rate limit — brute-force vulnerable |
| debug=False | ✅ Good | |
| Session secret | ✅ Good | env var → file → generated |
| Input sanitization | ✅ Partial | Uses parameterized queries |

### AI Agent Widget
| Check | Status | Notes |
|-------|--------|-------|
| Security headers | ✅ Partial | X-Content-Type + X-Frame + Referrer-Policy present |
| Password hashing | ✅ bcrypt | 12 rounds — good |
| CSRF protection | ❌ MISSING | No CSRF tokens |
| Rate limiting | ✅ Good | Custom in-memory limiter (login + chat) |
| **debug=True** | 🚨 CRITICAL | `app.run(debug=True)` — exposes Werkzeug shell on production! |
| CSP header | ❌ MISSING | |

### Pet Vet AI
| Check | Status | Notes |
|-------|--------|-------|
| Security headers | ✅ Good | X-Frame + X-Content-Type + CSP + XSS-Protection |
| Password hashing | ✅ bcrypt + fallback | bcrypt for new, sha256 for legacy |
| CSRF protection | ✅ Present | Custom `_get_csrf_token()` + `_validate_csrf()` |
| Rate limiting | ✅ Present | DB-backed rate limiter |
| debug=False | ✅ Good | |
| CSP | ✅ Present | Though it's broad (`unsafe-inline` / `unsafe-eval`) |

**Pet Vet AI is our most secure app. Use it as the template.**

### EcDash (jay-portfolio)
| Check | Status | Notes |
|-------|--------|-------|
| Security headers | ❌ MISSING | None detected |
| Rate limiting | ❌ MISSING | |
| CSRF | ❌ MISSING | |

### Contractor Pro AI
| Check | Status | Notes |
|-------|--------|-------|
| Security headers | ❌ MISSING | |
| debug=False | ✅ Good | |

---

## 🚨 CRITICAL ISSUES TO FIX (Priority Order)

### 1. AI Agent Widget: debug=True in Production (CRITICAL)
```python
# CURRENT (line 2383) — DANGEROUS
app.run(debug=True, port=5000)

# FIX
app.run(debug=False, port=5000)
```
The Werkzeug debugger with `debug=True` allows **arbitrary code execution** on the server.

### 2. FloodClaim Pro: SHA-256 Passwords (HIGH)
```python
# CURRENT — weak, no salt
return hashlib.sha256(pw.encode()).hexdigest()

# FIX — use bcrypt
import bcrypt
def hash_password(pw): return bcrypt.hashpw(pw.encode(), bcrypt.gensalt(12)).decode()
def check_password(pw, hashed): return bcrypt.checkpw(pw.encode(), hashed.encode())
```
SHA-256 without salt = rainbow table vulnerable. Must migrate to bcrypt.

### 3. Missing Security Headers (FloodClaim, EcDash, Contractor Pro)
Add this `after_request` block to every app that's missing it:
```python
@app.after_request
def security_headers(response):
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    if 'Content-Security-Policy' not in response.headers:
        response.headers['Content-Security-Policy'] = (
            "default-src 'self' https: data: blob: 'unsafe-inline' 'unsafe-eval';"
        )
    return response
```

### 4. Missing CSRF Protection (FloodClaim, AI Widget, EcDash)
Add to any app missing it (copy from pet-vet-ai pattern):
```python
import secrets as _secrets_module

def _get_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = _secrets_module.token_hex(32)
    return session['csrf_token']

def _validate_csrf():
    token = request.form.get('csrf_token') or request.headers.get('X-CSRF-Token', '')
    return token and token == session.get('csrf_token', '')

app.jinja_env.globals['csrf_token'] = _get_csrf_token
```
Then in every HTML form: `<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">`

### 5. Missing Rate Limiting (FloodClaim login)
```python
_rate_store = {}

def is_rate_limited(key, max_calls=5, window=60):
    import time
    now = time.time()
    calls = [t for t in _rate_store.get(key, []) if now - t < window]
    _rate_store[key] = calls
    if len(calls) >= max_calls:
        return True
    _rate_store[key].append(now)
    return False

# In login route:
ip = request.remote_addr
if is_rate_limited(f'login:{ip}', max_calls=5, window=60):
    return jsonify({'error': 'Too many attempts. Try again later.'}), 429
```

---

## 📱 PWA Upgrade Path (for Any App)

To make any app installable on mobile home screen:

### Step 1: Add manifest.json
```json
{
  "name": "FloodClaim Pro",
  "short_name": "FloodClaim",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#1a1a2e",
  "theme_color": "#4f46e5",
  "icons": [
    {"src": "/static/icon-192.png", "sizes": "192x192", "type": "image/png"},
    {"src": "/static/icon-512.png", "sizes": "512x512", "type": "image/png"}
  ]
}
```

### Step 2: Serve manifest from Flask
```python
@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')
```

### Step 3: Link in base.html `<head>`
```html
<link rel="manifest" href="/manifest.json">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="theme-color" content="#4f46e5">
```

### Step 4: Register a Service Worker (optional but needed for "install" prompt)
```javascript
// static/sw.js
self.addEventListener('fetch', e => e.respondWith(fetch(e.request)));

// In base.html:
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js');
}
```

---

## 📲 Capacitor: Turn Any Flask App Into a Native App

Pet-vet-ai already has `capacitor.config.json`. Here's the full pattern:

```json
{
  "appId": "com.libertyemporium.floodclaimpro",
  "appName": "FloodClaim Pro",
  "webDir": "www",
  "server": {
    "url": "https://billy-floods.up.railway.app",
    "cleartext": false
  }
}
```

Then:
```bash
npm install @capacitor/core @capacitor/cli @capacitor/android @capacitor/ios
npx cap add android
npx cap add ios
npx cap open android  # Opens Android Studio
npx cap open ios      # Opens Xcode
```

Capacitor wraps the live Railway URL in a native shell — no separate mobile codebase needed.

---

## 🎯 Mobile UX Checklist (Apply to All Templates)

- [ ] Touch targets ≥ 44×44px (buttons, links)
- [ ] `font-size: 16px` minimum on inputs (prevents iOS zoom on focus)
- [ ] `input[type=number]` → use `inputmode="numeric"` on mobile to get numeric keyboard without arrows
- [ ] Bottom navigation bar pattern for mobile (not just sidebar that collapses)
- [ ] `autocomplete` attributes on login forms: `autocomplete="email"`, `autocomplete="current-password"`
- [ ] No `hover:` only interactions — everything should work with tap
- [ ] `loading="lazy"` on images
- [ ] Avoid tables on mobile — use card/list layouts with CSS grid
- [ ] `max-width: 100%; overflow-x: hidden` on body to prevent horizontal scroll

---

## 🔒 Flask Security: The Full Checklist (2025 OWASP Standard)

| Category | What | How |
|----------|------|-----|
| Auth | bcrypt passwords | `bcrypt.hashpw(pw, gensalt(12))` |
| Auth | Rate limit login | 5 attempts/60s per IP |
| Auth | Session expiry | `PERMANENT_SESSION_LIFETIME = timedelta(hours=8)` |
| Auth | Secure session cookie | `SESSION_COOKIE_SECURE=True`, `SESSION_COOKIE_HTTPONLY=True`, `SESSION_COOKIE_SAMESITE='Lax'` |
| Headers | X-Frame-Options | `SAMEORIGIN` |
| Headers | X-Content-Type-Options | `nosniff` |
| Headers | CSP | Restrict sources — avoid `unsafe-eval` where possible |
| Headers | HSTS | `Strict-Transport-Security: max-age=31536000` (Railway handles TLS but set anyway) |
| CSRF | Token in forms | `session['csrf_token']` validated on every POST |
| Injection | SQL | Always parameterized queries — never f-strings in SQL |
| Injection | XSS | Jinja2 auto-escapes by default — never use `| safe` on user data |
| Secrets | No hardcoded keys | All secrets via `os.environ.get()` |
| Secrets | Rotate tokens | GitHub PAT is temporary — plan rotation |
| Files | Upload validation | Check MIME type, not just extension |
| Deps | Keep updated | Run `pip list --outdated` regularly |
| Debug | debug=False | Always in production |

---

## 🔧 Tools I Can Run on Our Codebase

| Tool | What it does | Command |
|------|-------------|---------|
| `bandit` | Python security scanner | `bandit -r app.py -ll` |
| `ruff` | Linter + code quality | `ruff check app.py --fix` |
| `pip audit` | Dependency CVE check | `pip install pip-audit && pip-audit -r requirements.txt` |

---

## 📚 Key References

- OWASP Mobile Top 10: https://owasp.org/www-project-mobile-top-10/
- OWASP Mobile Security Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Mobile_Application_Security_Cheat_Sheet.html
- Flask Security Best Practices 2025: https://corgea.com/learn/flask-security-best-practices-2025/
- Capacitor PWA Docs: https://capacitorjs.com/docs/web/progressive-web-apps
- PWA Security 2025: https://appinstitute.com/9-pwa-security-practices-for-2025/

---

## 🗺️ Echo's Mobile/Security Roadmap for Liberty-Emporium Apps

### Phase 1 — Critical Security Fixes (do ASAP)
1. ✅ Already done: pet-vet-ai (our best-secured app)
2. 🔴 AI Agent Widget: fix `debug=True` → `debug=False`
3. 🔴 FloodClaim Pro: migrate passwords from SHA-256 → bcrypt
4. 🟡 FloodClaim Pro: add security headers + CSRF + rate limiting
5. 🟡 EcDash: add security headers + CSRF
6. 🟡 Contractor Pro: add security headers

### Phase 2 — PWA Upgrades
- Add `manifest.json` + service worker to FloodClaim Pro (field workers use it on mobile)
- Add to AI Agent Widget (widget embedded in customer sites)
- Add `apple-touch-icon` to all apps

### Phase 3 — Native Mobile Wrappers (Capacitor)
- Pet Vet AI → already has capacitor.config.json — finish wiring → Google Play
- FloodClaim Pro → Capacitor shell → field adjuster mobile app

### Phase 4 — Mobile UX Polish
- Audit all templates for touch target size
- Add bottom nav to mobile layouts
- Test with browser DevTools mobile emulator

---
_Last updated: 2026-04-22 by Echo_
