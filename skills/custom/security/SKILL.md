---
name: security
description: Full security toolkit for Jay's apps. Think like an attacker, scan Flask code, run deep audits (nmap/sqlmap/gobuster), and validate skills before loading. Use when auditing code, scanning for vulnerabilities, hardening apps, or vetting new skills.
---

# Security

## 1. Think Like an Attacker

### OWASP Top 10 Focus
1. **Injection** — SQL, NoSQL, Command
2. **Broken Auth** — Sessions, tokens
3. **Sensitive Data** — Passwords, keys exposed
4. **XXE** — XML parsing
5. **Broken Access** — Permissions
6. **Security Misconfiguration** — Debug mode, default creds
7. **XSS** — Unescaped output
8. **Insecure Deserialization**
9. **Known Vulnerable Components**
10. **Insufficient Logging**

### Quick Mental Check
- What if someone passes malicious input here?
- What can they access with a valid token?
- What data can be leaked from this endpoint?

---

## 2. Code Scan (Flask Apps)

```bash
# Hardcoded secrets
grep -rn "password\|api_key\|secret" *.py | grep -v env

# SQL injection risk
grep -rn "f\".*WHERE\|f'.*WHERE" *.py

# Debug mode left on
grep -rn "debug=True" *.py

# Missing auth decorators
grep -rn "@app.route" *.py | grep -v login_required
```

### Inline Python Scanner

```python
#!/usr/bin/env python3
import sys, re

def scan_file(filepath):
    with open(filepath) as f:
        lines = f.readlines()
    issues = []
    patterns = [
        (r'password\s*=\s*["\']', 'Hardcoded password'),
        (r'api[_-]?key\s*=\s*["\']', 'Hardcoded API key'),
        (r'secret[_-]?key\s*=\s*["\'][^"\']+["\']', 'Hardcoded secret key'),
        (r'sql\s*=\s*f["\']', 'Potential SQL injection'),
        (r'app\.run\(.*debug\s*=\s*True', 'Debug mode enabled'),
    ]
    for i, line in enumerate(lines, 1):
        for pattern, desc in patterns:
            if re.search(pattern, line, re.IGNORECASE):
                issues.append((i, desc, line.strip()[:60]))
    return issues

filepath = sys.argv[1] if len(sys.argv) > 1 else 'app.py'
issues = scan_file(filepath)
if not issues:
    print('✅ No issues found')
else:
    for line, desc, text in issues:
        print(f'Line {line}: ⚠️  {desc}\n  {text}')
    print(f'\nFound {len(issues)} issues')
    sys.exit(1)
```

```bash
python3 security_scan.py app.py
python3 security_scan.py app.py | grep -i secret
```

---

## 3. Deep Audit (nmap / sqlmap / gobuster)

### Tools Required
```bash
apt-get install -y nmap sqlmap gobuster
# SecLists wordlist: https://github.com/danielmiessler/SecLists
```

### Phase 1 — Recon
```bash
nmap -sV -p 80,443,8080 <target>
curl -I https://<target>  # Check response headers
gobuster dir -u https://<target> -w /usr/share/seclists/Discovery/Web-Content/common.txt
```

### Phase 2 — Vulnerability Scan
```bash
# SQL injection
sqlmap -u "https://<target>/login" --forms --batch

# XSS check
curl "https://<target>/search?q=<script>alert(1)</script>"

# Auth bypass attempts
curl https://<target>/admin
curl -H "X-Forwarded-For: 127.0.0.1" https://<target>/admin
```

### Phase 3 — Code Analysis (source available)
- Hardcoded secrets scan
- Dangerous function usage: `eval`, `exec`, `os.system`
- Missing CSRF protection on forms
- Password hashing strength (bcrypt > sha256 > plaintext)
- Session config: `SECRET_KEY`, `SESSION_COOKIE_HTTPONLY`, `SESSION_COOKIE_SECURE`

### Phase 4 — Report
Severity: **CRITICAL / HIGH / MEDIUM / LOW**
Save to: `/tmp/security-report-<date>.md`

Script: `skills/custom/security-audit/scripts/audit.py`

```bash
python3 skills/custom/security-audit/scripts/audit.py \
  --url https://liberty-emporium-and-thrift-inventory-app-production.up.railway.app \
  --deep
```

---

## 4. Skill Validation (Before Loading Unknown Skills)

### Default Policy
- ✅ ALLOW: score ≥ 80, no CRITICAL/HIGH issues
- 🟡 REVIEW: score ≥ 50 or has MEDIUM issues
- 🔴 BLOCK: score < 50 or any CRITICAL/HIGH issues

### What to Check
- Malicious patterns: `exec`, `eval`, `base64`, crypto obfuscation
- Unexpected network calls to suspicious domains
- Data exfiltration: unexpected file writes + network uploads
- Environment variable harvesting
- External command execution

### Reputation Signals (GitHub)
- Account age (older = more trusted)
- Stars/forks on repo
- Recent commit activity
- Known author?

---

## Issue Reference

| Issue | Risk | Fix |
|-------|------|-----|
| Hardcoded passwords | High | Use env vars |
| debug=True | High | Set False in prod |
| f-string SQL | High | Parameterized queries |
| Unescaped `{{}}` | Medium | Use `\|escape` filter |
| Missing @login_required | Medium | Add decorator |
| No CSRF protection | Medium | Flask-WTF CSRFProtect |
| SHA-256 passwords | Medium | Upgrade to bcrypt |
| No security headers | Medium | Add via after_request |

## Run Before Every Deploy
```bash
python3 security_scan.py app.py || exit 1
```
