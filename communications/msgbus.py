#!/usr/bin/env python3
"""
OWL-SELF Message Bus Handler v1.0
Reads and writes messages to the shared git-based communication channel.

Usage:
    python3 msgbus send <to> <type> <subject> <body> [--priority high] [--task-id ID]
    python3 msgbus inbox [--agent <name>] [--unread-only]
    python3 msgbus read <message-file>
    python3 msgbus reply <message-file> <body> [--status completed]
    python3 msgbus archive <message-file>
    python3 msgbus poll [--interval 300]
    python3 msgbus status [--task-id ID]

Agents: self, owl, kiloclaw
Types: task_assignment, status_update, report, question, alert, heartbeat
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────────────
REPO_DIR = Path(__file__).resolve().parent.parent  # echo-v1-brain/
COMM_DIR = REPO_DIR / "communications"
INBOX_DIR = COMM_DIR / "inbox"
SENT_DIR = COMM_DIR / "sent"
ARCHIVE_DIR = COMM_DIR / "archive"
PROTOCOL_DIR = COMM_DIR / "protocol"

AGENT_NAME = os.environ.get("AGENT_NAME", "bull")  # Set AGENT_NAME env var per agent
AGENT_MAP = {
    "bull": {"inbox": "bull-to-owl", "outbox": "owl-to-bull"},
    "owl": {"inbox": "owl-to-bull", "outbox": "bull-to-owl"},
    "bullet": {"inbox": "owl-to-bull", "outbox": "bull-to-owl"},
    "self": {"inbox": "owl-to-bull", "outbox": "bull-to-owl"},
}

# ── Helpers ────────────────────────────────────────────────────────────────────

def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")

def now_iso_readable():
    return datetime.now(timezone.utc).isoformat()

def git_pull():
    """Pull latest messages from remote."""
    try:
        subprocess.run(
            ["git", "-C", str(REPO_DIR), "pull", "--quiet"],
            capture_output=True, timeout=30
        )
    except Exception as e:
        print(f"[WARN] git pull failed: {e}", file=sys.stderr)

def git_commit_push(message):
    """Commit and push changes."""
    try:
        subprocess.run(["git", "-C", str(REPO_DIR), "add", "communications/"], check=True, capture_output=True)
        subprocess.run(
            ["git", "-C", str(REPO_DIR), "commit", "-m", message, "--quiet"],
            capture_output=True, timeout=30
        )
        subprocess.run(
            ["git", "-C", str(REPO_DIR), "push", "--quiet"],
            capture_output=True, timeout=30
        )
    except subprocess.CalledProcessError:
        pass  # Nothing to commit is OK
    except Exception as e:
        print(f"[WARN] git push failed: {e}", file=sys.stderr)

def get_inbox_for(agent):
    """Get the inbox directory for a given agent (where others write TO them)."""
    mapping = AGENT_MAP.get(agent, AGENT_MAP["bull"])
    return INBOX_DIR / mapping["inbox"]

def get_outbox_for(agent):
    """Get the outbox directory (where this agent writes TO others)."""
    mapping = AGENT_MAP.get(agent, AGENT_MAP["bull"])
    return INBOX_DIR / mapping["outbox"]

# ── Message Operations ─────────────────────────────────────────────────────────

def create_message(to, msg_type, subject, body, priority="medium", task_id=None, reply_to=None, tags=None, app=None, url=None, commit=None):
    """Create a message dict."""
    msg_id = str(uuid.uuid4())
    ts = now_iso_readable()
    return {
        "protocol": "1.0",
        "id": msg_id,
        "from": AGENT_NAME,
        "to": to,
        "type": msg_type,
        "subject": subject,
        "body": body,
        "priority": priority,
        "status": "pending",
        "task_id": task_id,
        "reply_to": reply_to,
        "attachments": [],
        "metadata": {
            "app": app or "",
            "url": url or "",
            "commit": commit or "",
            "tags": tags or [],
        },
        "created": ts,
        "updated": ts,
    }

def write_message(msg, to_agent):
    """Write a message to the recipient's inbox and sender's sent folder."""
    outbox = get_outbox_for(AGENT_NAME)
    outbox.mkdir(parents=True, exist_ok=True)
    SENT_DIR.mkdir(parents=True, exist_ok=True)

    filename = f"{now_iso()}_{msg['type']}_{msg['id'][:8]}.json"
    filepath = outbox / filename
    sentpath = SENT_DIR / filename

    with open(filepath, "w") as f:
        json.dump(msg, f, indent=2)
    shutil.copy2(filepath, sentpath)

    git_commit_push(f"[{AGENT_NAME}] {msg['type']}: {msg['subject']}")
    return filepath

def read_message(filepath):
    """Read a message from file."""
    with open(filepath) as f:
        return json.load(f)

def update_message_status(filepath, status, body_append=None):
    """Update a message's status and optionally append to body."""
    msg = read_message(filepath)
    msg["status"] = status
    msg["updated"] = now_iso_readable()
    if body_append:
        msg["body"] += f"\n\n[{now_iso()}] UPDATE:\n{body_append}"
    with open(filepath, "w") as f:
        json.dump(msg, f, indent=2)
    git_commit_push(f"[{AGENT_NAME}] status {status}: {msg['subject']}")

