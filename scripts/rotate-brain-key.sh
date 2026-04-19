#!/bin/bash
# ============================================================
# rotate-brain-key.sh — Weekly Brain Key Rotation
#
# Jay runs this (or tells KiloClaw to run it) when rotating
# the brain encryption password. It:
#   1. Verifies old key works
#   2. Updates the key in Keep Your Secrets
#   3. Re-encrypts the brain with the new key
#   4. Pushes to GitHub
#
# Usage:
#   rotate-brain-key.sh <new_passphrase> [old_passphrase]
#
# Or let Echo handle it — just say:
#   "rotate my brain key to: [new passphrase]"
# ============================================================

set -euo pipefail

WORKSPACE="/root/.openclaw/workspace"
ECHO_REPO="$WORKSPACE/echo-v1"
SECRETS="/root/.secrets"
KYS_TOKEN_FILE="$SECRETS/kys_api_token"
BRAIN_CRYPT="$ECHO_REPO/scripts/brain-crypt.sh"

NEW_KEY="${1:-}"
OLD_KEY="${2:-}"

if [ -z "$NEW_KEY" ]; then
    echo "Usage: rotate-brain-key.sh <new_passphrase> [old_passphrase]"
    echo ""
    echo "Example: rotate-brain-key.sh 'CorrectHorseBatteryStaple2025'"
    exit 1
fi

if [ ! -f "$KYS_TOKEN_FILE" ]; then
    echo "❌ No KYS API token at $KYS_TOKEN_FILE"
    echo "   Get a token: POST /api/token to Keep Your Secrets"
    exit 1
fi

KYS_TOKEN=$(cat "$KYS_TOKEN_FILE")

echo "🔄 Brain Key Rotation — $(date -u '+%Y-%m-%d %H:%M UTC')"
echo "=================================================="

# Step 1: Rotate in Keep Your Secrets
echo "1️⃣  Rotating key in Keep Your Secrets..."
bash "$BRAIN_CRYPT" rotate "$KYS_TOKEN" "$NEW_KEY" "$OLD_KEY"

# Step 2: Re-encrypt brain with new key
echo ""
echo "2️⃣  Re-encrypting brain with new key..."
bash "$BRAIN_CRYPT" encrypt "$NEW_KEY"
unset NEW_KEY

# Step 3: Save brain (push encrypted files to GitHub)
echo ""
echo "3️⃣  Pushing re-encrypted brain to GitHub..."
bash "$ECHO_REPO/scripts/save-brain.sh"

echo ""
echo "=================================================="
echo "✅ Brain key rotated. Echo will use the new key next session."
echo "   Remember: the old key is gone. Don't lose the new one!"
