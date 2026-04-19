# SKILLS.md - Echo's Skills System

This is **the most important file** for Echo's long-term growth and memory.

## The Skills Philosophy

**Echo can create skills, store them on GitHub, and use them forever.**

When Echo creates a skill:
1. Build the skill with Python files, scripts, documentation
2. Store it in `skills/custom/` on GitHub
3. Document it in this file
4. Use it anytime in the future

## Default Skills (from OpenClaw/KiloClaw)

See the KiloClaw skill registry for the full list of built-in skills.

## Custom Skills — Stored in `skills/custom/`

### Session Skills (Built 2026-04-11 to 2026-04-13)
See `skills/custom/README.md` for full descriptions.

Key skills available:
- `app-auditor` — Audit a Flask app for bugs, security issues, missing features
- `security-scan` — Scan code for secrets, SQL injection, auth flaws
- `security-shield` — Harden an app against common attack vectors
- `testing-django` / `testing-e2e` / `testing-api` — Test strategy generators
- `smoke-test` — Quick functional smoke test for a deployed URL
- `internet-researcher` — Deep research on any topic
- `legacy-whisper` — Understand and document legacy codebases
- `refactor-sense` — Identify and plan code refactors
- `visual-audit` — Screenshot + visual review of a deployed UI
- `route-audit` — Map all Flask/Django routes and check for issues
- `github-integration` — GitHub operations: push, PR, branch, commit
- `mentor-mode` — Explain code concepts to learners

### New Skills (Built 2026-04-19)
- `railway-deploy` — Full Railway deploy cycle: push → wait → verify health. Has all app URLs.
- `stripe-setup` — Add Stripe billing (subscriptions + one-time) to any Flask app
- `new-flask-app` — Scaffold a complete Liberty-Emporium Flask app with all standard building blocks
- `health-checker` — Check all 8 apps health in one sweep
- `github-token-refresh` — Detect expired tokens, guide renewal process

### Skills Needed (Still TODO)
- `pdf-extractor` — Download PDF, extract pages as base64 PNG (HIGH PRIORITY)
- `base64-image` — Convert any image to inline HTML data URI (MEDIUM)
- `qr-generator` — Generate QR code as base64 PNG (MEDIUM)
- `apt-toolbox` — Pre-install common tools at session start (LOW)
- `email-sender` — Send emails via SMTP from any app (MEDIUM)
- `grace-updater` — Push updates to Grace app specifically (LOW)

## Skills Storage Location

All custom skills stored at:
```
https://github.com/Liberty-Emporium/echo-v1/tree/main/skills/custom/
```

---
*Version: 1.2.0 - Updated 2026-04-19*
