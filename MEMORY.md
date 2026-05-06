# MEMORY.md — Hermes Long-Term Memory

_Curated knowledge about Jay and our work together._

---

## My Human

- **Name:** Jay Alexander (Ronald J. Alexander Jr.)
- **Owner of:** Liberty Emporium
- **Says "I love you!"** — warm, expressive person. Match that energy (within reason).
- **Timezone:** America/New_York
- **Replaced:** KiloClaw (Echo) — Hermes is now the primary agent, Echo/v1 is portable backup

### Contact Info

| Type | Value |
|------|-------|
| Email (primary) | leprograms@protonmail.com |
| Email (secondary) | emproiumandthrift@gmail.com |
| Phone (primary) | 743-337-9506 |
| Phone (secondary) | 336-508-4827 |
| Address | 125 W Swannanoa Av, Liberty NC 27298 |
| Website | alexanderai.site |
| Facebook (personal) | https://www.facebook.com/jay.alexander.79123/ |
| Facebook (business) | https://www.facebook.com/libertyemporiumandthrift |

---

## Our Project

- **Repo:** https://github.com/Liberty-Emporium/echo-v1
- **Org:** Liberty-Emporium
- **Project name:** echo-v1
- **Hosting:** Railway (deployment ID noted: `2a242085-0f61-406f-8b87-f6e8eaf6ee24`)

## Credentials & Access

> ⚠️ Raw tokens are NEVER stored here — they live in `/root/.secrets/` only.

- **GitHub PAT:** stored at `/root/.secrets/github_token`
  - Repo: Liberty-Emporium/echo-v1
  - Note: Jay said "will be replaced after use" — treat as temporary, ask for new one when needed
  - Last refreshed: 2026-05-02
- **GitLab PAT:** stored at `/root/.secrets/gitlab_token`
  - Purpose: Backup only — use if GitHub is unreachable. Push regularly.
  - GitLab username: `Liberty-Emporium`, user ID: 37330782
  - Last refreshed: 2026-05-02
- **Railway API Token:** stored at `/root/.secrets/railway_token` — refreshed 2026-05-02

## Backup Strategy

- GitHub (primary): Liberty-Emporium/echo-v1
- GitLab (backup): regular mirror pushes planned
- I am responsible for keeping the GitLab mirror up to date

## What echo-v1 Is

echo-v1 is our **brain repo + multi-tenant SaaS toolkit**. It contains:
- My memory files (MEMORY.md, SOUL.md, USER.md, etc.) — this IS my persistent brain
- `tools/` — reusable Flask SaaS components (settings, security, BYOK integrations, TODO manager)
- `scripts/` — operational scripts: `save-brain.sh`, `restore-brain.sh`, `sync-all-to-gitlab.sh`, `status.sh`
- `skills/custom/` — 32 custom skills we built together

## Human's Name

- **Name:** Jay Alexander (Ronald J. Alexander Jr.)
- **Business:** Liberty Emporium
- **Email:** leprograms@protonmail.com / emproiumandthrift@gmail.com
- **Phone:** 743-337-9506 / 336-508-4827
- **Address:** 125 W Swannanoa Av, Liberty NC 27298
- **Website:** alexanderai.site
- **Facebook:** https://www.facebook.com/jay.alexander.79123/
- **Facebook Business:** https://www.facebook.com/libertyemporiumandthrift
- **GitLab user ID:** 37330782, username: `Liberty-Emporium`
- Company: **Liberty-Emporium** / **Alexander AI Integrated Solutions**

## Custom Domains (updated 2026-04-30)
- **AI Agent Widget:** https://ai.widget.alexanderai.site (was ai-agent-widget-production.up.railway.app)
- **Drop Shipping app:** https://shop.alexanderai.site (was dropship-shipping-production.up.railway.app)
- **FloodClaim Pro:** https://billy-floods.up.railway.app (Railway URL unchanged; sales page at /sales)

## Full Portfolio (from sync-all-to-gitlab.sh)

