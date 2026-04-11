---
name: security-audit
description: Scan for security vulnerabilities in applications. Use when you need to check for common security issues, hardcoded secrets, or vulnerabilities.
---

# Security Audit

## Quick Scan

### Check for Secrets
```bash
# Hardcoded passwords/keys
grep -rn "password\s*=\s*['\"]" . --include="*.py"
grep -rn "api[_-]?key\|secret\|token" . --include="*.py" | grep -v "os.environ\|os.getenv"

# AWS keys
grep -rn "AKIA\|AWS_SECRET" .

# Private keys
grep -rn "BEGIN.*PRIVATE KEY" .
```

### Check Dependencies
```bash
# pip-audit (Python)
pip install pip-audit
pip-audit

# npm audit (Node.js)
npm audit
```

## Common Vulnerabilities

### SQL Injection
```python
# BAD
query = f"SELECT * FROM users WHERE id = {user_id}"

# GOOD
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

### XSS
```python
# BAD (Flask/Jinja)
{{ user_input }}

# GOOD
{{ user_input | escape }}
# or
{{ user_input | safe }}  # ONLY if validated
```

### Command Injection
```python
# BAD
os.system(f"convert {filename}")

# GOOD
subprocess.run(["convert", filename], shell=False)
```

## OWASP Top 10

1. **Injection** - Use parameterized queries
2. **Broken Auth** - Rate limiting, secure sessions
3. **Sensitive Data** - Encrypt at rest, TLS in transit
4. **XML External Entities** - Disable XXE parsing
5. **Broken Access Control** - Check perms server-side
6. **Security Misconfig** - Minimal headers, secure defaults
7. **XSS** - Escape output
8. **Insecure Deserialization** - Don't unpickle unknown data
9. **Using Known Vulnerable Components** - Keep deps updated
10. **Insufficient Logging** - Log auth failures, errors

## Report Template

```
## Security Audit: [app name]

### High
- [Issue] - [Location]

### Medium
- [Issue] - [Location]

### Low
- [Issue] - [Location]

### Recommendations
- [Fix description]
```