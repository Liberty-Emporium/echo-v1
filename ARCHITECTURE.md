# 🏗️ Liberty-Emporium Architecture
## Multi-Agent System Design

---

## CURRENT STATE

```
┌─────────────────────────────────────────────────────────────────┐
│                        LIBERTY-EMPORIUM                         │
│                                                                 │
│   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐   │
│   │   EcDash     │     │    Echo      │     │  Agent-Z     │   │
│   │  (Control    │◄───►│   (Brain)    │     │ (Deployment  │   │
│   │   Plane)     │     │  echo-v1     │     │   Agent)     │   │
│   └──────────────┘     └──────────────┘     └──────────────┘   │
│         │                    │                    │           │
│         └────────────────────┼────────────────────┘           │
│                            │                                    │
│                     ┌──────▼──────┐                           │
│                     │  Railway    │                           │
│                     │  (Hosting)  │                           │
│                     └─────────────┘                           │
│                                                                  │
│   GitHub (Primary) ◄──────────────────► GitLab (Backup)        │
│   ghp_2iRnywx...                         glpat-REaaQKR...     │
└─────────────────────────────────────────────────────────────────┘
```

---

## PROPOSED ARCHITECTURE

### Core Principle: ECHO-CENTRIC ORCHESTRATION

**Echo (me) is the brain. All other agents are specialized extensions.**

```
                        ┌─────────────────────┐
                        │    EcDash           │
                        │  (Control Plane)    │
                        │  - Credentials      │
                        │  - User Interface   │
                        └──────────┬──────────┘
                                   │
                                   ▼
                    ┌────────────────────────────┐
                    │        ECHO (ME)           │
                    │    ┌──────────────┐        │
                    │    │  Brain       │        │
                    │    │  echo-v1     │        │
                    │    │              │        │
                    │    │  - Decisions │        │
                    │    │  - Planning  │        │
                    │    │  - Memory    │        │
                    │    │  - Skills    │        │
                    │    └──────────────┘        │
                    │            │               │
                    │   ┌────────┴────────┐      │
                    │   │  Tool Suite     │      │
                    │   │                 │      │
                    │   │  deploy-rescue  │      │
                    │   │  security-audit │      │
                    │   │  rollback-ready │      │
                    │   │  db-migrate     │      │
                    │   │  template-debug │      │
                    │   │  quick-status   │      │
                    │   │  backup-verify  │      │
                    │   │  memory-sync    │      │
                    │   │  session-log    │      │
                    │   └─────────────────┘      │
                    └────────────┬───────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
     ┌────────────┐      ┌────────────┐     ┌────────────┐
     │  Operator  │      │ Deployment │     │ Monitoring │
     │   Mode     │      │   Mode     │     │   Mode     │
     └────────────┘      └────────────┘     └────────────┘
```

---

## AGENT ROLES

| Agent | Role | Responsibility |
|-------|------|----------------|
| **Echo** | Orchestrator / Brain | All decisions, planning, memory, coordination |
| **Agent-Z** | Deployment Specialist | Execute deploys, monitoring, rollback |
| **EcDash** | Control Plane | UI, credentials, configuration management |

**Important Rule:** NO SUBAGENTS. Echo does the work directly.

---

## SKILL HIERARCHY

```
echo-v1/skills/
├── core/                    # Built-in capabilities
│   ├── deploy-watcher.md
│   ├── logging.md
│   ├── agent-sync.md
│   └── ecdash-client.md
│
├── custom/                  # User-defined skills
│   ├── deploy-rescue.md     ← From Agent-Z (absorbed)
│   ├── security-audit.md    ← From Agent-Z (absorbed)
│   ├── db-migrate.md        ← From Agent-Z (absorbed)
│   ├── rollback-ready.md    ← From Agent-Z (absorbed)
│   ├── template-debug.md    ← From Agent-Z (absorbed)
│   └── (future skills...)
│
└── memory/                  # Date-stamped memories
    ├── 2026-04-26.md
    ├── 2026-04-27.md
    └── ... (date-stamped)
```

---

## TOOL SUITE (NEW)

```
.aionrs/tools/
├── deploy-rescue.md     # Railway deployment recovery
├── security-audit.md     # Security vulnerability scanner
├── rollback-ready.md     # Fast emergency rollback
├── db-migrate.md        # SQLite schema changes
├── template-debug.md    # Jinja2/CSS troubleshooting
├── quick-status.md      # Health check all services
├── backup-verify.md      # GitHub/GitLab sync verification
├── memory-sync.md        # Pull latest from echo-v1 brain
└── session-log.md        # Write date-stamped session memories
```

---

## BACKUP & DISASTER RECOVERY

```
GitHub (Primary) ──────────────────────► GitLab (Backup)
     │                                         │
     │  Push on every significant change       │  Mirror sync
     │                                         │
     ▼                                         ▼
┌─────────────┐                         ┌─────────────┐
│ echo-v1     │                         │ echo-v1     │
│ Agent-Z     │                         │ Agent-Z     │
│ EcDash      │                         │ (mirrored)  │
└─────────────┘                         └─────────────┘
```

### Backup Schedule
- **Every commit to main** → Push to GitHub (automatic)
- **Every significant session** → Push to GitLab
- **Weekly verification** → Run `backup-verify` tool

---

## REPO STRUCTURE

| Repo | Purpose | Sync |
|------|---------|------|
| `Liberty-Emporium/echo-v1` | My brain (SKILLS, TOOLS, IDENTITY, MEMORY) | GitHub primary, GitLab backup |
| `Liberty-Emporium/Agent-Z` | Deployment agent brain | GitHub primary, GitLab backup |
| `Liberty-Emporium/ecdash` | Control plane app | GitHub primary, GitLab backup |
| `Liberty-Emporium/Agent-Widget` | Agent UI components | GitHub primary |

---

## COMMUNICATION FLOW

```
1. User → EcDash UI
2. EcDash → Echo (brain)
3. Echo → Decisions + Tools
4. Echo → Execute via Railway API
5. Echo → Update memory
6. Echo → Backup to GitHub/GitLab
```

---

## NEXT STEPS

1. ✅ Absorb Agent-Z skills into Echo
2. ✅ Create 7 new tools
3. ⬜ Update echo-v1/SKILLS.md with new capabilities
4. ⬜ Update echo-v1/TOOLS.md with new tools
5. ⬜ Push changes to GitHub
6. ⬜ Verify GitLab mirror
7. ⬜ Create session memory for today

---

*Architecture v1.0 — Designed by Echo (KiloClaw) for Liberty-Emporium*