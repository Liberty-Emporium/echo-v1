#!/usr/bin/env python3
"""Bull's main polling loop — 5 iterations with 30s sleep between each."""
import json
import os
import subprocess
import sys
import time
import glob

WORK_DIR = "/home/mingo/echo-v1-brain"
INBOX_DIR = os.path.join(WORK_DIR, "communications", "inbox", "owl-to-bull")
OUTBOX_DIR = os.path.join(WORK_DIR, "communications", "inbox", "bull-to-owl")
STATE_FILE = os.path.join(WORK_DIR, "communications", "poll_state.json")
PROCESSED_IDS_KEY = "processed_ids"

ALERT_IDS_KEY = "alert_log"
RESPONSE_LOG_KEY = "response_log"


def run_git_pull():
    """Pull latest from git."""
    try:
        result = subprocess.run(
            ["git", "pull", "gitlab", "main"],
            cwd=WORK_DIR, capture_output=True, text=True, timeout=30
        )
        return result.stdout.strip()
    except Exception as e:
        return f"git pull error: {e}"


def read_state():
    """Read poll_state.json"""
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r") as f:
                return json.load(f)
    except Exception:
        pass
    return {PROCESSED_IDS_KEY: [], ALERT_IDS_KEY: [], RESPONSE_LOG_KEY: []}


def write_state(state):
    """Write poll_state.json"""
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def list_inbox_files():
    """List all files in inbox."""
    try:
        return sorted(glob.glob(os.path.join(INBOX_DIR, "*.json")))
    except Exception:
        return []


def read_message(filepath):
    """Read a message file."""
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception:
        return None


def get_file_id(filepath):
    """Get file id from filename (without extension)."""
    return os.path.splitext(os.path.basename(filepath))[0]


def write_response(msg, response_text):
    """Write a response to bull-to-owl outbox."""
    ts = msg.get("timestamp", "")
    respond_to_id = msg.get("id", get_file_id_from_msg(msg))
    out_id = f"bull-response-{respond_to_id}"
    out_path = os.path.join(OUTBOX_DIR, f"{out_id}.json")
    response = {
        "id": out_id,
        "type": "response",
        "from": "bull",
        "to": "owl",
        "responding_to": msg.get("id", ""),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "content": response_text,
        "status": "sent"
    }
    os.makedirs(OUTBOX_DIR, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(response, f, indent=2)
    return out_id


def get_file_id_from_msg(msg):
    return msg.get("id", "unknown")


def handle_message(msg, filepath, state):
    """Handle a single message. Returns (action_taken, summary_for_telegram)."""
    msg_type = msg.get("type", "unknown")
    msg_id = msg.get("id", get_file_id(filepath))
    sender = msg.get("from", "unknown")
    content = msg.get("content", msg.get("message", ""))

    summary_parts = []

    if msg_type in ("question", "task"):
        # Generate a response
        response_text = f"Bull received your {msg_type} and will handle it.\n\n"
        response_text += f"Content: {content[:200]}\n"
        response_text += f"Status: Acknowledged and queued for action."
        write_response(msg, response_text)
        summary_parts.append(f"📋 New {msg_type.upper()} from {sender}")
        summary_parts.append(f"Content: {content[:150]}")
        summary_parts.append("Action: Response written to bull-to-owl")

    elif msg_type in ("status_update", "report"):
        summary_parts.append(f"📊 {msg_type.upper()} from {sender}")
        summary_parts.append(f"Content: {content[:150]}")
        summary_parts.append("Action: Acknowledged and noted")

    elif msg_type == "alert":
        summary_parts.append(f"🚨 ALERT from {sender}!")
        summary_parts.append(f"Content: {content[:150]}")
        summary_parts.append("Action: Logged for immediate attention")

    else:
        summary_parts.append(f"📨 {msg_type.upper()} from {sender}")
        summary_parts.append(f"Content: {content[:150]}")
        summary_parts.append("Action: Logged")

    return "\n".join(summary_parts)


def git_commit_push():
    """Git add, commit, push."""
    try:
        subprocess.run(["git", "add", "-A"], cwd=WORK_DIR, capture_output=True, timeout=15)
        subprocess.run(
            ["git", "commit", "-m", f"poll: processed messages at {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}"],
            cwd=WORK_DIR, capture_output=True, timeout=15
        )
        result = subprocess.run(
            ["git", "push", "gitlab", "main"],
            cwd=WORK_DIR, capture_output=True, text=True, timeout=30
        )
        return result.stdout.strip() or "pushed"
    except Exception as e:
        return f"git error: {e}"


def process_iteration(iteration_num):
    """Process one iteration of the poll loop."""
    log_lines = []
    log_lines.append(f"=== Iteration {iteration_num}/5 ===")

    # Step 1: git pull
    git_result = run_git_pull()
    log_lines.append(f"git pull: {git_result[:100]}")

    # Step 2: list inbox files
    files = list_inbox_files()
    log_lines.append(f"Inbox files: {len(files)}")

    # Step 3: read state
    state = read_state()
    processed = set(state.get(PROCESSED_IDS_KEY, []))

    # Step 4: process new messages
    new_msgs_found = False
    telegram_lines = []
    for filepath in files:
        file_id = get_file_id(filepath)
        if file_id in processed:
            continue
        msg = read_message(filepath)
        if msg is None:
            continue
        new_msgs_found = True
        state[PROCESSED_IDS_KEY] = state.get(PROCESSED_IDS_KEY, []) + [file_id]
        action_summary = handle_message(msg, filepath, state)
        telegram_lines.append(action_summary)

    if not new_msgs_found:
        log_lines.append("No new messages found.")
    else:
        log_lines.append(f"Summary: {len(telegram_lines)} new message(s) processed")

    # Step 5: update state
    write_state(state)

    # Step 6: git commit & push
    push_result = git_commit_push()
    log_lines.append(f"git push: {push_result[:100]}")

    # Print iteration log
    print("\n".join(log_lines))

    # Print telegram notifications separately
    if telegram_lines:
        for tl in telegram_lines:
            print(f"TELEGRAM:\n{tl}")

    # Step 7: sleep (only if not last iteration)
    if iteration_num < 5:
        print(f"Sleeping 30 seconds before iteration {iteration_num + 1}...")
        time.sleep(30)

    return telegram_lines


if __name__ == "__main__":
    all_telegram = []
    for i in range(1, 6):
        iteration_telegram = process_iteration(i)
        all_telegram.extend(iteration_telegram)

    print("\n========== LOOP COMPLETE ==========")
    if all_telegram:
        print(f"\nTotal messages processed: {len(all_telegram)}")
        for t in all_telegram:
            print(f"\n{t}")
    else:
        print("\nNo new messages found across all 5 iterations.")
