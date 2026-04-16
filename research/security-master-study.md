# Security Master Study — KiloClaw
*Deep study session: 2026-04-16*
*Sources: OWASP Cheat Sheet Series (Auth, Crypto, SQL, CSRF, Sessions, Input Validation, Secrets, TLS) + Flask 2025 best practices*

---

## THE 8 ATTACK TYPES WE MUST DEFEND AGAINST

### 1. SQL INJECTION
**What it is:** Attacker types SQL code into a form field and your database executes it.
Example: username field gets `' OR '1'='1` and suddenly they're logged in as anyone.

**Our current status:** ✅ SAFE — all our apps use `?` parameterized queries like:
```python
c.execute('SELECT * FROM users WHERE username = ?', (username,))
```
This is the correct defense. The `?` separates code from data — the DB never confuses user input for SQL commands. Never use f-strings or concatenation in SQL queries. Ever.

---

### 2. PASSWORD STORAGE
**What it is:** If our DB gets stolen, how hard is it to crack the passwords?

**Our current status:** ❌ VULNERABLE — SHA-256 with no salt. A GPU can crack 10 billion/sec.

**OWASP #1 recommendation — Argon2id:**
- Memory-hard (64MB minimum) — GPUs can't parallelize attacks
- Minimum: `time_cost=2, memory_cost=65536, parallelism=1`
- Even with a stolen DB, cracking one password takes hours not seconds

**#2 — bcrypt (what we already have installed):**
- 12 rounds minimum
- ~100 guesses/sec for attacker vs 10 billion for SHA-256
- Good enough — use this now, upgrade to Argon2id later

**The Pepper trick (new concept):**
- A secret string stored in Railway env vars (NOT in DB)
- Prepended to password before hashing: `hash(pepper + password)`
- Even if attacker steals entire database, they still can't crack without the pepper
- This is an extra layer on top of bcrypt/Argon2id

**Password rules OWASP actually says:**
- Minimum 8 chars WITH MFA, minimum 15 chars WITHOUT MFA
- Maximum at LEAST 64 chars (allow passphrases)
- Don't force special chars/numbers/uppercase — it makes weak passwords
- DO check against HaveIBeenPwned — don't allow known-breached passwords
- Don't force periodic changes — it trains people to use weak passwords

---

### 3. CSRF (Cross-Site Request Forgery)
**What it is:** User is logged into our app. They visit a malicious website. That site secretly submits a form to our app using the user's browser/cookies. Our app thinks it's the real user.

Example: Attacker's site has a hidden form that POSTs to `/change-password` on our app. User visits attacker's site while logged in → their password changes without them knowing.

**Our current status:** ⚠️ PARTIAL — KYS has CSRF tokens in the code but they're not enforced on every form (the `_validate_csrf()` function exists but isn't called consistently).

**The fix:** Every POST form needs a hidden CSRF token field. Flask-WTF handles this automatically. The token must:
- Be generated server-side per session
- Be included as hidden field in every form
- Be validated on every POST request
- Change after successful use (per-request tokens are more secure than per-session)

**SameSite cookies** also help: `SESSION_COOKIE_SAMESITE='Lax'` — we already have this ✅

---

### 4. XSS (Cross-Site Scripting)
**What it is:** Attacker stores `<script>alert('hacked')</script>` in your database (e.g. as their username). When another user views that page, the script runs in their browser. Can steal session cookies, redirect to phishing sites, etc.

**Our current status:** ✅ MOSTLY SAFE — Jinja2 auto-escapes variables by default. Our CSP headers help too.

**The gap:** Our CSP includes `'unsafe-inline'` which partially defeats it. Should tighten to nonces or hashes for inline scripts eventually.

**Rules:**
- Never use `{{ var | safe }}` in templates unless you absolutely trust the content
- Always use `{{ var }}` — Jinja2 escapes it automatically
- CSP headers add a second line of defense

---

### 5. SESSION HIJACKING
**What it is:** Attacker steals a user's session cookie and pretends to be them. Can happen via XSS, network sniffing (if HTTP), or guessing weak session IDs.