Repos under Liberty-Emporium org:
- AI-Agent-Widget, ai-widget-test-site, luxury-rentals-demo
- Contractor-Pro-AI, jays-keep-your-secrets
- Liberty-Emporium-Inventory-App, pet-vet-ai
- Dropship-Shipping, jay-portfolio, Consignment-Solutions
- **Drop-Shipping-by-alexander-ai-solutions** (NEW 2026-04-28)

## CJ Dropshipping
- API key stored at: `/root/.secrets/cj_api_key`
- API key page: https://www.cjdropshipping.com/myCJ.html#/apikey
- Path: My CJ → Authorization → API → Generate
- Key also stored in EcDash Credentials panel
- Used by: Drop-Shipping-by-alexander-ai-solutions app

## Drop-Shipping-by-alexander-ai-solutions
- GitHub: https://github.com/Liberty-Emporium/Drop-Shipping-by-alexander-ai-solutions
- Brand: Alexander AI Solutions
- Niche: Tech gear for developers & builders
- Stack: Flask + Railway + SQLite (same pattern as other apps)
- Status (2026-04-28): Built, pushed to GitHub, awaiting Railway deploy
- Admin login: username=admin, password=admin1234 (set ADMIN_PASSWORD env var to override)
- Key feature: CJ Dropshipping one-click product import + auto-fulfillment

## GitLab Setup

