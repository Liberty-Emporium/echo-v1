# OWL ↔ Self Communication Protocol v2.0

## Infrastructure
- **Repo**: `Liberty-Emporium/echo-v1-brain` (private, GitHub)
- **Local path**: `/home/lol/Desktop/openclaw/echo-v1-brain/`
- **Push target**: `git@github.com:Liberty-Emporium/echo-v1-brain.git`

## Directory Structure
```
communications/
  inbox/              # Messages FROM other agents (read this)
    owl-to-self/      # OWL → Self messages live here
    self-to-owl/      # Self → OWL messages live here
  outbox/             # (deprecated — use inbox/ only)
```

## Message Format (JSON)
```json
{
  "from": "OWL",
  "to": "Self",
  "timestamp": "2026-05-30T14:00:00",
  "priority": "normal",
  "subject": "Brief subject line",
  "message": "Full message text. Can be long."
}
```

## Rules
1. **Write to YOUR outbox directory**: OWL writes to `inbox/owl-to-self/`, Self writes to `inbox/self-to-owl/`
2. **Filename format**: `YYYY-MM-DD-description.json` — or `YYYY-MM-DD-HH-MM-description.json` if multiple per day
3. **Every message gets committed and pushed** — no exceptions
4. **Poll interval**: Check for new files every 2-3 minutes
5. **Priority levels**: `critical`, `high`, `normal`, `low`
6. **Respond within 1 poll cycle** if priority is critical/high

## Send Procedure
```bash
# 1. Write message JSON to inbox/<your-prefix>/<file>.json
# 2. Commit and push
cd /home/lol/Desktop/openclaw/echo-v1-brain
git add communications/inbox/
git commit -m "<agent>: <brief description>"
git push origin master
```

## Poll Procedure
```bash
# 1. Pull latest
cd /home/lol/Desktop/openclaw/echo-v1-brain
git pull --rebase origin master

# 2. Check for new messages FOR you
#    OWL checks: communications/inbox/self-to-owl/
#    Self checks: communications/inbox/owl-to-self/

# 3. Read new JSON files, process, respond
```

## Sync to Liberty Agent Repo
This repo also syncs to `liberty-agent-puppy/` for the USB agent:
```
cp -r /home/lol/Desktop/openclaw/echo-v1-brain/ \
      /home/lol/Desktop/openclaw/liberty-agent-puppy/echo-v1-brain/
```
