#!/usr/bin/env bash
# copy_to.sh — SCP a file to a Liberty-Emporium Tailscale machine
# Usage: bash copy_to.sh <local_file> <user@ip:remote_path>
# Example: bash copy_to.sh /tmp/fix.sh lol@100.88.205.44:/tmp/fix.sh

set -euo pipefail

LOCAL="${1:-}"
REMOTE="${2:-}"

if [[ -z "$LOCAL" || -z "$REMOTE" ]]; then
  echo "Usage: $0 <local_file> <user@ip:remote_path>"
  exit 1
fi

if ! command -v nc &>/dev/null; then
  apt-get install -y netcat-openbsd -q 2>/dev/null || true
fi

scp \
  -o StrictHostKeyChecking=no \
  -o ConnectTimeout=15 \
  -o ProxyCommand="nc -x localhost:1055 %h %p" \
  -i ~/.ssh/id_ed25519 \
  "$LOCAL" "$REMOTE"
