#!/bin/bash
# bootstrap.sh — Echo's post-reboot setup script
# Run this on a fresh KiloClaw instance to restore full capability
# Usage: bash /root/.openclaw/workspace/echo-v1/scripts/bootstrap.sh
# Last updated: 2026-05-12

set -e
echo "🚀 Echo Bootstrap starting..."
echo "================================"

# ── 1. Install pip + tools ────────────────────────────────────────────────────
echo ""
echo "📦 Installing Python tools..."
curl -sS https://bootstrap.pypa.io/get-pip.py | python3 - --break-system-packages --quiet 2>/dev/null || true
python3 -m pip install bandit ruff playwright pytest pytest-flask httpx black alembic --break-system-packages --quiet
python3 -m playwright install chromium --quiet 2>/dev/null || true
echo "  ✅ bandit $(bandit --version 2>&1 | head -1)"
echo "  ✅ ruff $(ruff --version)"
echo "  ✅ playwright $(python3 -m playwright --version 2>/dev/null)"
echo "  ✅ pytest $(pytest --version 2>&1 | head -1)"
echo "  ✅ black $(black --version 2>&1 | head -1)"

# ── 2. Git config ─────────────────────────────────────────────────────────────
echo ""
echo "🔧 Configuring git..."
git config --global user.email "echo@liberty-emporium.ai"
git config --global user.name "Echo (KiloClaw)"
echo "  ✅ git configured"

# ── 3. Secrets directory ──────────────────────────────────────────────────────
echo ""
echo "🔐 Setting up secrets directory..."
mkdir -p /root/.secrets
chmod 700 /root/.secrets
if [ ! -f /root/.secrets/github_token ]; then
  echo "  ⚠️  /root/.secrets/github_token NOT FOUND — ask Jay or add manually"
else
  echo "  ✅ github_token present"
fi
if [ ! -f /root/.secrets/gitlab_token ]; then
  echo "  ⚠️  /root/.secrets/gitlab_token NOT FOUND — ask Jay or add manually"
else
  echo "  ✅ gitlab_token present"
fi
if [ ! -f /root/.secrets/willie_api_key ]; then
  echo "  ⚠️  /root/.secrets/willie_api_key NOT FOUND — get from AI Agent Widget"
else
  echo "  ✅ willie_api_key present"
fi
if [ ! -f /root/.secrets/ecdash_token ]; then
  echo "  ⚠️  /root/.secrets/ecdash_token NOT FOUND — get from EcDash → Settings → Create Token"
else
  echo "  ✅ ecdash_token present"
fi

# ── 4. Clone echo-v1 (brain repo only) ───────────────────────────────────────
echo ""
echo "📁 Cloning brain repo..."
if [ ! -f /root/.secrets/github_token ]; then
  echo "  ❌ Cannot clone — github_token missing. Add it to /root/.secrets/ and re-run."
else
  GH_TOKEN=$(cat /root/.secrets/github_token)
  cd /root/.openclaw/workspace

  if [ -d "echo-v1" ]; then
    echo "  ⏩ echo-v1 (already cloned, pulling latest...)"
    cd echo-v1
    git pull --quiet 2>/dev/null || true
    cd ..
  else
    git clone https://oauth2:${GH_TOKEN}@github.com/Liberty-Emporium/echo-v1.git --quiet && echo "  ✅ echo-v1 cloned"
  fi

  # Set token in remote for pushing
  cd /root/.openclaw/workspace/echo-v1
  git remote set-url origin https://oauth2:${GH_TOKEN}@github.com/Liberty-Emporium/echo-v1.git 2>/dev/null || true
  cd /root/.openclaw/workspace
fi

# ── 5. Set up GitLab remote on echo-v1 ───────────────────────────────────────
echo ""
echo "🦊 Setting up GitLab backup remote..."
if [ -f /root/.secrets/gitlab_token ] && [ -d "/root/.openclaw/workspace/echo-v1" ]; then
  GL_TOKEN=$(cat /root/.secrets/gitlab_token)
  cd /root/.openclaw/workspace/echo-v1
  git remote remove gitlab 2>/dev/null || true
  git remote add gitlab https://oauth2:${GL_TOKEN}@gitlab.com/Liberty-Emporium/echo-v1.git 2>/dev/null || true
  echo "  ✅ echo-v1 → gitlab remote set"
  cd /root/.openclaw/workspace
