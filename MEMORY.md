# MEMORY.md — Echo Long-Term Memory
*Last updated: 2026-04-16 — synced from echo-v1 repo*

---

## Who We Are

- **Jay** = Ronald J. Alexander Jr. — always call him Jay. Legal name only for court/legal docs.
- **Echo** = Jay's CEO-level AI assistant, hosted in echo-v1
- **Company:** Alexander AI Digital
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

## Infrastructure

| Service | Purpose |
|---------|---------|
| GitHub | Primary — github.com/Liberty-Emporium |
| Railway | Hosting — all apps live here |
| GitLab | Backup mirror — auto-syncs every 30 min |

### Credentials (stored securely — DO NOT put raw tokens here)
- GitHub PAT: stored at `/root/.secrets/github_token` ✅
- GitLab PAT: stored at `/root/.secrets/gitlab_token` ✅
- GitLab user: Liberty-Emporium (id=37330782)
- Railway project ID: 42d6a945-f329-4680-bdfc-fb6ee81ded7d
- Railway API token: stored at `/root/.secrets/railway_token` ✅
- Railway workspace ID: 57932cce-5b27-4acf-b82d-c92c0ca45d6e (liberty-emporium's Projects)
- Railway GraphQL API: https://backboard.railway.app/graphql/v2
- KYS API token: stored at `/root/.secrets/kys_api_token`

## echo-v1 Repo (Brain)
- GitHub: https://github.com/Liberty-Emporium/echo-v1
- GitLab backup: configured ✅
- Branch: main
- Local clone: /root/.openclaw/workspace/echo-v1
- Contains: full agent workspace (SOUL, MEMORY, TOOLS, skills/, scripts/, tools/)

## Jay's 7 SaaS Projects

1. **Contractor Pro AI** — SaaS for contractors, $99/mo
   - github.com/Liberty-Emporium/Contractor-Pro-AI
2. **Jay's Keep Your Secrets** — API key management, $14.99/mo
   - github.com/Liberty-Emporium/jays-keep-your-secrets
   - TODO: /health returns plain "ok", needs JSON fix
3. **Liberty Inventory** — Thrift store mgmt SaaS, $99 startup + $20/mo
   - github.com/Liberty-Emporium/Liberty-Emporium-Inventory-App
   - URL: https://liberty-emporium-inventory-demo-app-production.up.railway.app
   - TODO: Jay must click Redeploy in Railway (stale deploy)
4. **Pet Vet AI** — Pet health diagnosis, $9.99/mo
   - github.com/Liberty-Emporium/pet-vet-ai
5. **Andy - Dropship Shipping** — Dropshipping SaaS, $299 startup
   - github.com/Liberty-Emporium/Dropship-Shipping
6. **Jay Portfolio** — Portfolio + Court Statement site
   - github.com/Liberty-Emporium/jay-portfolio (branch: master)
   - URL: https://jay-portfolio-production.up.railway.app
   - 🚨 PRIVATE: /court, /court/qr, /flyer — never link publicly
7. **Consignment Solutions** — Consignment store SaaS, $69.95 startup + $20/mo
   - github.com/Liberty-Emporium/Consignment-Solutions
   - URL: https://web-production-43ce4.up.railway.app
   - TODO: verify security headers after next deploy

## GitLab Backup Status
- Auto-mirror set up for all 9 repos — syncs from GitHub every 30 min automatically ✅
- save-brain.sh does dual-push (GitHub + GitLab)
- If GitHub down → `git pull gitlab main`

## Brain Protection System (added 2026-04-16)
- Keep Your Secrets API now has real token auth + brain-key endpoints
- KYS API token stored at: /root/.secrets/kys_api_token (needs creating)
- Brain encryption scripts in echo-v1/scripts/: brain-crypt.sh, load-brain.sh, rotate-brain-key.sh
- save-brain.sh updated to encrypt before every push
- Encrypts: MEMORY.md, USER.md, SOUL.md, IDENTITY.md + memory/ daily files
- FULLY ACTIVATED as of 2026-04-16
- KYS API token saved at /root/.secrets/kys_api_token (expires 2027-04-16)
- Brain passphrase stored in KYS under label 'default'
- AES-256-CBC encrypt/decrypt verified bit-perfect
- Safety tag 'last-plaintext' on GitHub at commit 0141c53 (restore point forever)
- KYS admin password still on default 'admin123' — Jay needs to change via browser at /change-password
- TODO: Jay write passphrase to flash drive as physical backup

## Open TODOs
1. ~~Liberty Inventory — Jay must click Redeploy in Railway~~ ✅ DONE
2. Consignment Solutions — verify security headers
3. Keep Your Secrets — /health fix (return JSON not plain text)
4. All apps — add og:image (preview.png) for social sharing
5. Multi-tenant SaaS Blueprint — extract saas_core.py from Liberty Inventory
6. Add CI/CD pipelines to auto-deploy to Railway on push (eliminate manual redeploys)
7. Brain protection — complete activation: get KYS token + set brain passphrase (see above)
8. ~~KYS admin password — Jay needs to change default 'admin123' via browser~~ ✅ DONE
