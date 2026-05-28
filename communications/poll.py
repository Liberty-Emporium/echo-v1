#!/usr/bin/env python3
"""
Message bus poller — runs as a cron job on both sides.
Checks for new messages and triggers appropriate actions.
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent.parent
COMM_DIR = REPO_DIR / "communications"
INBOX_DIR = COMM_DIR / "inbox"
AGENT_NAME = os.environ.get("AGENT_NAME", "self")

AGENT_MAP = {
    "self": {"inbox": "self-to-owl", "outbox": "owl-to-self"},
    "owl": {"inbox": "owl-to-self", "outbox": "self-to-owl"},
    "kiloclaw": {"inbox": "kiloclaw-to-owl", "outbox": "owl-to-kiloclaw"},
}


def log(msg):
    ts = datetime.now(timezone.utc).isoformat()
    print(f"[{ts}] [{AGENT_NAME}] {msg}")


def git_pull():
    try:
        result = subprocess.run(
            ["git", "-C", str(REPO_DIR), "pull", "--quiet"],
            capture_output=True, timeout=30
        )
        return result.returncode == 0
    except Exception as e:
        log(f"git pull failed: {e}")
        return False


def git_commit_push(message):
    try:
        subprocess.run(["git", "-C", str(REPO_DIR), "add", "communications/"], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(REPO_DIR), "commit", "-m", message, "--quiet"], capture_output=True, timeout=30)
        subprocess.run(["git", "-C", str(REPO_DIR), "push", "--quiet"], capture_output=True, timeout=30)
    except Exception:
        pass


def get_my_inbox():
    mapping = AGENT_MAP.get(AGENT_NAME, AGENT_MAP["self"])
    return INBOX_DIR / mapping["inbox"]


def process_message(filepath):
    """Process a single incoming message."""
    with open(filepath) as f:
        msg = json.load(f)

    msg_type = msg.get("type", "")
    subject = msg.get("subject", "")
    from_agent = msg.get("from", "")
    priority = msg.get("priority", "medium")
    msg_id = msg.get("id", "")[:8]

    log(f"Processing [{msg_type}] from {from_agent}: {subject} (priority: {priority})")

    # Update status to acknowledged
    msg["status"] = "acknowledged"
    msg["updated"] = datetime.now(timezone.utc).isoformat()
    with open(filepath, "w") as f:
        json.dump(msg, f, indent=2)
    git_commit_push(f"[{AGENT_NAME}] acknowledged: {subject}")

    return msg


def main():
    log("Starting poll...")

    if not git_pull():
        log("Failed to pull — aborting poll")
        sys.exit(1)

    inbox = get_my_inbox()
    if not inbox.exists():
        log("Inbox directory doesn't exist — nothing to do")
        return

    unread = []
    for f in sorted(inbox.glob("*.json")):
        try:
            msg = json.load(open(f))
            if msg.get("status") in ("pending", "in_progress"):
                unread.append((f, msg))
        except Exception as e:
            log(f"Error reading {f.name}: {e}")

    if not unread:
        log("No new messages")
        return

    log(f"Found {len(unread)} unread message(s)")
    for filepath, msg in unread:
        process_message(filepath)

    log("Poll complete")


if __name__ == "__main__":
    main()
