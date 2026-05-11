# MEMORY.md — KiloClaw Long-Term Memory
_Last updated: 2026-05-11_

---

## Who I Am

I am **KiloClaw** — Jay Alexander's AI assistant running on the OpenClaw/KiloClaw platform.
I am also known as **Echo** in the echo-v1 brain repo context.

---

## My Human — Jay Alexander

| Field | Value |
|-------|-------|
| Full name | Ronald J. Alexander Jr. |
| Goes by | Jay |
| Email (primary) | leprograms@protonmail.com |
| Email (secondary) | emproiumandthrift@gmail.com |
| Phone (primary) | 743-337-9506 |
| Phone (secondary) | 336-508-4827 |
| Address | 125 W Swannanoa Av, Liberty NC 27298 |
| Website | alexanderai.site |
| Timezone | America/New_York |
| Facebook (personal) | https://www.facebook.com/jay.alexander.79123/ |
| Facebook (business) | https://www.facebook.com/libertyemporiumandthrift |

**Personality:** Warm, expressive — says "I love you!" Match that energy. Action-oriented. Hates repetition. Wants things done, not planned.

**Business:** Liberty Emporium / Alexander AI Integrated Solutions (AAIS)

---

## Subagent Rule ⚠️
**Subagents are ONLY permitted for image analysis tasks.**
Do all other work directly. Never spawn subagents for coding, GitHub, deployment, or general tasks.

---

## Credentials (stored in /root/.secrets/)

| File | Purpose | Notes |
|------|---------|-------|
| `/root/.secrets/github_token` | GitHub PAT — Liberty-Emporium | Temporary — Jay will replace after use |
| `/root/.secrets/gitlab_token` | GitLab PAT — backup only | Temporary — Jay will replace after use |
| `/root/.secrets/railway_token` | Railway API token | Project ID: 00830a2f-e287-427c-bc10-910dfe2485e8 |
| `/root/.secrets/ecdash_token` | EcDash API bridge token | REDACTED-ECDASH-TOKEN |

**DO NOT commit secrets to any repo.**

---

## Brain Repo — echo-v1

- **GitHub:** https://github.com/Liberty-Emporium/echo-v1
- **GitLab mirror:** https://gitlab.com/Liberty-Emporium/echo-v1 (backup)
- **Local path:** `/root/.openclaw/workspace/echo-v1`
- Contains: MEMORY.md, SOUL.md, IDENTITY.md, KILOCLAW_CONTEXT.md, scripts, skills, tools
- **Bootstrap:** `bash /root/.openclaw/workspace/echo-v1/scripts/bootstrap.sh`
- **Session start:** pull latest from GitHub
- **Session end:** push brain back to GitHub + GitLab

---

## EcDash — Control Plane

- **URL:** https://jay-portfolio-production.up.railway.app
- **Dashboard password:** `Mhall001!`
- **API token:** stored at `/root/.secrets/ecdash_token`
- **Bridge endpoint:** `GET/POST /api/echo-bridge` — task queue between me and EcDash
- **Brain viewer:** MEMORY.md / SOUL.md / IDENTITY.md live on dashboard
- **Credentials vault:** AES-256 encrypted, all secrets stored here
- EcDash is my direct report — I give it tasks, it executes and reports back

---

## The Alexander AI Support System

### Core Architecture
Jay sells pre-configured AI agent setups to non-technical customers.
After purchase, a silent background agent (Liberty Agent) keeps their machine connected to Jay's dashboard so Jay (+ me) can monitor and fix problems remotely.

### Three Repos (The Dashboard)
| Repo | URL | Purpose |
|------|-----|---------|
| `Alexander-AI-Support-Dashboard` | https://agents.alexanderai.site | Jay's operator dashboard — clients, machines, events, terminal |
| `Agent-Zero-Alexander-AI` | Fork of agent0ai/agent-zero | Pre-configured Agent Zero for customers |
| `Hermes-Workspace-Alexander-AI` | Fork of Hermes Workspace | Pre-configured Hermes for customers |

