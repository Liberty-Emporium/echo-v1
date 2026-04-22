#!/usr/bin/env python3
"""
Sweet Spot Custom Cakes — Visual Playwright Test Suite
Captures screenshots at every step + video recording + HTML report.

Usage:
    python3 test_sweet_spot_visual.py           # runs tests, saves all artifacts
    python3 test_sweet_spot_visual.py --headed  # watch live in browser window (needs display)

After running:
    open test-report/index.html                 # Mac
    xdg-open test-report/index.html             # Linux/Kali
    start test-report\\index.html               # Windows

Screenshots saved to: ./screenshots/
Videos saved to:      ./videos/
HTML report at:       ./test-report/index.html
"""

import sys, os, time, datetime, json, argparse, shutil, base64
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_URL = "https://sweet-spot-cakes.up.railway.app"
EMAIL    = "info@sweetspotcustomcakes.com"
PASSWORD = "sweetspot2026"

# ── Output dirs ───────────────────────────────────────────────────────────────
OUT_DIR         = Path("test-results-sweetspot")
SCREENSHOT_DIR  = OUT_DIR / "screenshots"
VIDEO_DIR       = OUT_DIR / "videos"
REPORT_DIR      = OUT_DIR / "report"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

results  = []
shot_idx = [0]

def snap(page, name):
    """Take a screenshot and save it."""
    shot_idx[0] += 1
    fname = SCREENSHOT_DIR / f"{shot_idx[0]:02d}_{name.replace(' ', '_')}.png"
    try:
        page.screenshot(path=str(fname), full_page=False)
        print(f"     📸 Screenshot: {fname.name}")
        return str(fname)
    except Exception as e:
        print(f"     ⚠️  Screenshot failed: {e}")
        return None

def record(name, passed, detail="", screenshot=None):
    icon = "✅ PASS" if passed else "❌ FAIL"
    print(f"  {icon} — {name}")
    if detail: print(f"         {detail}")
    results.append({
        "name": name, "passed": passed,
        "detail": detail, "screenshot": screenshot
    })

