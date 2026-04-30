# Skill: self-heal
Keep Echo running longer and recover automatically from crashes.

## The Problem
Echo (KiloClaw/OpenClaw) crashes periodically and Jay has to manually reboot. 
Goal: detect crashes early, auto-recover where possible, minimize manual reboots.

## Self-Healing Strategy

### 1. Heartbeat Watchdog (cron)
A cron job pings the OpenClaw gateway every 5 minutes and restarts if unresponsive.

### 2. Memory Pressure Prevention  
Clear Python `__pycache__`, temp files, and old logs before they pile up.

### 3. Save Brain Before Crash
Push MEMORY.md + brain files to GitHub every 2 hours automatically via cron.

### 4. Crash Detection Signals
Things that predict an upcoming crash:
- Response times slowing dramatically
- Memory usage climbing (check with: `free -h`)
- Disk filling up (check with: `df -h /root`)
- Process count spiking

---

## Setup: Auto Brain-Save Cron

Run this once to install the 2-hour brain-save cron:

```bash
bash /root/.openclaw/workspace/echo-v1/skills/self-heal/setup-watchdog.sh
```

## Manual Health Check

```bash
bash /root/.openclaw/workspace/echo-v1/skills/self-heal/health-check.sh
```

## What to check when Echo seems slow/unstable

```bash
free -h                          # memory
df -h /root                      # disk
ps aux --sort=-%mem | head -10   # top memory processes
openclaw gateway status          # gateway status
journalctl -u openclaw -n 50     # recent logs (if systemd)
```

## Recovery Steps (if crashed)
1. Jay runs: reboot or restart from Fly.io dashboard  
2. On next boot: bootstrap.sh runs automatically (if configured)
3. Or manually: `bash /root/.openclaw/workspace/echo-v1/scripts/bootstrap.sh`

## Prevention Checklist (run during heartbeat)
- [ ] `free -h` — alert Jay if available RAM < 200MB
- [ ] `df -h /root` — alert Jay if disk > 85% full
- [ ] Check openclaw process is running
- [ ] Auto-save brain if >2h since last save
