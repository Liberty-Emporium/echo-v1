# sqlite-patterns

**Version:** 1.0.0
**Created:** 2026-04-18
**Author:** Echo

## Description

SQLite best practices for Jay's Railway Flask apps. WAL mode, safe queries, migrations, and performance patterns. Distilled from lessons-learned.md.

## THE RULE: Always Set WAL Pragmas

Add this to EVERY database connection in EVERY app — no exceptions:

```python
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")      # prevents readers blocking writers
    conn.execute("PRAGMA synchronous=NORMAL")    # safe + faster than FULL
    conn.execute("PRAGMA foreign_keys=ON")       # enforce FK constraints
    conn.execute("PRAGMA cache_size=-64000")     # 64MB cache
    return conn
```

Without WAL: readers block writers → app hangs under concurrent load.

## Safe DB Path Pattern (Railway)

```python
import os, sqlite3
from pathlib import Path

# Railway-safe: /data persists across deploys, app dir does NOT
DATA_DIR = os.environ.get('DATA_DIR', '/data')
Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, 'app.db')
```

## Schema Init Pattern

```python
def init_db():
    """Create tables if they don't exist. Safe to run on every startup."""
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            plan TEXT DEFAULT 'trial',
            plan_status TEXT DEFAULT 'active',
            trial_ends_at TEXT,
            stripe_customer_id TEXT,
            stripe_subscription_id TEXT,
            drip_sent TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER REFERENCES users(id),
            token TEXT UNIQUE NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        );
    """)
    conn.commit()
    conn.close()

# Call at startup:
# with app.app_context():
#     init_db()
```

## Migration Pattern (No Alembic Needed for SQLite)

```python
def run_migrations():
    """Add columns safely if they don't exist."""
    conn = get_db()
    cursor = conn.execute("PRAGMA table_info(users)")
    existing_cols = {row['name'] for row in cursor.fetchall()}

    migrations = [
        ("stripe_customer_id", "ALTER TABLE users ADD COLUMN stripe_customer_id TEXT"),
        ("stripe_subscription_id", "ALTER TABLE users ADD COLUMN stripe_subscription_id TEXT"),
        ("drip_sent", "ALTER TABLE users ADD COLUMN drip_sent TEXT DEFAULT ''"),
        ("plan_status", "ALTER TABLE users ADD COLUMN plan_status TEXT DEFAULT 'active'"),
    ]
    for col, sql in migrations:
        if col not in existing_cols:
            conn.execute(sql)
            print(f"  ✅ Migration: added column {col}")

    conn.commit()
    conn.close()
```

## Query Safety

```python
# NEVER — SQL injection risk
user = conn.execute(f"SELECT * FROM users WHERE email='{email}'").fetchone()

# ALWAYS — parameterized queries
user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()

# NEVER — raw user input in LIKE
conn.execute(f"SELECT * FROM items WHERE name LIKE '%{query}%'")

# ALWAYS
conn.execute("SELECT * FROM items WHERE name LIKE ?", (f"%{query}%",))
```

## Context Manager Pattern (Auto-Close)

```python
from contextlib import contextmanager

@contextmanager
def db_connection():
    conn = get_db()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

# Usage:
with db_connection() as conn:
    conn.execute("INSERT INTO users (email) VALUES (?)", (email,))
```

## Performance Tips

```python
# Batch inserts — 100x faster than individual inserts
conn.executemany(
    "INSERT INTO items (name, price) VALUES (?, ?)",
    [(item['name'], item['price']) for item in items]
)

# Index on frequently queried columns
conn.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
conn.execute("CREATE INDEX IF NOT EXISTS idx_users_plan ON users(plan)")

# EXPLAIN QUERY PLAN to check index usage
plan = conn.execute("EXPLAIN QUERY PLAN SELECT * FROM users WHERE email=?", (email,))
print(plan.fetchall())
```

## When to Move to PostgreSQL

SQLite is fine until:
- Write TPS > 500/second
- DB > 100GB
- Multi-region needed
- Need PostgreSQL RLS (Row Level Security)

For now, all 7 apps are well within SQLite range. When migrating to Fly.io → add Litestream for streaming backup.
