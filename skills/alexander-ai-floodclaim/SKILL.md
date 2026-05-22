---
name: alexander-ai-floodclaim
description: Work on the FloodClaim Pro app — professional flood damage assessment SaaS built with Python Flask, deployed on Railway.
---

# FloodClaim Pro Skill

## Overview
Professional flood damage assessment SaaS for insurance adjusters and homeowners.

- **Repo:** Liberty-Emporium/alexander-ai-floodclaim
- **Live URL:** https://floodclaim-pro-production.up.railway.app (check current Railway URL)
- **Stack:** Python Flask + SQLite/PostgreSQL + OpenRouter AI
- **Deploy:** Railway (auto-deploy from main)

## Clone
```bash
cd /root/.openclaw/workspace
git clone https://$(cat /root/.secrets/github_token)@github.com/Liberty-Emporium/alexander-ai-floodclaim.git
```

## Key Features
- Photo upload + AI damage assessment
- Room-by-room damage documentation
- PDF report generation
- Claim amount estimation

## Env Vars (Railway)
- `OPENROUTER_API_KEY` — AI assessments
- `SECRET_KEY` — Flask session key
- `DATABASE_URL` — PostgreSQL (Railway provides)

## Push Workflow
```bash
cd /root/.openclaw/workspace/alexander-ai-floodclaim
git add -A && git commit -m "fix: description" && git push
# Railway auto-deploys from main
```