def run(headed=False):
    print(f"\n{'='*60}")
    print(f"  🍰 Sweet Spot — Visual Playwright Test Suite")
    print(f"  {BASE_URL}")
    print(f"  {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Mode: {'👁️  HEADED (watch live)' if headed else '🤖 Headless + recording'}")
    print(f"{'='*60}\n")

    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            headless=not headed,
            slow_mo=300 if headed else 0,   # slow down in headed mode so you can see it
        )

        # Context with video recording
        ctx = browser.new_context(
            viewport={"width": 1280, "height": 800},
            record_video_dir=str(VIDEO_DIR),
            record_video_size={"width": 1280, "height": 800},
        )
        page = ctx.new_page()
        page.set_default_timeout(15000)

        # ── TEST 1: Health ─────────────────────────────────────────────────
        print("📋 TEST 1: Health endpoint")
        try:
            r = page.goto(f"{BASE_URL}/health")
            body = page.content()
            ok = r.status == 200 and "ok" in body.lower()
            shot = snap(page, "01_health")
            record("Health endpoint /health", ok, f"HTTP {r.status}", shot)
        except Exception as e:
            record("Health endpoint /health", False, str(e))

        # ── TEST 2: Public menu ────────────────────────────────────────────
        print("\n📋 TEST 2: Public order/menu page")
        try:
            page.goto(f"{BASE_URL}/order")
            page.wait_for_load_state("networkidle", timeout=8000)
            shot = snap(page, "02_public_menu")
            title = page.title()
            has_content = page.locator("h1, h2, form").count() > 0
            record("Public menu page loads", has_content, f"Title: {title}", shot)
        except Exception as e:
            record("Public menu page loads", False, str(e))

        # ── TEST 3: VIP Join ───────────────────────────────────────────────
        print("\n📋 TEST 3: VIP Loyalty /join")
        try:
            page.goto(f"{BASE_URL}/join")
            page.wait_for_load_state("networkidle", timeout=6000)
            shot = snap(page, "03_vip_join")
            has_form = page.locator("form").count() > 0
            record("VIP /join page", has_form, "Form found ✓" if has_form else "No form", shot)
        except Exception as e:
            record("VIP /join page", False, str(e))

        # ── TEST 4: Login ──────────────────────────────────────────────────
        print("\n📋 TEST 4: Admin login")
        try:
            page.goto(f"{BASE_URL}/login")
            page.wait_for_load_state("networkidle", timeout=6000)
            snap(page, "04a_login_form")
            page.fill('input[type="email"], input[name="email"]', EMAIL)
            page.fill('input[type="password"], input[name="password"]', PASSWORD)
            snap(page, "04b_login_filled")
            page.click('button[type="submit"], input[type="submit"]')
            page.wait_for_url(f"{BASE_URL}/dashboard", timeout=8000)
            shot = snap(page, "04c_dashboard_after_login")
            record("Admin login → /dashboard", "/dashboard" in page.url,
                   f"Redirected to: {page.url}", shot)
        except Exception as e:
            shot = snap(page, "04_login_error")
            record("Admin login → /dashboard", False, str(e), shot)

        # ── TEST 5: Dashboard ──────────────────────────────────────────────
        print("\n📋 TEST 5: Dashboard")
        try:
            page.goto(f"{BASE_URL}/dashboard")
            page.wait_for_load_state("networkidle", timeout=8000)
            shot = snap(page, "05_dashboard")
            text = page.inner_text("body")
            has_nav     = page.locator("nav, .sidebar, .sidebar-content").count() > 0
            has_content = any(w in text.lower() for w in ["order", "today", "revenue", "dashboard"])
            record("Dashboard loads with content", has_content, "", shot)
            record("Dashboard navigation visible", has_nav, "Sidebar/nav found" if has_nav else "No nav", shot)
        except Exception as e:
            record("Dashboard loads", False, str(e))

        # ── TEST 6: Orders ─────────────────────────────────────────────────
        print("\n📋 TEST 6: Orders page")
        try:
            page.goto(f"{BASE_URL}/orders")
            page.wait_for_load_state("networkidle", timeout=8000)
            shot = snap(page, "06_orders")
            text = page.inner_text("body")
            ok = any(w in text.lower() for w in ["order", "new order", "no orders", "customer"])
            record("Orders page", ok, text[:60].strip(), shot)
        except Exception as e:
            record("Orders page", False, str(e))

        # ── TEST 7: New order form ─────────────────────────────────────────
        print("\n📋 TEST 7: New order form")
        try:
            page.goto(f"{BASE_URL}/orders/new")
            page.wait_for_load_state("networkidle", timeout=6000)
            shot = snap(page, "07_new_order_form")
            inputs = page.locator("input, select, textarea").count()
            record("New order form (≥3 fields)", inputs >= 3, f"{inputs} input fields found", shot)
        except Exception as e:
            record("New order form", False, str(e))

        # ── TEST 8: Inventory ──────────────────────────────────────────────
        print("\n📋 TEST 8: Inventory")
        try:
            page.goto(f"{BASE_URL}/inventory")
            page.wait_for_load_state("networkidle", timeout=8000)
            shot = snap(page, "08_inventory")
            text = page.inner_text("body")
            ok = any(w in text.lower() for w in ["ingredient", "stock", "unit", "inventory", "add"])
            record("Inventory page", ok, text[:60].strip(), shot)
        except Exception as e:
            record("Inventory page", False, str(e))

        # ── TEST 9: Recipes ────────────────────────────────────────────────
        print("\n📋 TEST 9: Recipes")
        try:
            page.goto(f"{BASE_URL}/recipes")
            page.wait_for_load_state("networkidle", timeout=8000)
            shot = snap(page, "09_recipes")
            text = page.inner_text("body")
            ok = any(w in text.lower() for w in ["recipe", "cake", "cost", "margin", "add recipe", "no recipe"])
            record("Recipes page", ok, text[:60].strip(), shot)
        except Exception as e:
            record("Recipes page", False, str(e))

        # ── TEST 10: Employees ─────────────────────────────────────────────
        print("\n📋 TEST 10: Employees")
        try:
            page.goto(f"{BASE_URL}/employees")
            page.wait_for_load_state("networkidle", timeout=8000)
            shot = snap(page, "10_employees")
            text = page.inner_text("body")
            ok = any(w in text.lower() for w in ["employee", "staff", "clock", "add", "no employee"])
            record("Employees page", ok, text[:60].strip(), shot)
        except Exception as e:
            record("Employees page", False, str(e))

        # ── TEST 11: Customers ─────────────────────────────────────────────
        print("\n📋 TEST 11: Customers")
        try:
            page.goto(f"{BASE_URL}/customers")
            page.wait_for_load_state("networkidle", timeout=8000)
            shot = snap(page, "11_customers")
            text = page.inner_text("body")
            ok = any(w in text.lower() for w in ["customer", "email", "phone", "vip", "no customer"])
            record("Customers page", ok, text[:60].strip(), shot)
        except Exception as e:
            record("Customers page", False, str(e))

        # ── TEST 12: Reports ───────────────────────────────────────────────
        print("\n📋 TEST 12: Reports")
        try:
            page.goto(f"{BASE_URL}/reports")
            page.wait_for_load_state("networkidle", timeout=8000)
            shot = snap(page, "12_reports")
            text = page.inner_text("body")
            ok = any(w in text.lower() for w in ["revenue", "report", "sales", "total", "$"])
            record("Reports page", ok, text[:60].strip(), shot)
        except Exception as e:
            record("Reports page", False, str(e))

        # ── TEST 13: Mobile no horizontal scroll ──────────────────────────
        print("\n📋 TEST 13: Mobile viewport (375px iPhone)")
        try:
            mob_ctx  = browser.new_context(
                viewport={"width": 375, "height": 812},
                record_video_dir=str(VIDEO_DIR / "mobile"),
                record_video_size={"width": 375, "height": 812},
            )
            Path(str(VIDEO_DIR / "mobile")).mkdir(exist_ok=True)
            mob = mob_ctx.new_page()
            mob.set_default_timeout(12000)
            mob.goto(f"{BASE_URL}/dashboard")
            mob.wait_for_load_state("networkidle", timeout=8000)
            shot = snap(mob, "13a_mobile_dashboard")
            sw = mob.evaluate("document.documentElement.scrollWidth")
            cw = mob.evaluate("document.documentElement.clientWidth")
            record("Mobile dashboard: no horizontal scroll",
                   sw <= cw + 2, f"scrollWidth={sw}px  clientWidth={cw}px {'✓' if sw<=cw+2 else '← OVERFLOW!'}", shot)

            mob.goto(f"{BASE_URL}/order")
            mob.wait_for_load_state("networkidle", timeout=8000)
            shot2 = snap(mob, "13b_mobile_order")
            sw2 = mob.evaluate("document.documentElement.scrollWidth")
            cw2 = mob.evaluate("document.documentElement.clientWidth")
            record("Mobile /order page: no horizontal scroll",
                   sw2 <= cw2 + 2, f"scrollWidth={sw2}px  clientWidth={cw2}px", shot2)
            mob_ctx.close()
        except Exception as e:
            record("Mobile overflow check", False, str(e))

        # Close main context — this finalizes the video file
        ctx.close()
        browser.close()

    # ── Find video file ───────────────────────────────────────────────────────
    video_files = list(VIDEO_DIR.glob("*.webm"))
    video_path  = str(video_files[0]) if video_files else None

    # ── Generate HTML report ──────────────────────────────────────────────────
    generate_report(video_path)

    # ── Print summary ─────────────────────────────────────────────────────────
    passed_list = [r for r in results if r["passed"]]
    failed_list = [r for r in results if not r["passed"]]
    total = len(results)

    print(f"\n{'='*60}")
    print(f"  🍰 RESULTS — {len(passed_list)}/{total} PASSED  ({round(100*len(passed_list)/total)}%)")
    print(f"{'='*60}")
    for r in results:
        print(f"  {'✅' if r['passed'] else '❌'}  {r['name']}")
    if failed_list:
        print(f"\n  ❌ Failures:")
        for r in failed_list:
            print(f"     • {r['name']}: {r['detail'][:80]}")

    print(f"\n{'='*60}")
    print(f"  📁 Artifacts saved to: {OUT_DIR.absolute()}/")
    print(f"  📸 Screenshots:  {SCREENSHOT_DIR}/")
    if video_path:
        print(f"  🎬 Video:        {video_path}")
    print(f"  📊 HTML Report:  {REPORT_DIR}/index.html")
    print(f"\n  To open report:")
    print(f"    xdg-open {REPORT_DIR}/index.html   (Linux/Kali)")
    print(f"    open {REPORT_DIR}/index.html        (Mac)")
    print(f"    start {REPORT_DIR}\\index.html      (Windows)")
    print(f"{'='*60}\n")

    return 0 if not failed_list else 1


