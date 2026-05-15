# Sweet Spot Custom Cakes — Site Monitor Skill

## Purpose
Monitor Sweet Spot Custom Cakes (`sweet-spot-cakes.up.railway.app`) for downtime,
errors, and performance issues. Alert Jay immediately if anything is wrong.

## When to Run
- During every heartbeat check
- Anytime Jay asks "how is Sweet Spot?" / "is the site up?" / "check Sweet Spot"
- After any deploy to Sweet Spot

## How to Check

### 1. Direct Health Probe
```bash
curl -s -o /dev/null -w "%{http_code} %{time_total}s" https://sweet-spot-cakes.up.railway.app/health
```
- Expected: `200` in under 2s
- If non-200 or timeout → site is DOWN

### 2. EcDash Monitor Status API
```bash
ECDASH_TOKEN=$(cat /root/.secrets/ecdash_reporter_token)
curl -s -H "X-Reporter-Token: $ECDASH_TOKEN" \
  https://jay-portfolio-production.up.railway.app/api/monitor/status
```
Parse the JSON — find `app == "Sweet Spot Custom Cakes"` and check:
- `status`: should be `"ok"` (not `"down"`)
- `stale`: should be `false`
- `age_minutes`: should be < 10
- `errors_24h`: ideally 0; if > 0 investigate
- `last_event`: look for `shutdown` or `crash` events

### 3. Check Public Pages
```bash
for path in "/" "/menu" "/join"; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "https://sweet-spot-cakes.up.railway.app$path")
  echo "$path → $code"
done
```

## Alert Thresholds
| Condition | Action |
|-----------|--------|
| `/health` returns non-200 | 🔴 ALERT Jay immediately |
| `age_minutes` > 10 (stale pings) | 🔴 ALERT — app may be down |
| `errors_24h` > 5 | 🟡 Warn Jay |
| Response time > 3s | 🟡 Warn — performance degraded |
| `last_event.event == "shutdown"` | 🔴 ALERT — check Railway logs |

## Alerting Jay
When Sweet Spot is DOWN or has critical errors, say:
> 🚨 **Sweet Spot is DOWN** — `sweet-spot-cakes.up.railway.app` is not responding.
> Last ping: X minutes ago. Last event: [event]. Errors (24h): N.
> Check Railway: https://railway.app/project/a776da33-228a-4a8b-bede-d1bf4cfe3c77

When all clear:
> ✅ Sweet Spot is healthy — last ping Xm ago, 0 errors in 24h.

## Railway Quick Links
- Project: https://railway.app/project/a776da33-228a-4a8b-bede-d1bf4cfe3c77
- Service ID: 484711dc-5f65-4cfd-b299-189b5eb86800
- Env ID: d7d33fe5-14ef-4870-997a-66ee6a7bacf4

## Auto-Restart (if down)
If the site is down and last deployment shows SUCCESS, trigger a redeploy:
```bash
RAILWAY_TOKEN=$(cat /root/.secrets/railway_token)
curl -s -X POST https://backboard.railway.app/graphql/v2 \
  -H "Authorization: Bearer $RAILWAY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"mutation { serviceInstanceRedeploy(serviceId: \"484711dc-5f65-4cfd-b299-189b5eb86800\", environmentId: \"d7d33fe5-14ef-4870-997a-66ee6a7bacf4\") }"}'
```
Wait 90s then re-check.

## State File
Track state in `memory/sweet-spot-status.json`:
```json
{
  "last_checked": 1234567890,
  "last_status": "ok",
  "last_age_minutes": 2.1,
  "errors_24h": 0,
  "alerted": false,
  "alert_sent_at": null
}
```
Only alert Jay ONCE per downtime — set `alerted: true` after alerting.
Reset `alerted: false` when site comes back up.
