#!/bin/bash
# ============================================================
# brain-crypt.sh — Brain Encryption/Decryption
#
# Uses AES-256-CBC via OpenSSL with a passphrase fetched from
# Jay's Keep Your Secrets API at startup / rotation.
#
# Usage:
#   brain-crypt.sh encrypt <passphrase>   — encrypt all brain files
#   brain-crypt.sh decrypt <passphrase>   — decrypt all brain files
#   brain-crypt.sh fetch-key <api_token>  — fetch passphrase from KYS API
#   brain-crypt.sh rotate <api_token> <new_key> [old_key]  — rotate key
#
# Encrypted files get a .enc extension alongside the original.
# On GitHub, only .enc files exist — never plaintext secrets.
# ============================================================

set -euo pipefail

KYS_API="https://ai-api-tracker-production.up.railway.app"
WORKSPACE="/root/.openclaw/workspace"
ECHO_REPO="$WORKSPACE/echo-v1"

# Files to encrypt (sensitive brain content)
ENCRYPT_FILES=(
    "MEMORY.md"
    "USER.md"
    "SOUL.md"
    "IDENTITY.md"
)

# Memory directory (daily files — also sensitive)
ENCRYPT_MEMORY_DIR=true

usage() {
    echo "Usage: brain-crypt.sh <command> [args]"
    echo ""
    echo "Commands:"
    echo "  encrypt <passphrase>              Encrypt brain files"
    echo "  decrypt <passphrase>              Decrypt brain files (load into workspace)"
    echo "  fetch-key <api_token>             Fetch passphrase from Keep Your Secrets"
    echo "  set-key <api_token> <passphrase>  Store passphrase in Keep Your Secrets"
    echo "  rotate <api_token> <new> [old]    Rotate passphrase"
    echo "  status                            Show encryption status"
    exit 1
}

# ── Encrypt a single file ─────────────────────────────────
encrypt_file() {
    local src="$1"
    local passphrase="$2"
    local dst="${src}.enc"

    if [ ! -f "$src" ]; then
        return 0
    fi

    openssl enc -aes-256-cbc -pbkdf2 -iter 100000 \
        -pass pass:"$passphrase" \
        -in "$src" -out "$dst"

    echo "  🔒 Encrypted: $(basename $src) → $(basename $dst)"
}

# ── Decrypt a single file ─────────────────────────────────
decrypt_file() {
    local src="$1"
    local passphrase="$2"
    local dst="${src%.enc}"

    if [ ! -f "$src" ]; then
        return 0
    fi

    openssl enc -aes-256-cbc -pbkdf2 -iter 100000 -d \
        -pass pass:"$passphrase" \
        -in "$src" -out "$dst" 2>/dev/null

    if [ $? -eq 0 ]; then
        echo "  🔓 Decrypted: $(basename $src) → $(basename $dst)"
    else
        echo "  ❌ Failed to decrypt: $(basename $src) — wrong passphrase?"
        return 1
    fi
}

# ── Fetch key from Keep Your Secrets ─────────────────────
cmd_fetch_key() {
    local api_token="$1"
    local label="${2:-default}"

    response=$(curl -sf -X GET \
        -H "Authorization: Bearer $api_token" \
        "$KYS_API/api/brain-key?label=$label") || {
        echo "❌ Failed to reach Keep Your Secrets API"
        exit 1
    }

    # Extract key_value from JSON (no jq dependency)
    key=$(echo "$response" | python3 -c "import sys,json; print(json.load(sys.stdin)['key_value'])" 2>/dev/null) || {
        echo "❌ Could not parse API response: $response"
        exit 1
    }

    echo "$key"
}

# ── Store key in Keep Your Secrets ───────────────────────
cmd_set_key() {
    local api_token="$1"
    local passphrase="$2"
    local label="${3:-default}"

    response=$(curl -sf -X PUT \
        -H "Authorization: Bearer $api_token" \
        -H "Content-Type: application/json" \
        -d "{\"label\": \"$label\", \"key_value\": \"$passphrase\"}" \
        "$KYS_API/api/brain-key") || {
        echo "❌ Failed to store key in Keep Your Secrets"
        exit 1
    }

    echo "$response" | python3 -c "
import sys, json
d = json.load(sys.stdin)
if d.get('success'):
    print('  ✅ Brain key stored in Keep Your Secrets')
else:
    print(f'  ❌ Error: {d.get(\"error\", d)}')
"
}

