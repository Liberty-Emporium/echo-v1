#!/bin/bash
# ============================================================
# restore-brain.sh — Echo Session Startup Script
# Run this at the start of every session to sync brain from
# GitHub (echo-v1) into the active workspace.
# ============================================================

set -e

WORKSPACE="/root/.openclaw/workspace"
ECHO_REPO="$WORKSPACE/echo-v1"
SECRETS="/root/.secrets"
GITHUB_TOKEN_FILE="$SECRETS/github_token"

echo "🐙 Echo Brain Restore — $(date -u '+%Y-%m-%d %H:%M UTC')"
echo "=================================================="

# ── 1. Token ──────────────────────────────────────────────
if [ ! -f "$GITHUB_TOKEN_FILE" ]; then
  echo "❌ No GitHub token at $GITHUB_TOKEN_FILE"
  echo "   Jay: paste new token, I'll save it and continue."
  exit 1
fi
TOKEN=$(cat "$GITHUB_TOKEN_FILE")
echo "✅ GitHub token loaded"

# ── 2. Clone or pull echo-v1 ──────────────────────────────
if [ -d "$ECHO_REPO/.git" ]; then
  echo "📥 Pulling latest echo-v1..."
  cd "$ECHO_REPO"
  git remote set-url origin "https://$TOKEN@github.com/Liberty-Emporium/echo-v1.git"
  git pull --ff-only origin main 2>&1 | tail -3
else
  echo "📥 Cloning echo-v1..."
  GH_TOKEN="$TOKEN" gh repo clone Liberty-Emporium/echo-v1 "$ECHO_REPO"
fi
echo "✅ echo-v1 up to date"

# ── 3. Copy brain files into workspace ────────────────────
echo "🧠 Copying brain files..."
FILES=(MEMORY.md SOUL.md AGENTS.md TOOLS.md USER.md IDENTITY.md SKILLS.md SHORT_TERM_MEMORY.md HEARTBEAT.md)
for f in "${FILES[@]}"; do
  if [ -f "$ECHO_REPO/$f" ]; then
    cp "$ECHO_REPO/$f" "$WORKSPACE/$f"
    echo "  ✅ $f"
  else
    echo "  ⚠️  $f not found in repo (skipping)"
  fi
done

# ── 4. Copy memory diary ──────────────────────────────────
echo "📅 Syncing memory diary..."
mkdir -p "$WORKSPACE/memory"
if [ -d "$ECHO_REPO/memory" ]; then
  cp -r "$ECHO_REPO/memory/." "$WORKSPACE/memory/"
  COUNT=$(ls "$WORKSPACE/memory/" | wc -l)
  echo "  ✅ $COUNT memory files synced"
fi

# ── 5. Copy custom skills ─────────────────────────────────
echo "🛠️  Syncing custom skills..."
mkdir -p "$WORKSPACE/skills/custom"
if [ -d "$ECHO_REPO/skills/custom" ]; then
  cp -r "$ECHO_REPO/skills/custom/." "$WORKSPACE/skills/custom/"
  COUNT=$(ls "$WORKSPACE/skills/custom/" | wc -l)
  echo "  ✅ $COUNT custom skills synced"
fi

# ── 6. Copy research library ─────────────────────────────
echo "📚 Syncing research library..."
mkdir -p "$WORKSPACE/research"
if [ -d "$ECHO_REPO/research" ]; then
  cp -r "$ECHO_REPO/research/." "$WORKSPACE/research/"
  COUNT=$(ls "$WORKSPACE/research/" | wc -l)
  echo "  ✅ $COUNT research files synced"
fi

# ── 7. Copy scripts ───────────────────────────────────────
if [ -d "$ECHO_REPO/scripts" ]; then
  cp -r "$ECHO_REPO/scripts/." "$WORKSPACE/scripts/"
fi

# ── 8. Save Railway creds if provided ────────────────────
if [ ! -f "$SECRETS/railway_creds" ]; then
  echo "⚠️  No Railway creds at $SECRETS/railway_creds"
  echo "   Jay: share Railway client_id + secret when needed"
fi

echo ""
echo "=================================================="
echo "✅ Brain restore complete — Echo is ready"
echo ""

# ── 9. Show today's priorities ────────────────────────────
TODAY=$(date -u '+%Y-%m-%d')
if [ -f "$WORKSPACE/memory/$TODAY.md" ]; then
  echo "📋 Today's memory ($TODAY):"
  head -20 "$WORKSPACE/memory/$TODAY.md"
elif [ -f "$WORKSPACE/SHORT_TERM_MEMORY.md" ]; then
  echo "📋 Last session priorities:"
  grep -A 20 "Next Session Priorities\|Next Up\|Fix First" "$WORKSPACE/SHORT_TERM_MEMORY.md" | head -25 || true
fi
