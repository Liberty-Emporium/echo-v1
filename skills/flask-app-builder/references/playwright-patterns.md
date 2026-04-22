# Playwright Test Patterns

## Standard Test Structure

```python
from playwright.sync_api import sync_playwright
import sys, datetime

BASE_URL = "https://your-app.up.railway.app"
EMAIL    = "admin@yourapp.com"
PASSWORD = "password123"
results  = []

def record(name, passed, detail=""):
    icon = "✅ PASS" if passed else "❌ FAIL"
    print(f"  {icon} — {name}")
    if detail: print(f"         {detail}")
    results.append({"name": name, "passed": passed})

def run():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx     = browser.new_context(viewport={"width": 1280, "height": 800})
        page    = ctx.new_page()
        page.set_default_timeout(15000)
        # ... tests here ...
        browser.close()
    passed = sum(1 for r in results if r["passed"])
    print(f"\n  Grade: {passed}/{len(results)} ({round(100*passed/len(results))}%)")
    return 0 if passed == len(results) else 1

if __name__ == "__main__":
    sys.exit(run())
```

## Common Test Patterns

### Health check
```python
r = page.goto(f"{BASE_URL}/health")
record("Health endpoint", r.status == 200 and "ok" in page.content().lower())
```

### Login
```python
page.goto(f"{BASE_URL}/login")
page.fill('input[name="email"]', EMAIL)
page.fill('input[name="password"]', PASSWORD)
page.click('button[type="submit"]')
page.wait_for_url(f"{BASE_URL}/dashboard", timeout=8000)
record("Login → dashboard", "/dashboard" in page.url)
```

### Page loads with expected content
```python
page.goto(f"{BASE_URL}/orders")
page.wait_for_load_state("networkidle", timeout=8000)
text = page.inner_text("body")
record("Orders page", any(w in text.lower() for w in ["order", "new order", "no orders"]))
```

### Form has inputs
```python
page.goto(f"{BASE_URL}/orders/new")
inputs = page.locator("input, select, textarea").count()
record("New order form", inputs >= 3, f"{inputs} fields found")
```

### Mobile no horizontal scroll (most important!)
```python
mobile_ctx  = browser.new_context(viewport={"width": 375, "height": 812})
mobile_page = mobile_ctx.new_page()
mobile_page.goto(f"{BASE_URL}/dashboard")
mobile_page.wait_for_load_state("networkidle")
sw = mobile_page.evaluate("document.documentElement.scrollWidth")
cw = mobile_page.evaluate("document.documentElement.clientWidth")
record("Mobile: no horizontal scroll", sw <= cw + 2, f"scrollWidth={sw}, clientWidth={cw}")
mobile_ctx.close()
```

### Fill and submit a form
```python
page.goto(f"{BASE_URL}/orders/new")
page.fill('input[name="customer_name"]', "Test Customer")
page.fill('input[name="phone"]', "336-555-0100")
page.select_option('select[name="order_type"]', "Custom Cake")
page.click('button[type="submit"]')
page.wait_for_load_state("networkidle")
record("Create order", "/orders/" in page.url or "success" in page.inner_text("body").lower())
```

### Check dollar amount present
```python
import re
text = page.inner_text("body")
has_dollar = bool(re.search(r'\$[\d,]+', text))
record("Report shows revenue", has_dollar)
```

## Running Tests

```bash
# From this machine
python3 /root/.openclaw/workspace/echo-v1/scripts/test_<appname>.py

# From Jay's Kali machine
pip3 install playwright --break-system-packages
playwright install chromium
curl -o test_app.py https://raw.githubusercontent.com/Liberty-Emporium/echo-v1/main/scripts/test_<appname>.py
python3 test_app.py
```
