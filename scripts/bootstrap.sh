#!/bin/bash
# bootstrap.sh — Echo's post-reboot setup script
# Run this on a fresh KiloClaw instance to restore full capability
# Usage: bash /root/.openclaw/workspace/echo-v1/scripts/bootstrap.sh

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

# ── 4. Clone repos ────────────────────────────────────────────────────────────
echo ""
echo "📁 Cloning repos..."
if [ ! -f /root/.secrets/github_token ]; then
  echo "  ❌ Cannot clone — github_token missing. Add it to /root/.secrets/ and re-run."
else
  GH_TOKEN=$(cat /root/.secrets/github_token)
  cd /root/.openclaw/workspace

  REPOS=(
    "echo-v1"
    "floodclaim-pro"
    "AI-Agent-Widget"
    "jay-portfolio"
    "pet-vet-ai"
    "Contractor-Pro-AI"
    "Dropship-Shipping"
    "Consignment-Solutions"
    "Liberty-Emporium-Inventory-App"
    "liberty-oil-website"
  )

  for repo in "${REPOS[@]}"; do
    if [ -d "$repo" ]; then
      echo "  ⏩ $repo (already cloned)"
    else
      git clone https://oauth2:${GH_TOKEN}@github.com/Liberty-Emporium/${repo}.git --quiet && echo "  ✅ $repo"
    fi
  done

  # Set token in git remotes for pushing
  for repo in "${REPOS[@]}"; do
    if [ -d "$repo" ]; then
      cd /root/.openclaw/workspace/$repo
      git remote set-url origin https://oauth2:${GH_TOKEN}@github.com/Liberty-Emporium/${repo}.git 2>/dev/null || true
      cd /root/.openclaw/workspace
    fi
  done
fi

# ── 5. Set up GitLab remotes ──────────────────────────────────────────────────
echo ""
echo "🦊 Setting up GitLab backup remotes..."
if [ -f /root/.secrets/gitlab_token ]; then
  GL_TOKEN=$(cat /root/.secrets/gitlab_token)
  for repo in echo-v1 floodclaim-pro AI-Agent-Widget jay-portfolio; do
    if [ -d "/root/.openclaw/workspace/$repo" ]; then
      cd /root/.openclaw/workspace/$repo
      git remote remove gitlab 2>/dev/null || true
      git remote add gitlab https://oauth2:${GL_TOKEN}@gitlab.com/Liberty-Emporium/${repo}.git 2>/dev/null || true
      echo "  ✅ $repo → gitlab remote set"
      cd /root/.openclaw/workspace
    fi
  done
else
  echo "  ⚠️  gitlab_token missing — skipping GitLab remotes"
fi

# ── 6. Quick health check ─────────────────────────────────────────────────────
echo ""
echo "🏥 Health check..."
echo -n "  FloodClaim Pro: " && curl -s https://billy-floods.up.railway.app/health 2>/dev/null || echo "unreachable"
echo -n "  EcDash: " && curl -s -o /dev/null -w "HTTP %{http_code}" https://jay-portfolio-production.up.railway.app/ 2>/dev/null || echo "unreachable"
echo -n "  AI Agent Widget: " && curl -s -o /dev/null -w "HTTP %{http_code}" https://ai-agent-widget-production.up.railway.app/ 2>/dev/null || echo "unreachable"

echo ""
echo "================================"
echo "✅ Echo Bootstrap complete!"
echo ""
echo "Next steps:"
echo "  1. Add /root/.secrets/github_token if missing"
echo "  2. Add /root/.secrets/gitlab_token if missing"
echo "  3. Run: python3 echo-v1/scripts/bug-hunter.py floodclaim-pro"
echo "  4. Read echo-v1/memory/$(date +%Y-%m-%d).md for today's context"
