# Memory Architecture Research
*Researched: 2026-04-16 by Echo*

## What I Learned About My Own Memory Problem

### The Core Problem
I wake up fresh every session. My memory lives in markdown files. The issues:
1. **Flat structure** — MEMORY.md is one big blob, hard to search
2. **No contradiction detection** — stale data quietly sits next to fresh data
3. **No consolidation** — daily logs pile up, never get distilled
4. **No priority** — TODOs have no age, status, or urgency
5. **No verification** — I say something is done without checking

### What Current Research Says (2025/2026)

#### Memory Types (Human → AI Mapping)
| Human Memory | AI Equivalent | What It Stores |
|---|---|---|
| Working memory | Context window | Current session, active task |
| Episodic memory | Daily logs (memory/YYYY-MM-DD.md) | What happened, when, in what context |
| Semantic memory | MEMORY.md + structured_memory.json | Facts, preferences, relationships |
| Procedural memory | SOUL.md, AGENTS.md, skills/ | How to do things |

#### Best Patterns Found

**HINDSIGHT Architecture** (best for us):
- 4 memory networks: world facts, agent experiences, entity summaries, evolving beliefs
- 3 operations: **Retain** (store) → **Recall** (retrieve) → **Reflect** (consolidate)
- Temporal metadata on everything
- Result: 39% → 83.6% accuracy on long-horizon benchmarks

**MEM1** (key insight):
- Don't just append forever — consolidate at each step
- A compact shared state that fuses memory + reasoning
- 3.7x memory reduction, 3.5x performance gain

**RetainDB** (7 memory types):
- Fact, Preference, Event, Relationship, Opinion, Goal, Instruction
- Version chains — track how beliefs evolve
- Delta compression for token savings

### What I Built

1. **`tools/todo_manager.py`** — JSON-backed TODO system
   - Priority (high/medium/low) + status + project + timestamps
   - `overdue` command flags stale items automatically
   - `report` generates fresh markdown for MEMORY.md
   - Replaces: flat "Open TODOs" list that never got cleaned

2. **`tools/memory_manager.py`** — Structured memory with Retain-Recall-Reflect
   - 7 memory types (fact/preference/event/goal/instruction/relationship/opinion)
   - Keyword search (no vector DB needed — file-based, fast)
   - Contradiction detection — flags conflicts with existing memories
   - `reflect` generates full snapshot of what I know

3. **`tools/memory_consolidator.py`** — Memory health + distillation
   - Scans daily logs for key info
   - Detects stale TODOs by cross-referencing recent logs
   - Full health report — gaps, missing logs, stale items
   - Auto-extracts facts (URLs, endpoints, etc.) from logs

### Usage Workflow

**Every session start:**
```bash
python3 tools/memory_consolidator.py report   # What's my memory health?
python3 tools/todo_manager.py list --status open  # What needs doing?
```

**When I learn something:**
```bash
python3 tools/memory_manager.py retain "Jay's Railway project ID is 42d6a945" --type fact --tags jay,railway
```

**When a TODO is done:**
```bash
python3 tools/todo_manager.py done todo_001
```

**Weekly (heartbeat):**
```bash
python3 tools/memory_consolidator.py check-stale  # Catch stale TODOs
python3 tools/memory_manager.py reflect           # Consolidate knowledge
```

### What's Still Missing (Future Improvements)
- Vector embeddings for semantic search (needs a local embedding model)
- Auto-extraction of facts from session transcripts
- Memory importance scoring (what to keep vs. forget)
- Cross-session contradiction resolution

### Key Insight
> The problem isn't that I forget — it's that I don't have good tools to *manage* what I remember.
> Flat markdown files are write-only. These tools make memory read-write-search.

---
*Sources: arxiv HINDSIGHT, MemVerse, MEM1, RetainDB, vectorize.io Hindsight, LLM agent memory survey 2026*
