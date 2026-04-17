# Unit Test Patterns by Framework

## Vitest + React Testing Library

```typescript
// src/__tests__/AuthForm.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { vi, describe, it, expect, beforeEach, afterEach } from 'vitest'
import { AuthForm } from '../components/AuthForm'
import * as authApi from '../api/auth'

vi.mock('../api/auth')

describe('AuthForm', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders email and password fields', () => {
    render(<AuthForm />)
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument()
  })

  it('submits credentials and calls login API', async () => {
    vi.mocked(authApi.login).mockResolvedValue({ token: 'abc123' })
    render(<AuthForm />)
    fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'jay@test.com' } })
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'secret' } })
    fireEvent.click(screen.getByRole('button', { name: /login/i }))
    await waitFor(() => expect(authApi.login).toHaveBeenCalledWith('jay@test.com', 'secret'))
  })

  it('shows error message on failed login', async () => {
    vi.mocked(authApi.login).mockRejectedValue(new Error('Invalid credentials'))
    render(<AuthForm />)
    fireEvent.click(screen.getByRole('button', { name: /login/i }))
    await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent(/invalid credentials/i))
  })

  it('disables submit button while loading', async () => {
    vi.mocked(authApi.login).mockImplementation(() => new Promise(() => {})) // never resolves
    render(<AuthForm />)
    fireEvent.click(screen.getByRole('button', { name: /login/i }))
    expect(screen.getByRole('button', { name: /login/i })).toBeDisabled()
  })
})
```

## Jest + Vue Test Utils

```javascript
// tests/unit/CartItem.spec.js
import { mount } from '@vue/test-utils'
import CartItem from '@/components/CartItem.vue'

describe('CartItem', () => {
  it('displays product name and price', () => {
    const wrapper = mount(CartItem, {
      props: { name: 'Widget', price: 9.99, quantity: 1 }
    })
    expect(wrapper.text()).toContain('Widget')
    expect(wrapper.text()).toContain('9.99')
  })

  it('emits remove event when remove button clicked', async () => {
    const wrapper = mount(CartItem, { props: { name: 'Widget', price: 9.99, quantity: 1 } })
    await wrapper.find('[data-testid="remove-btn"]').trigger('click')
    expect(wrapper.emitted('remove')).toHaveLength(1)
  })
})
```

## pytest (Flask)

```python
# tests/test_auth.py
import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def client():
    app = create_app({'TESTING': True, 'DATABASE_URL': 'sqlite:///:memory:'})
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_login_success(client):
    client.post('/register', json={'email': 'jay@test.com', 'password': 'secret'})
    res = client.post('/login', json={'email': 'jay@test.com', 'password': 'secret'})
    assert res.status_code == 200
    assert 'token' in res.get_json()

def test_login_wrong_password(client):
    client.post('/register', json={'email': 'jay@test.com', 'password': 'secret'})
    res = client.post('/login', json={'email': 'jay@test.com', 'password': 'wrong'})
    assert res.status_code == 401
    assert res.get_json()['error'] == 'Invalid credentials'

def test_login_missing_fields(client):
    res = client.post('/login', json={})
    assert res.status_code == 400
```

## Utility Function Pattern (any framework)

```typescript
// src/__tests__/utils/formatPrice.test.ts
import { formatPrice } from '../../utils/formatPrice'

describe('formatPrice', () => {
  it('formats a whole number with dollar sign', () => {
    expect(formatPrice(10)).toBe('$10.00')
  })

  it('formats a decimal price correctly', () => {
    expect(formatPrice(9.99)).toBe('$9.99')
  })

  it('returns $0.00 for zero', () => {
    expect(formatPrice(0)).toBe('$0.00')
  })

  it('throws for negative input', () => {
    expect(() => formatPrice(-1)).toThrow('Price cannot be negative')
  })

  it('returns $0.00 for null/undefined input', () => {
    expect(formatPrice(null)).toBe('$0.00')
    expect(formatPrice(undefined)).toBe('$0.00')
  })
})
```
