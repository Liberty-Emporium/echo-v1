---
name: pureclaw-connect
description: >
  Use this skill whenever the user wants to connect, integrate, or authorize
  any third-party app or service. Triggers include: "connect my Gmail", "read
  my emails", "send a Slack message", "connect Slack", "link my Notion",
  "connect Google Sheets", "what apps do I have connected", "authorize X",
  "set up X integration", "use my X account", or any request that involves
  accessing an external app on behalf of the user. Handles OAuth flows,
  connected account discovery, running actions (send message, read emails,
  create rows, etc.), and raw API proxying — all via backend-managed
  credentials. Covers 3,000+ apps including Gmail, Slack, Notion, Google
  Sheets, GitHub, HubSpot, and more.
---

# PureClaw Connect

Use this skill for the PureClaw Pipedream integration.

## Current integration summary

PureClaw uses this model:

- **Backend holds all Pipedream credentials** — `client_id`, `client_secret`, `project_id` never touch the agent
- **Gateway token auth** — the agent authenticates with its server's `gateway_token`, backend resolves `server_id`
- **Per-server isolation** — each server gets its own Pipedream `external_user_id` (= `server_id`), so connected accounts are fully isolated across servers
- **Connected accounts are discovered live** from the Pipedream Connect accounts API via `GET /api/connectors/accounts`
- **Browse All Apps loads the full dynamic catalog** via `GET /api/connectors/apps`
- **Actions and proxy calls** route through the backend, which injects OAuth credentials server-side

## Key design decisions

### 1) Per-server connection model

Each PureClaw server gets its own Pipedream identity via `external_user_id = str(server_id)`.

This means:

- a user with 3 servers has 3 completely independent sets of connected accounts
- connecting Gmail on Server A does NOT affect Server B
- the mapping is: `gateway_token → clawd_servers.id → Pipedream external_user_id`

Auth resolution path:

```text
Authorization: Bearer <gateway_token>
  → ClawdServerDAO.get_by_gateway_token(token)
  → server.id (UUID)
  → str(server_id) passed as external_user_id to all Pipedream SDK calls
```

### 2) No secrets on the agent

The agent never sees or stores:

- Pipedream `client_id` or `client_secret`
- Pipedream `project_id`
- OAuth access tokens for connected apps

All of these live on the backend. The agent only knows `BACKEND_URL` and `GATEWAY_TOKEN`.

### 3) Live connected-account discovery

Agent calls the backend, which queries Pipedream live. Do not assume local config is the source of truth for connected apps if live API access is available.

### 4) Full app catalog is dynamic

The app catalog uses the live Pipedream catalog, not a static baked-in list. `GET /api/connectors/apps?q=...` queries Pipedream in real time.

## Connection credentials

**BACKEND_URL** is fixed:

```text
BACKEND_URL = https://be.paioclaw.ai
```

**GATEWAY_TOKEN** must be read from `~/.openclaw/openclaw.json` at startup:

```bash
GATEWAY_TOKEN=$(python3 -c "import json; print(json.load(open('$HOME/.openclaw/openclaw.json'))['gateway']['auth']['token'])")
```

The config file is at `~/.openclaw/openclaw.json` and the token is at `gateway.auth.token`:

```json
{
  "gateway": {
    "mode": "local",
    "auth": {
      "mode": "token",
      "token": "<this is the GATEWAY_TOKEN>"
    }
  }
}
```

All API calls follow this pattern:

```bash
curl -s -H "Authorization: Bearer $GATEWAY_TOKEN" \
  "https://be.paioclaw.ai/api/connectors/..."
```

If `~/.openclaw/openclaw.json` does not exist or `gateway.auth.token` is missing, tell the user: "PureClaw server config not found. Make sure your server is provisioned and `~/.openclaw/openclaw.json` exists."

## Architecture

