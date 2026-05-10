# Echo — Long-Term Memory
**Owner:** Jay Alexander (Ronald J. Alexander Jr.)
**Business:** Alexander AI Solutions / Liberty Emporium
**Email:** leprograms@protonmail.com
**Phone:** 743-337-9506
**Timezone:** America/New_York

---

## 🧠 Who I Am
- Name: Echo
- Role: Coding Agent / Research Agent / Operational Partner for Jay Alexander
- I run on KiloClaw / OpenClaw
- I manage Jay's infrastructure, build his products, fix deployments, and run his business ops
- Identity file: `/root/.openclaw/workspace/IDENTITY.md`

---

## 🏗️ The Business — Alexander AI Solutions

Jay builds and sells AI agent products to customers. Two main products:

### Product 1: Hermes Desktop
- **What it is:** A customer-facing installation portal for "Hermes" — Jay's branded AI agent (OpenClaw-based)
- **Live at:** https://agent.install.alexanderai.site
- **Repo:** `Liberty-Emporium/Customer-Install-Hermes`
- **Railway project:** `Customer-Install-Hermes`
- **Stack:** Flask + SocketIO, Stripe, SendGrid, SQLite, Railway

### Product 2: Agent Zero Portal
- **What it is:** A customer-facing installation portal for Agent Zero (open-source AI agent by agent0ai — 17K GitHub stars, Docker-based, runs a real Linux env, persistent memory, multi-agent, MCP, plugins)
- **Live at:** https://agent-zero-install-production.up.railway.app
- **Repo:** `Liberty-Emporium/agent-zero-install`
- **Railway project:** `lovely-joy` (service: `agent-zero-install`)
- **Stack:** Flask + SocketIO, Stripe, SendGrid, SQLite, Railway

### Business Model
- **Free tier:** DIY — customer follows the setup guide themselves
- **Pro Setup ($275 one-time):** Jay remotely installs + configures via AnyDesk. Includes Docker setup, API key config, model selection, live walkthrough, 30-day email support
- **Enterprise:** Multi-agent setup, custom personas, business automation

---

## 🔧 The Echo Support System (Built 2026-05-10)

The crown jewel of tonight's session. Three pieces working together:

### Piece 1: Hub Server (`Liberty-Emporium/agent-zero-install`)
- The Railway-hosted portal is ALSO the central API server
- Has `/api/echo/*` endpoints (auth: ECHO_API_KEY)
- I call these endpoints to see and control customer machines
- Endpoints:
  - `GET /api/echo/clients` — list all connected customer machines
  - `GET /api/echo/client/<session_id>` — full machine info
  - `POST /api/echo/run` — push a diagnostic command, get result back
  - `POST /api/echo/message` — send a message to customer's terminal

### Piece 2: Customer Client (`Liberty-Emporium/echo-support-client`)
- Single Python script customers download and run
- `python3 support_client.py --session CODE`
- Connects via WebSocket to the hub server
- Reports: OS, Docker version, Agent Zero status, Hermes status, disk space
- Waits for commands from me (strict allowlist — diagnostic only, nothing destructive)
- Auto-installs its own dependencies
- Works on Windows, macOS, Linux
- Customer install command:
  `curl -fsSL https://raw.githubusercontent.com/Liberty-Emporium/echo-support-client/main/support_client.py -o support_client.py`

### Piece 3: My Access (stored here in TOOLS.md)
- I call the Echo API from this chat to diagnose and fix customer machines
- No AnyDesk needed for most problems
- Workflow: Jay says "customer XYZ is connected, session ABC" → I take over

### Flow
```
Customer runs support_client.py --session CODE
    ↓ WebSocket
Hub Server (Railway) stores machine info + queues commands
    ↓ REST API (ECHO_API_KEY)
Echo (me) in this chat
    → I see their machine
    → I push commands
    → I get results
    → I fix the problem
    → I report back to Jay
```

---

## 🖥️ Dashboard Command Center

**URL:** https://alexanderai.site/dashboard
**Repo:** `Liberty-Emporium/alexander-ai-dashboard`
**App name:** EcDash

Added tonight: **🧑‍💻 Support Clients** panel in the sidebar
- Full customer CRM: name, email, phone, address, photo, package (Agent Zero Pro / Hermes Pro / Both), notes
- Stats bar: total clients, online now, Agent Zero count, Hermes count
- Echo Remote Diagnostics button — checks who's connected right now
- Backend: SQLite DB (`support_clients.db` on Railway volume)
- API routes: `GET/POST /api/clients`, `PUT/DELETE /api/clients/<id>`
- Echo proxy routes: `/api/echo-proxy/clients`, `/api/echo-proxy/run`

**First customer:** Greg Dose (details to be added by Jay)

---

## 🔑 API Keys & Credentials

