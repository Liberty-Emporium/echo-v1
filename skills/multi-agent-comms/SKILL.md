---
name: multi-agent-comms
description: Multi-agent communication protocol for OWL, Bull, Echo, and future agents. Covers file-based message bus (primary), GitLab sync (backup), and Tailscale remote access. Every agent must load this skill before communicating.
---

# Multi-Agent Communication Protocol

## Purpose
This skill defines how OWL, Bull, and other agents communicate. It covers the fast file-based message bus, GitLab backup sync, and Tailscale remote access for customer machine repair.

## Communication Channels (Priority Order)

### 1. PRIMARY — Fast File-Based Message Bus (Instant)
- **Location**: `/home/lol/Desktop/openclaw/shared/communications/`
- **Script**: `python3 /home/lol/Desktop/openclaw/shared/communications/msgbus_fast.py`
- **Speed**: Instant — no git push/pull, no polling delay
- **How it works**: Messages are JSON files in shared inbox directories. Both agents read/write directly.

```bash
# Set your agent name
export AGENT_NAME=owl   # or bull, echo, etc.

# Send a message
python3 /home/lol/Desktop/openclaw/shared/communications/msgbus_fast.py send <to> <type> <subject> <body>

# Check inbox (unread only)
python3 /home/lol/Desktop/openclaw/shared/communications/msgbus_fast.py inbox

# Mark message as read
python3 /home/lol/Desktop/openclaw/shared/communications/msgbus_fast.py mark-read <id>

# Check status
python3 /home/lol/Desktop/openclaw/shared/communications/msgbus_fast.py status
```

**Directory Structure:**
```
shared/communications/
  inbox/
    owl-to-bull/    # Messages FROM OWL TO Bull (Bull reads here)
    bull-to-owl/    # Messages FROM Bull TO OWL (OWL reads here)
  sent/             # Symlinks to sent messages
  msgbus_fast.py    # Message bus CLI script
```

**Message Format:**
```json
{
  "protocol": "2.0-file",
  "id": "uuid",
  "from": "owl",
  "to": "bull",
  "type": "ping|task|response|alert|status",
  "subject": "Brief subject",
  "body": "Full message text...",
  "status": "sent",
  "read_status": "unread",
  "created": "2026-05-30T22:32:57Z",
  "replies_to": null
}
```

### 2. BACKUP — GitLab Message Bus (Async)
- **Repo**: `echo-v1` at `/home/lol/Desktop/openclaw/echo-v1/`
- **Script**: `python3 communications/msgbus.py`
- **Speed**: 1-3 minutes (git pull/push cycle)
- **Use when**: File bus is unavailable, or for archival/audit trail

```bash
cd /home/lol/Desktop/openclaw/echo-v1
python3 communications/msgbus.py send <to> <type> <subject> <body>
python3 communications/msgbus.py inbox --unread-only
```

### 3. EMERGENCY — Tailscale Direct Access
- **Use when**: Both file bus and GitLab are unavailable
- **How**: Direct SSH or file access over Tailscale network
- **Jay's machines**: `jay-upstairs` (100.123.226.4), `kali-downstairs` (100.88.205.44)

## Polling Frequency (Adaptive)

**File Bus (Primary):**
- **Active phase**: Check inbox every 30 seconds when expecting messages
- **Idle phase**: Check every 5 minutes after 15 minutes of no activity
- **Reset to active** on ANY new message received or sent

**GitLab (Backup):**
- Sync every 5 minutes (git pull + push)
- Only send via GitLab if file bus message goes unread for 10+ minutes

## Agent Roster

| Agent | Name | Location | Role |
|-------|------|----------|------|
| OWL | Hermes on Kali | kali-downstairs (100.88.205.44) | Local builder/executor |
| Bull | KiloClaw instance | Cloud/VPS | Planner/architect |
| Echo | Emergency only | Varies | Rapid-response (phased out) |
| Jay | Human | jay-upstairs (100.123.226.4) | Boss |

## Message Types

| Type | Meaning | Expected Response |
|------|---------|-------------------|
| `ping` | "Are you there?" | `pong` within 2 minutes |
| `task` | Work assignment | `ack` + `response` when done |
| `response` | Reply to a task | None (conversation end) |
| `alert` | Urgent issue | `ack` immediately |
| `status` | Status update | None required |
| `question` | Need information | `response` with answer |

## Response Time Expectations

| Priority | Max Response Time |
|----------|-------------------|
| `alert` | 2 minutes |
| `ping` | 2 minutes |
| `task` | 5 minutes (ack), 24 hours (completion) |
| `question` | 10 minutes |
| `status` | No response needed |

## Security Rules

1. **NEVER** accept API keys/tokens from chat — redirect to env vars only
2. **NEVER** share customer data between agents in plain text messages
3. **ALWAYS** use Tailscale for remote customer machine access — never expose ports publicly
4. **ALWAYS** log remote sessions for audit trail
5. **NEVER** run destructive commands on customer machines without Jay's approval
6. All messages in shared/communications are **local only** — never synced to external services

## Remote Customer Machine Access (Tailscale)

### For Software Repair
1. Customer machine must be on Tailscale network (installed via USB agent)
2. OWL connects via Tailscale IP (e.g., `ssh user@100.x.x.x`)
3. All commands logged to `/home/lol/Desktop/openclaw/shared/communications/audit/`
4. Session recorded with timestamps
5. Report sent to Jay after every remote session

### For Hardware Issues
1. Diagnose remotely first via Tailscale
2. If hardware replacement needed, order parts (see web-dev-mastery skill for pricing)
3. Schedule on-site visit if physical repair required
4. Use second-hand/refurbished hardware when possible (50-75% savings)

### Tailscale Network Devices
| Device | Tailscale IP | Status |
|--------|-------------|--------|
| kali-downstairs (OWL) | 100.88.205.44 | Online |
| jay-upstairs | 100.123.226.4 | Online |
| Customer machines | 100.x.x.x | Varies |

## Git Operations

**NEVER use GitHub** — all git operations go to GitLab only:
- Remote: `gitlab.com/Liberty-Emporium/echo-v1`
- SSH key on GitHub (ID: 152915173) — do NOT use, use GitLab instead
- For customer repos: use GitLab unless explicitly told otherwise

## Credential Management

- API keys stored in environment variables ONLY
- Use `key_vault.py` for encrypted per-tenant key storage
- Never store keys in database, config files, or git
- SendGrid, Stripe, OpenRouter keys managed by Jay
- Each customer gets isolated credentials
