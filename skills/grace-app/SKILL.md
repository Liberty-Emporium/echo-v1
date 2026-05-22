---
name: grace-app
description: Work on Grace — the elderly care assistant app built with Python Flask, deployed on Railway.
---

# Grace App Skill

## Overview
Grace is an AI-powered elderly care assistant — helps families monitor, communicate with, and care for elderly loved ones.

- **Repo:** Liberty-Emporium/grace-app
- **Live URL:** https://grace-app.up.railway.app (verify current Railway URL)
- **Stack:** Python Flask + OpenRouter AI + SQLite
- **Deploy:** Railway (auto-deploy from main)

## Clone
```bash
cd /root/.openclaw/workspace
git clone https://$(cat /root/.secrets/github_token)@github.com/Liberty-Emporium/grace-app.git
```

## Key Features
- Daily check-in reminders
- Medication tracking
- Family communication portal
- AI assistant for elderly users (simple UI, large text)
- Emergency contact alerts

## Env Vars (Railway)
- `OPENROUTER_API_KEY`
- `SECRET_KEY`
- `DATABASE_URL`

## Push Workflow
```bash
cd /root/.openclaw/workspace/grace-app
git add -A && git commit -m "fix: description" && git push
```
