# Railway Services — Liberty Emporium

**Project ID:** `00830a2f-e287-427c-bc10-910dfe2485e8`
**Token:** `/root/.secrets/railway_token` (ask Jay if missing — get from railway.com → Account Settings → Tokens)
**API Endpoint:** `https://backboard.railway.app/graphql/v2`

> ⚠️ Service IDs below need to be populated. Run the service-list query from SKILL.md once the railway_token is stored.

## Environment IDs
| Name | ID |
|------|-----|
| production | _(run query to get)_ |

## Services

| Service Name | Repo | Live URL | Service ID |
|---|---|---|---|
| EcDash (alexander-ai-dashboard) | Liberty-Emporium/alexander-ai-dashboard | https://jay-portfolio-production.up.railway.app | _(query)_ |
| Alexander AI Support Dashboard | Liberty-Emporium/Alexander-AI-Support-Dashboard | https://agents.alexanderai.site | _(query)_ |
| FloodClaim Pro | Liberty-Emporium/alexander-ai-floodclaim | https://billy-floods.up.railway.app | _(query)_ |
| AI Agent Widget | Liberty-Emporium/alexander-ai-agent-widget | https://ai-agent-widget-production.up.railway.app | _(query)_ |
| Pet Vet AI | Liberty-Emporium/alexander-ai-petvet | (Railway) | _(query)_ |
| Contractor Pro AI | Liberty-Emporium/alexander-ai-contractor | (Railway) | _(query)_ |
| Liberty Oil & Propane | Liberty-Emporium/liberty-oil-website | https://liberty-oil-propane.up.railway.app | _(query)_ |

## How to Populate This File

Run once when railway_token is available:

```python
import json, urllib.request

TOKEN = open("/root/.secrets/railway_token").read().strip()

def gql(q):
    body = json.dumps({"query": q}).encode()
    req = urllib.request.Request(
        "https://backboard.railway.app/graphql/v2",
        data=body,
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    )
    return json.loads(urllib.request.urlopen(req, timeout=15).read())

result = gql("""
query {
  project(id: "00830a2f-e287-427c-bc10-910dfe2485e8") {
    environments { edges { node { id name } } }
    services { edges { node { id name } } }
  }
}
""")
print(json.dumps(result, indent=2))
```

## Key Env Vars Per Service

### Alexander AI Support Dashboard
- `ADMIN_PASSWORD` — dashboard login password (currently: `Treetop121570!`)
- `JWT_SECRET` — JWT signing secret
- `RAILWAY_VOLUME_MOUNT_PATH` — SQLite DB volume path (usually `/data`)

### EcDash (alexander-ai-dashboard)
- `ADMIN_PASSWORD` — dashboard login (currently: `Mhall001!`)
- `JWT_SECRET` — JWT signing secret
- `BRAIN_SYNC_TOKEN` — token for Echo's brain sync

## Deploy Flow
All services auto-deploy from GitHub `master`/`main` branch push.
To force a redeploy without a code change: use `deploymentRedeploy` mutation (see SKILL.md).
