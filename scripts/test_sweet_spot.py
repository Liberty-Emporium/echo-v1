#!/usr/bin/env python3
"""
Sweet Spot Custom Cakes — Playwright Browser Test Suite
Tests all major modules with real Chromium.
Usage: python3 test_sweet_spot.py
"""

from playwright.sync_api import sync_playwright, expect
import sys, time, datetime

BASE_URL = "https://sweet-spot-cakes.up.railway.app"
EMAIL    = "info@sweetspotcustomcakes.com"
PASSWORD = "sweetspot2026"

results = []

def log(msg): print(f"  {msg}")

def record(name, passed, detail=""):
    icon = "✅ PASS" if passed else "❌ FAIL"
    print(f"  {icon} — {name}")
    if detail: print(f"         {detail}")
    results.append({"name": name, "passed": passed, "detail": detail})

def run():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx     = browser.new_context(viewport={"width": 1280, "height": 800})
        page    = ctx.new_page()
        page.set_default_timeout(15000)

        print(f"\n{'='*60}")
        print(f"  🍰 Sweet Spot Custom Cakes — Playwright Test Suite")
        print(f"  {BASE_URL}")
        print(f"  {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")

        # ── TEST 1: Health endpoint ──────────────────────────────────────
        print("📋 TEST 1: Health endpoint")
        try:
            r = page.goto(f"{BASE_URL}/health")
            body = page.content()
            passed = r.status == 200 and "ok" in body.lower()
            record("Health endpoint /health", passed, f"HTTP {r.status} — {body[:60].strip()}")
        except Exception as e:
            record("Health endpoint /health", False, str(e))

        # ── TEST 2: Public menu page ─────────────────────────────────────
        print("\n📋 TEST 2: Public menu page")
        try:
            page.goto(f"{BASE_URL}/order")
            title = page.title()
            has_heading = page.locator("h1, h2").count() > 0
            record("Public order/menu page loads", has_heading, f"Title: {title}")
        except Exception as e:
            record("Public order/menu page loads", False, str(e))

        # ── TEST 3: VIP loyalty join page ────────────────────────────────
        print("\n📋 TEST 3: VIP Loyalty /join page")
        try:
            page.goto(f"{BASE_URL}/join")
            has_form = page.locator("form").count() > 0
            record("VIP Loyalty /join page loads", has_form,
                   "Form found ✓" if has_form else "No form found")
        except Exception as e:
            record("VIP Loyalty /join page loads", False, str(e))

        # ── TEST 4: Login ────────────────────────────────────────────────
        print("\n📋 TEST 4: Admin login")
        try:
            page.goto(f"{BASE_URL}/login")
            page.fill('input[type="email"], input[name="email"]', EMAIL)
            page.fill('input[type="password"], input[name="password"]', PASSWORD)
            page.click('button[type="submit"], input[type="submit"]')
            page.wait_for_url(f"{BASE_URL}/dashboard", timeout=8000)
            record("Admin login → /dashboard", True, f"Redirected to {page.url}")
        except Exception as e:
            # Try current URL check
            if "/dashboard" in page.url:
                record("Admin login → /dashboard", True, f"At {page.url}")
            else:
                record("Admin login → /dashboard", False, f"{e} | URL: {page.url}")

        # ── TEST 5: Dashboard loads with stats ───────────────────────────
        print("\n📋 TEST 5: Dashboard stats")
        try:
            page.goto(f"{BASE_URL}/dashboard")
            page.wait_for_load_state("networkidle", timeout=8000)
            text = page.inner_text("body")
            has_orders   = any(w in text.lower() for w in ["order", "recent", "today"])
            has_nav      = page.locator("nav, .sidebar, .sidebar-content").count() > 0
            record("Dashboard content loads",   has_orders, "Orders/stats visible" if has_orders else "No order content found")
            record("Dashboard navigation visible", has_nav,  "Nav/sidebar found" if has_nav else "No nav found")
        except Exception as e:
            record("Dashboard content loads", False, str(e))

        # ── TEST 6: Orders page ──────────────────────────────────────────
        print("\n📋 TEST 6: Orders page")
        try:
            page.goto(f"{BASE_URL}/orders")
            page.wait_for_load_state("networkidle", timeout=8000)
            text = page.inner_text("body")
            has_content = any(w in text.lower() for w in ["order", "new order", "customer", "no orders"])
            record("Orders page loads", has_content, text[:80].strip())
        except Exception as e:
            record("Orders page loads", False, str(e))

        # ── TEST 7: Create new order ─────────────────────────────────────
        print("\n📋 TEST 7: New order form")
        try:
            page.goto(f"{BASE_URL}/orders/new")
            has_form = page.locator("form").count() > 0
            inputs   = page.locator("input, select, textarea").count()
            record("New order form renders", has_form and inputs >= 2,
                   f"{inputs} input fields found")
        except Exception as e:
            record("New order form renders", False, str(e))

        # ── TEST 8: Inventory page ───────────────────────────────────────
        print("\n📋 TEST 8: Inventory")
        try:
            page.goto(f"{BASE_URL}/inventory")
            page.wait_for_load_state("networkidle", timeout=8000)
            text = page.inner_text("body")
            has_content = any(w in text.lower() for w in ["ingredient", "stock", "unit", "inventory", "add"])
            record("Inventory page loads", has_content, text[:80].strip())
        except Exception as e:
            record("Inventory page loads", False, str(e))

        # ── TEST 9: Recipes page ─────────────────────────────────────────
        print("\n📋 TEST 9: Recipes")
        try:
            page.goto(f"{BASE_URL}/recipes")
            page.wait_for_load_state("networkidle", timeout=8000)
            text = page.inner_text("body")
            has_content = any(w in text.lower() for w in ["recipe", "cake", "cost", "margin", "add recipe", "no recipe"])
            record("Recipes page loads", has_content, text[:80].strip())
        except Exception as e:
            record("Recipes page loads", False, str(e))

        # ── TEST 10: Employees page ──────────────────────────────────────
        print("\n📋 TEST 10: Employees")
        try:
            page.goto(f"{BASE_URL}/employees")
            page.wait_for_load_state("networkidle", timeout=8000)
            text = page.inner_text("body")
            has_content = any(w in text.lower() for w in ["employee", "staff", "clock", "add", "no employee"])
            record("Employees page loads", has_content, text[:80].strip())
        except Exception as e:
            record("Employees page loads", False, str(e))

        # ── TEST 11: Customers page ──────────────────────────────────────
        print("\n📋 TEST 11: Customers")
        try:
            page.goto(f"{BASE_URL}/customers")
            page.wait_for_load_state("networkidle", timeout=8000)
            text = page.inner_text("body")
            has_content = any(w in text.lower() for w in ["customer", "email", "phone", "vip", "no customer"])
            record("Customers page loads", has_content, text[:80].strip())
        except Exception as e:
            record("Customers page loads", False, str(e))

        # ── TEST 12: Suppliers page ──────────────────────────────────────
        print("\n📋 TEST 12: Suppliers")
        try:
            page.goto(f"{BASE_URL}/suppliers")
            page.wait_for_load_state("networkidle", timeout=8000)
            text = page.inner_text("body")
            has_content = any(w in text.lower() for w in ["supplier", "vendor", "contact", "add", "no supplier"])
            record("Suppliers page loads", has_content, text[:80].strip())
        except Exception as e:
            record("Suppliers page loads", False, str(e))

        # ── TEST 13: Reports page ────────────────────────────────────────
        print("\n📋 TEST 13: Reports")
        try:
            page.goto(f"{BASE_URL}/reports")
            page.wait_for_load_state("networkidle", timeout=8000)
            text = page.inner_text("body")
            has_content = any(w in text.lower() for w in ["revenue", "report", "sales", "total", "$"])
            record("Reports page loads", has_content, text[:80].strip())
        except Exception as e:
            record("Reports page loads", False, str(e))

        # ── TEST 14: Settings page ───────────────────────────────────────
        print("\n📋 TEST 14: Settings")
        try:
            page.goto(f"{BASE_URL}/settings")
            page.wait_for_load_state("networkidle", timeout=8000)
            has_form = page.locator("form").count() > 0
            text = page.inner_text("body")
            has_content = any(w in text.lower() for w in ["setting", "stripe", "api", "email", "bakery"])
            record("Settings page loads", has_form or has_content, text[:80].strip())
        except Exception as e:
            record("Settings page loads", False, str(e))

        # ── TEST 15: Mobile viewport — no horizontal scroll ──────────────
        print("\n📋 TEST 15: Mobile viewport (375px — no horizontal scroll)")
        try:
            mobile_ctx  = browser.new_context(viewport={"width": 375, "height": 812})
            mobile_page = mobile_ctx.new_page()
            mobile_page.goto(f"{BASE_URL}/dashboard")
            mobile_page.wait_for_load_state("networkidle", timeout=8000)
            scroll_width = mobile_page.evaluate("document.documentElement.scrollWidth")
            client_width = mobile_page.evaluate("document.documentElement.clientWidth")
            no_overflow  = scroll_width <= client_width + 2   # 2px tolerance
            record("Mobile: no horizontal scroll on dashboard",
                   no_overflow,
                   f"scrollWidth={scroll_width}px, clientWidth={client_width}px {'✓' if no_overflow else '← OVERFLOW!'}")
            mobile_page.goto(f"{BASE_URL}/orders")
            mobile_page.wait_for_load_state("networkidle", timeout=6000)
            sw = mobile_page.evaluate("document.documentElement.scrollWidth")
            cw = mobile_page.evaluate("document.documentElement.clientWidth")
            record("Mobile: no horizontal scroll on orders",
                   sw <= cw + 2, f"scrollWidth={sw}px, clientWidth={cw}px {'✓' if sw <= cw+2 else '← OVERFLOW!'}")
            mobile_ctx.close()
        except Exception as e:
            record("Mobile: no horizontal scroll", False, str(e))

        # ── TEST 16: Public /order page on mobile ────────────────────────
        print("\n📋 TEST 16: Public order page — mobile")
        try:
            mobile_ctx2  = browser.new_context(viewport={"width": 375, "height": 812})
            mobile_page2 = mobile_ctx2.new_page()
            mobile_page2.goto(f"{BASE_URL}/order")
            mobile_page2.wait_for_load_state("networkidle", timeout=8000)
            sw = mobile_page2.evaluate("document.documentElement.scrollWidth")
            cw = mobile_page2.evaluate("document.documentElement.clientWidth")
            record("Mobile: public /order page no overflow",
                   sw <= cw + 2, f"scrollWidth={sw}px, clientWidth={cw}px")
            mobile_ctx2.close()
        except Exception as e:
            record("Mobile: public /order page no overflow", False, str(e))

        browser.close()

    # ── Summary ──────────────────────────────────────────────────────────────
    passed_list = [r for r in results if r["passed"]]
    failed_list = [r for r in results if not r["passed"]]
    total = len(results)

    print(f"\n{'='*60}")
    print(f"  🍰 SWEET SPOT TEST RESULTS — {len(passed_list)}/{total} PASSED")
    print(f"{'='*60}")
    for r in results:
        icon = "✅" if r["passed"] else "❌"
        print(f"  {icon}  {r['name']}")
    if failed_list:
        print(f"\n  ❌ FAILURES:")
        for r in failed_list:
            print(f"     • {r['name']}")
            if r["detail"]:
                print(f"       {r['detail'][:120]}")
    print(f"\n  Grade: {len(passed_list)}/{total} ({round(100*len(passed_list)/total)}%)")
    print(f"{'='*60}\n")

    return 0 if not failed_list else 1

if __name__ == "__main__":
    sys.exit(run())