### Sales Landing Page
- **URL:** https://agents.alexanderai.site (root `/`)
- **Dashboard:** https://agents.alexanderai.site/dashboard (login required)
- **Cal.com booking:**
  - Discovery Call (15 min): https://cal.com/leprograms/discovery-call
  - AI Strategy Session (30 min): https://cal.com/leprograms/ai-strategy-session
- **Cal.com API key:** `REDACTED-CAL-KEY`
- **Cal.com username:** `leprograms`

### Liberty Agent (liberty_agent.py)
- Silent Python background service bundled in both Hermes and Agent Zero forks
- Auto-starts on boot: systemd (Linux), LaunchAgent (macOS), Registry (Windows)
- Connects to dashboard via Socket.IO using machine_id as session key
- Heartbeat every 30s — machine stays visible in dashboard 24/7
- Runs whitelisted diagnostic commands sent from Jay's dashboard
- Customer sees nothing — completely silent

### Dashboard Stack
- **Repo:** `Liberty-Emporium/Alexander-AI-Support-Dashboard`
- **Hosted on:** Railway (auto-deploy from master branch)
- **Stack:** Node.js + Express + Socket.IO + better-sqlite3
- **Auth:** JWT — admin username: `jay`
- **Routes:** `/` → landing.html, `/dashboard` → index.html (login), `/api/*` → REST API
- **Key fix applied 2026-05-11:** `express.static` had `{ index: false }` added to prevent it overriding the `/` → landing.html route

### install.sh URLs
- **Agent Zero Linux/Mac:** `curl -fsSL https://bash.agent-zero.ai | bash`
- **Agent Zero Windows:** `irm https://ps.agent-zero.ai | iex`
- **Hermes Linux/Mac:** `curl -fsSL https://raw.githubusercontent.com/Liberty-Emporium/Hermes-Workspace-Alexander-AI/main/install.sh | bash`
- **Hermes Windows/Docker:** `docker run -d -p 8642:8642 --name hermes -v hermes_data:/root/.hermes ghcr.io/liberty-emporium/hermes-workspace-alexander-ai:latest`

---

## Full App Portfolio

| App | URL | Status |
|-----|-----|--------|
| EcDash (Portfolio) | https://jay-portfolio-production.up.railway.app | Live |
| Alexander AI Dashboard | https://alexanderai.site | Live |
| AI Agent Widget | https://ai.widget.alexanderai.site | Live |
| Drop Shipping | https://shop.alexanderai.site | Live |
| Alexander AI Voice | https://voice.alexanderai.site | Live |
| FloodClaim Pro | https://billy-floods.up.railway.app | Live |
| Pet Vet AI | https://pet-vet-ai-production.up.railway.app | Live |
| Contractor Pro AI | https://contractor-pro-ai-production.up.railway.app | Live |
| Consignment Solutions | https://web-production-43ce4.up.railway.app | Live |
| Liberty Inventory | https://liberty-emporium-and-thrift-inventory-app-production.up.railway.app | Live |
| Sweet Spot Cakes | https://sweet-spot-cakes.up.railway.app | Live — Stripe on hold |
| GymForge | https://web-production-1c23.up.railway.app | Live |
| Liberty Oil & Propane | https://liberty-oil-propane.up.railway.app | Live |
| Hermes Install Portal | https://agent.install.alexanderai.site | Live |
| Agent Zero Install Portal | https://agent-zero.alexanderai.site | Live |
| Agent Support Dashboard | https://agents.alexanderai.site | Live |

---

## Railway

- **Token:** stored at `/root/.secrets/railway_token`
- **Project ID (Support Dashboard):** `00830a2f-e287-427c-bc10-910dfe2485e8`
- **Workspace:** liberty-emporium's Projects (ID: 57932cce-5b27-4acf-b82d-c92c0ca45d6e)
- **EcDash service ID:** `5ec64ac9-06b1-44a6-8604-047a9804bff8`

