#!/usr/bin/env python3
"""
ecdash_poll.py — Echo's EcDash heartbeat poller
Run during heartbeat to get full operational picture from EcDash in one call.

Usage:
    python3 /root/.openclaw/workspace/echo-v1/scripts/ecdash_poll.py
    python3 /root/.openclaw/workspace/echo-v1/scripts/ecdash_poll.py --complete-task <id> "Task completed: ..."
"""

import json
import sys
import urllib.request
import urllib.error
import os

ECDASH_URL   = "https://jay-portfolio-production.up.railway.app"
TOKEN_FILE   = "/root/.secrets/ecdash_token"

def _token():
    with open(TOKEN_FILE) as f:
        return f.read().strip()

def _headers():
    return {
        "Authorization": f"Bearer {_token()}",
        "Content-Type":  "application/json",
    }

def get_summary():
    """Fetch /api/echo/summary — full operational picture."""
    req = urllib.request.Request(
        f"{ECDASH_URL}/api/echo/summary",
        headers=_headers(),
        method="GET"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.read().decode()[:200]}"}
    except Exception as e:
        return {"error": str(e)}

def complete_task(task_id, response_text, status="done"):
    """PATCH /api/echo-bridge/<id> to mark a task complete."""
    payload = json.dumps({"status": status, "response": response_text}).encode()
    req = urllib.request.Request(
        f"{ECDASH_URL}/api/echo-bridge/{task_id}",
        data=payload,
        headers=_headers(),
        method="PATCH"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        return {"error": str(e)}

def post_note(text, pinned=False):
    """POST a note from Echo to EcDash (visible in Jay's dashboard)."""
    payload = json.dumps({"text": text, "pinned": pinned}).encode()
    req = urllib.request.Request(
        f"{ECDASH_URL}/api/notes/echo",
        data=payload,
        headers=_headers(),
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        return {"error": str(e)}

def get_pending_tasks():
    """Fetch pending/queued tasks from echo-bridge."""
    req = urllib.request.Request(
        f"{ECDASH_URL}/api/echo-bridge",
        headers=_headers(),
        method="GET"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            tasks = json.loads(r.read().decode())
            return [t for t in tasks if t.get("status") in ("pending", "queued")]
    except Exception as e:
        return []

if __name__ == "__main__":
    args = sys.argv[1:]

    if args and args[0] == "--complete-task" and len(args) >= 3:
        task_id   = int(args[1])
        response  = args[2]
        status    = args[3] if len(args) > 3 else "done"
        result    = complete_task(task_id, response, status)
        print(json.dumps(result, indent=2))

    elif args and args[0] == "--post-note":
        text   = args[1] if len(args) > 1 else "Echo checked in."
        pinned = "--pin" in args
        result = post_note(text, pinned)
        print(json.dumps(result, indent=2))

    else:
        # Default: print full summary
        summary = get_summary()
        if "error" in summary:
            print(f"ERROR: {summary['error']}", file=sys.stderr)
            sys.exit(1)

        print(f"=== EcDash Summary @ {summary.get('checked_at', 'unknown')} ===")

        alerts = summary.get("alerts", [])
        if alerts:
            print("\n🚨 ALERTS:")
            for a in alerts:
                print(f"  {a}")
        else:
            print("\n✅ No alerts — all clear")

        pending = summary.get("pending_tasks", [])
        if pending:
            print(f"\n📋 PENDING TASKS ({len(pending)}):")
            for t in pending:
                print(f"  [{t['id']}] {t['task'][:100]}")

        down = summary.get("down_apps", [])
        if down:
            print(f"\n⬇️  DOWN APPS: {', '.join(down)}")

        errors = summary.get("recent_errors", [])
        if errors:
            print(f"\n🔴 RECENT ERRORS ({len(errors)}):")
            for e in errors[:5]:
                print(f"  {e.get('app')} {e.get('route')} — {e.get('error','')[:80]}")

        notes = summary.get("jay_notes", [])
        if notes:
            print(f"\n📝 JAY'S NOTES ({len(notes)}):")
            for n in notes[:3]:
                print(f"  [{n.get('created','')[:16]}] {n.get('text','')[:120]}")

        todos = summary.get("open_todos", [])
        if todos:
            print(f"\n✅ OPEN TODOS ({len(todos)}): {', '.join(t.get('text','')[:40] for t in todos[:3])}...")
