# 🔐 Security Checklist — Alexander AI Digital
*Run through this before every deploy. No shortcuts.*

---

## PRE-DEPLOY CHECKLIST

### Secrets
- [ ] `SECRET_KEY` set in Railway env vars (not in code)
- [ ] `PASSWORD_PEPPER` set in Railway env vars (not in code)
- [ ] No hardcoded tokens, passwords, or API keys in source
- [ ] `.gitignore` blocks `.env`, `*.secret`, `*_token`, `data/`, `*.db`
- [ ] `git log --all --full-history -- "*.env"` returns nothing sensitive

### Passwords
- [ ] Using `hash_password()` from saas_security_core.py (bcrypt/Argon2id)
- [ ] NOT using plain SHA-256 for passwords
- [ ] Password minimum 8 chars enforced
- [ ] Common passwords blocked

### Sessions
- [ ] `SESSION_COOKIE_SECURE=True` in production
- [ ] `SESSION_COOKIE_HTTPONLY=True`
- [ ] `SESSION_COOKIE_SAMESITE='Lax'`
- [ ] Using `secure_login()` (prevents session fixation)
- [ ] Session expires in ≤ 1 hour

### CSRF
- [ ] `{{ csrf_token() }}` in every HTML form
- [ ] CSRF validated on every POST route (or @csrf_protect decorator)
- [ ] API routes use Bearer tokens instead (skip CSRF for /api/)

### UI / UX Security
- [ ] All password fields have show/hide eye toggle 👁️
- [ ] Error messages don't reveal whether username exists
  (say "Invalid credentials" not "Wrong password" or "User not found")

### Rate Limiting
- [ ] Login endpoint: ≤ 10 attempts/min, lockout after
- [ ] Signup endpoint: rate limited
- [ ] Password reset: rate limited
- [ ] API endpoints: rate limited

### SQL
- [ ] All DB queries use `?` parameterized placeholders
- [ ] No f-strings or concatenation in SQL queries
- [ ] User input never goes directly into SQL

### Headers
- [ ] `X-Frame-Options: DENY` (clickjacking)
- [ ] `X-Content-Type-Options: nosniff`
- [ ] `Strict-Transport-Security` set
- [ ] `Content-Security-Policy` set
- [ ] `Referrer-Policy` set

### HTTPS
- [ ] App deployed behind Railway HTTPS (auto ✅)
- [ ] No HTTP-only links in app
- [ ] Session cookie secure flag on

### Error Handling
- [ ] `debug=False` in production
- [ ] 404/500 handlers don't expose stack traces to users
- [ ] `/api/` routes return JSON errors (not HTML)

### Logging & Monitoring
- [ ] Failed login attempts logged
- [ ] Admin actions logged
- [ ] No passwords or tokens written to logs

---

## POST-DEPLOY CHECKS

- [ ] Hit `/health` — returns `{"status": "ok"}` (JSON not plain text)
- [ ] Try logging in with wrong password — get generic error
- [ ] Try SQL injection in login: `' OR '1'='1` — gets rejected
- [ ] Check browser DevTools — no secrets in page source or JS
- [ ] HTTPS lock icon showing in browser

---

## RAILWAY ENV VARS EVERY APP NEEDS

```
SECRET_KEY=<run: python -c "import secrets; print(secrets.token_hex(32))">
PASSWORD_PEPPER=<run: python -c "import secrets; print(secrets.token_hex(32))">
FLASK_ENV=production
DEMO_MODE=false
```

---

## WHEN SOMETHING GOES WRONG

**If a token/secret is leaked:**
1. Rotate it immediately (GitHub → Settings → Tokens → Regenerate)
2. Scrub git history: `git filter-branch` or `git-filter-repo`
3. Force push: `git push --force`
4. Tell Jay

**If DB is compromised:**
1. Rotate all API tokens immediately
2. Force all users to reset passwords
3. Check if pepper is still secret (it's separate from DB)
4. Audit logs for unauthorized access

**If session is hijacked:**
1. Call `session.clear()` + force re-login
2. Invalidate all active sessions for that user
3. Check for XSS that could have stolen the cookie

---

*Last updated: 2026-04-16 | Owner: KiloClaw / Alexander AI Digital*
