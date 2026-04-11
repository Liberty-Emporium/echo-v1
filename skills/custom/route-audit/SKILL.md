---
name: route-audit
description: Map all routes in a Flask app and check for dead links. Use when you need to audit an application for broken routes, find all endpoints, or verify link consistency.
---

# Route Audit Skill

## Quick Start

```bash
python3 scripts/route_audit.py http://localhost:5000
python3 scripts/route_audit.py https://app.railway.app --auth
```

## What It Does

1. **Extract all routes** - From app source code
2. **Test each route** - Verify it returns valid response
3. **Find dead links** - 404s and 500s
4. **Report coverage** - Which routes are tested

## Output Example

```
📍 Route Audit
============
✅ / (200)
✅ /login (200)
✅ /dashboard (302) → requires auth
✅ /admin/users (200)
✅ /reports (200)
✅ /markdown-calculator (200)
✅ /slow-movers (200)
✅ /fifo (200)

8 routes tested, 0 dead links
```

## Script

```python
#!/usr/bin/env python3
"""Route audit - find and test all routes."""
import re
import sys
import requests
import subprocess

def get_routes(app_file):
    """Extract @app.route decorators from source."""
    result = subprocess.run(['grep', '-E', r'@app\.route', app_file], capture_output=True, text=True)
    routes = []
    for line in result.stdout.split('\n'):
        match = re.search(r"@app\.route\(['\"])(.+?)\1", line)
        if match:
            routes.append(match.group(2))
    return routes

def test_routes(base_url, routes):
    """Test each route."""
    sess = requests.Session()
    results = []
    for route in routes:
        try:
            resp = sess.get(base_url + route, timeout=5)
            results.append((route, resp.status_code))
        except:
            results.append((route, 'ERROR'))
    return results

def main():
    app_file = sys.argv[1] if len(sys.argv) > 1 else 'app.py'
    base = sys.argv[2] if len(sys.argv) > 2 else 'http://localhost:5000'
    
    print(f'📍 Route Audit: {app_file}')
    print('=' * 40)
    
    routes = get_routes(app_file)
    print(f'Found {len(routes)} routes')
    
    results = test_routes(base, routes)
    dead = 0
    for route, status in results:
        if status in [404, 500, 'ERROR']:
            print(f'❌ {route} → {status}')
            dead += 1
        else:
            print(f'✅ {route} → {status}')
    
    print(f'\n{len(routes)} tested, {dead} dead')
    sys.exit(1 if dead > 0 else 0)

if __name__ == '__main__':
    main()
```

## Usage

```bash
# Audit local app
python3 scripts/route_audit.py app_with_ai.py http://localhost:5000

# Audit production
python3 scripts/route_audit.py app.py https://app.railway.app

# GitHub repo
gh repo clone owner/repo
cd repo
python3 ../skills/route-audit/scripts/route_audit.py app.py http://localhost:5000
```

## Common Routes to Check

- `/` - Home
- `/login`, `/logout`, `/signup`
- `/dashboard`
- `/admin/*`
- `/reports`, `/reports/sales`
- `/api/*` - API endpoints
- `/new`, `/edit/<sku>`, `/delete/<sku>`
- `/markdown-calculator`, `/slow-movers`, `/fifo`

## Best Practice

Run after:
- Every new feature deployment
- Adding new routes
- Refactoring code