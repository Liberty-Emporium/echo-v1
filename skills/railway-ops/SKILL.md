---
name: railway-ops
description: 'Manage Railway deployments for Liberty Emporium / Alexander AI projects. Use when checking service status, reading deployment logs, setting or reading environment variables, triggering redeploys, or diagnosing Railway failures. Covers Railway GraphQL API (no CLI installed), Jay''s project IDs, and service map. Trigger on: "check Railway", "redeploy", "Railway logs", "env var on Railway", "deployment failed", "Railway is down", "push to Railway".'
---

# Railway Ops

Railway uses a **GraphQL API** at `https://backboard.railway.app/graphql/v2`.
Token stored at `/root/.secrets/railway_token`.
Jay's project ID: `00830a2f-e287-427c-bc10-910dfe2485e8`

## Auth Pattern

```python
import json, urllib.request

TOKEN = open("/root/.secrets/railway_token").read().strip()
PROJECT_ID = "00830a2f-e287-427c-bc10-910dfe2485e8"

def gql(query, variables=None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        "https://backboard.railway.app/graphql/v2",
        data=body,
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    )
    return json.loads(urllib.request.urlopen(req, timeout=15).read())
```

## Common Operations

### List all services in Jay's project
```python
result = gql("""
query {
  project(id: "%s") {
    services { edges { node { id name } } }
  }
}
""" % PROJECT_ID)
for edge in result["data"]["project"]["services"]["edges"]:
    print(edge["node"]["id"], edge["node"]["name"])
```

### Get latest deployment status for a service
```python
result = gql("""
query($serviceId: String!) {
  deployments(input: { serviceId: $serviceId }, first: 1) {
    edges { node { id status createdAt url } }
  }
}
""", {"serviceId": SERVICE_ID})
```
Status values: `SUCCESS`, `FAILED`, `CRASHED`, `BUILDING`, `DEPLOYING`, `REMOVED`

### Trigger a redeploy
```python
result = gql("""
mutation($deploymentId: String!) {
  deploymentRedeploy(id: $deploymentId) { id status }
}
""", {"deploymentId": DEPLOYMENT_ID})
```

### Read environment variables
```python
result = gql("""
query($serviceId: String!, $environmentId: String!) {
  variables(serviceId: $serviceId, environmentId: $environmentId)
}
""", {"serviceId": SERVICE_ID, "environmentId": ENV_ID})
```

### Set an environment variable
```python
result = gql("""
mutation($input: VariableCollectionUpsertInput!) {
  variableCollectionUpsert(input: $input)
}
""", {"input": {
    "projectId": PROJECT_ID,
    "environmentId": ENV_ID,
    "serviceId": SERVICE_ID,
    "variables": {"KEY_NAME": "value"}
}})
```

### Get deployment logs
Logs are streamed — use the Railway dashboard UI for real-time logs.
For recent log lines via API, use the `deploymentLogs` query (requires deployment ID):
```python
result = gql("""
query($deploymentId: String!) {
  deploymentLogs(deploymentId: $deploymentId) { message timestamp }
}
""", {"deploymentId": DEPLOYMENT_ID})
```

## Service Map
See `references/services.md` for all service IDs, URLs, and environment IDs.

## Workflow: Debug a Failed Deploy
1. List services → find service ID for the broken app
2. Get latest deployment → check status + deployment ID
3. If `FAILED` or `CRASHED`: fetch logs → read error
4. Fix code → push to GitHub → Railway auto-deploys (or trigger redeploy mutation)
5. Poll deployment status until `SUCCESS`

## Workflow: Update an Env Var
1. Get service ID + environment ID from `references/services.md`
2. Use `variableCollectionUpsert` mutation
3. Trigger redeploy so the new var takes effect
