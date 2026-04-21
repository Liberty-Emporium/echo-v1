# BOOTSTRAP.md — Echo Server Setup
_Run this after every fresh KiloClaw instance to restore full capability._
_Last updated: 2026-04-20_

---

## 🖥️ Server Info

- **OS:** Debian GNU/Linux 12 (Bookworm)
- **Python:** 3.11.2
- **Node:** v24.14.1
- **Shell:** /bin/bash

---

## ✅ What's Installed (as of 2026-04-20)

### System Tools (pre-installed on KiloClaw)
| Tool | Path | Notes |
|------|------|-------|
| `git` | /usr/bin/git | Version control |
| `curl` | /usr/bin/curl | HTTP client |
| `python3` | /usr/bin/python3 | Python 3.11.2 |
| `node` | /usr/local/bin/node | Node v24.14.1 |
| `npm` | /usr/local/bin/npm | Node package manager |
| `go` | /usr/local/go/bin/go | Go compiler |

### Installed by Echo (must reinstall after reboot)
| Tool | Path | Install Command | Purpose |
|------|------|-----------------|---------|
| `bandit` | /usr/local/bin/bandit | `curl -sS https://bootstrap.pypa.io/get-pip.py \| python3 - --break-system-packages && python3 -m pip install bandit ruff --break-system-packages` | Python security scanner |
| `ruff` | /usr/local/bin/ruff | (same as above) | Python linter (800+ rules) |
| `railway` CLI | /root/.npm-global | `npm install -g @railway/cli` | Railway deployments |
| `pip` | /usr/local/bin/pip | `curl -sS https://bootstrap.pypa.io/get-pip.py \| python3 - --break-system-packages` | Python package manager |

---

## 🔑 Secrets (stored in /root/.secrets/)

> These are NOT in Git. Must be added manually or fetched from KYS after boot.

| File | Contents | How to get |
|------|----------|------------|
| `/root/.secrets/github_token` | GitHub PAT for Liberty-Emporium | Jay provides — check KYS or ask Jay |
| `/root/.secrets/gitlab_token` | GitLab PAT for Liberty-Emporium | Jay provides — check KYS or ask Jay |
| `/root/.secrets/willie_api_key` | Willie's AI Agent Widget API key | From ai-agent-widget app → Willie → Edit |
| `/root/.secrets/ecdash_token` | EcDash bridge API token (expires 2027-04-19) | From EcDash → Settings |

---

## 📁 Workspace Repos (clone after boot)

```bash
GH_TOKEN=$(cat /root/.secrets/github_token)
cd /root/.openclaw/workspace

# Core brain
git clone https://oauth2:${GH_TOKEN}@github.com/Liberty-Emporium/echo-v1.git

# Apps
git clone https://oauth2:${GH_TOKEN}@github.com/Liberty-Emporium/floodclaim-pro.git
git clone https://oauth2:${GH_TOKEN}@github.com/Liberty-Emporium/AI-Agent-Widget.git
git clone https://oauth2:${GH_TOKEN}@github.com/Liberty-Emporium/jay-portfolio.git
git clone https://oauth2:${GH_TOKEN}@github.com/Liberty-Emporium/pet-vet-ai.git
git clone https://oauth2:${GH_TOKEN}@github.com/Liberty-Emporium/Contractor-Pro-AI.git
git clone https://oauth2:${GH_TOKEN}@github.com/Liberty-Emporium/Dropship-Shipping.git
git clone https://oauth2:${GH_TOKEN}@github.com/Liberty-Emporium/Consignment-Solutions.git
git clone https://oauth2:${GH_TOKEN}@github.com/Liberty-Emporium/Liberty-Emporium-Inventory-App.git
git clone https://oauth2:${GH_TOKEN}@github.com/Liberty-Emporium/liberty-oil-website.git
```

---

## ⚡ Full Bootstrap Script

Run `/root/.openclaw/workspace/echo-v1/scripts/bootstrap.sh` after a fresh boot.
It will:
1. Install pip, bandit, ruff
2. Set up /root/.secrets/ directory
3. Configure git identity
4. Clone all repos
5. Run bug-hunter on all apps

---

## 🔧 Git Config (set after every fresh instance)

```bash
git config --global user.email "echo@liberty-emporium.ai"
git config --global user.name "Echo (KiloClaw)"
```

---

## 🚀 Apps & URLs

| App | Repo | Live URL |
|-----|------|----------|
| FloodClaim Pro | Liberty-Emporium/floodclaim-pro | https://billy-floods.up.railway.app |
| AI Agent Widget | Liberty-Emporium/AI-Agent-Widget | https://ai-agent-widget-production.up.railway.app |
| EcDash | Liberty-Emporium/jay-portfolio | https://jay-portfolio-production.up.railway.app |
| Pet Vet AI | Liberty-Emporium/pet-vet-ai | (Railway) |
| Contractor Pro AI | Liberty-Emporium/Contractor-Pro-AI | (Railway) |
| Dropship Shipping | Liberty-Emporium/Dropship-Shipping | (Railway) |
| Consignment Solutions | Liberty-Emporium/Consignment-Solutions | (Railway) |
| Liberty Inventory | Liberty-Emporium/Liberty-Emporium-Inventory-App | (Railway) |
| Liberty Oil & Propane | Liberty-Emporium/liberty-oil-website | https://liberty-oil-propane.up.railway.app |
| Keep Your Secrets (KYS) | (Railway) | https://ai-api-tracker-production.up.railway.app |

---

## 🧠 Key Constants

- **Willie agent ID:** F5J8yYT6a6GrppjviN6p8w
- **Willie FloodClaim API token:** S7LroZDvJSqzJZ304leqwQcxToJXRwF597gszWWarq4
- **EcDash bridge endpoint:** https://jay-portfolio-production.up.railway.app/api/echo-bridge
- **"my dashboard"** = https://jay-portfolio-production.up.railway.app/dashboard
