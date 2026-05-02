#!/usr/bin/env python3
"""
Phase 2 Activation Script — Full run
1. Login to EcDash, delete old app tokens, generate fresh ones
2. Use Railway API to set ECDASH_APP_TOKEN + ECDASH_URL on every service
3. Saves tokens to /root/.secrets/app-tokens/
"""
import requests, json, os, sys, time, hashlib, secrets as _sec

ECDASH_URL     = "https://jay-portfolio-production.up.railway.app"
ECDASH_TOKEN   = open('/root/.secrets/ecdash_token').read().strip()
RAILWAY_TOKEN  = open('/root/.secrets/railway_token').read().strip()
DASHBOARD_PW   = "Mhall001!"
SECRETS_DIR    = "/root/.secrets/app-tokens"
RAILWAY_GQL    = "https://backboard.railway.app/graphql/v2"
RW_HEADERS     = {"Authorization": f"Bearer {RAILWAY_TOKEN}", "Content-Type": "application/json"}
os.makedirs(SECRETS_DIR, exist_ok=True)

# ── Railway service map (from API discovery) ─────────────────────────────────
# app_name → {project_id, service_id, env_id}
SERVICES = {}

print("=" * 65)
print("🚀  Phase 2 Activation — Liberty-Emporium App Network")
print("=" * 65)

# ── Step 1: Fetch all environment IDs per project ────────────────────────────
print("\n📡  Fetching Railway service environments...")

# Known project→service mappings from our discovery run
RAW_MAP = [
    ("FloodClaim Pro",       "eb151b42-4433-4da5-9d48-fc1d27c50d57", "c267c526-0489-473a-8add-7431baeafd0f"),
    ("AI Agent Widget",      "b8b1a484-031e-4d67-8652-953c1cf722bc", "91f73b39-c66e-435a-abb3-d7505d3a7b15"),
    ("Sweet Spot Cakes",     "a776da33-228a-4a8b-bede-d1bf4cfe3c77", "484711dc-5f65-4cfd-b299-189b5eb86800"),
    ("Pet Vet AI",           "7fa1de6b-d138-4ef7-9ebb-581f010fb6ad", "188b1389-302d-4e9c-9821-fdbb2b2afee6"),
    ("Contractor Pro AI",    "ec3ac8ba-3120-448a-be16-445f00ed7957", "23ef2d0a-dceb-4f44-ab0d-f0cd3c84f04f"),
    ("Drop Shipping",        "d066213b-4fc9-4663-bc14-0a8bb1f0d981", "79ffa602-0b96-42d3-a4f1-19e3a9d578f6"),
    ("Consignment",          "8546cf9f-6d35-4bf0-b3a3-8910d226fb8b", "665b7716-4ef8-4004-846b-4570c2077d2f"),
    ("Liberty Inventory",    "ac53d15a-8713-4d5e-83eb-46d2fb6082f0", "685c4544-acd3-4506-aaa6-229ee1f7d26c"),
    ("GymForge",             "93886aca-30b0-4429-92ff-1458abc62128", "72fbacd4-7a56-4f8a-bb5b-65af05bf2df4"),
    ("Liberty Oil",          "24d59343-9363-4290-882d-28604f23bb10", "e46f4f35-c5ef-4141-a67a-cb8e9228865e"),
]

# Get production environment ID for each project
def get_prod_env(project_id):
    r = requests.post(RAILWAY_GQL, headers=RW_HEADERS, timeout=10, json={
        "query": f'{{ project(id: "{project_id}") {{ environments {{ edges {{ node {{ id name }} }} }} }} }}'
    })
    envs = r.json()["data"]["project"]["environments"]["edges"]
    for e in envs:
        if e["node"]["name"] == "production":
            return e["node"]["id"]
    return envs[0]["node"]["id"] if envs else None

for app_name, proj_id, svc_id in RAW_MAP:
    env_id = get_prod_env(proj_id)
    SERVICES[app_name] = {"project_id": proj_id, "service_id": svc_id, "env_id": env_id}
    status = "✅" if env_id else "⚠️ "
    print(f"  {status} {app_name:25} env={env_id[:8] if env_id else 'NOT FOUND'}...")

# ── Step 2: Login to EcDash + regenerate app tokens ──────────────────────────
print("\n🔑  Logging into EcDash & regenerating app tokens...")

import re as _re
session = requests.Session()
# GET login page first to grab CSRF token
get_login = session.get(f"{ECDASH_URL}/login", timeout=10)
csrf_match = _re.search(r'name=["\']csrf_token["\'] value=["\']([a-f0-9]+)["\']', get_login.text)
if not csrf_match:
    csrf_match = _re.search(r'csrf_token.*?value=["\']([a-f0-9]+)["\']', get_login.text)
