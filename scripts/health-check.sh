#!/bin/bash
# health-check.sh — Ping /health on all live Railway apps
# Usage: ./health-check.sh

APPS=(
  "Liberty Inventory|https://liberty-emporium-inventory-demo-app-production.up.railway.app"
  "Jay Portfolio|https://jay-portfolio-production.up.railway.app"
  "Consignment|https://web-production-43ce4.up.railway.app"
  "Jay Keep Secrets|https://ai-api-tracker-production.up.railway.app"
  "Pet Vet AI|https://pet-vet-ai-production.up.railway.app"
)

echo "🏥 App Health Check — $(date -u '+%Y-%m-%d %H:%M UTC')"
echo "=================================================="
ALL_OK=true

for entry in "${APPS[@]}"; do
  NAME="${entry%%|*}"
  URL="${entry##*|}"
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 8 "$URL/health" 2>/dev/null)
  RESP=$(curl -s --max-time 8 "$URL/health" 2>/dev/null)

  if [ "$STATUS" = "200" ]; then
    echo "  ✅ $NAME ($STATUS) — $RESP"
  elif [ "$STATUS" = "000" ]; then
    echo "  ❌ $NAME — TIMEOUT / DOWN"
    ALL_OK=false
  else
    echo "  ⚠️  $NAME ($STATUS) — $RESP"
    ALL_OK=false
  fi
done

echo ""
$ALL_OK && echo "🟢 All systems go" || echo "🔴 Action needed"
