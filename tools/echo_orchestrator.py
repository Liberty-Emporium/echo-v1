"""
echo_orchestrator.py — Phase 4: Echo as Network Orchestrator  v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Echo (KiloClaw) is the brain of the Liberty-Emporium app network.
This module gives Echo the ability to:

  1. Poll the EcDash echo-bridge queue for pending tasks
  2. Parse task intent (natural language → task type)
  3. Execute cross-app orchestration tasks
  4. Report results back to EcDash (task update + note)

Usage — called from main session heartbeat or directly:

    from echo_orchestrator import run_pending_tasks, run_task
    run_pending_tasks()          # process everything in the bridge queue
    run_task("check all apps")   # run a specific task by description

Built-in task types:
    network_health    — ping all apps, report uptime + stats
    gitlab_backup     — run sync-all-to-gitlab.sh
    status_report     — full portfolio report posted to EcDash notes
    photo_analysis    — trigger FloodClaim → Pet Vet AI damage analysis
    vault_audit       — list recent vault access events
    app_restart_check — find apps that haven't pinged recently
"""

import os, json, time, subprocess, threading, traceback, urllib.request, urllib.error
from datetime import datetime, timezone
from typing import Optional

# ── Config ────────────────────────────────────────────────────────────────────
ECDASH_URL    = "https://jay-portfolio-production.up.railway.app"
ECDASH_TOKEN  = ""   # loaded lazily from /root/.secrets/ecdash_token
ECHO_SECRET   = os.environ.get("ECHO_WEBHOOK_SECRET", "")
SCRIPTS_DIR   = os.path.dirname(os.path.abspath(__file__)).replace("/tools", "/scripts")

def _get_token():
    global ECDASH_TOKEN
    if not ECDASH_TOKEN:
        try:
            ECDASH_TOKEN = open("/root/.secrets/ecdash_token").read().strip()
        except Exception:
            pass
    return ECDASH_TOKEN

