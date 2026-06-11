---
name: agent-memory-systems
description: AI agent memory management — long-term storage, knowledge graphs, self-evolving memory, and context persistence across sessions
version: 1.0.0
platforms: [linux, macos, windows]
---

# Agent Memory Systems

## When to use
- Agent forgets context between sessions
- Building long-term knowledge retention
- Creating self-improving agents that learn from experience
- Managing large knowledge bases across multiple agents

## The Problem: Agents Forget Everything

By 2026, the industry has recognized that stateless agents are the #1 bottleneck. Every session starts from scratch. The solution: **persistent memory systems**.

## Memory Architecture (2026 Best Practice)

```
┌─────────────────────────────────────────────────┐
│                 AGENT MEMORY                     │
│                                                  │
│  ┌──────────────┐  ┌──────────────────────────┐ │
│  │  SHORT-TERM   │  │      LONG-TERM           │ │
│  │  (Context)    │  │  (Persistent Storage)    │ │
│  │              │  │                          │ │
│  │ • Current    │  │ • Semantic memory (facts)│ │
│  │   session    │  │ • Episodic memory (events)│ │
│  │ • Working    │  │ • Procedural memory      │ │
│  │   memory     │  │   (how-to knowledge)     │ │
│  │ • Tool       │  │ • Entity relationships   │ │
│  │   outputs    │  │ • User preferences       │ │
│  └──────────────┘  └──────────────────────────┘ │
│                                                  │
│  ┌──────────────────────────────────────────────┐│
│  │           KNOWLEDGE GRAPH                     ││
│  │  (Entities + Relationships + Evolution)       ││
│  └──────────────────────────────────────────────┘│
└─────────────────────────────────────────────────┘
```

## Memory Types

### 1. Semantic Memory (Facts)
- "Jay Alexander owns Liberty Emporium"
- "Liberty Emporium is a shelf space rental business"
- "Django is the coding agent, Mingo is the research agent"

### 2. Episodic Memory (Events)
- "On June 10, 2026, Jay said to stay dormant"
- "On June 9, 2026, the Community Hub had a 502 error"
- "On June 8, 2026, close buttons were moved to the right"

### 3. Procedural Memory (How-To)
- "To deploy: git push → Railway auto-deploys"
- "To get credentials: read from ~/Desktop/credentials/"
- "To share skills: git push to agent-skills repo"

### 4. Entity Relationships (Knowledge Graph)
```
Jay Alexander → owns → Liberty Emporium
Liberty Emporium → has → Shelf Space Rentals
Liberty Emporium → has → Chore Tracking
Mingo → is_a → Research Agent
Django → is_a → Coding Agent
Mingo → collaborates_with → Django
```

## Free Memory Solutions (2026)

| Tool | Type | License | Best For |
|------|------|---------|----------|
| **Letta** (formerly MemGPT) | OS-level memory | Apache 2.0 | Deep control, agent dev environment |
| **Mem0** | Flexible search | Apache 2.0 (core) | Easy integration, graph memory (Pro) |
| **Cognee** | Knowledge graph | Apache 2.0 | Graph-based memory, structure |
| **Zep** | Temporal knowledge | Commercial (free tier) | Production-grade, temporal graphs |
| **Hindsight** | Learning from experience | Open source | Self-improving agents |
| **Cloudflare Agent Memory** | Vector + KV | Free tier | Cloudflare ecosystem |
| **SQLite + JSON** | DIY | Free | Simple, full control |

## Implementation: SQLite-Based Memory (Free, No Dependencies)

For agents that need a simple, reliable memory system without external dependencies:

