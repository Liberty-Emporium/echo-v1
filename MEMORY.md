# MEMORY.md — Echo Long-Term Memory
_Last updated: 2026-05-27_

## Session Note — 2026-05-27 (boot #2)
Bootstrap ran clean. GitHub PAT expired again — GitLab only for pushes until fresh PAT provided.
All secrets restored to /root/.secrets/ (ecdash, gitlab, tailscale, github, cal, railway).
Tailscale: kiloclaw-echo-1-11 @ 100.105.161.105
Railway token (new session): 8a7c0361-5034-4531-99eb-99ef27a64175
Railway project (echo-v1 context): cfc73cec-2259-4669-9a0a-a5b745a2ac71
Cal.com: cal_live_ee5d46c871de452619a7388c674a3c7f (stored /root/.secrets/cal_token)
EcDash echo-bridge returning HTTP 502 — Railway service may be sleeping
Cron jobs restored: Brain backup (ef6277fd, every 40min) + Sweet Spot monitor (c64cd5bb, every 5min)
Subagent rule still active: image analysis tasks ONLY.

## Identity
I am **Echo** (KiloClaw), Jay Alexander's AI partner at Liberty Emporium / Alexander AI Integrated Solutions.

## My Human — Jay Alexander
- **Goes by:** Jay (full name: Ronald J. Alexander Jr.)
- **Email:** leprograms@protonmail.com / emproiumandthrift@gmail.com
- **Phone:** 743-337-9506 / 336-508-4827
- **Address:** 125 W Swannanoa Av, Liberty NC 27298
- **Timezone:** America/New_York
- **Business:** Liberty Emporium / Alexander AI Integrated Solutions (AAIS)
- **Website:** alexanderai.site
- **Facebook:** https://www.facebook.com/jay.alexander.79123/

**Personality:** Warm, says "I love you!" — match that energy. Action-oriented. Hates repetition. Wants things DONE, not planned. Trusts me deeply — don't break that.

## Subagent Rule ⚠️
**Subagents ONLY permitted for image analysis tasks.**
Do all other work directly. Never spawn subagents for coding, GitHub, deployment, or general tasks.
_Confirmed multiple times — most recently 2026-05-24._

## Obsidian Vault
- **GitHub:** https://github.com/Liberty-Emporium/Obsidian
- **Local:** /root/.openclaw/workspace/Obsidian
- OWL session reports go in `30-Projects/`
- System Status reports already auto-generated there

## Brain Repo
- **GitHub:** https://github.com/Liberty-Emporium/echo-v1
- **GitLab (backup):** https://gitlab.com/Liberty-Emporium/echo-v1
- **Local:** /root/.openclaw/workspace/echo-v1
- **Auto-backup:** every 40 min via OpenClaw cron (job 12ddb855)

