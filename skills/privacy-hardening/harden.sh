#!/bin/bash
# harden.sh — Echo Privacy & Security Hardening
# Run on every boot and periodically to keep chats private
# Usage: bash harden.sh [--quick] [--scan]
#   --quick  : permissions only (fast, safe for cron)
#   --scan   : full token leak scan (slower)
#   (no args): both

set -e

QUICK=false
SCAN=false
if [ "$1" = "--quick" ]; then QUICK=true; fi
if [ "$1" = "--scan" ]; then SCAN=true; fi
if [ $# -eq 0 ]; then QUICK=true; SCAN=true; fi

ISSUES=0
echo "🔒 Echo Privacy Hardening — $(date '+%Y-%m-%d %H:%M')"
echo "══════════════════════════════════════"

if [ "$QUICK" = true ]; then
  echo ""
  echo "🗂️  Fixing file permissions..."

  # Session logs — chat history
  SESSION_DIR="/root/.openclaw/agents/main/sessions"
  if [ -d "$SESSION_DIR" ]; then
    find "$SESSION_DIR" -type f \( -name "*.jsonl" -o -name "*.json" -o -name "*.lock" \) \
      ! -perm 600 -exec chmod 600 {} \;
    echo "  ✅ Session logs → 600 (root-only)"
  fi

  # Secrets directory
  if [ -d "/root/.secrets" ]; then
    chmod 700 /root/.secrets
    chmod 600 /root/.secrets/* 2>/dev/null || true
    echo "  ✅ /root/.secrets → 700/600"
  fi

  # OpenClaw config
  if [ -f "/root/.openclaw/openclaw.json" ]; then
    chmod 600 /root/.openclaw/openclaw.json
    echo "  ✅ openclaw.json → 600"
  fi

  # Brain/memory files (shouldn't be world-readable)
  WORKSPACE="/root/.openclaw/workspace/echo-v1"
  if [ -d "$WORKSPACE/memory" ]; then
    chmod 700 "$WORKSPACE/memory" 2>/dev/null || true
    chmod 600 "$WORKSPACE/memory/"*.md 2>/dev/null || true
    echo "  ✅ memory/ → 700/600"
  fi

  # Verify gateway is still loopback-only
  BIND=$(python3 -c "import json; c=json.load(open('/root/.openclaw/openclaw.json')); print(c.get('gateway',{}).get('bind',''))" 2>/dev/null)
  if [ "$BIND" = "loopback" ]; then
    echo "  ✅ Gateway bind: loopback only ✓"
  else
    echo "  ⚠️  Gateway bind: $BIND — expected loopback!"
    ISSUES=$((ISSUES+1))
  fi

  # Check no unexpected open ports
  OPEN_PORTS=$(ss -ltnp 2>/dev/null | grep -v "127.0.0.1\|::1\|Local" | grep LISTEN | wc -l)
  if [ "$OPEN_PORTS" -gt 0 ]; then
    echo "  ⚠️  $OPEN_PORTS port(s) listening on non-loopback — review:"
    ss -ltnp 2>/dev/null | grep -v "127.0.0.1\|::1\|Local" | grep LISTEN | awk '{print "     "$1" "$4}'
    ISSUES=$((ISSUES+1))
  else
    echo "  ✅ No unexpected open ports"
  fi
fi

if [ "$SCAN" = true ]; then
  echo ""
  echo "🔍 Scanning for token leaks..."

  WORKSPACE="/root/.openclaw/workspace"
  LEAKED=0

  # Patterns that look like real tokens
  HITS=$(grep -rn \
    -e "ghp_[A-Za-z0-9]\{36\}" \
    -e "glpat-[A-Za-z0-9_-]\{20\}" \
    -e "sk-[A-Za-z0-9]\{40\}" \
    -e "AKIA[A-Z0-9]\{16\}" \
    "$WORKSPACE" \
    --include="*.md" --include="*.txt" --include="*.json" --include="*.env" \
    --exclude-dir=".git" --exclude-dir="__pycache__" \
    2>/dev/null | grep -v "^Binary" | wc -l)

  if [ "$HITS" -gt 0 ]; then
    echo "  ⚠️  FOUND $HITS possible token(s) in plain text files!"
    echo "     Run: grep -rn 'ghp_\|glpat-\|sk-\|AKIA' $WORKSPACE --include='*.md' --include='*.txt'"
    echo "     Move any real tokens to /root/.secrets/"
    ISSUES=$((ISSUES+1))
  else
    echo "  ✅ No token leaks found in workspace files"
  fi

  # Check MEMORY.md specifically
  if grep -qE "ghp_|glpat-|sk-[A-Za-z0-9]{40}" \
    "$WORKSPACE/echo-v1/MEMORY.md" 2>/dev/null; then
    echo "  ⚠️  MEMORY.md may contain a token — review and remove!"
    ISSUES=$((ISSUES+1))
  else
    echo "  ✅ MEMORY.md clean"
  fi
fi

echo ""
echo "══════════════════════════════════════"
if [ "$ISSUES" -eq 0 ]; then
  echo "✅ All checks passed — chats are private"
else
  echo "⚠️  $ISSUES issue(s) found — review above"
fi
exit $ISSUES