**OWASP requirements for secure sessions:**
- Session IDs must have at least **64 bits of entropy** — Flask uses `secrets.token_urlsafe()` which is good ✅
- `SESSION_COOKIE_HTTPONLY = True` — we have this ✅ (JS can't steal the cookie)
- `SESSION_COOKIE_SECURE = True` — we have `False` ❌ (should be True in production)
- `SESSION_COOKIE_SAMESITE = 'Lax'` — we have this ✅
- Regenerate session ID after login (prevent session fixation attacks)
- Expire sessions: we have 1 hour ✅

**Session fixation attack** (new concept I learned):
Attacker tricks user into using a session ID the attacker already knows. After user logs in, attacker uses that same ID to access their account. Fix: always call `session.clear()` then regenerate after successful login.

---

### 6. BRUTE FORCE / CREDENTIAL STUFFING
**What it is:** Attacker tries millions of username/password combos. Credential stuffing uses real leaked passwords from other sites.

**Our current status:** ✅ GOOD — KYS has rate limiting (10 login attempts/minute/IP)

**What we're missing:**
- Account lockout after N failures (we just slow them down, don't lock)
- CAPTCHA for repeated failures
- Alerting when an account gets hammered
- Checking passwords against HaveIBeenPwned at registration time

---

### 7. SECRETS IN CODE
**What it is:** API keys, passwords, tokens committed to git. GitHub scans for these. So do attackers.

**We learned this the hard way tonight.** PAT was in MEMORY.md, GitHub caught it, we had to rewrite history and rotate.

**The rule:** ZERO secrets in any committed file. Ever.
- Railway env vars for app secrets (`SECRET_KEY`, `DATABASE_URL`, `PEPPER`)
- `/root/.secrets/` for local machine tokens (not in git)
- `.gitignore` must block: `.env`, `*.secret`, `secrets/`, `*_token`, `*_key`

---

### 8. TRANSPORT SECURITY (HTTPS/TLS)
**What it is:** Data intercepted in transit. Passwords, session cookies, everything readable if HTTP.

**OWASP says:** TLS 1.3 only (disable 1.0 and 1.1). Railway handles this for us ✅

**What we still need:** `SESSION_COOKIE_SECURE = True` in all apps. Currently False.

---

## THE FLASK-SPECIFIC SECURITY STACK (what to install in all apps)

```python
# requirements.txt additions for all apps:
flask-wtf          # CSRF protection + form validation
flask-bcrypt       # Password hashing (already in KYS)
flask-talisman     # Security headers (replaces our manual headers)
flask-limiter      # Rate limiting (already in KYS manually)
argon2-cffi        # Upgrade path from bcrypt (future)
```

```python
# The proper Flask security config block:
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY'),      # from Railway env var
    SESSION_COOKIE_SECURE=True,                    # HTTPS only
    SESSION_COOKIE_HTTPONLY=True,                  # no JS access
    SESSION_COOKIE_SAMESITE='Lax',                 # CSRF protection
    PERMANENT_SESSION_LIFETIME=3600,               # 1 hour
    WTF_CSRF_ENABLED=True,                         # CSRF tokens on forms
)
```

---

## WHAT WE NEED TO BUILD: "saas_security_core.py"

A reusable security module that every app imports. Contains:
1. `hash_password(password)` → bcrypt with pepper
2. `verify_password(password, hash)` → bcrypt verify with pepper
3. `require_login` decorator
4. `require_admin` decorator
5. CSRF validation middleware
6. Standard security headers
7. Rate limiter setup

Every new SaaS app starts by importing this. One upgrade fixes all 7 apps.

---

## PRIORITY UPGRADE LIST

### 🔴 Do Next Session:
1. Add `SESSION_COOKIE_SECURE=True` to all 7 apps
2. Migrate KYS password hashing: SHA-256 → bcrypt (lib already installed)
3. Add `PEPPER` env var to Railway for KYS
4. Enforce CSRF token on all KYS forms (already partially implemented)

### 🟡 Next Sprint:
5. Build `saas_security_core.py` and roll out to all 7 apps
6. Add HaveIBeenPwned check on signup/password change
7. Add account lockout after 10 failed logins
8. Tighten CSP (remove `unsafe-inline`)

### 🟢 Future:
9. Upgrade bcrypt → Argon2id
10. Add TOTP/2FA for admin accounts
11. Upgrade brain-crypt.sh CBC → GCM
12. Session fixation protection (regenerate ID after login)
13. Add `.gitignore` to all repos blocking secret patterns

---

*Last updated: 2026-04-16 | Next review: after implementing Priority 1 items*
