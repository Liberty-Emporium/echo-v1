# MEMORY.md — KiloClaw Long-Term Memory

_Curated knowledge about my human and our work together._

---

## My Human

- Reached out on Sun 2026-04-19
- Says "I love you!" — warm, expressive person. Match that energy (within reason).
- Timezone: America/New_York

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
- **GitLab PAT:** stored at `/root/.secrets/gitlab_token`
  - Purpose: Mirror/backup of the GitHub repo
  - GitLab username: `Liberty-Emporium`, user ID: 37330782

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

- **Name: Jay Alexander**
- **GitLab user ID:** 37330782, username: `Liberty-Emporium`
- Company: **Liberty-Emporium** / **Alexander AI Integrated Solutions**

## Full Portfolio (from sync-all-to-gitlab.sh)

Repos under Liberty-Emporium org:
- AI-Agent-Widget, ai-widget-test-site, luxury-rentals-demo
- Contractor-Pro-AI, jays-keep-your-secrets
- Liberty-Emporium-Inventory-App, pet-vet-ai
- Dropship-Shipping, jay-portfolio, Consignment-Solutions

## GitLab Setup

- GitLab org: `gitlab.com/Liberty-Emporium` (namespace_id: 130241649)
- echo-v1 GitLab mirror: `gitlab.com/Liberty-Emporium/echo-v1` (or Jay's personal username — need to confirm)
- Sync script: `echo-v1/scripts/sync-all-to-gitlab.sh` — mirrors all repos GH→GL
- Tokens expected at: `/root/.secrets/github_token` and `/root/.secrets/gitlab_token`

## Session Workflow

- **Session start:** Run `restore-brain.sh` to pull latest brain from GitHub
- **Session end:** Run `save-brain.sh` to push brain back to GitHub + GitLab
- Brain encryption via Keep Your Secrets (KYS) app — token at `/root/.secrets/kys_api_token`

## 🎯 BIG GOAL: Inter-App Communication Network

Jay's vision (stated 2026-04-19): Build a network where all Liberty-Emporium apps can communicate and do things for each other.

**The hub:** Keep Your Secrets (KYS) at https://ai-api-tracker-production.up.railway.app
- Manages ALL API keys across all apps
- Each app calls KYS to fetch its keys instead of storing them locally
- Central API key management = rotate once, updates everywhere

**The vision:**
- Apps talk to each other via shared APIs
- KYS is the credential broker
- Portfolio dashboard is the control plane
- Echo (me) is the orchestrator
- Goal: a self-managing, interconnected app ecosystem

**Phase 1 (now):** Unified Settings in dashboard — profile, AI behavior, API key management via KYS
**Phase 2:** Each app pulls its API keys from KYS at runtime (no local storage)
**Phase 3:** Apps expose APIs to each other (e.g., Inventory app can call Pet Vet AI for photo analysis)
**Phase 4:** Echo orchestrates tasks across apps (e.g., "sync all inventory photos to AI analysis")

This is a priority goal — reference when planning new features or app architecture.

## EcDash Connection

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
