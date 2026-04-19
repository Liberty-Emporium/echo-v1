---
name: project-briefing
description: Generate a full status briefing for any Liberty-Emporium project. Use when Jay asks "what's the status of X", "brief me on X", "catch me up on X", "what did we do on X", or at session start to remind Jay what's happening across his portfolio. Combines git log, open todos, recent diary mentions, and live health check.
---

# Project Briefing

Produces a concise, actionable status card for any project in the Liberty-Emporium portfolio.

## Workflow

### 1. Identify the project
Map Jay's words to the right repo and URL:

| Jay says | Repo | Live URL |
|---|---|---|
| inventory / liberty inventory | Liberty-Emporium-Inventory-App | liberty-emporium-and-thrift... |
| inventory demo | liberty-emporium-inventory-demo-app | ...demo-app-production... |
| KYS / keep your secrets | jays-keep-your-secrets | ai-api-tracker-production... |
| pet vet / petvet | pet-vet-ai | pet-vet-ai-production... |
| gymforge / gym | GymForge | web-production-1c23... |
| contractor / contractor pro | Contractor-Pro-AI | contractor-pro-ai-production... |
| dropship / andy | Dropship-Shipping | dropship-shipping-production... |
| consignment | Consignment-Solutions | web-production-43ce4... |
| portfolio / jay portfolio | jay-portfolio | jay-portfolio-production... |
| echo / brain | echo-v1 | (GitHub only) |

### 2. Run check-repo.sh for the project

```bash
bash /root/.openclaw/workspace/echo-v1/scripts/check-repo.sh <repo-local-path>
```

Or manually:
```bash
cd /root/.openclaw/workspace/<repo>
git log --oneline -10          # Recent commits
git status                     # Uncommitted changes
```

### 3. Check live health

```bash
curl -s -o /dev/null -w "%{http_code}" --max-time 6 <URL>/health
```
- 200 = healthy ✅
- 503/timeout = down ❌
- 404 = no /health endpoint (try /)

### 4. Pull open todos for this project

```bash
python3 /root/.openclaw/workspace/echo-v1/tools/todo_manager.py list --project <project-name>
```

### 5. Search recent diary for mentions

```bash
grep -r "<project-name>" /root/.openclaw/workspace/memory/ --include="*.md" -l
```

### 6. Produce the briefing card

```
## 🚀 [Project Name] — Status Brief
📅 As of: YYYY-MM-DD

**Live:** ✅/❌ [URL]
**Last commit:** [hash] [message] ([time ago])
**Uncommitted changes:** [yes/no]

**Recent work:**
- [commit summary 1]
- [commit summary 2]

**Open todos:**
- 🔴 [high priority item]
- 🟡 [medium priority item]

**Notes from memory:**
- [relevant diary mention]

**Recommended next step:**
→ [concrete suggestion]
```

## Quick Brief (no git access)

If repo isn't cloned locally, give a memory-based brief:
- Pull from MEMORY.md and diary files
- Check entities.json for project details
- Note: "based on memory — run a full brief after cloning for live data"