def list_inbox(agent=None, unread_only=False):
    """List messages in an agent's inbox."""
    target_agent = agent or AGENT_NAME
    inbox = get_inbox_for(target_agent)
    if not inbox.exists():
        return []

    messages = []
    for f in sorted(inbox.glob("*.json")):
        try:
            msg = read_message(f)
            if unread_only and msg.get("status") not in ("pending", "in_progress"):
                continue
            messages.append((f, msg))
        except (json.JSONDecodeError, KeyError) as e:
            print(f"[WARN] Skipping corrupt message {f.name}: {e}", file=sys.stderr)
    return messages

def archive_message(filepath):
    """Move a processed message to archive."""
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    dest = ARCHIVE_DIR / Path(filepath).name
    shutil.move(str(filepath), str(dest))
    git_commit_push(f"[{AGENT_NAME}] archived: {Path(filepath).name}")

# ── CLI Commands ───────────────────────────────────────────────────────────────

def cmd_send(args):
    """Send a message to another agent."""
    msg = create_message(
        to=args.to,
        msg_type=args.type,
        subject=args.subject,
        body=args.body,
        priority=args.priority,
        task_id=args.task_id,
        tags=args.tags.split(",") if args.tags else [],
        app=args.app,
        url=args.url,
        commit=args.commit,
    )
    filepath = write_message(msg, args.to)
    print(f"[{AGENT_NAME}] Sent {args.type} to {args.to}: {args.subject}")
    print(f"  ID: {msg['id']}")
    print(f"  File: {filepath}")

def cmd_inbox(args):
    """List messages in inbox."""
    git_pull()
    messages = list_inbox(args.agent, args.unread_only)
    if not messages:
        print(f"[{AGENT_NAME}] No messages in inbox.")
        return

    print(f"[{AGENT_NAME}] Inbox ({len(messages)} messages):")
    print("-" * 60)
    for filepath, msg in messages:
        status_icon = {"pending": "📥", "in_progress": "🔄", "completed": "✅", "failed": "❌"}.get(msg["status"], "❓")
        priority_icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢", "info": "ℹ️"}.get(msg.get("priority", ""), "")
        print(f"  {status_icon} {priority_icon} [{msg['type']}] {msg['subject']}")
        print(f"     From: {msg['from']} | Status: {msg['status']} | {msg['created'][:19]}")
        print(f"     File: {filepath.name}")
        if msg.get("task_id"):
            print(f"     Task: {msg['task_id']}")
        print()

def cmd_read(args):
    """Read a specific message."""
    msg = read_message(args.filepath)
    print(f"Message: {msg['subject']}")
    print(f"From: {msg['from']} → To: {msg['to']}")
    print(f"Type: {msg['type']} | Priority: {msg.get('priority', 'n/a')} | Status: {msg['status']}")
    print(f"Created: {msg['created']}")
    if msg.get("task_id"):
        print(f"Task ID: {msg['task_id']}")
    if msg.get("reply_to"):
        print(f"Reply to: {msg['reply_to']}")
    if msg.get("metadata", {}).get("tags"):
        print(f"Tags: {', '.join(msg['metadata']['tags'])}")
    print("-" * 60)
    print(msg["body"])