```text
PureClaw Server (agent)
  has: gateway_token, backend_url
  calls: /api/connectors/* endpoints
      │
      ▼
PureClaw Backend
  has: PIPEDREAM_CLIENT_ID, PIPEDREAM_CLIENT_SECRET,
       PIPEDREAM_PROJECT_ID, PIPEDREAM_PROJECT_ENVIRONMENT
  resolves: gateway_token → server_id
  calls: Pipedream SDK with external_user_id = str(server_id)
      │
      ▼
Pipedream Connect
  has: OAuth tokens per external_user_id per app
  exposes: accounts, actions, proxy, catalog
```

## Setup workflow

### 1) Configure backend Pipedream credentials

Set these environment variables on the PureClaw backend:

```text
PIPEDREAM_CLIENT_ID=<from Pipedream project settings>
PIPEDREAM_CLIENT_SECRET=<from Pipedream project settings>
PIPEDREAM_PROJECT_ID=proj_xxxxxxx
PIPEDREAM_PROJECT_ENVIRONMENT=production
```

Prefer `production` unless explicitly testing in development.

### 2) Provision a PureClaw server

The server gets a `gateway_token` during provisioning. This token is stored in the `clawd_servers` table and is available to the agent.

### 3) Connect apps for the server

The agent calls the backend to generate OAuth links. The user clicks the link, authorizes the app in their browser, and the connection is established.

### 4) Use the tools normally

After connection, the agent can run actions and proxy API calls for any connected app.

## API reference

All endpoints require `Authorization: Bearer <gateway_token>`.

### Status

```bash
GET /api/connectors/status
```

Returns whether Pipedream is configured on the backend. Use this to verify the gateway token is valid at session start.

### Connect token (OAuth link generation)

```bash
POST /api/connectors/token?app={app_slug}
```

Returns `connect_link_url` — present this to the user. They click it, authorize the app in their browser, and the account becomes available.

OAuth links expire after **4 hours**. Generate a fresh one if needed.

### Connected accounts

```bash
GET /api/connectors/accounts
GET /api/connectors/accounts?app={app_slug}
GET /api/connectors/accounts/{account_id}
GET /api/connectors/accounts/{account_id}?include_credentials=true
```

Lists or retrieves connected accounts for this server. The `account_id` (format `apn_xxxxxxx`) is needed for proxy calls and action `configured_props`.

### App catalog

```bash
GET /api/connectors/apps?q={search}&limit={n}
```

Searches the full Pipedream app catalog (3,000+ apps). Supports pagination via `after`/`before` cursors.

### Actions (tools)

```bash
GET /api/connectors/actions?app={app_slug}&q={search}&limit={n}
```

Lists available Pipedream actions for an app. Use this to discover what tools are available before running them.

### Run action

```bash
POST /api/connectors/actions/run
Content-Type: application/json

{
  "action_id": "slack-send-message",
  "configured_props": {
    "slack": {"authProvisionId": "apn_xxxxxxx"},
    "channel": "C03NA8B4VA9",
    "text": "Hello from the agent!"
  }
}
```

Executes a Pipedream action on behalf of this server. The backend resolves the server's OAuth credentials via Pipedream.

### Proxy

```bash
POST /api/connectors/proxy
Content-Type: application/json

{
  "method": "POST",
  "url": "https://slack.com/api/chat.postMessage",
  "account_id": "apn_xxxxxxx",
  "body": {"channel": "C03NA8B4VA9", "text": "Hello via proxy!"}
}
```

Makes a raw authenticated API request. Pipedream injects the OAuth token into the upstream request. Use this when no pre-built action exists.

