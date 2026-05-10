---
name: anydesk
description: "Use AnyDesk CLI to remotely connect to customer computers for hardware/software diagnosis, agent troubleshooting, and technical support sessions for Alexander AI Solutions."
metadata:
  {
    "openclaw":
      {
        "emoji": "🖥️",
        "os": ["linux", "darwin", "win32"],
        "requires": { "bins": ["anydesk"] },
        "install":
          [
            {
              "id": "apt",
              "kind": "apt",
              "package": "anydesk",
              "bins": ["anydesk"],
              "label": "Install AnyDesk (apt)",
            },
          ],
      },
  }
---

# AnyDesk Remote Support Skill

Use AnyDesk to remotely access customer computers for diagnosis, repair, and support on behalf of Alexander AI Solutions.

## When to Use

✅ **USE this skill when:**
- Customer reports hardware or software problems they can't resolve themselves
- Diagnosing AI agent issues on the customer's machine (Hermes install, OpenClaw, etc.)
- Installing or configuring software on a customer's computer
- Running diagnostics (event logs, device manager, disk health, network)
- Verifying a remote install is working correctly
- Providing live hands-on support during a scheduled session

## When NOT to Use

❌ **DON'T use this skill when:**
- Customer has NOT given you their AnyDesk ID — always get it first
- Session is not pre-authorized — confirm consent before connecting
- The issue can be resolved via chat/instructions alone
- Customer is not present and did not set up unattended access

---

## Setup & Installation

### Linux (Debian/Ubuntu)
```bash
# Download and install AnyDesk
wget -qO - https://keys.anydesk.com/repos/DEB-GPG-KEY | apt-key add -
echo "deb http://deb.anydesk.com/ all main" > /etc/apt/sources.list.d/anydesk-stable.list
apt update && apt install -y anydesk

# Start the AnyDesk daemon
anydesk --start-service
```

### Check AnyDesk Status
```bash
anydesk --version
anydesk --get-id        # Get your own AnyDesk ID to share with customer
systemctl status anydesk 2>/dev/null || anydesk --status
```

---

## Core Commands

### Get Your AnyDesk ID (share with customer)
```bash
anydesk --get-id
```

### Connect to a Customer
```bash
# Connect using their AnyDesk ID (9-digit number or alias)
anydesk <CUSTOMER_ANYDESK_ID>

# Example
anydesk 123456789
```

### Connect with Password (unattended access)
```bash
anydesk <CUSTOMER_ANYDESK_ID> --with-password
# Then pipe the password via stdin or set it up in their unattended config
```

### Request File Transfer
```bash
# Open file manager during a session (from within AnyDesk GUI)
# Or use SCP/SFTP if SSH is available on customer machine
```

### List Active / Recent Sessions
```bash
anydesk --list-connections 2>/dev/null || cat ~/.anydesk/connections.log 2>/dev/null | tail -20
```

---

## Remote Diagnosis Playbook

### 1. Get Customer's AnyDesk ID
Ask the customer to:
1. Open AnyDesk on their computer
2. Read you the 9-digit number shown under "Your Address"
3. Click "Accept" when the connection request appears

### 2. Connect
```bash
anydesk <THEIR_ID>
```

### 3. Hardware Diagnostics (Windows customer)

Once connected, open a terminal on their machine and run:

```powershell
# System info
systeminfo | findstr /B /C:"OS" /C:"Total Physical Memory" /C:"Processor"

# Disk health
wmic diskdrive get status,model,size

# Check for disk errors
chkdsk C: /scan

# CPU/RAM usage snapshot
tasklist /FO TABLE | sort /R | head -20

# Check temperatures (requires HWMonitor or OpenHardwareMonitor)
# Download: https://www.cpuid.com/softwares/hwmonitor.html
```

### 4. Hardware Diagnostics (Linux customer)

```bash
# System overview
uname -a && lscpu | grep -E "Model|CPU|Thread|Core"

# Memory
free -h && dmidecode -t memory 2>/dev/null | grep -E "Size|Speed|Type" | head -20

# Disk health
lsblk
smartctl -a /dev/sda 2>/dev/null || smartctl -a /dev/nvme0 2>/dev/null

# Temperatures
sensors 2>/dev/null || vcgencmd measure_temp 2>/dev/null

# Hardware errors in logs
dmesg | grep -iE "error|fail|warn" | tail -30
```

