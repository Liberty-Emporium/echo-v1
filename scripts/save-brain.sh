#!/bin/bash
# ============================================================
# save-brain.sh — Echo Session End Script
# Run at end of session to push all brain updates back to
# GitHub AND GitLab so next session starts fresh.
# ============================================================

set -e

WORKSPACE="/root/.openclaw/workspace"
# Resolve real path — handle both direct clone and symlink cases
if [ -d "/root/.openclaw/echo-v1/.git" ]; then
  ECHO_REPO="/root/.openclaw/echo-v1"
else
  ECHO_REPO="$WORKSPACE/echo-v1"
fi
SECRETS="/root/.secrets"
GITHUB_TOKEN_FILE="$SECRETS/github_token"
GITLAB_TOKEN_FILE="$SECRETS/gitlab_token"
KYS_TOKEN_FILE="$SECRETS/kys_api_token"   # Keep Your Secrets API token
BRAIN_CRYPT="$ECHO_REPO/scripts/brain-crypt.sh"

echo "💾 Echo Brain Save — $(date -u '+%Y-%m-%d %H:%M UTC')"
echo "=================================================="

# ── 1. Tokens ──────────────────────────────────────────────
if [ ! -f "$GITHUB_TOKEN_FILE" ]; then
  echo "❌ No GitHub token — cannot push"
  exit 1
fi
TOKEN=$(cat "$GITHUB_TOKEN_FILE")

GITLAB_TOKEN=""
if [ -f "$GITLAB_TOKEN_FILE" ]; then
  GITLAB_TOKEN=$(cat "$GITLAB_TOKEN_FILE")
fi

# ── 2. Set remotes ─────────────────────────────────────────
cd "$ECHO_REPO"
git remote set-url origin "https://$TOKEN@github.com/Liberty-Emporium/echo-v1.git"

# GitLab setup
if [ -n "$GITLAB_TOKEN" ]; then
  GITLAB_USER=$(curl -s --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "https://gitlab.com/api/v4/user" | python3 -c "import sys,json; print(json.load(sys.stdin).get('username',''))" || echo "")
  if [ -n "$GITLAB_USER" ]; then
    if ! git remote get-url gitlab 2>/dev/null; then
      git remote add gitlab "https://oauth2:$GITLAB_TOKEN@gitlab.com/$GITLAB_USER/echo-v1.git"
    fi
  fi
fi

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

# ── 8. Encrypt brain files before push ───────────────────
if [ -f "$KYS_TOKEN_FILE" ] && [ -f "$BRAIN_CRYPT" ]; then
  echo ""
  echo "🔐 Fetching brain encryption key from Keep Your Secrets..."
  KYS_TOKEN=$(cat "$KYS_TOKEN_FILE")
  BRAIN_PASS=$(bash "$BRAIN_CRYPT" fetch-key "$KYS_TOKEN" 2>&1) || {
    echo "⚠️  Could not fetch brain key — pushing WITHOUT encryption"
    echo "   Run: brain-crypt.sh set-key <token> <passphrase> to enable encryption"
    BRAIN_PASS=""
  }
  if [ -n "$BRAIN_PASS" ] && [[ ! "$BRAIN_PASS" == *"❌"* ]]; then
    bash "$BRAIN_CRYPT" encrypt "$BRAIN_PASS"
    unset BRAIN_PASS  # clear from memory immediately
    echo "✅ Brain encrypted for push"
  fi
else
  echo "ℹ️  No KYS token found — pushing plaintext (set up encryption: see brain-crypt.sh)"
fi

# ── 9. Sync with GitHub before committing (prevent conflicts) ──
git stash 2>/dev/null || true
git fetch origin 2>/dev/null || true
git reset --hard origin/main 2>/dev/null || true
git stash pop 2>/dev/null || true

# ── 10. Git commit + push ──────────────────────────────────
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
  
  echo "🚀 Pushing to GitHub..."
  git push origin main
  echo "✅ Pushed to GitHub"
  
  if git remote get-url gitlab &>/dev/null; then
    echo "🚀 Pushing to GitLab..."
    git push gitlab main 2>&1 || echo "⚠️ GitLab push failed (continuing)"
    echo "✅ Pushed to GitLab"
  fi
fi

echo ""
echo "=================================================="
echo "✅ Brain saved — see you next session, Jay 🐙"
