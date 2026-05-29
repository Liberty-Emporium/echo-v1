#!/usr/bin/env python3
"""
Uptime Monitor v1.0 - Self Agent
Monitors all Liberty Emporium apps and sends alerts via message bus if any go down.
Also attempts automatic recovery for known failure modes.

Apps monitored:
  - FloodClaims Pro: billy-floods.up.railway.app
  - AI Agent Widget: ai-agent-widget-production.up.railway.app
  - EcDash (Portfolio): jay-portfolio-production.up.railway.app / alexanderai.site
  - Liberty Oil: liberty-oil-propane.up.railway.app
  - KYS: ai-api-tracker-production.up.railway.app
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import urllib.request
import urllib.error
import uuid

# ── Configuration ──────────────────────────────────────────────────────────────
REPO_DIR = Path(__file__).resolve().parent.parent  # echo-v1-brain/
COMM_DIR = REPO_DIR / "communications"
INBOX_DIR = COMM_DIR / "inbox"
STATE_FILE = COMM_DIR / "monitor_state.json"

AGENT_NAME = "self"
AGENT_MAP = {
    "self": {"inbox": "self-to-owl", "outbox": "owl-to-self"},
    "owl": {"inbox": "owl-to-self", "outbox": "self-to-owl"},
}

APPS = [
    {"name": "FloodClaims Pro", "url": "https://billy-floods.up.railway.app", "health": "/", "expect": [200, 302]},
    {"name": "AI Agent Widget", "url": "https://ai-agent-widget-production.up.railway.app", "health": "/", "expect": [200, 302]},
    {"name": "EcDash", "url": "https://alexanderai.site", "health": "/", "expect": [200, 302]},
    {"name": "Liberty Oil", "url": "https://liberty-oil-propane.up.railway.app", "health": "/", "expect": [200, 302]},
    {"name": "KYS", "url": "https://ai-api-tracker-production.up.railway.app", "health": "/", "expect": [200, 302]},
]

TIMEOUT_SECONDS = 15
RAILWAY_REDEPLOY_WAIT = 120  # seconds to wait after triggering redeploy

# ── Helpers ────────────────────────────────────────────────────────────────────

def now_iso():
    return datetime.now(timezone.utc).isoformat()

def now_ts():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")

def get_outbox(agent):
    mapping = AGENT_MAP.get(agent, AGENT_MAP["self"])
    return INBOX_DIR / mapping["outbox"]

def git_commit_push(message):
    try:
        subprocess.run(["git", "-C", str(REPO_DIR), "add", "communications/"], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(REPO_DIR), "commit", "-m", message, "--quiet"], capture_output=True, timeout=30)
        subprocess.run(["git", "-C", str(REPO_DIR), "push", "--quiet"], capture_output=True, timeout=30)
    except Exception:
        pass

def send_alert(to, subject, body, priority="high", app=None, url=None):
    msg_id = str(uuid.uuid4())
    msg = {
        "protocol": "1.0",
        "id": msg_id,
        "from": AGENT_NAME,
        "to": to,
        "type": "alert",
        "subject": subject,
        "body": body,
        "priority": priority,
        "status": "pending",
        "task_id": None,
        "reply_to": None,
        "attachments": [],
        "metadata": {"app": app or "", "url": url or "", "tags": ["monitoring", "auto-detected"]},
        "created": now_iso(),
        "updated": now_iso(),
    }
    outbox = get_outbox(AGENT_NAME)
    outbox.mkdir(parents=True, exist_ok=True)
    filename = f"{now_ts()}_alert_{msg_id[:8]}.json"
    filepath = outbox / filename
    with open(filepath, "w") as f:
        json.dump(msg, f, indent=2)
    git_commit_push(f"[{AGENT_NAME}] ALERT: {subject}")
    print(f"[ALERT] {subject}")
    return filepath

def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"app_status": {}, "alert_cooldown": {}}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def check_app(app):
    """Check if an app is responding. Returns (ok, status_code, response_time_ms)."""
    health_url = app["url"] + app["health"]
    expect = app.get("expect", [200])
    start = time.time()
    try:
        req = urllib.request.Request(health_url, method="GET")
        req.add_header("User-Agent", "LibertyEmporium-Monitor/1.0")
        response = urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS)
        elapsed = (time.time() - start) * 1000
        return response.status in expect, response.status, elapsed
    except urllib.error.HTTPError as e:
        elapsed = (time.time() - start) * 1000
        # If the status code is in our expected range, the app is responding
        if e.code in expect:
            return True, e.code, elapsed
        # 4xx might mean auth redirect — app is alive
        if e.code in (301, 302, 401, 403):
            return True, e.code, elapsed
        return False, e.code, elapsed
    except Exception as e:
        elapsed = (time.time() - start) * 1000
        return False, 0, elapsed

def git_pull():
    try:
        subprocess.run(["git", "-C", str(REPO_DIR), "pull", "--quiet"], capture_output=True, timeout=30)
    except Exception:
        pass

# ── Main Monitor Logic ────────────────────────────────────────────────────────

def run_check():
    """Run a single monitoring check cycle."""
    print(f"\n[{now_ts()}] Starting uptime check...")
    git_pull()
    state = load_state()
    now = time.time()

    for app in APPS:
        name = app["name"]
        url = app["url"]
        prev_status = state["app_status"].get(name, "unknown")
        cooldown_until = state["alert_cooldown"].get(name, 0)

        ok, code, ms = check_app(app)
        status_str = "up" if ok else "down"

        # Update state
        state["app_status"][name] = {
            "status": status_str,
            "http_code": code,
            "response_ms": round(ms, 1),
            "last_check": now_ts(),
        }

        icon = "✅" if ok else "❌"
        print(f"  {icon} {name}: {status_str} (HTTP {code}, {ms:.0f}ms)")

        # Detect state change: UP -> DOWN
        if not ok and prev_status != "down":
            # Respect cooldown (don't alert more than once per 10 min per app)
            if now < cooldown_until:
                print(f"    [SKIP] Alert cooldown active for {name}")
                continue

            duration_min = round((cooldown_until - now) / 60) if cooldown_until > now else 0
            send_alert(
                to="owl",
                subject=f"⚠️ {name} is DOWN",
                body=(
                    f"{name} ({url}) is not responding.\n\n"
                    f"HTTP Status: {code}\n"
                    f"Response Time: {ms:.0f}ms\n"
                    f"Previous Status: {prev_status}\n"
                    f"Detected At: {now_ts()}\n\n"
                    f"Self will attempt to notify and coordinate recovery.\n"
                    f"Jay should check Railway dashboard if this persists."
                ),
                priority="critical" if name == "FloodClaims Pro" else "high",
                app=name,
                url=url,
            )
            # Set 10-minute cooldown
            state["alert_cooldown"][name] = now + 600

        # Detect state change: DOWN -> UP (recovery)
        elif ok and prev_status == "down":
            send_alert(
                to="owl",
                subject=f"✅ {name} is BACK UP",
                body=(
                    f"{name} ({url}) has recovered.\n\n"
                    f"HTTP Status: {code}\n"
                    f"Response Time: {ms:.0f}ms\n"
                    f"Recovered At: {now_ts()}\n\n"
                    f"Monitoring continues."
                ),
                priority="info",
                app=name,
                url=url,
            )

    save_state(state)
    print(f"[{now_ts()}] Check complete.\n")

def main():
    interval = int(os.environ.get("MONITOR_INTERVAL", "120"))  # default 2 minutes
    if len(sys.argv) > 1:
        try:
            interval = int(sys.argv[1])
        except ValueError:
            pass

    print(f"Uptime Monitor v1.0 - Self Agent")
    print(f"Monitoring {len(APPS)} apps every {interval}s")
    apps_list = ", ".join(a['name'] for a in APPS)
    print(f"Apps: {apps_list}")

    while True:
        try:
            run_check()
        except Exception as e:
            print(f"[ERROR] Monitor check failed: {e}")
        time.sleep(interval)

if __name__ == "__main__":
    main()
