# SKILL: Web Scraping Engine

> Automated data collection from websites — for research, monitoring, lead generation.

## When to Use
- Competitor price monitoring
- Lead generation (finding emails, phone numbers)
- Content aggregation
- Market research
- SEO monitoring (rankings, backlinks)
- Social media monitoring

## Legal & Ethical Rules
1. **Always check robots.txt** — respect crawl-delay and disallow rules
2. **Rate limit yourself** — max 1 request/second to any domain
3. **Identify your bot** — use a proper User-Agent string
4. **Don't scrape personal data** — GDPR/CCPA compliance
5. **Cache results** — don't re-scrape unchanged content
6. **Prefer APIs** — if a site has an API, use it instead

## Python Scraping Stack

### Basic: requests + BeautifulSoup
```python
import requests
from bs4 import BeautifulSoup
import time

def scrape_page(url: str) -> dict:
    headers = {"User-Agent": "LibertyBot/1.0 (research@libertyemporium.com)"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    return {
        "title": soup.title.string if soup.title else "",
        "headings": [h.text.strip() for h in soup.find_all(["h1", "h2", "h3"])],
        "links": [a["href"] for a in soup.find_all("a", href=True)],
        "text": soup.get_text(separator=" ", strip=True)[:5000],
    }

# Rate-limited scraping
def scrape_urls(urls: list[str], delay: float = 1.0) -> list[dict]:
    results = []
    for url in urls:
        try:
            results.append(scrape_page(url))
            time.sleep(delay)  # Be respectful
        except Exception as e:
            results.append({"url": url, "error": str(e)})
    return results
```

### Advanced: Playwright (JavaScript-rendered sites)
```python
from playwright.sync_api import sync_playwright

def scrape_dynamic(url: str) -> dict:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent="LibertyBot/1.0")
        page.goto(url, wait_until="networkidle", timeout=30000)
        
        # Wait for dynamic content
        page.wait_for_selector(".product-list", timeout=10000)
        
        data = page.evaluate("""() => {
            return {
                title: document.title,
                products: Array.from(document.querySelectorAll('.product')).map(el => ({
                    name: el.querySelector('.name')?.textContent,
                    price: el.querySelector('.price')?.textContent,
                }))
            }
        }""")
        
        browser.close()
        return data
```

### Structured Data Extraction
```python
import re
from urllib.parse import urljoin, urlparse

def extract_emails(text: str) -> list[str]:
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return list(set(re.findall(pattern, text)))

def extract_phones(text: str) -> list[str]:
    pattern = r'[\+]?[(]?[0-9]{1,4}[)]?[-\s\./0-9]{7,}'
    return list(set(re.findall(pattern, text)))

def extract_social_links(soup, base_url: str) -> dict:
    social = {}
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "twitter.com" in href or "x.com" in href:
            social["twitter"] = href
        elif "linkedin.com" in href:
            social["linkedin"] = href
        elif "facebook.com" in href:
            social["facebook"] = href
        elif "instagram.com" in href:
            social["instagram"] = href
    return social
```

### Sitemap Scraping
```python
import xml.etree.ElementTree as ET

def get_sitemap_urls(sitemap_url: str) -> list[str]:
    response = requests.get(sitemap_url, timeout=10)
    root = ET.fromstring(response.content)
    ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return [loc.text for loc in root.findall(".//ns:loc", ns)]

# Usage: crawl all pages from sitemap
urls = get_sitemap_urls("https://example.com/sitemap.xml")
pages = scrape_urls(urls, delay=0.5)
```

### Storing Results
```python
import sqlite3
import json
from datetime import datetime

class ScrapingDB:
    def __init__(self, db_path: str = "scraping.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS scraped_pages (
                id INTEGER PRIMARY KEY,
                url TEXT NOT NULL,
                title TEXT,
                content TEXT,
                metadata JSON,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(url, scraped_at)
            )
        """)
    
    def save(self, url: str, data: dict):
        self.conn.execute(
            "INSERT INTO scraped_pages (url, title, content, metadata) VALUES (?, ?, ?, ?)",
            (url, data.get("title"), data.get("text"), json.dumps(data))
        )
        self.conn.commit()
    
    def search(self, query: str) -> list[dict]:
        cursor = self.conn.execute(
            "SELECT url, title, scraped_at FROM scraped_pages WHERE content LIKE ?",
            (f"%{query}%",)
        )
        return [{"url": r[0], "title": r[1], "scraped_at": r[2]} for r in cursor]
```

## Cron-Based Monitoring
```python
# Run daily to check for changes
def monitor_site(url: str, selector: str, db: ScrapingDB):
    soup = scrape_page(url)
    current_hash = hash(str(soup.select(selector)))
    
    last = db.get_latest(url)
    if last and last["hash"] != current_hash:
        # Content changed — alert!
        send_alert(f"Content changed on {url}")
    
    db.save_hash(url, current_hash)
```
