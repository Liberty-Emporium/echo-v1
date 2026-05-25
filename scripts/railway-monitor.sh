#!/usr/bin/env bash
# railway-monitor.sh — Auto-redeploy Railway services + report to EcDash
# Cron: */5 * * * *

RAILWAY_TOKEN="9728986d-5225-4529-9207-72d40b04e691"
ECDASH_TOKEN="u8aKEAXz-ulQyaGLa11ALMR0LYUv98a6pZuiP4ErXXY"
ECDASH_URL="https://jay-portfolio-production.up.railway.app/api/echo-bridge"
LOG="/root/.openclaw/workspace/echo-v1/scripts/railway-monitor.log"

# service_id|env_id|name|health_url
SERVICES=(
  "5ec64ac9-06b1-44a6-8604-047a9804bff8|5c86d574-b1a0-42cf-851c-34c533f52431|Jays-Portfolio|https://jay-portfolio-production.up.railway.app/health"
  "484711dc-5f65-4cfd-b299-189b5eb86800|d7d33fe5-14ef-4870-997a-66ee6a7bacf4|Sweet-Spot-Cakes|https://sweet-spot-cakes.up.railway.app/health"
  "188b1389-302d-4e9c-9821-fdbb2b2afee6|f8cb2a58-b62e-4c92-ad8f-5fd1d673fefe|Pet-Vet-AI|https://pet-vet-ai-production.up.railway.app/health"
  "79ffa602-0b96-42d3-a4f1-19e3a9d578f6|352f2d88-0bbb-4909-befb-6d670aa6d52e|Drop-Shipping|https://drop-shipping-by-alexander-ai-solutions-production.up.railway.app/health"
  "23ef2d0a-dceb-4f44-ab0d-f0cd3c84f04f|792184db-43b4-4796-8b7f-763313ff312f|Contractor-Pro-AI|https://contractor-pro-ai-production.up.railway.app/health"
  "ef7e7fbf-8bf3-43a8-8e26-424eb94bccf6|b25793b4-7977-48b4-ae45-b73a73e5b1b4|Remote-Repair-Services|https://remote-repair-services-production.up.railway.app/health"
  "b7793de8-5a28-4349-95eb-ddff8e1d46ef|e94bef32-f17a-4e89-b43f-e5de97f02727|Liberty-Inventory|https://liberty-emporium-and-thrift-inventory-app-production.up.railway.app/health"
  "631d5576-2012-46c4-b441-5f97f76c8f46|f9e636bc-7c47-4b69-9605-49e6ed1071e3|Echo-AI|https://alexander-ai-support-dashboard-production.up.railway.app/health"
  "fcb012b7-cb89-4733-90df-26eabac82d8b|a94e3287-e9da-463c-85c9-c07f354793a2|Extra-Mile-Photography|https://extra-mile-photography-production.up.railway.app/health"
)

TS=$(date '+%Y-%m-%d %H:%M:%S')
REDEPLOYED=()
FAILED_DEPLOY=()

for entry in "${SERVICES[@]}"; do
  SVC_ID=$(echo "$entry" | cut -d'|' -f1)
  ENV_ID=$(echo "$entry" | cut -d'|' -f2)
  NAME=$(echo "$entry"  | cut -d'|' -f3)

  STATUS=$(curl -s -X POST https://backboard.railway.app/graphql/v2 \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $RAILWAY_TOKEN" \
    -d "{\"query\":\"{ deployments(input: { serviceId: \\\"$SVC_ID\\\", environmentId: \\\"$ENV_ID\\\" }, first: 1) { edges { node { status } } } }\"}" \
    | python3 -c "import json,sys; d=json.load(sys.stdin); e=d['data']['deployments']['edges']; print(e[0]['node']['status'] if e else 'NO_DEPLOYMENTS')" 2>/dev/null)

  if [[ "$STATUS" == "REMOVED" ]]; then
    echo "[$TS] REMOVED → redeploying $NAME" | tee -a "$LOG"
    RESULT=$(curl -s -X POST https://backboard.railway.app/graphql/v2 \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $RAILWAY_TOKEN" \
      -d "{\"query\":\"mutation { serviceInstanceRedeploy(environmentId: \\\"$ENV_ID\\\", serviceId: \\\"$SVC_ID\\\") }\"}")
    if echo "$RESULT" | grep -q "true"; then
      REDEPLOYED+=("$NAME")
      echo "[$TS] ✅ Redeployed $NAME" >> "$LOG"
    else
      FAILED_DEPLOY+=("$NAME")
      echo "[$TS] ❌ Redeploy failed for $NAME: $RESULT" >> "$LOG"
    fi
  else
    echo "[$TS] OK ($STATUS) $NAME" >> "$LOG"
  fi
done

# Report to EcDash bridge if anything was redeployed or failed
if [ ${#REDEPLOYED[@]} -gt 0 ] || [ ${#FAILED_DEPLOY[@]} -gt 0 ]; then
  MSG="[Monitor $TS]"
  [ ${#REDEPLOYED[@]} -gt 0 ] && MSG="$MSG Redeployed: ${REDEPLOYED[*]}."
  [ ${#FAILED_DEPLOY[@]} -gt 0 ] && MSG="$MSG FAILED to redeploy: ${FAILED_DEPLOY[*]} — needs attention!"
  curl -s -X POST "$ECDASH_URL" \
    -H "Authorization: Bearer $ECDASH_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"task\": \"$MSG\"}" >> "$LOG" 2>&1
  echo "" >> "$LOG"
fi

# Trim log to last 500 lines
tail -500 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"
