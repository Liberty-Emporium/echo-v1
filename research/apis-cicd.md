# REST APIs & CI/CD — Research Notes
**Researched:** 2026-04-14 | Echo's Self-Education Session

---

## REST API Design Best Practices

### URI Design Rules
```
# Good URIs — nouns, plural, hierarchical
GET    /users              # List all users
GET    /users/123          # Get user 123
POST   /users              # Create user
PUT    /users/123          # Update user 123 (full replace)
PATCH  /users/123          # Update user 123 (partial)
DELETE /users/123          # Delete user 123

# Relationships
GET /clients/acme/invoices         # ACME's invoices
GET /clients/acme/invoices/456     # Specific invoice

# Filtering via query params
GET /users?active=true&plan=pro
GET /invoices?status=pending&limit=20&offset=40

# Bad URIs — never do these
GET /getUsers
GET /cust
POST /createUser
GET /user-info
```

### HTTP Status Codes — Use Them Correctly
| Code | Meaning | When |
|------|---------|------|
| 200 | OK | Successful GET/PUT/PATCH |
| 201 | Created | Successful POST (new resource) |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Client sent invalid data |
| 401 | Unauthorized | Not authenticated |
| 403 | Forbidden | Authenticated but no permission |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate (email already exists) |
| 422 | Unprocessable Entity | Validation failed |
| 429 | Too Many Requests | Rate limited |
| 500 | Internal Server Error | Server bug |
| 503 | Service Unavailable | Stripe down, DB unreachable |

### API Versioning
URI versioning is most common:
```
/api/v1/users
/api/v2/users  # Breaking change
```

**When to bump version:**
- Removing a field from response
- Changing field types
- Changing auth requirements
- Breaking webhook payload format

**Never version for:**
- Adding new optional fields (backward compatible)
- New endpoints
- Bug fixes

### Authentication
```python
# JWT Bearer Token pattern (our current approach)
headers = {'Authorization': f'Bearer {token}'}

# JWT structure
# header.payload.signature
# payload contains: user_id, role, exp (expiration), iat (issued at)

import jwt, datetime

def generate_token(user_id, role):
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        'iat': datetime.datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated
```

### Rate Limiting
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1000 per day", "100 per hour"]
)

# Tighter limit for sensitive endpoints
@app.route('/api/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    ...

@app.route('/api/reset-password', methods=['POST'])
@limiter.limit("3 per hour")
def reset_password():
    ...
```

### Pagination
```python
@app.route('/api/v1/clients')
@require_auth
def list_clients():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)

    clients = Client.query.paginate(page=page, per_page=per_page)

    return jsonify({
        'data': [c.to_dict() for c in clients.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': clients.total,
            'pages': clients.pages,
            'has_next': clients.has_next,
            'has_prev': clients.has_prev
        }
    })
```

---

## GitHub Actions CI/CD for Our Flask Apps

### Basic Test Workflow
```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          sudo apt-get install -y python3-flask python3-sqlite3
          pip install pytest pytest-flask

      - name: Run tests
        run: pytest tests/ -v --tb=short
        env:
          FLASK_ENV: testing
          SECRET_KEY: test-secret-key
          DATA_DIR: /tmp/test-data
```

### Deploy Workflow (After Tests Pass)
```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pytest tests/ -v

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install Railway CLI
        run: npm install -g @railway/cli
      - name: Deploy
        run: railway up
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

### Security Scanning Workflow
```yaml
# .github/workflows/security.yml
name: Security Scan

on: [push]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install bandit safety
      - name: Bandit security scan
        run: bandit -r . -x tests/ -ll
      - name: Check for known vulnerabilities
        run: safety check
```

### Writing Testable Flask Code
```python
# conftest.py
import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app('testing')
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_client(client):
    """Client with valid auth token"""
    # Login and return client with auth headers
    response = client.post('/login', json={
        'email': 'admin@test.com',
        'password': 'admin1'
    })
    token = response.json['token']
    client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {token}'
    return client

# test_auth.py
def test_login_success(client):
    response = client.post('/login', json={
        'email': 'admin@test.com',
        'password': 'admin1'
    })
    assert response.status_code == 200
    assert 'token' in response.json

def test_login_wrong_password(client):
    response = client.post('/login', json={
        'email': 'admin@test.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401

def test_login_rate_limited(client):
    for _ in range(6):
        client.post('/login', json={'email': 'x', 'password': 'x'})
    response = client.post('/login', json={'email': 'x', 'password': 'x'})
    assert response.status_code == 429
```

---

## Background Jobs — When We Need Them

Currently all our routes are synchronous. This is fine for small scale.
When to add async background jobs:

### Signs You Need Background Jobs
- Email sending adds >500ms to response time
- AI API calls timeout in browser
- Generating reports takes >2 seconds
- Bulk operations (import CSV, mass email)

### Celery + Redis Pattern (For Later)
```python
# tasks.py
from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379')

@celery.task
def send_trial_expiry_email(user_id):
    user = User.query.get(user_id)
    email_service.send_trial_expiry(user.email)

# Route — returns immediately
@app.route('/trial/start', methods=['POST'])
def start_trial():
    user = create_trial_user(request.form)
    send_trial_expiry_email.delay(user.id)  # Async!
    return jsonify({'success': True})
```

### Simpler Alternative for Railway: Thread-Based
```python
import threading

def send_email_async(to, subject, body):
    thread = threading.Thread(
        target=actual_send_email,
        args=(to, subject, body)
    )
    thread.daemon = True
    thread.start()

# Use in routes
send_email_async(user.email, "Welcome!", welcome_body)
return jsonify({'success': True})  # Returns immediately
```
