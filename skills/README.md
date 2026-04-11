# Skills Folder

This folder would contain the actual skill files for Echo.

## How Skills Work

Skills are in `/usr/local/lib/node_modules/openclaw/skills/` on the running system.

Each skill has:
- `SKILL.md` - Description and metadata
- Optional scripts/ - Helper scripts

## Key Skills We Use

### For This Project
- **github** - GitHub operations (we use gh CLI)
- **deployment** - Railway deployment
- **internet-researcher** - Web research
- **debugging** - Debug apps

## Skill Structure Example

```yaml
---
name: skill-name
description: What it does
metadata:
  openclaw:
    emoji: 🎯
    requires:
      bins: [command]
```

---
*Version: 1.0.0*
