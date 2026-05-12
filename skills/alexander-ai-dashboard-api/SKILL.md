---
name: alexander-ai-dashboard-api
description: 'Interact with the Alexander AI Support Dashboard API (agents.alexanderai.site). Use when checking connected client machines, adding/updating clients, verifying Liberty Agent status, sending remote commands to customer machines, or reading machine health data. Trigger on: "support dashboard", "check if machine is online", "add a client", "Liberty Agent connected?", "send command to customer", "agents.alexanderai.site".'
---

# Alexander AI Support Dashboard API

**Base URL:** `https://agents.alexanderai.site`
**Login:** `jay` / `Treetop121570!`
**Auth:** JWT — get token from `/api/login`, pass as `Authorization: Bearer <token>`

## Auth Helper

```python
import json, urllib.request

BASE = "https://agents.alexanderai.site"

def get_token():
    data = json.dumps({"username": "jay", "password": "Treetop121570!"}).encode()
    req = urllib.request.Request(f"{BASE}/api/login", data=data,
          headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=15).read())["token"]

def api(path, token, method="GET", body=None):
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(f"{BASE}{path}", data=data,
          headers={"Authorization": f"Bearer {token}",
                   "Content-Type": "application/json"})
    req.get_method = lambda: method
    return json.loads(urllib.request.urlopen(req, timeout=15).read())
```

## Endpoints

### Clients
| Action | Method | Path |
|--------|--------|------|
| List all | GET | `/api/clients` |
| Get one + machines | GET | `/api/clients/:id` |
| Create | POST | `/api/clients` |
| Update | PATCH | `/api/clients/:id` |
| Delete | DELETE | `/api/clients/:id` |

**Create client body:**
```json
{ "name": "Customer Name", "email": "email@example.com", "agent_type": "hermes", "notes": "..." }
```
Returns: `{ "id": "<uuid>", "name": "...", "install_token": "<32-char-hex>" }`

### Machines
| Action | Method | Path |
|--------|--------|------|
| List all | GET | `/api/machines` |
| Get one | GET | `/api/machines/:machine_id` |
| Link to client | POST | `/api/clients/:id/link-machine` |

**Link-machine** (called by Liberty Agent on boot, no auth — uses install token):
```
POST /api/clients/:client_id/link-machine
Header: X-Install-Token: <install_token>
Body: { "machine_id": "<uuid>" }
```

### Commands (remote terminal)
```
POST /api/machines/:machine_id/command   { "cmd": "df -h" }
GET  /api/machines/:machine_id/commands  (history)
```

### Health
```
GET /health   → { "ok": true, "ts": "..." }
```

## Jay's Client Record
| Field | Value |
|-------|-------|
| Client ID | `ac13f2b8-9f94-431a-91b8-6439b4d12ab0` |
| Install Token | `b6e9431bcaed4c468e42256c52bede8e` |
| Email | `alexanderjay70@gmail.com` |
| Agent type | `hermes` |

## Common Tasks

### Check if a machine is online
```python
token = get_token()
machines = api("/api/machines", token)
for m in machines:
    status = "🟢 ONLINE" if m["online"] else "⚫ offline"
    print(f"{status} | {m['hostname']} | {m['machine_id'][:8]}...")
```

### Add a new client + get their install command
```python
token = get_token()
client = api("/api/clients", token, "POST",
    {"name": "John Smith", "email": "john@example.com", "agent_type": "hermes"})
print(f"Client ID: {client['id']}")
print(f"Install token: {client['install_token']}")
# Give customer this one-liner with their credentials baked in:
print(f"LIBERTY_CLIENT_ID={client['id']} LIBERTY_INSTALL_TOKEN={client['install_token']} curl ... | bash")
```

### Send a remote command to a machine
```python
token = get_token()
result = api(f"/api/machines/{MACHINE_ID}/command", token, "POST", {"cmd": "df -h"})
# Result appears in dashboard in real time via Socket.IO
```

## Architecture Notes
- Machines connect via **Socket.IO** to `wss://agents.alexanderai.site` using `?session_id=<machine_id>`
- `machine_info` event sent on connect + every 30s heartbeat — creates/updates machine record in SQLite
- `link-machine` call ties a machine_id to a client_id — must be called with correct CLIENT_ID + INSTALL_TOKEN
- Liberty Agent must be restarted with `LIBERTY_CLIENT_ID` + `LIBERTY_INSTALL_TOKEN` env vars set for linking to work
- DB lives on Railway persistent volume at `/data/alexander.db`