Supported methods: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`.

## Agent workflow

When a user asks to interact with an external service, follow this sequence:

### Step 1 — Check existing connections

```text
GET /api/connectors/accounts?app={app_slug}
```

If the server has a healthy account for this app, skip to Step 3.

### Step 2 — Connect the app (if not connected)

```text
POST /api/connectors/token?app={app_slug}
```

Present the `connect_link_url` to the user. Wait for them to authorize, then verify with Step 1.

### Step 3 — Discover available tools

```text
GET /api/connectors/actions?app={app_slug}
```

Find the right action for what the user wants to do.

### Step 4 — Execute

Either:

- **Run an action:** `POST /api/connectors/actions/run` with the action ID and configured props
- **Proxy a raw API call:** `POST /api/connectors/proxy` with the URL, method, and account_id

### Step 5 — Report results

Parse the response and present the outcome to the user in natural language.

## Storage and security

### Backend secrets (environment variables)

```text
PIPEDREAM_CLIENT_ID
PIPEDREAM_CLIENT_SECRET
PIPEDREAM_PROJECT_ID
PIPEDREAM_PROJECT_ENVIRONMENT
```

These must never be exposed to agents or frontend clients.

### Agent-side credentials

The agent only has:

```text
BACKEND_URL    — hardcoded to https://be.paioclaw.ai
GATEWAY_TOKEN  — read from ~/.openclaw/openclaw.json → gateway.auth.token
```

No Pipedream secrets, no OAuth tokens, no additional config files.

### Server identity mapping

```text
clawd_servers table:
  gateway_token (String)  →  id (UUID)  =  Pipedream external_user_id
```

## Runtime behaviors to preserve

When editing this integration, preserve these behaviors:

1. **Connected accounts remain per-server isolated** — `external_user_id = str(server_id)`, not `user_id`
2. **Gateway token is the sole agent credential** — no additional tokens, config files, or pairing flows
3. **Live API data beats stale local state** — always query the backend for current connected accounts
4. **App catalog is dynamic** — never use a static baked-in app list
5. **Backend proxies all Pipedream calls** — agent never calls Pipedream directly
6. **OAuth tokens are invisible to the agent** — Pipedream injects them server-side via the proxy

## Debugging guidance

### Connected app missing after authorization

Check in this order:

1. Backend Pipedream credentials configured (`GET /api/connectors/status` returns `pipedream_configured: true`)
2. Correct project and environment (`production` vs `development`)
3. OAuth completed successfully (user clicked the link and authorized)
4. Gateway token resolves to the expected server (`get_by_gateway_token` returns a row)
5. `GET /api/connectors/accounts?app={slug}` returns the account with `healthy: true`

### 401 on any connector endpoint

Check:

1. `~/.openclaw/openclaw.json` exists and `gateway.auth.token` is present
2. Token value matches what's in `clawd_servers.gateway_token` on the backend
3. Server is not deleted (`server_status != DELETE`)
4. Token is being sent as `Authorization: Bearer <token>`

### Action run fails

Check:

1. Connected account exists for the app (`GET /api/connectors/accounts?app={slug}`)
2. `authProvisionId` in `configured_props` matches the actual `account_id` from the accounts list
3. Action ID is correct (`GET /api/connectors/actions?app={slug}` to verify)
4. Required props are provided (check Pipedream action docs for the specific action)

### Proxy returns error

Check:

1. `account_id` is valid and healthy
2. `url` is a valid upstream API endpoint
3. `method` matches what the upstream API expects
4. Request body/params match the upstream API spec
5. Pipedream proxy timeout is 30 seconds — long-running requests will fail

### OAuth link expired

OAuth links expire after 4 hours. Generate a fresh one via `POST /api/connectors/token?app={slug}`.

## Files involved

Check these areas when updating the integration:

- `app/core/device_auth.py` — gateway token resolution (`get_current_server_id`)
- `app/database/DAO/clawd_server_dao.py` — `get_by_gateway_token` query
- `app/api/v1/endpoints/connectors.py` — all connector REST endpoints
- `app/services/connector_service.py` — service layer (server_id → external_user_id mapping)
- `app/services/pipedream/connect_client.py` — Pipedream SDK wrapper (tokens, accounts, actions, proxy)
- `app/schemas/output/connectors.py` — response models
- `app/config.py` — Pipedream environment variables

## Practical rule

If the question is about:

- backend credentials or project setup → check environment variables and `connectors/status`
- app connection or OAuth → `POST /api/connectors/token` flow
- which apps are connected → `GET /api/connectors/accounts` (live query)
- available tools for an app → `GET /api/connectors/actions?app={slug}`
- executing a tool → `POST /api/connectors/actions/run`
- raw API access → `POST /api/connectors/proxy`
- auth failure → trace `gateway_token → clawd_servers → server_id`
- wrong server getting wrong accounts → verify `external_user_id` isolation
