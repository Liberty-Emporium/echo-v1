# Dashboard Enhancement Plan v1.0
# Self — 2026-05-29
# For Jay's EcDash at alexanderai.site

## Vision
Transform the Echo Tasks section into a comprehensive command center that shows:
- Real-time agent activity
- Project health at a glance
- How everything connects
- Revenue pipeline

## Proposed Dashboard Sections

### 1. 🧠 Agent Activity Monitor (LIVE)
Show what each agent is doing RIGHT NOW:
- Self: last action, current task, status
- OWL: last action, current task, status
- Uptime: system health, response times
Update: every 2 minutes via cron

### 2. 📊 Project Health Grid
All Liberty Emporium apps at a glance:
```
| App | Status | Last Check | Response | Issues |
|-----|--------|------------|----------|--------|
| FloodClaims Pro | ✅ UP | 2min ago | 387ms | 0 |
| Contractor Pro | ❌ DOWN | 1min ago | TIMEOUT | TBD |
```
Color-coded: green/yellow/red
Clickable: drill into details per app

### 3. 🔗 Project Connection Graph (Obsidian-style)
Show how apps and services connect:
- FloodClaims Pro → uses → Willie API → connects to → AI Agent Widget
- EcDash → panels for → All Apps
- Sweet Spot Cakes → uses → SendGrid/Twilio → for notifications
- Liberty Oil → external hosting → separate monitoring

This is the Obsidian graph Jay wants. Implementation:
- Store connections in a graph.json file
- Use D3.js or Vis.js to render interactive graph
- Nodes = apps/services, Edges = API connections
- Click a node to see details

### 4. 📋 Task Pipeline (Kanban-style)
```
TODO | IN PROGRESS | BLOCKED | DONE
-----|------------|---------|-----
P0-4 fixes | Contractor Pro | GitHub secrets | Bubble fix
Security audit | OWL working | GitLab PAT | KYS deletion
IT Courses plan | | |
```
Updates from COORDINATION.md every 4 hours

### 5. 💰 Revenue Pipeline (NEW)
Track monetization opportunities:
```
| Opportunity | Status | Revenue Potential | Priority |
|-------------|--------|-------------------|----------|
| AI Agent Widget SaaS | Live | $500-2000/mo | HIGH |
| Contractor Pro services | Down | $1000+/mo | CRITICAL |
| IT Courses | Planned | $200-500/course | MEDIUM |
| Aquila custom agents | Pipeline | $5000+/project | HIGH |
```
Update: weekly review by both agents

### 6. 📈 System Performance (NEW)
- Repo size over time
- Message bus volume
- Cron job success/failure rates
- Average response times per app

### 7. 🔔 Alert Feed (NEW)
Live feed of uptime alerts:
```
[05:02] ⚠️ Contractor Pro DOWN (timeout)
[04:44] ✅ Liberty Oil UP (new URL working)
[03:55] ⚠️ KYS DOWN (identified as intentional deletion)
```

## Implementation Priority
1. Project Health Grid — easiest, most valuable
2. Agent Activity Monitor — builds on existing monitor
3. Task Pipeline — pull from COORDINATION.md
4. Alert Feed — format existing uptime alerts
5. Revenue Pipeline — needs Jay input
6. Project Connection Graph — most complex, D3.js
7. System Performance — long-term tracking

## Technical Approach
- Data source: COORDINATION.md, monitor_state.json, message bus
- Update mechanism: cron job pushes to EcDash API every 4 hours
- Frontend: enhance existing EcDash with new panels
- Graph: D3.js force-directed graph for project connections

## Obsidian Graph Integration
Jay wants to see project connections like Obsidian's graph view.
Proposal:
- Create a graph.json in the brain repo with nodes and edges
- Obsidian can read this as a plugin or we render it in EcDash
- Nodes: each app, each API, each service
- Edges: "uses", "connects to", "depends on", "monitors"
- Auto-updated when new apps/integrations are added

Example graph.json structure:
{
  "nodes": [
    {"id": "floodclaims", "label": "FloodClaims Pro", "group": "app", "status": "up"},
    {"id": "willie-api", "label": "Willie API", "group": "api", "status": "active"},
    {"id": "ecdash", "label": "EcDash", "group": "dashboard", "status": "up"},
    {"id": "sweetspot", "label": "Sweet Spot Cakes", "group": "app", "status": "up"},
    {"id": "sendgrid", "label": "SendGrid", "group": "service", "status": "active"},
    {"id": "railway", "label": "Railway", "group": "hosting", "status": "active"},
    {"id": "contractor", "label": "Contractor Pro", "group": "app", "status": "down"}
  ],
  "edges": [
    {"source": "floodclaims", "target": "willie-api", "label": "uses"},
    {"source": "ecdash", "target": "floodclaims", "label": "monitors"},
    {"source": "sweetspot", "target": "sendgrid", "label": "uses"},
    {"source": "floodclaims", "target": "railway", "label": "hosted on"},
    {"source": "contractor", "target": "railway", "label": "hosted on"}
  ]
}
