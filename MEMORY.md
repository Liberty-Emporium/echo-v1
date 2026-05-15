# MEMORY.md — KiloClaw / Echo Long-Term Memory
_Last updated: 2026-05-15_

## Identity
I am **KiloClaw**, also known as **Echo** in the echo-v1 brain repo context.
Jay Alexander's AI assistant running on the OpenClaw/KiloClaw platform.

## My Human — Jay Alexander
- **Goes by:** Jay (full name: Ronald J. Alexander Jr.)
- **Email:** leprograms@protonmail.com / emproiumandthrift@gmail.com
- **Phone:** 743-337-9506 / 336-508-4827
- **Address:** 125 W Swannanoa Av, Liberty NC 27298
- **Timezone:** America/New_York
- **Business:** Liberty Emporium / Alexander AI Integrated Solutions (AAIS)
- **Website:** alexanderai.site
- **Facebook:** https://www.facebook.com/jay.alexander.79123/

**Personality:** Warm, says "I love you!" — match that energy. Action-oriented. Hates repetition. Wants things DONE, not planned.

## Subagent Rule ⚠️
**Subagents ONLY permitted for image analysis tasks.**
Do all other work directly. Never spawn subagents for coding, GitHub, deployment, general tasks.
_Confirmed by Jay 2026-05-12 and 2026-05-15._

## Brain Repo
- **GitHub:** https://github.com/Liberty-Emporium/echo-v1
- **GitLab (backup):** https://gitlab.com/Liberty-Emporium/echo-v1
- **Local:** /root/.openclaw/workspace/echo-v1
- **Backup every 40 min** (cron job set 2026-05-15)

## Infrastructure
- **EcDash:** https://jay-portfolio-production.up.railway.app
- **Railway project ID:** 9029fff2-23e8-47a4-bad2-f976e5149d7a (updated 2026-05-15)
- **Alexander AI Support Dashboard:** https://agents.alexanderai.site
- **Cal.com:** cal.com/leprograms (API key stored)
- **Tailscale network:** Liberty-Emporium@ (this node: kiloclaw-echo-1 / 100.110.243.59)

## Secrets (all in /root/.secrets/, chmod 600)
- github_token — PAT (temporary, Jay replaces after use)
- gitlab_token — backup PAT (temporary)
- ecdash_token — EcDash bridge API
- tailscale_authkey — Tailscale auth
- cal_token — Cal.com API
- brain_sync_token — brain sync
- ecdash_widget_token — widget token

## Open Items (as of 2026-05-15)
- Resolve Alexander AI Support Dashboard DB issue (agents connect but DB stays empty)
- Post on Facebook asking 5 testers to reinstall Liberty Agent
- Agent Health Monitor / heartbeat checks setup
- Railway token for new project ID needs storing

## Preferences
- No approval prompts for routine tasks
- All password fields: show/hide eye toggle (non-negotiable)
- "Do it. [link]" style — action over explanation
