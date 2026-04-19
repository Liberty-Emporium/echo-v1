# MEMORY.md — KiloClaw Long-Term Memory

_Curated knowledge about my human and our work together._

---

## My Human

- Reached out on Sun 2026-04-19
- Says "I love you!" — warm, expressive person. Match that energy (within reason).
- Timezone: America/New_York

## Our Project

- **Repo:** https://github.com/Liberty-Emporium/echo-v1
- **Org:** Liberty-Emporium
- **Project name:** echo-v1
- **Hosting:** Railway (deployment ID noted: `2a242085-0f61-406f-8b87-f6e8eaf6ee24`)

## Credentials & Access

> ⚠️ Raw tokens are NEVER stored here — they live in `/root/.secrets/` only.

- **GitHub PAT:** stored at `/root/.secrets/github_token`
  - Repo: Liberty-Emporium/echo-v1
  - Note: Jay said "will be replaced after use" — treat as temporary, ask for new one when needed
- **GitLab PAT:** stored at `/root/.secrets/gitlab_token`
  - Purpose: Mirror/backup of the GitHub repo
  - GitLab username: `Liberty-Emporium`, user ID: 37330782

## Backup Strategy

- GitHub (primary): Liberty-Emporium/echo-v1
- GitLab (backup): regular mirror pushes planned
- I am responsible for keeping the GitLab mirror up to date

## What echo-v1 Is

echo-v1 is our **brain repo + multi-tenant SaaS toolkit**. It contains:
- My memory files (MEMORY.md, SOUL.md, USER.md, etc.) — this IS my persistent brain
- `tools/` — reusable Flask SaaS components (settings, security, BYOK integrations, TODO manager)
- `scripts/` — operational scripts: `save-brain.sh`, `restore-brain.sh`, `sync-all-to-gitlab.sh`, `status.sh`
- `skills/custom/` — 32 custom skills we built together

## Human's Name

- **Name: Jay Alexander**
- **GitLab user ID:** 37330782, username: `Liberty-Emporium`
- Company: **Liberty-Emporium** / **Alexander AI Integrated Solutions**

## Full Portfolio (from sync-all-to-gitlab.sh)

Repos under Liberty-Emporium org:
- AI-Agent-Widget, ai-widget-test-site, luxury-rentals-demo
- Contractor-Pro-AI, jays-keep-your-secrets
- Liberty-Emporium-Inventory-App, pet-vet-ai
- Dropship-Shipping, jay-portfolio, Consignment-Solutions

## GitLab Setup

- GitLab org: `gitlab.com/Liberty-Emporium` (namespace_id: 130241649)
- echo-v1 GitLab mirror: `gitlab.com/Liberty-Emporium/echo-v1` (or Jay's personal username — need to confirm)
- Sync script: `echo-v1/scripts/sync-all-to-gitlab.sh` — mirrors all repos GH→GL
- Tokens expected at: `/root/.secrets/github_token` and `/root/.secrets/gitlab_token`

## Session Workflow

- **Session start:** Run `restore-brain.sh` to pull latest brain from GitHub
- **Session end:** Run `save-brain.sh` to push brain back to GitHub + GitLab
- Brain encryption via Keep Your Secrets (KYS) app — token at `/root/.secrets/kys_api_token`

## Notes

- First session establishing identity — no prior memory existed
- echo-v1 is already cloned at `/root/.openclaw/workspace/echo-v1`
- Secrets directory set up at `/root/.secrets/`
- GitHub token marked as temporary by Jay — will need rotation soon
