# Liberty Emporium & Thrift App — Security & Code Audit
**Date:** 2026-05-20  
**Audited by:** Echo (KiloClaw)  
**File:** app_with_ai.py (2373 lines) + templates/

---

## 🔴 Critical Issues (Fix ASAP)

### 1. Weak Password Hashing — SHA-256
**Line 78:** `hashlib.sha256(pw.encode()).hexdigest()`  
SHA-256 is fast — an attacker who gets your `users.json` can crack every password in seconds with a GPU. You need **bcrypt** or **argon2**.  
**Fix:** Replace `hash_password()` with bcrypt.

### 2. Default Admin Password in Code
**Line 63:** `ADMIN_PASS = os.environ.get('ADMIN_PASSWORD', 'admin123')`  
If `ADMIN_PASSWORD` is not set in Railway variables, admin password is literally `admin123`.  
**Fix:** Remove the default. Make the env var required — crash loudly at startup if missing.

### 3. Hardcoded Fallback Secret Key
**Line 21:** `app.secret_key = os.environ.get('SECRET_KEY', 'liberty-emporium-secret-2026')`  
If `SECRET_KEY` isn't set, sessions are trivially forgeable.  
**Fix:** Same — no fallback. Require it at startup.

### 4. No CSRF Protection
Zero CSRF protection on any form or POST route. An attacker can trick a logged-in admin into adding/deleting products, changing passwords, or approving users by just having them visit a malicious page.  
**Fix:** Add `flask-wtf` with `CSRFProtect(app)` — 3 lines of code.

### 5. `debug=True` in Production Code
**Line 2338:** `app.run(debug=True)`  
This is only hit when running locally (Railway uses gunicorn), but it's a bad habit and dangerous if someone ever runs it directly. The Werkzeug debugger exposes a Python console.  
**Fix:** `app.run(debug=os.environ.get('FLASK_DEBUG','false') == 'true')`

---

## 🟠 Medium Issues (Fix Soon)

### 6. No Rate Limiting on Login
No brute-force protection on `/login`. An attacker can try thousands of passwords automatically.  
**Fix:** Add `flask-limiter` — `@limiter.limit("10 per minute")` on the login route.

### 7. Uploads Served Without Auth
**Line 482:** `/uploads/<filename>` has no `@login_required`.  
Anyone on the internet can access all product photos by guessing filenames (UUIDs make it hard but not impossible, and filenames are visible in product pages).  
**Risk:** Low for a thrift store, but worth noting if you ever add sensitive docs.

### 8. `change_password` Route Missing Auth
**Line 1802:** `def change_password()` has no `@login_required` decorator. It just redirects to forgot_password, so no real exploit right now — but it's a bug waiting to happen if that logic changes.

### 9. Admin Password Shown on Login Page Demo
**Line 279:** `demo_password=ADMIN_PASS` is passed to the login template and likely rendered visibly. If this renders to the page HTML, it exposes the admin password to anyone who views source.  
**Fix:** Remove this from the template context, or at minimum don't pass the actual value.

---

## 🟡 Low / Code Quality Issues

### 10. Bare `except:` Clauses (8 instances)
Swallows all errors including keyboard interrupts, memory errors, etc. Makes debugging impossible.  
**Fix:** Use `except Exception:` at minimum, log the error.

### 11. Unused Variables (4 instances)
- `font_sm` (line 762) — assigned, never read
- `pulse` (line 1229) — calculated, never used  
- `store_alpha` (line 1235) — calculated, never used
- `search_query` (line 2048) — built, never sent

### 12. Unused Imports
- `PIL.ImageFilter` (line 1105)
- `tempfile` (line 1449)
- `io` (line 1854)

### 13. Unnecessary f-strings (2 instances)
Lines 268 and 2353 — `f'...'` with no `{}` placeholders.

### 14. Single-file 2373-line Monolith
The whole app is one file. As you add features this becomes hard to maintain.  
**Recommendation:** Not urgent, but eventually split into blueprints (routes/auth.py, routes/inventory.py, routes/ai.py, etc.)

---

## ✅ Things Done Well

- `secure_filename()` used on music uploads ✅
- File extension allowlist enforced on image uploads ✅  
- UUID-based filenames for uploaded images (no guessable paths) ✅
- `send_from_directory()` used (prevents path traversal) ✅
- Signup goes to pending queue — admin must approve ✅
- Role-based access control system exists ✅
- Volume + DATA_DIR now set (data persists) ✅
- Password reset via email token (not plain text) ✅

---

## Priority Fix Plan

| Priority | Issue | Effort |
|----------|-------|--------|
| 🔴 Do tonight | Remove hardcoded `admin123` default | 2 min |
| 🔴 Do tonight | Remove hardcoded `SECRET_KEY` default | 2 min |
| 🔴 This week | Upgrade password hashing to bcrypt | 30 min |
| 🔴 This week | Add CSRF protection | 15 min |
| 🟠 This week | Add login rate limiting | 10 min |
| 🟠 Soon | Fix debug=True | 2 min |
| 🟡 Whenever | Clean up bare excepts, unused vars | 20 min |