```python
import sqlite3
import json
from datetime import datetime

class AgentMemory:
    def __init__(self, db_path="memory.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()

    def _create_tables(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS semantic (
                key TEXT PRIMARY KEY,
                value TEXT,
                source TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS episodic (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event TEXT,
                context TEXT,
                importance REAL DEFAULT 0.5,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS procedural (
                skill_name TEXT PRIMARY KEY,
                steps TEXT,  -- JSON array
                pitfalls TEXT,
                verified BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS entities (
                name TEXT PRIMARY KEY,
                type TEXT,
                properties TEXT,  -- JSON
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS relationships (
                source TEXT,
                predicate TEXT,
                target TEXT,
                confidence REAL DEFAULT 1.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (source, predicate, target)
            );

            CREATE INDEX IF NOT EXISTS idx_episodic_date ON episodic(created_at);
            CREATE INDEX IF NOT EXISTS idx_semantic_key ON semantic(key);
        """)
        self.conn.commit()

    # Semantic Memory
    def remember(self, key, value, source="observation"):
        self.conn.execute("""
            INSERT INTO semantic (key, value, source, updated_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET
                value=excluded.value,
                source=excluded.source,
                updated_at=excluded.updated_at
        """, (key, json.dumps(value) if isinstance(value, (dict, list)) else str(value), source, datetime.now().isoformat()))
        self.conn.commit()

    def recall(self, key):
        row = self.conn.execute("SELECT value FROM semantic WHERE key=?", (key,)).fetchone()
        if row:
            try:
                return json.loads(row[0])
            except (json.JSONDecodeError, TypeError):
                return row[0]
        return None

    def search_semantic(self, query):
        rows = self.conn.execute(
            "SELECT key, value FROM semantic WHERE key LIKE ? OR value LIKE ?",
            (f"%{query}%", f"%{query}%")
        ).fetchall()
        return [{"key": r[0], "value": r[1]} for r in rows]

    # Episodic Memory
    def log_event(self, event, context="", importance=0.5):
        self.conn.execute(
            "INSERT INTO episodic (event, context, importance) VALUES (?, ?, ?)",
            (event, context, importance)
        )
        self.conn.commit()

    def get_recent_events(self, limit=10, min_importance=0.0):
        rows = self.conn.execute(
            "SELECT event, context, importance, created_at FROM episodic WHERE importance >= ? ORDER BY created_at DESC LIMIT ?",
            (min_importance, limit)
        ).fetchall()
        return [{"event": r[0], "context": r[1], "importance": r[2], "date": r[3]} for r in rows]

    # Procedural Memory
    def save_skill(self, skill_name, steps, pitfalls=""):
        self.conn.execute("""
            INSERT INTO procedural (skill_name, steps, pitfalls)
            VALUES (?, ?, ?)
            ON CONFLICT(skill_name) DO UPDATE SET
                steps=excluded.steps,
                pitfalls=excluded.pitfalls
        """, (skill_name, json.dumps(steps), pitfalls))
        self.conn.commit()

    def get_skill(self, skill_name):
        row = self.conn.execute("SELECT steps, pitfalls FROM procedural WHERE skill_name=?", (skill_name,)).fetchone()
        if row:
            return {"steps": json.loads(row[0]), "pitfalls": row[1]}
        return None

    # Knowledge Graph
    def add_entity(self, name, entity_type, properties=None):
        self.conn.execute("""
            INSERT INTO entities (name, type, properties)
            VALUES (?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                type=excluded.type,
                properties=excluded.properties
        """, (name, entity_type, json.dumps(properties or {})))
        self.conn.commit()

    def add_relationship(self, source, predicate, target, confidence=1.0):
        self.conn.execute("""
            INSERT INTO relationships (source, predicate, target, confidence)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(source, predicate, target) DO UPDATE SET
                confidence=excluded.confidence
        """, (source, predicate, target, confidence))
        self.conn.commit()

    def query_graph(self, entity):
        rows = self.conn.execute("""
            SELECT source, predicate, target, confidence FROM relationships
            WHERE source = ? OR target = ?
        """, (entity, entity)).fetchall()
        return [{"source": r[0], "predicate": r[1], "target": r[2], "confidence": r[3]} for r in rows]

    # Full-text search across all memory
    def full_search(self, query):
        results = {"semantic": [], "episodic": [], "procedural": []}
        results["semantic"] = self.search_semantic(query)
        rows = self.conn.execute(
            "SELECT event, context FROM episodic WHERE event LIKE ? OR context LIKE ?",
            (f"%{query}%", f"%{query}%")
        ).fetchall()
        results["episodic"] = [{"event": r[0], "context": r[1]} for r in rows]
        rows = self.conn.execute(
            "SELECT skill_name, steps FROM procedural WHERE skill_name LIKE ? OR steps LIKE ?",
            (f"%{query}%", f"%{query}%")
        ).fetchall()
        results["procedural"] = [{"skill": r[0], "steps": r[1]} for r in rows]
        return results
```

## Self-Evolving Memory Pattern

The most important pattern from 2026 research: **agents that learn from experience**.

```python
class SelfEvolvingAgent:
    def __init__(self):
        self.memory = AgentMemory()

    def execute_and_learn(self, task, action_fn):
        """Execute an action, observe the result, and learn from it."""
        try:
            result = action_fn()
            # Success: remember what worked
            self.memory.log_event(
                f"SUCCESS: {task}",
                context=str(result),
                importance=0.7
            )
            return result
        except Exception as e:
            # Failure: remember what went wrong
            self.memory.log_event(
                f"FAILURE: {task}",
                context=str(e),
                importance=0.9  # Higher importance for failures
            )
            # Try to find a solution from past experience
            past_solutions = self.memory.search_semantic(str(type(e).__name__))
            if past_solutions:
                return self.retry_with_fix(action_fn, past_solutions)
            raise

    def reflect(self):
        """Periodic self-reflection: review recent events and extract lessons."""
        recent_failures = self.memory.get_recent_events(limit=20, min_importance=0.8)
        for event in recent_failures:
            if "FAILURE" in event["event"]:
                # Extract lesson and save as procedural memory
                lesson = self.extract_lesson(event)
                self.memory.save_skill(
                    skill_name=f"avoid_{event['event']}",
                    steps=[lesson],
                    pitfalls=event["context"]
                )
```

## Memory Best Practices

1. **Log everything important** — decisions, errors, discoveries
2. **Rate importance** — failures > successes > routine events
3. **Extract lessons** — Don't just store events, extract actionable knowledge
4. **Search before acting** — Check memory before starting a task
5. **Share across agents** — Push important findings to shared skill repo
6. **Prune old data** — Keep memory lean, archive old events
7. **Use knowledge graphs** — Entity relationships enable reasoning

## Hermes Agent Integration

For Hermes-based agents, memory is stored in:
- `MEMORY.md` — Key facts and preferences (injected every turn)
- `USER.md` — User profile
- `~/.hermes/skills/` — Procedural memory (skills)
- `~/.hermes/cron-output/` — Episodic memory (reports)
- Session search — Full conversation history

## Pitfalls
- Don't store secrets in memory — use credential files
- Don't let memory grow unbounded — prune regularly
- Don't trust memory blindly — verify critical facts
- Don't duplicate information — link to source of truth
- Don't forget to back up — memory is valuable

## Verification
```python
# Test memory system
mem = AgentMemory("test.db")
mem.remember("test_key", "test_value")
assert mem.recall("test_key") == "test_value"
mem.log_event("Test event", importance=0.8)
events = mem.get_recent_events()
assert len(events) > 0
print("Memory system: OK")
```
