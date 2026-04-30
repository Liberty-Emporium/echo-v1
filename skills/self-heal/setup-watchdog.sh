#!/bin/bash
# setup-watchdog.sh — Install self-healing cron jobs for Echo
# Run once after bootstrap to set up auto brain-save + health monitoring

echo "🔧 Setting up Echo self-heal watchdog..."

WORKSPACE="/root/.openclaw/workspace"
ECHO_REPO="$WORKSPACE/echo-v1"
SAVE_BRAIN="$ECHO_REPO/scripts/save-brain.sh"
HEALTH_CHECK="$ECHO_REPO/skills/self-heal/health-check.sh"
LOG_DIR="/root/.openclaw/logs"

mkdir -p "$LOG_DIR"
chmod +x "$SAVE_BRAIN" 2>/dev/null || true
chmod +x "$HEALTH_CHECK" 2>/dev/null || true

# ── Build the auto-save script ─────────────────────────────────────────────────
AUTO_SAVE="/root/.openclaw/workspace/echo-v1/skills/self-heal/auto-save.sh"
cat > "$AUTO_SAVE" << 'AUTOSAVE'
#!/bin/bash
# auto-save.sh — Lightweight brain save for cron (no KYS encryption)
set -e
WORKSPACE="/root/.openclaw/workspace"
ECHO_REPO="$WORKSPACE/echo-v1"
TOKEN=$(cat /root/.secrets/github_token 2>/dev/null) || exit 0

cd "$ECHO_REPO"
git remote set-url origin "https://$TOKEN@github.com/Liberty-Emporium/echo-v1.git" 2>/dev/null

# Copy key brain files
for f in MEMORY.md SOUL.md AGENTS.md TOOLS.md USER.md IDENTITY.md HEARTBEAT.md; do
  [ -f "$WORKSPACE/$f" ] && cp "$WORKSPACE/$f" "$ECHO_REPO/$f"
done
[ -d "$WORKSPACE/memory" ] && cp -r "$WORKSPACE/memory/." "$ECHO_REPO/memory/" 2>/dev/null || true

# Only push if changes exist
git add -A
CHANGED=$(git diff --cached --name-only | wc -l)
if [ "$CHANGED" -gt 0 ]; then
  git config user.email "echo@liberty-emporium.ai"
  git config user.name "Echo"
  git commit -m "🧠 Auto brain-save $(date -u '+%Y-%m-%d %H:%M UTC')"
  git push origin main 2>/dev/null
  # Mirror to GitLab
  GL_TOKEN=$(cat /root/.secrets/gitlab_token 2>/dev/null) || true
  [ -n "$GL_TOKEN" ] && git push "https://oauth2:${GL_TOKEN}@gitlab.com/Liberty-Emporium/echo-v1.git" main 2>/dev/null || true
fi
AUTOSAVE
chmod +x "$AUTO_SAVE"

# ── Install crontab entries ────────────────────────────────────────────────────
TMPFILE=$(mktemp)
crontab -l 2>/dev/null | grep -v "echo-auto-save\|echo-health-check" > "$TMPFILE" || true

# Auto brain-save every 2 hours
echo "0 */2 * * * bash $AUTO_SAVE >> $LOG_DIR/auto-save.log 2>&1 # echo-auto-save" >> "$TMPFILE"

# Health check every 30 minutes — log only, alert if critical
echo "*/30 * * * * bash $HEALTH_CHECK >> $LOG_DIR/health.log 2>&1 # echo-health-check" >> "$TMPFILE"

crontab "$TMPFILE"
rm "$TMPFILE"

echo "✅ Watchdog installed:"
echo "   • Brain auto-save: every 2 hours → GitHub + GitLab"
echo "   • Health check:    every 30 min  → $LOG_DIR/health.log"
echo ""
echo "Verify with: crontab -l"
crontab -l | grep echo
