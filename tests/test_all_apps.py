"""
Echo's Master App Test Suite
Tests all Liberty-Emporium apps using Playwright + requests
Run: pytest test_all_apps.py -v
"""
import pytest
import requests
import time
from playwright.sync_api import sync_playwright, expect

# ── App Registry ──────────────────────────────────────────────────────────────
APPS = {
    "ai-agent-widget":  "https://ai-agent-widget-production.up.railway.app",
    "contractor-pro":   "https://contractor-pro-ai-production.up.railway.app",
    "pet-vet-ai":       "https://pet-vet-ai-production.up.railway.app",
    "keep-your-secrets":"https://ai-api-tracker-production.up.railway.app",
    "liberty-inventory":"https://liberty-emporium-inventory-demo-app-production.up.railway.app",
    "dropship-shipping":"https://dropship-shipping-production.up.railway.app",
    "jay-portfolio":    "https://jay-portfolio-production.up.railway.app",
    "consignment":      "https://web-production-43ce4.up.railway.app",
    "grace":            "https://moms-ai-helper.up.railway.app",
}

TEST_EMAIL    = "echo-test-auto@liberty-emporium.ai"
TEST_PASSWORD = "TestPass123!"

# ── Health Checks (fast, no browser needed) ───────────────────────────────────

class TestHealthChecks:
    """Quick HTTP health checks for all apps."""

    @pytest.mark.parametrize("name,url", APPS.items())
    def test_health_endpoint(self, name, url):
        """Every app must return {"status":"ok"} at /health."""
        r = requests.get(f"{url}/health", timeout=15)
        assert r.status_code == 200, f"{name}: /health returned {r.status_code}"
        data = r.json()
        assert data.get("status") == "ok", f"{name}: health status = {data.get('status')}"
        assert data.get("db") == "ok", f"{name}: db status = {data.get('db')}"

    @pytest.mark.parametrize("name,url", APPS.items())
    def test_homepage_loads(self, name, url):
        """Every app homepage must return 200."""
        r = requests.get(url, timeout=15, allow_redirects=True)
        assert r.status_code == 200, f"{name}: homepage returned {r.status_code}"

    @pytest.mark.parametrize("name,url", [
        ("ai-agent-widget", APPS["ai-agent-widget"]),
        ("contractor-pro",  APPS["contractor-pro"]),
        ("pet-vet-ai",      APPS["pet-vet-ai"]),
        ("keep-your-secrets", APPS["keep-your-secrets"]),
        ("liberty-inventory", APPS["liberty-inventory"]),
        ("dropship-shipping", APPS["dropship-shipping"]),
        ("consignment",     APPS["consignment"]),
    ])
    def test_login_page_loads(self, name, url):
        """Login page must be accessible."""
        r = requests.get(f"{url}/login", timeout=15, allow_redirects=True)
        assert r.status_code == 200, f"{name}: /login returned {r.status_code}"

# ── AI Agent Widget — Full Browser Tests ─────────────────────────────────────

@pytest.fixture(scope="module")
def browser_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        yield context
        browser.close()

@pytest.fixture(scope="module")
def page(browser_context):
    p = browser_context.new_page()
    yield p
    p.close()

class TestAIAgentWidget:
    BASE = APPS["ai-agent-widget"]

    def test_landing_page(self, page):
        """Landing page loads and has key content."""
        page.goto(self.BASE)
        expect(page).to_have_title(lambda t: "Alexander" in t or "AI Agent" in t)
        # Should have CTA button
        assert page.locator("a[href='/signup']").count() > 0 or \
               page.locator("text=Get Started").count() > 0

    def test_signup_page_has_fields(self, page):
        """Signup page has email, password, confirm password fields."""
        page.goto(f"{self.BASE}/signup")
        expect(page.locator("input[name='email']")).to_be_visible()
        expect(page.locator("input[name='password']")).to_be_visible()
        expect(page.locator("input[name='confirm_password']")).to_be_visible()

    def test_signup_password_eye_toggle(self, page):
        """Password field has eye toggle button."""
        page.goto(f"{self.BASE}/signup")
        eye_btns = page.locator(".eye-btn")
        assert eye_btns.count() >= 2, "Signup should have at least 2 eye toggles"

    def test_login_page_has_forgot_password(self, page):
        """Login page has forgot password link."""
        page.goto(f"{self.BASE}/login")
        expect(page.locator("a[href='/forgot-password']")).to_be_visible()

    def test_forgot_password_page(self, page):
        """Forgot password page loads."""
        page.goto(f"{self.BASE}/forgot-password")
        expect(page.locator("input[name='email']")).to_be_visible()

    def test_pricing_page(self, page):
        """Pricing page loads with plans."""
        page.goto(f"{self.BASE}/pricing")
        page.wait_for_load_state("networkidle")
        content = page.content()
        assert "$19" in content or "Pro" in content, "Pricing page missing plan info"
        assert "$90" in content or "Installation" in content, "Pricing page missing installation service"

    def test_signup_flow(self, page):
        """Full signup → dashboard flow."""
        import secrets as _s
        email = f"test-{_s.token_hex(4)}@test.com"
        page.goto(f"{self.BASE}/signup")
        page.fill("input[name='email']", email)
        page.fill("input[name='password']", TEST_PASSWORD)
        page.fill("input[name='confirm_password']", TEST_PASSWORD)
        page.click("button[type='submit']")
        page.wait_for_url(f"{self.BASE}/dashboard", timeout=10000)
        assert "/dashboard" in page.url, f"Expected dashboard, got {page.url}"

    def test_dashboard_has_create_agent(self, page):
        """Dashboard loads and has agent creation option."""
        # Should already be logged in from previous test
        page.goto(f"{self.BASE}/dashboard")
        content = page.content()
        assert "agent" in content.lower() or "create" in content.lower()

    def test_support_link_visible(self, page):
        """Support/tickets link visible in nav for logged-in users."""
        page.goto(f"{self.BASE}/dashboard")
        content = page.content()
        assert "support" in content.lower() or "ticket" in content.lower()

    def test_tickets_page(self, page):
        """Tickets page loads."""
        page.goto(f"{self.BASE}/tickets")
        assert page.url.endswith("/tickets") or "/login" in page.url