csrf = csrf_match.group(1) if csrf_match else ''
login = session.post(f"{ECDASH_URL}/login",
    data={"password": DASHBOARD_PW, "csrf_token": csrf}, allow_redirects=True, timeout=10)
logged_in = "dashboard" in login.url or (login.status_code == 200 and "logout" in login.text.lower())
print(f"  {'✅' if logged_in else '❌'} Login: {login.status_code} → {login.url}")

app_tokens = {}

if logged_in:
    # Delete all existing app tokens
    existing_r = requests.get(f"{ECDASH_URL}/api/vault/app-tokens",
        headers={"Authorization": f"Bearer {ECDASH_TOKEN}"}, timeout=10)
    existing = existing_r.json() if existing_r.ok else []
    for tok in existing:
        session.delete(f"{ECDASH_URL}/api/vault/app-tokens/{tok['id']}", timeout=10)
    print(f"  🗑️  Cleared {len(existing)} old token(s)")

    # Category map per app
    CATS = {
        "FloodClaim Pro":    "Stripe,App Logins,App URLs",
        "AI Agent Widget":   "Stripe,AI / LLM,App Logins,App URLs",
        "Sweet Spot Cakes":  "Stripe,App URLs",
        "Pet Vet AI":        "Stripe,App URLs",
        "Contractor Pro AI": "Stripe,App URLs",
        "Drop Shipping":     "CJ Dropshipping,Stripe,App URLs",
        "Consignment":       "Stripe,App URLs",
        "Liberty Inventory": "Stripe,App URLs",
        "GymForge":          "Stripe,App Logins,App URLs",
        "Liberty Oil":       "App URLs",
    }

    for app_name in SERVICES:
        cats = CATS.get(app_name, "App URLs")
        r = session.post(f"{ECDASH_URL}/api/vault/app-tokens",
            json={"app_name": app_name, "categories": cats}, timeout=10)
        if r.ok:
            result = r.json()
            raw_token = result.get("token", "")
            if raw_token:
                app_tokens[app_name] = raw_token
                safe = app_name.lower().replace(" ", "_").replace("-", "_")
                with open(f"{SECRETS_DIR}/{safe}.token", "w") as f:
                    f.write(raw_token)
                print(f"  ✅ {app_name}: token generated")
            else:
                print(f"  ❌ {app_name}: no token in response")
        else:
            print(f"  ❌ {app_name}: HTTP {r.status_code} — {r.text[:80]}")
else:
    print("  ❌ Not logged in — cannot generate tokens")
    sys.exit(1)

# ── Step 3: Push env vars to Railway ─────────────────────────────────────────
print(f"\n🚂  Setting Railway env vars ({len(app_tokens)} apps)...")

UPSERT = """
mutation Upsert($input: VariableCollectionUpsertInput!) {
  variableCollectionUpsert(input: $input)
}
"""

results = {"success": [], "failed": []}

for app_name, info in SERVICES.items():
    token = app_tokens.get(app_name)
    if not token:
        print(f"  ⚠️  {app_name}: no token — skip")
        results["failed"].append(app_name)
        continue

    payload = {
        "query": UPSERT,
        "variables": {
            "input": {
                "projectId":     info["project_id"],
                "serviceId":     info["service_id"],
                "environmentId": info["env_id"],
                "variables": {
                    "ECDASH_APP_TOKEN": token,
                    "ECDASH_URL":       ECDASH_URL,
                }
            }
        }
    }

    r = requests.post(RAILWAY_GQL, headers=RW_HEADERS, json=payload, timeout=15)
    d = r.json()
    if "errors" in d:
        err = d["errors"][0].get("message", "unknown")
        print(f"  ❌ {app_name}: {err[:70]}")
        results["failed"].append(app_name)
    else:
        print(f"  ✅ {app_name}: ECDASH_APP_TOKEN + ECDASH_URL set → Railway redeploying")
        results["success"].append(app_name)
    time.sleep(0.25)

# ── Summary ───────────────────────────────────────────────────────────────────
print("\n" + "=" * 65)
print("📊  PHASE 2 SUMMARY")
print("=" * 65)
print(f"✅  Activated ({len(results['success'])}): {', '.join(results['success'])}")
if results["failed"]:
    print(f"❌  Failed  ({len(results['failed'])}): {', '.join(results['failed'])}")
print()

if len(results["success"]) == len(SERVICES):
    print("🎉  ALL APPS ACTIVATED — Phase 2 is fully live!")
    print()
    print("What happens next:")
    print("  • Each Railway service has ECDASH_APP_TOKEN + ECDASH_URL")
    print("  • On next deploy/restart, each app can call:")
    print(f"    POST {ECDASH_URL}/api/vault/app-keys")
    print("    with its token to pull its own secrets at runtime")
    print("  • No more hardcoded API keys in any app")
else:
    print(f"⚠️   {len(results['failed'])} app(s) need manual attention (see above)")
