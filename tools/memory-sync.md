# Tool: memory-sync
**Type:** Context Management
**Use when:** Starting session, need current project state, resuming work
**Trigger phrases:** "Sync memory", "What's latest?", "Update context", "Pull latest"

## What It Does
Pull latest context from echo-v1 memory files. Keep local memory current with brain.

## How To Use

### Step 1: Check Echo-v1 Brain (GitHub)
```bash
# Get latest memory files
curl -s "https://api.github.com/repos/Liberty-Emporium/echo-v1/contents/memory" | grep '"name"'
```

### Step 2: Get Date-Stamped Memories
```bash
# Download recent memory files
curl -s "https://raw.githubusercontent.com/Liberty-Emporium/echo-v1/main/memory/2026-05-01.md"
curl -s "https://raw.githubusercontent.com/Liberty-Emporium/echo-v1/main/memory/2026-05-02.md"
# etc.
```

### Step 3: Check SKILLS.md and TOOLS.md
```bash
# Get current capabilities
curl -s "https://raw.githubusercontent.com/Liberty-Emporium/echo-v1/main/SKILLS.md"
curl -s "https://raw.githubusercontent.com/Liberty-Emporium/echo-v1/main/TOOLS.md"
```

### Step 4: Merge with Local Memory
- Combine what's in GitHub with local session memory
- Identify any new projects or changes
- Update context for current session

## Related
- `backup-verify` — Ensure memory is backed up
- `session-log` — Write new memories

---
*Tool: memory-sync v1.0 — Built for Liberty-Emporium by Echo (KiloClaw)*