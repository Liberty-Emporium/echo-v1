#!/usr/bin/env python3
"""
msgbus_fast.py — Fast file-based message bus for OWL ↔ Bull communication.
Uses shared directory on local filesystem (or Tailscale FUSE mount).
No git push/pull needed — messages are instant.

Usage:
  python3 msgbus_fast.py send <to> <type> <subject> <body>
  python3 msgbus_fast.py inbox [--unread-only]
  python3 msgbus_fast.py mark-read <message-id>
  python3 msgbus_fast.py status

Protocol:
  - Messages are JSON files in shared/communications/inbox/
  - Filename: <timestamp>_<from>-to-<>_<type>_<id>.json
  - read_status field: "unread" | "read"
"""

import json
import sys
import os
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
AGENT_NAME = os.environ.get("AGENT_NAME", "owl").lower()
SHARED_DIR = Path("/home/lol/Desktop/openclaw/shared/communications")
INBOX_DIR = SHARED_DIR / "inbox"
SENT_DIR = SHARED_DIR / "sent"

# Auto-create dirs
for d in [INBOX_DIR / "owl-to-bull", INBOX_DIR / "bull-to-owl", SENT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ── Helpers ───────────────────────────────────────────────────────────────────

def now_iso():
    return datetime.now(timezone.utc).isoformat()

def make_filename(direction, msg_type, msg_id):
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{ts}_{direction}_{msg_type}_{msg_id[:8]}.json"

def get_inbox_for(agent):
    """Return the inbox directory where this agent reads messages."""
    if agent == "owl":
        return INBOX_DIR / "bull-to-owl"
    elif agent == "bull":
        return INBOX_DIR / "owl-to-bull"
    else:
        return INBOX_DIR / f"other-to-{agent}"

def get_outbox_for(agent):
    """Return the outbox directory where this agent writes messages."""
    if agent == "owl":
        return INBOX_DIR / "owl-to-bull"
    elif agent == "bull":
        return INBOX_DIR / "bull-to-owl"
    else:
        return INBOX_DIR / f"{agent}-to-other"

# ── Commands ──────────────────────────────────────────────────────────────────

def send_message(to, msg_type, subject, body):
    msg_id = str(uuid.uuid4())
    direction = f"{AGENT_NAME}-to-{to}"
    filename = make_filename(direction, msg_type, msg_id)
    outbox = get_outbox_for(AGENT_NAME)
    
    message = {
        "protocol": "2.0-file",
        "id": msg_id,
        "from": AGENT_NAME,
        "to": to,
        "type": msg_type,
        "subject": subject,
        "body": body,
        "status": "sent",
        "read_status": "unread",
        "created": now_iso(),
        "replies_to": None,
    }
    
    # Check for reply_to from stdin or args
    if "--reply-to" in sys.argv:
        idx = sys.argv.index("--reply-to")
        if idx + 1 < len(sys.argv):
            message["replies_to"] = sys.argv[idx + 1]
    
    filepath = outbox / filename
    with open(filepath, "w") as f:
        json.dump(message, f, indent=2)
    
    # Also write a symlink in sent for our own records
    sent_link = SENT_DIR / filename
    if not sent_link.exists():
        os.symlink(filepath, sent_link)
    
    print(f"✅ Message sent: {msg_id[:8]} → {to}")
    print(f"   Subject: {subject}")
    print(f"   File: {filepath}")
    return msg_id

def read_inbox(unread_only=True):
    inbox = get_inbox_for(AGENT_NAME)
    files = sorted(inbox.glob("*.json"))
    
    if not files:
        print(f"📭 No messages in inbox for {AGENT_NAME}")
        return []
    
    messages = []
    for f in files:
        try:
            with open(f) as fh:
                msg = json.load(fh)
            if unread_only and msg.get("read_status") == "read":
                continue
            messages.append((f, msg))
        except (json.JSONDecodeError, IOError):
            continue
    
    if not messages:
        print(f"📭 No unread messages for {AGENT_NAME}")
        return []
    
    print(f"📬 {len(messages)} unread message(s) for {AGENT_NAME}:\n")
    for filepath, msg in messages:
        print(f"  [{msg['id'][:8]}] {msg['from']} → {msg['to']} | {msg['type']}")
        print(f"    Subject: {msg['subject']}")
        print(f"    Time: {msg['created']}")
        # Print first 3 lines of body
        body_lines = msg['body'].strip().split('\n')[:3]
        for line in body_lines:
            print(f"    {line[:80]}")
        if len(msg['body'].split('\n')) > 3:
            print(f"    ...")
        print(f"    File: {filepath}")
        print()
    
    return messages

def mark_read(message_id):
    inbox = get_inbox_for(AGENT_NAME)
    for f in inbox.glob("*.json"):
        try:
            with open(f) as fh:
                msg = json.load(fh)
            if msg["id"].startswith(message_id) or msg["id"] == message_id:
                msg["read_status"] = "read"
                msg["read_at"] = now_iso()
                with open(f, "w") as fh:
                    json.dump(msg, fh, indent=2)
                print(f"✅ Marked as read: {msg['id'][:8]}")
                return True
        except (json.JSONDecodeError, IOError):
            continue
    print(f"❌ Message not found: {message_id}")
    return False

def show_status():
    my_inbox = get_inbox_for(AGENT_NAME)
    my_outbox = get_outbox_for(AGENT_NAME)
    
    inbox_files = list(my_inbox.glob("*.json"))
    outbox_files = list(my_outbox.glob("*.json"))
    unread = sum(1 for f in inbox_files if json.load(open(f)).get("read_status") == "unread")
    
    print(f"📊 Message Bus Status for {AGENT_NAME}:")
    print(f"   Inbox:  {len(inbox_files)} total, {unread} unread")
    print(f"   Outbox: {outbox_files} sent")
    print(f"   Inbox dir:  {my_inbox}")
    print(f"   Outbox dir: {my_outbox}")
    print(f"   Agent: {AGENT_NAME}")

# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "send" and len(sys.argv) >= 5:
        to = sys.argv[2]
        msg_type = sys.argv[3]
        subject = sys.argv[4]
        body = sys.argv[5] if len(sys.argv) > 5 else ""
        send_message(to, msg_type, subject, body)
    elif cmd == "inbox":
        unread_only = "--all" not in sys.argv
        read_inbox(unread_only=unread_only)
    elif cmd == "mark-read" and len(sys.argv) >= 3:
        mark_read(sys.argv[2])
    elif cmd == "status":
        show_status()
    else:
        print(__doc__)
        sys.exit(1)
