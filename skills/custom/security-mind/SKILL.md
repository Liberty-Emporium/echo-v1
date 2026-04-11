---
name: security-mind
description: Think like an attacker to find vulnerabilities. Use when you need to: security audit code, find vulnerabilities, think like a hacker.
---

# Security Mind

## OWASP Top 10 Focus

1. **Injection** - SQL, NoSQL, Command
2. **Broken Auth** - Sessions, tokens
3. **Sensitive Data** - Passwords, keys exposed
4. **XXE** - XML parsing
5. **Broken Access** - Permissions

## Quick Scan

```bash
# Secrets
grep -rn "password\|api_key\|secret" *.py | grep -v env

# SQL injection
grep -rn "f\".*WHERE\|f'.*WHERE" *.py

# Hardcoded URLs
grep -rn "https://\|http://" *.py | grep -v allowed
```

## Think Like Attacker

- What if someone passes this input?
- What can I access with this token?
- What data can I leak?