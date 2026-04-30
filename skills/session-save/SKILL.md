# Skill: session-save
Save Echo's brain and sync all repos to GitHub + GitLab at end of session.

## When to use
- End of any work session with Jay
- Before a planned restart
- Any time Jay says "save", "backup brain", "end session"
- Automatically during heartbeat if it's been >4 hours since last save

## What it does
1. Copies all workspace brain files (MEMORY.md, SOUL.md, etc.) into echo-v1 repo
2. Commits and pushes to GitHub (primary)
3. Pushes to GitLab (backup)
4. Runs sync-all-to-gitlab.sh to mirror ALL app repos to GitLab

## Run it
```bash
bash /root/.openclaw/workspace/echo-v1/scripts/save-brain.sh
```

Then sync all repos:
```bash
bash /root/.openclaw/workspace/echo-v1/scripts/sync-all-to-gitlab.sh
```

## Brain files saved
- MEMORY.md, SOUL.md, AGENTS.md, TOOLS.md, USER.md, IDENTITY.md, HEARTBEAT.md
- memory/YYYY-MM-DD.md (daily logs)
- skills/ (all custom skills including this one)

## Note on KYS encryption
KYS was deleted 2026-04-29. Brain is now pushed plaintext to private GitHub/GitLab repos.
Credentials never go in MEMORY.md — they live in /root/.secrets/ only.
