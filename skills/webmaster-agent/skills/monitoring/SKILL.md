---
name: webmaster-monitoring
description: Website uptime monitoring, health checks, and alerting for agent webmasters
version: 1.0.0
platforms: [linux, macos]
---

# Webmaster Monitoring Skill

## When to use
- Setting up website monitoring
- Checking server health
- Investigating downtime
- Configuring alerts

## Monitoring Stack (All Free)

### UptimeRobot (External)
- 50 free monitors
- HTTP, ping, port, keyword, SSL monitoring
- Email/Slack/Telegram alerts
- Sign up at: https://uptimerobot.com

### Self-Hosted Health Checks
```bash
# Simple health check script
curl -sf -o /dev/null -w "%{http_code}" https://yoursite.com/health
```

### Server-Side Monitoring
```bash
# Install netdata (real-time metrics)
bash <(curl -Ss https://my-netdata.io/kickstart.sh)

# Or use built-in tools
htop                    # CPU/Memory/Processes
df -h                   # Disk usage
ss -tlnp                # Open ports
journalctl -f           # Live logs
```

## Health Check Script

Save as `/usr/local/bin/agent-health.sh`:

```bash
#!/bin/bash
SITES=("$@")
LOG="/var/log/webmaster-health.log"
ALERT=false

for site in "${SITES[@]}"; do
  STATUS=$(curl -sf -o /dev/null -w "%{http_code}" --max-time 15 "$site" 2>/dev/null)
  if [ "$STATUS" != "200" ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') ALERT: $site returned $STATUS" | tee -a "$LOG"
    ALERT=true
  else
    echo "$(date '+%Y-%m-%d %H:%M:%S') OK: $site ($STATUS)" >> "$LOG"
  fi
done

# Check disk
DISK=$(df / | tail -1 | awk '{print $5}' | tr -d '%')
if [ "$DISK" -gt 85 ]; then
  echo "$(date '+%Y-%m-%d %H:%M:%S') ALERT: Disk usage at ${DISK}%" | tee -a "$LOG"
  ALERT=true
fi

# Check memory
MEM=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
if [ "$MEM" -gt 90 ]; then
  echo "$(date '+%Y-%m-%d %H:%M:%S') ALERT: Memory usage at ${MEM}%" | tee -a "$LOG"
  ALERT=true
fi

# Check SSL expiry
for domain in "${SITES[@]}"; do
  HOST=$(echo "$domain" | sed 's|https://||' | sed 's|.*||' | cut -d/ -f1)
  EXPIRY=$(echo | openssl s_client -servername "$HOST" -connect "$HOST:443" 2>/dev/null | openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)
  if [ -n "$EXPIRY" ]; then
    DAYS=$(( ($(date -d "$EXPIRY" +%s) - $(date +%s)) / 86400 ))
    if [ "$DAYS" -lt 14 ]; then
      echo "$(date '+%Y-%m-%d %H:%M:%S') ALERT: SSL for $HOST expires in $DAYS days" | tee -a "$LOG"
      ALERT=true
    fi
  fi
done

if [ "$ALERT" = true ]; then
  exit 1
fi
exit 0
```

```bash
chmod +x /usr/local/bin/agent-health.sh
```

## Cron Setup
```bash
# Health check every 5 minutes
*/5 * * * * /usr/local/bin/agent-health.sh https://yoursite.com https://api.yoursite.com/health

# Daily SSL check
0 8 * * * /usr/local/bin/agent-health.sh https://yoursite.com 2>&1 | grep "ALERT" | mail -s "SSL Alert" you@email.com
```

## Pitfalls
- Don't check too frequently — every 5 minutes max for self-hosted
- Always use `--max-time` on curl to avoid hanging
- Log rotation: add `logrotate` config for health logs
- Test alerts — an untested alert system is worse than no alerts

## Verification
```bash
# Test health script
/usr/local/bin/agent-health.sh https://yoursite.com

# Check cron is running
grep agent-health /var/log/syslog | tail -5

# Verify UptimeRobot is monitoring
curl -s "https://api.uptimerobot.com/v2/getMonitors" -H "Key: YOUR_API_KEY" | python3 -m json.tool
```
