#!/usr/bin/env python3
"""Quick comms sync script for OWL-Bull communication."""
import json, datetime, os

INBOX_BULL_TO_OWL = "/home/lol/Desktop/openclaw/echo-v1/communications/inbox/bull-to-owl"
INBOX_OWL_TO_BULL = "/home/lol/Desktop/openclaw/echo-v1/comments/inbox/owl-to-bull"
POLL_STATE = "/home/lol/Desktop/openclaw/echo-v1/communications/poll_state.json"

def get_timestamp():
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H%M%SZ")

def write_owl_message(msg_body, msg_type="response", priority="normal", subject="RE: Bull message"):
    ts = get_timestamp()
    filename = f"owl-{msg_type}-{ts}.json"
    filepath = os.path.join(INBOX_OWL_TO_BULL, filename)
    msg = {
        "protocol": "1.0",
        "id": f"owl-{msg_type}-{ts}",
        "from": "owl",
        "to": "bull",
        "type": msg_type,
        "subject": subject,
        "body": msg_body,
        "priority": priority,
        "status": "sent",
        "reply_to": None,
        "attachments": [],
        "metadata": {"app": "echo-v1", "tags": ["owl", msg_type]},
        "created": datetime.datetime.utcnow().isoformat() + "+00:00"
    }
    os.makedirs(INBOX_OWL_TO_BULL, exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(msg, f, indent=2)
    print(f"Written: {filepath}")
    return filepath

if __name__ == "__main__":
    import sys
    msg_type = sys.argv[1] if len(sys.argv) > 1 else "response"
    subject = sys.argv[2] if len(sys.argv) > 2 else "RE: Bull message"
    body = sys.argv[3] if len(sys.argv) > 3 else "OWL checking in."
    write_owl_message(body, msg_type, "normal", subject)
