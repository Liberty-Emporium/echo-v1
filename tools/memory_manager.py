#!/usr/bin/env python3
"""
memory_manager.py — Echo's Structured Memory System
=====================================================
Based on research into AI agent memory architectures (2025):
- Retain-Recall-Reflect pattern (HINDSIGHT architecture)
- 7 memory types: fact, preference, event, goal, instruction, relationship, opinion
- Keyword + category search (no vector DB needed — we're file-based)
- Contradiction detection — flags conflicts with existing memories
- Temporal tagging — every memory has context of when/why it was stored

Usage:
  python3 memory_manager.py retain "Jay prefers dark mode" --type preference --tags jay,ui
  python3 memory_manager.py recall "Jay's preferences"
  python3 memory_manager.py recall "railway deploy" --type instruction
  python3 memory_manager.py reflect              # Summarize what we know
  python3 memory_manager.py list --type fact
  python3 memory_manager.py forget <id>          # Soft-delete (mark stale)
  python3 memory_manager.py stats
"""

import json
import sys
import os
import argparse
import re
from datetime import datetime, timezone
from pathlib import Path

MEMORY_FILE = Path(__file__).parent.parent / "memory" / "structured_memory.json"

MEMORY_TYPES = ["fact", "preference", "event", "goal", "instruction", "relationship", "opinion"]


def load_memory():
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE) as f:
            return json.load(f)
    return {"memories": [], "reflections": [], "version": "1.0", "last_updated": None}


def save_memory(data):
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    data["last_updated"] = now_iso()
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def next_id(data):
    ids = [m["id"] for m in data["memories"]]
    nums = [int(i.replace("mem_", "")) for i in ids if i.startswith("mem_")]
    return f"mem_{(max(nums) + 1) if nums else 1:04d}"


def tokenize(text):
    """Simple keyword tokenizer"""
    return set(re.findall(r'\b[a-z0-9_-]{3,}\b', text.lower()))


def score_relevance(memory, query_tokens):
    """Score a memory against query tokens"""
    mem_text = f"{memory['content']} {' '.join(memory.get('tags', []))}"
    mem_tokens = tokenize(mem_text)
    overlap = query_tokens & mem_tokens
    return len(overlap)


def detect_contradiction(new_content, existing_memories):
    """Flag potential contradictions — same tags + opposite sentiment keywords"""
    contradictions = []
    neg_words = {"not", "never", "don't", "no", "disabled", "off", "false", "removed", "deleted"}
    new_tokens = tokenize(new_content)
    new_has_neg = bool(new_tokens & neg_words)

    for m in existing_memories:
        if m.get("stale"):
            continue
        existing_tokens = tokenize(m["content"])
        existing_has_neg = bool(existing_tokens & neg_words)
        overlap = new_tokens & existing_tokens - neg_words - {"the", "and", "for", "with"}

        # If they share significant keywords but differ in negation
        if len(overlap) >= 2 and new_has_neg != existing_has_neg:
            contradictions.append(m)

    return contradictions


def cmd_retain(args):
    data = load_memory()

    # Check for contradictions
    contradictions = detect_contradiction(args.content, data["memories"])
    if contradictions:
        print(f"⚠️  Potential contradiction(s) detected with existing memories:")
        for c in contradictions[:3]:
            print(f"   [{c['id']}] {c['content'][:80]}")
        print("   Storing new memory anyway — use 'forget <id>' to mark old ones stale.\n")

    tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
    memory = {
        "id": next_id(data),
        "type": args.type,
        "content": args.content,
        "tags": tags,
        "source": args.source or "manual",
        "confidence": args.confidence or "high",
        "created": now_iso(),
        "updated": now_iso(),
        "stale": False,
        "notes": args.note or ""
    }
    data["memories"].append(memory)
    save_memory(data)
    print(f"🧠 Retained [{memory['id']}] ({memory['type']}) {memory['content'][:60]}")


def cmd_recall(args):
    data = load_memory()
    memories = [m for m in data["memories"] if not m.get("stale")]

    if args.type:
        memories = [m for m in memories if m["type"] == args.type]

    if args.content:
        query_tokens = tokenize(args.content)
        scored = [(score_relevance(m, query_tokens), m) for m in memories]
        scored = [(s, m) for s, m in scored if s > 0]
        scored.sort(key=lambda x: -x[0])
        memories = [m for _, m in scored[:args.limit or 10]]

    if not memories:
        print("🔍 No matching memories found.")
        return

    type_icon = {
        "fact": "📌", "preference": "💜", "event": "📅",
        "goal": "🎯", "instruction": "📋", "relationship": "🤝", "opinion": "💭"
    }

    for m in memories:
        icon = type_icon.get(m["type"], "🧠")
        tags = f" [{', '.join(m['tags'])}]" if m["tags"] else ""
        note = f"\n      📝 {m['notes']}" if m["notes"] else ""
        age = _age_str(m["created"])
        print(f"{icon} [{m['id']}] {m['content']}{tags} ({age}){note}")