# ── Rotate key ────────────────────────────────────────────
cmd_rotate() {
    local api_token="$1"
    local new_key="$2"
    local old_key="${3:-}"
    local label="${4:-default}"

    body="{\"label\": \"$label\", \"new_key\": \"$new_key\""
    if [ -n "$old_key" ]; then
        body="$body, \"old_key\": \"$old_key\""
    fi
    body="$body}"

    response=$(curl -sf -X POST \
        -H "Authorization: Bearer $api_token" \
        -H "Content-Type: application/json" \
        -d "$body" \
        "$KYS_API/api/brain-key/rotate") || {
        echo "❌ Failed to rotate key"
        exit 1
    }

    echo "$response" | python3 -c "
import sys, json
d = json.load(sys.stdin)
if d.get('success'):
    print('  ✅ Brain key rotated in Keep Your Secrets')
    print(f'  ⏱  Rotated at: {d.get(\"rotated_at\", \"?\")}')
    print('  ⚠️  Re-run save-brain.sh to re-encrypt with new key!')
else:
    print(f'  ❌ Error: {d.get(\"error\", d)}')
"
}

# ── Encrypt all brain files ───────────────────────────────
cmd_encrypt() {
    local passphrase="$1"
    echo "🔒 Encrypting brain files..."

    cd "$ECHO_REPO"

    for f in "${ENCRYPT_FILES[@]}"; do
        encrypt_file "$f" "$passphrase"
    done

    # Encrypt memory/ directory
    if [ "$ENCRYPT_MEMORY_DIR" = true ] && [ -d "memory" ]; then
        for mf in memory/*.md; do
            [ -f "$mf" ] && encrypt_file "$mf" "$passphrase"
        done
    fi

    echo "✅ All brain files encrypted"
}

# ── Decrypt all brain files ───────────────────────────────
cmd_decrypt() {
    local passphrase="$1"
    echo "🔓 Decrypting brain files..."

    cd "$ECHO_REPO"

    for f in "${ENCRYPT_FILES[@]}"; do
        decrypt_file "${f}.enc" "$passphrase"
    done

    if [ "$ENCRYPT_MEMORY_DIR" = true ] && [ -d "memory" ]; then
        for encf in memory/*.md.enc; do
            [ -f "$encf" ] && decrypt_file "$encf" "$passphrase"
        done
    fi

    echo "✅ Brain decrypted into workspace"
}

# ── Status ────────────────────────────────────────────────
cmd_status() {
    echo "🧠 Brain Encryption Status"
    echo "=========================="
    cd "$ECHO_REPO"

    for f in "${ENCRYPT_FILES[@]}"; do
        if [ -f "${f}.enc" ]; then
            if [ -f "$f" ]; then
                echo "  ⚠️  $f — BOTH plaintext and .enc exist (push will encrypt)"
            else
                echo "  ✅ $f — encrypted only (.enc)"
            fi
        else
            if [ -f "$f" ]; then
                echo "  ❌ $f — PLAINTEXT, not encrypted"
            else
                echo "  ➖ $f — not present"
            fi
        fi
    done
}

# ── Main ──────────────────────────────────────────────────
COMMAND="${1:-}"

case "$COMMAND" in
    encrypt)
        [ -z "${2:-}" ] && { echo "Usage: brain-crypt.sh encrypt <passphrase>"; exit 1; }
        cmd_encrypt "$2"
        ;;
    decrypt)
        [ -z "${2:-}" ] && { echo "Usage: brain-crypt.sh decrypt <passphrase>"; exit 1; }
        cmd_decrypt "$2"
        ;;
    fetch-key)
        [ -z "${2:-}" ] && { echo "Usage: brain-crypt.sh fetch-key <api_token>"; exit 1; }
        cmd_fetch_key "$2" "${3:-default}"
        ;;
    set-key)
        [ -z "${2:-}" ] || [ -z "${3:-}" ] && { echo "Usage: brain-crypt.sh set-key <api_token> <passphrase>"; exit 1; }
        cmd_set_key "$2" "$3" "${4:-default}"
        ;;
    rotate)
        [ -z "${2:-}" ] || [ -z "${3:-}" ] && { echo "Usage: brain-crypt.sh rotate <api_token> <new_key> [old_key]"; exit 1; }
        cmd_rotate "$2" "$3" "${4:-}" "${5:-default}"
        ;;
    status)
        cmd_status
        ;;
    *)
        usage
        ;;
esac
