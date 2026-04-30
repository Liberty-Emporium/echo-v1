# Skill: privacy-hardening
Keep Jay's chats private and the instance hardened. Run on every boot and periodically.

## What this covers
1. Session log file permissions (most important — chats stored on disk)
2. Secrets directory permissions
3. Workspace file permission audit
4. Token leak scan (checks if secrets accidentally ended up in plain text files)

## Run it
```bash
bash /root/.openclaw/workspace/echo-v1/skills/privacy-hardening/harden.sh
```

## What it does

### 1. Lock down session logs (chat history)
Chat sessions are stored at `/root/.openclaw/agents/main/sessions/`.
OpenClaw creates them as `644` (world-readable in some environments).
This script forces them to `600` (root-only).

### 2. Lock down secrets
- `/root/.secrets/` → `700`
- `/root/.secrets/*` → `600`
- `/root/.openclaw/openclaw.json` → `600`

### 3. Scan for token leaks
Checks all `.md`, `.txt`, `.json`, `.env` files in the workspace for patterns
that look like real tokens (ghp_, glpat-, sk-, AKIA...).
Alerts if any are found OUTSIDE of `/root/.secrets/`.

### 4. Check for exposed ports
Verifies the gateway is still loopback-only (not accidentally exposed publicly).

## Run automatically
This is called by the health watchdog every 5 minutes (permissions check only — fast).
Full scan runs once per hour via the auto brain-save cron.

## What can't be fixed here
- Chat content is stored in plaintext by design (OpenClaw needs it for context)
- The only way to truly erase a conversation is to delete the session .jsonl file
- Session files are on the encrypted Fly.io volume — protected at rest
- Traffic between you and the gateway is TLS-encrypted (HTTPS via Kilo proxy)

## Your privacy architecture (summary)
```
You (browser) ──TLS──▶ Kilo edge proxy ──▶ Fly.io machine (your private sandbox)
                                                    │
                                          Gateway: loopback:3001
                                          Session logs: /root/.openclaw/agents/
                                          Secrets: /root/.secrets/ (600 perms)
```
Nobody else can reach your gateway. Your chats don't go anywhere except:
- The AI model API (for generating responses) — sent over TLS
- Your Fly.io disk (stored as .jsonl) — single-tenant, your machine only
