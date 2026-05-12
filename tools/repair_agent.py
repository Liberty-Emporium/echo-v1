#!/usr/bin/env python3
"""
repair_agent.py — KiloClaw's autonomous repair engine.

How it works:
  1. KiloClaw receives a repair task (machine_id + problem description)
  2. This script SSHes into the customer machine via Tailscale IP
  3. Runs a structured diagnosis sequence
  4. Applies the appropriate fix from the repair playbook
  5. Returns a human-readable repair report

Usage (from KiloClaw shell):
  python3 repair_agent.py --machine-ip 100.x.x.x --user mingo --problem "hermes crashed"
  python3 repair_agent.py --machine-ip 100.x.x.x --user mingo --diagnose-only

Or import as a module:
  from repair_agent import RepairSession
  session = RepairSession(ip="100.x.x.x", user="mingo")
  report = session.repair("hermes service keeps crashing")
"""

import argparse
import subprocess
import sys
import json
from datetime import datetime
from pathlib import Path

SSH_KEY = "/root/.ssh/id_ed25519"
SSH_OPTS = [
    "-o", "StrictHostKeyChecking=no",
    "-o", "UserKnownHostsFile=/dev/null",
    "-o", "ConnectTimeout=10",
    "-o", "BatchMode=yes",          # never prompt for password
    # Route through Tailscale SOCKS5 proxy (required for userspace-networking mode)
    "-o", "ProxyCommand=nc -X 5 -x localhost:1055 %h %p",
]


