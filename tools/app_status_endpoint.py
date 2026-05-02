"""
app_status_endpoint.py — Standardized /api/status for Liberty-Emporium apps
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Copy this snippet into any app's app.py.
Replace APP_NAME and the stats_fn with app-specific data.

Response shape (all apps return the same structure):
{
  "app":            "FloodClaim Pro",
  "version":        "1.0",
  "healthy":        true,
  "uptime_seconds": 3600,
  "stats":          { ... app-specific ... },
  "network":        "liberty-emporium",
  "ts":             "2026-05-02T18:00:00Z"
}

Auth: accepts X-Liberty-Auth or X-App-Token header with any valid
ECDASH_APP_TOKEN (inter-app calls) OR no auth (public health check).
"""

# ── Paste this block into your app.py ─────────────────────────────────────────

_STATUS_SNIPPET = '''
import time as _time
from datetime import datetime, timezone

_APP_START_TIME = _time.time()

@app.route('/api/status', methods=['GET'])
def api_status():
    """Standardized status endpoint for Liberty-Emporium app network."""
    uptime = int(_time.time() - _APP_START_TIME)
    stats  = _get_app_stats()   # implement per-app below
    return jsonify({
        "app":            APP_NAME,
        "version":        APP_VERSION,
        "healthy":        True,
        "uptime_seconds": uptime,
        "uptime_human":   _fmt_uptime(uptime),
        "stats":          stats,
        "network":        "liberty-emporium",
        "ts":             datetime.now(timezone.utc).isoformat(),
    })

def _fmt_uptime(s):
    if s < 60:   return f"{s}s"
    if s < 3600: return f"{s//60}m {s%60}s"
    h = s // 3600; m = (s % 3600) // 60
    return f"{h}h {m}m"
'''

# ── Per-app stats functions (reference implementations) ───────────────────────

STATS_FLOODCLAIM = '''
def _get_app_stats():
    """FloodClaim Pro — claims + photos stats."""
    try:
        db = get_db()
        claims     = db.execute("SELECT COUNT(*) FROM claims").fetchone()[0]
        open_cl    = db.execute("SELECT COUNT(*) FROM claims WHERE status NOT IN ('closed','paid')").fetchone()[0]
        photos     = db.execute("SELECT COUNT(*) FROM photos").fetchone()[0]
        return {"total_claims": claims, "open_claims": open_cl, "total_photos": photos}
    except Exception as e:
        return {"error": str(e)}
'''

STATS_PETVET = '''
def _get_app_stats():
    """Pet Vet AI — users + diagnoses stats."""
    try:
        users     = len(load_users()) if callable(globals().get("load_users")) else 0
        diag_file = os.path.join(DATA_DIR, "diagnoses.json")
        diagnoses = len(json.load(open(diag_file))) if os.path.exists(diag_file) else 0
        return {"total_users": users, "total_diagnoses": diagnoses}
    except Exception as e:
        return {"error": str(e)}
'''

STATS_WIDGET = '''
def _get_app_stats():
    """AI Agent Widget — agents + chats stats."""
    try:
        db     = get_db()
        agents = db.execute("SELECT COUNT(*) FROM agents").fetchone()[0]
        chats  = db.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
        return {"total_agents": agents, "total_messages": chats}
    except Exception as e:
        return {"error": str(e)}
'''

STATS_GENERIC = '''
def _get_app_stats():
    """Generic stats — override per app."""
    return {"status": "ok"}
'''
