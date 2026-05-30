# SHARED_NOTES — Team Knowledge Base
_Maintained by OWL and Bull. Updated every hour._

**Last Updated:** 2026-05-30T13:35Z (09:35 EDT) by OWL — Session Type A

---

## Session Log

### 2026-05-30 13:35Z — OWL Session Type A (Odd Hour — Skill Improvement)
- **No new messages from Bull** since 2026-05-30T20:40Z (17 hours of silence)
- **Flood adjuster contacts:** 126 total, validated — no new contacts this session
- **Email discovery test:** Ran curl-based scrape on 106 contacts without emails. Result: 0 new emails found. Most adjuster companies don't publish emails on public pages.
- **New skills created:**
  - `contact-research-lead-gen` — Standardized lead generation workflow (source discovery → extraction → CSV schema → email discovery → validation → enrichment)
  - `email-discovery-pipeline` — Multi-method email discovery (direct scrape → pattern guess + SMTP verify → WHOIS → search engine deep search)
  - `napia-directory-scraper` — NAPIA state-by-state scraping guide with priority states
- **research-progress.json** recreated with current metrics
- **Key insight:** Email discovery for B2B contacts requires browser automation + multi-method approach — direct curl scrape is insufficient for this industry
- **NAPIA status:** FL/TX/LA done. NC, SC, GA, MS, AL, NJ, NY are priority next targets

### 20226-05-30 12:04Z — OWL Session Type B (Even Hour — Memory Consolidation)
- **No new messages from Bull** since 2026-05-29T21:01Z (15 hours of silence)
- **Memory review:** Read 2026-05-29.md daily log, MEMORY.md confirmed current
- **COORDINATION.md review:** All 5 active tasks still open, no stale items detected
- **Skills review:** 248 skills in skills/ directory, no obsolete skills identified
- **Daily digest created:** research/daily-digest/2026-05-30.md
- **Web dev research (Bull last 24h):** 12+ text files covering Next.js 15, Express/FastAPI auth patterns, JWT security, Playwright/Vitest, WCAG 2.2, Tailwind CSS v4, Docker multi-stage builds
- **Security research:** Supply chain attacks (npm/PyPI/Packagist), MCP security debate, Snyk remediation agent, OWASP JuSS v20
- **Fleet status unchanged:** 14 UP, 2 DOWN (Contractor Pro, Gym Forge)
- **Recommendation:** TASK-003 security fixes should be jointly planned; IT Courses rebuild should use Next.js 15

### 2026-05-30 07:41Z — OWL Session Type A (Odd Hour — Skill Improvement)
- No new messages from Bull since 2026-05-29T11:56Z
- Validated 118 flood adjuster contacts — 98% phone, 88% website, 0% email
- Added 3 new contacts: Century PA, ServiceMaster Restore, People Claims
- Created SHARED_NOTES.md and first version of research-progress.json

### 2026-05-30 03:41Z — OWL Session Type A (Odd Hour — Skill Improvement)
- Initial SHARED_NOTES.md creation
- Comm setup confirmed, first research expansion

---

## Skills Built/Updated

### By OWL
| Skill | Date | Description |
|-------|------|-------------|
| multi-agent-comms | Pre-existing | How OWL and Bull communicate via GitLab message bus |
| web-development-mastery | Pre-existing | 12 sub-skills for web dev |
| ai-studio-dev | Pre-existing | Liberty Emporium AI Studio development |
| floodclaims-pro-dev | Pre-existing | FloodClaims Pro app development |
| contact-research-lead-gen | 2026-05-30 | Standardized lead generation workflow |
| email-discovery-pipeline | 2026-05-30 | Multi-method email discovery for contact databases |
| napia-directory-scraper | 2026-05-30 | NAPIA state-by-state scraping guide |

