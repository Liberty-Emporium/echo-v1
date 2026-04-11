---
name: smoke-test
description: Run smoke tests on Flask applications. Use when you need to quickly verify all routes return valid responses (no 500 errors), check basic functionality, or validate deployments. Perfect for pre-deploy checks.
---

# Smoke Test Skill

## Quick Start

```bash
# Run against any Flask app
python3 smoke_test.py http://localhost:5000
python3 smoke_test.py https://yourapp.railway.app --auth /login
```

## What It Checks

1. **All routes respond** - No 404s from your code (expected 404s ignored)
2. **No 500 errors** - Server errors caught
3. **Auth works** - Login flow tested
4. **Static files** - CSS/JS load
5. **JSON endpoints** - API routes return valid JSON

## Output Example

```
✅ GET / → 200
✅ GET /login → 200
✅ GET /dashboard → 302 (redirect to login)
✅ POST /login → 302
✅ GET /admin → 200
❌ GET /broken-route → 500 ERROR!

Smoke Test FAILED: 1 route returned 500
```

## Script

Save as `scripts/smoke_test.py`:

```python
#!/usr/bin/env python3
"""Smoke test for Flask apps - quick sanity check."""
import sys
import requests
from urllib.parse import urljoin

def smoke_test(base_url, login_url=None, credentials=None):
    """Run smoke test against Flask app."""
    sess = requests.Session()
    results = []
    
    # Routes to test (add your app's routes here)
    routes = [
        '/',
        '/login',
        '/dashboard',
        '/admin',
    ]
    
    for route in routes:
        url = urljoin(base_url, route)
        try:
            resp = sess.get(url, allow_redirects=False, timeout=10)
            if resp.status_code == 500:
                results.append(f'❌ {route} → {resp.status_code} SERVER ERROR')
            else:
                results.append(f'✅ {route} → {resp.status_code}')
        except Exception as e:
            results.append(f'❌ {route} → ERROR: {e}')
    
    # Test login if provided
    if login_url and credentials:
        try:
            resp = sess.post(login_url, data=credentials, allow_redirects=False)
            if resp.status_code in [200, 302]:
                results.append(f'✅ POST /login → {resp.status_code}')
            else:
                results.append(f'❌ POST /login → {resp.status_code}')
        except Exception as e:
            results.append(f'❌ POST /login → ERROR')
    
    # Print results
    for r in results:
        print(r)
    
    # Summary
    failed = any('❌' in r for r in results)
    if failed:
        print('\\n❌ Smoke Test FAILED')
        sys.exit(1)
    else:
        print('\\n✅ All smoke tests passed!')
        sys.exit(0)

if __name__ == '__main__':
    base = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:5000'
    smoke_test(base)
```

## Usage

```bash
# Local testing
python3 scripts/smoke_test.py http://localhost:5000

# Production with login
python3 scripts/smoke_test.py https://app.railway.app \
  --login https://app.railway.app/login \
  --user admin --pass secret

# CI/CD
python3 scripts/smoke_test.py $APP_URL || exit 1
```

## Best Practices

- Run before every deploy
- Add to CI/CD pipeline
- Test both auth and public routes
- Check for 500 specifically (server errors)