#!/usr/bin/env python3
"""
memory_consolidator.py — Echo's Memory Consolidation Engine
============================================================
Based on MEM1 / HINDSIGHT research:
- Reads daily memory logs (memory/YYYY-MM-DD.md)
- Extracts key facts, decisions, lessons, TODOs
- Detects stale/completed items in MEMORY.md
- Generates a consolidation report
- Optionally updates MEMORY.md with distilled learnings

Usage:
  python3 memory_consolidator.py scan           # Scan recent daily logs
  python3 memory_consolidator.py check-stale    # Find stale TODOs in MEMORY.md
  python3 memory_consolidator.py report         # Full memory health report
  python3 memory_consolidator.py distill        # Extract facts to memory_manager
"""

import json
import re
import sys
import os
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path

WORKSPACE = Path(__file__).parent.parent
MEMORY_DIR = WORKSPACE / "memory"
MEMORY_MD = WORKSPACE / "MEMORY.md"
TODO_FILE = MEMORY_DIR / "todos.json"
STRUCT_MEMORY = MEMORY_DIR / "structured_memory.json"

# Patterns that suggest a TODO is completed
DONE_PATTERNS = [
    r'\bdone\b', r'\bcomplete[d]?\b', r'\bfixed\b', r'\bdeployed\b',
    r'\bchanged\b', r'\bupdated\b', r'\bworking\b', r'\bactivated\b',
    r'✅', r'\bfinished\b', r'\bpushed\b', r'\bmerged\b'
]

# Patterns that suggest important facts to remember
FACT_PATTERNS = [
    r'(?:URL|url|endpoint)[:\s]+https?://\S+',
    r'(?:password|token|key)[:\s]+\S+',
    r'(?:project ID|project_id)[:\s]+[\w-]+',
    r'(?:port|PORT)[:\s]+\d+',
    r'(?:version|v)\s*[\d.]+',
]


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def load_daily_log(date_str):
    path = MEMORY_DIR / f"{date_str}.md"
    if path.exists():
        return path.read_text()
    return None


def get_recent_dates(days=7):
    today = datetime.now(timezone.utc).date()
    return [(today - timedelta(days=i)).isoformat() for i in range(days)]


def extract_todos_from_md(text):
    """Find TODO-like items in markdown text"""
    todos = []
    patterns = [
        r'- \[ \] (.+)',           # GitHub-style unchecked
        r'TODO[:\s]+(.+)',          # TODO: label
        r'(?:^|\n)- (.+)\s*$',    # Simple list items
    ]
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
        todos.extend(matches)
    return list(set(todos))


def check_stale_memory():
    """Scan MEMORY.md for TODOs and check if they seem done based on daily logs"""
    if not MEMORY_MD.exists():
        print("❌ MEMORY.md not found")
        return

    memory_text = MEMORY_MD.read_text()

    # Extract TODO section
    todo_section_match = re.search(r'## Open TODOs(.+?)(?=\n## |\Z)', memory_text, re.DOTALL)
    if not todo_section_match:
        print("✅ No TODO section found in MEMORY.md")
        return

    todo_text = todo_section_match.group(1)
    todo_lines = [l.strip() for l in todo_text.split('\n') if l.strip() and l.strip().startswith(('-', '*'))]

    # Load recent daily logs
    recent_text = ""
    for date_str in get_recent_dates(7):
        log = load_daily_log(date_str)
        if log:
            recent_text += f"\n{log}"

    print(f"🔍 Checking {len(todo_lines)} TODO items against last 7 days of logs...\n")

    done_pattern = re.compile('|'.join(DONE_PATTERNS), re.IGNORECASE)
    possibly_done = []
    still_open = []

    for todo in todo_lines:
        # Extract the core task text (strip checkboxes, bullets)
        task = re.sub(r'^[-*]\s*(?:\[[ x]\])?\s*', '', todo).strip()
        task_keywords = [w for w in re.findall(r'\b\w{4,}\b', task.lower()) if w not in
                         {'with', 'this', 'that', 'from', 'have', 'will', 'need', 'must', 'should'}]

        # Check if this task's keywords appear near completion words in recent logs
        found_in_logs = False
        for keyword in task_keywords[:3]:
            pattern = rf'.{{0,100}}{re.escape(keyword)}.{{0,100}}'
            snippets = re.findall(pattern, recent_text, re.IGNORECASE)
            for snippet in snippets:
                if done_pattern.search(snippet):
                    found_in_logs = True
                    break
            if found_in_logs:
                break

        if found_in_logs:
            possibly_done.append(task)
        else:
            still_open.append(task)

    if possibly_done:
        print("⚠️  These TODOs MIGHT be done (mentioned with completion language in recent logs):")
        for t in possibly_done:
            print(f"   🤔 {t[:80]}")
        print()

    if still_open:
        print("📋 These TODOs appear still open:")
        for t in still_open:
            print(f"   ⬜ {t[:80]}")

    print(f"\n📊 Summary: {len(possibly_done)} possibly done, {len(still_open)} still open")
    print("   → Review above and run `todo_manager.py done <id>` to mark completed")


