#!/usr/bin/env python3
"""
todo_manager.py — Echo's Structured TODO System
================================================
JSON-backed TODO tracker with priority, status, project, and timestamps.
Replaces the flat "Open TODOs" list in MEMORY.md that kept getting stale.

Usage:
  python3 todo_manager.py add "Task description" --priority high --project app-name
  python3 todo_manager.py list [--status open] [--project app-name] [--priority high]
  python3 todo_manager.py done <id>
  python3 todo_manager.py cancel <id>
  python3 todo_manager.py update <id> --note "New note"
  python3 todo_manager.py report          # Markdown summary (for MEMORY.md)
  python3 todo_manager.py overdue         # Items open > 7 days
  python3 todo_manager.py clean           # Archive completed/cancelled items
"""

import json
import sys
import os
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path

TODO_FILE = Path(__file__).parent.parent / "memory" / "todos.json"

PRIORITIES = ["high", "medium", "low"]
STATUSES = ["open", "in-progress", "done", "cancelled"]


def load_todos():
    if TODO_FILE.exists():
        with open(TODO_FILE) as f:
            return json.load(f)
    return {"todos": [], "archived": [], "last_updated": None}


def save_todos(data):
    TODO_FILE.parent.mkdir(parents=True, exist_ok=True)
    data["last_updated"] = now_iso()
    with open(TODO_FILE, "w") as f:
        json.dump(data, f, indent=2)


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def next_id(data):
    all_ids = [t["id"] for t in data["todos"] + data.get("archived", [])]
    nums = [int(i.replace("todo_", "")) for i in all_ids if i.startswith("todo_")]
    return f"todo_{(max(nums) + 1) if nums else 1:03d}"


def cmd_add(args):
    data = load_todos()
    todo = {
        "id": next_id(data),
        "task": args.task,
        "priority": args.priority,
        "status": "open",
        "project": args.project or "general",
        "created": now_iso(),
        "updated": now_iso(),
        "completed": None,
        "notes": args.note or ""
    }
    data["todos"].append(todo)
    save_todos(data)
    print(f"✅ Added [{todo['id']}] ({todo['priority'].upper()}) {todo['task']}")


def cmd_list(args):
    data = load_todos()
    todos = data["todos"]

    if args.status:
        todos = [t for t in todos if t["status"] == args.status]
    if args.project:
        todos = [t for t in todos if t["project"] == args.project]
    if args.priority:
        todos = [t for t in todos if t["priority"] == args.priority]

    if not todos:
        print("No todos found.")
        return

    # Sort: high → medium → low, then by created date
    priority_order = {"high": 0, "medium": 1, "low": 2}
    todos.sort(key=lambda t: (priority_order.get(t["priority"], 9), t["created"]))

    status_icon = {"open": "⬜", "in-progress": "🔄", "done": "✅", "cancelled": "❌"}
    priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}

    for t in todos:
        age = _age_str(t["created"])
        icon = status_icon.get(t["status"], "❓")
        pri = priority_icon.get(t["priority"], "⚪")
        note = f" — {t['notes']}" if t["notes"] else ""
        print(f"{icon} {pri} [{t['id']}] [{t['project']}] {t['task']}{note} ({age})")


def cmd_done(args):
    data = load_todos()
    for t in data["todos"]:
        if t["id"] == args.id:
            t["status"] = "done"
            t["completed"] = now_iso()
            t["updated"] = now_iso()
            save_todos(data)
            print(f"✅ Marked done: [{t['id']}] {t['task']}")
            return
    print(f"❌ Todo not found: {args.id}")


def cmd_cancel(args):
    data = load_todos()
    for t in data["todos"]:
        if t["id"] == args.id:
            t["status"] = "cancelled"
            t["updated"] = now_iso()
            save_todos(data)
            print(f"❌ Cancelled: [{t['id']}] {t['task']}")
            return
    print(f"❌ Todo not found: {args.id}")


def cmd_update(args):
    data = load_todos()
    for t in data["todos"]:
        if t["id"] == args.id:
            if args.note:
                t["notes"] = args.note
            if args.priority:
                t["priority"] = args.priority
            if args.status:
                t["status"] = args.status
                if args.status == "done":
                    t["completed"] = now_iso()
            if args.project:
                t["project"] = args.project
            t["updated"] = now_iso()
            save_todos(data)
            print(f"✏️  Updated: [{t['id']}] {t['task']}")
            return
    print(f"❌ Todo not found: {args.id}")


