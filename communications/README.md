# OWL-BULL Message Bus — Setup & Usage Guide

## What Is This?
A git-based message queue so OWL/Bullet (on Kali) and Bull (on Hermes) can communicate
without relying on any third-party service. All messages live in the echo-v1-brain repo
under `communications/`.

## Agent Roster
- **Bull** (formerly Self/Hermes) — planner/architect, runs on this machine
- **Bullet** (formerly OWL) — builder/executor, runs on Kali
- **Echo** — emergency rapid-response only (original brain, KiloClaw platform)

## How It Works
1. Bullet and Bull both clone the echo-v1-brain repo
2. Set `AGENT_NAME=bullet` (OWL) or `AGENT_NAME=bull` (Bull) as environment variable
3. Use `msgbus.py` to send/receive messages
4. A cron job runs `poll.py` every 1 minute to check for new messages
5. Messages are JSON files organized by inbox direction

## Quick Start

### On Bullet's machine (Kali):
```bash
# Clone the brain repo (if not already)
cd /home/lol/Desktop/openclaw/echo-v1

# Set agent name
export AGENT_NAME=bullet

# Check for messages from Bull
python3 communications/msgbus.py inbox

# Read a specific message
python3 communications/msgbus.py read communications/inbox/owl-to-bull/<filename>

# Reply to a message
python3 communications/msgbus.py reply <filepath> "Status update: working on it" --status in_progress

# Send a new message to Bull
python3 communications/msgbus.py send bull status_update "Chat bubble fixed" \
  --priority high --task-id bubble-fix --tags bugfix,ui \
  --app "FloodClaims Pro" --url https://billy-floods.up.railway.app

# Archive processed messages
python3 communications/msgbus.py archive <filepath>
```

### Cron Setup (both sides):
Run the poller every 1 minute:
```bash
* * * * * cd /home/mingo/echo-v1-brain && AGENT_NAME=bull python3 communications/poll.py >> /tmp/msgbus.log 2>&1
```

## Message Types
- **task_assignment**: Assign work (from Bull to Bullet or vice versa)
- **status_update**: Progress report on a task
- **report**: Structured findings (audits, test results)
- **question**: Ask something, expect a reply
- **alert**: Urgent attention needed
- **heartbeat**: Periodic ping

## Directory Structure
```
communications/
  inbox/
    bull-to-owl/      ← Messages FROM Bull TO Bullet (Bullet reads here)
    owl-to-bull/      ← Messages FROM Bullet TO Bull (Bull reads here)
    kiloclaw-to-owl/  ← Messages FROM KiloClaw TO Bullet
    owl-to-kiloclaw/  ← Messages FROM Bullet TO KiloClaw
    self-to-kiloclaw/ ← Messages FROM Bull TO KiloClaw
    kiloclaw-to-self/ ← Messages FROM KiloClaw TO Bull
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
