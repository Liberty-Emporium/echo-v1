---
name: web-test-coverage
description: Automatically write full, production-quality test coverage for any web feature or codebase. Use this skill whenever the user mentions testing, test coverage, writing tests, unit tests, integration tests, E2E tests, Playwright, Vitest, Jest, Cypress, test suites, or coverage reports. Also trigger when the user shares a component, function, module, or feature and wants it verified or tested. Trigger on keywords like "write tests", "add tests", "test this", "test coverage", "unit test", "integration test", "E2E", "Playwright", "Cypress", "Vitest", "Jest", "does this work", "verify this feature". Do not wait for explicit test keywords — if code is shared and reliability matters, offer to use this skill.
---

# Web Test Coverage Skill

Analyze code and write complete, production-quality test coverage: unit, integration, and E2E.

## Step 1 — Detect the Stack

Before writing any tests, identify:

- **Framework**: React, Vue, Svelte, vanilla JS, Next.js, Nuxt, Flask, Django, Express, etc.
- **Test runner**: Check for `vitest.config.*`, `jest.config.*`, `mocha.*` — or infer from `package.json` / `requirements.txt`
- **Component testing**: React Testing Library, Vue Test Utils, etc.
- **E2E tool**: Check for `playwright.config.*` or `cypress.config.*`
- **Language**: TypeScript or JavaScript or Python

If unclear, default to **Vitest + React Testing Library + Playwright** for JS/TS, **pytest** for Python, and state the assumption.

See `references/stack-detection.md` for detection patterns per framework.

## Step 2 — Analyze the Feature

Before writing a single test, build a checklist:
- All exported functions and their signatures
- All component props, state, and user interactions
- All API calls, async operations, side effects
- All conditional branches and error states
- Edge cases: empty input, null/undefined, boundary values, network failure

## Step 3 — Write Unit Tests

Target: every pure function, utility, hook, and isolated logic unit.

Rules:
- One `describe` block per file/module
- One `it`/`test` per behavior (not per function)
- Mock all external deps: `vi.mock()`, `jest.mock()`, `msw` for APIs
- Test: happy path + at least 2 edge cases + at least 1 error path per function
- Name in plain English: `it('returns null when input is empty')`
- No shared mutable state — use `beforeEach` for setup
- Clean up side effects in `afterEach` / `afterAll`

See `references/unit-test-patterns.md` for patterns by framework.

## Step 4 — Write Integration Tests

Target: how components/modules interact.

Rules:
- Use realistic internal dependencies (not mocked)
- Mock only external boundaries (APIs, DB, filesystem)
- Test data flow between parent/child components
- Test state changes triggered by user actions
- For APIs: test request/response contract with realistic payloads

## Step 5 — Write E2E Tests (if Playwright/Cypress available)

Write at least:
- 1 critical happy-path user journey
- 1 failure/error path

Rules:
- Assert on visible UI outcomes, not implementation details
- Use `data-testid` attributes or accessible roles — never CSS classes
- No hardcoded waits — use `waitFor`, `expect(locator).toBeVisible()`, etc.

See `references/e2e-patterns.md` for Playwright and Cypress patterns.

## Step 6 — Run Coverage and Report

After writing tests, run the coverage tool:

```bash
# Vitest
npx vitest run --coverage

# Jest
npx jest --coverage

# pytest
pytest --cov=app --cov-report=term-missing
```

Report results in this table format:

| File | Lines % | Branches % | Notes |
|------|---------|------------|-------|
| src/auth.ts | 94% | 88% | Error handler untested — requires DB mock |

**Targets:** 80%+ line coverage, 75%+ branch coverage.
List any gaps and explain why they were left uncovered.

## Quality Rules (Non-Negotiable)

- Tests must be **independent** — no shared mutable state between tests
- Every `expect` must have a clear, meaningful assertion — no `expect(true).toBe(true)`
- No snapshot tests unless explicitly requested
- No `.skip` or `.only` in final output
- Do NOT modify source code to make tests pass
- If a function is untestable as-is, **flag it** and explain why

## Output Format

For each test file output:
1. Full file path
2. Complete test file content
3. Short summary: what was tested + notable decisions

End with a coverage summary table.
