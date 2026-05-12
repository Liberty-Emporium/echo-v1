#!/usr/bin/env python3
"""
widget-brain-pull.py — Pull Echo's brain from AI Agent Widget at boot.

Fetches IDENTITY.md, SOUL.md, MEMORY.md, system_prompt, and api_key
from https://ai-agent-widget-production.up.railway.app and writes them
locally so Echo starts every session with the canonical brain.

Usage:
    python3 echo-v1/scripts/widget-brain-pull.py

Config (set once):
    /root/.secrets/widget_agent_id   — Echo's agent ID in the Widget
    /root/.secrets/widget_api_key    — Echo's OpenRouter API key (from Widget)
    /root/.secrets/willie_api_key    — alias, same key (willie = widget api key)
"""

import os, sys, json, urllib.request, urllib.error

WIDGET_URL   = "https://ai-agent-widget-production.up.railway.app"
AGENT_ID_FILE = "/root/.secrets/widget_agent_id"
API_KEY_FILE  = "/root/.secrets/willie_api_key"
BRAIN_DIR     = "/root/.openclaw/workspace"
ECHO_BRAIN_DIR = "/root/.openclaw/workspace/echo-v1"


def load_config():
    agent_id = ""
    api_key  = ""
    if os.path.exists(AGENT_ID_FILE):
        agent_id = open(AGENT_ID_FILE).read().strip()
    if os.path.exists(API_KEY_FILE):
        api_key = open(API_KEY_FILE).read().strip()
    # Fallbacks from env
    agent_id = agent_id or os.environ.get("WIDGET_AGENT_ID", "")
    api_key  = api_key  or os.environ.get("WILLIE_API_KEY", "")
    return agent_id, api_key


def pull_brain(agent_id, api_key):
    """
    Pull brain via /agent/<id>/brain/update endpoint.
    Uses api_key as the token (that's how the Widget authenticates external apps).
    We do a GET to /agent/<id>/brain/public using brain_sync_token,
    OR we read via the update endpoint pattern.
    """
    # Primary: use /agent/<id>/brain/public with brain_sync_token
    sync_token_file = "/root/.secrets/brain_sync_token"
    sync_token = open(sync_token_file).read().strip() if os.path.exists(sync_token_file) else ""

    if sync_token:
        req = urllib.request.Request(
            f"{WIDGET_URL}/agent/{agent_id}/brain/public",
            headers={"X-Brain-Sync-Token": sync_token},
            method="GET",
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            print(f"  ⚠️  brain/public returned HTTP {e.code}: {body}")
            print(f"  ↪  Falling back to api_key auth...")

    # Fallback: POST to brain/update with api_key to get current values
    # (Widget returns current brain in response)
    if api_key:
        payload = json.dumps({"token": api_key}).encode("utf-8")
        req = urllib.request.Request(
            f"{WIDGET_URL}/agent/{agent_id}/brain/update",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            print(f"  ❌ brain/update returned HTTP {e.code}: {body}")
            return None

    print("  ❌ No auth token available (need brain_sync_token or willie_api_key)")
    return None


def write_brain_files(brain):
    """Write pulled brain files to local workspace."""
    written = []

    mapping = {
        "identity_md": (f"{ECHO_BRAIN_DIR}/IDENTITY.md", f"{BRAIN_DIR}/IDENTITY.md"),
        "soul_md":     (f"{ECHO_BRAIN_DIR}/SOUL.md",     f"{BRAIN_DIR}/SOUL.md"),
        "memory_md":   (f"{ECHO_BRAIN_DIR}/MEMORY.md",   f"{BRAIN_DIR}/MEMORY.md"),
    }

    for key, (primary, fallback) in mapping.items():
        content = brain.get(key, "").strip()
        if not content:
            print(f"  ⚠️  {key}: empty in Widget — skipping (keeping local)")
            continue
        # Write to echo-v1 brain dir (primary)
        os.makedirs(os.path.dirname(primary), exist_ok=True)
        with open(primary, "w", encoding="utf-8") as f:
            f.write(content + "\n")
        # Also write to workspace root for KiloClaw to pick up
        with open(fallback, "w", encoding="utf-8") as f:
            f.write(content + "\n")
        written.append(key)
        print(f"  ✅ {key}: {len(content)} chars → written")

    # Write system_prompt if present
    system_prompt = brain.get("system_prompt", "").strip()
    if system_prompt:
        sp_path = f"{ECHO_BRAIN_DIR}/SYSTEM_PROMPT.md"
        with open(sp_path, "w", encoding="utf-8") as f:
            f.write(system_prompt + "\n")
        written.append("system_prompt")
        print(f"  ✅ system_prompt: {len(system_prompt)} chars → written")

    # Write api_key if present (this IS the willie_api_key / OpenRouter key)
    api_key = brain.get("api_key", "").strip()
    if api_key:
        with open(API_KEY_FILE, "w") as f:
            f.write(api_key + "\n")
        os.chmod(API_KEY_FILE, 0o600)
        print(f"  ✅ api_key: stored → /root/.secrets/willie_api_key")
        written.append("api_key")

    return written


def main():
    print("🧠 Pulling brain from AI Agent Widget...")

    agent_id, api_key = load_config()

    if not agent_id:
        print("  ❌ No widget_agent_id found.")
        print("     Go to https://ai-agent-widget-production.up.railway.app/dashboard")
        print("     Open Echo's agent, copy ID from URL, then run:")
        print("     echo '<agent_id>' > /root/.secrets/widget_agent_id")
        sys.exit(1)

    print(f"  📡 Agent ID: {agent_id}")
    brain = pull_brain(agent_id, api_key)

    if not brain:
        print("  ❌ Could not pull brain from Widget.")
        sys.exit(1)

    written = write_brain_files(brain)

    if written:
        print(f"\n  ✅ Brain pulled successfully ({len(written)} files)")
        print(f"     Echo is now running with Widget brain: {', '.join(written)}")
    else:
        print("  ⚠️  No brain files were written (Widget may have empty brain)")


if __name__ == "__main__":
    main()
