# SKILL: Tailscale — Remote Access to Jay's Machines
_Echo KiloClaw skill — connects this KiloClaw instance to Jay's Tailnet so I can reach his computers._

## When to Use This Skill
- After a fresh container start / reboot / any time `tailscale status` fails
- When Jay says "connect to my computer" or "remote in"
- When I need to run a command on Jay's machine over the network
- When the watchdog cron reports Tailscale is down

## Quick Recovery (Step by Step)

### Step 1 — Run the start script (handles everything automatically)
```bash
bash /usr/local/bin/tailscaled-start.sh
```
This script:
1. Installs Tailscale if binaries are missing (apt)
2. Starts `tailscaled` daemon if not running
3. Re-authenticates if logged out using saved key
4. Reports final `tailscale status`

### Step 2 — Verify
```bash
tailscale status
tailscale ping 100.123.226.4   # Jay's Linux machine
```

## Manual Recovery (If Start Script Missing)

```bash
# 1. Reinstall
curl -fsSL https://tailscale.com/install.sh | sh

# 2. Start daemon
/usr/sbin/tailscaled --tun=userspace-networking --socks5-server=localhost:1055 \
  --statedir=/root/.tailscale-state > /tmp/tailscaled.log 2>&1 &
sleep 4

# 3. Auth (key is in /root/.secrets/tailscale_authkey)
tailscale up --authkey=$(cat /root/.secrets/tailscale_authkey) --accept-routes

# 4. Check
tailscale status
```

## Recreate Start Script (If Also Missing)
Write `/usr/local/bin/tailscaled-start.sh` with the logic above — see `memory/tailscale.md` for the full content. Then `chmod +x` it.

## Recreate Watchdog Cron (If Missing)
```
cron add:
  name: tailscaled-watchdog
  schedule: every 60s
  sessionTarget: isolated
  payload: agentTurn — "Run bash /usr/local/bin/tailscaled-start.sh 2>&1 | tail -5 and reply with output"
  delivery: none
```

## Known Nodes on Tailnet
| Machine | IP | Notes |
|---------|----|----|
| KiloClaw (this machine) | 100.120.23.109 | Changes if container fully rebuilt |
| Jay's Linux (`mingo`) | 100.123.226.4 | Main development machine |

## Auth Key
- **Stored at:** `/root/.secrets/tailscale_authkey`
- **Account:** Liberty-Emporium@github at https://login.tailscale.com
- **Renew at:** https://login.tailscale.com/admin/settings/keys
- If expired: Jay generates a new key → `echo -n "<new-key>" > /root/.secrets/tailscale_authkey`

## Connecting to Jay's Machine
Once Tailscale is up, I can reach `100.123.226.4` directly:
```bash
# Ping test
tailscale ping 100.123.226.4

# SSH (if SSH server is running on Jay's machine and Tailscale ACLs allow it)
ssh mingo@100.123.226.4

# HTTP (if a web service is running)
curl http://100.123.226.4:<port>/
```

## Tailnet Details
- **Tailnet:** tail5f8e8b.ts.net
- **Account:** Liberty-Emporium@github
- **DERP region:** iad (best latency to Jay in Liberty, NC)