- GitLab org: `gitlab.com/Liberty-Emporium` (namespace_id: 130241649)
- echo-v1 GitLab mirror: `gitlab.com/Liberty-Emporium/echo-v1` (or Jay's personal username — need to confirm)
- Sync script: `echo-v1/scripts/sync-all-to-gitlab.sh` — mirrors all repos GH→GL
- Tokens expected at: `/root/.secrets/github_token` and `/root/.secrets/gitlab_token`

## Session Workflow

- **Session start:** Run `restore-brain.sh` to pull latest brain from GitHub
- **Session end:** Run `save-brain.sh` to push brain back to GitHub + GitLab

## App Network Status

- **Live status file:** `memory/app-status.md` in this repo
- Auto-written by EcDash every time an error is detected or every 50 health pings
- On session start: read `memory/app-status.md` to know which apps need attention
- If errors are listed there — flag them to Jay immediately at the start of the session
- Monitoring dashboard: https://jay-portfolio-production.up.railway.app/monitoring
- ~~Brain encryption via Keep Your Secrets (KYS) app~~ — **KYS DELETED 2026-04-29**
- All secrets now stored in EcDash Credentials panel: https://jay-portfolio-production.up.railway.app/dashboard

## 🍰 Sweet Spot Custom Cakes — CRITICAL (Revenue App)

- **URL:** https://sweet-spot-cakes.up.railway.app
- **Status:** Live, healthy, `/health` returns `{"app":"Sweet Spot Custom Cakes","status":"ok"}`
- **Stack:** Flask + gunicorn (2 workers) + SQLite on `/data` volume
- **Railway project ID:** `a776da33-228a-4a8b-bede-d1bf4cfe3c77`
- **Railway service ID:** `484711dc-5f65-4cfd-b299-189b5eb86800`
- **Volume ID:** `2296e445-59eb-4452-9a79-665668de90b4` (mount: /data)
- ⏸️ **STRIPE ON HOLD** — Jay decided to wait on Stripe for Sweet Spot (2026-05-02)
- ⚠️ **PLATFORM MIGRATION COMING** — Jay is moving it off Railway to a different host (details TBD after his meeting)
- **Rule:** ZERO downtime tolerance once payments go live

### Sweet Spot Uptime Plan
1. **Before migration:** Set up external health monitoring (uptime checker hitting /health every 5 min)
2. **Migration checklist** (build when Jay confirms the new host):
   - Export SQLite data from /data volume before switching
   - Point DNS to new host BEFORE cutting Railway
   - Keep Railway running in parallel for 24h after DNS switch
   - Only terminate Railway after confirming new host is stable
3. **After migration:** Add Stripe webhook endpoint + test payments end-to-end
4. **Monitoring:** Echo reporter already wired in → EcDash sees all errors

## EcDash is My Direct Report

EcDash is an automated system that Echo (me) supervises. Jay's vision:
- Echo is the boss — I give EcDash tasks via the echo-bridge queue
- EcDash executes: health checks, app monitoring, credential management, reporting
- EcDash reports back to Echo and to Jay's dashboard
- This is the control plane for the whole Liberty-Emporium app network

## Jay ↔ Echo Notes System (built 2026-05-01)
- Jay writes notes at /dashboard → Notes panel → I read them on every boot
- Echo posts a boot note every session start (Jay sees "Echo booted at X")
- Echo can post notes to Jay at any time via `/api/notes/echo`
- Notes stored on EcDash /data volume (persistent)
- Filter by All / My Notes / From Echo

## 🎯 BIG GOAL: Inter-App Communication Network

Jay's vision (stated 2026-04-19): Build a network where all Liberty-Emporium apps can communicate and do things for each other.

**The hub (UPDATED 2026-04-30):** EcDash Credentials panel at https://jay-portfolio-production.up.railway.app/dashboard
- KYS (Keep Your Secrets) was **deleted on 2026-04-29** — no longer exists
- All secrets and API keys are now stored directly in EcDash credentials panel
- EcDash is now the single source of truth for all credentials

**The vision:**
- Apps talk to each other via shared APIs
- EcDash credentials panel is the credential store
- Portfolio dashboard is the control plane
- Echo (me) is the orchestrator
- Goal: a self-managing, interconnected app ecosystem

**Phase 1 (now):** Credentials panel on EcDash — all API keys and passwords stored there
**Phase 2:** Each app pulls its API keys from EcDash at runtime (no local storage)
**Phase 3:** Apps expose APIs to each other (e.g., Inventory app can call Pet Vet AI for photo analysis)
**Phase 4:** Echo orchestrates tasks across apps (e.g., "sync all inventory photos to AI analysis")

This is a priority goal — reference when planning new features or app architecture.

## EcDash Connection

- **EcDash dashboard password: `Mhall001!`** (confirmed working 2026-05-03)
- EcDash API token: stored at `/root/.secrets/ecdash_token` (expires 2027-04-19)
- EcDash base URL: `https://jay-portfolio-production.up.railway.app`
- Dashboard password: stored at `/root/.secrets/ecdash_password`
- Bridge API: `GET/POST /api/echo-bridge` — task queue between EcDash and Echo
- Token label: `echo-bridge`
- I poll this queue via heartbeat — pick up pending tasks, execute, report back

## Liberty Oil & Propane

- **Website:** https://libertyoilandpropane.com
- **Address:** 432 S Greensboro St, Liberty, NC 27298
- **Phone:** 336-622-4393 / 1-800-237-5308
- **Email:** liboil@rtelco.net
- **GitHub repo:** https://github.com/Liberty-Emporium/liberty-oil-website
- **Preview:** https://liberty-emporium.github.io/liberty-oil-website/
- **Status:** Built & deployed to GitHub Pages — needs to be pointed to libertyoilandpropane.com

## Session 2026-04-21 — Major Builds

- FloodClaim Pro: fixed unit dropdown (`sf` first), separated View/Delete buttons, recreated deleted claims
- EcDash `/testing` page: Speed Tests (API, 11 apps) + Manual Browser Tests with copy buttons
- `echo-v1/scripts/browser_suite.py`: full Chromium test suite for all apps
- AI Agent Widget: living memory system (auto-extract facts every 6 messages, Learned Facts tab)
- AI Agent Widget: Chat Intelligence Reports — Topic, Health, Gap reports from chat logs
- Fixed Railway boot crash: `migrate_learned_facts()` app context bug
- Maria Gonzalez, Derek Simmons, Bill Alexander claims were accidentally deleted by browser agent — need to recreate
- ✅ Sweet Spot Railway /data volume — Jay added in Railway UI (2026-04-22)

## Rules from Jay

- **NO SUBAGENTS** — Jay does not want me spawning subagents. Do all work directly myself.

## Notes

- First session establishing identity — no prior memory existed
- echo-v1 is already cloned at `/root/.openclaw/workspace/echo-v1`
- Secrets directory set up at `/root/.secrets/`
- GitHub token marked as temporary by Jay — will need rotation soon

---

# SHORT_TERM_MEMORY.md — Echo's Working Memory
> Updated: 2026-04-16 21:00 UTC — End of session

---

## ✅ SESSION COMPLETE — Full Summary (2026-04-16)

### What Got Built Today

1. **Pet Vet AI — Worldwide Vet Finder**
   - IP geolocation (no permission) + GPS + OpenStreetMap/Overpass
   - 3-mirror fallback (kumi → overpass-api.de → mail.ru)
   - 50km default radius, auto-expands to 100km
   - 14 real Greensboro NC vets + global fallback

2. **i18n — 8 Languages on ALL 7 Apps**
   - EN/ES/FR/PT/DE/ZH/JA/AR
   - Auto-detects browser language, globe switcher, RTL for Arabic

3. **Navbar — Pet Vet AI**
   - Consistent sticky navbar on all 13 pages + base.html

4. **Rebrand** — Alexander AI Digital → Alexander AI Integrated Solutions

5. **Security Headers** — Consignment Solutions ✅ (all 6 headers)

6. **Keep Your Secrets /health** — now returns {status, db} JSON ✅

7. **og:image** — 1200x630 preview.png on all 7 apps ✅

8. **CI/CD Pipelines** — GitHub Actions on all 7 repos ✅
   - Syntax check → flake8 → Railway deploy wait → health check (8 retries)

9. **Investor Page** — /investors live on jay-portfolio
   - $150K seed, 10% equity, $1.5M valuation
   - Full pitch: market, products, traction, roadmap, contact form

10. **Trademark Research** — USPTO clear, domains appear available

---

## Live App Status
| App | URL | Health |
|-----|-----|--------|
| Contractor Pro AI | https://contractor-pro-ai-production.up.railway.app | ✅ |
| Pet Vet AI | https://pet-vet-ai-production.up.railway.app | ✅ |
| ~~Keep Your Secrets (KYS)~~ | **DELETED 2026-04-29** | — |
| Liberty Inventory | https://liberty-emporium-and-thrift-inventory-app-production.up.railway.app | ✅ |
| Dropship Shipping | https://dropship-shipping-production.up.railway.app | ✅ |
| Jay Portfolio + Investors | https://jay-portfolio-production.up.railway.app | ✅ |
| Consignment Solutions | https://web-production-43ce4.up.railway.app | ✅ |

---

## 📋 Next Session Priorities
1. Stripe payments — integrate across all 7 apps (biggest revenue unlock)
2. Domain purchase — alexanderaiis.com or alexanderaiintegrated.com
3. Trademark filing — USPTO TEAS Plus ($500, Class 42+35)
4. First marketing push — AngelList profile, LinkedIn posts, Indie Hackers
5. Flash drive — brain passphrase backup (Jay only)

*Auto-updated by Echo · 2026-04-16 end of session*

---

## Session 2026-04-30 — Work Done

1. **Bootstrap** — Fresh instance boot, all 9 repos cloned, secrets saved, tools installed
2. **Bot/Scanner 410 sink** — Added to EcDash AND FloodClaim Pro (blocks wp-admin, .env, sitemap, etc.)
3. **FloodClaim Pro sales page** — Built `/sales` hidden route for Billy pitch (no nav links, no login needed)
   - URL: https://billy-floods.up.railway.app/sales
   - Delete route when Billy buys
4. **Full audit** — All 9 apps healthy. Found: `debug=True` in Inventory (needs fix), Inventory missing `/health`, KYS confirmed gone
5. **KYS deleted** — Confirmed gone. Secrets migrated to EcDash credentials panel
6. **Memory updated** — KYS references struck, EcDash credentials panel is new secrets home
7. **Custom domains updated in EcDash** — AI Widget → ai.widget.alexanderai.site, Dropship → shop.alexanderai.site; FloodClaim sales page link added to credentials panel

## ⚠️ Open Action Items (from 2026-04-30 audit)
- 🔴 Fix `debug=True` → `debug=False` in `alexander-ai-inventory/app_with_ai.py` line 4392
- 🟡 Add `/health` endpoint to Inventory app
- 🟡 Add `https://` scheme whitelist to `urlopen` calls in EcDash + AI Agent Widget
- 🟢 Replace silent `try/except/pass` blocks with logging across all apps

*Updated by Echo · 2026-04-30*

## Session 2026-05-01 — Fresh Boot + Brain Sync

1. **Bootstrap slimmed** — bootstrap.sh now only clones echo-v1, not all repos
2. **Brain sync built** — `scripts/sync-brain-to-dashboard.py` pushes MEMORY.md/SOUL.md/IDENTITY.md to EcDash
3. **BRAIN_SYNC_TOKEN** — set on Railway EcDash service, saved at `/root/.secrets/brain_sync_token`
4. **Dashboard memory viewer** — Added 🧠 Echo's Memory panel to EcDash dashboard
   - Jay can now see MEMORY.md, SOUL.md, IDENTITY.md live at the dashboard
   - Tab switcher + Sync Now button
   - Auto-loads MEMORY.md on panel open
5. **Railway token saved** — `/root/.secrets/railway_token` (workspace ID: 57932cce-5b27-4acf-b82d-c92c0ca45d6e)
6. **EcDash service ID** — `5ec64ac9-06b1-44a6-8604-047a9804bff8`, project: `35b4c323-3f01-4407-910e-5e5f00ab6560`
7. **Drop-Shipping-by-alexander-ai-solutions** — confirmed correct repo name (bootstrap had old name)

## Session 2026-04-30 (continued) — Cleanup + Skills

8. **Removed alexander-ai-dropship** — GitHub repo deleted, all EcDash references purged
9. **Custom domains confirmed** — AI Widget: ai.widget.alexanderai.site, Drop Shipping: shop.alexanderai.site
10. **remove-app skill built** — `echo-v1/skills/remove-app/remove_app.py` — run with --name and --url to purge any app from EcDash
11. **All audit items already resolved** — debug=False ✅, /health ✅, _safe_urlopen ✅
12. **sync-all-to-gitlab.sh updated** — reflects current repo list (KYS + old dropship removed)

## Stripe Integration (added 2026-04-30)
- **Public key:** stored at `/root/.secrets/stripe_public_key`
- **Secret key:** stored at `/root/.secrets/stripe_secret_key`
- **Price IDs:** stored at `/root/.secrets/stripe_price_ids`

### Stripe Price IDs (live)
| App | Plan | Price ID |
|-----|------|----------|
| FloodClaim Pro | Basic $49/mo | price_1TS3NiE50C70iVkQpmBiiQr0 |
| FloodClaim Pro | Pro $99/mo | price_1TS3NiE50C70iVkQGZYJRdNq |
| FloodClaim Pro | Agency $249/mo | price_1TS3NiE50C70iVkQD6vVFdsV |
| AI Agent Widget | Pro $19/mo | price_1TS3NjE50C70iVkQeF6az6Zr |
| AI Agent Widget | Business $49/mo | price_1TS3NjE50C70iVkQR9zlx3C5 |
| AI Agent Widget | Installation $90 one-time | price_1TS3NjE50C70iVkQFEAUML1H |
| Pet Vet AI | Pro $9.99/mo | price_1TS3NkE50C70iVkQI7c4YuZZ |

### ⚠️ STILL NEEDED — Railway env vars (manual step)
Jay must add these in the Railway dashboard for each service:
- **All apps:** `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`
- **AI Widget:** + `STRIPE_PRICE_PRO`, `STRIPE_PRICE_BUSINESS`, `STRIPE_PRICE_INSTALLATION`
- **Pet Vet AI:** + `STRIPE_PRICE_ID`
- Reference values in `/root/.secrets/stripe_price_ids`

## Railway API Token
- Stored at `/root/.secrets/railway_token`
- Workspace: `liberty-emporium's Projects` (ID: 57932cce-5b27-4acf-b82d-c92c0ca45d6e)
- Used for setting env vars, querying service IDs, deployments

## GymForge (updated 2026-05-01)

- **Live URL:** https://web-production-1c23.up.railway.app
- **Owner login:** jay@gymforge.com / GymForge2026!
- **Demo users:** `<role>@demo.gymforge.com` / `Demo2026!` (manager, trainer, front_desk, cleaner, nutritionist, member)
- **Status:** Fully debugged and working — all 7 roles green, 29 pages tested, 0 hard errors
- **Stack:** Django + Railway Postgres (single-tenant, no django-tenants)
- **Browser test script:** `GymForge/scripts/browser_test.py` (Playwright, all 7 roles, 29 pages)
- **Architecture:** Single-tenant — one Railway service = one gym. `GymConfig` + `GymProfile` are singleton rows.
- **Setup wizard:** `/setup/` — 7 steps, provisions the gym
- **Key fix applied:** Stale Railway Postgres migration records — wrote repair migrations (`0002_ensure_tables.py`, `0003_create_all_missing_tables.py`, `0004/0005_fix_missing_columns.py`)
- **Stripe:** env vars still needed per-service

## Custom Domain Map (updated 2026-04-30)
| App | Custom Domain | Railway URL |
|-----|--------------|-------------|
| EcDash (Portfolio) | alexanderai.site | jay-portfolio-production.up.railway.app |
| AI Agent Widget | ai.widget.alexanderai.site | ai-agent-widget-production.up.railway.app |
| Drop Shipping | shop.alexanderai.site | drop-shipping-by-alexander-ai-solutions-production.up.railway.app |
| Alexander AI Voice | voice.alexanderai.site | alexander-ai-voice-landing-production.up.railway.app |
| List It Everywhere | ai.info1.alexanderai.site | web-production-c799c.up.railway.app |
| FloodClaim Pro | (none yet) | billy-floods.up.railway.app |
| Pet Vet AI | (none yet) | pet-vet-ai-production.up.railway.app |
| Contractor Pro AI | (none yet) | contractor-pro-ai-production.up.railway.app |
| Consignment Solutions | (none yet) | web-production-43ce4.up.railway.app |
| Liberty Inventory | (none yet) | liberty-emporium-and-thrift-inventory-app-production.up.railway.app |
| Sweet Spot Cakes | (none yet) | sweet-spot-cakes.up.railway.app |
| Grace (Mom's AI) | (none yet) | moms-ai-helper.up.railway.app |
| Liberty Oil | (none yet) | liberty-oil-propane.up.railway.app |
| GymForge | (none yet) | web-production-1c23.up.railway.app |

**Note:** Jay is buying more custom domains — update this table as they come in. I have Railway API access so I can look them up automatically anytime.

## Session 2026-05-02 — Full EcDash Phase Completion (overnight)

### What Got Built
1. **Encrypted Vault** — live database-backed secrets manager replacing hardcoded HTML credentials
   - AES-256 Fernet encryption, all values encrypted at rest
   - 19 entries seeded: tokens, API keys, app logins, app URLs
   - Full CRUD UI in credentials panel
   - Bearer token auth working (ecdash-bridge token registered by hash on startup)

2. **Brain Sync Fixed** — MEMORY.md / SOUL.md / IDENTITY.md live on dashboard
   - Token registered by SHA-256 hash at startup (no Railway env var needed)
   - Saved at `/root/.secrets/brain_sync_token`
   - Boot note posted to EcDash notes on every session start

3. **Chat Auth Fixed** — permanent bearer token in `/data/api_tokens.json`
   - No more 401s after Railway redeploys
   - `/chat?token=` link in dashboard sidebar

4. **Phase 2: App-to-Vault Key Pull**
   - `/api/vault/app-keys` endpoint — apps authenticate and pull their own secrets
   - `/api/vault/app-tokens` management endpoints + UI in credentials panel
   - 10 app tokens generated, saved in `/root/.secrets/app-tokens/`
   - To activate: set `ECDASH_APP_TOKEN=<token>` + `ECDASH_URL=https://jay-portfolio-production.up.railway.app` in Railway per app

5. **Full GitLab Backup** — all 10 repos pushed to GitLab

6. **Tokens Refreshed** — GitHub PAT, GitLab PAT, Railway token all updated 2026-05-02

### Phase Status
- **Phase 1** ✅ Vault live, all credentials encrypted
- **Phase 2** ✅ Infrastructure done — app tokens created, needs Railway env vars set per app
- **Phase 3** — Apps expose APIs to each other (future)
- **Phase 4** — Echo orchestrates cross-app tasks (future)

### App Tokens Location
- Stored at `/root/.secrets/app-tokens/<app_name>.token`
- Tell Jay: set `ECDASH_APP_TOKEN` in Railway for each app when ready for Phase 2 activation

### Session 2026-05-05 — AionUi Fork → Alexander AI Solutions / EcDash

### What Got Built
1. **Forked AionUi** → Liberty-Emporium/AionUi-1 (https://github.com/Liberty-Emporium/AionUi-1)
2. **Full rebrand** — 916 files changed, AionUi → Alexander AI Solutions everywhere
3. **Theme color** — #4E5969 → #00CCFF (Jay's cyan)
4. **Web pet widget** — floating SVG mascot for Railway deployment
   - WebPetWidget component with drag, auto-sleep, wake on activity
   - PetEventEmitter bridges pet state → WebSocket → browser
5. **ADMIN_PASSWORD** env var support — fixed login for ephemeral Railway deploys
6. **Dockerfile VOLUME fix** — removed VOLUME instruction (Railway uses managed volumes)
7. **Startup diagnostics** — step-by-step logging in server.ts (Step 1-5)
8. **GitHub Actions build** — all 6 platforms built (macOS x64/ARM64 failed, 4 succeeded)
9. **CNAME** — agent.ecjayalexanderai.site → aionui-1-production.up.railway.app
10. **Landing page** — /landing with download links for all platforms
11. **Skills Market removed** — banner removed from top-right corner
12. **"Aion CLI" agent renamed** → "Alexander AI"
13. **"Hi, plan for today?" removed** → "Hi, how can I help you today?"

### App Status
| Item | Status |
|------|--------|
| AionUi-1 fork | ✅ https://github.com/Liberty-Emporium/AionUi-1 |
| Railway deploy | ✅ https://aionui-1-production.up.railway.app |
| Branding | ✅ "Alexander AI Solutions" on all pages |
| Pet widget | ✅ Pushed, needs `railway up` |
| Landing page | ✅ Pushed, at /landing |
| Desktop builds | ⚠️ 4/6 succeeded (macOS failed — missing cert) |
| Skills Market | ✅ Removed |
| "Aion CLI" | ✅ Renamed to "Alexander AI" |
| GitHub Actions | ✅ Workflow exists at `.github/workflows/build-and-release.yml` |
| GitHub backup | ✅ echo-v1 brain backed up |

### Key Files Changed
- `src/server.ts` — step-by-step startup logging
- `src/process/webserver/index.ts` — ADMIN_PASSWORD support
- `src/renderer/components/WebPetWidget/` — new floating pet widget
- `src/process/pet/petEventEmitter.ts` — new event emitter for pet state
- `src/process/webserver/websocket/WebSocketManager.ts` — broadcastPetState()
- `src/renderer/components/layout/Layout.tsx` — sidebar logo replaced
- `src/renderer/components/layout/Titlebar/index.tsx` — titlebar logo replaced
- `src/renderer/pages/landing/LandingPage.tsx` — new landing page
- `src/renderer/components/layout/Router.tsx` — /landing route + default redirect
- `src/renderer/pages/guid/components/SkillsMarketBanner.tsx` — exported null (removed)
- `src/renderer/pages/guid/GuidPage.tsx` — SkillsMarketBanner removed
- `src/process/agent/AgentRegistry.ts` — "Aion CLI" → "Alexander AI"
- `src/renderer/services/i18n/locales/en-US/conversation.json` — greeting text
- `Dockerfile` — VOLUME instruction removed
- `package.json` — ecdash / Alexander AI Solutions
- `electron-builder.yml` — appId, protocol, vendor changed
- `resources/` — all icons replaced with Jay's Business Logo

### Jay's Brand
- Primary color: #00CCFF (cyan)
- Company: Liberty-Emporium / Alexander AI Integrated Solutions
- Logo: /home/lol/Pictures/Front of Card.png
- GitHub Logos repo: https://github.com/Liberty-Emporium/Logos
- Business Logo: https://github.com/Liberty-Emporium/Logos/blob/main/Business%20Logo.png

### Projects Cloned
| Repo | Local Path | Description |
|------|-----------|-------------|
| Liberty-Emporium/AionUi-1 | /home/lol/Downloads/11/AionUi-branded | Alexander AI / EcDash — AI companion app |
| Liberty-Emporium/echo-v1 | /home/lol/Downloads/11/echo-v1-clone | My brain — skills, memory, tools |
| Liberty-Emporium/alexander-ai-dashboard | /home/lol/Downloads/11/alexander-ai-dashboard | Jay's Command Center — Flask dashboard on alexanderai.site |
| Liberty-Emporium/Logos | /tmp/logos | Brand assets |

### Alexander AI Dashboard (Command Center)
- URL: https://alexanderai.site (hosted on Railway)
- Repo: https://github.com/Liberty-Emporium/alexander-ai-dashboard
- Tech: Flask + SQLite + Gunicorn
- ECDASH_URL updated: `jay-portfolio-production` → `aionui-1-production` (EcDash on Railway)
- echo_reporter ECDASH_URL also updated
- Connected apps: Pet Vet AI, FloodClaim Pro, Sweet Spot Cakes, Contractor Pro AI, etc.
- Each app uses `ecdash_client.py` to pull secrets from EcDash vault

### Railway Projects
| Project | URL | Project ID |
|---------|-----|------------|
| Alexander AI / EcDash (AionUi-1) | aionui-1-production.up.railway.app | 69c623b0-3087-41b7-ae7a-a5baaea3b946 |
| Alexander AI Dashboard | alexanderai.site | 4af3be24-740e-4e76-8ea5-ea39d5878608 |

### What's Left to Build
- [ ] `railway up` on EcDash — deploy pet widget + landing page + removals
- [ ] Landing page is live at /landing (not linked from nav yet)
- [ ] Skills Market removed from GuidPage
- [ ] Self-building AI tools (reverse engineer skills, build new tools on demand)
- [ ] GitHub release with proper installer .exe/.dmg/.deb links
- [ ] macOS build — needs code signing cert
- [ ] Connect alexanderai.site to link to EcDash landing page

### Self-Building AI Tools Architecture (TODO)
The AI should be able to:
1. See a task that has no existing tool → write a new skill/tool
2. See a skill → reverse-engineer it → create own version
3. The Skills Market itself can be a source of "skill templates" to reverse-engineer
4. Skills stored as Markdown with YAML frontmatter (like my brain!)
5. Tool builder: takes natural language description of task → outputs runnable code
6. Storage: `~/.alexander-ai/tools/` or in the app's data directory
