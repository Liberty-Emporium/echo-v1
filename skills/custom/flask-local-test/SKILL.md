# flask-local-test

**Version:** 1.0.0
**Created:** 2026-04-14
**Author:** Echo

## Description

Test Flask app routes locally before pushing to Railway. Catches template errors, 500s, missing templates, and broken routes in seconds — without waiting for Railway to deploy.

Born from: Multiple rounds of push → wait 35 seconds → still 500 → debug → push again. Local testing would have caught all of these in under 5 seconds.

## When To Use

- ALWAYS before `git push` on any Flask app change
- After adding new routes or templates
- After editing base.html or any shared template
- When debugging a 500 error

## Usage

```python
# Quick test — paste this at the bottom of any Flask app dir
import sys, os
os.environ['DATA_DIR'] = '/tmp/test_data_dir'

# Import the app
import app as flask_app

flask_app.app.config['TESTING'] = True
client = flask_app.app.test_client()

routes_to_test = [
    ('GET', '/', None),           # (method, path, expected_text)
    ('GET', '/login', 'Sign In'),
    ('GET', '/dashboard', None),
    ('GET', '/pricing', 'Pricing'),
]

passed = failed = 0
for method, path, expected in routes_to_test:
    if method == 'GET':
        resp = client.get(path)
    status = resp.status_code
    body = resp.data.decode('utf-8', errors='replace')
    ok = status < 400 and (not expected or expected.lower() in body.lower())
    icon = '✅' if ok else '❌'
    print(f"{icon} {method} {path} → HTTP {status}")
    if not ok:
        print(f"   Error: {body[:200]}")
        failed += 1
    else:
        passed += 1

print(f"\n{passed} passed, {failed} failed")
```

## Full Workflow

```bash
# 1. Install Flask locally if needed
apt-get install -y python3-flask

# 2. Run quick test
cd /tmp/MyApp && DATA_DIR=/tmp/test python3 -c "
import app; app.app.config['TESTING']=True
c = app.app.test_client()
for path in ['/', '/login', '/dashboard', '/pricing']:
    r = c.get(path)
    print(f'HTTP {r.status_code} {path}')
    if r.status_code >= 400:
        print(r.data[:300].decode())
"

# 3. Only push if all routes return 200
git push origin main
```

## Common Errors Caught

| Error | Cause | Fix |
|-------|-------|-----|
| `TemplateSyntaxError: Missing end of comment tag` | `{#` in CSS | Use jinja2-safe-css skill |
| `TemplateNotFound: pricing.html` | Missing template file | Create the template |
| `KeyError: 'username'` | Session variable not set | Fix the route logic |
| `sqlite3.OperationalError` | DB not initialized | Check init_db() runs at startup |

## Notes

- Set `DATA_DIR=/tmp/test_xxx` to avoid polluting real data
- Flask test client does NOT need gunicorn or a real server
- Errors show the full traceback — much faster than reading Railway logs
