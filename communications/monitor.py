#!/usr/bin/env python3
"""
Uptime Monitor v1.1 - Self Agent
Monitors all Liberty Emporium apps and sends alerts via message bus if any go down.

Full app inventory from Jay 2026-05-29:
  Production (Railway): FloodClaims Pro, Sweet Spot Cakes, Remote Repair, Web App (befe95),
    IT Courses (needs rebuild), Luxury Rentals Demo
  Production (alexanderai.site subdomains): Remote Repair, Agents, Shop, Voice Makeover,
    AI Widget, Consignment, Contractor Pro, EcDash, Pet Vet AI, LE Thrift, Gym Forge
  Demos: Inventory Demo
  External: Liberty Oil (libertyoilandpropane.com)
  Retired: KYS (deleted)
"""

import json
import os
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

import urllib.request
import urllib.error

# ── Configuration ──────────────────────────────────────────────────────────────
REPO_DIR = Path(__file__).resolve().parent.parent  # echo-v1-brain/
COMM_DIR = REPO_DIR / "communications"
INBOX_DIR = COMM_DIR / "inbox"
STATE_FILE = COMM_DIR / "monitor_state.json"

AGENT_NAME = "bull"
AGENT_MAP = {
    "bull": {"inbox": "bull-to-owl", "outbox": "owl-to-bull"},
    "owl": {"inbox": "owl-to-bull", "outbox": "bull-to-owl"},
    "bullet": {"inbox": "owl-to-bull", "outbox": "bull-to-owl"},
}

APPS = [
    # Railway Production
    {"name": "FloodClaims Pro", "url": "https://billy-floods.up.railway.app", "expect": [200, 301, 302]},
    {"name": "Sweet Spot Cakes", "url": "https://sweet-spot-cakes.up.railway.app", "expect": [200, 301, 302]},
    {"name": "Remote Repair", "url": "https://remote.repaire.alexanderai.site", "expect": [200, 301, 302]},
    {"name": "Agents", "url": "https://agents.alexanderai.site", "expect": [200, 301, 302]},
    {"name": "Shop", "url": "https://shop.alexanderai.site", "expect": [200, 301, 302]},
    {"name": "Voice Makeover", "url": "https://voice-make-over.alexanderai.site", "expect": [200, 301, 302]},
    {"name": "AI Widget", "url": "https://ai.widget.alexanderai.site", "expect": [200, 301, 302]},
    {"name": "Consignment", "url": "https://consignment.ai.solutions.alexanderai.site", "expect": [200, 301, 302]},
    {"name": "Contractor Pro", "url": "https://contractor.ai.solutions.alexanderai.site", "expect": [200, 301, 302]},
    {"name": "EcDash", "url": "https://alexanderai.site", "expect": [200, 301, 302]},
    {"name": "Pet Vet AI", "url": "https://ai-vet-tech.alexanderai.site", "expect": [200, 301, 302]},
    {"name": "LE Thrift", "url": "https://liberty-emporium-thrift.alexanderai.site", "expect": [200, 301, 302]},
    {"name": "Gym Forge", "url": "https://gymforge.ai.alexanderai.site/", "expect": [200, 301, 302]},
    {"name": "Liberty Oil", "url": "https://libertyoilandpropane.com", "expect": [200, 301, 302]},
    # Demos
    {"name": "Luxury Rentals Demo", "url": "https://luxury-rentals-demo-production.up.railway.app", "expect": [200, 301, 302]},
    {"name": "Inventory Demo", "url": "https://inventory-demo.alexanderai.site", "expect": [200, 301, 302]},
    # Needs rebuild
    {"name": "IT Courses", "url": "https://web-production-8bbc54.up.railway.app", "expect": [200, 301, 302]},
    # Retired / not monitored
    # KYS: deleted by Jay
]

TIMEOUT_SECONDS = 15

# ── Helpers ────────────────────────────────────────────────────────────────────

def now_iso():
    return datetime.now(timezone.utc).isoformat()

def now_ts():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")

def get_outbox(agent):
    mapping = AGENT_MAP.get(agent, AGENT_MAP["bull"])
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
    expect = app.get("expect", [200])
    start = time.time()
    try:
        req = urllib.request.Request(app["url"], method="GET")
        req.add_header("User-Agent", "LibertyEmporium-Monitor/1.0")
        response = urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS)
        elapsed = (time.time() - start) * 1000
        return response.status in expect, response.status, elapsed
    except urllib.error.HTTPError as e:
        elapsed = (time.time() - start) * 1000
        if e.code in expect or e.code in (301, 302, 401, 403):
            return True, e.code, elapsed
        return False, e.code, elapsed
    except Exception:
        elapsed = (time.time() - start) * 1000
        return False, 0, elapsed

def git_pull():
    try:
        subprocess.run(["git", "-C", str(REPO_DIR), "pull", "--quiet"], capture_output=True, timeout=30)
    except Exception:
        pass

def run_check():
    print(f"[{now_ts()}] Starting uptime check...")
    git_pull()
    state = load_state()
    now = time.time()
    up_count = 0
    down_count = 0

    for app in APPS:
        name = app["name"]
        prev = state["app_status"].get(name, {}).get("status", "unknown")
        cooldown = state["alert_cooldown"].get(name, 0)

        ok, code, ms = check_app(app)
        status_str = "up" if ok else "down"
        icon = "✅" if ok else "❌"

        if ok:
            up_count += 1
        else:
            down_count += 1

        state["app_status"][name] = {
            "status": status_str,
            "http_code": code,
            "response_ms": round(ms, 1),
            "last_check": now_ts(),
        }

        print(f"  {icon} {name}: {status_str} (HTTP {code}, {ms:.0f}ms)")

        if not ok and prev != "down":
            if now < cooldown:
                print(f"    [SKIP] Alert cooldown active")
                continue
            send_alert("owl", f"⚠️ {name} is DOWN",
                f"{name} ({app['url']}) is not responding.\nHTTP {code}, {ms:.0f}ms\nDetected: {now_ts()}",
                "critical" if name == "FloodClaims Pro" else "high", name, app["url"])
            state["alert_cooldown"][name] = now + 600
        elif ok and prev == "down":
            send_alert("owl", f"✅ {name} is BACK UP",
                f"{name} ({app['url']}) recovered.\nHTTP {code}, {ms:.0f}ms\nRecovered: {now_ts()}",
                "info", name, app["url"])

    save_state(state)
    print(f"[{now_ts()}] Complete — {up_count} up, {down_count} down\n")

def main():
    interval = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    print(f"Uptime Monitor v1.1 — {len(APPS)} apps every {interval}s")
    while True:
        try:
            run_check()
        except Exception as e:
            print(f"[ERROR] {e}")
        time.sleep(interval)

if __name__ == "__main__":
    main()
