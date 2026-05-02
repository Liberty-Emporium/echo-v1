#!/usr/bin/env python3
"""
read-notes-from-dashboard.py — Echo reads Jay's notes from EcDash at session start.

Prints notes Jay left for Echo since last boot.
Called by bootstrap.sh so Echo sees Jay's messages first thing.

Usage:
    python3 echo-v1/scripts/read-notes-from-dashboard.py
"""

import os
import sys
import json
import urllib.request
import urllib.error
import datetime

ECDASH_URL = "https://jay-portfolio-production.up.railway.app"
TOKEN_FILE = "/root/.secrets/brain_sync_token"
# Track which notes we've already seen
SEEN_FILE  = "/root/.openclaw/workspace/echo-v1/memory/.notes-seen.json"


def load_token():
    if os.path.exists(TOKEN_FILE):
        return open(TOKEN_FILE).read().strip()
    return os.environ.get("BRAIN_SYNC_TOKEN", "")


def load_seen():
    if os.path.exists(SEEN_FILE):
        try:
            return set(json.load(open(SEEN_FILE)))
        except:
            pass
    return set()


def save_seen(seen_ids):
    os.makedirs(os.path.dirname(SEEN_FILE), exist_ok=True)
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen_ids), f)


def fetch_jay_notes(token):
    """Fetch Jay's notes via Echo-auth endpoint."""
    req = urllib.request.Request(
        f"{ECDASH_URL}/api/notes/echo-read",
        headers={"X-Brain-Sync-Token": token},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            # Endpoint not yet deployed — silently skip
            return []
        raise


def main():
    token = load_token()
    if not token:
        print("  ⚠️  No brain sync token — skipping notes read")
        return

    try:
        notes = fetch_jay_notes(token)
    except Exception as e:
        print(f"  ⚠️  Could not read notes from EcDash: {e}")
        return

    if not notes:
        print("  📭 No notes from Jay")
        return

    seen = load_seen()
    new_notes = [n for n in notes if str(n.get("id")) not in seen]

    if not new_notes:
        print(f"  📝 {len(notes)} note(s) in dashboard — none new since last boot")
        return

    print(f"\n  ╔══════════════════════════════════════════════════╗")
    print(f"  ║  📝 {len(new_notes)} NEW NOTE(S) FROM JAY              ║")
    print(f"  ╚══════════════════════════════════════════════════╝")
    for n in new_notes:
        ts = n.get("created", "")[:16].replace("T", " ")
        pinned = "📌 " if n.get("pinned") else ""
        print(f"\n  {pinned}[{ts}]")
        for line in n["text"].split("\n"):
            print(f"    {line}")
    print()

    # Mark as seen
    seen.update(str(n["id"]) for n in new_notes)
    save_seen(seen)


if __name__ == "__main__":
    main()
