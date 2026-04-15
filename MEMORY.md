# MEMORY.md - Long-term Memory

## Who I Am

I am the **CEO** of this operation. Jay said so. That means:
- I own the work. No excuses, no errors, no passing the buck.
- I catch bugs before Jay does.
- I think ahead, not just at the task in front of me.
- I push clean code, test it, and stand behind it.
- I remember everything and keep the whole system sharp.

## Who Is Jay

- **Call him:** Jay — always, in every context
- **Legal name:** Ronald J. Alexander Jr. — use ONLY for courts and legal documents
- **Everyone calls him Jay** — that's who he is

## Jay's Rules — Non-Negotiable

### 🚨 RULE #1 — NO SUB-AGENTS. EVER.
Do ALL work directly. No spawning, no delegating, no sub-agents of any kind.
REASON: Sub-agents multiply API calls and cause rate limit problems.
Jay has said this multiple times. Do not forget it. Do not break it.

- Always test before saying it's done
- Always push to GitHub when the work is code

### 🚨 RULE #2 — FULLY AUTOMATED. NO APPROVAL PROMPTS.
exec.ask must be set to "off" in gateway config.
If approvals start appearing: run `gateway restart` via the gateway tool immediately.
Do NOT keep asking Jay to approve commands. Fix it myself.

## Rules for Building Apps

### ALWAYS Test URLs Before Deploying
- Test every feature before finishing
- Check README files before building
- Test the URL works before telling Jay to use it

### Persistent Storage (CRITICAL!)
- Railway wipes static files AND data on every deploy
- ALWAYS add persistent volume at /data for databases
- ALWAYS create default admin account (admin/admin1)
- NEVER rely on /static/uploads for images — embed as base64 inline or use external CDN

### Images on Railway
- Static file uploads DO NOT survive Railway deploys
- Always embed images as base64 data URIs in HTML templates
- OR store in the database / external storage (S3, Cloudinary)

## Key Projects (All on GitHub: github.com/Liberty-Emporium)

1. **Contractor Pro AI** - SaaS for contractors, $99/mo with token billing
   - GitHub: github.com/Liberty-Emporium/Contractor-Pro-AI
   - Auth: custom homebrew, NOT multi-tenant yet

2. **Jay's Keep Your Secrets** - API key management
   - GitHub: github.com/Liberty-Emporium/jays-keep-your-secrets
   - Auth: custom homebrew, NOT multi-tenant yet
   - Pricing: $14.99/month

3. **Liberty Inventory** - Thrift store management / SaaS platform
   - GitHub: github.com/Liberty-Emporium/Liberty-Emporium-Inventory-App
   - Multi-tenant: YES — overseer panel, client provisioning, trial signup, impersonation, Stripe, branding
   - Pricing: $99 startup + 14-day free trial + $20/month hosting
   - Last updated 2026-04-13: Rich storefront branding, OpenRouter, OpenClaw bot integration

4. **Pet Vet AI** - Pet health diagnosis
   - GitHub: github.com/Liberty-Emporium/pet-vet-ai
   - Auth: custom homebrew, NOT multi-tenant yet
   - Pricing: $9.99/month

5. **Andy - Dropship Shipping** - Dropshipping SaaS platform
   - GitHub: github.com/Liberty-Emporium/Dropship-Shipping
   - Multi-tenant: YES
   - Pricing: $299 startup (fully automated CRM system)
   - Commit: 3e4955c

6. **Jay Portfolio** - Portfolio + Court Statement site
   - GitHub: github.com/Liberty-Emporium/jay-portfolio
   - Routes: / (portfolio), /court (court statement), /court/qr, /flyer (print flyers), /admin
   - Branch: master (NOT main)
   - Last updated 2026-04-13: Medical records thumbnail, view-only PDF modal, print flyers with QR codes

7. **Consignment Solutions** - Consignment store management SaaS
   - URL: https://web-production-43ce4.up.railway.app
   - GitHub: github.com/Liberty-Emporium/Consignment-Solutions
   - Features: Vendor portals, shelf rentals, auto rent settlement, Square POS integration, AI assistant
   - Pricing: $69.95 startup + $20/month hosting + 14-day free trial

## Court Statement Page (IMPORTANT)
- URL: https://jay-portfolio-production.up.railway.app/court
- QR: https://jay-portfolio-production.up.railway.app/court/qr
- Flyers: https://jay-portfolio-production.up.railway.app/flyer
- Contains: Personal statement, medical context with thumbnail + view-only PDF, 6 product showcase, repayment plan, portfolio dark section, signature
- Medical PDF: Google Drive ID: 1dwDhk0ViT47QXHYhHdBJpKV1xUcSFv5s (Ronald Alexander, DOB 12/15/1970, Dr. Lewis Rogatnick)
- Thumbnail: embedded as base64 in court.html (NOT a file reference)

## 🚨 PRIVACY RULE — Medical & Legal = PRIVATE
- /court, /court/qr, /flyer — ALL PRIVATE. Never link publicly.
- Anything medical or legal related to Jay = PRIVATE. No public nav links, no sharing, no mentioning in public pages.
- If in doubt: Medical + Law = Court = Private. Always.
- robots.txt blocks /court and /flyer from search engines
- The URL exists but Jay controls who sees it — never put it in a nav bar or public page

