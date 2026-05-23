#!/usr/bin/env bash
# bootstrap.sh — Echo (KiloClaw) fresh instance setup
# Last updated: 2026-05-23
# Run this at session start: bash /root/.openclaw/workspace/echo-v1/scripts/bootstrap.sh

set -e

echo "=== Echo Bootstrap Starting ==="

# 1. Git config
git config --global user.email "echo@liberty-emporium.ai"
git config --global user.name "Echo (KiloClaw)"
echo "[1/7] Git config set."

# 2. Secrets directory
mkdir -p /root/.secrets
chmod 700 /root/.secrets
echo "[2/7] Secrets directory ready. Add secrets manually if not present."

# 3. Python tools
echo "[3/7] Installing Python tools..."
curl -sS https://bootstrap.pypa.io/get-pip.py | python3 - --break-system-packages -q
python3 -m pip install bandit ruff playwright pytest pytest-flask httpx black alembic --break-system-packages -q
playwright install chromium --with-deps 2>/dev/null || true
echo "    Python tools installed."

# 4. Railway CLI
echo "[4/7] Installing Railway CLI..."
npm install -g @railway/cli -q
echo "    railway $(railway --version) ready."

# 5. Tailscale
echo "[5/7] Setting up Tailscale..."
which tailscale &>/dev/null || (curl -fsSL https://tailscale.com/install.sh | sh -s - 2>/dev/null)
if [ -f /root/.secrets/tailscale_authkey ]; then
    tailscaled --state=/root/.tailscale-state &>/dev/null &
    sleep 3
    tailscale up --authkey="$(cat /root/.secrets/tailscale_authkey)" --hostname=kiloclaw-echo-1 &>/dev/null &
    sleep 5
    tailscale status 2>/dev/null | head -1 && echo "    Tailscale connected." || echo "    Tailscale connecting (check manually)."
else
    echo "    SKIP: /root/.secrets/tailscale_authkey not found."
fi

# 6. GitLab backup remote on echo-v1
echo "[6/7] Setting up GitLab remote..."
cd /root/.openclaw/workspace/echo-v1
if [ -f /root/.secrets/gitlab_token ]; then
    GL_TOKEN=$(cat /root/.secrets/gitlab_token)
    git remote get-url gitlab &>/dev/null && \
        git remote set-url gitlab "https://oauth2:${GL_TOKEN}@gitlab.com/Liberty-Emporium/echo-v1.git" || \
        git remote add gitlab "https://oauth2:${GL_TOKEN}@gitlab.com/Liberty-Emporium/echo-v1.git"
    echo "    GitLab remote configured."
else
    echo "    SKIP: /root/.secrets/gitlab_token not found."
fi

# 7. EcDash health check
echo "[7/7] Checking EcDash..."
if [ -f /root/.secrets/ecdash_token ]; then
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
        -H "Authorization: Bearer $(cat /root/.secrets/ecdash_token)" \
        "https://jay-portfolio-production.up.railway.app/api/echo-bridge")
    echo "    EcDash echo-bridge: HTTP $STATUS"
else
    echo "    SKIP: /root/.secrets/ecdash_token not found."
fi

echo ""
echo "=== Bootstrap Complete ==="
echo "Remember to restore cron jobs in KiloClaw Control UI:"
echo "  - Brain backup (every 40 min)"
echo "  - Sweet Spot monitor (every 5 min)"
