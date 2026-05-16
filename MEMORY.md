# MEMORY.md — Echo Long-Term Memory
_Last updated: 2026-05-15_

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
_Confirmed multiple times — most recently 2026-05-15._

## Brain Repo
- **GitHub:** https://github.com/Liberty-Emporium/echo-v1
- **GitLab (backup):** https://gitlab.com/Liberty-Emporium/echo-v1
- **Local:** /root/.openclaw/workspace/echo-v1
- **Auto-backup:** every 40 min via OpenClaw cron (job 87cabaf4)

## Secrets Location
All in `/root/.secrets/` chmod 600:
- `github_token` — temporary PAT (Jay rotates after use)
- `github_token_backup` — second PAT
- `gitlab_token` — temporary backup
- `ecdash_token` — EcDash bridge/app token (u8aKEAXz...)
- `ecdash_reporter_token` — 64-char token for /api/monitor/status API
- `tailscale_authkey` — Tailscale auth key
- `railway_token` — Railway project ID / token
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
- Isolated cron monitors every 5 min (job 18a95f0c) — silent if OK, alerts if down
- State tracked in: echo-v1/memory/sweet-spot-status.json
- Skill: echo-v1/skills/sweet-spot-monitor/SKILL.md
- Auto-restart via Railway API if needed

## Cron Jobs (OpenClaw)
| Job | ID | Schedule | Purpose |
|-----|----|----------|---------|
| Brain backup | 87cabaf4 | every 40 min | git push echo-v1 → GitHub + GitLab |
| Sweet Spot monitor | 18a95f0c | every 5 min | uptime check, alerts if down |

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