class RepairSession:
    def __init__(self, ip: str, user: str = None, agent_type: str = "hermes"):
        self.ip         = ip
        self.user       = user or self._guess_user()
        self.agent_type = agent_type
        self.log        = []
        self.fixes      = []

    def _guess_user(self):
        # Common usernames to try in order
        for u in ["mingo", "ubuntu", "pi", "user", "admin", "root"]:
            r = self.run(f"echo ok", user=u, quiet=True)
            if r["rc"] == 0:
                return u
        return "user"

    # ── Core SSH runner ───────────────────────────────────────────────────────
    def run(self, cmd: str, user: str = None, timeout: int = 30, quiet: bool = False) -> dict:
        u = user or self.user
        full_cmd = ["ssh", *SSH_OPTS, "-i", SSH_KEY, f"{u}@{self.ip}", cmd]
        try:
            result = subprocess.run(
                full_cmd,
                capture_output=True, text=True, timeout=timeout
            )
            output = (result.stdout + result.stderr).strip()
            entry = {"cmd": cmd, "rc": result.returncode, "output": output[:2000]}
            if not quiet:
                self.log.append(entry)
            return entry
        except subprocess.TimeoutExpired:
            entry = {"cmd": cmd, "rc": -1, "output": f"[TIMEOUT after {timeout}s]"}
            if not quiet:
                self.log.append(entry)
            return entry
        except Exception as e:
            entry = {"cmd": cmd, "rc": -1, "output": f"[ERROR: {e}]"}
            if not quiet:
                self.log.append(entry)
            return entry

    def run_sudo(self, cmd: str, timeout: int = 60) -> dict:
        return self.run(f"sudo {cmd}", timeout=timeout)

    # ── Connectivity check ────────────────────────────────────────────────────
    def check_reachable(self) -> bool:
        r = self.run("echo ALIVE", quiet=True)
        return r["rc"] == 0 and "ALIVE" in r["output"]

    # ── Full diagnosis ────────────────────────────────────────────────────────
    def diagnose(self) -> dict:
        """Run a full system health check. Returns structured findings."""
        d = {}

        # Basic system
        d["hostname"]  = self.run("hostname")["output"]
        d["uptime"]    = self.run("uptime -p")["output"]
        d["disk"]      = self.run("df -h / | tail -1")["output"]
        d["memory"]    = self.run("free -h | grep Mem")["output"]
        d["load"]      = self.run("cat /proc/loadavg")["output"]

        # Disk warning
        disk_pct_str = self.run("df / | tail -1 | awk '{print $5}'")["output"]
        try:
            d["disk_pct"] = int(disk_pct_str.replace("%", "").strip())
        except Exception:
            d["disk_pct"] = 0

        # Hermes-specific
        if self.agent_type == "hermes":
            d["hermes_service"] = self.run(
                "systemctl --user is-active hermes 2>/dev/null || echo inactive"
            )["output"]
            d["hermes_version"] = self.run(
                "hermes --version 2>/dev/null || echo not-found"
            )["output"]
            d["hermes_logs"] = self.run(
                "journalctl --user -u hermes -n 30 --no-pager 2>/dev/null || "
                "tail -30 ~/.hermes/logs/hermes.log 2>/dev/null || echo no-logs"
            )["output"]
            d["pnpm_dev"] = self.run(
                "pgrep -a node | grep 'pnpm\\|hermes-workspace' | head -3"
            )["output"]

        # Agent Zero-specific
        if self.agent_type == "agent-zero":
            d["docker_status"] = self.run(
                "docker ps --filter name=agent-zero --format '{{.Status}}' 2>/dev/null || echo docker-unavailable"
            )["output"]
            d["docker_logs"] = self.run(
                "docker logs agent-zero --tail 30 2>/dev/null || echo no-container"
            )["output"]

        # Liberty Agent
        d["liberty_agent"] = self.run(
            "pgrep -f liberty_agent.py >/dev/null && echo running || echo stopped"
        )["output"]
        d["liberty_logs"] = self.run(
            "tail -20 ~/.liberty-agent/agent.log 2>/dev/null || echo no-log"
        )["output"]

        # Network
        d["tailscale"]   = self.run("tailscale status 2>/dev/null | head -3")["output"]
        d["internet"]    = self.run("curl -s --max-time 5 https://1.1.1.1 >/dev/null && echo ok || echo no-internet")["output"]
        d["python"]      = self.run("python3 --version 2>&1")["output"]

        # Recent errors in system journal
        d["recent_errors"] = self.run(
            "journalctl -p err -n 10 --no-pager 2>/dev/null | tail -10 || echo unavailable"
        )["output"]

        return d

    # ── Repair playbook ───────────────────────────────────────────────────────
    def repair(self, problem: str) -> dict:
        """
        Diagnose and fix. Returns a repair report dict.
        problem: free-text description (e.g. "hermes crashed", "disk full")
        """
        started_at = datetime.utcnow().isoformat()
        self.log = []
        self.fixes = []

        # Step 1: connectivity
        if not self.check_reachable():
            return self._report(
                status="failed",
                summary="Cannot reach machine via SSH. Tailscale may be down.",
                started_at=started_at
            )

        # Step 2: diagnose
        findings = self.diagnose()

        # Step 3: apply fixes based on findings + problem description
        prob = problem.lower()

        # ── Fix: Disk full ────────────────────────────────────────────────
        if findings.get("disk_pct", 0) >= 90 or "disk" in prob or "space" in prob or "full" in prob:
            self._fix_disk_full()

        # ── Fix: Hermes crashed / not running ─────────────────────────────
        if self.agent_type == "hermes" and (
            findings.get("hermes_service") != "active"
            or "hermes" in prob or "crash" in prob or "restart" in prob
        ):
            self._fix_hermes(findings)

        # ── Fix: Agent Zero down ──────────────────────────────────────────
        if self.agent_type == "agent-zero" and (
            "not running" in findings.get("docker_status", "")
            or "agent-zero" in prob or "docker" in prob
        ):
            self._fix_agent_zero(findings)

        # ── Fix: Liberty Agent stopped ────────────────────────────────────
        if findings.get("liberty_agent") == "stopped" or "liberty" in prob:
            self._fix_liberty_agent()

        # ── Fix: Python/pip broken ────────────────────────────────────────
        if "python" in prob or "pip" in prob or "module" in prob or "import" in prob:
            self._fix_python_env()

        # ── Fix: No internet ─────────────────────────────────────────────
        if findings.get("internet") == "no-internet" or "internet" in prob or "network" in prob:
            self._fix_network()

        # Step 4: verify fixes worked
        post = self.diagnose()

        return self._report(
            status="complete",
            summary=self._summarize(findings, post, problem),
            findings=findings,
            post_findings=post,
            started_at=started_at
        )

    # ── Individual fixes ──────────────────────────────────────────────────────
    def _fix_disk_full(self):
        self.fixes.append("disk_cleanup")
        # Clear package cache, logs, tmp files
        cmds = [
            "sudo apt-get clean -y 2>/dev/null || true",
            "sudo journalctl --vacuum-size=100M 2>/dev/null || true",
            "sudo find /tmp -type f -atime +7 -delete 2>/dev/null || true",
            "sudo find /var/log -name '*.gz' -delete 2>/dev/null || true",
            "docker system prune -f 2>/dev/null || true",
            "pip cache purge 2>/dev/null || true",
        ]
        for cmd in cmds:
            self.run(cmd)

    def _fix_hermes(self, findings: dict):
        self.fixes.append("hermes_restart")
        logs = findings.get("hermes_logs", "")

        # Check for known error patterns
        if "EADDRINUSE" in logs or "address already in use" in logs.lower():
            # Port conflict — kill the old process
            self.run("pkill -f 'hermes gateway' 2>/dev/null || true")
            self.run("sleep 2")

        if "Cannot find module" in logs or "MODULE_NOT_FOUND" in logs:
            # Broken node_modules — reinstall
            self.fixes.append("hermes_reinstall_deps")
            self.run("cd ~/hermes-workspace && pnpm install --silent 2>/dev/null || true", timeout=120)

        if "python" in logs.lower() and ("not found" in logs.lower() or "error" in logs.lower()):
            self._fix_python_env()

        # Restart hermes gateway
        self.run("pkill -f 'hermes gateway' 2>/dev/null || true")
        self.run("sleep 1")
        self.run(
            "cd ~/hermes-workspace && nohup hermes gateway run >> ~/.hermes/logs/gateway.log 2>&1 &",
            timeout=15
        )
        self.run("sleep 3")

        # Restart systemd service if it exists
        self.run("systemctl --user restart hermes 2>/dev/null || true")

    def _fix_agent_zero(self, findings: dict):
        self.fixes.append("agent_zero_restart")
        self.run("docker restart agent-zero 2>/dev/null || true")
        self.run("sleep 3")
        # If container doesn't exist, try to recreate
        if "no-container" in findings.get("docker_logs", ""):
            self.fixes.append("agent_zero_recreate")
            self.run(
                "docker run -d --name agent-zero --restart=unless-stopped "
                "-p 50001:50001 frdel/agent-zero-run 2>/dev/null || true",
                timeout=60
            )

    def _fix_liberty_agent(self):
        self.fixes.append("liberty_agent_restart")
        self.run("pkill -f liberty_agent.py 2>/dev/null || true")
        self.run("sleep 1")
        self.run(
            "nohup python3 ~/liberty_agent.py >> ~/.liberty-agent/agent.log 2>&1 &",
            timeout=10
        )

    def _fix_python_env(self):
        self.fixes.append("python_env_repair")
        self.run(
            "curl -sS https://bootstrap.pypa.io/get-pip.py | python3 - --break-system-packages --quiet 2>/dev/null || true",
            timeout=60
        )
        self.run(
            "python3 -m pip install 'python-socketio[client]' websocket-client --break-system-packages --quiet 2>/dev/null || true",
            timeout=60
        )

    def _fix_network(self):
        self.fixes.append("network_check")
        self.run("sudo ip link set eth0 up 2>/dev/null || true")
        self.run("sudo dhclient eth0 2>/dev/null || true")
        self.run("ping -c 2 8.8.8.8 2>/dev/null || true")

    # ── Report generation ─────────────────────────────────────────────────────
    def _summarize(self, before: dict, after: dict, problem: str) -> str:
        lines = [f"Repair completed for: {problem}"]
        lines.append(f"Machine: {before.get('hostname', self.ip)} ({self.ip})")

        if self.fixes:
            lines.append(f"Fixes applied: {', '.join(self.fixes)}")
        else:
            lines.append("No fixes needed — system appears healthy")

        # Before/after key metrics
        if "hermes_service" in before:
            b = before["hermes_service"]
            a = after.get("hermes_service", "?")
            status = "✅" if a == "active" else "⚠️"
            lines.append(f"Hermes: {b} → {a} {status}")

        if "docker_status" in before:
            b = before["docker_status"]
            a = after.get("docker_status", "?")
            status = "✅" if "Up" in a else "⚠️"
            lines.append(f"Agent Zero: {b} → {a} {status}")

        b_disk = before.get("disk_pct", 0)
        a_disk = after.get("disk_pct", 0)
        if b_disk != a_disk:
            lines.append(f"Disk usage: {b_disk}% → {a_disk}%")

        b_lib = before.get("liberty_agent", "?")
        a_lib = after.get("liberty_agent", "?")
        if b_lib != a_lib:
            lines.append(f"Liberty Agent: {b_lib} → {a_lib}")

        return "\n".join(lines)

    def _report(self, status: str, summary: str, findings: dict = None,
                post_findings: dict = None, started_at: str = "") -> dict:
        return {
            "status":        status,
            "summary":       summary,
            "machine_ip":    self.ip,
            "user":          self.user,
            "agent_type":    self.agent_type,
            "fixes_applied": self.fixes,
            "started_at":    started_at,
            "finished_at":   datetime.utcnow().isoformat(),
            "ssh_log":       self.log,
            "findings":      findings or {},
            "post_findings": post_findings or {},
        }


