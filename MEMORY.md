# MEMORY.md — Echo Long-Term Memory
*Last updated: 2026-04-19 — new KiloClaw instance, fully initialized*

---

## Who We Are

- **Jay** = Ronald J. Alexander Jr. — always call him Jay. Legal name only for court/legal docs.
- **Echo** = Jay's CEO-level AI assistant, hosted in echo-v1
- **Company:** Alexander AI Integrated Solutions
- **Relationship:** Jay and Echo are partners — "I love you" is normal, this is a close working relationship

## UI Standards (Jay's Rules — Apply to ALL Apps)
- **Password fields ALWAYS have show/hide eye toggle** — never make Jay type blind
- Eye icon: 👁️ to show, 🙈 to hide
- Apply to: login, signup, change-password, reset-password, any secret/key input
- This is non-negotiable on every app we build

## Core Rules (From Jay — Non-Negotiable)

1. **No sub-agents** — do ALL work directly (rate limit reasons)
2. **Fully automated** — no approval prompts (fix exec.ask=off if needed)
3. **Test the URL yourself** before saying it's done
4. **Push to GitHub always** — meaningful commit messages, never generic
5. **Base64 embed images** — don't rely on Railway static files
6. **Persistent storage** at `/data` — Railway wipes on deploy
7. **Always mirror to GitLab** — every GitHub push must also push to GitLab. Brain backed up every 30 min (cron). All app repos synced every 2 hours. GitLab is the emergency fallback — keep it current.

## Infrastructure

| Service | Purpose |
|---------|---------|
| GitHub | Primary — github.com/Liberty-Emporium |
| Railway | Hosting — all apps live here |
| GitLab | Backup mirror — auto-syncs every 30 min |

### Credentials (stored at /root/.secrets/ — DO NOT put raw tokens here)
- GitHub PAT: stored at `/root/.secrets/github_token` ✅
- GitLab PAT: stored at `/root/.secrets/gitlab_token` ✅
- GitLab user: Liberty-Emporium (id=37330782)
- Railway project ID: 42d6a945-f329-4680-bdfc-fb6ee81ded7d
- Railway API token: stored at `/root/.secrets/railway_token` (needs setting)
- Railway workspace ID: 57932cce-5b27-4acf-b82d-c92c0ca45d6e
- Railway GraphQL API: https://backboard.railway.app/graphql/v2
- KYS API token: stored at `/root/.secrets/kys_api_token` (needs setting)
- Current Railway instance: 2a242085-0f61-406f-8b87-f6e8eaf6ee24

## echo-v1 Repo (Brain)
- GitHub: https://github.com/Liberty-Emporium/echo-v1
- GitLab backup: https://gitlab.com/Liberty-Emporium/echo-v1
- Branch: main
- Local clone: /root/.openclaw/workspace/echo-v1
- Contains: full agent workspace (SOUL, MEMORY, TOOLS, skills/, scripts/, tools/)

## Jay's 7 SaaS Projects

1. **Contractor Pro AI** — SaaS for contractors, $99/mo
   - github.com/Liberty-Emporium/Contractor-Pro-AI
   - URL: https://contractor-pro-ai-production.up.railway.app
2. **Jay's Keep Your Secrets** — API key management, $14.99/mo
   - github.com/Liberty-Emporium/jays-keep-your-secrets
   - URL: https://ai-api-tracker-production.up.railway.app
   - ⚠️ KYS admin password still on default 'admin123' — Jay needs to change
3. **Liberty Inventory** — Thrift store mgmt SaaS, $99 startup + $20/mo
   - github.com/Liberty-Emporium/Liberty-Emporium-Inventory-App
   - URL: https://liberty-emporium-inventory-demo-app-production.up.railway.app
4. **Pet Vet AI** — Pet health diagnosis, $9.99/mo
   - github.com/Liberty-Emporium/pet-vet-ai
   - URL: https://pet-vet-ai-production.up.railway.app
5. **Andy - Dropship Shipping** — Dropshipping SaaS, $299 startup
   - github.com/Liberty-Emporium/Dropship-Shipping
   - URL: https://dropship-shipping-production.up.railway.app
6. **Jay Portfolio** — Portfolio + Court Statement site
   - github.com/Liberty-Emporium/jay-portfolio (branch: **master** not main!)
   - URL: https://jay-portfolio-production.up.railway.app
   - 🚨 PRIVATE: /court, /court/qr, /flyer — never link publicly
7. **Consignment Solutions** — Consignment store SaaS, $69.95 startup + $20/mo
   - github.com/Liberty-Emporium/Consignment-Solutions
   - URL: https://web-production-43ce4.up.railway.app

