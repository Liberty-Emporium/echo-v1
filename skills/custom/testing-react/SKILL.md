---
name: testing-react
description: Write and run tests for React and Next.js applications using Vitest, Jest, and React Testing Library.
metadata:
  openclaw:
    emoji: ⚛️
    requires:
      bins: [npm, node]
---

# React/Next.js Testing Skill

## Usage

Write tests for React/Next.js apps:
- Component tests
- Hook tests
- Integration tests
- E2E tests with Playwright

## Commands

```bash
# Run tests
npm test

# Watch mode
npm test -- --watch

# Coverage
npm test -- --coverage

# Run specific file
npm test -- Header.test.jsx

# E2E with Playwright
npx playwright test
```

## Examples

```javascript
import { render, screen } from '@testing-library/react'
import { Button } from './Button'

test('renders button', () => {
  render(<Button>Click me</Button>)
  expect(screen.getByText('Click me')).toBeInTheDocument()
})
```
