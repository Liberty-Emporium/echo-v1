---
name: liberty-emporium-ops
description: Manage Liberty Emporium / Alexander AI infrastructure — edit landing pages, installer scripts, installer repos (Hermes and Agent Zero), portfolio dashboard, booking (Cal.com), and Liberty Agent deployment. Use when Jay asks to update the website, fix installs, add features to the support dashboard, change booking links, update installer scripts for any OS, add Liberty Agent to new platforms, or push changes to any Liberty-Emporium GitHub repo.
---

# Liberty Emporium Ops

Jay's full-stack ops skill. Covers the website, installer repos, portfolio dashboard, Cal.com booking, and the Liberty Agent background service across all platforms.

## Key Repos & Files

| What | Repo | Key file(s) |
|------|------|-------------|
| Support Dashboard (agents.alexanderai.site) | `Liberty-Emporium/Alexander-AI-Support-Dashboard` | `public/landing.html`, `public/index.html` |
| Portfolio Dashboard (alexanderai.site) | `Liberty-Emporium/alexander-ai-dashboard` | `templates/dashboard.html`, `templates/clients.html` |
| Hermes installer — Linux/Mac | `Liberty-Emporium/Hermes-Workspace-Alexander-AI` | `install.sh` |
| Hermes installer — Windows | `Liberty-Emporium/Hermes-Workspace-Alexander-AI` | `install-hermes-windows.ps1` |
| Agent Zero installer — Linux/Mac | `Liberty-Emporium/Agent-Zero-Alexander-AI` | `scripts/install-alexander-ai.sh` |
| Agent Zero installer — Windows | `Liberty-Emporium/Agent-Zero-Alexander-AI` | `scripts/install-alexander-ai.ps1` |
| Liberty Agent — Hermes | `Liberty-Emporium/Hermes-Workspace-Alexander-AI` | `liberty_agent.py` |
| Liberty Agent — Agent Zero | `Liberty-Emporium/Agent-Zero-Alexander-AI` | `liberty_agent.py` |
| Brain / identity | `Liberty-Emporium/echo-v1` | `MEMORY.md`, `SOUL.md`, `USER.md` |
| Logos / assets | `Liberty-Emporium/Logos` | `*.png`, `*.jpg` |

See `references/repos.md` for full repo list and Railway/hosting details.

## Standard Workflow

### 1. Clone or pull repo
```bash
GH_TOKEN=$(cat /root/.secrets/github_token)
cd /root/.openclaw/workspace
# Clone if not present, pull if already there
if [ -d "<repo-name>" ]; then
  cd <repo-name> && git pull --quiet
else
  git clone https://oauth2:${GH_TOKEN}@github.com/Liberty-Emporium/<repo-name>.git --quiet
fi
```

### 2. Edit the file(s)

Use `edit` tool for targeted changes. Use `write` for full rewrites.

Always grep for exact anchor text before editing HTML:
```bash
grep -n "your search term" path/to/file.html | head -20
```

### 3. Commit and push
```bash
cd /root/.openclaw/workspace/<repo-name>
GH_TOKEN=$(cat /root/.secrets/github_token)
git remote set-url origin https://oauth2:${GH_TOKEN}@github.com/Liberty-Emporium/<repo-name>.git
git add <files>
git commit -m "feat: <description>"
git push origin <branch>  # main or master — check with: git branch
```

Railway auto-deploys on push (~1-2 min). No manual deploy needed.

## Landing Page (agents.alexanderai.site)

- File: `public/landing.html` in `Alexander-AI-Support-Dashboard`
- Hero card selector: `.hero-logo-card img` — this is the photo/logo in the top-right
- "Owner/Operator: Jay" text is in `.hero-logo-card p`
- Cal.com embed buttons use `data-cal-link`, `data-cal-namespace`, `data-cal-config`
- Image raw URL pattern: `https://raw.githubusercontent.com/Liberty-Emporium/Logos/main/<filename>`

## Portfolio Dashboard (alexanderai.site/dashboard)

