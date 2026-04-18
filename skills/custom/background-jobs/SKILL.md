# background-jobs

**Version:** 1.0.0
**Created:** 2026-04-18
**Author:** Echo

## Description

Lightweight background job patterns for Jay's Railway Flask apps. No Redis, no Celery — just Python threads and SQLite. Covers email sending, drip schedulers, periodic cleanup, and webhook delivery.

## When To Use

- Email sending (never block a route)
- Drip email scheduler (run every hour)
- Periodic cleanup tasks (expired trials, old data)
- Webhook delivery with retry
- Any work that shouldn't slow down a user request

## Pattern 1 — Simple Background Thread (Fire and Forget)

Best for: Single async task (send one email, run one check)

```python
import threading

def send_in_background(fn, *args, **kwargs):
    """Run any function in a daemon thread. Non-blocking."""
    t = threading.Thread(target=fn, args=args, kwargs=kwargs, daemon=True)
    t.start()

# Usage in a route:
@app.route('/signup', methods=['POST'])
def signup():
    # ... create user ...
    send_in_background(send_welcome_email, user_email, user_name)
    return redirect('/dashboard')
```

## Pattern 2 — Recurring Background Worker (Every N Seconds)

Best for: Drip emails, trial expiry checks, cleanup jobs

```python
import threading, time

def start_background_worker(fn, interval_seconds, name="worker"):
    """
    Start a recurring background worker. Runs fn every interval_seconds.
    Safe to call at app startup.
    """
    def _loop():
        while True:
            try:
                fn()
            except Exception as e:
                print(f"[{name}] Error: {e}")
            time.sleep(interval_seconds)

    t = threading.Thread(target=_loop, name=name, daemon=True)
    t.start()
    print(f"✅ Background worker started: {name} (every {interval_seconds}s)")
    return t

# Usage in app.py (after app creation):
from drip_scheduler import run_drip_scheduler
from cleanup import run_cleanup

# Only start workers once (not in debug reload)
import os
if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    start_background_worker(run_drip_scheduler, 3600, "drip-scheduler")
    start_background_worker(run_cleanup, 86400, "daily-cleanup")
```

## Pattern 3 — SQLite Job Queue (Reliable, Survives Restarts)

Best for: Webhook delivery, retry logic, tasks that must not be lost

```python
import sqlite3, json, time, threading
from datetime import datetime, timezone

QUEUE_DB = '/data/jobs.db'

def init_job_queue():
    conn = sqlite3.connect(QUEUE_DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_type TEXT NOT NULL,
            payload TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            attempts INTEGER DEFAULT 0,
            max_attempts INTEGER DEFAULT 3,
            created_at TEXT DEFAULT (datetime('now')),
            run_after TEXT DEFAULT (datetime('now')),
            completed_at TEXT
        )
    """)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.commit()
    conn.close()

def enqueue(job_type, payload, delay_seconds=0):
    """Add a job to the queue."""
    from datetime import timedelta
    run_after = (datetime.now(timezone.utc) + timedelta(seconds=delay_seconds)).isoformat()
    conn = sqlite3.connect(QUEUE_DB)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute(
        "INSERT INTO jobs (job_type, payload, run_after) VALUES (?, ?, ?)",
        (job_type, json.dumps(payload), run_after)
    )
    conn.commit()
    conn.close()

def process_jobs(handlers):
    """
    Process pending jobs. Call handlers dict: {'job_type': handler_fn}
    handler_fn(payload_dict) -> None (raise exception on failure)
    """
    conn = sqlite3.connect(QUEUE_DB)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.row_factory = sqlite3.Row
    now = datetime.now(timezone.utc).isoformat()

    jobs = conn.execute("""
        SELECT * FROM jobs
        WHERE status = 'pending' AND run_after <= ? AND attempts < max_attempts
        ORDER BY created_at LIMIT 10
    """, (now,)).fetchall()

    for job in jobs:
        handler = handlers.get(job['job_type'])
        if not handler:
            continue
        try:
            conn.execute("UPDATE jobs SET status='running', attempts=attempts+1 WHERE id=?", (job['id'],))
            conn.commit()
            handler(json.loads(job['payload']))
            conn.execute("UPDATE jobs SET status='done', completed_at=datetime('now') WHERE id=?", (job['id'],))
        except Exception as e:
            print(f"[JOB ERROR] {job['job_type']} #{job['id']}: {e}")
            conn.execute("UPDATE jobs SET status='pending' WHERE id=?", (job['id'],))
        conn.commit()
    conn.close()

# Start queue processor in app.py:
# JOB_HANDLERS = {
#     'send_email': handle_send_email,
#     'stripe_webhook': handle_stripe_webhook,
# }
# start_background_worker(lambda: process_jobs(JOB_HANDLERS), 10, "job-queue")
```

## Railway-Specific Notes

- All background threads are in-process — they die with the dyno
- For work that must survive restarts: use SQLite job queue (Pattern 3)
- `/data` volume persists across deploys; thread state does NOT
- Railway has a 30s request timeout — always offload to background

## Common Jobs to Background

| Job | Interval | Pattern |
|-----|----------|---------|
| Welcome email | on-demand | Pattern 1 |
| Drip email scheduler | hourly | Pattern 2 |
| Trial expiry check | daily | Pattern 2 |
| Stripe webhook processing | on-demand | Pattern 1 or 3 |
| Cleanup old sessions | daily | Pattern 2 |
| /data backup to S3 | daily | Pattern 2 |
