# memory-compress

**Version:** 1.0.0
**Created:** 2026-04-18
**Author:** Echo

## Description

Compress old daily memory logs into monthly summaries to prevent memory bloat. Per research: stale memories degrade agent performance. Monthly compression keeps context sharp.

## When To Use

- Monthly (first session of each new month)
- When daily memory files exceed 10+ entries
- When MEMORY.md starts getting too long (>200 lines)

## Compression Rules

1. Daily files older than 30 days → compress into `memory/YYYY-MM-summary.md`
2. Keep the last 7 days of daily files intact (uncompressed)
3. MEMORY.md = curated long-term wisdom only (not raw logs)
4. Remove completed TODOs from MEMORY.md that are more than 60 days old
5. Archive `todos.json` completed items older than 30 days (already handled by `todo_manager.py clean`)

## Monthly Summary Format

```markdown
# Memory Summary — [MONTH YEAR]

## Key Events
- [1-line summary of major events]

## Lessons Learned
- [Permanent lessons from this month]

## Projects Worked On
- [App]: [what was done]

## Decisions Made
- [Architectural, business, or technical decisions]

## Still Relevant
- [Any open items that haven't been resolved]
```

## Script: compress-memory.sh

```bash
#!/bin/bash
# compress-memory.sh — Monthly memory compression
# Run first session of each month

MEMORY_DIR="/root/.openclaw/echo-v1/memory"
CUTOFF_DATE=$(date -d "30 days ago" +%Y-%m-%d)
MONTH=$(date -d "30 days ago" +%Y-%m)
SUMMARY_FILE="$MEMORY_DIR/${MONTH}-summary.md"

echo "📦 Compressing memory files older than $CUTOFF_DATE..."

# List files to compress
OLD_FILES=$(ls "$MEMORY_DIR"/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].md 2>/dev/null | \
    awk -F/ '{print $NF}' | awk -F. '{print $1}' | \
    awk -v cutoff="$CUTOFF_DATE" '$0 < cutoff')

if [ -z "$OLD_FILES" ]; then
    echo "✅ Nothing to compress"
    exit 0
fi

echo "Files to compress:"
echo "$OLD_FILES"

# Create summary header
cat > "$SUMMARY_FILE" << EOF
# Memory Summary — $MONTH
*Auto-compressed from daily logs on $(date +%Y-%m-%d)*

EOF

# Append all old file content
for f in $OLD_FILES; do
    FILE="$MEMORY_DIR/${f}.md"
    if [ -f "$FILE" ]; then
        echo "## Daily: $f" >> "$SUMMARY_FILE"
        cat "$FILE" >> "$SUMMARY_FILE"
        echo "" >> "$SUMMARY_FILE"
        rm "$FILE"
        echo "  ✅ Compressed $f"
    fi
done

echo "✅ Summary saved to $SUMMARY_FILE"
```

## MEMORY.md Cleanup Pattern

When MEMORY.md exceeds 200 lines:
1. Move `## Completed TODOs` older than 60 days to `memory/archived-todos.md`
2. Move `## Session Notes` older than 30 days to the appropriate monthly summary
3. Keep: Who We Are, Core Rules, Infrastructure, Open TODOs, App URLs