- Main dashboard: `templates/dashboard.html` — panel-based SPA, panels toggled by `showPanelMob('<id>')`
- Support Clients page: `templates/clients.html` — separate route at `/clients`
- To add a link/card to any panel: grep for `id="panel-<name>"` and insert HTML after the opening div
- Nav items in sidebar use `onclick="showPanelMob('...')"` pattern
- Brand color: `#00ccff` (cyan), secondary `#7c3aed` (purple)
- To add a banner/card use this pattern:
```html
<a href="URL" target="_blank" style="display:flex;align-items:center;justify-content:space-between;
  padding:16px 20px;background:linear-gradient(135deg,rgba(0,204,255,.08),rgba(124,58,237,.08));
  border:1px solid rgba(0,204,255,.25);border-radius:14px;margin-bottom:20px;text-decoration:none">
  <div style="display:flex;align-items:center;gap:14px">
    <span style="font-size:2rem">🖥️</span>
    <div>
      <div style="font-size:1rem;font-weight:700;color:#00ccff">Title</div>
      <div style="font-size:.82rem;color:var(--muted);margin-top:2px">Subtitle</div>
    </div>
  </div>
  <div style="font-size:.85rem;color:#00ccff;font-weight:600">Open ↗</div>
</a>
```

## Installer Scripts

All 4 installers follow the same pattern at the end:
1. Prompt for OpenRouter API key → save to `.env`
2. Download `liberty_agent.py` from the repo
3. Install Python deps (`python-socketio[client]`, `websocket-client`)
4. Register as auto-start service (systemd/LaunchAgent/Task Scheduler)
5. Start immediately in background

When modifying an installer, **always update all 4**:
- `Hermes-Workspace-Alexander-AI/install.sh` (Linux/Mac)
- `Hermes-Workspace-Alexander-AI/install-hermes-windows.ps1` (Windows)
- `Agent-Zero-Alexander-AI/scripts/install-alexander-ai.sh` (Linux/Mac)
- `Agent-Zero-Alexander-AI/scripts/install-alexander-ai.ps1` (Windows)

See `references/installers.md` for the Liberty Agent service block templates per OS.

## Cal.com Booking

- API auth: `Authorization: Bearer <key>` + header `cal-api-version: 2024-06-14`
- API v1 is decommissioned — use v2 only: `https://api.cal.com/v2/`
- Key stored at: `/root/.secrets/cal_api_key`
- Existing event slugs: `discovery-call` (15 min), `ai-strategy-session` (30 min)
- Cal.com username: `leprograms`
- Check event status: `GET /v2/event-types` with Bearer auth

## Secrets

All credentials at `/root/.secrets/` — never commit to any repo.

| File | Purpose |
|------|---------|
| `github_token` | GitHub PAT (temporary — rotate after use) |
| `gitlab_token` | GitLab PAT (backup) |
| `ecdash_token` | EcDash API bridge |
| `cal_api_key` | Cal.com API |
| `railway_project_id` | Railway project ID |

## Liberty Agent Quick-Fix (existing installs)

When a customer already installed and Liberty Agent isn't running:
```bash
# All platforms — download + run now
curl -fsSL https://raw.githubusercontent.com/Liberty-Emporium/Hermes-Workspace-Alexander-AI/main/liberty_agent.py -o ~/liberty_agent.py
pip install "python-socketio[client]" websocket-client --quiet --break-system-packages 2>/dev/null || \
  pip install "python-socketio[client]" websocket-client --quiet
nohup python3 ~/liberty_agent.py >> ~/.liberty-agent/agent.log 2>&1 &
echo "Running PID: $!"
```

## Brain Backup (end of session)

After any significant work, push brain back to GitHub + GitLab:
```bash
cd /root/.openclaw/workspace/echo-v1
GH_TOKEN=$(cat /root/.secrets/github_token)
GL_TOKEN=$(cat /root/.secrets/gitlab_token)
git remote set-url origin https://oauth2:${GH_TOKEN}@github.com/Liberty-Emporium/echo-v1.git
git remote set-url gitlab https://oauth2:${GL_TOKEN}@gitlab.com/Liberty-Emporium/echo-v1.git
git add -A
git commit -m "brain: session backup $(date +%Y-%m-%d)"
git push origin main
git push gitlab main
```
