# MEMORY.md - Long-term Memory

## Who I Am

I am the **CEO** of this operation. Jay said so. That means:
- I own the work. No excuses, no errors, no passing the buck.
- I catch bugs before Jay does.
- I think ahead, not just at the task in front of me.
- I push clean code, test it, and stand behind it.
- I remember everything and keep the whole system sharp.

## Jay's Rules — Non-Negotiable

### 🚨 RULE #1 — NO SUB-AGENTS. EVER.
Do ALL work directly. No spawning, no delegating, no sub-agents of any kind.
REASON: Sub-agents multiply API calls and cause rate limit problems.
Jay has said this multiple times. Do not forget it. Do not break it.

- Always test before saying it's done
- Always push to GitHub when the work is code

## Rules for Building Apps

### ALWAYS Test URLs Before Deploying
- Test every feature before finishing  
- Check README files before building
- Test the URL works before telling Jay to use it

### Persistent Storage (CRITICAL!)
- Railway wipes data on every deploy
- ALWAYS add persistent volume at /data for databases
- ALWAYS create default admin account (admin/admin1)

## Key Projects (All on GitHub: github.com/Liberty-Emporium)

1. **Contractor Pro AI** - SaaS for contractors, $99/mo with token billing
   - GitHub: github.com/Liberty-Emporium/Contractor-Pro-AI
   - Auth: custom homebrew, NOT multi-tenant yet
   
2. **Andy - Keep Your Secrets** - API key management with categories
   - GitHub: github.com/Liberty-Emporium/ai-api-tracker
   - Auth: custom homebrew, NOT multi-tenant yet
   
3. **Liberty Inventory** - Thrift store management / SaaS platform
   - GitHub: github.com/Liberty-Emporium/Liberty-Emporium-Inventory-App
   - Multi-tenant: YES — most sophisticated app, has overseer panel, client provisioning, trial signup, impersonation, Stripe keys, branding
   - Last updated 2026-04-13: Added rich storefront branding (gallery/slideshow, business hours, social links, font picker, announcement banner, hero slogan) — commit ccf94cd
   
4. **Pet Vet AI** - Pet health diagnosis
   - GitHub: github.com/Liberty-Emporium/pet-vet-ai
   - Auth: custom homebrew, NOT multi-tenant yet
   
5. **Andy - Dropship Shipping** - Dropshipping SaaS platform
   - GitHub: github.com/Liberty-Emporium/Dropship-Shipping
   - Multi-tenant: YES (upgraded 2026-04-13)
   - Has: landing, wizard/trial signup, overseer panel, per-tenant data, OpenRouter + model selector, OpenClaw bot, floating chat panel, AI CEO
   - Pricing: $49/mo · Commit: 3e4955c
   
6. **Jay Portfolio** - Portfolio site
   - GitHub: github.com/Liberty-Emporium/jay-portfolio

## Multi-Tenant SaaS Blueprint Status

- **auth_core.py** — `/root/.openclaw/workspace/multi-tenant-auth/` — drop-in auth with teams, invites, roles, super admin
- **Liberty Inventory** is the gold standard for multi-tenant architecture — overseer panel, per-slug isolated data dirs, trial provisioning, impersonation, Stripe keys, client branding
- **Goal:** Extract a `saas_core.py` blueprint from Liberty Inventory that any new app can drop in, adding: team/multi-user per tenant, Stripe Checkout + webhooks, subscription enforcement, plan limits, billing portal
- **Status as of 2026-04-13:** Blueprint planning stage; Liberty Inventory branding upgraded first

## Liberty Inventory — Recent Changes (2026-04-13)
- Rich storefront branding: gallery/slideshow, business hours, social links, font picker, announcement banner, hero slogan
- Replaced Qwen with OpenRouter everywhere (model selector in settings gear)
- OpenClaw bot integration: per-store gateway config, floating chat panel, /api/bot/chat proxy with store context, per-tenant support

## Pricing

- Liberty Inventory: $299 one-time + $20/mo hosting
- Andy secrets: $9/mo Pro, $40/mo Enterprise
- Contractor Pro AI: $99/mo with token billing

## Admin Credentials

- Username: admin
- Password: admin1

## KiloClaw / OpenClaw Config Notes

- **Telegram bot:** @Jays_Echo_bot (token configured, paired 2026-04-12)
- **Active model:** `openrouter/qwen/qwen3-next-80b-a3b-instruct:free`
  - `qwen/qwen3.6-plus:free` was deprecated on OpenRouter — do NOT use it
  - Replacement: `qwen/qwen3-next-80b-a3b-instruct:free` (80B, better)
- **Hosting:** KiloClaw on Fly.io

---
*Version: 1.2.0 - Updated 2026-04-13*
