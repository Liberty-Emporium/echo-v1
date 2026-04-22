#!/usr/bin/env python3
"""
Liberty-Emporium Flask App Security Auditor
Checks an app.py for known security issues.

Usage: python3 security_audit.py <path_to_app.py>
"""
import sys, re, pathlib

def audit(filepath):
    path = pathlib.Path(filepath)
    if not path.exists():
        print(f"ERROR: {filepath} not found")
        sys.exit(1)

    code = path.read_text()
    issues = []
    passes = []

    checks = [
        # (label, pass_condition, severity)
        ("debug=False in production",
         lambda c: 'debug=False' in c or 'debug=False' in c.lower()
                   or 'DEBUG' not in c.upper().split('APP.RUN')[1].split(')')[0]
                   if 'app.run(' in c.lower() else True,
         "CRITICAL"),
        ("bcrypt password hashing",
         lambda c: 'bcrypt' in c.lower(),
         "HIGH"),
        ("no raw SHA-256 for passwords",
         lambda c: not ('hashlib.sha256' in c and 'password' in c.lower()
                        and 'SECRET_KEY' not in c[max(0,c.find('hashlib.sha256')-200):c.find('hashlib.sha256')]),
         "HIGH"),
        ("login rate limiting",
         lambda c: 'rate_limit' in c.lower() or 'is_rate_limited' in c,
         "MEDIUM"),
        ("CSRF protection",
         lambda c: 'csrf' in c.lower(),
         "MEDIUM"),
        ("security headers (@after_request)",
         lambda c: 'after_request' in c and ('X-Frame' in c or 'x-frame' in c.lower()),
         "MEDIUM"),
        ("SESSION_COOKIE_HTTPONLY",
         lambda c: 'SESSION_COOKIE_HTTPONLY' in c,
         "MEDIUM"),
        ("SESSION_COOKIE_SAMESITE",
         lambda c: 'SESSION_COOKIE_SAMESITE' in c,
         "LOW"),
        ("no hardcoded secrets",
         lambda c: not re.search(r'(api_key|secret_key|password)\s*=\s*["\'][^"\']{10,}["\']', c, re.IGNORECASE),
         "HIGH"),
        ("parameterized SQL (no f-string queries)",
         lambda c: not re.search(r'execute\s*\(\s*f["\']', c),
         "HIGH"),
        ("/health endpoint",
         lambda c: "'/health'" in c or '"/health"' in c,
         "LOW"),
        ("login_required decorator",
         lambda c: 'login_required' in c,
         "MEDIUM"),
    ]

    print(f"\n{'='*56}")
    print(f"  🔍 Security Audit: {path.name}")
    print(f"{'='*56}")

    for label, check_fn, severity in checks:
        try:
            passed = check_fn(code)
        except Exception:
            passed = False
        if passed:
            passes.append(label)
            print(f"  ✅  {label}")
        else:
            issues.append((label, severity))
            print(f"  ❌  [{severity}] {label}")

    print(f"\n{'='*56}")
    print(f"  Score: {len(passes)}/{len(checks)} checks passed")

    if issues:
        print(f"\n  ⚠️  Issues to fix:")
        for label, sev in sorted(issues, key=lambda x: ['CRITICAL','HIGH','MEDIUM','LOW'].index(x[1])):
            print(f"     [{sev}] {label}")
    else:
        print(f"\n  🎉 All checks passed!")

    print(f"{'='*56}\n")
    return len(issues)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 security_audit.py <path_to_app.py>")
        sys.exit(1)
    sys.exit(1 if audit(sys.argv[1]) > 0 else 0)
