---
name: testing-e2e
description: Write and run end-to-end tests using Playwright. Test full user flows in real browsers.
metadata:
  openclaw:
    emoji: 🎭
    requires:
      bins: [npx, node]
---

# E2E/Playwright Testing Skill

## Usage

Write browser tests:
- User flows
- Visual regression
- Performance
- Accessibility

## Commands

```bash
# Run tests
npx playwright test

# UI mode
npx playwright test --ui

# Specific file
npx playwright test login.spec.ts

# With headed browser
npx playwright test --headed

# Generate tests
npx playwright codegen
```

## Examples

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
