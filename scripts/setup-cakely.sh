#!/bin/bash
# Setup Cakely agent brain + actions in AI Agent Widget
# Run after Railway deploys both apps

WIDGET_URL="https://ai-agent-widget-production.up.railway.app"
SWEET_URL="https://sweet-spot-cakes-production.up.railway.app"  # update when deployed
CAKELY_TOKEN="cakely-sweet-spot-2026"

# Get session
SESSION_COOKIE=$(curl -si -X POST "${WIDGET_URL}/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "email=alexanderjay70@gmail.com" \
  --data-urlencode "password=Treetop121570!" \
  | grep -i "set-cookie" | head -1 | cut -d';' -f1 | sed 's/.*set-cookie: //i')

echo "Logged in."

# Find Cakely agent ID
CAKELY_ID=$(curl -s -H "Cookie: $SESSION_COOKIE" "${WIDGET_URL}/dashboard" \
  | python3 -c "
import sys,re,json
html=sys.stdin.read()
ids=re.findall(r'/agent/([A-Za-z0-9_\-]{10,})', html)
print(' '.join(list(set(ids))))
")
echo "Agent IDs: $CAKELY_ID"

# Pull brain from Sweet Spot
BRAIN=$(curl -s "${SWEET_URL}/cakely/api/memory")
echo "Brain fetched: $(echo $BRAIN | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d.get("ok","fail"))')"

# For each candidate ID check if it's Cakely
for ID in $CAKELY_ID; do
  NAME_CHECK=$(curl -s -H "Cookie: $SESSION_COOKIE" "${WIDGET_URL}/agent/${ID}/brain/api" \
    | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('identity_md','')[:20])" 2>/dev/null)
  if echo "$NAME_CHECK" | grep -qi "cakely\|sweet\|bakery"; then
    echo "Found Cakely: $ID"
    AGENT_ID=$ID
    break
  fi
  # Also check if identity is empty — might be a new blank agent
  if [ -z "$NAME_CHECK" ] || [ "$NAME_CHECK" = "[no identity]" ]; then
    echo "Candidate blank agent: $ID"
  fi
done

echo ""
echo "To finish setup, go to:"
echo "${WIDGET_URL}/dashboard"
echo "Find Cakely → Brain Editor → all 3 tabs are pre-populated from memory endpoint"
echo ""
echo "Then add these actions:"
echo "1. get_dashboard    GET ${SWEET_URL}/cakely/api/dashboard"
echo "2. get_todays_orders GET ${SWEET_URL}/cakely/api/orders/today"
echo "3. lookup_order     GET ${SWEET_URL}/cakely/api/orders?q={query}"
echo "4. get_low_stock    GET ${SWEET_URL}/cakely/api/inventory/low"
echo "5. get_inventory    GET ${SWEET_URL}/cakely/api/inventory"
echo "6. lookup_customer  GET ${SWEET_URL}/cakely/api/customers?q={query}"
echo "7. get_staff_status GET ${SWEET_URL}/cakely/api/employees/status"
echo "8. get_recipes      GET ${SWEET_URL}/cakely/api/recipes"
echo ""
echo "All actions need header: Authorization: Bearer ${CAKELY_TOKEN}"
