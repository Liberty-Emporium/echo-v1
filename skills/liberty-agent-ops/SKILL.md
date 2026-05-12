---
name: liberty-agent-ops
description: 'Install, debug, restart, and manage Liberty Agent on customer machines. Liberty Agent is the silent background service that keeps customer machines connected to Jay''s support dashboard (agents.alexanderai.site). Use when a machine isn''t showing up in the dashboard, Liberty Agent isn''t running, credentials need updating, or a new customer needs to be onboarded. Trigger on: "not showing in dashboard", "Liberty Agent", "machine offline", "agent not connected", "customer machine", "link machine to client".'
---

# Liberty Agent Ops

Liberty Agent (`liberty_agent.py`) is a Python Socket.IO client that runs silently on customer machines and maintains a persistent connection to `agents.alexanderai.site` so Jay can monitor and assist remotely.

**Script location on customer machine:** `~/liberty_agent.py`
**Log file:** `~/.liberty-agent/agent.log`
**Portal URL:** `https://agent.install.alexanderai.site` (Socket.IO server)
**Dashboard:** `https://agents.alexanderai.site/dashboard`

## Required Env Vars for Linking

| Var | Purpose |
|-----|---------|
| `LIBERTY_CLIENT_ID` | UUID from dashboard client record |
| `LIBERTY_INSTALL_TOKEN` | 32-char hex token from dashboard client record |
| `LIBERTY_AGENT_TYPE` | `hermes` or `agent-zero` |
| `LIBERTY_PORTAL_URL` | defaults to `https://agent.install.alexanderai.site` |

**Without CLIENT_ID + INSTALL_TOKEN the agent connects but never links to a client record — machine won't appear in dashboard.**

## Diagnosing "Not Showing in Dashboard"

Step 1 — Is it running?
```bash
pgrep -f liberty_agent.py && echo "RUNNING" || echo "NOT RUNNING"
```

Step 2 — Is it linked? (check logs)
```bash
tail -20 ~/.liberty-agent/agent.log
# Look for: "Machine registered with dashboard" or "Auto-register skipped"
```

Step 3 — Are credentials set?
```bash
# Check systemd service
cat ~/.config/systemd/user/liberty-agent.service | grep -E "CLIENT_ID|INSTALL_TOKEN"
# Or check running process env
cat /proc/$(pgrep -f liberty_agent.py)/environ 2>/dev/null | tr '\0' '\n' | grep LIBERTY
```

## Fix: Restart with Correct Credentials

```bash
# Stop old instance
pkill -f liberty_agent.py 2>/dev/null; sleep 1

# Update systemd service (Linux)
sed -i '/LIBERTY_CLIENT_ID\|LIBERTY_INSTALL_TOKEN/d' \
  ~/.config/systemd/user/liberty-agent.service 2>/dev/null
sed -i '/Environment=LIBERTY_AGENT_TYPE/a \
Environment=LIBERTY_CLIENT_ID=<CLIENT_ID>\nEnvironment=LIBERTY_INSTALL_TOKEN=<TOKEN>' \
  ~/.config/systemd/user/liberty-agent.service

systemctl --user daemon-reload
systemctl --user restart liberty-agent
systemctl --user status liberty-agent --no-pager
```

## Fix: No systemd — Background fallback

```bash
mkdir -p ~/.liberty-agent
LIBERTY_CLIENT_ID="<CLIENT_ID>" \
LIBERTY_INSTALL_TOKEN="<TOKEN>" \
LIBERTY_AGENT_TYPE="hermes" \
nohup python3 ~/liberty_agent.py >> ~/.liberty-agent/agent.log 2>&1 &
echo "PID: $!"
```

## Fresh Install on Already-Running Machine

If the customer already ran the old installer (without credentials), re-run the updated one:
```bash
curl -fsSL https://raw.githubusercontent.com/Liberty-Emporium/Hermes-Workspace-Alexander-AI/main/install.sh | bash
```
The updated installer bakes `CLIENT_ID` and `INSTALL_TOKEN` directly into the systemd service.

## Onboarding a New Customer (Full Flow)

1. **Create client in dashboard:**
```python
# See alexander-ai-dashboard-api skill
client = api("/api/clients", token, "POST",
    {"name": "Customer Name", "email": "...", "agent_type": "hermes"})
CLIENT_ID = client["id"]
INSTALL_TOKEN = client["install_token"]
```

2. **Update installer with new credentials** (if doing a mass update):
Edit `CLIENT_ID` and `INSTALL_TOKEN` constants in `install.sh` before sending to customer.

3. **Send customer the one-liner** — they run it, Liberty Agent installs + links automatically.

4. **Verify in dashboard** — machine appears within ~30s of agent starting.

## Windows (Task Scheduler)

Liberty Agent installs as a Task Scheduler entry on Windows via `install-hermes-windows.ps1`.
To check status on Windows:
```powershell
Get-ScheduledTask -TaskName "LibertyAgent" | Select-Object State
# Restart:
Stop-ScheduledTask -TaskName "LibertyAgent"; Start-ScheduledTask -TaskName "LibertyAgent"
```

## macOS (LaunchAgent)

```bash
# Check
launchctl list | grep liberty-agent
# Restart
launchctl stop com.alexander-ai.liberty-agent
launchctl start com.alexander-ai.liberty-agent
# Logs
tail -f ~/Library/Logs/liberty-agent.log
```

## Key IDs (Jay's own machine — mingo)

| Field | Value |
|-------|-------|
| Client ID | `ac13f2b8-9f94-431a-91b8-6439b4d12ab0` |
| Install Token | `b6e9431bcaed4c468e42256c52bede8e` |
| Machine | `mingo@mingo-To-Be-Filled-By-O-E-M` (Ubuntu Linux) |

See `references/troubleshooting.md` for common errors and fixes.