else
  echo "  ⚠️  gitlab_token missing or echo-v1 not cloned — skipping"
fi

# ── 6. Dashboard health check + brain sync ───────────────────────────────────
echo ""
echo "🏥 Dashboard health check..."
DASHBOARD_URL="https://jay-portfolio-production.up.railway.app"

HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$DASHBOARD_URL/" 2>/dev/null || echo "000")
if [ "$HTTP_STATUS" = "200" ]; then
  echo "  ✅ EcDash: HTTP $HTTP_STATUS — dashboard is live"
else
  echo "  ⚠️  EcDash: HTTP $HTTP_STATUS — may be down or slow"
fi

# Check echo-bridge queue
if [ -f /root/.secrets/ecdash_token ]; then
  ECDASH_TOKEN=$(cat /root/.secrets/ecdash_token)
  BRIDGE_RESP=$(curl -s -H "Authorization: Bearer $ECDASH_TOKEN" "$DASHBOARD_URL/api/echo-bridge" 2>/dev/null || echo "{}")
  TASK_COUNT=$(echo "$BRIDGE_RESP" | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d.get('tasks',[])))" 2>/dev/null || echo "?")
  echo "  📬 Echo-bridge queue: $TASK_COUNT pending task(s)"
else
  echo "  ⚠️  ecdash_token missing — skipping bridge check"
fi

# Read notes Jay left for Echo
echo ""
echo "📝 Reading notes from Jay..."
if [ -f /root/.openclaw/workspace/echo-v1/scripts/read-notes-from-dashboard.py ]; then
  python3 /root/.openclaw/workspace/echo-v1/scripts/read-notes-from-dashboard.py 2>&1 | sed 's/^/  /'
else
  echo "  ⚠️  read-notes-from-dashboard.py not found — skipping"
fi

# Sync brain files to dashboard
echo ""
echo "🧠 Syncing brain to dashboard..."
if [ -f /root/.openclaw/workspace/echo-v1/scripts/sync-brain-to-dashboard.py ]; then
  python3 /root/.openclaw/workspace/echo-v1/scripts/sync-brain-to-dashboard.py 2>&1 | sed 's/^/  /'
else
  echo "  ⚠️  sync-brain-to-dashboard.py not found — skipping"
fi

# ── 7. Tailscale ─────────────────────────────────────────────────────────────
echo ""
echo "🔗 Starting Tailscale..."
if [ -f /usr/local/bin/tailscaled-start.sh ]; then
  bash /usr/local/bin/tailscaled-start.sh 2>&1 | sed 's/^/  /'
else
  echo "  ⚠️  tailscaled-start.sh missing — creating it now..."
  cat > /usr/local/bin/tailscaled-start.sh << 'TSEOF'
#!/bin/bash
STATEDIR="/root/.tailscale-state"
AUTHKEY_FILE="/root/.secrets/tailscale_authkey"
LOGFILE="/tmp/tailscaled.log"
if ! command -v tailscaled &>/dev/null; then
  curl -fsSL https://tailscale.com/install.sh | sh >> "$LOGFILE" 2>&1
fi
if ! pgrep -x tailscaled > /dev/null; then
  mkdir -p "$STATEDIR"
  /usr/sbin/tailscaled --tun=userspace-networking --socks5-server=localhost:1055 --statedir="$STATEDIR" >> "$LOGFILE" 2>&1 &
  sleep 4
fi
STATUS=$(tailscale status 2>&1)
if echo "$STATUS" | grep -q "Logged out"; then
  if [ -f "$AUTHKEY_FILE" ]; then
    tailscale up --authkey="$(cat $AUTHKEY_FILE)" --accept-routes >> "$LOGFILE" 2>&1
  fi
fi
tailscale status 2>&1
TSEOF
  chmod +x /usr/local/bin/tailscaled-start.sh
  bash /usr/local/bin/tailscaled-start.sh 2>&1 | sed 's/^/  /'
fi

echo ""
echo "================================"
echo "✅ Echo Bootstrap complete!"
echo ""
echo "Next steps:"
echo "  1. Add /root/.secrets/ecdash_token if missing (EcDash → Settings → Create Token → label: echo-bridge)"
echo "  2. Add /root/.secrets/willie_api_key if missing"
echo "  3. Check https://jay-portfolio-production.up.railway.app/dashboard"
echo "  4. Read echo-v1/memory/$(date +%Y-%m-%d).md for today's context"
