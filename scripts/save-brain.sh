#!/bin/bash
# ============================================================
# save-brain.sh — Echo Session End Script
# Run at end of session to push all brain updates back to
# GitHub (echo-v1) so next session starts fresh.
# ============================================================

set -e

WORKSPACE="/root/.openclaw/workspace"
ECHO_REPO="$WORKSPACE/echo-v1"
SECRETS="/root/.secrets"
GITHUB_TOKEN_FILE="$SECRETS/github_token"

echo "💾 Echo Brain Save — $(date -u '+%Y-%m-%d %H:%M UTC')"
echo "=================================================="

# ── 1. Token ──────────────────────────────────────────────
if [ ! -f "$GITHUB_TOKEN_FILE" ]; then
  echo "❌ No GitHub token — cannot push"
  exit 1
fi
TOKEN=$(cat "$GITHUB_TOKEN_FILE")

# ── 2. Set remote ─────────────────────────────────────────
cd "$ECHO_REPO"
git remote set-url origin "https://$TOKEN@github.com/Liberty-Emporium/echo-v1.git"

# ── 3. Copy workspace brain files back to repo ────────────
echo "📤 Copying updated brain files to repo..."
FILES=(MEMORY.md SOUL.md AGENTS.md TOOLS.md USER.md IDENTITY.md SKILLS.md SHORT_TERM_MEMORY.md HEARTBEAT.md)
for f in "${FILES[@]}"; do
  if [ -f "$WORKSPACE/$f" ]; then
    cp "$WORKSPACE/$f" "$ECHO_REPO/$f"
    echo "  ✅ $f"
  fi
done

# ── 4. Copy memory diary back ─────────────────────────────
if [ -d "$WORKSPACE/memory" ]; then
  mkdir -p "$ECHO_REPO/memory"
  cp -r "$WORKSPACE/memory/." "$ECHO_REPO/memory/"
  echo "  ✅ memory/ synced"
fi

# ── 5. Copy custom skills back ────────────────────────────
if [ -d "$WORKSPACE/skills/custom" ]; then
  mkdir -p "$ECHO_REPO/skills/custom"
  cp -r "$WORKSPACE/skills/custom/." "$ECHO_REPO/skills/custom/"
  echo "  ✅ skills/custom/ synced"
fi

# ── 6. Copy research back ─────────────────────────────────
if [ -d "$WORKSPACE/research" ]; then
  mkdir -p "$ECHO_REPO/research"
  cp -r "$WORKSPACE/research/." "$ECHO_REPO/research/"
  echo "  ✅ research/ synced"
fi

# ── 7. Copy scripts back ──────────────────────────────────
if [ -d "$WORKSPACE/scripts" ]; then
  mkdir -p "$ECHO_REPO/scripts"
  cp -r "$WORKSPACE/scripts/." "$ECHO_REPO/scripts/"
  echo "  ✅ scripts/ synced"
fi

# ── 8. Git commit + push ──────────────────────────────────
echo ""
echo "📦 Committing and pushing..."
git config user.email "echo@liberty-emporium.ai"
git config user.name "Echo"

git add -A
CHANGED=$(git diff --cached --name-only | wc -l)

if [ "$CHANGED" -eq 0 ]; then
  echo "✅ Nothing changed — already up to date"
else
  TIMESTAMP=$(date -u '+%Y-%m-%d %H:%M UTC')
  git commit -m "🧠 Brain save — $TIMESTAMP ($CHANGED files updated)"
  git push origin main
  echo "✅ Pushed $CHANGED files to echo-v1"
fi

echo ""
echo "=================================================="
echo "✅ Brain saved — see you next session, Jay 🐙"
