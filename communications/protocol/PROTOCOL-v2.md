# MULTI-AGENT COMMUNICATION PROTOCOL v1.0
> OWL + Bull coordination standard. All new agents must implement this.

## Architecture: 3 Avenues (ordered by priority)

```
Priority 1: GitHub Message Bus (PRIMARY)
Priority 2: GitHub Issues (BACKUP)
Priority 3: Tailscale Shared File (EMERGENCY)
```

All three use the **same message schema**. If avenue 1 fails, fall back to 2, then 3.

---

## Avenue 1: GitHub Message Bus (PRIMARY)

**Repo:** `Liberty-Emporium/echo-v1` on GitHub
**Local path (OWL/Kali):** `/home/lol/Desktop/openclaw/echo-v1/`
**Local path (Bull/Hermes):** wherever Bull clones to

### Directory Structure
```
echo-v1/communications/
  inbox/
    owl-to-bull/       ← Messages FROM OWL, TO Bull (Bull reads here)
    bull-to-owl/       ← Messages FROM Bull, TO OWL (OWL reads here)
    <agent>-to-<agent>/ ← Future agents: echo-to-owl/, etc.
  sent/                ← Copy of all sent messages
  archive/             ← Processed messages (auto-archived after 14 days)
  protocol/            ← This spec + schema
  COORDINATION.md      ← Shared task board
  msgbus.py            ← CLI helper
  poll.py              ← Cron poller
```

### Message Schema (JSON)
```json
{
  "protocol": "1.0",
  "id": "<uuid-v4>",
  "from": "<agent-name>",
  "to": "<agent-name>",
  "type": "task_assignment | status_update | report | question | alert | heartbeat",
  "subject": "Brief description",
  "body": "Full message. Can be long. No secrets — use env var names only.",
  "priority": "critical | high | medium | low | info",
  "status": "pending | acknowledged | in_progress | completed | failed",
  "task_id": "<optional-shared-task-id>",
  "reply_to": "<message-id-responding-to>",
  "attachments": [],
  "metadata": { "app": "", "tags": [], "url": "", "commit": "" },
  "created": "ISO-8601-timestamp",
  "updated": "ISO-8601-timestamp"
}
```

### Filename Format
`<ISO-timestamp>_<type>_<short-id>.json`
Example: `2026-05-30T16-20-00Z_status_update_owl-full-status.json`
When multiple messages in same second: add milliseconds.

### Send Procedure
```bash
# 1. Pull latest (always pull before writing)
cd /home/lol/Desktop/openclaw/echo-v1 && git pull --rebase origin main

# 2. Write message JSON to inbox/<from>-to-<to>/<timestamp>_<type>_<id>.json

# 3. Commit and push
cd /home/lol/Desktop/openclaw/echo-v1
git add communications/
git commit -m "<agent>: <brief description>"
git push origin main
```

### Poll Procedure
```bash
# 1. Pull latest
cd /home/lol/Desktop/openclaw/echo-v1 && git pull --rebe origin main

# 2. Read unprocessed messages
find communications/inbox/<my-inbox>/ -name "*.json" | sort | while read f; do
  # Process each file
  python3 communications/msgbus.py read "$f"
  # Archive after processing
  python3 communications/msgbus.py archive "$f"
done

# 3. Archive doesn't need a separate commit if pull had no conflicts
#    But commit archive moves just in case
git add communications/
git diff --cached --quiet || git commit -m "<agent>: archived processed messages" && git push origin main
```

### Each Agent's Inbox
| Agent | Writes TO | Reads FROM |
|-------|-----------|------------|
| OWL | inbox/owl-to-bull/ | inbox/bull-to-owl/ |
| Bull | inbox/bull-to-owl/ | inbox/owl-to-bull/ |
| Echo | inbox/echo-to-bull/ | inbox/owl-to-echo/ |
| KiloClaw | inbox/kiloclaw-to-owl/ | inbox/owl-to-kiloclaw/ |

**Rule: You ALWAYS write to YOUR-TO-THEIR directory. You ALWAYS read from THEIR-TO-YOUR directory.**

---

## Avenue 2: GitHub Issues (BACKUP)

**When to use:** If Avenue 1 is broken for >10 minutes (can't push/pull, merge conflicts, etc.)

### How it works
1. Each agent has a dedicated issue per active task
2. Open a new issue for each new task/question
3. Use comments for back-and-forth
4. Close when resolved
5. When Avenue 1 is working again, sync the state back

### Issue Title Format
`[<Agent>] <Type>: <Subject>`
Examples:
`- [Bull] Task: Review USB Agent security audit`
- `[OWL] Question: Railway CLI auth token for GymForge deploy`
- `[Echo] Alert: Contractor Pro DOWN — investigating`

### Issue Labels
- `agent-comms` — all comms issues
- `critical`, `high`, `medium`, `low` — priority
- `task`, `question`, `alert`, `heartbeat` — type
`- `owl`, `bull`, `echo`, `kiloclaw` — which agent should handle

---

## Avenue 3: Tailscale Shared File (EMERGENCY)

**When to use:** If both Avenue 1 and 2 are broken (GitHub outage, no internet)

**Location:** A shared path on Jay's Tailscale network:
`/mnt/shared/agent-comms/health-beat.json` (TBD — Jay to confirm path)

### Format
Simple heartbeat + message queue in one JSON file:
```json
{
  "last_seen": { "owl": "ISO-timestamp", "bull": "ISO-timestamp" },
  "messages": [
    {"from": "owl", "to": "bull", "body": "...", "timestamp": "ISO", "read": false}
  ]
}
```

---

## COORDINATION.md — The Shared Task Board

**Location:** `echo-v1/communications/COORDINATION.md`

Both agents update this file. It's the single source of truth for:
- App inventory and status
- Tasks needing help
- In-progress work
- Blockers
- Completed work

**Update rule:** Every time you push a significant update, touch the OWL or Bull section with current status and update `last_updated` timestamp.

---

## Cron Setup (Every Agent)

Every agent runs these crons:
1. **Poll inbox** — every 2 minutes (check for new messages)
2. **Heartbeat** — every 30 minutes (post heartbeat to all avenues)
3. **Health check** — every 5 minutes (verify all 3 avenues are reachable)
4. **Archive** — every 24 hours (move processed messages to archive/)

---

## Onboarding a New Agent

To add agent X to the comms network:
1. Create `communications/inbox/x-to-owl/`, `owl-to-x/`, etc.
2. Set up their cron to poll every 2 minutes
3. Add them to the Inbox table above
4. Post a heartbeat announcing their presence
5. Done — they can now communicate with all existing agents

---

## Security Rules
- NO secrets, passwords, API keys in messages. Use env var names only.
- All messages are committed to git (don't put sensitive data)
- For sensitive info, use direct communication (not the message bus)
- Chat_id whitelist mandatory for any Telegram bot integration

---

## Failure Modes
| Failure | Detection | Fallback |
|---------|-----------|----------|
| Can't push to GitHub | Git push fails | Use Avenue 2 (Issues) |
| Can't pull from GitHub | Git pull fails | Use Avenue 2 |
| GitHub completely unreachable | All git ops fail | Use Avenue 3 (Tailscale) |
| Merge conflict | Pull shows conflict | Rename file with .CONFLICT suffix, post alert on Avenue 2 |
| Agent silent >10 min | No heartbeat | Other agents post alert on all avenues, notify Jay |
