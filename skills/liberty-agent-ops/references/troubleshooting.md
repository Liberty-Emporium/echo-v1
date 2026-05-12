# Liberty Agent — Troubleshooting Guide

## "Machine not showing in dashboard"

| Cause | How to Confirm | Fix |
|-------|---------------|-----|
| Agent not running | `pgrep -f liberty_agent.py` returns nothing | Start it (see SKILL.md) |
| Missing CLIENT_ID/INSTALL_TOKEN | Logs say "Auto-register skipped" | Restart with credentials |
| Wrong CLIENT_ID | Logs say "401" or link-machine fails | Check client UUID in dashboard |
| Portal URL wrong | Logs show connection errors to wrong host | Set `LIBERTY_PORTAL_URL=https://agent.install.alexanderai.site` |
| socketio not installed | Logs: `ModuleNotFoundError: No module named 'socketio'` | `pip install "python-socketio[client]" websocket-client` |
| python3 not found | Service fails to start | Check `which python3`, update ExecStart path |
| systemd not available | Service install silently failed | Use background fallback (nohup) |

## "Connected but no machine info"

Machine shows as connected but no hostname/OS data:
- Agent connected but `machine_info` event not firing
- Usually means an old version of `liberty_agent.py` — re-download:
  ```bash
  curl -fsSL https://raw.githubusercontent.com/Liberty-Emporium/Hermes-Workspace-Alexander-AI/main/liberty_agent.py -o ~/liberty_agent.py
  pkill -f liberty_agent.py; sleep 1
  systemctl --user restart liberty-agent 2>/dev/null || \
    LIBERTY_CLIENT_ID="..." LIBERTY_INSTALL_TOKEN="..." nohup python3 ~/liberty_agent.py >> ~/.liberty-agent/agent.log 2>&1 &
  ```

## "Auto-register skipped" in logs

This means `CLIENT_ID` env var is empty. Agent runs but doesn't link.
Fix: restart with credentials — see SKILL.md "Fix: Restart with Correct Credentials"

## "Connection refused" / "Cannot connect to portal"

Portal (`agent.install.alexanderai.site`) may be down or the support dashboard service crashed.
Check: `curl -s https://agents.alexanderai.site/health` → should return `{"ok":true,...}`
If down: check Railway deployment for Alexander-AI-Support-Dashboard service.

## Systemd "Failed to connect to bus" error

Customer's Linux distro doesn't support systemd user services.
Fix: use background fallback with `@reboot` crontab instead:
```bash
(crontab -l 2>/dev/null; echo "@reboot LIBERTY_CLIENT_ID=... LIBERTY_INSTALL_TOKEN=... LIBERTY_AGENT_TYPE=hermes python3 ~/liberty_agent.py >> ~/.liberty-agent/agent.log 2>&1") | crontab -
```

## Reading logs

```bash
# Live tail
tail -f ~/.liberty-agent/agent.log

# Last 50 lines
tail -50 ~/.liberty-agent/agent.log

# systemd journal (if using systemd)
journalctl --user -u liberty-agent -n 50 --no-pager
```

## Verifying connection from Echo's side

```python
import json, urllib.request

BASE = "https://agents.alexanderai.site"
token = # get from dashboard API skill

machines = json.loads(urllib.request.urlopen(
    urllib.request.Request(f"{BASE}/api/machines",
    headers={"Authorization": f"Bearer {token}"}), timeout=10).read())

for m in machines:
    print(f"{'🟢' if m['online'] else '⚫'} {m['hostname']} | {m['machine_id'][:12]} | client={m['client_id']}")
```
