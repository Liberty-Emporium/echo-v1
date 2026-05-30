# SKILL: Testing Strategies

> Comprehensive testing for web apps — unit, integration, E2E.

## Testing Pyramid
```
        /  E2E  \          ← Few tests (slow, expensive)
       / Integration \     ← Some tests (APIs, DB)
      /   Unit Tests  \    ← Many tests (fast, isolated)
```

## Frontend Testing (React/Next.js)

### Vitest + React Testing Library
```tsx
// src/components/__tests__/button.test.tsx
import { render, screen, fireEvent } from "@testing-library/react"
import { Button } from "@/components/ui/button"

describe("Button", () => {
  it("renders children", () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText("Click me")).toBeInTheDocument()
  })

  it("calls onClick", () => {
    const handleClick = vi.fn()
    render(<Button onClick={handleClick}>Click</Button>)
    fireEvent.click(screen.getByText("Click"))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it("is disabled when loading", () => {
    render(<Button loading>Click</Button>)
    expect(screen.getByRole("button")).toBeDisabled()
  })

  it("shows spinner when loading", () => {
    render(<Button loading>Click</Button>)
    expect(screen.getByRole("progressbar")).toBeInTheDocument()
  })
})

// src/app/__tests__/page.test.tsx
import { render, screen } from "@testing-library/react"
import Dashboard from "@/app/dashboard/page"

jest.mock("@/lib/auth", () => ({
  auth: jest.fn().mockResolvedValue({ user: { id: "1", name: "Jay" } }),
}))

describe("Dashboard", () => {
  it("renders welcome message", async () => {
    render(await Dashboard())
    expect(screen.getByText(/welcome/i)).toBeInTheDocument()
  })
})
```

### Playwright E2E
```ts
// e2e/auth.spec.ts
import { test, expect } from "@playwright/test"

test.describe("Authentication", () => {
  test("user can sign in", async ({ page }) => {
    await page.goto("/login")
    await page.fill('[name="email"]', "jay@test.com")
    await page.fill('[name="password"]', "password123")
    await page.click('button[type="submit"]')
    
    // Should redirect to dashboard
    await expect(page).toHaveURL("/dashboard")
    await expect(page.getByText("Welcome back")).toBeVisible()
  })

  test("shows error for wrong password", async ({ page }) => {
    await page.goto("/login")
    await page.fill('[name="email"]', "jay@test.com")
    await page.fill('[name="password"]', "wrong")
    await page.click('button[type="submit"]')
    
    await expect(page.getByText(/invalid credentials/i)).toBeVisible()
  })

  test("redirects to login when not authenticated", async ({ page }) => {
    await page.goto("/dashboard")
    await expect(page).toHaveURL("/login")
  })
})

// e2e/projects.spec.ts
test("user can create a project", async ({ page }) => {
  await login(page) // helper
  await page.goto("/dashboard")
  await page.click('button:has-text("New Project")')
  await page.fill('[name="name"]', "My Test Project")
  await page.click('button:has-text("Create")')
  await expect(page.getByText("My Test Project")).toBeVisible()
})
```

### Playwright Config
```ts
// playwright.config.ts
import { defineConfig } from "@playwright/test"

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  reporter: "html",
  use: {
    baseURL: process.env.BASE_URL || "http://localhost:3000",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },
  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
    { name: "firefox", use: { ...devices["Desktop Firefox"] } },
    { name: "mobile", use: { ...devices["iPhone 14"] } },
  ],
  webServer: {
    command: "npm run dev",
    port: 3000,
    reuseExistingServer: !process.env.CI,
  },
})
```

## Backend Testing (FastAPI/Python)

### Pytest + Async
```python
# tests/conftest.py
import pytest_asyncio
from httpx import AsyncClient
from app.main import app
from app.database import engine, Base

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# tests/test_projects.py
import pytest

@pytest.mark.asyncio
async def test_create_project(client: AsyncClient):
    # Register and login
    await client.post("/api/auth/register", json={
        "email": "test@test.com", "password": "Pass123!", "name": "Test"
    })
    login = await client.post("/api/auth/login", json={
        "email": "test@test.com", "password": "Pass123!"
    })
    token = login.json()["access_token"]
    
    # Create project
    response = await client.post(
        "/api/v1/projects/",
        json={"name": "Test Project", "description": "A test"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Project"
    assert "id" in data

@pytest.mark.asyncio
async def test_list_projects(client: AsyncClient):
    # ... create project first
    response = await client.get(
        "/api/v1/projects/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["meta"]["total"] >= 1

@pytest.mark.asyncio
async def test_project_not_found(client: AsyncClient):
    response = await client.get(
        "/api/v1/projects/nonexistent-id",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404

# Test error handling
@pytest.mark.asyncio
async def test_create_project_validation(client: AsyncClient):
    response = await client.post(
        "/api/v1/projects/",
        json={"name": ""},  # Invalid: empty name
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 422
```

### Test Configuration
```ini
# pytest.ini
[pytest]
asyncio_mode = auto
testpaths = tests
python_files = test_*.py
```

```txt
# requirements-test.txt
pytest==8.2.*
pytest-asyncio==0.23.*
httpx==0.27.*
pytest-cov==5.0.*
factory-boy==3.3.*
faker==25.*
```

## Coverage
```bash
# Run with coverage
pytest --cov=app --cov-report=html --cov-report=term-missing

# Minimum coverage thresholds (set in pyproject.toml)
# fail_under = 80
```

## CI/CD Testing Pipeline
```yaml
# .github/workflows/test.yml
name: Test
on: [push, pull_request]
jobs:
  unit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: npm ci
      - run: npm run test -- --coverage
      
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npx playwright test
```
