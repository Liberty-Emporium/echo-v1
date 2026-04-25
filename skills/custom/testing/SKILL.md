---
name: testing
description: Write and run tests for applications — Flask/Python, Node.js/JavaScript, TypeScript, React, Go, Rust, Django, REST APIs, and E2E Playwright flows. Use when creating test suites, running tests, implementing TDD, or debugging test failures.
---

# Testing

## Python / Flask (pytest)

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
    assert resp.status_code == 302

def test_login_failure(client):
    resp = client.post('/login', data={'username': 'admin', 'password': 'wrong'})
    assert b'Invalid' in resp.data
```

```bash
pytest -v
pytest -v --tb=short
pytest -v -k "login"
pytest --cov=app --cov-report=html
```

## Django (pytest-django)

```python
# pytest.ini
[pytest]
DJANGO_SETTINGS_MODULE = myproject.settings

# tests/test_views.py
import pytest
from django.test import Client

@pytest.mark.django_db
def test_home():
    client = Client()
    response = client.get('/')
    assert response.status_code == 200
```

```bash
pytest --ds=myproject.settings
python manage.py test
coverage run manage.py test && coverage report
```

## Node.js / JavaScript (Jest)

```javascript
// sum.test.js
import { sum } from './sum';
test('adds 1 + 2 to equal 3', () => {
  expect(sum(1, 2)).toBe(3);
});
```

```bash
npm test
npm test -- --coverage
npm test -- --watch
```

## TypeScript (Jest / Vitest)

```typescript
// utils.test.ts
import { add } from './utils';
describe('add', () => {
  it('returns correct sum', () => {
    expect(add(2, 3)).toBe(5);
  });
});
```

```bash
npx jest --coverage
npx vitest run
npx vitest --coverage
```

## React / Next.js (Vitest + React Testing Library)

```javascript
import { render, screen } from '@testing-library/react'
import Button from './Button'

test('renders button text', () => {
  render(<Button>Click me</Button>)
  expect(screen.getByText('Click me')).toBeInTheDocument()
})
```

```bash
npm test
npx vitest run
npx vitest --ui
```

## Go

```go
// math_test.go
package main
import "testing"

func TestAdd(t *testing.T) {
    result := Add(2, 3)
    if result != 5 {
        t.Errorf("Expected 5, got %d", result)
    }
}
```

```bash
go test ./...
go test -v ./...
go test -cover ./...
```

## Rust

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(2, 3), 5);
    }
}
```

```bash
cargo test
cargo test -- --nocapture
cargo test specific_test_name
```

## REST API (curl / Supertest)

```bash
# Test endpoint
curl -X GET https://api.example.com/users
curl -H "Authorization: Bearer TOKEN" https://api.example.com/me
curl -X POST -H "Content-Type: application/json" -d '{"key":"val"}' https://api.example.com/data

# Postman collection
newman run collection.json
```

```javascript
// Supertest
const request = require('supertest')
const app = require('../app')

describe('API', () => {
  test('GET /users', async () => {
    const res = await request(app).get('/users')
    expect(res.status).toBe(200)
    expect(res.body).toHaveProperty('users')
  })
})
```

## E2E / Playwright

```bash
npx playwright test
npx playwright test --ui
npx playwright test login.spec.ts
npx playwright test --headed
npx playwright codegen
```

```javascript
const { test, expect } = require('@playwright/test')

test('login flow', async ({ page }) => {
  await page.goto('/login')
  await page.fill('[name="email"]', 'test@example.com')
  await page.fill('[name="password"]', 'password')
  await page.click('button[type="submit"]')
  await expect(page).toHaveURL('/dashboard')
})
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
