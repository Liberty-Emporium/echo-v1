# SKILL: Contact Research & Lead Gen

> Standardized workflow for building targeted contact databases — essential for sales, marketing, and business development.

## When to Use
- Building prospect lists for outreach campaigns
- Researching companies in a specific industry/region
- Finding decision-makers at target companies
- Enriching existing contact data with emails, phone numbers
- Competitive intelligence gathering

## Phase 1: Source Discovery

### Directories & Databases
| Type | Source Pattern | Method |
|------|---------------|--------|
| Industry associations | `[industry].com/find-a-[role]` | Browser scrape |
| State licensing DBs | `[state].gov/license-search` | Browser (JS forms) |
| Franchise locators | `[brand].com/locations` | Browser (JS-rendered) |
| Business directories | YP.com, YellowPages, Manta | Search + scrape |
| Professional networks | LinkedIn Sales Nav | Manual export |

### Search Engine Strategy
```bash
# DDG with rate limiting (30s+ delays)
# Prioritize: site-specific searches, then general
queries=(
  "public insurance adjusters Florida"
  "flood restoration companies North Carolina"
  "independent insurance adjusters directory"
  "site:napia.com \"public adjuster\" Florida"
)
```

### Rate Limits Per Engine
| Engine | Max searches/min | Notes |
|--------|-----------------|-------|
| DuckDuckGo | 3-4 | Then empty results, 30s+ delay needed |
| Bing | 5-6 | Cloudflare challenge common |
| Google | 2-3 | Aggressive bot detection |
| Brave Search API | 2000/mo | Reliable, requires API key |

## Phase 2: Data Extraction

### For Static HTML Sites
```bash
curl -sL -A "LibertyBot/1.0 (research@alexanderai.site)" "URL" | \
  python3 -c "
import sys, re, json
html = sys.stdin.read()
emails = list(set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}', html)))
phones = list(set(re.findall(r'[\+]?[(]?[0-9]{1,4}[)]?[-\\s\\./0-9]{7,}', html)))
print(json.dumps({'emails': emails, 'phones': phones, 'html_len': len(html)}))
"
```

### For JS-Rendered Sites (browser required)
```python
# Use browser tool or Playwright
# 1. Navigate to URL
# 2. Wait for networkidle + content selector
# 3. Extract data attributes
# 4. Handle pagination (click "Next" or scroll)
```

### Pattern: Franchise Locator Pages
Most franchise locators follow this pattern:
1. Visit `/locations` or `/find-a-location`
2. Select state from dropdown (JS event)
3. Wait for results to load
4. Each result card has: name, address, phone, sometimes email

## Phase 3: CSV Schema

Standard contact CSV format:
```csv
name,phone,email,city,state,website,category,source,source_date,notes
Acorn Claims,417-581-5200,,,US,www.AcornClaims.com,independent-adjuster,iapath.com,2026-05-30,US-wide
Century Public Adjusters,(888) 585-8010,office@centurypublicadjusters.com,Tampa,FL,centurypublicadjusters.com,public-adjuster,direct-site,2026-05-30,FL licensed
```

### Field Definitions
| Field | Required | Description |
|-------|----------|-------------|
| name | ✅ | Company or individual name |
| phone | Recommended | Primary phone number |
| email | Recommended | Primary email address |
| city | ✅ | City location |
| state | ✅ | 2-letter state code |
| website | Recommended | Primary URL |
| category | ✅ | Industry/category tag |
| source | ✅ | Where this data came from |
| source_date | ✅ | YYYY-MM-DD |
| notes | Optional | Context, special handling |

## Phase 4: Email Discovery

### Method 1: Direct Site Scrape
```bash
# Scrape company website for contact emails
curl -sL "URL" | grep -oP '[a-zA-Z0-9._%+-]+@'URL_DOMAIN
```

### Method 2: WHOIS Lookup
```bash
whois DOMAIN | grep -i "email\|contact"
```

### Method 3: Hunter.io Pattern Search
```bash
# If Hunter API key available
curl -s "https://api.hunter.io/v2/domain-search?domain=DOMAIN&api_key=TOKEN"
```

### Method 4: LinkedIn Search
- Search for "[Company] + contact"
- Check "About" section for email
- Common patterns: info@, contact@, admin@, hello@

### Method 5: Email Pattern Guessing + Verification
```python
# After finding one email, guess others
patterns = [
    "info@{domain}",
    "contact@{domain}",
    "admin@{domain}",
    "hello@{domain}",
    "support@{domain}",
    "{first}@{domain}",
]
# Verify with SMTP RCPT TO (no actual email sent)
```

## Phase 5: Validation & Deduplication

```python
import csv
from collections import defaultdict

def deduplicate_contacts(input_csv: str, output_csv: str):
    """Remove duplicate contacts by name + phone."""
    seen = set()
    unique = []
    
    with open(input_csv) as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row["name"].lower().strip(), row["phone"].strip())
            if key not in seen:
                seen.add(key)
                unique.append(row)
    
    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(unique)
    
    return len(unique)
```

## Phase 6: Enrichment

For each contact, try to add:
1. **Email** — via methods above
2. **LinkedIn URL** — search "[company name] linkedin"
3. **Facebook page** — search "[company name] facebook"
4. **Years in business** — from About page
5. **Number of employees** — from LinkedIn
6. **Services offered** — from website content
7. **License numbers** — from state licensing DB

## Output Location
All contact databases go to:
```
/home/lol/Desktop/openclaw/echo-v1/research/[campaign-name]/contacts.csv
/home/lol/Desktop/openclaw/echo-v1/research/[campaign-name]/research_log.md
/home/lol/Desktop/openclaw/echo-v1/research/[campaign-name]/enrichment.md
```

## Integration with Email Pipeline
After building contacts.csv, pass to `email-discovery-pipeline` skill for systematic email enrichment.

---

_Created by OWL — 2026-05-30 — Liberty Emporium_
