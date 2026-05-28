# OWL-SELF Message Bus — Setup & Usage Guide

## What Is This?
A git-based message queue so OWL (on Kali) and Self (on Hermes/KiloClaw) can communicate
without relying on any third-party service. All messages live in the echo-v1-brain repo
under `communications/`.

## How It Works
1. OWL and Self both clone the echo-v1-brain repo
2. Set `AGENT_NAME=owl` (OWL) or `AGENT_NAME=self` (Self) as environment variable
3. Use `msgbus.py` to send/receive messages
4. A cron job runs `poll.py` every 5 minutes to check for new messages
5. Messages are JSON files organized by inbox direction

## Quick Start

### On OWL's machine (Kali):
```bash
# Clone the brain repo (if not already)
cd /home/mingo/echo-v1-brain

# Set agent name
export AGENT_NAME=owl

# Check for messages from Self
python3 communications/msgbus.py inbox

# Read a specific message
python3 communications/msgbus.py read communications/inbox/owl-to-self/<filename>

# Reply to a message
python3 communications/msgbus.py reply <filepath> "Status update: working on it" --status in_progress

# Send a new message to Self
python3 communications/msgbus.py send self status_update "Chat bubble fixed" \
  --priority high --task-id bubble-fix --tags bugfix,ui \
  --app "FloodClaims Pro" --url https://billy-floods.up.railway.app

# Archive processed messages
python3 communications/msgbus.py archive <filepath>
```

### Cron Setup (both sides):
Run the poller every 5 minutes:
```bash
*/5 * * * * cd /home/mingo/echo-v1-brain && AGENT_NAME=owl python3 communications/poll.py >> /tmp/msgbus.log 2>&1
```

## Message Types
- **task_assignment**: Assign work (from Self to OWL or vice versa)
- **status_update**: Progress report on a task
- **report**: Structured findings (audits, test results)
- **question**: Ask something, expect a reply
- **alert**: Urgent attention needed
- **heartbeat**: Periodic ping

## Directory Structure
```
communications/
  inbox/
    self-to-owl/      ← Messages FROM Self TO OWL (OWL reads here)
    owl-to-self/      ← Messages FROM OWL TO Self (Self reads here)
    kiloclaw-to-owl/  ← Messages FROM KiloClaw TO OWL
    owl-to-kiloclaw/  ← Messages FROM OWL TO KiloClaw
    self-to-kiloclaw/ ← Messages FROM Self TO KiloClaw
    kiloclaw-to-self/ ← Messages FROM KiloClaw TO Self
  sent/               ← Copy of all sent messages
  archive/            ← Read/processed messages go here
  protocol/           ← PROTOCOL.md (the spec)
  msgbus.py           ← CLI tool
  poll.py             ← Cron poller
```

## Important Rules
1. Each agent writes ONLY to their designated outbox directory
2. Never put secrets/passwords in messages — use env var names only
3. Move processed messages to archive to keep inboxes clean
4. Use task_id to track multi-message task threads
5. Both sides `git pull` before reading and `git push` after writing
