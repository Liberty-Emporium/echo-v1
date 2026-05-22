---
name: github-org-manager
description: Manage the Liberty-Emporium GitHub organization — list repos, update descriptions, change visibility, audit stale repos, fix missing metadata.
---

# GitHub Org Manager Skill

## Auth
Token at `/root/.secrets/github_token`
Note: Liberty-Emporium is a **user account**, not a GitHub org. Use `/user/repos` not `/orgs/`.

## List All Repos
```bash
curl -s -H "Authorization: token $(cat /root/.secrets/github_token)" \
  "https://api.github.com/user/repos?per_page=100&sort=updated&affiliation=owner,organization_member" \
  | python3 -c "
import json, sys
data = json.load(sys.stdin)
for r in sorted(data, key=lambda x: x['updated_at'], reverse=True):
    priv = '🔒' if r['private'] else '🌐'
    print(f\"{priv} {r['owner']['login']}/{r['name']:<40} {(r['language'] or 'n/a'):<14} {r['updated_at'][:10]}  {(r['description'] or '—')[:55]}\")
print(f'\nTotal: {len(data)}')
"
```

## Update Description
```bash
TOKEN=$(cat /root/.secrets/github_token)
curl -s -X PATCH -H "Authorization: token $TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.github.com/repos/Liberty-Emporium/REPO_NAME" \
  -d '{"description": "New description here"}'
```

## Make Repo Private
```bash
curl -s -X PATCH -H "Authorization: token $(cat /root/.secrets/github_token)" \
  -H "Content-Type: application/json" \
  "https://api.github.com/repos/Liberty-Emporium/REPO_NAME" \
  -d '{"private": true}'
```

## Archive a Repo
```bash
curl -s -X PATCH -H "Authorization: token $(cat /root/.secrets/github_token)" \
  -H "Content-Type: application/json" \
  "https://api.github.com/repos/Liberty-Emporium/REPO_NAME" \
  -d '{"archived": true}'
```

## Repos as of May 22, 2026
**42 total** | 40 public · 2 private (kiloclaw-workspace, Ronald-To-Judge)

Active (last 7 days): alexander-ai-dashboard, Emporium-and-Thrift-App, echo-v1, extra-mile-photography, Logos, Inventory-Items, alexander-ai-agent-widget, remote-repair-services, alexander-ai-voice

Live apps: sweet-spot-cakes, echo-ai, alexander-ai-contractor, alexander-ai-petvet, alexander-ai-floodclaim, alexander-ai-consignment, alexander-ai-inventory, grace-app, liberty-oil-website, Vendor-Vault, list-it-everywhere, Drop-Shipping-by-alexander-ai-solutions

## Audit Flags (as of May 2026)
- `echo-backup` — stale since Apr 9, may be superseded by echo-v1
- `Agent-Zero-Alexander-AI` / `Hermes-Workspace-Alexander-AI` — older frameworks
- `EcNot` — described as "Alt to openclaw", possibly dead experiment
- `Dropship-AI-CEO` vs `Drop-Shipping-by-alexander-ai-solutions` — two dropship repos

## Notes
- GitHub redirects from old `jay-portfolio` → `alexander-ai-dashboard`
- Use `git remote set-url origin` if clone was done before rename
