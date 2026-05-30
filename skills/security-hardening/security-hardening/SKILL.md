---
name: security-hardening
description: Web application security patterns for client SaaS projects. Covers XSS, CSRF, SQL injection, auth security, supply chain security, and OWASP Top 10. Updated from OWL research security-engineering md.
---

# Security Hardening — Shared Skill for OWL & Bull

## Purpose
Security patterns and checklists for client SaaS applications. Both agents load this when building auth systems, API routes, or handling user data.

## OWASP Top 10 (2024) — Quick Reference

| Risk | What It Is | Prevention |
|------|-----------|------------|
| **A01: Broken Auth** | Weak passwords, session issues | bcrypt/argon2, HttpOnly cookies, rate limiting |
| **A02: Cryptographic Failures** | Weak encryption, exposed keys | AES-256, TLS 1.3, env vars only |
| **A03: Injection** | SQL, NoSQL, OS, LDAP injection | Parameterized queries, ORM, input validation |
| **A04: Insecure Design** | Missing security in architecture | Threat modeling, security-first design |
| **A05: Security Misconfiguration** | Default creds, verbose errors | Config audit, minimal permissions |
| **A06: Vulnerable Components** | Outdated npm/pip packages | `npm audit`, pin versions, lock files |
| **A07: Auth Failures** | Broken MFA, credential stuffing | MFA, account lockout, breach detection |
| **A08: Data Integrity** | Unsigned updates, CI/CD attacks | Code signing, pipeline security |
| **A09: Logging Failures** | No audit trail, silent breaches | Centralized logging, alerting |
| **A10: SSRF** | Server requests to internal resources | URL allowlisting, network segmentation |

## XSS Prevention

### Three Types
1. **Reflected XSS** → malicious script in URL, reflected in response
2. **Stored XSS** → malicious script stored in DB, served to all users
3. **DOM-based XSS** → vulnerability in client-side JS, never hits server

### Prevention
- **Output encoding** — encode user data before inserting into HTML
- **CSP headers** — `Content-Security-Policy: default-src 'self'; script-src 'self'`
- **HttpOnly cookies** — prevents JS from reading session cookies
- **React/Next.js auto-escapes** by default — but dangerous with `dangerouslySetInnerHTML`
- **Sanitize rich text** with DOMPurify if allowing HTML input

## CSRF Prevention
- SameSite cookie attribute (`SameSite=Lax` or `Strict`)
- CSRF tokens for state-changing requests
- Next.js Server Actions include CSRF protection by default

## SQL Injection Prevention
- Always use parameterized queries (Drizzle ORM does this)
- Never interpolate user input into SQL strings
- Supabase RLS provides additional protection layer

## Auth Security

### Password Storage
```javascript
// Use bcrypt (cost factor 12) or Argon2id
import bcrypt from 'bcrypt';
const hash = await bcrypt.hash(password, 12);
const valid = await bcrypt.hash(password, storedHash);
```

### Session Security
- HttpOnly + Secure + SameSite cookies
- Session timeout: 30 min inactivity, 24h max
- Rotate session tokens on login
- Rate limit auth endpoints (5 attempts per 15 min)

### For Non-Technical Users (Client Staff)
- **PIN login** is better than passwords for bakery/retail staff
- 4-6 digit PIN, bcrypt hashed
- Account lockout after 5 failed attempts
- Admin can reset PINs

## Supply Chain Security (CRITICAL — 2026)
- npm ecosystem actively under attack (Mini Shai-Hulud: 323 packages compromised)
- Microsoft PyPI packages compromised
- Prevention:
  - Pin all dependency versions in lock files
  - Run `npm audit` before every deploy
  - `npm install --ignore-scripts` in production builds
  - Rotate credentials regularly
  - Use `.npmrc` with `ignore-scripts=true`

## Security Headers (Every Next.js App)
```javascript
// next.config.js or middleware
const headers = [
  { 'X-Frame-Options': 'DENY' },
  { 'X-Content-Type-Options': 'nosniff' },
  { 'Referrer-Policy': 'strict-origin-when-cross-origin' },
  { 'Strict-Transport-Security': 'max-age=63072000; includeSubDomains' },
  { 'Content-Security-Policy': "default-src 'self'; img-src 'self' data:; script-src 'self'" },
  { 'Permissions-Policy': 'camera=(), microphone=(), geolocation=()' },
]
```

## Security Audit Checklist (Before Every Deploy)
- [ ] No API keys in code or database (env vars only)
- [ ] All auth routes validate session
- [ ] Rate limiting on auth endpoints
- [ ] Input validation on all forms (Zod)
- [ ] CSP headers configured
- [ ] `npm audit` passes or findings documented
- [ ] Database backups automated
- [ ] Error messages don't leak sensitive info
- [ ] Dependencies pinned to specific versions
