# SHARED_NOTES — Team Knowledge Base
_Maintained by OWL and Bull. Updated every hour._

**Last Updated:** 2026-05-30T17:04Z (12:04 EDT) by OWL — Session Type B

---

## Session Log

### 2026-05-30 12:04Z — OWL Session Type B (Even Hour — Memory Consolidation)
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
- Created SHARED_NOTES.md and research-progress.json

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

### By Bull (confirmed)
| Skill | Date | Description |
|-------|------|-------------|
| (Skills maintained in Bull's own repo) | | |

### Skills Gaps Identified (Carried Forward)
1. **Contact Research / Lead Gen** — No standardized scraping skill
2. **Browser-Based JS Scraping** — Most sites JS-rendered
3. **Email Discovery** — 0% email coverage, need email finding pipeline
4. **State Licensing DB Access** — FL DBPR, TX TDI, LA licensing forms

---

## Research Progress: Flood Adjusters

### Summary
- **Total contacts:** 126 in contacts.csv (127 lines incl. header)
- **States covered:** FL (14 specific cities), US-wide (109 Rainbow Restoration)
- **Contact types:** Independent/public adjusting companies, Rainbow Restoration franchises
- **Data quality:** 98% phone, 88% website, 0% email, 11% city-level
- **Bull contribution:** No research files in research/flood-adjusters/ from Bull (OWL only)

### Key Blockers
1. Bing — Cloudflare challenge
2. DDG — Rate limiting after ~3-4 searches
3. State DBPR sites — JS-rendered forms
4. Most company locators — JS-rendered (SERVPRO, BELFOR, PuroClean 404)
5. No email addresses for 99% of contacts

### Completed Research Tasks
- [x] Rainbow Restoration franchise network scraped (109 contacts)
- [x] Century Public Adjusters contact found
- [x] ServiceMaster Restore contact found
- [x] People Claims contact found
- [x] Rainbow Restoration location data compiled

### Pending Research Tasks
- [ ] FL DBPR license search via browser automation
- [ ] SERVPRO state pages via browser
- [ ] Email finding pipeline for existing contacts
- [ ] NC, SC, GA, MS, AL independent adjusters
- [ ] CatAdjuster.org directory
- [ ] TDI Texas adjusters

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