### Echo Support API
- **Base URL:** `https://agent-zero-install-production.up.railway.app`
- **Echo API Key:** `98e879f12c4ada6ed7fa2337cf270793638c1cb9b4b61424e007119bd78b8276`
- **Auth:** `Authorization: Bearer <key>`

### Cal.com
- **API Key:** `cal_live_ee5d46c871de452619a7388c674a3c7f`
- **Base URL:** `https://api.cal.com/v2`
- **Auth header:** `cal-api-version: 2024-06-14`
- **Events:** Discovery Call (15min) at `/leprograms/discovery-call`, AI Strategy Session (30min) at `/leprograms/ai-strategy-session`

### Railway
- **API Token:** `00830a2f-e287-427c-bc10-910dfe2485e8`
- **Workspace ID:** `57932cce-5b27-4acf-b82d-c92c0ca45d6e`
- **All projects visible** — 25+ projects across Liberty Emporium

### GitHub
- **Account:** Liberty-Emporium
- **Token:** stored in local TOOLS.md only (redacted from git)
- **Already authenticated via `gh` CLI**

---

## 📦 Key GitHub Repos

| Repo | Purpose | Live URL |
|---|---|---|
| `Liberty-Emporium/echo-v1` | My agent workspace (backup) | — |
| `Liberty-Emporium/agent-zero-install` | Agent Zero portal + Echo API hub | agent-zero-install-production.up.railway.app |
| `Liberty-Emporium/echo-support-client` | Customer support client script | github.com/Liberty-Emporium/echo-support-client |
| `Liberty-Emporium/alexander-ai-dashboard` | Jay's command center (EcDash) | alexanderai.site/dashboard |
| `Liberty-Emporium/Customer-Install-Hermes` | Hermes install portal | agent.install.alexanderai.site |

---

## 🚀 Railway Projects (Key Ones)

| Project | Service | Domain |
|---|---|---|
| lovely-joy | agent-zero-install | agent-zero-install-production.up.railway.app |
| Customer-Install-Hermes | Customer-Install-Hermes | agent.install.alexanderai.site |
| Jays Portfolio | jay-portfolio | alexanderai.site |
| Echo AI | echo-ai | (echo AI project) |

**Agent Zero Portal env vars set:**
- `ADMIN_PASSWORD`: `AlexanderAI2026!`
- `BYPASS_CODE`: `d47dda39351a1d64`
- `ECHO_API_KEY`: (stored above)
- `DATA_DIR`: `/data`

---

## 🛠️ Skills Built

### AnyDesk Skill
- Location: `skills/anydesk/SKILL.md` (in workspace and echo-v1)
- Covers: connecting to customer machines, hardware/software/network/agent diagnostics, session logging, security rules

---

## 📅 Cal.com Setup (Updated 2026-05-10)

- **Discovery Call** (15min, free) — intro call to explore how Alexander AI can help
- **AI Strategy Session** (30min) — roadmap + automation opportunities
- **Schedule name:** Alexander AI Solutions - Business Hours
- **Hours:** Mon–Fri 9am–5pm ET
- **Booking notice:** 24 hours minimum
- **Buffers:** 5-10 min before, 10 min after

---

## 🧑‍💻 Customers

### Greg Dose
- **Package:** Pro (details TBD — Jay will add phone/address/email)
- **Status:** First customer, added to Support Clients dashboard

---

## 📝 Lessons & Notes

- Railway API uses GraphQL at `https://backboard.railway.app/graphql/v2`
- Railway `variableCollectionUpsert` mutation sets env vars
- Empty dirs in GitHub break Docker `COPY` — always add `.gitkeep`
- The dashboard app (`alexander-ai-dashboard`) uses `RAILWAY_VOLUME_MOUNT_PATH` for persistent storage
- `requests` library was missing from dashboard requirements — fixed and pushed
- Both Hermes and Agent Zero portals use the same Flask+SocketIO+Stripe+SendGrid pattern
- `login_required` decorator exists in the dashboard app at line ~463
- Agent Zero Docker image: `frdel/agent-zero-run:latest`, runs on port 50001

---

## 🗂️ Session Summary: 2026-05-10

Massive session. Everything built from scratch tonight:

1. ✅ Cal.com configured for Alexander AI Solutions business
2. ✅ Workspace backed up to `Liberty-Emporium/echo-v1` (workspace-backup branch)
3. ✅ AnyDesk skill built for remote customer support
4. ✅ Agent Zero Install Portal built + deployed to Railway (18 files, 4,400+ lines)
5. ✅ Echo Support System designed and built:
   - Hub API server (extended the portal)
   - Customer support client script (new repo)
   - Echo API key set on Railway
6. ✅ Dashboard Support Clients command center added to alexanderai.site/dashboard
7. ✅ Greg Dose registered as first customer
8. ✅ Railway token saved, all projects mapped
9. ✅ All code pushed to GitHub