### 5. Software Diagnostics (Windows)

```powershell
# Check Event Viewer for critical errors
Get-EventLog -LogName System -EntryType Error -Newest 20 | Format-Table TimeGenerated, Source, Message -Wrap

# Check running services
Get-Service | Where-Object {$_.Status -eq "Stopped"} | Format-Table Name, DisplayName

# Network connectivity
ping 8.8.8.8 -n 4
tracert google.com

# Check for malware indicators
netstat -ano | findstr ESTABLISHED

# Windows Update status
wuauclt /detectnow
```

### 6. AI Agent / Hermes Troubleshooting

```bash
# Check if Hermes/OpenClaw is running
ps aux | grep -iE "openclaw|hermes|kilo" | grep -v grep

# Check service logs
journalctl -u openclaw --since "1 hour ago" -n 50 2>/dev/null
cat /var/log/hermes/*.log 2>/dev/null | tail -50

# Verify API keys are loaded
env | grep -iE "api_key|cal_|stripe_|openai" | sed 's/=.*/=***REDACTED***/'

# Test network to key endpoints
curl -s https://api.cal.com/v2/me -H "Authorization: Bearer $CAL_API_KEY" | jq .status
curl -s https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY" | jq .object

# Restart agent service
systemctl restart openclaw 2>/dev/null || pm2 restart all 2>/dev/null

# Check Docker containers (if running in Docker)
docker ps -a
docker logs <container_name> --tail 50
```

### 7. Network Diagnostics

```bash
# Speed test
curl -s https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py | python3 -

# DNS check
nslookup google.com
dig +short api.cal.com

# Open ports
ss -tlnp 2>/dev/null || netstat -tlnp

# Traceroute to key service
traceroute api.openai.com
```

---

## Unattended Access Setup (for repeat customers)

For customers who want you to be able to connect without them being present:

### On their Windows machine:
1. Open AnyDesk → Settings → Security
2. Enable "Allow unattended access"
3. Set a strong password and share it with Jay securely (NOT via chat)

### On their Linux machine:
```bash
# Set unattended password
echo "ANYDESK_PASSWORD" | anydesk --set-password

# Or edit config
nano ~/.anydesk/user.conf
# Add: ad.security.unattended_access=1
```

---

## Session Notes Template

After every support session, log what was done:

```
Customer: [Name]
AnyDesk ID: [ID]
Date: [YYYY-MM-DD]
Issue: [Brief description]
Diagnosis: [What was found]
Fix Applied: [What was done]
Outcome: [Resolved / Follow-up needed]
Follow-up: [Any next steps]
```

Save to: `/root/.openclaw/workspace/memory/support-sessions/YYYY-MM-DD-customer-name.md`

---

## Common Issues & Fixes

| Symptom | Likely Cause | Fix |
|---|---|---|
| AnyDesk won't connect | Firewall blocking port 7070 | Open TCP/UDP 7070 on customer's router |
| Black screen on connect | Display driver issue | Try "Show remote cursor" mode |
| Lag / slow session | Poor network | Enable "Optimize speed" in AnyDesk settings |
| Agent not starting | Missing env vars | Check `.env` file, restart service |
| Cal.com not booking | API key expired | Re-issue key at cal.com/settings/developer |
| Stripe webhook failing | Wrong endpoint URL | Verify endpoint in Stripe dashboard |
| Docker container crash | OOM / bad config | `docker logs` + check resource limits |

---

## Security Rules (NON-NEGOTIABLE)

1. **Always get verbal or written consent** before connecting
2. **Never access files outside the agreed scope** of the support session
3. **Log every session** with customer name, ID, and what was done
4. **Never store unattended passwords** in plaintext — use a password manager
5. **Disconnect immediately** when the session is complete
6. **Notify the customer** via message when you connect and when you disconnect

---

## Notes

- AnyDesk ID format: 9-digit number (e.g., `123 456 789`) or custom alias
- Default port: TCP/UDP 7070 (also works over HTTPS port 443 as fallback)
- AnyDesk relay servers handle NAT traversal — no port forwarding usually needed
- For persistent remote access, prefer setting up SSH as a backup channel
- Customer-facing booking link for support sessions: `https://cal.com/leprograms/discovery-call`