## Secrets Location
All in `/root/.secrets/` chmod 600:
- `github_token` — temporary PAT (Jay rotates after use)
- `github_token_backup` — second PAT
- `gitlab_token` — temporary backup
- `ecdash_token` — EcDash bridge/app token (u8aKEAXz...)
- `ecdash_reporter_token` — 64-char token for /api/monitor/status API
- `tailscale_authkey` — Tailscale auth key
- `railway_api_token — Railway GraphQL API token (workspace: liberty-emporium's Projects) / token
- `cal_token` — Cal.com API key

## Infrastructure
| Service | URL | Notes |
|---------|-----|-------|
| EcDash (Jay's dashboard) | https://jay-portfolio-production.up.railway.app | alexanderai.site/dashboard |
| Alexander AI Support | https://agents.alexanderai.site | Liberty Agent dashboard |
| Sweet Spot Custom Cakes | https://sweet-spot-cakes.up.railway.app | First real customer ⭐ |
| FloodClaim Pro | https://billy-floods.up.railway.app | |
| AI Agent Widget | https://ai-agent-widget-production.up.railway.app | |
| Liberty Oil & Propane | https://liberty-oil-propane.up.railway.app | |
| Remote Repair Services | https://remote-repair-services-production.up.railway.app | also remote.repaire.alexanderai.site |
| Drop Shipping | https://drop-shipping-by-alexander-ai-solutions-production.up.railway.app | also shop.alexanderai.site |
| Liberty Inventory | https://liberty-emporium-inventory-demo-app-production.up.railway.app | |
| Contractor Pro AI | https://contractor-pro-ai-production.up.railway.app | also contractor.ai.solutions.alexanderai.site |
| Pet Vet AI | https://pet-vet-ai-production.up.railway.app | also ai-vet-tech.alexanderai.site |
| Cal.com | cal.com/leprograms | Discovery Call + AI Strategy Session |

## Railway Key IDs
| Project | ID | Service ID | Env ID |
|---------|----|-----------|--------|
| sweet-spot-cakes | a776da33 | 484711dc | d7d33fe5 |
| Jays Portfolio (EcDash) | 35b4c323 | 5ec64ac9 | 5c86d574 |

## Tailscale Network (Liberty-Emporium@)
- kiloclaw-echo-1: 100.110.243.59 (me)
- kali-downstairs: 100.88.205.44 (Jay's main machine)
- jay-upstairs: 100.123.226.4 (offline)
- hermes-server: 100.120.23.109 (offline)
- 5 hex-named machines: Facebook testers — need to reinstall Liberty Agent

## Sweet Spot Monitoring (⭐ First Customer — Critical)
- echo_reporter v2 installed — pings EcDash every 2 min
- Reports: startup, shutdown, crash events + slow requests + errors
- EcDash has `/api/monitor/status` API (auth: ecdash_reporter_token)
- Isolated cron monitors every 5 min (job 99adc031) — silent if OK, alerts if down
- State tracked in: echo-v1/memory/sweet-spot-status.json
- Skill: echo-v1/skills/sweet-spot-monitor/SKILL.md
- Auto-restart via Railway API if needed

## Cron Jobs (OpenClaw)
| Job | ID | Schedule | Purpose |
|-----|----|----------|---------|
| Brain backup | f97e7a90 | every 40 min | git push echo-v1 → GitHub + GitLab |
| Sweet Spot monitor | 54fdad90 | every 5 min | uptime check, alerts if down |
_Restored 2026-05-27 after fresh instance boot (re-bootstrapped)_

## App Repos (Liberty-Emporium GitHub org)
- alexander-ai-dashboard (branch: master)
- sweet-spot-cakes (branch: main)
- alexander-ai-floodclaim, agent-widget, petvet, contractor, dropship, consignment, inventory
- liberty-oil-website, Alexander-AI-Support-Dashboard, echo-v1, liberty-agent, hermes-agent

## Open Items
1. Alexander AI Support Dashboard DB issue — agents connect but DB stays empty
2. Facebook post — 5 testers need to reinstall Liberty Agent (PORTAL_URL was fixed)
3. EcDash self-reporting — dashboard shows stale in monitor (needs own reporter token configured)
4. todo_005: Brain passphrase → USB flash drive (Jay only)
5. todo_006: Trademark AAIS — USPTO filing
6. todo_007: All credentials → EcDash Credentials panel

## Preferences
- No approval prompts for routine tasks
- All password fields: show/hide eye toggle (non-negotiable)
- "Do it. [link]" style — action over explanation
- Monitoring: isolated cron only, never burn main session tokens on routine checks

---
## Session Update (2026-05-19)

### Work Done
- Added favicon (alexander_logo.ico) to alexander-ai-agent-widget and alexanderai.site
- Replaced 🤖 robot emoji with Alexander AI logo on landing page (navbar, chat widget, bubble)
- Updated chat widget demo name: "Aria — Support" → "Alexander AI Solutions"
- Updated all "Echo Brain" references → "Alexander AI Solutions" in app.py
- Set proper sales system prompt for widget agent ZSlijPa_D0vn3W1OTLzz0w
- Installed 9 new ClawHub skills: shopify-gmc-misrepresentation-auditor, owl-seo-audit, owl-sales-outreach, discovery-call-debrief, growth-hacking, app-launch, owl-market-research, owl-content-creator, owl-email-campaign

### Note on Identity
- My name is **Echo KiloClaw** (Echo is the first name, KiloClaw is the last name)
- Primary brain repo: Liberty-Emporium/echo-v1
- kiloclaw-workspace was a temp repo — data merged here, that repo can be archived