def cmd_reflect(args):
    """Summarize what we know — generate a reflection"""
    data = load_memory()
    memories = [m for m in data["memories"] if not m.get("stale")]

    if not memories:
        print("No memories yet to reflect on.")
        return

    # Group by type
    by_type = {}
    for m in memories:
        by_type.setdefault(m["type"], []).append(m)

    print(f"🔮 Memory Reflection — {len(memories)} total memories\n")
    print("=" * 60)

    type_icon = {
        "fact": "📌", "preference": "💜", "event": "📅",
        "goal": "🎯", "instruction": "📋", "relationship": "🤝", "opinion": "💭"
    }

    for mtype in MEMORY_TYPES:
        items = by_type.get(mtype, [])
        if not items:
            continue
        icon = type_icon.get(mtype, "🧠")
        print(f"\n{icon} {mtype.upper()} ({len(items)} items)")
        for m in items[-5:]:  # Show last 5 per type
            print(f"  • {m['content'][:80]}")

    # Recent events
    recent = sorted(memories, key=lambda x: x["created"], reverse=True)[:5]
    print(f"\n\n🕐 Most Recent Memories:")
    for m in recent:
        age = _age_str(m["created"])
        print(f"  • [{m['type']}] {m['content'][:70]} ({age})")

    print("\n" + "=" * 60)

    # Save reflection
    reflection = {
        "timestamp": now_iso(),
        "total_memories": len(memories),
        "by_type": {k: len(v) for k, v in by_type.items()}
    }
    data.setdefault("reflections", []).append(reflection)
    save_memory(data)
    print(f"\n✅ Reflection saved to structured_memory.json")


def cmd_list(args):
    data = load_memory()
    memories = data["memories"]

    if not args.include_stale:
        memories = [m for m in memories if not m.get("stale")]
    if args.type:
        memories = [m for m in memories if m["type"] == args.type]

    if not memories:
        print("No memories found.")
        return

    # Sort newest first
    memories.sort(key=lambda x: x["created"], reverse=True)
    limit = args.limit or 20
    memories = memories[:limit]

    type_icon = {
        "fact": "📌", "preference": "💜", "event": "📅",
        "goal": "🎯", "instruction": "📋", "relationship": "🤝", "opinion": "💭"
    }

    for m in memories:
        icon = type_icon.get(m["type"], "🧠")
        stale_flag = " [STALE]" if m.get("stale") else ""
        tags = f" [{', '.join(m['tags'])}]" if m["tags"] else ""
        age = _age_str(m["created"])
        print(f"{icon} [{m['id']}]{stale_flag} {m['content'][:80]}{tags} ({age})")


def cmd_forget(args):
    data = load_memory()
    for m in data["memories"]:
        if m["id"] == args.id:
            m["stale"] = True
            m["updated"] = now_iso()
            save_memory(data)
            print(f"🗑️  Marked stale: [{m['id']}] {m['content'][:60]}")
            return
    print(f"❌ Memory not found: {args.id}")


def cmd_stats(args):
    data = load_memory()
    total = len(data["memories"])
    active = len([m for m in data["memories"] if not m.get("stale")])
    stale = total - active

    by_type = {}
    for m in data["memories"]:
        if not m.get("stale"):
            by_type[m["type"]] = by_type.get(m["type"], 0) + 1

    print(f"🧠 Memory Stats")
    print(f"   Total: {total} | Active: {active} | Stale: {stale}")
    print(f"\n   By type:")
    for t, count in sorted(by_type.items(), key=lambda x: -x[1]):
        print(f"     {t}: {count}")

    if data.get("last_updated"):
        print(f"\n   Last updated: {_age_str(data['last_updated'])}")


def _age_str(iso_str):
    try:
        created = datetime.fromisoformat(iso_str)
        delta = datetime.now(timezone.utc) - created
        if delta.days == 0:
            hours = delta.seconds // 3600
            return f"{hours}h ago" if hours > 0 else "just now"
        elif delta.days == 1:
            return "yesterday"
        else:
            return f"{delta.days}d ago"
    except:
        return "unknown"


def main():
    parser = argparse.ArgumentParser(description="Echo Memory Manager")
    sub = parser.add_subparsers(dest="command")

    # retain
    p_retain = sub.add_parser("retain", help="Store a new memory")
    p_retain.add_argument("content", help="Memory content")
    p_retain.add_argument("--type", choices=MEMORY_TYPES, default="fact")
    p_retain.add_argument("--tags", help="Comma-separated tags")
    p_retain.add_argument("--source", help="Source (session/script/etc)")
    p_retain.add_argument("--confidence", choices=["high", "medium", "low"], default="high")
    p_retain.add_argument("--note", help="Additional notes")

    # recall
    p_recall = sub.add_parser("recall", help="Search memories")
    p_recall.add_argument("content", nargs="?", help="Query text")
    p_recall.add_argument("--type", choices=MEMORY_TYPES)
    p_recall.add_argument("--limit", type=int, default=10)

    # reflect
    sub.add_parser("reflect", help="Summarize what we know")

    # list
    p_list = sub.add_parser("list", help="List memories")
    p_list.add_argument("--type", choices=MEMORY_TYPES)
    p_list.add_argument("--limit", type=int, default=20)
    p_list.add_argument("--include-stale", action="store_true")

    # forget
    p_forget = sub.add_parser("forget", help="Mark a memory as stale")
    p_forget.add_argument("id")

    # stats
    sub.add_parser("stats", help="Memory statistics")

    args = parser.parse_args()

    cmds = {
        "retain": cmd_retain,
        "recall": cmd_recall,
        "reflect": cmd_reflect,
        "list": cmd_list,
        "forget": cmd_forget,
        "stats": cmd_stats,
    }

    if args.command in cmds:
        cmds[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