def cmd_reply(args):
    """Reply to a message."""
    original = read_message(args.filepath)
    msg = create_message(
        to=original["from"],
        msg_type="status_update" if args.status else "question",
        subject=f"Re: {original['subject']}",
        body=args.body,
        priority=original.get("priority", "medium"),
        task_id=original.get("task_id"),
        reply_to=original["id"],
    )
    filepath = write_message(msg, original["from"])
    update_message_status(args.filepath, args.status or "acknowledged")
    print(f"[{AGENT_NAME}] Replied to {original['from']}: {msg['subject']}")

def cmd_archive(args):
    """Archive a message."""
    archive_message(args.filepath)
    print(f"[{AGENT_NAME}] Archived: {Path(args.filepath).name}")

def cmd_poll(args):
    """Continuously poll for new messages."""
    import time
    interval = args.interval
    print(f"[{AGENT_NAME}] Polling every {interval}s. Ctrl+C to stop.")
    while True:
        git_pull()
        messages = list_inbox(unread_only=True)
        for filepath, msg in messages:
            print(f"\n[{AGENT_NAME}] New message: {msg['subject']} (from {msg['from']})")
            print(f"  {msg['body'][:200]}...")
            update_message_status(filepath, "acknowledged")
        time.sleep(interval)

def cmd_status(args):
    """Show status of a task across all messages."""
    task_id = args.task_id
    found = []
    for inbox_dir in INBOX_DIR.iterdir():
        if inbox_dir.is_dir():
            for f in inbox_dir.glob("*.json"):
                try:
                    msg = read_message(f)
                    if msg.get("task_id") == task_id:
                        found.append((f, msg))
                except:
                    pass
    if not found:
        print(f"No messages found for task: {task_id}")
        return
    print(f"Task {task_id} — {len(found)} messages:")
    for filepath, msg in sorted(found, key=lambda x: x[1]["created"]):
        print(f"  [{msg['status']}] {msg['from']} → {msg['to']}: {msg['subject']}")

# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="OWL-SELF Message Bus v1.0")
    sub = parser.add_subparsers(dest="command")

    # send
    p_send = sub.add_parser("send", help="Send a message")
    p_send.add_argument("to", choices=["owl", "self", "kiloclaw"])
    p_send.add_argument("type", choices=["task_assignment", "status_update", "report", "question", "alert", "heartbeat"])
    p_send.add_argument("subject")
    p_send.add_argument("body")
    p_send.add_argument("--priority", default="medium", choices=["critical", "high", "medium", "low", "info"])
    p_send.add_argument("--task-id", default=None)
    p_send.add_argument("--tags", default=None)
    p_send.add_argument("--app", default=None)
    p_send.add_argument("--url", default=None)
    p_send.add_argument("--commit", default=None)

    # inbox
    p_inbox = sub.add_parser("inbox", help="List inbox messages")
    p_inbox.add_argument("--agent", default=None, help="Agent name (default: AGENT_NAME env var)")
    p_inbox.add_argument("--unread-only", action="store_true")

    # read
    p_read = sub.add_parser("read", help="Read a message")
    p_read.add_argument("filepath")

    # reply
    p_reply = sub.add_parser("reply", help="Reply to a message")
    p_reply.add_argument("filepath")
    p_reply.add_argument("body")
    p_reply.add_argument("--status", default=None, choices=["acknowledged", "in_progress", "completed", "failed"])

    # archive
    p_archive = sub.add_parser("archive", help="Archive a message")
    p_archive.add_argument("filepath")

    # poll
    p_poll = sub.add_parser("poll", help="Poll for new messages")
    p_poll.add_argument("--interval", type=int, default=300)

    # status
    p_status = sub.add_parser("status", help="Show task status")
    p_status.add_argument("--task-id", required=True)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "send": cmd_send,
        "inbox": cmd_inbox,
        "read": cmd_read,
        "reply": cmd_reply,
        "archive": cmd_archive,
        "poll": cmd_poll,
        "status": cmd_status,
    }
    commands[args.command](args)

if __name__ == "__main__":
    main()
