#!/bin/bash
# health-check.sh — Echo system health check
# Run anytime to see current system state

echo "🏥 Echo Health Check — $(date '+%Y-%m-%d %H:%M')"
echo "══════════════════════════════════════"

# Memory
echo ""
echo "💾 Memory:"
free -h | grep -E "Mem|Swap"
MEM_AVAIL=$(free -m | awk '/^Mem:/ {print $7}')
if [ "$MEM_AVAIL" -lt 200 ]; then
  echo "  ⚠️  LOW MEMORY: ${MEM_AVAIL}MB available — risk of crash!"
else
  echo "  ✅ Memory OK: ${MEM_AVAIL}MB available"
fi

# Disk
echo ""
echo "💿 Disk:"
df -h /root | tail -1
DISK_PCT=$(df /root | awk 'NR==2 {print $5}' | tr -d '%')
if [ "$DISK_PCT" -gt 85 ]; then
  echo "  ⚠️  DISK FULL: ${DISK_PCT}% used — risk of crash!"
else
  echo "  ✅ Disk OK: ${DISK_PCT}% used"
fi

# OpenClaw process
echo ""
echo "⚙️  OpenClaw Process:"
if pgrep -f "openclaw" > /dev/null 2>&1; then
  PID=$(pgrep -f "openclaw" | head -1)
  echo "  ✅ Running (PID: $PID)"
else
  echo "  ❌ NOT RUNNING — restart needed!"
fi

# Gateway ping
echo ""
echo "🌐 Gateway:"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:4000/health 2>/dev/null || echo "000")
if [ "$STATUS" = "200" ] || [ "$STATUS" = "401" ]; then
  echo "  ✅ Responding (HTTP $STATUS)"
else
  echo "  ❌ Not responding (HTTP $STATUS)"
fi

# Top memory processes
echo ""
echo "🔝 Top 5 memory consumers:"
ps aux --sort=-%mem 2>/dev/null | head -6 | tail -5 | awk '{printf "  %s %s%%mem %sMB\n", $11, $4, int($6/1024)}'

# Last brain save
echo ""
echo "🧠 Last brain save:"
cd /root/.openclaw/workspace/echo-v1 2>/dev/null && \
  git log --oneline -1 --format="  %cr — %s" 2>/dev/null || echo "  unknown"

# Temp/cache cleanup opportunity
CACHE_SIZE=$(du -sm /root/.openclaw/workspace/*/__pycache__ 2>/dev/null | awk '{sum+=$1} END {print sum+0}')
if [ "$CACHE_SIZE" -gt 50 ]; then
  echo ""
  echo "🧹 ${CACHE_SIZE}MB of __pycache__ found — run: find /root/.openclaw/workspace -name '__pycache__' -exec rm -rf {} + 2>/dev/null"
fi

echo ""
echo "══════════════════════════════════════"
echo "✅ Health check complete"
