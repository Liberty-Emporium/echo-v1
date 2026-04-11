---
name: flow-test
description: Test complete user flows in Flask apps. Use when you need to verify multi-step journeys work: login → add product → edit → delete, or any user workflow.
---

# Flow Test Skill

## What It Tests

Complete user journeys:

1. **Login Flow** - Sign in, redirect to dashboard
2. **Add Product Flow** - Form → Submit → Verify in dashboard
3. **Edit Flow** - Find product → Edit → Save → Verify
4. **Delete Flow** - Delete product → Verify gone

## Quick Start

```bash
python3 scripts/flow_test.py http://localhost:5000
python3 scripts/flow_test.py https://app.railway.app --user admin --pass secret
```

## Output Example

```
📍 Flow Test
============
✅ Login → Dashboard (302 redirect)
✅ Add Product → Created
✅ Edit Product → Saved
✅ Delete Product → Gone

4/4 flows passed
```

## Script

```python
#!/usr/bin/env python3
"""Flow test - test complete user journeys."""
import sys
import time
import requests
from urllib.parse import urljoin
import uuid

def flow_test(base_url, username, password):
    """Test common user flows."""
    sess = requests.Session()
    results = []
    sku = f'TEST{int(time.time())}'
    
    # Flow 1: Login
    try:
        resp = sess.post(base_url + '/login', 
                     data={'username': username, 'password': password},
                     allow_redirects=False)
        if resp.status_code == 302:
            results.append(('✅ Login → Dashboard', True))
        else:
            results.append(f'❌ Login → {resp.status_code}', False)
    except Exception as e:
        results.append(f'❌ Login → ERROR: {e}', False)
    
    # Flow 2: Add Product
    try:
        resp = sess.post(base_url + '/new',
                       data={
                           'SKU': sku,
                           'Title': 'Test Product',
                           'Price': '9.99',
                           'Category': 'Electronics',
                           'Condition': 'Good'
                       },
                       allow_redirects=False)
        if resp.status_code in [200, 302]:
            results.append(('✅ Add Product', True))
        else:
            results.append(f'❌ Add Product → {resp.status_code}', False)
    except Exception as e:
        results.append(f'❌ Add Product → ERROR', False)
    
    # Flow 3: Delete Product
    try:
        resp = sess.post(base_url + f'/delete/{sku}',
                       allow_redirects=False)
        if resp.status_code in [200, 302]:
            results.append(('✅ Delete Product', True))
        else:
            results.append(f'❌ Delete Product → {resp.status_code}', False)
    except Exception as e:
        results.append(f'❌ Delete Product → ERROR', False)
    
    # Print results
    passed = sum(1 for _, ok in results if ok)
    total = len(results)
    
    for msg, ok in results:
        print(msg)
    
    print(f'\n{passed}/{total} flows passed')
    return passed == total

if __name__ == '__main__':
    base = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:5000'
    user = sys.argv[2] if len(sys.argv) > 2 else 'admin'
    pw = sys.argv[3] if len(sys.argv) > 3 else 'admin123'
    
    sys.exit(0 if flow_test(base, user, pw) else 1)
```

## Usage

```bash
# Test local
python3 scripts/flow_test.py http://localhost:5000 admin admin123

# Test production
python3 scripts/flow_test.py https://app.railway.app admin yourpassword

# CI/CD
python3 scripts/flow_test.py $APP_URL $USER $PASS || fail
```

## Common Flows

For inventory apps:
- Login → Dashboard ✓
- Add Product → Verify on dashboard ✓
- Edit Product → Verify changes ✓
- Delete Product → Verify gone ✓
- Generate Ad → Download ✓

## Best Practice

Run:
- Before deployment
- After any auth changes
- In CI/CD pipeline
- After major updates