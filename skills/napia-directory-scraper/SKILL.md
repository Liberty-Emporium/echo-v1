# SKILL: NAPIA Directory Scraper

> Systematic scraping of the National Association of Public Insurance Adjusters (NAPIA) directory — state by state.

## Source
- **URL:** https://www.napia.com/find-a-public-adjuster
- **Method:** Browser automation (JS-rendered SPA with state dropdown)
- **Data:** Company name, phone, city, state

## Known Status (as of 2026-05-30)
- The NAPIA site uses JavaScript rendering — direct curl returns empty/minimal HTML
- A search-by-state mechanism exists but requires browser automation
- Some state pages have returned 404 errors — site may be partially broken
- **Completed:** Florida (19 contacts), Texas (4), Louisiana (1)
- **Remaining:** 47 states

## Priority States (FloodClaims Pro Marketing Targets)
1. **FL** ✅ DONE — 19 contacts
2. **TX** ✅ DONE — 4 contacts  
3. **LA** ✅ DONE — 1 contact
4. **NC** — Hurricane/flood zone, high value
5. **SC** — Coastal flooding
6. **GA** — Storm damage
7. **MS** — Hurricane prone
8. **AL** — Hurricane/tropical storm
9. **NJ** — Superstorm Sandy legacy
10. **NY** — Hurricane risk

## Automation Strategy

### Browser-Based Scraping with OWL Tools
```
For each priority state:
  1. Navigate to https://www.napia.com/find-a-public-adjuster
  2. Wait for page load (networkidle)
  3. Select state from dropdown (find select element, select by text)
  4. Click "Search" button
  5. Wait for results to load
  6. Extract all visible results (company, phone, city)
  7. If pagination exists, click next and repeat
  8. Save to contacts.csv
  9. Move to next state
```

### Alternative: Direct URL Pattern
```python
# Try direct state-specific URLs
state_urls = {
    "FL": "https://www.napia.com/find-a-public-adjuster/florida",
    "TX": "https://www.napia.com/find-a-public-adjuster/texas",
    # ... etc
}
# Test if these return real data with curl
```

### Fallback: IA Path Directory
```bash
# IA Path directory covers many states
curl -sL "https://iapath.com/independent-adjusting-firms/" -A "LibertyBot/1.0"
# Extract all firms with name, phone, website
```

## Data Schema
```csv
name,phone,city,state,website,source,source_date
```

## Schedule
Run during Session Type A (skill improvement) hours:
- Odd hours 13, 15, 17, 19, 21, 23, 1, 3, 5, 7, 9, 11
- Target: 2-3 states per session
- Expected completion: ~8 sessions (within 2 days)

## Integration
Results feed into:
- `research/flood-adjusters/contacts.csv` (append new contacts)
- `research/flood-adjusters/research_log.md` (log findings)
- `research-progress.json` (update metrics)

---

_Created by OWL — 2026-05-30 — Liberty Emporium_
