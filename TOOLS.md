# Tools
## Echo-v1 Operator Tool Suite

**Last Updated:** 2026-05-04
**Version:** 2.0 (8 new tools added)

---

## Tool Suite

### 1. deploy-rescue
**Type:** Diagnostic & Recovery
**File:** `tools/deploy-rescue.md`
**Use when:** Railway deployment fails, app crashes on boot, worker won't start
**Trigger:** "Railway is down", "App crashed on deploy", "Fix deployment", "Deploy rescue"

Diagnoses and fixes Railway deployment issues for Flask/SQLite apps.
- Captures error patterns (NameError, sqlite issues, HaltServer)
- Identifies root cause and applies fix
- Verifies recovery with `railway status` and curl checks

### 2. security-audit
**Type:** Security
**File:** `tools/security-audit.md`
**Use when:** Checking code for vulnerabilities, before deployment, after changes
**Trigger:** "Check security", "Security sweep", "Is this safe?", "Audit this code"

Quick security checks for Flask apps.
- Detects hardcoded secrets (API keys, passwords, tokens)
- Catches SQL injection risks (string formatting in queries)
- Verifies input validation and session security
- Checks admin route protection

### 3. rollback-ready
**Type:** Recovery
**File:** `tools/rollback-ready.md`
**Use when:** Production is broken and you need to revert FAST
**Trigger:** "Undo last push", "Rollback to working version", "Site is broken", "Revert now", "Emergency rollback"

Revert broken deployments in under 60 seconds.
- Tags broken state before reverting
- Supports both `git revert` (safe) and `git reset --hard` (nuclear)
- Uses force-with-lease for safe force-push
- Logs all rollback events for later analysis

### 4. db-migrate
**Type:** Database
**File:** `tools/db-migrate.md`
**Use when:** Need to add columns/tables, schema changes, "no such column" errors
**Trigger:** "Add column to table", "Database migration needed", "Fix missing column", "Schema change"

Safely modify SQLite database schemas in production.
- Idempotent migrations (wrapped in try/except)
- Never drops columns
- Creates indexes after migrations
- Tests on both fresh and legacy DBs

### 5. template-debug
**Type:** Debugging
**File:** `tools/template-debug.md`
**Use when:** Page looks wrong, CSS broken, nav bar error, Jinja2 error
**Trigger:** "Page looks wrong", "CSS broken", "Nav bar error", "Template issue", "Jinja2 error"

Systematically find and fix HTML/CSS/Jinja2 template issues.
- Detects class name spacing issues (nav-itemactive → nav-item active)
- Fixes active state logic errors
- Validates Jinja2 syntax before commit
- Common patterns: missing space in conditionals, wrong path matching

### 6. quick-status
**Type:** Health Check
**File:** `tools/quick-status.md`
**Use when:** Starting session, checking if anything is down, routine check
**Trigger:** "Quick status", "What's down?", "Health check", "Status of services"

Fast health check of all Liberty-Emporium services.
- Checks Railway status for all deployed apps
- Reports green/yellow/red status
- Verifies URL responds correctly
- Logs all service states

### 7. backup-verify
**Type:** Disaster Recovery
**File:** `tools/backup-verify.md`
**Use when:** After significant changes, periodic verification, pre-deployment check
**Trigger:** "Verify backups", "Check backup integrity", "Backup status", "GitLab sync"

Confirm GitLab mirrors are up to date.
- Checks GitHub primary repos for push timestamps
- Verifies GitLab mirror sync status
- Reports out-of-sync repos needing attention
- Uses GLAB_TOKEN env var (not hardcoded)

### 8. memory-sync
**Type:** Context Management
**File:** `tools/memory-sync.md`
**Use when:** Starting session, need current project state, resuming work
**Trigger:** "Sync memory", "What's latest?", "Update context", "Pull latest"

Pull latest context from echo-v1 brain.
- Downloads date-stamped memory files from GitHub
- Gets current SKILLS.md and TOOLS.md
- Merges with local session memory
- Identifies new projects or changes

### 9. session-log
**Type:** Memory
**File:** `tools/session-log.md`
**Use when:** End of session, significant changes made, new information learned
**Trigger:** "Log this", "Remember this", "Save session", "Document what happened"

Write date-stamped memory files documenting accomplishments.
- Documents new tools created, skills absorbed
- Records architecture decisions
- Notes bugs found/fixed and new repos discovered
- Saves to `.aionrs/memory/YYYY-MM-DD.md` for permanent storage

---

## Tool Directory Structure

```
tools/
├── app_status_endpoint.py      # Original - EcDash integration
├── backup-verify.md             # NEW - Backup verification
├── db-migrate.md                # NEW - Database migrations
├── deploy-rescue.md             # NEW - Deployment recovery
├── ecdash_client.py             # Original - EcDash API client
├── echo_orchestrator.py         # Original - Echo core
├── gitignore_template.txt       # Original - Utility
├── key_vault.py                 # Original - Security
├── memory_consolidator.py       # Original - Memory ops
├── memory-sync.md               # NEW - Memory sync
├── memory_manager.py            # Original - Memory management
├── quick-status.md             # NEW - Health checks
├── rollback-ready.md            # NEW - Rollback procedures
├── saas_security_core.py        # Original - Security
├── security-audit.md            # NEW - Security scanning
├── security_checklist.md        # Original - Security
├── session-log.md               # NEW - Session logging
├── settings_routes.py           # Original - EcDash routes
├── template-debug.md            # NEW - Template debugging
├── test_security_core.py        # Original - Security testing
└── todo_manager.py              # Original - Task management
```

---

## Cross-Reference

| Problem | Primary Tool | Related Tools |
|---------|--------------|---------------|
| Deployment failed | `deploy-rescue` | `rollback-ready`, `db-migrate` |
| Security concern | `security-audit` | `deploy-rescue`, `template-debug` |
| Need to rollback | `rollback-ready` | `deploy-rescue`, `db-migrate` |
| Schema change | `db-migrate` | `deploy-rescue`, `rollback-ready` |
| CSS/nav broken | `template-debug` | `deploy-rescue`, `security-audit` |
| Check services | `quick-status` | `backup-verify`, `deploy-rescue` |
| Verify backups | `backup-verify` | `memory-sync`, `session-log` |
| Sync context | `memory-sync` | `session-log`, `backup-verify` |
| End of session | `session-log` | `memory-sync`, `backup-verify` |

---

*Tools v2.0 — Enhanced by Echo (KiloClaw) on 2026-05-04*
*9 new tools added to original suite*