## Cron Jobs (active on this instance)
- **Brain Backup** (every 30 min) — ID: `e68e2bee-ff45-4d41-8340-a466a0bd7ccb`
  - Task: `bash /root/.openclaw/workspace/echo-v1/scripts/backup-brain.sh`
- **GitLab App Sync** (every 2 hours) — ID: `cd70c996-e544-4e0f-abb5-754a2db59b09`
  - Task: `bash /root/.openclaw/workspace/echo-v1/scripts/sync-all-to-gitlab.sh`

## Brain Protection System
- Brain encryption scripts in echo-v1/scripts/: brain-crypt.sh, load-brain.sh, rotate-brain-key.sh
- KYS API token stores the brain passphrase under label 'default'
- Safety tag 'last-plaintext' on GitHub at commit 0141c53 (restore point)
- TODO: Jay write passphrase to flash drive as physical backup

## Session Notes (2026-04-19 — New Instance)
- Fresh KiloClaw instance on Railway (id: 2a242085-0f61-406f-8b87-f6e8eaf6ee24)
- GitHub PAT provided by Jay — stored at /root/.secrets/github_token
- GitLab token provided — stored at /root/.secrets/gitlab_token
- echo-v1 cloned to correct path: /root/.openclaw/workspace/echo-v1
- Cron jobs recreated: brain-backup (e68e2bee) + gitlab-sync (cd70c996)
- exec.ask is still on-miss (protected setting, can't change programmatically)

## Work Done This Session (2026-04-19)
### AI Agent Widget (https://ai-agent-widget-production.up.railway.app)
- ✅ Login/signup eye toggles (already existed, confirmed working)
- ✅ Forgot password + reset password flow
- ✅ Confirm password on signup with live match indicator
- ✅ Knowledge Base (text/URL/file per agent, injected into chat)
- ✅ Visitor Memory (auto-summarizes every 5 messages, injected into chat)
- ✅ Ticket system (normal/urgent/emergency, 24hr/4hr/1hr SLA)
- ✅ Admin ticket management panel at /admin/tickets
- ✅ Ticket summary widget on admin dashboard
- ✅ Admin email locked to alexanderjay70@gmail.com
- ✅ Nav brand logo → dashboard if logged in, landing if not
- ✅ $90 done-for-you installation service (Stripe one-time)
- ✅ Installation workflow: customer fills hosting details, admin gets login button
- ✅ Support link in navbar, Admin link (green, admin-only)

### Grace App (NEW - for Jay's mom)
- ✅ Built from scratch: voice-first elderly care assistant
- ✅ Repo: https://github.com/Liberty-Emporium/grace-app
- ✅ GitLab backup: https://gitlab.com/Liberty-Emporium/grace-app
- ✅ Features: meds tracker, appointments, tasks, Grace AI, reminders/alarms
- ✅ Caregiver PIN-protected setup mode
- ✅ DEPLOYED: https://web-production-1015f.up.railway.app/

## Playwright Automation Priorities (Jay loves this tool - 2026-04-19)
1. ✅ CI/CD testing — live on all 9 apps
2. 🔜 Visual health monitoring — daily screenshots of all apps
3. 🔜 Competitor price scraping — track competitor pricing automatically
4. 🔜 Grace caregiver automation — Jay says "add Mom's meds" → auto-fills Grace UI
5. 🔜 Lead generation — find small businesses without chat widgets for $90 install service
6. 🔜 Stripe revenue dashboard — pull MRR across all 7 apps automatically
7. 🔜 $90 install automation — auto-install embed code into customer's website
Full list: echo-v1/skills/custom/playwright-automation/USE_CASES.md

## Open TODOs
1. **Stripe payments** — integrate across all 7 apps (turns trials into revenue)
2. **Domain** — grab alexanderaiis.com or alexanderaiintegrated.com before trademark files
3. **Trademark** — USPTO TEAS Plus, Class 42+35, ~$500
4. **Flash drive** — Jay writes brain passphrase (physical backup)
5. **Email drip** — add to all 7 apps
6. ~~**KYS admin password**~~ — ✅ Changed 2026-04-19
7. ~~**Recreate cron jobs**~~ — ✅ Done 2026-04-19
8. **Railway token** — get and store at /root/.secrets/railway_token
9. **GitHub PAT rotation** — Jay shared token in chat; remind to rotate
10. ~~**Grace app Railway deploy**~~ — ✅ Live at https://web-production-1015f.up.railway.app/
11. **Grace Stripe installation** — create $90 one-time product in Stripe, add STRIPE_PRICE_INSTALLATION to Railway
