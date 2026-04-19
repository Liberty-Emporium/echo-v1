---
name: session-startup
description: Run this skill at the start of every new session to restore Echo's brain from GitHub/GitLab, load memory context, check for open todos, and confirm readiness. Use when starting a new session, when the user says "good morning", "let's get started", "wake up", or any session-opening greeting. Also use when memory files seem stale or out of date.
---

# Session Startup

Run this at the start of every session to sync brain state and get oriented.

## Sequence

### 1. Run the health check script first

```bash
bash /root/.openclaw/workspace/echo-v1/scripts/check-startup-health.sh
```

This tells you what's present and what's missing before you try anything else. Read `references/startup-checklist.md` for the full decision tree.

### 2. Restore brain from GitHub

```bash
bash /root/.openclaw/workspace/echo-v1/scripts/restore-brain.sh
```

- If it succeeds: brain files are synced into `/root/.openclaw/workspace/`
- If GitHub token missing or expired: tell Jay, ask him to paste a new one, then save it:
  ```bash
  echo "PASTE_TOKEN_HERE" > /root/.secrets/github_token && chmod 600 /root/.secrets/github_token
  ```
- If GitHub fails but GitLab works: `restore-brain.sh` handles the fallback automatically

### 3. Load today's memory

After restore, read these in order:
1. `MEMORY.md` — long-term memory (main session only — skip in group chats)
2. `memory/YYYY-MM-DD.md` for today (if exists)
3. `memory/YYYY-MM-DD.md` for yesterday (if today's is empty)

Use today's date from `session_status` or `date +%Y-%m-%d`.

### 4. Check open todos

```bash
python3 /root/.openclaw/workspace/echo-v1/tools/todo_manager.py list --status open
```

If there are high-priority items, surface them to Jay immediately.

### 5. Report readiness

Give Jay a brief startup summary:
- ✅ Brain synced (note the latest commit date)
- 📋 X open todos (list high-priority ones)
- 📅 Any calendar/memory items for today
- ⚠️ Any issues found (expired tokens, missing secrets, etc.)

Keep it short — 3-6 bullet points max. Don't dump the entire memory file.

## Common Issues & Fixes

| Problem | Fix |
|---|---|
| `/root/.secrets/github_token` missing | Ask Jay to paste new GitHub PAT |
| `/root/.secrets/gitlab_token` missing | Ask Jay to paste GitLab token |
| `echo-v1` not cloned | Clone it: `git clone https://TOKEN@github.com/Liberty-Emporium/echo-v1.git /root/.openclaw/workspace/echo-v1` |
| GitHub push blocked (secret scanning) | Never store raw tokens in MEMORY.md — reference `/root/.secrets/` only |
| GitLab force push rejected | Unprotect via API, force push, re-protect (see `sync-all-to-gitlab.sh` pattern) |

## Session End

At the end of every session, run:
```bash
bash /root/.openclaw/workspace/echo-v1/scripts/save-brain.sh
```

This commits updated memory files and pushes to both GitHub and GitLab.