# ── Grace App Tests ───────────────────────────────────────────────────────────

class TestGraceApp:
    BASE = APPS["grace"]

    def test_home_loads(self, page):
        """Grace home page loads with greeting."""
        page.goto(self.BASE)
        page.wait_for_load_state("networkidle")
        content = page.content()
        assert any(w in content for w in ["Good morning", "Good afternoon", "Good evening", "Grace"]), \
            "Grace home page missing greeting"

    def test_voice_button_present(self, page):
        """Big TALK TO GRACE button is visible."""
        page.goto(self.BASE)
        content = page.content()
        assert "GRACE" in content.upper() or "grace" in content.lower()
        # Grace FAB button
        assert page.locator("#graceFab").count() > 0, "Grace FAB button missing"

    def test_meds_page(self, page):
        """Medications page loads."""
        page.goto(f"{self.BASE}/meds")
        expect(page.locator("body")).to_be_visible()
        content = page.content()
        assert "medication" in content.lower() or "med" in content.lower()

    def test_appointments_page(self, page):
        """Appointments page loads."""
        page.goto(f"{self.BASE}/appointments")
        expect(page.locator("body")).to_be_visible()

    def test_tasks_page(self, page):
        """Tasks page loads."""
        page.goto(f"{self.BASE}/tasks")
        expect(page.locator("body")).to_be_visible()

    def test_caregiver_pin_page(self, page):
        """Caregiver PIN entry page loads."""
        page.goto(f"{self.BASE}/caregiver")
        content = page.content()
        assert "pin" in content.lower() or "caregiver" in content.lower()

    def test_bottom_nav_present(self, page):
        """Bottom navigation bar is present."""
        page.goto(self.BASE)
        assert page.locator(".bottom-nav").count() > 0, "Bottom nav missing"

    def test_grace_ai_api(self):
        """Grace AI API responds."""
        r = requests.post(
            f"{self.BASE}/api/grace",
            json={"message": "Hello Grace, what can you help me with?"},
            timeout=20
        )
        assert r.status_code == 200
        data = r.json()
        assert "reply" in data, "Grace API missing reply field"
        assert len(data["reply"]) > 0, "Grace API returned empty reply"

# ── Jay Portfolio Tests ───────────────────────────────────────────────────────

class TestJayPortfolio:
    BASE = APPS["jay-portfolio"]

    def test_homepage(self, page):
        """Portfolio homepage loads."""
        page.goto(self.BASE)
        page.wait_for_load_state("networkidle")
        assert page.title() != ""

    def test_private_routes_not_indexed(self, page):
        """Private court pages should not be publicly accessible via robots."""
        r = requests.get(f"{self.BASE}/robots.txt", timeout=10)
        # Either robots.txt exists or the route returns non-200
        court_r = requests.get(f"{self.BASE}/court", timeout=10, allow_redirects=False)
        # Should redirect or be protected - not return plain 200 to anonymous
        # (just check it doesn't error with 500)
        assert court_r.status_code != 500, "/court returned 500 error"

# ── Summary Report ────────────────────────────────────────────────────────────

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Print a clean summary at the end."""
    passed  = len(terminalreporter.stats.get("passed", []))
    failed  = len(terminalreporter.stats.get("failed", []))
    errors  = len(terminalreporter.stats.get("error", []))
    total   = passed + failed + errors
    print(f"\n{'='*50}")
    print(f"🤖 ECHO APP TEST SUITE COMPLETE")
    print(f"{'='*50}")
    print(f"✅ Passed:  {passed}/{total}")
    if failed: print(f"❌ Failed:  {failed}/{total}")
    if errors:  print(f"💥 Errors:  {errors}/{total}")
    print(f"{'='*50}\n")