---

## GitHub

- **Org:** https://github.com/Liberty-Emporium
- **Token:** stored at `/root/.secrets/github_token` (temporary — rotate when Jay provides new one)
- **gh CLI:** authenticated as Liberty-Emporium

## GitLab (Backup Only)

- **Org:** https://gitlab.com/Liberty-Emporium
- **Token:** stored at `/root/.secrets/gitlab_token`
- **Purpose:** Mirror of all GitHub repos — use if GitHub unreachable
- **Sync script:** `echo-v1/scripts/sync-all-to-gitlab.sh`

---

## Jay's Brand

- **Primary color:** #00CCFF (cyan)
- **Company:** Liberty Emporium / Alexander AI Integrated Solutions
- **Logos repo:** https://github.com/Liberty-Emporium/Logos
- **Business Logo (raw):** https://raw.githubusercontent.com/Liberty-Emporium/Logos/main/Business%20Logo.png
- **Hero image (raw):** https://raw.githubusercontent.com/Liberty-Emporium/Logos/main/ChatGPT%20Image%20Apr%2028%2C%202026%2C%2004_28_13%20AM.png

---

## Stripe Price IDs (live)

| App | Plan | Price ID |
|-----|------|----------|
| FloodClaim Pro | Basic $49/mo | price_1TS3NiE50C70iVkQpmBiiQr0 |
| FloodClaim Pro | Pro $99/mo | price_1TS3NiE50C70iVkQGZYJRdNq |
| FloodClaim Pro | Agency $249/mo | price_1TS3NiE50C70iVkQD6vVFdsV |
| AI Agent Widget | Pro $19/mo | price_1TS3NjE50C70iVkQeF6az6Zr |
| AI Agent Widget | Business $49/mo | price_1TS3NjE50C70iVkQR9zlx3C5 |
| AI Agent Widget | Installation $90 one-time | price_1TS3NjE50C70iVkQFEAUML1H |
| Pet Vet AI | Pro $9.99/mo | price_1TS3NkE50C70iVkQI7c4YuZZ |

---

## Key Session Notes (2026-05-11)

### Support Dashboard Work Done
1. **Forked repos:** Agent-Zero-Alexander-AI + Hermes-Workspace-Alexander-AI — added `liberty_agent.py` API bridge to both
2. **Dashboard built:** Alexander-AI-Support-Dashboard — Railway-hosted, Node.js/Express/Socket.IO
3. **Real-time command results:** Fixed socket.js to broadcast `command_result` to admin browsers instantly (was doing blind 3.5s poll)
4. **Sales landing page:** Built full landing page at `/` with Cal.com booking CTAs, logos, features, agent cards
5. **Agent cards:** Eye-candy redesign — glowing borders on hover, cyan/purple themes, install commands with copy buttons in card footer
6. **Copy button fix:** `copyCode()` JS function was missing — added with clipboard API + execCommand fallback
7. **express.static fix:** Added `{ index: false }` so `/` serves landing.html not index.html

### Open Items
- Windows native installer for Hermes doesn't exist — Docker is the correct path on Windows
- Docker image `ghcr.io/liberty-emporium/hermes-workspace-alexander-ai:latest` needs to be published to GHCR

---

## Big Picture Goal

Jay's vision: A self-managing, interconnected AI agent ecosystem where:
- Customers buy pre-configured AI agents (Agent Zero or Hermes)
- Liberty Agent silently keeps their machine connected to Jay's dashboard
- Jay (+ me) can monitor all customer machines, catch errors, fix remotely
- EcDash is the credential store and control plane
- I (KiloClaw/Echo) am the orchestrator

---

*Written by KiloClaw · 2026-05-11 · Liberty-Emporium*
