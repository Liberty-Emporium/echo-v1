#!/bin/bash
# status.sh — Full Alexander AI Digital portfolio status
# Shows: all app health, recent commits, open issues, GitLab sync status

GH_TOKEN=$(cat /root/.secrets/github_token 2>/dev/null)
GL_TOKEN=$(cat /root/.secrets/gitlab_token 2>/dev/null)

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║   Alexander AI Digital — Portfolio Status        ║"
echo "║   $(date -u '+%Y-%m-%d %H:%M UTC')                    ║"
echo "╚══════════════════════════════════════════════════╝"

# ── App health ────────────────────────────────────────────────────────
echo ""
echo "🏥 Live App Health:"
APPS=(
  "Liberty Inventory|https://liberty-emporium-inventory-demo-app-production.up.railway.app"
  "Jay Portfolio|https://jay-portfolio-production.up.railway.app"
  "Consignment|https://web-production-43ce4.up.railway.app"
  "Jay Keep Secrets|https://ai-api-tracker-production.up.railway.app"
  "Pet Vet AI|https://pet-vet-ai-production.up.railway.app"
)
for entry in "${APPS[@]}"; do
  NAME="${entry%%|*}"
  URL="${entry##*|}"
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 6 "$URL/health" 2>/dev/null)
  [ "$STATUS" = "200" ] && ICON="✅" || ICON="❌"
  printf "  %s  %-22s %s\n" "$ICON" "$NAME" "($STATUS)"
done

# ── Recent commits ────────────────────────────────────────────────────
echo ""
echo "📝 Recent Activity (last 2 commits per repo):"
REPOS="Liberty-Emporium-Inventory-App Contractor-Pro-AI pet-vet-ai Dropship-Shipping Consignment-Solutions jays-keep-your-secrets list-it-everywhere jay-portfolio"
for REPO in $REPOS; do
  echo ""
  echo "  [$REPO]"
  GH_TOKEN=$GH_TOKEN gh api repos/Liberty-Emporium/$REPO/commits?per_page=2 \
    --jq '.[] | "    \(.sha[0:7]) \(.commit.author.date[0:10]) \(.commit.message | split("\n")[0] | .[0:60])"' 2>/dev/null || echo "    (no access)"
done

# ── Open issues ───────────────────────────────────────────────────────
echo ""
echo "🐛 Open Issues:"
for REPO in $REPOS; do
  COUNT=$(GH_TOKEN=$GH_TOKEN gh api repos/Liberty-Emporium/$REPO/issues?state=open --jq 'length' 2>/dev/null)
  [ "$COUNT" -gt "0" ] 2>/dev/null && echo "  ⚠️  $REPO: $COUNT open"
done

echo ""
echo "══════════════════════════════════════════════════"