def generate_report(video_path=None):
    """Build a self-contained HTML report with embedded screenshots."""
    passed = [r for r in results if r["passed"]]
    failed = [r for r in results if not r["passed"]]
    now    = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pct    = round(100 * len(passed) / len(results)) if results else 0
    grade_color = "#10b981" if pct == 100 else "#f59e0b" if pct >= 70 else "#ef4444"

    # Build test rows with embedded screenshots
    rows = ""
    for r in results:
        status_badge = (
            '<span style="background:rgba(16,185,129,.15);color:#10b981;padding:3px 10px;'
            'border-radius:999px;font-size:.75rem;font-weight:700;">✅ PASS</span>'
            if r["passed"] else
            '<span style="background:rgba(239,68,68,.15);color:#ef4444;padding:3px 10px;'
            'border-radius:999px;font-size:.75rem;font-weight:700;">❌ FAIL</span>'
        )
        # Embed screenshot as base64
        img_tag = ""
        if r.get("screenshot") and Path(r["screenshot"]).exists():
            try:
                with open(r["screenshot"], "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                img_tag = (
                    f'<div style="margin-top:8px">'
                    f'<img src="data:image/png;base64,{b64}" '
                    f'style="max-width:100%;border-radius:8px;border:1px solid #334155;cursor:pointer" '
                    f'onclick="this.style.maxWidth=this.style.maxWidth==\'100%\'?\'none\':\'100%\'" '
                    f'title="Click to expand" />'
                    f'</div>'
                )
            except Exception:
                pass

        rows += f"""
        <div style="background:#111827;border:1px solid #1f2937;border-radius:10px;
                    padding:16px;margin-bottom:12px;">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:4px">
            <div style="font-weight:600;color:#f1f5f9">{r['name']}</div>
            {status_badge}
          </div>
          {f'<div style="font-size:.82rem;color:#6b7280;margin-top:4px">{r["detail"]}</div>' if r["detail"] else ''}
          {img_tag}
        </div>"""

    # Video embed
    video_section = ""
    if video_path and Path(video_path).exists():
        rel = Path(video_path).name
        shutil.copy(video_path, REPORT_DIR / rel)
        video_section = f"""
        <div style="margin-bottom:2rem">
          <h2 style="font-size:1rem;font-weight:700;color:#f1f5f9;margin-bottom:12px">🎬 Test Recording</h2>
          <video controls style="width:100%;max-width:900px;border-radius:10px;
                                  border:1px solid #334155;background:#000">
            <source src="{rel}" type="video/webm">
            Your browser does not support WebM video.
          </video>
          <p style="color:#6b7280;font-size:.8rem;margin-top:6px">
            Full test run recording · {Path(video_path).stat().st_size // 1024} KB
          </p>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Sweet Spot Test Report — {now}</title>
  <style>
    *{{box-sizing:border-box;margin:0;padding:0}}
    html,body{{overflow-x:hidden;max-width:100%}}
    body{{font-family:'Inter',system-ui,sans-serif;background:#0a0f1a;color:#e2e8f0;padding:2rem;line-height:1.6}}
    @media(max-width:600px){{body{{padding:1rem}}}}
  </style>
</head>
<body>
  <div style="max-width:900px;margin:0 auto">

    <!-- Header -->
    <div style="margin-bottom:2rem">
      <div style="font-size:1.75rem;font-weight:800;margin-bottom:4px">🍰 Sweet Spot Test Report</div>
      <div style="color:#6b7280;font-size:.9rem">{now} · {BASE_URL}</div>
    </div>

    <!-- Score card -->
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
                gap:1rem;margin-bottom:2rem">
      <div style="background:#111827;border:1px solid #1f2937;border-radius:12px;padding:20px;text-align:center">
        <div style="font-size:2.5rem;font-weight:800;color:{grade_color}">{pct}%</div>
        <div style="color:#6b7280;font-size:.8rem;margin-top:4px">PASS RATE</div>
      </div>
      <div style="background:#111827;border:1px solid #1f2937;border-radius:12px;padding:20px;text-align:center">
        <div style="font-size:2.5rem;font-weight:800;color:#10b981">{len(passed)}</div>
        <div style="color:#6b7280;font-size:.8rem;margin-top:4px">PASSED</div>
      </div>
      <div style="background:#111827;border:1px solid #1f2937;border-radius:12px;padding:20px;text-align:center">
        <div style="font-size:2.5rem;font-weight:800;color:{'#ef4444' if failed else '#10b981'}">{len(failed)}</div>
        <div style="color:#6b7280;font-size:.8rem;margin-top:4px">FAILED</div>
      </div>
      <div style="background:#111827;border:1px solid #1f2937;border-radius:12px;padding:20px;text-align:center">
        <div style="font-size:2.5rem;font-weight:800;color:#6366f1">{len(results)}</div>
        <div style="color:#6b7280;font-size:.8rem;margin-top:4px">TOTAL TESTS</div>
      </div>
    </div>

    <!-- Video -->
    {video_section}

    <!-- Test results -->
    <h2 style="font-size:1rem;font-weight:700;color:#f1f5f9;margin-bottom:12px">📋 Test Results</h2>
    {rows}

    <div style="margin-top:2rem;color:#374151;font-size:.78rem;text-align:center">
      Generated by Echo · Liberty-Emporium Test Suite · {now}
    </div>

  </div>
</body>
</html>"""

    report_file = REPORT_DIR / "index.html"
    report_file.write_text(html)
    print(f"\n  📊 HTML report generated: {report_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sweet Spot Visual Test Suite")
    parser.add_argument("--headed", action="store_true",
                        help="Run with visible browser window (requires display)")
    args = parser.parse_args()
    sys.exit(run(headed=args.headed))
