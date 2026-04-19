---
name: playwright-automation
description: Browser automation with Playwright for testing and scraping. Use when you need to test web apps, scrape dynamic content, or automate browser tasks.
---

# Playwright Automation

## Install

```bash
pip install playwright
playwright install chromium
```

## Basic Usage

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://example.com')
    print(page.title())
    browser.close()
```

## Testing

```python
def test_login():
    with sync_playwright() as p:
        page = p.chromium.launch().new_page()
        page.goto('/login')
        page.fill('#username', 'admin')
        page.fill('#password', 'secret')
        page.click('button[type="submit"]')
        assert '/dashboard' in page.url
```

## Scraping

```python
def scrape_products():
    with sync_playwright() as p:
        page = p.chromium.launch().new_page()
        page.goto('/products')
        items = page.query_selector_all('.product')
        for item in items:
            print(item.query('h3').inner_text())
```

## Grace Caregiver Automation

Echo can manage Mom's Grace app directly — no UI needed.

### Natural language (preferred — Echo parses and runs):
```
"Add blood pressure pill, Lisinopril, 10mg, every morning at 8am"
"Add doctor appointment, Dr. Smith, April 25th at 2pm at 123 Main St"
"Add task: call the pharmacy tomorrow"
"Remove Lisinopril"
"Set name to Dorothy"
```

### Direct CLI:
```bash
cd /root/.openclaw/workspace/echo-v1/scripts
python3 grace_natural.py "Add Lisinopril 10mg every morning at 8am"

# Or direct:
python3 grace_caregiver.py add_med --name "Lisinopril" --dose "10mg" --times "08:00"
python3 grace_caregiver.py add_appointment --name "Dr. Smith" --date "2026-04-25" --time "14:00"
python3 grace_caregiver.py add_task --name "Call pharmacy" --due_date "2026-04-20"
python3 grace_caregiver.py remove_med --name "Lisinopril"
python3 grace_caregiver.py set_name --name "Dorothy"
python3 grace_caregiver.py screenshot
```

### Env vars needed:
- GRACE_URL: https://web-production-1015f.up.railway.app
- GRACE_PIN: your caregiver PIN (default: 1234)

## Best Practices

- Use `wait_for_load_state('networkidle')` for SPAs
- Take screenshots on failure
- Use selectors: `page.locator('#id')` over xpath
- Handle dialogs with `page.on('dialog', ...)`