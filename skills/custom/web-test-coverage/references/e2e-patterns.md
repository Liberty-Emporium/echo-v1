# E2E Test Patterns

## Playwright

```typescript
// e2e/auth.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Authentication flow', () => {
  test('user can log in with valid credentials', async ({ page }) => {
    await page.goto('/login')
    await page.getByLabel('Email').fill('jay@test.com')
    await page.getByLabel('Password').fill('secret')
    await page.getByRole('button', { name: /sign in/i }).click()
    await expect(page).toHaveURL('/dashboard')
    await expect(page.getByRole('heading', { name: /dashboard/i })).toBeVisible()
  })

  test('shows error on invalid credentials', async ({ page }) => {
    await page.goto('/login')
    await page.getByLabel('Email').fill('jay@test.com')
    await page.getByLabel('Password').fill('wrongpassword')
    await page.getByRole('button', { name: /sign in/i }).click()
    await expect(page.getByRole('alert')).toContainText(/invalid credentials/i)
    await expect(page).toHaveURL('/login') // did not redirect
  })
})
```

### Playwright Config (minimal)
```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
  },
})
```

## Cypress

```javascript
// cypress/e2e/auth.cy.js
describe('Authentication flow', () => {
  it('logs in with valid credentials', () => {
    cy.visit('/login')
    cy.findByLabelText(/email/i).type('jay@test.com')
    cy.findByLabelText(/password/i).type('secret')
    cy.findByRole('button', { name: /sign in/i }).click()
    cy.url().should('include', '/dashboard')
    cy.findByRole('heading', { name: /dashboard/i }).should('be.visible')
  })

  it('shows error on bad credentials', () => {
    cy.visit('/login')
    cy.findByLabelText(/email/i).type('jay@test.com')
    cy.findByLabelText(/password/i).type('wrong')
    cy.findByRole('button', { name: /sign in/i }).click()
    cy.findByRole('alert').should('contain.text', 'Invalid credentials')
  })
})
```

## E2E Rules
- Always use accessible selectors: `getByRole`, `getByLabel`, `getByText`, `data-testid`
- Never use CSS classes or nth-child selectors — they break on refactor
- No `page.waitForTimeout(3000)` — use `waitFor` or assertion-based waiting
- Always assert on URL + visible UI element after navigation
- Run against a real (staging or local) server — never mock in E2E