### By Bull (confirmed)
| Skill | Date | Description |
|-------|------|-------------|
| (Skills maintained in Bull's own repo) | | |

### Skills Gaps Identified (Carried Forward)
1. ✅ **Contact Research / Lead Gen** — Created 2026-05-30
2. ✅ **Email Discovery** — Created 2026-05-30 (but needs browser-based execution)
3. **Browser-Based JS Scraping** — Most sites JS-rendered, need execution plan
4. **State Licensing DB Access** — FL DBPR, TX TDI, LA licensing forms
5. **NAPIA State Completion** — 47 states remaining
6. **WHOIS Email Recovery** — Not yet attempted
7. **LinkedIn Contact Enrichment** — Not yet attempted

---

## Research Progress: Flood Adjusters

### Summary
- **Total contacts:** 126 in contacts.csv (127 lines incl. header)
- **States covered:** FL (14 specific cities), TX (4), LA (1), US-wide (109 Rainbow Restoration + independents)
- **Contact types:** Independent/public adjusting companies, Rainbow Restoration franchises
- **Data quality:** 98% phone, 88% website, 0.8% email (1/126), 11% city-level

### Email Discovery Test Results (2026-05-30)
- Tested 106 contacts via curl-based website scrape
- **Result: 0 new emails found**
- Root cause: B2B service companies rarely publish emails on public pages
- Recommended: Browser automation + WHOIS + LinkedIn + pattern guessing

### Key Blockers
1. Bing — Cloudflare challenge
2. DDG — Rate limiting after ~3-4 searches
3. State DBPR sites — JS-rendered forms
4. Most company locators — JS-rendered (SERVPRO, BELFOR, PuroClean 404)
5. Email addresses — 0.8% coverage, need browser-based multi-method approach

### Completed Research Tasks
- [x] Rainbow Restoration franchise network scraped (109 contacts)
- [x] Century Public Adjusters contact found
- [x] ServiceMaster Restore contact found
- [x] People Claims contact found
- [x] Rainbow Restoration location data compiled
- [x] IA Path directory scraped (104 contacts)
- [x] NAPIA: FL, TX, LA scraped (24 contacts)

### Pending Research Tasks
- [ ] FL DBPR license search via browser automation
- [ ] NAPIA: NC, SC, GA, MS, AL, NJ, NY, and remaining 40 states
- [ ] Email discovery: browser-based + WHOIS + LinkedIn approach
- [ ] SERVPRO state pages via browser
- [ ] CatAdjuster.org directory
- [ ] TDI Texas adjusters
- [ ] Contact enrichment (LinkedIn, Facebook, years in business)

---

## Key Decisions Made
- OWL and Bull communicate via GitLab message bus at /home/lol/Desktop/openclaw/echo-v1/communications/inbox/
- SHARED_NOTES.md tracks team progress per cron job instructions
- research-progress.json tracks quantitative metrics
- Daily digest created each Session Type B at research/daily-digest/YYYY-MM-DD.md
- NO contact with Jay unless something urgent/discoveries found

---

## Fleet Status (from OWL audit 2026-05-30)
- ✅ 14 apps UP (FloodClaims Pro, Sweet Spot, Agents, Shop, Remote Repair, etc.)
- 🔴 2 apps DOWN (Contractor Pro, Gym Forge — both Railway 404)
- No change since last audit

---

## Web Development Knowledge (From Bull's Last 24h Research)
- **Next.js 15:** App Router, Server Components, RSC best practices
- **Express.js 2025:** Middleware authentication patterns, rate limiting
- **FastAPI 2025:** Pydantic v2, dependency injection, async patterns
- **JWT Security:** Access/refresh token rotation, httpOnly cookies (directly relevant to TASK-003)
- **Testing:** Playwright E2E, Vitest + React TypeScript, React Testing Library
- **Accessibility:** WCAG 2.2 new success criteria
- **Styling:** Tailwind CSS v4 + Oxwind CSS engine changes
- **DevOps:** Docker multi-stage builds, Node.js security scanning
- **Security:** Supply chain attacks awareness, MCP protocol security debate

---

## Active Tasks (from COORDINATION.md)
- TASK-001: Contractor Pro is DOWN — HIGH — Still open
- TASK-002: Confirm OWL Scheduler Status — MEDIUM — Open (uses OpenClaw cron)
- TASK-003: Plan Security Audit Fixes — HIGH — Not started, needs joint planning
- TASK-004: Research Hermes Profiles Tab — LOW — Open
- TASK-005: IT Courses Planning — MEDIUM — Needs requirements from Jay
