#!/usr/bin/env bash
# plant_key.sh — Plant KiloClaw's SSH public key on a remote machine
# Usage: bash plant_key.sh <user> <ip>
# The user must paste the generated command into their terminal.
# Call this when a machine is new and key auth isn't set up yet.

set -euo pipefail

USER="${1:-}"
IP="${2:-}"

if [[ -z "$USER" || -z "$IP" ]]; then
  echo "Usage: $0 <username> <ip>"
  exit 1
fi

# Ensure we have a key
if [[ ! -f ~/.ssh/id_ed25519 ]]; then
  ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N "" -C "kiloclaw@liberty-emporium.ai"
fi

PUBKEY=$(cat ~/.ssh/id_ed25519.pub)

echo ""
echo "Ask ${USER}@${IP} to run this command:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "mkdir -p ~/.ssh && echo \"$PUBKEY\" >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys && chmod 700 ~/.ssh"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Once done, test with:"
echo "  bash remote.sh ${USER}@${IP} 'whoami'"
