#!/usr/bin/env python3
"""
widget-brain-push.py — Push Echo's updated brain back to AI Agent Widget.

Pushes IDENTITY.md, SOUL.md, MEMORY.md back to the Widget after a session
so the Widget stays in sync with what Echo learned.

Usage:
    python3 echo-v1/scripts/widget-brain-push.py

Config:
    /root/.secrets/widget_agent_id  — Echo's agent ID in the Widget
    /root/.secrets/willie_api_key   — Echo's api_key (auth token for brain/update)
"""

import os, sys, json, urllib.request, urllib.error

WIDGET_URL     = "https://ai-agent-widget-production.up.railway.app"
AGENT_ID_FILE  = "/root/.secrets/widget_agent_id"
API_KEY_FILE   = "/root/.secrets/willie_api_key"
BRAIN_DIR      = "/root/.openclaw/workspace/echo-v1"
WORKSPACE_DIR  = "/root/.openclaw/workspace"


def load_config():
    agent_id = open(AGENT_ID_FILE).read().strip() if os.path.exists(AGENT_ID_FILE) else ""
    api_key  = open(API_KEY_FILE).read().strip()  if os.path.exists(API_KEY_FILE)  else ""
    agent_id = agent_id or os.environ.get("WIDGET_AGENT_ID", "")
    api_key  = api_key  or os.environ.get("WILLIE_API_KEY", "")
    return agent_id, api_key


def read_file(filename):
    for base in [BRAIN_DIR, WORKSPACE_DIR]:
        path = os.path.join(base, filename)
        if os.path.exists(path):
            return open(path, encoding="utf-8").read().strip()
    return ""


def push_brain(agent_id, api_key):
    identity_md = read_file("IDENTITY.md")
    soul_md     = read_file("SOUL.md")
    memory_md   = read_file("MEMORY.md")

    print(f"  📄 IDENTITY.md: {len(identity_md)} chars")
    print(f"  📄 SOUL.md:     {len(soul_md)} chars")
    print(f"  📄 MEMORY.md:   {len(memory_md)} chars")

    payload = json.dumps({
        "token":       api_key,
        "identity_md": identity_md,
        "soul_md":     soul_md,
        "memory_md":   memory_md,
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{WIDGET_URL}/agent/{agent_id}/brain/update",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            if result.get("ok"):
                print(f"  ✅ Brain pushed to Widget successfully")
                print(f"     View at: {WIDGET_URL}/agent/{agent_id}/brain")
                return True
            else:
                print(f"  ❌ Push failed: {result}")
                return False
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"  ❌ HTTP {e.code}: {body}")
        return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def main():
    print("🧠 Pushing brain to AI Agent Widget...")

    agent_id, api_key = load_config()

    if not agent_id:
        print("  ❌ No widget_agent_id — run widget-brain-pull.py first")
        sys.exit(1)
    if not api_key:
        print("  ❌ No willie_api_key — needed to authenticate brain push")
        sys.exit(1)

    print(f"  📡 Agent ID: {agent_id}")
    success = push_brain(agent_id, api_key)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
