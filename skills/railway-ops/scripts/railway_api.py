#!/usr/bin/env python3
"""
railway_api.py — Reusable Railway GraphQL helper for Echo/KiloClaw

Usage:
  from railway_api import gql, PROJECT_ID, get_services, get_deployments, redeploy, set_env_var

Or run directly:
  python3 railway_api.py services
  python3 railway_api.py deploys <service_id>
  python3 railway_api.py redeploy <deployment_id>
  python3 railway_api.py set-var <service_id> <env_id> KEY=value
"""
import json, sys, urllib.request
from pathlib import Path

TOKEN_PATH = Path.home() / ".secrets" / "railway_token"
TOKEN = TOKEN_PATH.read_text().strip() if TOKEN_PATH.exists() else ""
PROJECT_ID = "00830a2f-e287-427c-bc10-910dfe2485e8"
API = "https://backboard.railway.app/graphql/v2"


def gql(query: str, variables: dict = None) -> dict:
    """Use curl subprocess — urllib has intermittent 403s against Railway API."""
    if not TOKEN:
        raise RuntimeError("No railway_token at ~/.secrets/railway_token")
    import subprocess
    payload = json.dumps({"query": query, "variables": variables or {}})
    result = subprocess.run(
        ["curl", "-s", "-X", "POST", API,
         "-H", f"Authorization: Bearer {TOKEN}",
         "-H", "Content-Type: application/json",
         "-d", payload],
        capture_output=True, text=True, timeout=20
    )
    data = json.loads(result.stdout)
    if "errors" in data:
        raise RuntimeError(f"Railway API error: {data['errors']}")
    return data["data"]


def get_services():
    data = gql(f"""query {{
      project(id: "{PROJECT_ID}") {{
        name
        environments {{ edges {{ node {{ id name }} }} }}
        services {{ edges {{ node {{ id name }} }} }}
      }}
    }}""")
    return data["project"]


def get_deployments(service_id: str, limit: int = 5):
    data = gql("""
    query($sid: String!, $limit: Int!) {
      deployments(input: { serviceId: $sid }, first: $limit) {
        edges { node { id status createdAt url } }
      }
    }""", {"sid": service_id, "limit": limit})
    return [e["node"] for e in data["deployments"]["edges"]]


def redeploy(deployment_id: str):
    data = gql("""
    mutation($id: String!) {
      deploymentRedeploy(id: $id) { id status }
    }""", {"id": deployment_id})
    return data["deploymentRedeploy"]


def set_env_var(service_id: str, environment_id: str, key: str, value: str):
    data = gql("""
    mutation($input: VariableCollectionUpsertInput!) {
      variableCollectionUpsert(input: $input)
    }""", {"input": {
        "projectId": PROJECT_ID,
        "environmentId": environment_id,
        "serviceId": service_id,
        "variables": {key: value}
    }})
    return data


def get_env_vars(service_id: str, environment_id: str):
    data = gql("""
    query($sid: String!, $eid: String!) {
      variables(serviceId: $sid, environmentId: $eid)
    }""", {"sid": service_id, "eid": environment_id})
    return data["variables"]


# ── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "services"

    if cmd == "services":
        proj = get_services()
        print(f"Project: {proj['name']}")
        print("\nEnvironments:")
        for e in proj["environments"]["edges"]:
            print(f"  {e['node']['id']}  {e['node']['name']}")
        print("\nServices:")
        for s in proj["services"]["edges"]:
            print(f"  {s['node']['id']}  {s['node']['name']}")

    elif cmd == "deploys" and len(sys.argv) > 2:
        deploys = get_deployments(sys.argv[2])
        for d in deploys:
            print(f"  {d['id']}  {d['status']}  {d['createdAt']}")

    elif cmd == "redeploy" and len(sys.argv) > 2:
        result = redeploy(sys.argv[2])
        print(f"Redeployed: {result}")

    elif cmd == "set-var" and len(sys.argv) > 4:
        # python3 railway_api.py set-var <service_id> <env_id> KEY=value
        key, value = sys.argv[4].split("=", 1)
        set_env_var(sys.argv[2], sys.argv[3], key, value)
        print(f"Set {key} on service {sys.argv[2]}")

    else:
        print(__doc__)
