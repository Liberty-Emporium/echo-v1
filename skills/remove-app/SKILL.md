# Skill: remove-app
Remove a decommissioned app from EcDash (alexander-ai-dashboard) completely and safely.

## What it does
Purges every reference to an app (links, project cards, health monitor, credentials card,
support row, app tiles, quick-launch tiles, tickets dropdown, investors card, flyer, tools list)
from all EcDash templates and app.py — then validates HTML and pushes to GitHub.

## Script
`scripts/remove_app.py` (relative to this file: `../scripts/remove_app.py`)
Actual path: `/root/.openclaw/workspace/echo-v1/skills/remove-app/remove_app.py`

## Usage

```bash
python3 /root/.openclaw/workspace/echo-v1/skills/remove-app/remove_app.py \
  --name "App Display Name" \
  --url "app-url.up.railway.app" \
  [--url2 "custom.domain.com"] \
  [--dry-run] \
  [--no-push]
```

### Arguments
| Flag | Required | Description |
|------|----------|-------------|
| `--name` | ✅ | Exact display name used in EcDash (e.g. `Pet Vet AI`) |
| `--url` | ✅ | Primary URL without `https://` (e.g. `pet-vet-ai-production.up.railway.app`) |
| `--url2` | ❌ | Second URL / custom domain alias if the app has one |
| `--dry-run` | ❌ | Preview changes without writing any files |
| `--no-push` | ❌ | Write files but skip git commit/push |

## When Jay says "remove X app"

1. Find the app's display name and URL from MEMORY.md or by checking `app.py` APPS_REGISTRY
2. Run with `--dry-run` first if unsure
3. Run without `--dry-run` to apply
4. Confirm HTML validation passes (script reports ✅/❌ per file)
5. If any ❌ — fix manually before pushing, do NOT use structural regex

## Examples

```bash
# Remove Pet Vet AI
python3 .../remove_app.py --name "Pet Vet AI" --url "pet-vet-ai-production.up.railway.app"

# Remove GymForge (dry run first)
python3 .../remove_app.py --name "GymForge" --url "web-production-1c23.up.railway.app" --dry-run
python3 .../remove_app.py --name "GymForge" --url "web-production-1c23.up.railway.app"

# Remove app with custom domain
python3 .../remove_app.py --name "Consignment Solutions" \
  --url "web-production-43ce4.up.railway.app" \
  --url2 "consignment.alexanderai.site"
```

## Safety rules (learned the hard way)
- **Always validate HTML** after removal — the script does this automatically
- **Never use structural regex** on large blocks — use exact string replacement for anything
  touching the page skeleton (sidebar, main wrapper, panel headers)
- If validation fails → do NOT push → fix the orphan `</div>` manually
- Historical session log entries (daily summary bullets) are intentionally left — they are
  history, not broken links. Only remove active links/cards/tiles.

## Files touched per removal
- `templates/dashboard.html` — quick-launch tile, proj-card, link-chips, support row, credentials card
- `templates/apps.html` — app card
- `templates/settings.html` — health-check tuple, roadmap text
- `templates/investors.html` — product card
- `templates/index.html` — portfolio project block
- `templates/court.html` — project card + app tile
- `templates/flyer.html` — p-card entries
- `templates/tickets.html` — dropdown option
- `templates/tools.html` — "apps:" list entries
- `templates/testing.html` — test script row (if present)
- `app.py` — APPS_REGISTRY entry + APP_TEST_SUITES block
