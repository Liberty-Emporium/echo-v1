# SKILL: Email Discovery Pipeline

> Systematic email finding for contact databases — turns phone-only contacts into fully actionable leads.

## When to Use
- After building a contact database with phone/website but no emails
- Enriching existing CRM data
- Before launching email outreach campaigns
- Ongoing: periodic re-enrichment of stale contact data

## Strategy Overview

```
contacts.csv (phone + website)
        │
        ▼
┌─────────────────────┐
│ 1. Direct Site      │  ← scrape each website for contact emails
│    Scrape           │     (static HTML: curl, JS-rendered: browser)
└────────┬────────────┘
         │ (remaining missing)
         ▼
┌─────────────────────┐
│ 2. Pattern Guess    │  ← common patterns (info@, contact@, admin@)
│    + SMTP Verify    │     verify with SMTP RCPT TO + MX lookup
└────────┬────────────┘
         │ (remaining missing)
         ▼
┌─────────────────────┐
│ 3. WHOIS Lookup     │  ← domain WHOIS for registrant email
│                     │     (often privacy-protected but worth trying)
└────────┬────────────┘
         │ (remaining missing)
         ▼
┌─────────────────────┐
│ 4. Search Engine    │  ← DDG/Bing: "[company name] email contact"
│    Deep Search      │     "[name] @domain", "mailto: site:domain"
└────────┬────────────┘
         ▼
    enriched.csv  ← contacts with emails filled in
```

## Method 1: Direct Website Scrape

### Static Sites (bash)
```bash
# Extract all emails from a website
scrape_emails() {
    local url="$1"
    local domain=$(echo "$url" | sed 's|https\?://||;s|/.*||')
    curl -sL -A "Mozilla/5.0 (compatible; LibertyBot/1.0)" "$url" | \
        grep -oP "[a-zA-Z0-9._%+-]+@${domain}" | sort -u
}

# Scrape all pages from sitemap
scrape_sitemap_emails() {
    local domain="$1"
    local sitemap="https://${domain}/sitemap.xml"
    # Extract URLs from sitemap
    urls=$(curl -sL "$sitemap" | grep -oP 'https?://[^<]+' | head -20)
    for url in $urls; do
        emails=$(scrape_emails "$url")
        [ -n "$emails" ] && echo "$url: $emails"
        sleep 2
    done
}
```

### Requirements for JS-Rendered Sites
Use browser automation (Playwright or OWL browser tools):
1. Navigate to website
2. Wait for page load (networkidle)
3. Check common locations: footer, contact page, about page
4. Look for `mailto:` links
5. Check page source for email patterns

## Method 2: Pattern Guessing

```python
import dns.resolver
import smtplib
import socket

def guess_emails(domain: str, first_name: str = "") -> list[str]:
    """Generate likely email patterns for a domain."""
    patterns = [
        f"info@{domain}",
        f"contact@{domain}",
        f"admin@{domain}",
        f"hello@{domain}",
        f"support@{domain}",
        f"office@{domain}",
    ]
    if first_name:
        fn = first_name.lower().strip()
        patterns.extend([
            f"{fn}@{domain}",
            f"{fn[0]}@{domain}",
        ])
    return patterns

def verify_email_smtp(email: str) -> bool:
    """Verify email exists via SMTP RCPT TO (no actual email sent)."""
    domain = email.split("@")[1]
    try:
        # Get MX records
        records = dns.resolver.resolve(domain, "MX")
        mx_host = str(records[0].exchange).rstrip(".")
        
        # Connect to SMTP server
        with smtplib.SMTP(mx_host, timeout=10) as server:
            server.ehlo()
            server.mail("verify@alexanderai.site")
            code, _ = server.rcpt(email)
            return code == 250
    except Exception:
        return False
```

## Method 3: WHOIS Email Discovery

```bash
# Get WHOIS data for domain
whois DOMAIN | grep -iE "Registrant Email|Admin Email|Tech Email|Contact" | head -5

# Using Python whois library
python3 -c "
import whois
w = whois.whois('DOMAIN_HERE')
print('Registrant:', w.get('emails', 'N/A'))
"
```

## Method 4: Search Engine Queries

### DDG Queries for Email Discovery
```bash
# Query patterns that often reveal emails
queries=(
  "\"COMPANY NAME\" email contact"
  "\"COMPANY NAME\" \"@domain.com\""
  "site:domain.com inurl:contact"
  "mailto: site:domain.com"
  "telephone directory \"COMPANY NAME\" \"@\""
)
```

### Expected Success Rates
| Method | Typical Success Rate | Time per Contact |
|--------|---------------------|------------------|
| Direct site scrape | 15-25% | 5-10s |
| Pattern guess + verify | 10-20% | 15-30s |
| WHOIS lookup | 5-10% (often privacy-protected) | 3-5s |
| Search engine deep | 5-15% | 20-40s |

## Batch Processing Script

```python
#!/usr/bin/env python3
"""Enrich contacts.csv with discovered emails."""
import csv
import subprocess
import re
import time
import sys

def enrich_contacts(input_csv: str, output_csv: str):
    with open(input_csv) as f:
        reader = csv.DictReader(f)
        contacts = list(reader)
        fieldnames = reader.fieldnames + ["email_source"]
    
    enriched = 0
    for i, contact in enumerate(contacts):
        if contact.get("email"):
            enriched += 1
            continue
        
        website = contact.get("website", "")
        domain = re.sub(r'^(https?://)?(www\.)?', '', website).split('/')[0]
        
        if not domain:
            continue
                
        # Method 1: Try common patterns via curl
        try:
            result = subprocess.run(
                ["curl", "-sL", f"https://{domain}", "-A", "LibertyBot/1.0"],
                capture_output=True, text=True, timeout=10
            )
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@' + re.escape(domain), 
                              result.stdout)
            emails = [e for e in emails if not e.endswith(('.png','.jpg','.gif','.css'))]
            if emails:
                contact["email"] = emails[0]
                contact["email_source"] = f"site-scrape:{domain}"
                enriched += 1
                if enriched % 10 == 0:
                    print(f"  [{i+1}/{len(contacts)}] {enriched} emails found", 
                          file=sys.stderr)
        except Exception:
            pass
        
        time.sleep(1.5)  # Rate limit
    
    # Write output
    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(contacts)
    
    print(f"Complete: {enriched}/{len(contacts)} contacts have emails")

if __name__ == "__main__":
    enrich_contacts(
        "research/flood-adjusters/contacts.csv",
        "research/flood-adjusters/contacts_enriched.csv"
    )
```

## Quality Guidelines
1. **Never use scraped emails for spam** — only for legitimate business outreach
2. **Always include unsubscribe links** in any email campaign
3. **Respect CAN-SPAM and GDPR** — provide opt-out mechanism
4. **Verify before sending** — bounce rates >5% damage sender reputation
5. **Rate limit** — max 50 emails/day from a new sending domain

## Expected Outcomes
Starting from 0% email coverage, expect:
- **Phase 1 (direct scrape):** +15-25% coverage
- **Phase 2 (pattern + verify):** +10-15% coverage  
- **Phase 3 (WHOIS + search):** +5-10% coverage
- **Total expected:** 30-50% email coverage after full pipeline

---

_Created by OWL — 2026-05-30 — Liberty Emporium_
