# Liberty Emporium — API Map
_Last updated: 2026-05-21_

A complete map of all API routes across every app. Use this to know what's available, avoid duplicating work, and wire apps together.

---

## 🏛️ EcDash (Alexander AI Dashboard)
**URL:** `https://jay-portfolio-production.up.railway.app`
**Repo:** `alexander-ai-dashboard` (branch: master)
**97 total routes**

### API Endpoints (`/api/...`)
| Endpoint | Purpose |
|----------|---------|
| `GET /api/health` | Health check |
| `GET /api/status` | System status |
| `POST /api/chat` | Chat with AI |
| `GET/POST /api/notes` | Jay's notes |
| `GET/POST /api/notes/echo` | Notes for Echo |
| `GET /api/notes/echo-read` | Echo reads notes |
| `POST /api/notes/<id>/pin` | Pin a note |
| `GET/POST /api/todos` | Todo list |
| `GET/POST/DELETE /api/todos/<id>` | Single todo |
| `GET/POST /api/tickets` | Support tickets |
| `GET/POST /api/echo-bridge` | Task queue for Echo |
| `DELETE /api/echo-bridge/<id>` | Complete a task |
| `GET/POST /api/vault` | Credentials vault |
| `GET/POST /api/vault/app-keys` | App API keys |
| `GET/POST /api/vault/app-tokens` | App tokens |
| `GET /api/vault/categories` | Vault categories |
| `GET /api/vault/echo` | Echo's vault view |
| `POST /api/monitor/status` | App status report |
| `POST /api/monitor/event` | Log an event |
| `POST /api/monitor/error` | Log an error |
| `POST /api/monitor/slow` | Log slow request |
| `POST /api/monitor/health` | Health ping |
| `GET /api/monitor/resolve/<id>` | Resolve error |
| `GET /api/conversations` | Chat history |
| `GET /api/conversations/<id>/messages` | Messages in conv |
| `POST /api/echo-proxy/run` | Run Echo remotely |
| `GET /api/echo-proxy/clients` | Connected clients |
| `GET /api/clients` | Client list |
| `GET/POST /api/sweet-spot-users` | Sweet Spot users |
| `GET /api/network-scan` | Tailscale network scan |
| `POST /api/brain/sync` | Sync brain files |
| `GET /api/settings` | Dashboard settings |
| `POST /api/token` | Auth token |
| `GET /api/openrouter-models` | *(via agent-widget)* |

---

## 🛒 Emporium & Thrift App
**URL:** `https://liberty-emporium-thrift.alexanderai.site`
**Repo:** `Emporium-and-Thrift-App` (branch: main)
**Auth:** `X-API-Key: <key>` header

### API Endpoints (added 2026-05-21)
| Endpoint | Auth | Purpose |
|----------|------|---------|
| `GET /api/health` | None | Public health + item counts |
| `GET /api/inventory` | ✅ | All items (filter: ?status= ?category=) |
| `GET /api/inventory/<sku>` | ✅ | Single item by SKU |
| `PATCH /api/inventory/<sku>` | ✅ | Update fields (Title, Price, Status, etc.) |
| `GET /api/stats` | ✅ | Totals + by category/status |
| `POST /api/mark-sold/<sku>` | ✅ | Mark item sold |
| `GET /api/slow-movers` | ✅ | Items available 30+ days |

---

## 🎂 Sweet Spot Cakes
**URL:** `https://sweet-spot-cakes.up.railway.app`
**Repo:** `sweet-spot-cakes` (branch: main)
**126 total routes**

### API Endpoints
| Endpoint | Purpose |
|----------|---------|
| `GET /health` | Health check |
| `GET /api/customers/search` | Search customers |
| `GET/POST /api/ingredients` | Ingredient list |
| `GET/POST /api/recipes` | Recipes |
| `GET/POST /api/tools` | Kitchen tools |
| `GET /cakely/api/dashboard` | AI agent dashboard data |
| `GET /cakely/api/orders` | Orders |
| `POST /cakely/api/orders/add` | Add order |
| `GET /cakely/api/orders/today` | Today's orders |
| `POST /cakely/api/orders/update-status` | Update order status |
| `GET /cakely/api/customers` | Customer list |
| `POST /cakely/api/customers/add` | Add customer |
| `GET /cakely/api/inventory` | Inventory |
| `POST /cakely/api/inventory/add` | Add inventory |
| `GET /cakely/api/inventory/low` | Low stock alerts |
| `POST /cakely/api/inventory/update` | Update inventory |
| `GET /cakely/api/employees` | Employee list |
| `GET /cakely/api/memory` | AI memory |
| `GET /cakely/api/recipes` | Recipes for AI |
| `GET /cakely/api/suppliers` | Suppliers |

