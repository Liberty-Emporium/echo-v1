#!/usr/bin/env python3
"""
check_agent_status.py — Check Liberty Agent status across all machines in the dashboard.

Usage:
  python3 check_agent_status.py           # show all machines
  python3 check_agent_status.py online    # only online machines
  python3 check_agent_status.py offline   # only offline machines
"""
import json, sys, urllib.request

BASE = "https://agents.alexanderai.site"

def get_token():
    data = json.dumps({"username": "jay", "password": "Treetop121570!"}).encode()
    req = urllib.request.Request(f"{BASE}/api/login", data=data,
          headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=15).read())["token"]

def main():
    filter_mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    token = get_token()
    req = urllib.request.Request(f"{BASE}/api/machines",
          headers={"Authorization": f"Bearer {token}"})
    machines = json.loads(urllib.request.urlopen(req, timeout=10).read())

    online = [m for m in machines if m.get("online")]
    offline = [m for m in machines if not m.get("online")]

    print(f"\n{'='*60}")
    print(f"  Alexander AI Support Dashboard — Machine Status")
    print(f"  🟢 {len(online)} online  |  ⚫ {len(offline)} offline  |  {len(machines)} total")
    print(f"{'='*60}\n")

    show = machines
    if filter_mode == "online":
        show = online
    elif filter_mode == "offline":
        show = offline

    for m in show:
        status = "🟢 ONLINE " if m.get("online") else "⚫ OFFLINE"
        hostname = m.get("hostname") or "unknown"
        os_info = f"{m.get('os', '')} {m.get('os_release', '')}".strip() or "unknown OS"
        machine_id = m.get("machine_id", "")[:16] + "..."
        client_id = m.get("client_id") or "⚠️  NOT LINKED"
        disk = ""
        if m.get("disk_free_gb") and m.get("disk_total_gb"):
            disk = f"  💾 {m['disk_free_gb']:.1f}/{m['disk_total_gb']:.1f}GB free"
        last_seen = m.get("last_seen", "never")

        print(f"{status} {hostname}")
        print(f"  ID: {machine_id}  Client: {client_id}")
        print(f"  OS: {os_info}{disk}")
        print(f"  Last seen: {last_seen}")
        print()

if __name__ == "__main__":
    main()
