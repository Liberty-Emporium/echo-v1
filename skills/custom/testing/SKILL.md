---
name: testing
description: Write and run tests for applications. Use when you need to create test suites, run tests, implement TDD, or debug test failures.
---

# Testing

## Python/Flask Tests

### pytest setup
```python
# conftest.py
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# test_routes.py
def test_home(client):
    resp = client.get('/')
    assert resp.status_code == 200

def test_login_success(client):
    resp = client.post('/login', data={'username': 'admin', 'password': 'admin123'})
    assert resp.status_code == 302  # redirect

def test_login_failure(client):
    resp = client.post('/login', data={'username': 'admin', 'password': 'wrong'})
    assert b'Invalid' in resp.data
```

### Run tests
```bash
pytest -v
pytest -v --tb=short
pytest -v -k "login"
pytest --cov=app --cov-report=html
```

## Node.js Tests

### jest setup
```javascript
// sum.js
export function sum(a, b) {
  return a + b;
}

// sum.test.js
import { sum } from './sum';

test('adds 1 + 2 to equal 3', () => {
  expect(sum(1, 2)).toBe(3);
});
```

### Run tests
```bash
npm test
npm test -- --coverage
npm test -- --watch
```

## TDD Workflow

1. Write failing test
2. Write minimal code to pass
3. Refactor
4. Repeat

## Test Patterns

- **Unit tests**: Test individual functions
- **Integration**: Test routes/endpoints
- **Fixtures**: Mock data for tests
- **Factories**: Generate test data
- **Spies**: Verify function calls