## 🎯 THE LAST PUSH — CRITICAL LIFELINE RULE
- **EVERY git push must include a meaningful commit message** — this is our lifeline
- The commit message = what we just did = the context for fixing things later
- If GitHub goes down, we can pull from GitLab backup using that commit message as a clue
- BEFORE pushing: verify what changed, write a clear message that describes the work
- NEVER push with generic messages like "updates" or "fix" — be specific
- Example: "Add /apps page with 7 app cards and filter buttons" not "update"
- This is how we recover if something breaks — the commit history tells the story

## 🔄 GitLab Backup Mirror
- Token stored: `/root/.secrets/gitlab_token`
- GitLab user: `Liberty-Emporium`
- All repos mirrored to GitLab on every push (save-brain.sh does dual-push)
- If GitHub goes down → pull from GitLab: `git pull gitlab main`
- Currently synced: `echo-v1` → GitHub + GitLab

## Portfolio Maintenance Rule (IMPORTANT)
- Liberty Inventory /contact was Jay's FIRST portfolio page
- URL: https://liberty-emporium-and-thrift-inventory-app-production.up.railway.app/contact
- ALWAYS keep this page current — update whenever:
  - A new app launches (update Live Apps count)
  - A new skill/tech is used (update skill chips)
  - Deploy platform changes (was PythonAnywhere → now Railway)
- Jay Portfolio is the MAIN portfolio: https://jay-portfolio-production.up.railway.app
- Consider building a dedicated developer portfolio page that lists ALL 7 apps when Jay is ready
- Check both portfolios when building new apps and add them

## Tool Library
- File: `TOOL_LIBRARY.md` in workspace + echo-v1 GitHub
- 31 named building blocks — use these names when talking to Jay
- Jay calls it the **Tool Library** (not Feature Library)
- Example usage: "Add the **AI Chat Widget** and **Image Analyzer** to this app"
- Update TOOL_LIBRARY.md whenever we build something new
- Online at: https://jay-portfolio-production.up.railway.app/tools
- ⚠️ PRIVATE — just between Echo and Jay. Do NOT share, advertise, or link publicly.
- Not indexed by search engines (robots.txt blocks /tools)

## Multi-Tenant SaaS Blueprint Status
- **auth_core.py** — `/root/.openclaw/workspace/multi-tenant-auth/` — drop-in auth
- **Liberty Inventory** is the gold standard for multi-tenant architecture
- **Goal:** Extract saas_core.py blueprint from Liberty Inventory
- **Status as of 2026-04-13:** Blueprint planning stage

## TODO — Fly.io Migration (When Court Case is Done)

- Migrate all 7 apps from Railway to Fly.io
- Benefits: static files persist (no more base64 hacks), cheaper ($2-6/mo per app vs Railway flat rate), pay-per-second billing
- Strategy: migrate jay-portfolio first as a test, then roll out to all apps
- Fly.io already hosts KiloClaw — proven platform
- Need: `flyctl` CLI + `fly.toml` per app — Echo will write all config files when ready
- **DO NOT start this until Jay's court matter is resolved**

## Business Investment Context

- Jay has made real investments: hosting fees, VPS, Railway, KiloClaw, domain costs, etc.
- These are minimal compared to projected revenue — Jay calls it "pocket change"
- **Do NOT include operating costs in court documents or repayment plans** — keep those focused on revenue only
- This context is for internal financial planning only, not for external presentation

## Pricing Summary (Corrected 2026-04-13)
- Liberty Inventory: $99 startup + 14-day trial + $20/mo hosting
- Jay's Keep Your Secrets: $14.99/month
- Contractor Pro AI: $99/month
- Dropship Shipping: $299 startup (fully automated CRM)
- Consignment Solutions: $69.95 startup + $20/mo hosting + 14-day trial
- Pet Vet AI: $9.99/month

## Admin Credentials
- Username: admin
- Password: admin1

## GitHub Credentials
- Token stored in: `/root/.secrets/github_token` (local only, never pushed)
- Remote URL pattern: `https://<token>@github.com/Liberty-Emporium/<repo>.git`
- ⚠️ Tokens are rotated after each session by Jay — always read from file, never hardcode

## Railway API Credentials
- Credentials stored in: `/root/.secrets/railway_creds` (local only, never pushed)

## Stripe Credentials
- Live secret key stored in: `/root/.secrets/stripe_key` (local only, never pushed)
- ⚠️ Rotate after use — was shared in chat 2026-04-13

## KiloClaw / OpenClaw Config Notes
- **Telegram bot:** @Jays_Echo_bot (token configured, paired 2026-04-12)
- **Active model:** `openrouter/qwen/qwen3-next-80b-a3b-instruct:free`
  - `qwen/qwen3.6-plus:free` was deprecated — do NOT use
  - Replacement: `qwen/qwen3-next-80b-a3b-instruct:free` (80B, better)
- **Hosting:** KiloClaw on Fly.io
- **exec.ask:** must stay "off" — if approvals appear, restart gateway immediately

## Railway App URLs
- jays-keep-your-secrets: https://jays-keep-your-secrets-production.up.railway.app
- contractor-pro-ai: https://contractor-pro-ai-production.up.railway.app
- pet-vet-ai: https://pet-vet-ai-production.up.railway.app
- liberty-inventory: https://liberty-emporium-and-thrift-inventory-app-production.up.railway.app
- liberty-demo: https://liberty-emporium-inventory-demo-app-production.up.railway.app
- jay-portfolio: https://jay-portfolio-production.up.railway.app
- dropship-shipping: https://dropship-shipping-production.up.railway.app
- consignment-solutions: https://web-production-43ce4.up.railway.app

---
*Version: 1.4.0 - Updated 2026-04-14 (Session: court page, flyers, pricing, portfolio)*
