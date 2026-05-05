# Tool: db-migrate
**Type:** Database
**Use when:** Need to add columns/tables, schema changes, "no such column" errors
**Trigger phrases:** "Add column to table", "Database migration needed", "Fix missing column", "Schema change"

## What It Does
Safely modify SQLite database schemas in production Flask apps on Railway without breaking existing deployments.

## How To Use

### Step 1: Identify What Exists
```bash
# In Railway shell or local sqlite3
sqlite3 /path/to/app.db ".tables"
sqlite3 /path/to/app.db ".schema orders"
```

### Step 2: Write Idempotent Migration Function
```python
def _run_migrations(db):
    """Safe migrations: ALTER TABLE ADD COLUMN wrapped in try/except."""
    migrations = [
        ('orders',      'special_notes', "TEXT DEFAULT ''"),
        ('timesheets',  'source',        "TEXT DEFAULT 'web'"),
    ]
    for table, col, defn in migrations:
        try:
            db.execute(f'ALTER TABLE {table} ADD COLUMN {col} {defn}')
        except Exception:
            pass  # Already exists, safe to skip

    # Create indexes ONLY after columns are guaranteed to exist
    try:
        db.execute("CREATE INDEX IF NOT EXISTS idx_ts_source ON timesheets(source)")
    except Exception:
        pass
```

### Step 3: Call at the Right Time
```python
# GOOD: Call _run_migrations AFTER its definition
# Can be at module end or inside init_db if defined above
```

### Step 4: Test Locally
```bash
# Fresh DB (simulates new deployment)
rm app.db && python -c "from app import init_db; init_db()"

# Legacy DB (simulates production)
cp old_production.db app.db
python -c "from app import get_db; _run_migrations(get_db())"
```

## Rules
1. **Never drop columns** — SQLite can't recover them
2. **Always wrap ALTER TABLE in try/except** — must be idempotent
3. **Create indexes after migrations** — not before
4. **Never reference new columns in init_db's CREATE TABLE** — they belong in migrations
5. **Log every migration** — record what was added and when

## Quick Command
```bash
cd /a0/usr/workdir/sweet-spot-cakes && python -c "
import sqlite3
db = sqlite3.connect('app.db')
db.row_factory = sqlite3.Row
cols = db.execute('PRAGMA table_info(orders)').fetchall()
for c in cols: print(c['name'], c['type'])
"
```

## Related
- `deploy-rescue` — When migrations cause boot loops
- `rollback-ready` — Revert schema changes safely

---
*Tool: db-migrate v1.0 — Built from Agent-Z/skills by Echo (KiloClaw)*