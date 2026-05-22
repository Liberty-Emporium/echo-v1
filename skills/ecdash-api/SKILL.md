---
name: ecdash-api
description: Work with EcDash (Jay's portfolio/dashboard at jay-portfolio-production.up.railway.app). Covers the echo-bridge API, daily summary cards, AI panel updates, and the update-dashboard.py script in echo-v1/scripts/.
---

# EcDash API Skill

## What is EcDash?
Jay's developer portfolio + daily activity dashboard. Lives at:
- **URL:** https://jay-portfolio-production.up.railway.app
- **GitHub repo:** Liberty-Emporium/alexander-ai-dashboard (was: jay-portfolio)
- **Branch:** master

## Auth
Token stored at `/root/.secrets/ecdash_token`
Header: `Authorization: Bearer <token>`

## Echo-Bridge Queue
```bash
curl -s -H "Authorization: Bearer $(cat /root/.secrets/ecdash_token)" \
  "https://jay-portfolio-production.up.railway.app/api/echo-bridge"
# Returns: {"tasks": [...]}
```

## update-dashboard.py Script
Located at: `echo-v1/scripts/update-dashboard.py`

Requires `jay-portfolio` repo cloned to `/root/.openclaw/workspace/jay-portfolio/`
(GitHub now calls it `alexander-ai-dashboard` but local clone dir is `jay-portfolio`)

### Key functions:
```bash
# Status check
python3 scripts/update-dashboard.py --status

# Add daily summary card
python3 -c "
import importlib.util
spec = importlib.util.spec_from_file_location('upd', 'scripts/update-dashboard.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
m.add_daily_card(
    date_str='Fri May 22, 2026',
    title='Session Title Here',
    items=[
        ('🎬', 'Bold Label', 'Description of what was done'),
    ],
    color='#D4A017',
    push=False,
)
"

# Update AI panel
python3 scripts/update-dashboard.py \
  --update-ai \
  --last-session "May 22, 2026 — What we did" \
  --skills "35+ built for your projects" \
  --no-push
```

### Card colors by theme:
- Gold `#D4A017` — major overhaul sessions
- Cyan `#22d3ee` — bootstrap/setup sessions
- Purple `#8b5cf6` — infrastructure/CI
- Green `#10b981` — foundation/launch
- Indigo `#6366f1` — AI/automation

### Daily insertion point in dashboard.html:
```html
<div style="max-width:800px;display:flex;flex-direction:column;gap:1.25rem">
  <!-- NEW CARDS GO HERE -->
```

## Workflow: Add Today's Card + Push
```bash
cd /root/.openclaw/workspace/echo-v1
# 1. Update AI panel
python3 scripts/update-dashboard.py --update-ai --last-session "DATE — SUMMARY" --skills "N+ built" --no-push
# 2. Add daily card (use importlib method above)
# 3. Push portfolio repo
cd /root/.openclaw/workspace/jay-portfolio
git add templates/dashboard.html
git commit -m "EcDash: add MMDD daily summary"
git push origin master
```
