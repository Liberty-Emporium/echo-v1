# Flood Adjuster Research Log

## Session 1 — 2026-05-30 03:22Z (OWL Cron Run #1)

### Sources Attempted

| Source | Status | Notes |
|--------|--------|-------|
| Rainbow Restoration (rainbowrestores.com/locations) | ✅ SUCCESS | 321 locations found. Extracted 109 contacts in flood-prone states (FL, TX, LA, NC, SC, NJ, VA, MS, AL, TN, GA, KY, WV, MD, DE). All have phone numbers. |
| SERVPRO (servpro.com/locations) | ⚠️ PARTIAL | State pages work (FL, TX, LA lists ~100 franchise names) but individual franchise URLs all return 404. City-level data only, no phones. |
| PuroClean (puroclean.com/locations) | ❌ 404 | Location page not found |
| BELFOR (belfor.com/locations) | ❌ 404 | Page not found |
| NAPIA (napia.com/directory) | ❌ 404 | Page not found (JS-rendered, needs different URL) |
| FAPIA (fapia.net/member-directory) | ❌ 404 | Page not found |
| SAPIA (sapia.org/member-directory) | ❌ EMPTY | No content |
| Florida DBPR (myfloridalicense.com) | ⚠️ BLOCKED | Site uses JS form; download URL redirects to WordPress site. Need different approach. |
| Texas TDI (tdi.texas.gov) | ❌ BLOCKED | Client IP blocked |
| Bing Search | ❌ BLOCKED | Cloudflare challenge / sign-in required |
| BBB.org | ❌ BLOCKED | Cloudflare challenge |
| YellowPages.com | ❌ No results | Bing site: search returned nothing useful |

### Contacts Found This Session: 109
- All from Rainbow Restoration franchise locations
- States covered: FL(7), TX(27), LA(3), NC(11), SC(5), NJ(6), VA(13), AL(5), TN(5), GA(8), KY(2), WV(2), MD(3), DE(1), MS(1)
- All have phone numbers, no emails yet
- Website: rainbowrestores.com (all share same corporate site)

### Key Blockers
1. **Bing blocked** — Cloudflare challenges on most searches. Need alternative search engine or residential proxies.
2. **Most directory sites JS-rendered** — NAPIA, state licensing databases all require form interaction or have 404s.
3. **SERVPRO individual pages 404** — Franchise locator only shows state-level lists, no direct contact.
4. **Public adjuster sites mostly down** — Most individual PA company websites are offline or blocked.

### Next Session Priorities
1. Try DuckDuckGo or Yahoo search instead of Bing (avoid Cloudflare)
2. Try SERVPRO search API directly (find-a-location endpoint)
3. Try individual SERVPRO franchise pages via Google cache or different URL patterns
4. Scrape known public adjuster company sites that are still up
5. Try the Florida DBPR "Search by License Type" for Public Adjuster specifically
6. Check if delta-restore.com or other restoration sites have working locators
7. Try NAPIA via browser JS rendering (member directory might work with interaction)

### New Source URLs Discovered
- Rainbow Restoration: https://rainbowrestores.com/locations (WORKING — full list with phones)
- SERVPRO state pages: https://www.servpro.com/locations/{state}/ (working but no individual contact)
- Florida DBPR search: https://www.myfloridalicense.com/wl11.asp?mode=0&search=Public+Adjuster
