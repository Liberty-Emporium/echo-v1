# Stack Detection Patterns

## JavaScript / TypeScript

| Signal | Inferred Stack |
|--------|---------------|
| `vitest.config.*` present | Vitest |
| `jest.config.*` present | Jest |
| `react` in package.json | React + React Testing Library |
| `vue` in package.json | Vue + Vue Test Utils |
| `next` in package.json | Next.js (use Jest or Vitest) |
| `playwright.config.*` | Playwright for E2E |
| `cypress.config.*` | Cypress for E2E |
| `.ts` / `.tsx` files | TypeScript — use typed mocks |

### Default JS/TS fallback
Vitest + React Testing Library + Playwright. State assumption explicitly.

## Python

| Signal | Inferred Stack |
|--------|---------------|
| `pytest` in requirements | pytest |
| `flask` in requirements | Flask test client via pytest |
| `django` in requirements | Django TestCase or pytest-django |
| `fastapi` in requirements | TestClient from starlette |

### Default Python fallback
pytest + requests for API testing. State assumption explicitly.

## Detection Commands

```bash
# Check package.json for test runner
cat package.json | python3 -m json.tool | grep -E "jest|vitest|mocha|cypress|playwright"

# Check for config files
ls vitest.config.* jest.config.* playwright.config.* cypress.config.* 2>/dev/null

# Python
cat requirements.txt | grep -E "pytest|coverage|unittest"
```
