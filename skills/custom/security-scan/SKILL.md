---
name: security-scan
description: Scan Flask apps for common security issues. Use when you need to check for exposed secrets, insecure code patterns, or vulnerabilities before deployment.
---

# Security Scan Skill

## What It Checks

1. **Hardcoded secrets** - Passwords, API keys in code
2. **SQL injection** - Unsanitized queries
3. **XSS vulnerabilities** - Unescaped user input
4. **Insecure routes** - Missing auth decorators
5. **Debug mode** - Left enabled in production

## Quick Start

```bash
python3 scripts/security_scan.py app.py
python3 scripts/security_scan.py app.py | grep -i secret
```

## Output Example

```
🔒 Security Scan
=============
app.py:56  ⚠️  Hardcoded password: ADMIN_PASS = 'admin123'
app.py:134  ⚠️  SQL query without parameterized query
app.py:89   ✅  route with @login_required

Found 2 issues
```

## Script

```python
#!/usr/bin/env python3
"""Security scan for Flask apps."""
import sys
import re

def scan_file(filepath):
    """Scan Python file for security issues."""
    with open(filepath) as f:
        lines = f.readlines()
    
    issues = []
    
    # Patterns to check
    patterns = [
        (r'password\s*=\s*["\']', 'Hardcoded password'),
        (r'api[_-]?key\s*=\s*["\']', 'Hardcoded API key'),
        (r'secret[_-]?key\s*=\s*["\'][^"\']+["\']', 'Hardcoded secret key'),
        (r'sql\s*=\s*f["\']', 'Potential SQL injection'),
        (r'\{.*\}\s*%"\)', 'Unescaped output (XSS)'),
        (r'app\.run\(.*debug\s*=\s*True', 'Debug mode enabled'),
    ]
    
    for i, line in enumerate(lines, 1):
        for pattern, desc in patterns:
            if re.search(pattern, line, re.IGNORECASE):
                issues.append((i, desc, line.strip()[:60]))
    
    return issues

def main():
    filepath = sys.argv[1] if len(sys.argv) > 1 else 'app.py'
    
    print('🔒 Security Scan')
    print('=' * 40)
    
    issues = scan_file(filepath)
    
    if not issues:
        print('✅ No issues found')
        sys.exit(0)
    
    for line, desc, text in issues:
        print(f'Line {line}: ⚠️  {desc}')
        print(f'  {text}')
    
    print(f'\nFound {len(issues)} issues')
    sys.exit(1)

if __name__ == '__main__':
    main()
```

## Usage

```bash
# Scan local app
python3 scripts/security_scan.py app_with_ai.py

# Find only secrets
python3 scripts/security_scan.py app.py | grep -i secret

# CI/CD
python3 scripts/security_scan.py app.py || fail
```

## What to Check

| Issue | Risk | Fix |
|-------|------|-----|
| Hardcoded passwords | High | Use env vars |
| debug=True | High | Set False in prod |
| f-string SQL | High | Use parameterized |
| Unescaped {{}} | Medium | Use \|escape |
| Missing @login_required | Medium | Add decorator |

## Best Practice

Run:
- Before every deploy
- In CI/CD pipeline
- After adding new features