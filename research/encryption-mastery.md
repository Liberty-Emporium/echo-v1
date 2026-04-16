# Encryption Mastery — KiloClaw Reference
*Researched 2026-04-16 — OWASP + 2025 industry standards*

---

## 🔐 The Big Picture: Layers of Protection

Every app we build needs security at 3 layers:
1. **Passwords at rest** → hashing (bcrypt/Argon2)
2. **Data at rest** → encryption (AES-256-GCM)
3. **Data in transit** → TLS/HTTPS (always)

---

## 1. PASSWORD HASHING (Never store plaintext or plain SHA-256)

### What we're doing NOW (weak):
```python
hashlib.sha256(password.encode()).hexdigest()  # ❌ BAD — fast, no salt, brute-forceable
```

### What we SHOULD use:
```python
# Argon2id — the gold standard (2025 winner)
import argon2
ph = argon2.PasswordHasher(time_cost=3, memory_cost=65536, parallelism=2)
hash = ph.hash(password)           # store this
ph.verify(hash, password)          # verify on login

# bcrypt — battle-tested, widely supported
import bcrypt
hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
bcrypt.checkpw(password.encode(), hash)
```

### Why it matters:
- SHA-256 can be brute-forced at **10 BILLION hashes/second** on a GPU
- bcrypt at 12 rounds: **~100/second** — 100 million times slower
- Argon2id: memory-hard, even GPU attacks are expensive

### TODO for all our apps:
- [ ] Migrate all apps from SHA-256 → bcrypt (already have bcrypt lib in KYS)
- [ ] KYS already imports bcrypt but login still uses SHA-256 — fix this

---

## 2. DATA ENCRYPTION (AES-256)

### What we're using (good but not optimal):
```bash
# AES-256-CBC (what brain-crypt.sh uses) — good but no integrity check
openssl enc -aes-256-cbc -pbkdf2 -iter 100000
```

### What's BETTER (AES-256-GCM):
```python
# AES-256-GCM = encryption + authentication in one
# Detects if anyone tampered with the data
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

key = AESGCM.generate_key(bit_length=256)
nonce = os.urandom(12)  # unique per encryption
aesgcm = AESGCM(key)
ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data)
plaintext = aesgcm.decrypt(nonce, ciphertext, associated_data)
```

### Key modes:
| Mode | Encryption | Integrity Check | Use for |
|------|-----------|----------------|---------|
| CBC  | ✅ | ❌ | Files (what we use now — OK) |
| GCM  | ✅ | ✅ | APIs, databases, sensitive data |
| ECB  | ✅ | ❌ | ❌ NEVER USE — patterns leak |

### Upgrade brain-crypt.sh → GCM eventually

---

## 3. API TOKENS & JWT

### What we built (good):
- SHA-256 hash stored in DB ✅
- Expiry dates ✅
- Label-based revocation ✅

### What's even better — JWT with short expiry:
```python
import jwt, datetime, secrets

SECRET = secrets.token_hex(32)  # 256-bit — never hardcode

# Issue token (15 min access, 7 day refresh)
token = jwt.encode({
    'sub': user_id,
    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
    'iat': datetime.datetime.utcnow(),
}, SECRET, algorithm='HS256')

# Verify
data = jwt.decode(token, SECRET, algorithms=['HS256'])
```

### Rules:
- Access tokens: 15 min max
- Refresh tokens: 7 days
- Store in HttpOnly cookies (not localStorage)
- Always HTTPS — never send tokens over HTTP
- Never put sensitive data IN the token payload (it's just base64)
- Rotate secrets every 90 days

---

## 4. SECRETS MANAGEMENT (The Big Lesson from Tonight)

### ❌ NEVER do:
- Store tokens/passwords in MEMORY.md or any committed file
- Put secrets in source code
- Commit .env files with real values

### ✅ ALWAYS do:
- Store in `/root/.secrets/` (not in git)
- Use environment variables in Railway (`SECRET_KEY`, `DATABASE_URL`)
- Use `/root/.secrets/` files for local scripts
- Keep a `.gitignore` that blocks `.env`, `*.secret`, `secrets/`

### Our secret storage:
```
/root/.secrets/
  github_token       # GitHub PAT
  gitlab_token       # GitLab PAT  
  kys_api_token      # Keep Your Secrets API token
```

---

## 5. HTTPS & TRANSPORT SECURITY

### Every app needs:
```python
# Flask — force HTTPS in production
app.config['SESSION_COOKIE_SECURE'] = True     # cookies only over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True   # no JS access
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax' # CSRF protection

# Security headers (we have these ✅)
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Content-Security-Policy: default-src 'self'
```

### Railway handles HTTPS termination — our apps are good here ✅

---

## 6. DATABASE ENCRYPTION

### For SQLite (what most our apps use):
- Encrypt sensitive columns: API keys, SSNs, payment info
- Use SQLCipher for full DB encryption (future consideration)
- At minimum: never store raw secrets, always hash/encrypt

### Pattern for sensitive fields:
```python
from cryptography.fernet import Fernet

FIELD_KEY = Fernet(os.environ['FIELD_ENCRYPTION_KEY'])

def encrypt_field(value):
    return FIELD_KEY.encrypt(value.encode()).decode()

def decrypt_field(value):
    return FIELD_KEY.decrypt(value.encode()).decode()
```

---

## 7. WHAT TO UPGRADE IN OUR APPS (Priority Order)

### 🔴 CRITICAL (do soon):
1. **All apps** — Migrate password hashing from SHA-256 → bcrypt (already in KYS)
2. **GitHub PAT** — Rotate immediately (was in public history)
3. **brain-crypt.sh** — Upgrade CBC → GCM for authenticated encryption

### 🟡 IMPORTANT (next sprint):
4. **KYS** — Brain key storage: encrypt the key_value at rest in the DB
5. **All apps** — Add rate limiting to all auth endpoints (KYS has this ✅)
6. **All apps** — Add `SESSION_COOKIE_SECURE=True` when HTTPS confirmed

### 🟢 NICE TO HAVE (future):
7. JWT-based auth for API tokens (more scalable than our DB approach)
8. Argon2id for password hashing (stronger than bcrypt)
9. Full DB encryption with SQLCipher
10. TOTP/2FA for admin accounts

---

## 8. THE GOLDEN RULES (memorize these)

1. **Never store plaintext passwords** — always hash with bcrypt/Argon2
2. **Never commit secrets** — use env vars and /root/.secrets/
3. **Encrypt then authenticate** — use GCM or add HMAC after CBC
4. **Rotate everything** — tokens 90 days, passwords when in doubt
5. **HTTPS everywhere** — no exceptions in production
6. **Defense in depth** — assume one layer will fail, have a backup
7. **Least privilege** — tokens should only do what they need to
8. **Never roll your own crypto** — use OpenSSL, cryptography.py, bcrypt

---

*This is a living document. Update as we learn and implement.*
