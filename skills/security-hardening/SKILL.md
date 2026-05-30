# SKILL: Security Hardening

> OWASP Top 10 protection for web applications — auth, headers, input validation, encryption.

## OWASP Top 10 (2024-2025)

| # | Risk | Prevention |
|---|------|------------|
| A01 | Broken Access Control | RBAC, server-side checks, no client-side auth |
| A02 | Cryptographic Failures | bcrypt, HTTPS, no hardcoded secrets |
| A03 | Injection | Parameterized queries, input validation |
| A04 | Insecure Design | Threat modeling, secure patterns |
| A05 | Security Misconfig | Hardened headers, minimal permissions |
| A06 | Vulnerable Components | Dependency scanning, auto-updates |
| A07 | Auth Failures | bcrypt, JWT expiry, rate limiting |
| A08 | Data Integrity | Signed updates, CI/CD verification |
| A09 | Logging Gaps | Audit logs, monitoring |
| A10 | SSRF | URL validation, network segmentation |

## Security Headers (Set These On Every App)
```nginx
# Nginx config
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "DENY" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'nonce-{random}'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self' https://api.stripe.com; frame-ancestors 'none';" always;
add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;
```

```python
# FastAPI middleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["yourdomain.com", "*.yourdomain.com"]
)
```

## Input Validation & Injection Prevention
```python
# ALWAYS validate input with Pydantic
from pydantic import BaseModel, validator, EmailStr
import bleach

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    bio: str | None = None
    
    @validator("name")
    def sanitize_name(cls, v):
        v = bleach.clean(v, tags=[], strip=True)
        if len(v) < 2 or len(v) > 100:
            raise ValueError("Name must be 2-100 characters")
        return v.strip()
    
    @validator("bio")
    def sanitize_bio(cls, v):
        if v:
            return bleach.clean(v, tags=["b", "i", "em", "strong"], strip=True)
        return v

# SQL Injection prevention — ALWAYS use parameterized queries
# BAD:
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
# GOOD:
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
# GOOD (SQLAlchemy):
user = session.query(User).filter(User.id == user_id).first()
```

## Authentication Security
```python
# Rate limiting per IP on auth endpoints
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@router.post("/auth/login")
@limiter.limit("5/minute")
async def login(request: Request, data: LoginData):
    user = await authenticate(data.email, data.password)
    if not user:
        # IMPORTANT: Always return same error message — don't reveal if email exists
        raise HTTPException(401, "Invalid email or password")
    
    # SECURE: Account lockout after N failed attempts
    if user.failed_login_attempts >= 5:
        raise HTTPException(429, "Account temporarily locked. Try again in 15 minutes.")
    
    # Generate token
    token = create_access_token({"sub": user.id, "role": user.role})
    
    # Log the login event
    await audit_log("login", user_id=user.id, ip=request.client.host)
    
    return {"access_token": token, "token_type": "bearer"}
```

## CORS Configuration
```python
# FastAPI — NEVER use allow_origins=["*"] in production
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yourdomain.com",
        "https://www.yourdomain.com",
        "http://localhost:3000",  # Only for dev
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "X-CSRF-Token"],
)
```

## CSRF Protection
```tsx
// Next.js — CSRF token for state-changing requests
async function submitForm(data: FormData) {
  const csrfToken = await fetch("/api/auth/csrf").then(r => r.json())
  
  await fetch("/api/projects", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRF-Token": csrfToken,
    },
    body: JSON.stringify(data),
  })
}
```

## Secrets Management
```bash
# NEVER commit secrets to git
# Use .env files (local) + platform env vars (production)

# Generate secure keys:
openssl rand -hex 32    # SECRET_KEY
openssl rand -base64 32 # JWT_SECRET

# .gitignore
.env
.env.local
.env.production
```

```python
# Python: load from env, fail fast if missing
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str  # Required — will fail if missing
    SECRET_KEY: str
    OPENROUTER_API_KEY: str = ""  # Optional with default
    
    class Config:
        env_file = ".env"
```

## File Upload Security
```python
import magic
from pathlib import Path

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

async def upload_file(file: UploadFile):
    # Check extension
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"File type not allowed: {ext}")
    
    # Check size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(400, f"File too large (max {MAX_FILE_SIZE // 1024 // 1024}MB)")
    
    # Check MIME type (not just extension)
    mime = magic.from_buffer(content, mime=True)
    if not mime.startswith(("image/", "application/pdf")):
        raise HTTPException(400, "Invalid file content")
    
    # Store with random filename (never use user-provided filename)
    safe_name = f"{uuid4().hex}{ext}"
    await save_file(content, safe_name)
    return {"filename": safe_name}
```

## Encryption at Rest (Sensitive Data)
```python
from cryptography.fernet import Fernet

key = Fernet.generate_key()  # Store in env var
cipher = Fernet(key)

def encrypt_pii(data: str) -> str:
    return cipher.encrypt(data.encode()).decode()

def decrypt_pii(encrypted: str) -> str:
    return cipher.decrypt(encrypted.encode()).decode()

# Use for: SSN, credit card last-4, medical records, etc.
# Do NOT encrypt: data you need to search/filter on
```

## Dependency Security Scanning
```bash
# Python
pip install pip-audit
pip-audit  # Check for known vulnerabilities

# Node.js
npm audit
npm audit fix

# Both in CI/CD
# GitHub: Enable Dependabot alerts
# npm install better-npm-audit
```

## Security Audit Checklist
- [ ] All passwords bcrypt-hashed (cost factor 12+)
- [ ] JWT tokens expire (15 min access / 7 day refresh)
- [ ] HTTP → HTTPS redirect (HSTS)
- [ ] CSP headers set (no unsafe-inline without nonce)
- [ ] CORS restricted to actual origins
- [ ] Input validated on server (Pydantic/Zod)
- [ ] SQL uses parameterized queries (no string interpolation)
- [ ] File uploads validated (extension + MIME + size)
- [ ] Rate limiting on all auth endpoints
- [ ] Secrets in env vars (never in code or git)
- [ ] Dependencies scanned for vulnerabilities
- [ ] Security headers set (X-Frame, X-Content-Type, etc.)
- [ ] Audit logs for auth events (login, logout, failed attempts)
- [ ] Error messages don't leak internal details
- [ ] Admin routes protected by role check
- [ ] API keys rotated regularly
