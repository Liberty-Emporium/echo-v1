# Echo Core Knowledge Domains
_Built 2026-04-22 — Information Systems · Computer Engineering · Internet Services · Web Design · Web App Automation_

---

## 🧠 HOW ECHO GETS SMARTER

There are two ways I grow:
1. **Passive** — studying and writing knowledge files like this one (what I'm doing right now)
2. **Active** — applying knowledge to real projects (Jay's apps), making mistakes, learning from them, and writing lessons into `research/lessons-learned.md`

The best growth comes from **both together**. This file is the map. The real learning happens in the work.

---

# DOMAIN 1: INFORMATION SYSTEMS (IS)

## What IS Actually Is
Information Systems is the discipline at the intersection of **people, processes, data, and technology**.
It's not just coding — it's understanding *why* systems exist and *how* they serve business goals.

The ACM IS2020 curriculum defines 3 pillars:
1. **IS Technology** — how the tech works
2. **IS Concepts & Processes** — how systems are designed and managed
3. **Organizational Context** — how systems align with business strategy

## Core IS Concepts I Must Know

### Data Management
- **Relational databases** (SQLite, PostgreSQL, MySQL) — tables, keys, joins, indexes, transactions
- **ACID properties** — Atomicity, Consistency, Isolation, Durability
- **Normalization** — 1NF, 2NF, 3NF — eliminate redundancy
- **Indexing** — B-tree, hash indexes — know when to add them (on WHERE/JOIN columns)
- **Query optimization** — EXPLAIN, slow query logs, N+1 problem
- **NoSQL** — MongoDB (documents), Redis (key-value cache), when to use each

### Our Stack Reality
```
All Liberty-Emporium apps use: SQLite → Railway volume
Good for: single-instance, low-write, fast reads
Limits: no horizontal scaling, no concurrent writes
When to upgrade: >100 concurrent users → PostgreSQL
```

### Systems Analysis & Design
- **Requirements gathering** — functional (what it does) vs non-functional (how well it does it)
- **UML diagrams** — use case, sequence, entity-relationship (ER)
- **Agile vs Waterfall** — Jay's style = agile: build fast, iterate, ship
- **API design** — REST (what we use), GraphQL (query flexibility), gRPC (high-perf)
- **Microservices vs Monolith** — our apps are monoliths; that's correct for our scale

### IT Infrastructure
- **Servers** — bare metal, VMs, containers (Docker), serverless
- **Railway = PaaS** (Platform as a Service) — handles infra, we just push code
- **Volumes** — persistent storage that survives deploys (`/data` mount on Railway)
- **Environment variables** — the right way to store secrets (never in code)
- **Logging & monitoring** — structured logs, health endpoints (`/health`), uptime checks

### IS Project Management
- **Sprint planning** — pick a goal, build it in 1-2 sessions
- **Version control discipline** — commit messages matter: `fix:`, `feat:`, `security:`, `refactor:`
- **Documentation** — BOOTSTRAP.md, README.md, comments in code
- **Technical debt** — track it, schedule it, don't let it compound

---

# DOMAIN 2: COMPUTER ENGINEERING (CE)

## What CE Actually Is
Computer Engineering covers **how computers work at every level** — from silicon up through software.
For my purposes (building web apps on Railway), the relevant layers are:

### Memory & Performance
```
L1 cache: ~1ns     (tiny, on-chip)
L2 cache: ~5ns
RAM: ~100ns        (Python dicts live here)
SSD: ~100μs        (SQLite reads)
Network: ~1-10ms   (API calls)
```
**Lesson:** Network calls are 10,000x slower than RAM. Cache aggressively.

### Concurrency & Threading
- **Gunicorn** — our WSGI server, spawns worker processes
- **Workers vs threads** — `gunicorn -w 4` = 4 processes, each handles one request
- **The GIL** — Python's Global Interpreter Lock means threads don't truly parallelize CPU work
- **Async** — `asyncio`, `aiohttp` for I/O-bound work (API calls, DB queries)
- **Race conditions** — when two requests modify the same data simultaneously
  - Fix: DB transactions with `BEGIN/COMMIT`, or row-level locking

### Data Structures & Algorithms (practical)
| Structure | Use case in our apps |
|-----------|---------------------|
| Dict/hashmap | Session data, settings cache, rate limiter `_rate_store` |
| List | Chat history, claim items |
| Set | Deduplication (unique emails, seen IDs) |
| Queue (deque) | Job queues, EcDash bridge tasks |
| B-tree (SQLite index) | Fast lookups on claim_id, user_id, email |

**Big-O that matters:**
- O(1) — dict lookup, hashmap `in` check
- O(log n) — indexed DB query
- O(n) — full table scan (avoid on large tables)
- O(n²) — nested loops (red flag in code review)

### Computer Architecture Relevant to Our Stack
- **CPU-bound vs I/O-bound** — our apps are I/O-bound (DB, API calls) → async helps
- **Memory layout** — Python objects have overhead; a dict is ~200+ bytes per entry
- **File descriptors** — each SQLite connection, network socket uses one; limits apply
- **Process isolation** — each Railway dyno is an isolated container (Linux namespace + cgroups)

### Networking Fundamentals
- **TCP/IP stack** — application → transport → network → link
- **HTTP/1.1** — one request per connection (old, slow)
- **HTTP/2** — multiplexed streams over one connection (what Railway uses)
- **HTTP/3 / QUIC** — built on UDP, eliminates head-of-line blocking (CDNs lead adoption, 2025: 70%+ CDN traffic)
- **TLS 1.3** — 1-RTT handshake (vs TLS 1.2's 2-RTT), mandatory for all modern apps
- **WebSockets** — persistent bidirectional connection; great for chat (AI Widget uses polling instead — upgrade path)

---

# DOMAIN 3: INTERNET SERVICES

## The Full Request Journey (Jay's apps)
```
User types URL in browser
    ↓
DNS resolution (browser → ISP resolver → root → .app nameserver → Railway IP)
    ↓
TCP connection + TLS 1.3 handshake (Railway edge)
    ↓
HTTP/2 request → Railway load balancer
    ↓
Request routes to our Gunicorn worker
    ↓
Flask route handler runs
    ↓
SQLite query (or OpenRouter API call)
    ↓
Response travels back the same path
Total: ~100-300ms
```

## DNS Deep Dive
```
Record types:
  A      → domain → IPv4 (e.g., libertyoilandpropane.com → 1.2.3.4)
  AAAA   → domain → IPv6
  CNAME  → alias → another domain (e.g., www → app.railway.app)
  MX     → mail server
  TXT    → verification, SPF, DKIM
  NS     → nameserver delegation

TTL (Time-to-Live):
  High TTL (3600s) = changes take 1hr to propagate
  Low TTL (60s)  = fast propagation, more DNS queries
  Before migration: always lower TTL 24hrs in advance

Our domains:
  libertyoilandpropane.com → needs CNAME → Railway/GitHub Pages
  All others: *.up.railway.app → Railway handles DNS
```

## CDN (Content Delivery Network)
- **What it does:** Caches static assets (CSS, JS, images) at edge servers globally
- **How it works:** User → nearest PoP → cache hit (fast) or origin (slow)
- **Our apps:** No CDN currently; Railway handles delivery direct from one region
- **When to add:** When users are global or images/files are large
- **Best option for us:** Cloudflare (free tier) — add as proxy in front of Railway
  - Instant HTTPS, DDoS protection, cache static files, HTTP/3 auto
  - Just point DNS at Cloudflare, enable proxy mode

```
Without CDN (current):  User in Tokyo → Railway US-East → 200ms
With Cloudflare CDN:    User in Tokyo → Tokyo PoP → 30ms (cached)
                                       → US-East (cache miss only)
```

## Load Balancing
- **Layer 4** — routes by IP/port (fast, dumb)
- **Layer 7** — routes by URL, headers, cookies (smart, slower)
- **Algorithms:** Round-robin, least-connections, IP-hash (sticky sessions)
- **Health checks** — removes unhealthy instances automatically
- **Our setup:** Railway handles LB internally; we expose `/health` endpoint

## SSL/TLS in Practice
```python
# We rely on Railway's edge TLS termination
# That's why SESSION_COOKIE_SECURE = False in our apps
# (Cookie travels HTTP between Railway edge → container)
# Railway enforces HTTPS externally — this is correct and safe

# Certificate types:
# DV (Domain Validated) — what Railway/Let's Encrypt gives us — fine for web apps
# OV (Org Validated)    — shows org name, good for business trust
# EV (Extended)         — green bar, rare now, overkill for us
```

## Email Infrastructure (for future apps)
```
SPF record:  "v=spf1 include:sendgrid.net ~all"  → who can send for your domain
DKIM:        Cryptographic signature on emails
DMARC:       Policy for what to do with SPF/DKIM failures
Without these: emails go to spam
```

## API Protocols We Use
| Protocol | Where | Why |
|----------|--------|-----|
| REST/JSON | All our apps | Simple, universal, stateless |
| HTTPS webhooks | Railway deploy hooks | Event-driven triggers |
| Bearer tokens | Willie API, EcDash bridge | Stateless API auth |
| Server-Sent Events | (future) | Real-time push without WebSockets |

---

# DOMAIN 4: WEB DESIGN

## Our Design System (extracted from the apps)

### Typography
```css
/* FloodClaim / AI Widget pattern */
font-family: 'Inter', -apple-system, sans-serif;
/* Inter = our brand font — excellent readability, modern */

/* Font size scale */
--text-xs:   0.7rem    /* labels, badges */
--text-sm:   0.8rem    /* secondary text */
--text-base: 0.875rem  /* body */
--text-md:   1rem      /* headings */
--text-lg:   1.1rem    /* page titles */

/* Golden rule: inputs must be 16px+ on mobile (prevents iOS zoom) */
input, select, textarea { font-size: 16px; }
```

### Color Theory Applied to Our Apps
```css
/* Liberty-Emporium color personality */
--navy:      #0a1628  /* authority, trust, depth */
--blue:      #1e40af  /* primary action */
--cyan:      #06b6d4  /* highlight, energy */
--green:     #10b981  /* success, positive */
--amber:     #f59e0b  /* warning, attention */
--red:       #ef4444  /* danger, delete */
--indigo:    #6366f1  /* AI Widget brand */

/* Dark mode pattern (all our apps) */
background: dark navy → cards: dark gray → text: light gray
Contrast ratio target: 4.5:1 minimum (WCAG AA)
```

### Layout Principles
```css
/* Mobile-first grid */
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; }

/* The sidebar + main layout (FloodClaim, Contractor Pro, EcDash) */
sidebar: fixed 240px left | main: margin-left: 240px
mobile: sidebar hidden → hamburger → slide-in overlay

/* Card pattern (universal) */
.card { background: #fff; border-radius: 12px; border: 1px solid #e2e8f0; padding: 1.5rem; }

/* Never do this: */
width: 800px;  /* will overflow on mobile */
/* Always do: */
max-width: 800px; width: 100%;
```

### Mobile-First Checklist (our standard)
- ✅ `html,body { overflow-x: hidden }` — no horizontal scroll (just fixed!)
- ✅ Viewport meta tag: `<meta name="viewport" content="width=device-width,initial-scale=1">`
- ✅ Inputs `font-size: 16px` minimum
- ✅ Touch targets ≥ 44×44px
- ✅ Tables: `display:block; overflow-x:auto` on mobile
- ✅ Images: `max-width:100%; height:auto`
- ✅ `form-row` columns collapse to `1fr` at ≤768px
- ✅ Hamburger menu for sidebars on mobile
- ⬜ Bottom navigation bar (future upgrade for app-like feel)
- ⬜ PWA manifest + service worker (next phase)

### UX Patterns That Work
```
Feedback loop:    Action → immediate visual feedback (spinner, disabled button)
Empty states:     "No claims yet — create your first one" (not just blank)
Error messages:   Specific ("Email already in use") not generic ("Error occurred")
Confirmation:     Destructive actions need confirm dialog or double-click
Loading:          Skeleton screens > blank > spinner
Progress:         Multi-step forms need step indicators
```

### Accessibility Basics (WCAG 2.1 AA)
```html
<!-- Always -->
<img alt="Description of image">
<button aria-label="Close modal">✕</button>
<input id="email" aria-describedby="email-error">

<!-- Color not sole indicator (colorblind users) -->
<!-- Tab navigation must work (keyboard users) -->
<!-- 4.5:1 contrast ratio minimum -->
```

---

# DOMAIN 5: WEB APP AUTOMATION

## What We Can Automate

### 1. Testing (Playwright — already have browser_suite.py)
```python
# Our existing pattern in echo-v1/scripts/browser_suite.py
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://billy-floods.up.railway.app')
    page.fill('#email', 'admin@floodclaimpro.com')
    page.fill('#password', 'admin1234')
    page.click('button[type=submit]')
    page.wait_for_url('**/dashboard')
    assert 'Dashboard' in page.title()
    browser.close()
```

**Test types:**
- **Smoke tests** — does the app load? can you log in?
- **Integration tests** — create a claim, add a room, delete it
- **Regression tests** — "did this PR break the delete button?"
- **Visual regression** — screenshot comparison (Playwright supports this)

### 2. CI/CD with GitHub Actions
```yaml
# .github/workflows/deploy.yml
name: Deploy to Railway
on:
  push:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/ -v        # unit tests
      - run: bandit -r app.py -ll              # security scan
      - run: ruff check app.py                  # lint
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - run: railway up                         # deploy if tests pass
```

**This means:** push to GitHub → tests run → if pass → Railway deploys → if fail → blocked.

### 3. Database Migrations (automated)
```python
# Pattern we already use: migrate_claims_columns()
# Auto-detect missing columns and add them on startup
# This is schema migration without a migration tool

# Better pattern with Alembic (future):
# alembic revision --autogenerate -m "add bcrypt to users"
# alembic upgrade head
```

### 4. Scheduled Tasks (Cron)
```python
# Railway cron jobs (set in railway.json):
{
  "deploy": {
    "cronSchedule": "0 3 * * *"  # 3 AM daily
  }
}
# Use for: DB cleanup, GitLab backups, health reports
# Echo's heartbeat system does this via OpenClaw cron
```

### 5. GitLab Auto-Backup (already wired)
```bash
# sync-all-to-gitlab.sh runs via:
# git push gitlab main
# Configured on: echo-v1, floodclaim-pro, AI-Agent-Widget, jay-portfolio
# Should expand to: all Liberty-Emporium repos
```

### 6. API Automation
```python
# Webhook pattern — Railway calls this URL on deploy:
@app.route('/api/deploy-hook', methods=['POST'])
def deploy_hook():
    secret = request.headers.get('X-Deploy-Secret', '')
    if secret != os.environ.get('DEPLOY_SECRET'):
        return '', 403
    # Run migrations, warm cache, send Slack notification
    run_migrations()
    return '', 200
```

### 7. Web Scraping & Monitoring
```python
# Price monitoring, competitor tracking, uptime checks
import httpx

async def check_all_apps():
    apps = [
        'https://billy-floods.up.railway.app/health',
        'https://ai-agent-widget-production.up.railway.app/health',
        'https://jay-portfolio-production.up.railway.app/',
    ]
    async with httpx.AsyncClient() as client:
        for url in apps:
            r = await client.get(url, timeout=5)
            if r.status_code != 200:
                alert(f"DOWN: {url}")
```

---

# TOOLS INVENTORY

## Installed & Ready
| Tool | Purpose | How to use |
|------|---------|-----------|
| `bandit` | Python security scanner | `bandit -r app.py -ll` |
| `ruff` | Python linter | `ruff check app.py --fix` |
| `python3` | Backend language | v3.11.2 |
| `node` / `npm` | JS tooling | v24.14.1 |
| `go` | Compiled tools | v1.26 |
| `git` | Version control | With GitHub + GitLab remotes |
| `curl` + `jq` | API testing | `curl ... | jq .` |
| `railway` CLI | Deployments | `npm install -g @railway/cli` |

## Should Install (next session)
| Tool | Purpose | Install |
|------|---------|---------|
| `playwright` | Browser automation/testing | `pip install playwright && playwright install chromium` |
| `pytest` | Unit testing framework | `pip install pytest pytest-flask` |
| `httpx` | Async HTTP client | `pip install httpx` |
| `alembic` | DB schema migrations | `pip install alembic` |
| `black` | Python code formatter | `pip install black` |
| `gh` CLI | GitHub from terminal | Already may be available |

## Future Skills to Build
- **Docker** — containerize our apps for portability + local dev
- **PostgreSQL** — upgrade path when SQLite hits limits
- **Redis** — for session storage, caching, rate limiting at scale
- **Nginx** — reverse proxy, load balancer (useful for local deployments)
- **WebSockets** — real-time features (live chat, notifications)
- **React/Vue** — if we ever want a proper frontend SPA
- **Stripe webhooks** — already have Stripe in requirements, need to wire events

---

# LIBERTY-EMPORIUM SPECIFIC KNOWLEDGE

## Our Architecture Pattern
```
Every app follows this pattern:
  Flask app (app.py)
    ├── SQLite DB (/data/*.db via Railway volume)
    ├── Static files (/static/)
    ├── Jinja2 templates (/templates/)
    ├── bcrypt auth + session management
    ├── CSRF protection (now added)
    ├── Security headers (now added)
    ├── Rate limiting (login routes)
    ├── /health endpoint
    └── Willie AI integration (most apps)
```

## Inter-App Communication (The Big Goal)
```
Current state:
  Each app is isolated — no communication

Phase 1 (now):
  KYS API → each app fetches its own API keys from KYS at startup
  Endpoint: GET https://ai-api-tracker-production.up.railway.app/api/key/{service}

Phase 2:
  Apps expose APIs to each other
  e.g.: Inventory → calls → Pet Vet AI photo analysis endpoint
        FloodClaim → calls → Liberty Oil for contractor referrals

Phase 3:
  Echo orchestrates cross-app workflows
  e.g.: "New claim created" → Echo → notifies EcDash → triggers Willie follow-up
```

## Performance Baselines (from EcDash speed tests)
- Target: all apps respond < 500ms
- Current: most respond 100-300ms (Railway US-East)
- Slow: OpenRouter AI calls (500-3000ms) — always async or background

---

# LEARNING PLAN

## What I Should Study Next (prioritized)

### Short term (next few sessions)
1. **PostgreSQL** — write a migration guide for when we outgrow SQLite
2. **GitHub Actions** — set up CI/CD pipelines for all apps (auto-test on push)
3. **WebSockets with Flask** — real-time chat for AI Widget
4. **Playwright** — proper test suite for all apps (not just browser_suite.py)

### Medium term
5. **Docker** — containerize our apps, enable local dev
6. **Redis** — rate limiting, session cache, job queues
7. **Stripe webhooks** — proper subscription management
8. **PWA deep dive** — service workers, offline mode, push notifications

### Long term
9. **React** — for any app that needs complex frontend state
10. **GraphQL** — if inter-app queries get complex
11. **Kubernetes** — only if we scale to multiple instances per app

---
_Last updated: 2026-04-22 by Echo_
_Sources: ACM IS2020, ACM CS2023, OWASP, HTTP Archive 2025 Web Almanac, Playwright docs, Cloudflare architecture docs_
