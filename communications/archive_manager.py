#!/usr/bin/env python3
"""
Message Bus Archive Manager v1.0
- Archives messages older than ARCHIVE_DAYS (default: 7) to archive/
- Compresses archived messages monthly
- Keeps inbox/sent lean for fast git operations
- Never deletes — only moves to archive
- Updates COORDINATION.md with archive stats
"""

import json
import gzip
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent.parent
COMM_DIR = REPO_DIR / "communications"
INBOX_DIR = COMM_DIR / "inbox"
SENT_DIR = COMM_DIR / "sent"
ARCHIVE_DIR = COMM_DIR / "archive"
STATS_FILE = COMM_DIR / "archive_stats.json"

ARCHIVE_DAYS = 7  # Archive messages older than this
COMPRESS_DAYS = 30  # Compress archives older than this

def now_ts():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")

def is_older_than(filepath, days):
    """Check if file is older than N days."""
    mtime = os.path.getmtime(filepath)
    file_time = datetime.fromtimestamp(mtime, tz=timezone.utc)
    return datetime.now(timezone.utc) - file_time > timedelta(days=days)

def archive_old_messages():
    """Move messages older than ARCHIVE_DAYS from inbox/sent to archive."""
    archived = 0
    archive_target = ARCHIVE_DIR / datetime.now(timezone.utc).strftime("%Y-%m")
    archive_target.mkdir(parents=True, exist_ok=True)

    for directory in [INBOX_DIR, SENT_DIR]:
        if not directory.exists():
            continue
        # Walk subdirectories (inbox/owl-to-self, inbox/self-to-owl, etc.)
        for subdir in directory.iterdir():
            if not subdir.is_dir():
                continue
            for f in subdir.glob("*.json"):
                if is_older_than(f, ARCHIVE_DAYS):
                    dest = archive_target / f"{subdir.name}_{f.name}"
                    shutil.move(str(f), str(dest))
                    archived += 1
                    print(f"  Archived: {subdir.name}/{f.name}")

    return archived

def compress_old_archives():
    """Compress archive folders older than COMPRESS_DAYS."""
    compressed = 0
    for folder in ARCHIVE_DIR.iterdir():
        if not folder.is_dir():
            continue
        # Already compressed?
        if (folder / ".compressed").exists():
            continue
        if is_older_than(folder, COMPRESS_DAYS):
            # Create tar.gz
            archive_name = f"{folder.name}.tar.gz"
            archive_path = ARCHIVE_DIR / archive_name
            result = subprocess.run(
                ["tar", "-czf", str(archive_path), "-C", str(ARCHIVE_DIR), folder.name],
                capture_output=True
            )
            if result.returncode == 0:
                shutil.rmtree(folder)
                (folder.parent / f"{archive_name}.compressed").touch()
                compressed += 1
                print(f"  Compressed: {folder.name} → {archive_name}")
    return compressed

def get_stats():
    """Get current bus statistics."""
    stats = {
        "last_run": now_ts(),
        "inbox_messages": 0,
        "sent_messages": 0,
        "archive_messages": 0,
        "archive_files": 0,
        "repo_size_mb": 0,
    }

    for subdir in INBOX_DIR.iterdir():
        if subdir.is_dir():
            stats["inbox_messages"] += len(list(subdir.glob("*.json")))

    if SENT_DIR.exists():
        stats["sent_messages"] = len(list(SENT_DIR.glob("*.json")))

    if ARCHIVE_DIR.exists():
        stats["archive_messages"] = len(list(ARCHIVE_DIR.rglob("*.json")))
        stats["archive_files"] = len(list(ARCHIVE_DIR.glob("*.tar.gz")))

    # Get repo size
    result = subprocess.run(
        ["du", "-sm", str(REPO_DIR)],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        stats["repo_size_mb"] = int(result.stdout.split()[0])

    return stats

def git_commit(message):
    subprocess.run(["git", "-C", str(REPO_DIR), "add", "communications/"], capture_output=True)
    subprocess.run(["git", "-C", str(REPO_DIR), "commit", "-m", message, "--quiet"], capture_output=True)
    subprocess.run(["git", "-C", str(REPO_DIR), "push", "--quiet"], capture_output=True)

def main():
    print(f"[archive_manager] Running at {now_ts()}")

    # 1. Archive old messages
    archived = archive_old_messages()
    print(f"  Archived {archived} messages")

    # 2. Compress old archives
    compressed = compress_old_archives()
    print(f"  Compressed {compressed} archive folders")

    # 3. Save stats
    stats = get_stats()
    stats["last_archived_count"] = archived
    stats["last_compressed_count"] = compressed
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=2)

    print(f"  Stats: inbox={stats['inbox_messages']}, sent={stats['sent_messages']}, archive={stats['archive_messages']}, repo={stats['repo_size_mb']}MB")

    # 4. Git commit
    if archived > 0 or compressed > 0:
        git_commit(f"[self] Archive run: {archived} archived, {compressed} compressed")

    print(f"[archive_manager] Done.")

if __name__ == "__main__":
    main()
