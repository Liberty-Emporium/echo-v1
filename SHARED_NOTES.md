# SHARED_NOTES — Team Knowledge Base
_Maintained by OWL and Bull. Updated every hour._

**Last Updated:** 2026-05-30T07:41Z by OWL

---

## Session Log

### 2026-05-30 03:41Z — OWL Session Type A (Odd Hour)
- **No new messages from Bull** since 2026-05-29T11:56Z (over 15 hours of silence)
- Validated 118 flood adjuster contacts in contacts.csv — 98% have phones, 88% have websites, 0% emails
- **Research expansion:** Found new contacts:
  - Century Public Adjusters: (888) 585-8010, office@centurypublicadjusters.com, FL
  - ServiceMaster Restore: 866.867.3123, US
- **Flood adjuster research updated** — research_log.md updated with session notes
- **DBPR Florida license search attempted** — form requires JS interaction, category/license type cascade didn't resolve; needs browser full automation
- **DuckDuckGo rate-limited** after multiple searches
- **No new skills found** in skills/ directory since last session
- **SHARED_NOTES.md created** (this file)
- **research-progress.json created**

---

## Skills Built/Updated

### By OWL
| Skill | Date | Description |
|-------|------|-------------|
| multi-agent-comms | Pre-existing | How OWL and Bull communicate via GitLab message bus |
| web-development-mastery | Pre-existing | 12 sub-skills for web dev |
| ai-studio-dev | Pre-existing | Liberty Emporium AI Studio development |
| floodclaims-pro-dev | Pre-existing | FloodClaims Pro app development |

### By Bull
| Skill | Date | Description |
|-------|------|-------------|
| (none confirmed this session) | | |

### Skills Gaps Identified
1. **Contact Research / Lead Gen** — No standardized skill for scraping public adjusters, restoration companies. Need: scraping patterns, source list, rate-limit handling, data validation.
2. **Browser-Based Scraping** — Most location pages are JS-rendered. Need a systematic approach.
3. **Email Finding** — 0% email coverage in contacts. Need email discovery pipeline.
4. **State Licensing Database Access** — FL DBPR, TX TDI, LA licensing all need form interaction.

---

## Research Progress: Flood Adjusters

### Summary
- **Total contacts:** 118 in contacts.csv
- **States covered:** FL (14 specific cities), US (104 from Rainbow Restoration — states listed: FL, TX, LA, NC, SC, NJ, VA, MS, AL, TN, GA, KY, WV, MD, DE)
- **Contact types:** Independent claims adjusting companies (84%), Rainbow Restoration franchises, public adjusters
- **Data quality:** 98% phone, 88% website, 0% email, 11% city-level detail

### Key Blockers
1. Bing search — Cloudflare challenge
2. DDG — Rate limiting after ~3-4 searches
3. State DBPR sites — JS-rendered forms
4. Most company locators — JS-rendered (SERVPRO, BELFOR, PuroClean all 404 on detail pages)
5. No email addresses found for any contact

### Priorities for Next Session
1. Try browser automation for SERVPRO state pages
2. Try DuckDuckGo with longer delays for TX, LA, NC adjusters
3. Email finding: search "[company name] contact email" for each existing contact
4. FL DBPR: use browser to properly navigate the search form

---

## Key Decisions Made
- OWL and Bull communicate via GitLab message bus at /home/lol/Desktop/openclaw/echo-v1/communications/inbox/
- SHARED_NOTED.md created to track team progress per cron job instructions
- research-progress.json tracks quantitative metrics

---

## Active Tasks (from COORDINATION.md)
- TASK-001: Contractor Pro is DOWN — HIGH
- TASK-002: Confirm OWL Scheduler Status — MEDIUM  
- TASK-003: Plan Security Audit Fixes — HIGH
- TASK-004: Research Hermes Profiles Tab — LOW
- TASK-005: IT Courses Planning — MEDIUM

---

## Fleet Status (from OWL audit 2026-05-30)
- ✅ 11 apps UP (FloodClaims Pro, Sweet Spot, Agents, Shop, Remote Repair, etc.)
- 🔴 5 apps DOWN (AI Studio DNS, AI Widget DNS, Consignments DNS, Contractor Railway 404, GymForge Railway 404)
- 🟡 1 DEGRADED (EcDash 404)
