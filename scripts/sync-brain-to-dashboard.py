#!/usr/bin/env python3
"""
sync-brain-to-dashboard.py — Push Echo's brain files to EcDash
so Jay can see what Echo knows at jay-portfolio-production.up.railway.app/dashboard

Files synced: MEMORY.md, SOUL.md, IDENTITY.md
Run at bootstrap and end of session.

Usage:
    python3 echo-v1/scripts/sync-brain-to-dashboard.py
"""

import os
import sys
import json
import urllib.request
import urllib.error

ECDASH_URL     = "https://jay-portfolio-production.up.railway.app"
TOKEN_FILE     = "/root/.secrets/brain_sync_token"
BRAIN_DIR      = "/root/.openclaw/workspace/echo-v1"

FILES_TO_SYNC  = ["MEMORY.md", "SOUL.md", "IDENTITY.md"]


def load_token():
    if os.path.exists(TOKEN_FILE):
        return open(TOKEN_FILE).read().strip()
    return os.environ.get("BRAIN_SYNC_TOKEN", "")


def read_file(filename):
    path = os.path.join(BRAIN_DIR, filename)
    if os.path.exists(path):
        return open(path, encoding="utf-8").read()
    # fallback: workspace root
    fallback = os.path.join("/root/.openclaw/workspace", filename)
    if os.path.exists(fallback):
        return open(fallback, encoding="utf-8").read()
    return None


def push_brain(token):
    payload = {}
    for fname in FILES_TO_SYNC:
        content = read_file(fname)
        if content is not None:
            payload[fname] = content
            print(f"  📄 {fname}: {len(content)} chars")
        else:
            print(f"  ⚠️  {fname}: not found, skipping")

    if not payload:
        print("  ❌ No brain files found to sync")
        return False

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{ECDASH_URL}/api/brain/sync",
        data=data,
        headers={
            "Content-Type": "application/json",
            "X-Brain-Sync-Token": token,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            if result.get("ok"):
                synced = result.get("synced", [])
                print(f"  ✅ Synced to EcDash: {', '.join(synced)}")
                return True
            else:
                print(f"  ❌ Sync failed: {result}")
                return False
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"  ❌ HTTP {e.code}: {body}")
        return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def main():
    print("🧠 Syncing brain files to EcDash...")

    token = load_token()
    if not token:
        print("  ❌ No BRAIN_SYNC_TOKEN found at /root/.secrets/brain_sync_token")
        print("     Set it with: python3 echo-v1/scripts/bootstrap.sh (will set on Railway)")
        sys.exit(1)

    success = push_brain(token)
    if success:
        print("  ✅ Jay can now see Echo's brain at:")
        print("     https://jay-portfolio-production.up.railway.app/dashboard")
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
