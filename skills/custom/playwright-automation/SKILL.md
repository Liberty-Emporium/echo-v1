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

## Best Practices

- Use `wait_for_load_state('networkidle')` for SPAs
- Take screenshots on failure
- Use selectors: `page.locator('#id')` over xpath
- Handle dialogs with `page.on('dialog', ...)`