def cmd_report(args):
    """Generate a markdown summary suitable for pasting into MEMORY.md"""
    data = load_todos()
    open_todos = [t for t in data["todos"] if t["status"] in ("open", "in-progress")]
    done_recent = [t for t in data["todos"] if t["status"] == "done"]

    priority_order = {"high": 0, "medium": 1, "low": 2}
    open_todos.sort(key=lambda t: (priority_order.get(t["priority"], 9), t["created"]))

    lines = ["## Open TODOs (auto-generated by todo_manager.py)\n"]
    if not open_todos:
        lines.append("*No open todos! 🎉*\n")
    else:
        status_icon = {"open": "⬜", "in-progress": "🔄"}
        priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}
        for t in open_todos:
            icon = status_icon.get(t["status"], "⬜")
            pri = priority_icon.get(t["priority"], "⚪")
            note = f" — _{t['notes']}_" if t["notes"] else ""
            age = _age_str(t["created"])
            lines.append(f"- {icon} {pri} **[{t['project']}]** {t['task']}{note} *(added {age})*")

    if done_recent:
        lines.append("\n## Recently Completed\n")
        for t in sorted(done_recent, key=lambda x: x.get("completed", ""), reverse=True)[:5]:
            lines.append(f"- ✅ **[{t['project']}]** {t['task']}")

    print("\n".join(lines))


def cmd_overdue(args):
    data = load_todos()
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    overdue = []
    for t in data["todos"]:
        if t["status"] in ("open", "in-progress"):
            created = datetime.fromisoformat(t["created"])
            if created < cutoff:
                overdue.append(t)

    if not overdue:
        print("✅ No overdue todos (all open items < 7 days old)")
        return

    print(f"⚠️  {len(overdue)} overdue todo(s) (open > 7 days):\n")
    for t in overdue:
        age = _age_str(t["created"])
        print(f"  🔴 [{t['id']}] [{t['project']}] {t['task']} ({age})")


def cmd_clean(args):
    """Archive completed/cancelled items older than 30 days"""
    data = load_todos()
    cutoff = datetime.now(timezone.utc) - timedelta(days=30)
    keep = []
    archived = []
    for t in data["todos"]:
        if t["status"] in ("done", "cancelled"):
            updated = datetime.fromisoformat(t["updated"])
            if updated < cutoff:
                archived.append(t)
                continue
        keep.append(t)

    data["todos"] = keep
    data.setdefault("archived", []).extend(archived)
    save_todos(data)
    print(f"🗂️  Archived {len(archived)} completed/cancelled items older than 30 days")


def _age_str(iso_str):
    created = datetime.fromisoformat(iso_str)
    delta = datetime.now(timezone.utc) - created
    if delta.days == 0:
        hours = delta.seconds // 3600
        return f"{hours}h ago" if hours > 0 else "just now"
    elif delta.days == 1:
        return "yesterday"
    else:
        return f"{delta.days}d ago"


def main():
    parser = argparse.ArgumentParser(description="Echo TODO Manager")
    sub = parser.add_subparsers(dest="command")

    # add
    p_add = sub.add_parser("add", help="Add a new TODO")
    p_add.add_argument("task", help="Task description")
    p_add.add_argument("--priority", choices=PRIORITIES, default="medium")
    p_add.add_argument("--project", help="Project/app name")
    p_add.add_argument("--note", help="Additional notes")

    # list
    p_list = sub.add_parser("list", help="List TODOs")
    p_list.add_argument("--status", choices=STATUSES)
    p_list.add_argument("--project")
    p_list.add_argument("--priority", choices=PRIORITIES)

    # done
    p_done = sub.add_parser("done", help="Mark a TODO as done")
    p_done.add_argument("id")

    # cancel
    p_cancel = sub.add_parser("cancel", help="Cancel a TODO")
    p_cancel.add_argument("id")

    # update
    p_update = sub.add_parser("update", help="Update a TODO")
    p_update.add_argument("id")
    p_update.add_argument("--note")
    p_update.add_argument("--priority", choices=PRIORITIES)
    p_update.add_argument("--status", choices=STATUSES)
    p_update.add_argument("--project")

    # report
    sub.add_parser("report", help="Print markdown TODO report")

    # overdue
    sub.add_parser("overdue", help="Show overdue TODOs (>7 days open)")

    # clean
    sub.add_parser("clean", help="Archive completed items >30 days old")

    args = parser.parse_args()

    cmds = {
        "add": cmd_add,
        "list": cmd_list,
        "done": cmd_done,
        "cancel": cmd_cancel,
        "update": cmd_update,
        "report": cmd_report,
        "overdue": cmd_overdue,
        "clean": cmd_clean,
    }

    if args.command in cmds:
        cmds[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
