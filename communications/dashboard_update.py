#!/usr/bin/env python3
"""
Dashboard Auto-Update v1.0
Updates Jay's EcDash dashboard with recent work summaries every 4-5 hours.
Reads from COORDINATION.md, memory files, and recent commits.
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_DIR = Path("/home/mingo/echo-v1-brain")
MEMORY_DIR = REPO_DIR / "memory"
COORD_FILE = REPO_DIR / "communications/COORDINATION.md"

# EcDash API endpoint and credentials
ECDASH_URL = "https://alexanderai.site"
ECDASH_PASSWORD = os.environ.get("ECDASH_PASSWORD", "ech0v1agent!")

def now_ts():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

def get_recent_commits(hours=5):
    """Get recent git commits."""
    try:
        result = subprocess.run(
            ["git", "-C", str(REPO_DIR), "log", f"--since='{hours} hours ago'", "--oneline"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            commits = result.stdout.strip().split('\n')
            return commits[:10]  # Max 10
    except Exception:
        pass
    return []

def get_recent_memory_files(hours=5):
    """Get recently modified memory files."""
    recent = []
    cutoff = datetime.now(timezone.utc).timestamp() - (hours * 3600)
    for f in MEMORY_DIR.glob("*.md"):
        if f.stat().st_mtime > cutoff:
            recent.append(f.stem)
    return recent

def read_coordination_summary():
    """Extract key sections from COORDINATION.md."""
    if not COORD_FILE.exists():
        return "COORDINATION.md not found"
    content = COORD_FILE.read_text()
    # Extract just the key status sections
    lines = content.split('\n')
    summary = []
    for line in lines:
        if any(line.startswith(x) for x in ['##', '###', '✅', '❌', '🔴', '🔧', '📊', '📐', '📋', '🚧']):
            summary.append(line)
        elif line.strip().startswith('-') and any(x in line.lower() for x in ['status', 'priority', 'scope', 'next', 'blocked', 'completed']):
            summary.append(line)
    return '\n'.join(lines)

def build_dashboard_payload():
    """Build the update payload for EcDash."""
    commits = get_recent_commits(5)
    memory = get_recent_memory_files(5)
    coord_summary = read_coordination_summary()

    payload = {
        "timestamp": now_ts(),
        "active_agents": ["self", "owl"],
        "recent_commits": commits,
        "recent_memory": memory,
        "coordination_summary": coord_summary[:2000] if coord_summary else "No coordination data",
    }
    return payload

def push_to_ecdash(payload):
    """Push update to EcDash dashboard via API."""
    import urllib.request
    import urllib.error

    # Try to update via the EcDash API
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            f"{ECDASH_URL}/api/self-update",
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {ECDASH_PASSWORD}",
            },
            method="POST"
        )
        resp = urllib.request.urlopen(req, timeout=15)
        print(f"[dashboard] Push successful: {resp.status}")
        return True
    except Exception as e:
        print(f"[dashboard] API push failed: {e}")
        # Fallback: save locally for next sync
        fallback = REPO_DIR / "communications" / "dashboard_pending.json"
        with open(fallback, 'w') as f:
            json.dump(payload, f, indent=2)
        print(f"[dashboard] Saved to {fallback}")
        return False

def main():
    print(f"[dashboard_update] Running at {now_ts()}")
    payload = build_dashboard_payload()
    print(f"  Commits: {len(payload['recent_commits'])}")
    print(f"  Memory files: {len(payload['recent_memory'])}")
    push_to_ecdash(payload)
    print(f"[dashboard_update] Done.")

if __name__ == "__main__":
    main()
