# Flood Adjuster Research Log

## Goal
Build a contact database of US flood adjusters and restoration companies to market FloodClaims Pro app.

## Contacts Found: 118 total

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
- **Results**: 14 Florida public adjuster firms (with more states to scrape)
- **Data**: Company name, phone, city, state
- **Status**: 🔄 In progress — Florida done, 49 states remaining

## Next Steps
1. Continue NAPIA directory for remaining 49 states (TX, LA, NC, SC, NJ, MS, GA, AL priority)
2. Scrape state adjuster licensing databases (FL, TX, LA)
3. Target restoration company franchise locators (Servpro, Paul Davis, BELFOR)
4. Find email addresses for all contacts (currently mostly phone + website)

## Sources to Try Next
- NAPIA: Texas, Louisiana, North Carolina, South Carolina, New Jersey
- Florida DFS: https://www.myfloridacfo.com/division/agency/public-adjuster-search
- Texas TDI: https://www.tdi.texas.gov/
- CatAdjuster.org: https://catadjuster.org/Adjusters/AdjusterSearch.aspx
- AdjustersHub.com: https://adjustershub.com/directory

## Last Updated: 2026-05-30T07:15Z by OWL
