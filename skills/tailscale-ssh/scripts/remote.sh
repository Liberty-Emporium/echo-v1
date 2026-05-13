#!/usr/bin/env bash
# remote.sh — Run a command on a Liberty-Emporium Tailscale machine
# Usage: bash remote.sh <user@ip> <command>
# Example: bash remote.sh lol@100.88.205.44 "whoami"
#
# Prerequisites:
#   - Tailscale running in userspace mode with SOCKS5 on localhost:1055
#   - ~/.ssh/id_ed25519 present (kiloclaw@liberty-emporium.ai key)
#   - nc (netcat-openbsd) installed

set -euo pipefail

TARGET="${1:-}"
CMD="${2:-echo connected}"

if [[ -z "$TARGET" ]]; then
  echo "Usage: $0 <user@ip_or_hostname> [command]"
  exit 1
fi

# Ensure SSH key exists
if [[ ! -f ~/.ssh/id_ed25519 ]]; then
  echo "ERROR: ~/.ssh/id_ed25519 not found. Run: ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N '' -C 'kiloclaw@liberty-emporium.ai'"
  exit 1
fi

# Ensure nc is available
if ! command -v nc &>/dev/null; then
  apt-get install -y netcat-openbsd -q 2>/dev/null || true
fi

ssh \
  -o StrictHostKeyChecking=no \
  -o ConnectTimeout=15 \
  -o ProxyCommand="nc -x localhost:1055 %h %p" \
  -i ~/.ssh/id_ed25519 \
  "$TARGET" "$CMD"