def cmd_scan(args):
    """Scan recent daily logs for key info"""
    print("📖 Scanning recent daily memory logs...\n")

    found_logs = []
    for date_str in get_recent_dates(7):
        log = load_daily_log(date_str)
        if log:
            found_logs.append((date_str, log))

    if not found_logs:
        print("No daily logs found in the last 7 days.")
        return

    print(f"Found {len(found_logs)} daily log(s):\n")
    for date_str, log in found_logs:
        lines = log.strip().split('\n')
        print(f"📅 {date_str} ({len(lines)} lines)")

        # Extract notable items
        todos = extract_todos_from_md(log)
        if todos:
            print(f"   TODOs found: {len(todos)}")
            for t in todos[:3]:
                print(f"     • {t[:70]}")

        # Find URLs
        urls = re.findall(r'https?://\S+', log)
        if urls:
            print(f"   URLs: {len(urls)} found")
        print()


def cmd_check_stale(args):
    check_stale_memory()


def cmd_report(args):
    """Full memory health report"""
    print("🧠 Echo Memory Health Report")
    print("=" * 60)
    print(f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n")

    # 1. MEMORY.md stats
    if MEMORY_MD.exists():
        text = MEMORY_MD.read_text()
        lines = text.split('\n')
        sections = [l for l in lines if l.startswith('## ')]
        print(f"📝 MEMORY.md: {len(lines)} lines, {len(sections)} sections")
        for s in sections:
            print(f"   {s}")
    else:
        print("❌ MEMORY.md missing!")

    # 2. Daily logs
    print(f"\n📅 Daily Logs (last 7 days):")
    for date_str in get_recent_dates(7):
        log = load_daily_log(date_str)
        if log:
            print(f"   ✅ {date_str} ({len(log.split(chr(10)))} lines)")
        else:
            print(f"   ⬜ {date_str} (none)")

    # 3. Structured memory stats
    if STRUCT_MEMORY.exists():
        with open(STRUCT_MEMORY) as f:
            sm = json.load(f)
        active = len([m for m in sm.get("memories", []) if not m.get("stale")])
        total = len(sm.get("memories", []))
        print(f"\n🧩 Structured Memory: {active} active / {total} total")
    else:
        print(f"\n🧩 Structured Memory: not yet initialized")

    # 4. TODO stats
    if TODO_FILE.exists():
        with open(TODO_FILE) as f:
            td = json.load(f)
        open_count = len([t for t in td.get("todos", []) if t["status"] in ("open", "in-progress")])
        done_count = len([t for t in td.get("todos", []) if t["status"] == "done"])
        total_count = len(td.get("todos", []))
        print(f"\n✅ TODO Manager: {open_count} open, {done_count} done, {total_count} total")
    else:
        print(f"\n✅ TODO Manager: not yet initialized")

    # 5. Stale TODO check
    print(f"\n🔍 Stale TODO Analysis:")
    check_stale_memory()


def cmd_distill(args):
    """Extract key facts from daily logs into structured memory"""
    print("🔬 Distilling daily logs into structured memory...\n")

    # Load structured memory
    if STRUCT_MEMORY.exists():
        with open(STRUCT_MEMORY) as f:
            sm = json.load(f)
    else:
        sm = {"memories": [], "reflections": [], "version": "1.0", "last_updated": None}

    existing_contents = {m["content"] for m in sm["memories"]}
    added = 0

    for date_str in get_recent_dates(7):
        log = load_daily_log(date_str)
        if not log:
            continue

        # Find URL mentions
        urls = re.findall(r'(https?://\S+)', log)
        for url in set(urls):
            content = f"URL encountered: {url}"
            if content not in existing_contents:
                sm["memories"].append({
                    "id": f"mem_auto_{len(sm['memories']) + 1:04d}",
                    "type": "fact",
                    "content": content,
                    "tags": ["url", "auto-extracted"],
                    "source": f"daily-log-{date_str}",
                    "confidence": "medium",
                    "created": now_iso(),
                    "updated": now_iso(),
                    "stale": False,
                    "notes": f"Auto-extracted from {date_str} log"
                })
                existing_contents.add(content)
                added += 1

    sm["last_updated"] = now_iso()
    STRUCT_MEMORY.parent.mkdir(parents=True, exist_ok=True)
    with open(STRUCT_MEMORY, "w") as f:
        json.dump(sm, f, indent=2)

    print(f"✅ Distilled {added} new items into structured memory")
    print(f"   Total memories: {len(sm['memories'])}")


def main():
    parser = argparse.ArgumentParser(description="Echo Memory Consolidator")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("scan", help="Scan recent daily logs")
    sub.add_parser("check-stale", help="Find possibly-completed TODOs in MEMORY.md")
    sub.add_parser("report", help="Full memory health report")
    sub.add_parser("distill", help="Extract facts from daily logs into structured memory")

    args = parser.parse_args()

    cmds = {
        "scan": cmd_scan,
        "check-stale": cmd_check_stale,
        "report": cmd_report,
        "distill": cmd_distill,
    }

    if args.command in cmds:
        cmds[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
