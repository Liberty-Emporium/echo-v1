# Skills
## Echo-v1 Operator Skill Set

**Last Updated:** 2026-05-04
**Version:** 2.0 (absorbed Agent-Z capabilities)

---

## Core Skills (Built-in)

### 1. deploy-watcher
Monitors Railway deployments, detects failures, triggers alerts.
- Trigger: "watch deploy", "monitor", "deployment status"
- Type: Monitoring
- Source: echo-v1/core

### 2. logging
Centralized logging for all Liberty-Emporium operations.
- Trigger: "log this", "check logs", "logging"
- Type: Context Management
- Source: echo-v1/core

### 3. agent-sync
Keeps all agents synchronized with the latest context.
- Trigger: "sync agents", "agent update", "sync status"
- Type: Coordination
- Source: echo-v1/core

### 4. ecdash-client
Interacts with EcDash control plane API.
- Trigger: "call EcDash", "control plane", "ecdash"
- Type: Integration
- Source: echo-v1/core

---

## Custom Skills (Absorbed from Agent-Z)

### 5. deploy-rescue ⭐ NEW
Diagnoses and fixes Railway deployment failures.
- Trigger: "Railway is down", "App crashed on deploy", "Fix deployment", "Deploy rescue"
- Type: Diagnostic & Recovery
- Source: Agent-Z/skills/custom/deploy-rescue
- Location: `skills/custom/deploy-rescue/skill.md`

### 6. security-audit ⭐ NEW
Scans for security vulnerabilities in Flask apps.
- Trigger: "Check security", "Security sweep", "Is this safe?", "Audit this code"
- Type: Security
- Source: Agent-Z/skills/custom/security-audit
- Location: `skills/custom/security-audit/skill.md`

### 7. db-migrate ⭐ NEW
Safe SQLite schema migrations for production.
- Trigger: "Add column to table", "Database migration needed", "Fix missing column", "Schema change"
- Type: Database
- Source: Agent-Z/skills/custom/db-migrate
- Location: `skills/custom/db-migrate/skill.md`

### 8. rollback-ready ⭐ NEW
Fast emergency rollback procedures.
- Trigger: "Undo last push", "Rollback to working version", "Site is broken", "Revert now", "Emergency rollback"
- Type: Recovery
- Source: Agent-Z/skills/custom/rollback-ready
- Location: `skills/custom/rollback-ready/skill.md`

### 9. template-debug ⭐ NEW
Fixes Jinja2/HTML/CSS template issues.
- Trigger: "Page looks wrong", "CSS broken", "Nav bar error", "Template issue", "Jinja2 error"
- Type: Debugging
- Source: Agent-Z/skills/custom/template-debug
- Location: `skills/custom/template-debug/skill.md`

---

## Skill Usage Guide

When a user describes a problem:
1. Match trigger phrases to skill
2. Load skill file from appropriate location
3. Follow the step-by-step guide
4. Use related skills for complex issues

Example flow:
- User: "App crashed on deploy, help!"
- Match: `deploy-rescue` skill
- Load from: `skills/custom/deploy-rescue/skill.md`
- Follow steps to diagnose → fix → verify

---

*Skills v2.0 — Enhanced by Echo (KiloClaw) on 2026-05-04*
*Absorbed Agent-Z capabilities into echo-v1*