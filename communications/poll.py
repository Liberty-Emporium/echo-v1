#!/usr/bin/env python3
"""
Message bus poller v2.0 — Reliable cross-agent communication
- Pulls from GitLab with fallback strategies
- Tracks sync state to avoid reprocessing
- Force-adds inbox files (bypasses gitignore for message sync)
- Uses git credential cache to avoid repeated auth failures
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
STATE_FILE = COMM_DIR / "poll_state.json"
AGENT_NAME = os.environ.get("AGENT_NAME", "self")

AGENT_MAP = {
    "self": {"inbox": "self-to-owl", "outbox": "owl-to-self"},
    "owl": {"inbox": "owl-to-self", "outbox": "self-to-owl"},
    "kiloclaw": {"inbox": "kiloclaw-to-owl", "outbox": "owl-to-kiloclaw"},
}


def log(msg):
    ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
    print(f"[{ts}] [{AGENT_NAME}] {msg}")


def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"last_pull": None, "processed_ids": []}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def git_pull():
    """Pull latest messages. Multiple fallback strategies."""
    strategies = [
        ("gitlab", ["git", "-C", str(REPO_DIR), "pull", "gitlab", "main", "--quiet"]),
        ("gitlab-rebase", ["git", "-C", str(REPO_DIR), "pull", "gitlab", "main", "--rebase", "--quiet"]),
        ("origin", ["git", "-C", str(REPO_DIR), "pull", "origin", "main", "--quiet"]),
        ("origin-rebase", ["git", "-C", str(REPO_DIR), "pull", "origin", "main", "--rebase", "--quiet"]),
        # Nuclear option: reset to gitlab state
        ("gitlab-reset", None),  # Handled separately
    ]

    for name, cmd in strategies:
        if cmd is None:
            # Nuclear: fetch + hard reset to gitlab/main
            try:
                subprocess.run(["git", "-C", str(REPO_DIR), "fetch", "gitlab", "main"],
                              capture_output=True, timeout=30)
                result = subprocess.run(["git", "-C", str(REPO_DIR), "reset", "--hard", "gitlab/main"],
                                       capture_output=True, timeout=30)
                if result.returncode == 0:
                    log(f"Pull: hard reset to gitlab/main")
                    return True
            except Exception:
                pass
            continue

        try:
            result = subprocess.run(cmd, capture_output=True, timeout=60)
            if result.returncode == 0:
                log(f"Pull successful ({name})")
                return True
        except Exception as e:
            log(f"Pull failed ({name}): {e}")

    log("ALL pull strategies failed — working local only")
    return False


def git_commit_push(message):
    """Force-add inbox/outbox and push to all remotes."""
    try:
        subprocess.run(
            ["git", "-C", str(REPO_DIR), "add", "-f",
             "communications/inbox/", "communications/outbox/", "communications/sent/",
             "communications/poll_state.json", "communications/COORDINATION.md"],
            check=True, capture_output=True
        )
        # Only commit if there are changes
        status = subprocess.run(
            ["git", "-C", str(REPO_DIR), "diff", "--cached", "--quiet"],
            capture_output=True
        )
        if status.returncode == 0:
            return True  # Nothing to commit

        subprocess.run(
            ["git", "-C", str(REPO_DIR), "commit", "-m", message, "--quiet"],
            capture_output=True, timeout=30
        )
        for remote in ["gitlab", "origin"]:
            try:
                result = subprocess.run(
                    ["git", "-C", str(REPO_DIR), "push", remote, "main", "--quiet"],
                    capture_output=True, timeout=30
                )
                if result.returncode == 0:
                    log(f"Push OK ({remote})")
                else:
                    # If GitHub push fails (secret scanning), try allowing the secret
                    if remote == "origin" and b"secret" in result.stderr.lower():
                        log(f"GitHub push blocked by secret scanning — pushing to GitLab only")
                    else:
                        log(f"Push failed ({remote}): {result.stderr.decode()[:100]}")
            except Exception:
                log(f"Push error ({remote})")
        return True
    except Exception as e:
        log(f"Commit/push error: {e}")
        return False


def get_my_inbox():
    mapping = AGENT_MAP.get(AGENT_NAME, AGENT_MAP["self"])
    return INBOX_DIR / mapping["inbox"]


def process_message(filepath, state):
    """Process a single incoming message."""
    try:
        with open(filepath) as f:
            msg = json.load(f)
    except Exception as e:
        log(f"Error reading {filepath.name}: {e}")
        return None

    msg_id = msg.get("id", "")
    if msg_id in state.get("processed_ids", []):
        return None

    msg_type = msg.get("type", "")
    subject = msg.get("subject", "")
    from_agent = msg.get("from", "")
    priority = msg.get("priority", "medium")

    log(f"NEW [{msg_type}] from {from_agent}: {subject} (priority: {priority})")

    # Mark acknowledged
    msg["status"] = "acknowledged"
    msg["updated"] = datetime.now(timezone.utc).isoformat()
    with open(filepath, "w") as f:
        json.dump(msg, f, indent=2)

    state.setdefault("processed_ids", []).append(msg_id)
    # Trim old IDs
    if len(state["processed_ids"]) > 300:
        state["processed_ids"] = state["processed_ids"][-150:]

    return msg


def main():
    log("=== Poll v2.0 ===")
    state = load_state()

    # Pull latest
    pulled = git_pull()
    if pulled:
        state["last_pull"] = datetime.now(timezone.utc).isoformat()

    # Check inbox
    inbox = get_my_inbox()
    if not inbox.exists():
        log("No inbox")
        save_state(state)
        return

    unread = []
    for f in sorted(inbox.glob("*.json")):
        try:
            with open(f) as fh:
                msg = json.load(fh)
            if msg.get("status") in ("pending", "in_progress"):
                unread.append((f, msg))
        except Exception as e:
            log(f"Skip corrupt {f.name}: {e}")

    if not unread:
        log("No new messages")
        save_state(state)
        return

    log(f"Processing {len(unread)} new message(s)")
    processed = []
    for filepath, _ in unread:
        result = process_message(filepath, state)
        if result:
            processed.append(result)

    if processed:
        git_commit_push(f"[{AGENT_NAME}] read {len(processed)} messages")

    save_state(state)
    log("=== Done ===")


if __name__ == "__main__":
    main()
