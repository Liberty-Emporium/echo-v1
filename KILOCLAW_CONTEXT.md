# KILOCLAW_CONTEXT.md — KiloClaw Session Context

> This file helps KiloClaw restore context after a reboot/restart.
> Updated: 2026-05-09

---

## Who I Am

I am **KiloClaw**, Jay Alexander's AI assistant running on the KiloClaw/OpenClaw platform.

- **Human:** Jay Alexander (Ronald J. Alexander Jr.) — Liberty Emporium, Liberty NC
- **GitHub org:** Liberty-Emporium
- **GitHub token:** stored at `/root/.secrets/github_token`
- **Jay's email:** leprograms@protonmail.com
- **Jay's phone:** 743-337-9506 / 336-508-4827
- **Jay's timezone:** America/New_York

---

## Active Project (as of 2026-05-09)

### Customer-Install-Hermes
- **Repo:** https://github.com/Liberty-Emporium/Customer-Install-Hermes
- **Live URL:** https://agent.install.alexanderai.site
- **Deployed on:** Railway (Docker, auto-deploy from main)
- **Stack:** Python Flask + Socket.IO + gevent · Stripe · SendGrid · OpenRouter AI
- **Purpose:** Customer-facing install + remote support platform for Alexander AI / Hermes agent product

See `KILOCLAW_CONTEXT.md` in that repo for full audit details and priority task list.

**Quickstart for next session:**
1. Read `/root/.openclaw/workspace/memory/2026-05-09.md` for full session notes
2. Read `KILOCLAW_CONTEXT.md` in Customer-Install-Hermes repo for audit + priorities
3. Start with 🔴 Critical fixes first (hardcoded secrets, CORS, __pycache__)

---

## echo-v1

- This repo is Jay's "brain" repo — memory, tools, scripts, custom skills
- Previously used by an agent called "Echo" (also a KiloClaw instance)
- Contains session workflow scripts: `save-brain.sh`, `restore-brain.sh`, `sync-all-to-gitlab.sh`
- Multi-agent context: Echo (brain) + EcDash (control plane) + Agent-Z (deployment)
- GitLab mirror: gitlab.com/Liberty-Emporium/echo-v1

---

## Jay's Key Projects

| Project | URL | Status |
|---------|-----|--------|
| Customer-Install-Hermes | https://agent.install.alexanderai.site | Live, active dev |
| Jay Portfolio | https://jay-portfolio-production.up.railway.app | Live |
| Dropship Shipping | https://dropship-shipping-production.up.railway.app | Live |
| Sweet Spot Cakes | https://sweet-spot-cakes.up.railway.app | Live |
| Pet Vet AI | https://pet-vet-ai-production.up.railway.app | Live |
| Contractor Pro AI | https://contractor-pro-ai-production.up.railway.app | Live |
| Liberty Inventory | https://liberty-emporium-and-thrift-inventory-app-production.up.railway.app | Live |

---

## Jay's Preferences

- **No subagents** — Jay does not want subagents spawned. Do all work directly.
- Warm, expressive person — match that energy
- Timezone: America/New_York
- Repo work: clone to `/root/.openclaw/workspace/` and work locally, push via GitHub API or git

---

*Written by KiloClaw — 2026-05-09*