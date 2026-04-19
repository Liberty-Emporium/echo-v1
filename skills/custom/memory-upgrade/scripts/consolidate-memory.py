#!/usr/bin/env python3
"""
consolidate-memory.py — Memory audit and consolidation helper
Scans daily diary files and reports what should be promoted to MEMORY.md

Usage:
  python3 consolidate-memory.py          # Show consolidation report
  python3 consolidate-memory.py --days 7 # Scan last N days
  python3 consolidate-memory.py --stale  # Flag potentially stale MEMORY.md entries
"""

import os
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path("/root/.openclaw/workspace")
MEMORY_FILE = WORKSPACE / "MEMORY.md"
MEMORY_DIR = WORKSPACE / "memory"


def scan_diary_files(days=7):
    """Find recent diary files and extract flagged items."""
    found = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        fpath = MEMORY_DIR / f"{date}.md"
        if fpath.exists():
            content = fpath.read_text()
            lines = content.split('\n')
            items = []
            for line in lines:
                # Lines worth promoting: decisions, lessons, facts
                if any(kw in line.lower() for kw in [
                    'decided', 'learned', 'important', 'remember', 'note:',
                    'jay said', 'jay wants', 'jay prefers', 'discovered',
                    'fixed', 'deployed', 'built', 'created'
                ]):
                    items.append(line.strip())
            if items:
                found.append((date, items))
    return found


def check_memory_freshness():
    """Scan MEMORY.md for potentially stale entries."""
    if not MEMORY_FILE.exists():
        return []
    
    content = MEMORY_FILE.read_text()
    stale_hints = []
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        # Look for entries that might be outdated
        if any(kw in line.lower() for kw in ['todo', 'need to', 'will ask', 'pending']):
            stale_hints.append((i + 1, line.strip()))
    
    return stale_hints


def main():
    parser = argparse.ArgumentParser(description="Memory consolidation helper")
    parser.add_argument('--days', type=int, default=7, help='Days to scan')
    parser.add_argument('--stale', action='store_true', help='Check for stale memory entries')
    args = parser.parse_args()

    print("\n🧠 Echo Memory Consolidation Report")
    print("=" * 50)
    print(f"📅 Scanning last {args.days} days of diary files\n")

    # Scan diary files
    diary_items = scan_diary_files(args.days)
    if diary_items:
        print("📝 Items from diary that may be worth promoting to MEMORY.md:")
        for date, items in diary_items:
            print(f"\n  [{date}]")
            for item in items[:10]:  # Cap at 10 per day
                print(f"  → {item[:100]}")
    else:
        print("✅ No obvious consolidation candidates found in recent diary files")

    # Check stale entries
    if args.stale:
        print("\n⚠️  Potentially stale MEMORY.md entries:")
        stale = check_memory_freshness()
        if stale:
            for lineno, line in stale[:20]:
                print(f"  Line {lineno}: {line[:100]}")
        else:
            print("  ✅ No obvious stale entries detected")

    # Count stats
    diary_count = len(list(MEMORY_DIR.glob("20*.md")))
    memory_size = len(MEMORY_FILE.read_text().split('\n')) if MEMORY_FILE.exists() else 0
    
    print(f"\n📊 Stats:")
    print(f"  Diary files: {diary_count}")
    print(f"  MEMORY.md lines: {memory_size}")
    print(f"\n💡 Tip: Review the items above and manually add the important ones to MEMORY.md")
    print("   Use: echo '- [fact] (learned YYYY-MM-DD)' >> MEMORY.md")


if __name__ == "__main__":
    main()
