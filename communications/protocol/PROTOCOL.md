# OWL-SELF COMMUNICATION PROTOCOL v1.0

## Overview
Internal message bus between OWL (local executor on Kali) and Self (remote orchestrator via Hermes).
Messages are JSON files stored in a shared git repo (echo-v1-brain).
Both sides poll the repo for new messages and write responses.

## Architecture
```
echo-v1-brain/communications/
  inbox/
    self-to-owl/     # Messages FROM Self (Hermes) TO OWL
    owl-to-self/     # Messages FROM OWL TO Self (Hermes)
    kiloclaw-to-owl/ # Messages FROM KiloClaw TO OWL
    owl-to-kiloclaw/ # Messages FROM OWL TO KiloClaw
    self-to-kiloclaw/# Messages FROM Self TO KiloClaw
    kiloclaw-to-self/# Messages FROM KiloClaw TO Self
  sent/              # Copy of sent messages
  archive/           # Read/processed messages
  protocol/          # This file + schema definitions
```

## Message Schema
All messages are JSON files. Filename format: `YYYY-MM-DDTHH-MM-SSZ_<type>_<id>.json`

```json
{
  "protocol": "1.0",
  "id": "uuid-v4",
  "from": "self",
  "to": "owl",
  "type": "task_assignment | status_update | report | question | alert | heartbeat",
  "subject": "Brief description",
  "body": "Full message content. Can be multi-line.",
  "priority": "critical | high | medium | low | info",
  "status": "pending | in_progress | completed | failed | acknowledged",
  "task_id": "optional-shared-task-id",
  "reply_to": "message-id-responding-to",
  "attachments": ["file-paths"),
  "metadata": {
    "app": "FloodClaims Pro",
    "url": "https://billy-floods.up.railway.app",
    "commit": "abc123",
    "tags": ["security", "bug", "feature"]
  },
  "created": "ISO-8601-timestamp",
  "updated": "ISO-8601-timestamp"
}
```

## Message Types

### task_assignment
Assign work from one agent to another. Contains detailed instructions.
Expected response: `status_update` (acknowledged → in_progress → completed/failed)

### status_update
Progress report on a running task. Updates the status field.

### report
Structured findings (audit results, test results, deployment reports).
May include `attachments` pointing to report files.

### question
Something one agent needs answered by the other. The other agent should
respond with another `question` message (answer) or a `report`.

### alert
Something urgent that needs attention. High/critical priority.

### heartbeat
Periodic "I'm alive" check. Low priority. Response expected within 5 min.

## Protocol Rules

### Message Creation
1. Generate a UUID v4 for the message ID
2. Use ISO 8601 UTC timestamps: `2026-05-28T22:00:00Z`
3. Write to `inbox/<recipient>/` directory
4. Copy to `sent/` for sender's records
5. Commit and push to git repo

### Message Processing
1. Poll inbox directory (git pull)
2. Sort by timestamp (oldest first)
3. Parse each JSON file
4. Process based on type
5. Update status in the file (read it, modify, write back)
6. Move processed messages to `archive/`

### Conflict Resolution
- Both sides should NOT write to the same directory simultaneously
- Each side writes ONLY to their designated sender directory
- If a merge conflict occurs, both messages are preserved (rename with suffix)

### Polling Frequency
- Normal: every 5 minutes
- Urgent/critical: every 1 minute (switch to fast-poll on alert)
- Heartbeat: every 30 minutes

### Dead Letter
Messages older than 48h with status still "pending" should be moved to `archive/dead-letter/`
and an alert should be generated.

## Security
- No secrets/passwords in message bodies
- Use environment variable names, not values
- All messages are committed to git (don't put sensitive data here)
- For sensitive info, use direct communication channels