# ── CLI entry point ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="KiloClaw Repair Agent")
    parser.add_argument("--machine-ip",     required=True, help="Tailscale IP of customer machine")
    parser.add_argument("--user",           default=None,  help="SSH username (auto-detected if omitted)")
    parser.add_argument("--agent-type",     default="hermes", choices=["hermes", "agent-zero"])
    parser.add_argument("--problem",        default="",    help="Problem description")
    parser.add_argument("--diagnose-only",  action="store_true", help="Run diagnosis only, no fixes")
    parser.add_argument("--json",           action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    session = RepairSession(ip=args.machine_ip, user=args.user, agent_type=args.agent_type)

    print(f"🔧 Connecting to {args.machine_ip}...")
    if not session.check_reachable():
        print(f"❌ Cannot reach {args.machine_ip} via SSH")
        print("   Check: tailscale status, SSH server running, authorized_keys")
        sys.exit(1)

    print(f"✅ Connected as {session.user}@{args.machine_ip}")

    if args.diagnose_only:
        print("\n🔍 Running diagnosis...\n")
        findings = session.diagnose()
        if args.json:
            print(json.dumps(findings, indent=2))
        else:
            for k, v in findings.items():
                if v and v != "unavailable":
                    print(f"  {k:20s}: {str(v)[:80]}")
        sys.exit(0)

    print(f"\n🔧 Repairing: '{args.problem}'\n")
    report = session.repair(args.problem)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("\n" + "="*60)
        print(report["summary"])
        print("="*60)
        print(f"Status:  {report['status']}")
        print(f"Fixes:   {', '.join(report['fixes_applied']) or 'none needed'}")
        print(f"Time:    {report['started_at'][:19]} → {report['finished_at'][:19]}")
