# Flood Adjuster Research Log

## Goal
Build a contact database of US flood adjusters and restoration companies to market FloodClaims Pro app.

## Contacts Found: 123 total

### Source 1: IA Path — Independent Adjusters Directory
- **URL**: https://iapath.com/independent-adjusting-firms/
- **Date**: 2026-05-30
- **Method**: Browser + curl (full page scrape)
- **Results**: 104 US-based independent adjusting firms
- **Data**: Company name, phone, website
- **Categories**: Catastrophic adjusting, daily auto damage, PDR/hail
- **Top firms**: Crawford & Company, Pilot Catastrophe, EA Renfroe, Eberl Claims, Worley, Sedgwick
- **Status**: ✅ Complete

### Source 2: NAPIA — National Association of Public Insurance Adjusters
- **URL**: https://www.napia.com/find-a-public-adjuster
- **Date**: 2026-05-30
- **Method**: Browser automation (JS-rendered SPA, search by state)
- **Results**: 14 Florida + 4 Texas + 1 Louisiana = 19 NAPIA public adjuster firms (with more states to scrape)
- **Data**: Company name, phone, city, state
- **Status**: 🔄 In progress — Florida done, 49 states remaining

## Next Steps
1. Continue NAPIA directory for remaining 47 states (NC, SC, NJ, MS, GA, AL priority) — TX & LA done
2. Scrape state adjuster licensing databases (FL, TX, LA)
3. Target restoration company franchise locators (Servpro, Paul Davis, BELFOR)
4. Find email addresses for all contacts (currently mostly phone + website)

## Sources to Try Next
- NAPIA: Texas, Louisiana, North Carolina, South Carolina, New Jersey
- Florida DFS: https://www.myfloridacfo.com/division/agency/public-adjuster-search
- Texas TDI: https://www.tdi.texas.gov/
- CatAdjuster.org: https://catadjuster.org/Adjusters/AdjusterSearch.aspx
- AdjustersHub.com: https://adjustershub.com/directory

---

## Session 3 — 2026-05-30 07:41Z (OWL Cron Run #2)

### Sources Attempted

| Source | Status | Notes |
|--------|--------|-------|
| DuckDuckGo search (public adjusters FL/TX/LA/NC/SC/GA/AL) | ⚠️ RATE-LIMITED | Got 10 results for FL, then DDG started returning empty. Need longer delays (30s+) between searches. |
| centurypublicadjusters.com | ✅ SUCCESS | Phone: (888) 585-8010, (813) 588-5575. Email: office@centurypublicadjusters.com |
| servicemasterrestore.com | ✅ SUCCESS | Phone: 866.867.3123 |
| alphaclaims.com | ⚠️ WRONG SITE | Redirected to unrelated site (303 number is Colorado) |
| peopleclaims.com | ✅ SUCCESS | Phone: (954) 866-4986 |
| myfloridalicense.com (DBPR) | ⚠️ JS FORM | License Type dropdown depends on License Category via JS cascade. "Real Estate" category selected but no "Public Adjuster" license type appeared. Needs deeper browser automation. |
| pprtexas.com/locations | ❌ EMPTY | 114 bytes — JS-rendered |
| southernrestoration.com | ⚠️ WRONG NUMBER | 303-893-0552 is Colorado, not relevant |
| delta-restore.com | ❌ DNS FAIL | |
| restoration1.com | ❌ NO PHONES | JS-rendered, no phone numbers in source |
| dryco.us | ❌ DNS FAIL | |
| allstarpublicadjusting.com | ❌ SSL ERROR | |
| belfor.com/locations | ❌ 404 | |
| puroclean.com/locations | ❌ 404 | |

### Contacts Found This Session: 3 new
1. **Century Public Adjusters** — (888) 585-8010 — office@centurypublicadjusters.com — FL
2. **ServiceMaster Restore** — 866.867.3123 — US
3. **People Claims** — (954) 866-4986 — FL

### Data Quality Notes
- contacts.csv now has 118 entries (117 data rows + header)
- 98% have phone numbers, 0% have emails, 11% have city-level data
- Most entries are from Rainbow Restoration (same corporate website)
- Need to diversify sources to get independent adjusters with direct emails

### Key Learnings
1. **DDG rate limits fast** — max 3-4 searches per minute, then empty results
2. **Most restoration franchise locators are JS-rendered** — curl gets empty/minimal HTML
3. **FL DBPR form is complex** — category→license type cascade via JS, needs proper browser automation
4. **Direct company website scraping works** — when sites are static HTML, curl gets phone numbers
5. **Email finding** — only found 1 email (office@centurypublicadjusters.com) from direct site scrape

### Next Session Priorities
1. Use browser to properly navigate FL DBPR search (select correct category for Public Adjuster)
2. Try CatAdjuster.org directory (https://catadjuster.org/Adjusters/AdjusterSearch.aspx)
3. Try AdjustersHub.com directory
4. Use browser for SERVPRO state pages (JS-rendered)
5. Email finding: search each company name + "contact email" via DDG with 30s delays
6. Try NAPIA for remaining states (NC, SC, NJ, MS, GA, AL) — TX & LA already done

## Last Updated: 2026-05-30T07:41Z by OWL
