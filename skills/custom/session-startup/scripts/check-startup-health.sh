#!/bin/bash
# check-startup-health.sh — Pre-flight check before restore-brain.sh
# Tells Echo what's present, what's missing, what needs attention

WORKSPACE="/root/.openclaw/workspace"
ECHO_REPO="$WORKSPACE/echo-v1"
SECRETS="/root/.secrets"
TODAY=$(date +%Y-%m-%d)

echo ""
echo "🔍 Echo Startup Health Check — $TODAY"
echo "=================================================="

ISSUES=0

# ── Secrets ──────────────────────────────────────────────
echo ""
echo "🔑 Secrets:"
if [ -f "$SECRETS/github_token" ] && [ -s "$SECRETS/github_token" ]; then
  echo "  ✅ GitHub token present"
else
  echo "  ❌ GitHub token MISSING — ask Jay to paste a new one"
  ISSUES=$((ISSUES+1))
fi

if [ -f "$SECRETS/gitlab_token" ] && [ -s "$SECRETS/gitlab_token" ]; then
  echo "  ✅ GitLab token present"
else
  echo "  ⚠️  GitLab token missing (backup only — non-fatal)"
fi

if [ -f "$SECRETS/kys_api_token" ] && [ -s "$SECRETS/kys_api_token" ]; then
  echo "  ✅ KYS (brain encryption) token present"
else
  echo "  ℹ️  KYS token not set — brain pushes will be plaintext"
fi

# ── Repo ─────────────────────────────────────────────────
echo ""
echo "📁 echo-v1 repo:"
if [ -d "$ECHO_REPO/.git" ]; then
  cd "$ECHO_REPO"
  LAST_COMMIT=$(git log -1 --format="%h %s (%ar)" 2>/dev/null || echo "unknown")
  echo "  ✅ Cloned — last commit: $LAST_COMMIT"
  
  # Check remotes
  GH_REMOTE=$(git remote get-url origin 2>/dev/null | sed 's/https:\/\/[^@]*@/https:\/\/TOKEN@/' || echo "not set")
  GL_REMOTE=$(git remote get-url gitlab 2>/dev/null | sed 's/https:\/\/[^@]*@/https:\/\/TOKEN@/' || echo "not set")
  echo "  📡 GitHub remote: $GH_REMOTE"
  echo "  📡 GitLab remote: $GL_REMOTE"
else
  echo "  ❌ NOT CLONED at $ECHO_REPO"
  echo "     Fix: clone it after saving GitHub token"
  ISSUES=$((ISSUES+1))
fi

# ── Memory files ─────────────────────────────────────────
echo ""
echo "🧠 Memory files:"
for f in MEMORY.md SOUL.md USER.md AGENTS.md IDENTITY.md HEARTBEAT.md; do
  if [ -f "$WORKSPACE/$f" ]; then
    SIZE=$(wc -l < "$WORKSPACE/$f")
    echo "  ✅ $f ($SIZE lines)"
  else
    echo "  ⚠️  $f missing"
  fi
done

# ── Today's diary ─────────────────────────────────────────
echo ""
echo "📅 Diary:"
if [ -f "$WORKSPACE/memory/$TODAY.md" ]; then
  LINES=$(wc -l < "$WORKSPACE/memory/$TODAY.md")
  echo "  ✅ Today ($TODAY) — $LINES lines"
else
  echo "  ℹ️  No entry for today yet ($TODAY)"
fi

YESTERDAY=$(date -d "yesterday" +%Y-%m-%d 2>/dev/null || date -v-1d +%Y-%m-%d 2>/dev/null)
if [ -f "$WORKSPACE/memory/$YESTERDAY.md" ]; then
  echo "  ✅ Yesterday ($YESTERDAY) present"
fi

# ── Open TODOs ────────────────────────────────────────────
TODO_FILE="$WORKSPACE/memory/todos.json"
echo ""
echo "📋 TODOs:"
if [ -f "$TODO_FILE" ]; then
  OPEN=$(python3 -c "
import json
data = json.load(open('$TODO_FILE'))
open_todos = [t for t in data.get('todos', []) if t['status'] in ('open','in-progress')]
high = [t for t in open_todos if t['priority'] == 'high']
print(f'  {len(open_todos)} open ({len(high)} high priority)')
for t in high:
    print(f'  🔴 [{t[\"id\"]}] {t[\"task\"]}')
" 2>/dev/null || echo "  (could not read todos.json)")
  echo "$OPEN"
else
  echo "  ℹ️  No todos.json yet"
fi

# ── Summary ──────────────────────────────────────────────
echo ""
echo "=================================================="
if [ "$ISSUES" -eq 0 ]; then
  echo "✅ All clear — ready to run restore-brain.sh"
else
  echo "⚠️  $ISSUES issue(s) need attention before restore"
fi
echo ""
