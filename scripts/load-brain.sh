#!/bin/bash
# ============================================================
# load-brain.sh — Session Startup Brain Decryption
#
# Run at the start of each session to decrypt brain files
# from the repo into the workspace using the key from
# Jay's Keep Your Secrets API.
#
# If no encryption is set up, copies plaintext files as-is.
# ============================================================

set -euo pipefail

WORKSPACE="/root/.openclaw/workspace"
ECHO_REPO="$WORKSPACE/echo-v1"
SECRETS="/root/.secrets"
KYS_TOKEN_FILE="$SECRETS/kys_api_token"
BRAIN_CRYPT="$ECHO_REPO/scripts/brain-crypt.sh"

echo "🧠 Echo Brain Load — $(date -u '+%Y-%m-%d %H:%M UTC')"
echo "=================================================="

# ── Pull latest brain from GitHub ─────────────────────────
cd "$ECHO_REPO"
echo "📥 Pulling latest brain from GitHub..."
git pull origin main --quiet && echo "  ✅ Up to date" || echo "  ⚠️  Pull failed — using local copy"

# ── Decrypt if encryption is set up ──────────────────────
if [ -f "$KYS_TOKEN_FILE" ] && [ -f "$BRAIN_CRYPT" ]; then
    echo ""
    echo "🔑 Fetching brain key from Keep Your Secrets..."
    KYS_TOKEN=$(cat "$KYS_TOKEN_FILE")
    BRAIN_PASS=$(bash "$BRAIN_CRYPT" fetch-key "$KYS_TOKEN" 2>&1) || {
        echo "  ⚠️  Could not fetch brain key — falling back to plaintext"
        BRAIN_PASS=""
    }
    if [ -n "$BRAIN_PASS" ] && [[ ! "$BRAIN_PASS" == *"❌"* ]]; then
        bash "$BRAIN_CRYPT" decrypt "$BRAIN_PASS"
        unset BRAIN_PASS
    fi
else
    echo "ℹ️  No KYS token — loading plaintext files"
fi

# ── Copy workspace files into live workspace ─────────────
echo ""
echo "📤 Syncing brain files to workspace..."
BRAIN_FILES=(MEMORY.md SOUL.md AGENTS.md TOOLS.md USER.md IDENTITY.md SKILLS.md HEARTBEAT.md)
for f in "${BRAIN_FILES[@]}"; do
    if [ -f "$ECHO_REPO/$f" ]; then
        cp "$ECHO_REPO/$f" "$WORKSPACE/$f"
        echo "  ✅ $f"
    fi
done

if [ -d "$ECHO_REPO/memory" ]; then
    mkdir -p "$WORKSPACE/memory"
    cp -r "$ECHO_REPO/memory/." "$WORKSPACE/memory/"
    echo "  ✅ memory/ synced"
fi

echo ""
echo "=================================================="
echo "✅ Brain loaded — ready, Jay 🦄"
