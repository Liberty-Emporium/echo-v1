---
name: ecdash-bridge
description: Poll EcDash for pending tasks from Jay and execute them. Use when receiving a heartbeat or cron trigger with "EcDash task" context, or when Jay says "check EcDash tasks", "execute EcDash request", or "EcDash bridge". This skill lets EcDash (the dashboard AI) dispatch real code tasks to Echo (OpenClaw) for execution.
---

# EcDash Bridge

Polls EcDash's task queue, executes pending tasks, and reports results back.

## How It Works

1. Fetch pending tasks from `/api/echo-bridge` (authenticated)
2. For each `pending` task: read the request, execute it (write code, push to GitHub, etc.)
3. PATCH `/api/echo-bridge/<task_id>` with status=done and the result
4. EcDash shows Jay the completion in the bridge panel

## Authentication

The EcDash API requires a session cookie. Use the API token endpoint instead:

```bash
# Get a token (one-time setup — store in /root/.secrets/ecdash_token)
curl -s -X POST https://jay-portfolio-production.up.railway.app/api/token \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"DASHBOARD_PASSWORD","label":"echo-bridge","expires_days":365}'
```

Store token: `/root/.secrets/ecdash_token`

## Poll for Tasks

```python
import json, urllib.request, os

TOKEN = open('/root/.secrets/ecdash_token').read().strip()
BASE  = 'https://jay-portfolio-production.up.railway.app'

def get_pending_tasks():
    req = urllib.request.Request(
        f'{BASE}/api/echo-bridge',
        headers={'Authorization': f'Bearer {TOKEN}'}
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        tasks = json.loads(r.read())
    return [t for t in tasks if t['status'] == 'pending']

def complete_task(task_id, response, status='done'):
    payload = json.dumps({'status': status, 'response': response}).encode()
    req = urllib.request.Request(
        f'{BASE}/api/echo-bridge/{task_id}',
        data=payload,
        headers={
            'Content-Type': 'application/json',
            'X-Echo-Secret': open('/root/.secrets/ecdash_webhook_secret').read().strip()
        },
        method='PATCH'
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())
```

## Task Execution Guide

When you receive a task, interpret it and execute:

| Task contains | Action |
|---|---|
| "fix", "bug", "error", "crash" | Clone affected repo, find + fix the bug, push |
| "add feature", "build", "create" | Implement feature in the relevant repo, push |
| "update", "change", "improve" | Make targeted edit, validate, push |
| "brief me", "status", "how is" | Pull git log + health check, return report |
| "check all apps" | Run health check on all 9 URLs, return results |
| "save brain", "backup" | Run save-brain.sh, return confirmation |

## After Executing

Always:
1. PATCH the task with status=`done` and a clear summary of what was done
2. Include the GitHub commit URL if code was pushed
3. Keep response concise — EcDash shows it to Jay in the bridge panel

## Secrets Location

- `/root/.secrets/ecdash_token` — EcDash API bearer token
- `/root/.secrets/ecdash_webhook_secret` — Shared secret for PATCH auth
- `/root/.secrets/github_token` — For pushing code changes