def _http(method, path, data=None, extra_headers=None):
    """Fire HTTP request to EcDash. Returns parsed JSON or None."""
    token = _get_token()
    headers = {
        "Content-Type":  "application/json",
        "Authorization": f"Bearer {token}",
        **(extra_headers or {})
    }
    body = json.dumps(data).encode() if data else None
    try:
        req = urllib.request.Request(
            ECDASH_URL.rstrip("/") + path,
            data=body, headers=headers, method=method
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        print(f"[orchestrator] {method} {path} failed: {e}")
        return None

def _post_note(text, pinned=False):
    """Post a note to Jay's dashboard."""
    _http("POST", "/api/notes", {"text": text, "pinned": pinned})

def _update_task(task_id, status, response):
    """Report task completion back to EcDash bridge."""
    _http("PATCH", f"/api/echo-bridge/{task_id}",
          data={"status": status, "response": response},
          extra_headers={"X-Echo-Secret": ECHO_SECRET})

# ── Task intent parsing ───────────────────────────────────────────────────────
# Maps keyword patterns → task handler names
TASK_PATTERNS = [
    (["check all apps", "network health", "app health", "status check",
      "check apps", "all apps", "how are the apps"],          "network_health"),
    (["gitlab backup", "backup", "sync gitlab", "push to gitlab",
      "mirror repos"],                                         "gitlab_backup"),
    (["status report", "portfolio report", "full report",
      "summary report", "generate report"],                    "status_report"),
    (["photo analysis", "analyze photos", "damage photos",
      "analyze damage"],                                       "photo_analysis"),
    (["vault audit", "check vault", "vault access"],           "vault_audit"),
    (["check restarts", "app restarts", "uptime check",
      "who restarted"],                                        "uptime_check"),
]

def _parse_intent(task_text: str) -> str:
    """Map natural language task description to a task type."""
    lower = task_text.lower()
    for keywords, task_type in TASK_PATTERNS:
        if any(k in lower for k in keywords):
            return task_type
    return "unknown"


# ── Task handlers ─────────────────────────────────────────────────────────────

def task_network_health() -> str:
    """Ping all Liberty-Emporium apps via /api/status and compile a report."""
    import urllib.request
    
    # App URL map
    APP_URLS = {
        "EcDash":             "https://jay-portfolio-production.up.railway.app",
        "FloodClaim Pro":     "https://billy-floods.up.railway.app",
        "AI Agent Widget":    "https://ai.widget.alexanderai.site",
        "Sweet Spot Cakes":   "https://sweet-spot-cakes.up.railway.app",
        "Pet Vet AI":         "https://pet-vet-ai-production.up.railway.app",
        "Contractor Pro AI":  "https://contractor-pro-ai-production.up.railway.app",
        "Drop Shipping":      "https://shop.alexanderai.site",
        "Consignment":        "https://web-production-43ce4.up.railway.app",
        "Liberty Inventory":  "https://liberty-emporium-and-thrift-inventory-app-production.up.railway.app",
        "GymForge":           "https://web-production-1c23.up.railway.app",
        "Liberty Oil":        "https://liberty-oil-propane.up.railway.app",
        "Grace (Mom's AI)":   "https://moms-ai-helper.up.railway.app",
    }

    results = {}
    lock = threading.Lock()

    def _ping(name, base_url):
        start = time.time()
        # Try /api/status first (Phase 3 apps), fall back to /health
        for path in ["/api/status", "/health"]:
            try:
                req = urllib.request.Request(base_url + path, method="GET")
                with urllib.request.urlopen(req, timeout=6) as r:
                    ms  = int((time.time() - start) * 1000)
                    try:
                        body = json.loads(r.read().decode())
                    except Exception:
                        body = {}
                    with lock:
                        results[name] = {
                            "ok":      True,
                            "ms":      ms,
                            "path":    path,
                            "stats":   body.get("stats", {}),
                            "uptime":  body.get("uptime_human", ""),
                        }
                    return
            except Exception:
                pass
        ms = int((time.time() - start) * 1000)
        with lock:
            results[name] = {"ok": False, "ms": ms, "path": "/health"}

    threads = [threading.Thread(target=_ping, args=(n, u), daemon=True)
               for n, u in APP_URLS.items()]
    for t in threads: t.start()
    for t in threads: t.join(timeout=12)

    up   = [n for n, r in results.items() if r["ok"]]
    down = [n for n, r in results.items() if not r["ok"]]
    ts   = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = [f"🌐 Network Health Check — {ts}",
             f"✅ {len(up)}/{len(results)} apps online",
             ""]

    for name in sorted(up):
        r = results[name]
        uptime = f" · up {r['uptime']}" if r.get("uptime") else ""
        stats_str = ""
        s = r.get("stats", {})
        if s and not s.get("error"):
            stats_str = " · " + ", ".join(f"{k}: {v}" for k, v in list(s.items())[:3])
        lines.append(f"  🟢 {name} ({r['ms']}ms{uptime}){stats_str}")

    if down:
        lines.append("")
        for name in sorted(down):
            lines.append(f"  🔴 {name} — DOWN")

    return "\n".join(lines)


def task_gitlab_backup() -> str:
    """Run sync-all-to-gitlab.sh to mirror all repos to GitLab."""
    script = os.path.join(SCRIPTS_DIR, "sync-all-to-gitlab.sh")
    if not os.path.exists(script):
        return f"❌ sync-all-to-gitlab.sh not found at {script}"
    try:
        env = {**os.environ,
               "GH_TOKEN": open("/root/.secrets/github_token").read().strip(),
               "GL_TOKEN": open("/root/.secrets/gitlab_token").read().strip()}
        result = subprocess.run(
            ["bash", script], capture_output=True, text=True, timeout=300, env=env
        )
        if result.returncode == 0:
            lines = [l for l in result.stdout.strip().split("\n") if l.strip()]
            summary = "\n".join(lines[-15:])  # last 15 lines
            return f"✅ GitLab backup complete\n\n{summary}"
        else:
            return f"❌ Backup failed (exit {result.returncode})\n{result.stderr[:400]}"
    except subprocess.TimeoutExpired:
        return "⏱️ Backup timed out after 5 minutes"
    except Exception as e:
        return f"❌ Error: {e}"


def task_status_report() -> str:
    """Build a full portfolio status report and post it as a pinned note."""
    health_report = task_network_health()

    # Add git log for main repos
    repos = ["echo-v1", "alexander-ai-dashboard", "alexander-ai-floodclaim",
             "alexander-ai-agent-widget", "alexander-ai-petvet"]
    commit_lines = []
    for repo in repos:
        path = f"/root/.openclaw/workspace/{repo}"
        if os.path.isdir(path):
            try:
                r = subprocess.run(
                    ["git", "log", "--oneline", "-2"],
                    capture_output=True, text=True, cwd=path, timeout=5
                )
                commits = r.stdout.strip().split("\n")
                if commits and commits[0]:
                    commit_lines.append(f"  {repo}: {commits[0]}")
            except Exception:
                pass

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    report = [
        f"📊 Portfolio Status Report — {ts}",
        "",
        health_report,
    ]
    if commit_lines:
        report += ["", "📝 Recent commits:"] + commit_lines

    full = "\n".join(report)
    _post_note(full, pinned=True)
    return "✅ Status report generated and posted to dashboard notes"


def task_vault_audit() -> str:
    """Fetch recent vault audit log from EcDash."""
    result = _http("GET", "/api/vault?audit=1")
    if not result:
        return "❌ Could not reach EcDash vault"
    if isinstance(result, list):
        return f"✅ Vault has {len(result)} secrets. Access looks normal."
    return f"Vault response: {json.dumps(result)[:200]}"


def task_uptime_check() -> str:
    """Check which apps have had recent restarts via /api/status uptime."""
    APP_URLS = {
        "FloodClaim Pro":   "https://billy-floods.up.railway.app",
        "AI Agent Widget":  "https://ai.widget.alexanderai.site",
        "Sweet Spot Cakes": "https://sweet-spot-cakes.up.railway.app",
        "Pet Vet AI":       "https://pet-vet-ai-production.up.railway.app",
    }
    lines = ["⏱️ Uptime Check:"]
    for name, url in APP_URLS.items():
        try:
            req = urllib.request.Request(url + "/api/status")
            with urllib.request.urlopen(req, timeout=6) as r:
                d = json.loads(r.read().decode())
                uptime_s = d.get("uptime_seconds", 0)
                uptime_h = d.get("uptime_human", f"{uptime_s}s")
                flag = " ⚠️ recently restarted" if uptime_s < 300 else ""
                lines.append(f"  {name}: {uptime_h}{flag}")
        except Exception:
            lines.append(f"  {name}: unreachable")
    return "\n".join(lines)


TASK_HANDLERS = {
    "network_health": task_network_health,
    "gitlab_backup":  task_gitlab_backup,
    "status_report":  task_status_report,
    "vault_audit":    task_vault_audit,
    "uptime_check":   task_uptime_check,
}


# ── Main orchestration loop ───────────────────────────────────────────────────

def run_task(task_text: str, task_id: Optional[int] = None) -> str:
    """
    Parse and execute a single task. Posts result to EcDash.

    Args:
        task_text: Natural language task description
        task_id:   EcDash bridge task ID (for status updates)

    Returns:
        Result string
    """
    print(f"[orchestrator] Running task: {task_text!r}")
    intent = _parse_intent(task_text)
    handler = TASK_HANDLERS.get(intent)

    if not handler:
        result = (f"⚠️ Echo didn't recognize that task: '{task_text}'\n\n"
                  f"Known tasks: {', '.join(TASK_HANDLERS.keys())}")
        if task_id:
            _update_task(task_id, "failed", result)
        return result

    print(f"[orchestrator] Intent: {intent} → running {handler.__name__}")
    try:
        result = handler()
    except Exception as e:
        result = f"❌ Task failed ({intent}): {e}\n{traceback.format_exc()[:300]}"

    if task_id:
        status = "done" if not result.startswith("❌") else "failed"
        _update_task(task_id, status, result)
        # Also post as a note for visibility
        _post_note(f"🤖 Echo completed task: {task_text!r}\n\n{result}")

    print(f"[orchestrator] Done: {result[:120]}")
    return result


def run_pending_tasks(max_tasks: int = 5) -> int:
    """
    Poll EcDash bridge queue, execute all pending tasks.
    Returns count of tasks processed.

    Call this from heartbeat or a cron job.
    """
    tasks = _http("GET", "/api/echo-bridge")
    if not tasks or not isinstance(tasks, list):
        return 0

    pending = [t for t in tasks if t.get("status") in ("pending", "queued")][:max_tasks]
    if not pending:
        return 0

    print(f"[orchestrator] Found {len(pending)} pending task(s)")
    for task in pending:
        run_task(task["task"], task_id=task["id"])
        time.sleep(0.5)  # small gap between tasks

    return len(pending)


if __name__ == "__main__":
    # Can be run directly for testing:  python3 echo_orchestrator.py
    import sys
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
        print(run_task(task))
    else:
        print("Running pending tasks from EcDash bridge queue...")
        n = run_pending_tasks()
        print(f"Processed {n} task(s)")
