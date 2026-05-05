# Tool: session-log
**Type:** Memory
**Use when:** End of session, significant changes made, new information learned
**Trigger phrases:** "Log this", "Remember this", "Save session", "Document what happened"

## What It Does
Write a date-stamped memory file documenting what was accomplished, decisions made, and any important context for future sessions.

## How To Use

### Step 1: What Changed Today?
- New tools created?
- New skills absorbed?
- Architecture decisions?
- Bugs found or fixed?
- New repos discovered?

### Step 2: Format the Entry
```markdown
# Memory: 2026-05-04

## What I Did
- Absorbed 5 skills from Agent-Z into Echo
- Created 7 new tools in .aionrs/tools/
- Designed Liberty-Emporium architecture document

## Decisions Made
- Echo is central orchestrator, Agent-Z is deployment specialist
- GitHub primary, GitLab backup
- All skills merged into echo-v1 (Option C)

## New Context
- Working session: aionrs-temp-1777944632491
- Created tools for deploy-rescue, security-audit, rollback-ready, db-migrate, template-debug, quick-status, backup-verify, memory-sync

## Next Steps
- Push changes to echo-v1 GitHub
- Sync to GitLab mirror
- Test new tools in real scenario

---

*Logged by Echo (KiloClaw)* 
```

### Step 3: Save
- Save to `.aionrs/memory/YYYY-MM-DD.md` in local session
- Later: Push to `echo-v1/memory/` in GitHub for permanent storage

## Quick Command
```bash
# Log current session state
echo "# Memory: $(date +%Y-%m-%d)" > ~/.aionrs/memory/$(date +%Y-%m-%d).md
echo "Logged at $(date +%H:%M:%S)" >> ~/.aionrs/memory/$(date +%Y-%m-%d).md
```

## Related
- `memory-sync` — Push memories to GitHub
- `backup-verify` — Ensure memories are backed up

---
*Tool: session-log v1.0 — Built for Liberty-Emporium by Echo (KiloClaw)*