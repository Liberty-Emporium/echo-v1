# health-checker

Check the health of all Liberty-Emporium apps in one sweep.

## When to use
- Jay asks "how are the apps doing?"
- Before/after a deployment
- Routine check during heartbeat

## All app URLs to check
```bash
APPS=(
  "AI Agent Widget|https://ai-agent-widget-production.up.railway.app"
  "Contractor Pro AI|https://contractor-pro-ai-production.up.railway.app"
  "Pet Vet AI|https://pet-vet-ai-production.up.railway.app"
  "Keep Your Secrets|https://ai-api-tracker-production.up.railway.app"
  "Liberty Inventory|https://liberty-emporium-inventory-demo-app-production.up.railway.app"
  "Dropship Shipping|https://dropship-shipping-production.up.railway.app"
  "Jay Portfolio|https://jay-portfolio-production.up.railway.app"
  "Consignment Solutions|https://web-production-43ce4.up.railway.app"
)

for app in "${APPS[@]}"; do
  NAME="${app%%|*}"
  URL="${app##*|}"
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$URL/health" 2>/dev/null)
  HEALTH=$(curl -s --max-time 10 "$URL/health" 2>/dev/null)
  echo "$NAME: HTTP $STATUS — $HEALTH"
done
```

## Expected response
`{"status":"ok","db":"ok"}` with HTTP 200

## If an app is down
1. Check Railway dashboard for that service
2. Look at deployment logs
3. Try manual redeploy in Railway UI
4. If DB issue: check volume is mounted at /data

  "Grace App|https://web-production-1015f.up.railway.app"
