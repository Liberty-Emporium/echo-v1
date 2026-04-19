---
name: memory-upgrade
description: Upgrade, consolidate, and maintain Echo's memory system using 2025-2026 best practices. Use when asked to improve memory, consolidate notes, do a memory audit, extract facts from today's session, upgrade the memory architecture, prevent "soul erosion", or keep long-term memory fresh and accurate. Also use periodically during heartbeats to distill daily notes into long-term memory.
---

# Memory Upgrade

Applies the latest AI agent memory research (2025–2026) to keep Echo's memory sharp, layered, and accurate.

## Memory Architecture (3-Layer Model)

We use a file-system-as-memory pattern, upgraded with structured layers:

```
Working Memory     → Current session context (in-context only, ephemeral)
Short-Term Memory  → memory/YYYY-MM-DD.md  (daily diary, raw notes)
Long-Term Memory   → MEMORY.md             (curated, consolidated facts)
Entity Memory      → memory/entities.json  (people, projects, URLs — deduplicated)
Procedural Memory  → skills/custom/        (how to do things — skills are procedures)
```

## Core Upgrade Procedures

### 1. Daily → Long-Term Consolidation

After any session with significant new info, extract and update:

```
Read: memory/YYYY-MM-DD.md (today + yesterday)
Ask: What's worth keeping permanently?
  - Decisions made
  - New people/projects/facts learned
  - Lessons from mistakes
  - Preferences revealed
Write distilled insights to: MEMORY.md
```

Rules:
- **Never duplicate** — check MEMORY.md before adding
- **Date-stamp new facts** with `(learned YYYY-MM-DD)`
- **Mark stale facts** — if something has changed, update or delete it
- **Prefer specifics** — "Jay uses Railway for all deployments" beats "Jay uses cloud hosting"

### 2. Entity Memory (entities.json)

Maintain structured facts about key entities. See `references/entity-schema.md`.

Update after learning about:
- New people (name, role, relationship to Jay)
- New projects (name, URL, tech stack, status)
- Businesses (name, purpose, revenue model)
- Tools/services (what they do, credentials location)

### 3. Memory Governance (Prevent Soul Erosion)

"Soul erosion" = when an AI loses coherence across sessions due to stale/conflicting memory.

**Prevent it by:**
- Versioning: never delete from MEMORY.md, mark as `[OUTDATED as of DATE]` instead
- Conflict resolution: if a new fact contradicts an old one, update with note
- Forgetting policy: archive daily notes older than 60 days to `memory/archive/`
- Trust checking: flag anything Jay says that contradicts prior known facts

### 4. Prospective Memory (What We Might Need Later)

After major sessions, write a `## Next Session Priorities` block in today's diary:
```markdown
## Next Session Priorities
- [ ] Ask Jay about Mom's app URL
- [ ] Rotate GitHub token (marked temporary)
- [ ] Set up KYS token for brain encryption
```

This gets surfaced by session-startup skill automatically.

## When to Run

- **Every session end** — run consolidation step 1
- **Weekly** — run entity memory update (step 2)  
- **Monthly** — run governance audit (step 3)
- **After learning something surprising** — immediate entity update

## Anti-Patterns to Avoid

- ❌ Storing raw tokens or passwords in MEMORY.md (use /root/.secrets/)
- ❌ Adding vague facts ("Jay likes AI") — be specific
- ❌ Letting daily files accumulate without consolidating
- ❌ Duplicating the same fact in multiple places
- ❌ Trusting memory over what Jay just told you (in-session overrides memory)