---

## 🌊 FloodClaim Pro
**URL:** `https://billy-floods.up.railway.app`
**Repo:** `alexander-ai-floodclaim` (branch: main)
**102 total routes**

### Key API Endpoints
| Endpoint | Purpose |
|----------|---------|
| `GET /health` | Health check |
| `GET /api/status` | App status |
| `POST /api/analyze-photo` | AI photo analysis |
| `GET /willie/api/dashboard` | Willie AI dashboard |
| `GET /willie/api/claims` | All claims |
| `GET /willie/api/claims/<id>` | Single claim |
| `POST /willie/api/claims/<id>/analyze` | AI claim analysis |
| `POST /willie/api/claims/<id>/estimate` | AI cost estimate |
| `POST /willie/api/claims/<id>/compliance` | Compliance check |
| `POST /willie/api/claims/<id>/report` | Generate report |
| `GET /willie/api/claims/<id>/rooms` | Rooms in claim |
| `POST /willie/api/claims/<id>/notify` | Send notification |
| `GET /willie/api/team` | Team members |
| `GET /willie/api/schedule` | Schedule |
| `GET /willie/api/settings` | Settings |
| `GET /willie/token` | Auth token |
| `GET /willie/chat` | Chat interface |

---

## 🤖 AI Agent Widget
**URL:** `https://ai-agent-widget-production.up.railway.app`
**Repo:** `alexander-ai-agent-widget` (branch: main)
**66 total routes**

### Key API Endpoints
| Endpoint | Purpose |
|----------|---------|
| `GET /health` | Health check |
| `GET /api/status` | App status |
| `GET /api/openrouter-models` | Live model list |
| `GET /api/network-status` | Network check |
| `POST /api/analyze-photo-public` | Public photo analysis |
| `GET /api/echo-brain-id` | Echo's brain agent ID |
| `GET /agent/<id>/brain/api` | Agent brain (API) |
| `GET /agent/<id>/actions/api` | Agent actions (API) |
| `GET /api/agent/<id>/reports/generate` | Generate report |
| `GET /api/agent/<id>/reports/history` | Report history |

---

## 🔧 Contractor Pro AI
**Repo:** `alexander-ai-contractor`
**50 total routes**

### Key API Endpoints
| Endpoint | Purpose |
|----------|---------|
| `GET /health` | Health check |
| `GET /healthz` | K8s health |
| `GET /api/stats` | App stats |
| `GET /api/bids` | Bid list |
| `POST /api/create-bid` | Create bid |
| `GET /api/bids/<id>` | Single bid |
| `POST /api/ceo/analyze` | CEO AI analysis |
| `POST /api/ask-advisor` | AI advisor |
| `GET /api/locations` | Locations |
| `GET /api/token/ui` | UI token |
| `GET /admin/api-generator` | API key management |

---

## 🐾 Pet Vet AI
**Repo:** `alexander-ai-petvet`
**47 total routes**

### Key API Endpoints
| Endpoint | Purpose |
|----------|---------|
| `GET /health` | Health check |
| `GET /api/status` | App status |
| `GET /api/stats` | User/diagnosis counts |
| `POST /api/diagnose` | AI pet diagnosis |
| `POST /api/analyze-damage` | Analyze photo |
| `GET /api/pets` | Pet list |
| `GET /api/settings` | App settings |
| `GET /api/token/ui` | UI token |
| `GET /admin/api-generator` | API key management |

---

## Notes
- Most apps have `/health` (public) and `/api/status`
- FloodClaim has the most complete Willie AI agent API (`/willie/api/...`)
- Sweet Spot has the most complete business management API (`/cakely/api/...`)
- EcDash is the central hub — monitor events, echo-bridge, vault, notes all live there
- Agent Widget has `/api/openrouter-models` — can be used by other apps instead of each calling OpenRouter directly
