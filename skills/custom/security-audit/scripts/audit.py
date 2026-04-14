#!/usr/bin/env python3
"""
security-audit — Deep security scan for Jay's Flask apps
Usage: python3 audit.py --url <URL> [--deep]
"""
import sys
import os
import subprocess
import argparse
import urllib.request
import urllib.parse
import urllib.error
import json
import datetime
import re

RED    = "\033[91m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
BLUE   = "\033[94m"
RESET  = "\033[0m"

findings = []

def finding(severity, title, detail, remediation=""):
    color = RED if severity == "CRITICAL" else YELLOW if severity == "HIGH" else BLUE
    print(f"{color}[{severity}]{RESET} {title}")
    if detail: print(f"         {detail}")
    findings.append({"severity": severity, "title": title, "detail": detail, "remediation": remediation})

def ok(title, detail=""):
    print(f"{GREEN}[OK]{RESET} {title}" + (f" — {detail}" if detail else ""))

def info(msg):
    print(f"{BLUE}[INFO]{RESET} {msg}")

def get(url, timeout=10):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "SecurityAudit/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", errors="ignore"), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, "", dict(e.headers)
    except Exception:
        return 0, "", {}

def post(url, data, timeout=10):
    encoded = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=encoded, method="POST",
                                  headers={"Content-Type": "application/x-www-form-urlencoded",
                                           "User-Agent": "SecurityAudit/1.0"})
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *args): return None
    opener = urllib.request.build_opener(NoRedirect())
    try:
        with opener.open(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", errors="ignore"), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="ignore"), dict(e.headers)
    except Exception as e:
        return 0, str(e), {}

def run_cmd(cmd, timeout=30):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as e:
        return str(e)

def check_headers(base_url):
    print(f"\n{'='*50}\n[Phase 1] Security Headers\n{'='*50}")
    code, body, headers = get(f"{base_url}/login")
    h = {k.lower(): v for k, v in headers.items()}

    required = {
        "x-frame-options": "Prevents clickjacking — add X-Frame-Options: SAMEORIGIN",
        "x-content-type-options": "Prevents MIME sniffing — add X-Content-Type-Options: nosniff",
        "content-security-policy": "Prevents XSS — add Content-Security-Policy header",
        "x-xss-protection": "Legacy XSS filter — add X-XSS-Protection: 1; mode=block",
    }
    for header, fix in required.items():
        if header in h:
            ok(f"{header}: {h[header][:60]}")
        else:
            finding("MEDIUM", f"Missing header: {header}", f"Not present on {base_url}/login", fix)

    # Check for info leakage
    if "server" in h and ("werkzeug" in h["server"].lower() or "flask" in h["server"].lower()):
        finding("LOW", "Server header reveals framework", h["server"],
                "Set SERVER_NAME env var or use nginx to hide server header")
    if "x-powered-by" in h:
        finding("LOW", "X-Powered-By header leaks info", h["x-powered-by"], "Remove X-Powered-By header")

def check_auth(base_url):
    print(f"\n{'='*50}\n[Phase 2] Authentication Security\n{'='*50}")

    # SQL injection on login
    sqli_payloads = [
        ("' OR '1'='1", "' OR '1'='1"),
        ("admin'--", "anything"),
        ("admin' #", "anything"),
        ("' UNION SELECT 1,2,3--", "x"),
    ]
    for user, pw in sqli_payloads:
        code, body, h = post(f"{base_url}/login", {"username": user, "password": pw})
        h = {k.lower(): v for k, v in h.items()}
        if code in (302, 303) and "login" not in h.get("location", "login"):
            finding("CRITICAL", f"SQL Injection bypass: {user[:30]}", f"Login succeeded with payload, redirected to {h.get('location')}", 
                    "Use parameterized queries and check for injection in all db calls")
        else:
            ok(f"SQLi blocked: {user[:30]}")

    # Test for verbose error messages
    code, body, _ = post(f"{base_url}/login", {"username": "test' AND SLEEP(5)--", "password": "x"})
    if "traceback" in body.lower() or "sqlalchemy" in body.lower() or "sqlite" in body.lower():
        finding("HIGH", "Verbose DB errors exposed in login", "Database error details visible to users",
                "Set FLASK_ENV=production and add error handlers")

def check_routes(base_url):
    print(f"\n{'='*50}\n[Phase 3] Route Discovery\n{'='*50}")

    # Common sensitive paths to check
    sensitive = [
        "/admin", "/admin/users", "/admin/backups", "/admin/settings",
        "/overseer", "/debug", "/config", "/env", "/secret",
        "/.env", "/requirements.txt", "/app.py", "/wsgi.py",
        "/static/uploads", "/data", "/backup",
    ]
    exposed = []
    for path in sensitive:
        code, body, h = get(f"{base_url}{path}")
        h = {k.lower(): v for k, v in h.items()}
        if code == 200 and "login" not in body[:200].lower():
            exposed.append(path)
            finding("HIGH", f"Sensitive route accessible without auth: {path}", f"HTTP {code}",
                    f"Add @login_required decorator to {path}")
        elif code not in (302, 303, 404, 401, 403):
            info(f"{path} → HTTP {code}")

    if not exposed:
        ok("All sensitive routes require authentication")

def check_idor(base_url):
    print(f"\n{'='*50}\n[Phase 4] IDOR / Data Isolation\n{'='*50}")
    # Test accessing other store slugs
    test_slugs = ["admin", "test", "demo", "store1", "1", "0", "../admin"]
    for slug in test_slugs:
        code, body, h = get(f"{base_url}/store/{slug}")
        h = {k.lower(): v for k, v in h.items()}
        if code == 200 and "login" not in body[:500].lower():
            finding("HIGH", f"Store data accessible without auth: /store/{slug}", f"HTTP {code}",
                    "Ensure /store/<slug> routes verify authentication")

def check_xss(base_url):
    print(f"\n{'='*50}\n[Phase 5] XSS\n{'='*50}")
    xss_payloads = [
        "<script>alert(1)</script>",
        "<img src=x onerror=alert(1)>",
        "javascript:alert(1)",
    ]
    for payload in xss_payloads:
        code, body, _ = post(f"{base_url}/login", {"username": payload, "password": "x"})
        if payload in body:
            finding("HIGH", f"XSS payload reflected unescaped", f"Payload: {payload[:50]}",
                    "Use Jinja2 autoescaping (enabled by default) — ensure |safe is not used on user input")
        else:
            ok(f"XSS payload escaped: {payload[:30]}")

def run_gobuster(base_url):
    print(f"\n{'='*50}\n[Phase 6] Hidden Route Discovery (gobuster)\n{'='*50}")
    wordlist = "/usr/share/wordlists/dirb/common.txt"
    if not os.path.exists(wordlist):
        wordlist = "/usr/share/nmap/nselib/data/wp-plugins.lst"
    if not os.path.exists(wordlist):
        info("No wordlist found — skipping gobuster. Install: apt-get install dirb")
        return
    info(f"Running gobuster with {wordlist}...")
    output = run_cmd(f"gobuster dir -u {base_url} -w {wordlist} -t 10 -q --timeout 5s 2>/dev/null", timeout=60)
    found = [line for line in output.splitlines() if "(Status:" in line and "Status: 200" in line]
    if found:
        info(f"Found {len(found)} accessible paths:")
        for f in found[:20]:
            print(f"  {f}")
    else:
        ok("No unexpected paths found via gobuster")

def save_report(base_url):
    date = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
    path = f"/tmp/security-report-{date}.md"
    with open(path, "w") as f:
        f.write(f"# Security Audit Report\n\n")
        f.write(f"**Target:** {base_url}\n")
        f.write(f"**Date:** {datetime.datetime.now().isoformat()}\n\n")
        counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for fn in findings:
            counts[fn["severity"]] = counts.get(fn["severity"], 0) + 1
        f.write(f"## Summary\n\n")
        for sev, count in counts.items():
            f.write(f"- {sev}: {count}\n")
        f.write(f"\n## Findings\n\n")
        for fn in findings:
            f.write(f"### [{fn['severity']}] {fn['title']}\n\n")
            f.write(f"**Detail:** {fn['detail']}\n\n")
            if fn['remediation']:
                f.write(f"**Fix:** {fn['remediation']}\n\n")
    print(f"\n{GREEN}Report saved to: {path}{RESET}")
    return path

def run_audit(base_url, deep=False):
    base_url = base_url.rstrip("/")
    print(f"\n{BLUE}{'='*50}")
    print(f"  SECURITY AUDIT: {base_url}")
    print(f"  {datetime.datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"{'='*50}{RESET}\n")

    check_headers(base_url)
    check_auth(base_url)
    check_routes(base_url)
    check_idor(base_url)
    check_xss(base_url)
    if deep:
        run_gobuster(base_url)

    # Summary
    print(f"\n{'='*50}")
    crits = [f for f in findings if f["severity"] == "CRITICAL"]
    highs = [f for f in findings if f["severity"] == "HIGH"]
    meds  = [f for f in findings if f["severity"] == "MEDIUM"]
    lows  = [f for f in findings if f["severity"] == "LOW"]
    print(f"\n{RED}CRITICAL: {len(crits)}{RESET}  {YELLOW}HIGH: {len(highs)}{RESET}  MEDIUM: {len(meds)}  LOW: {len(lows)}")
    report_path = save_report(base_url)
    return 1 if crits or highs else 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Security audit a Jay Liberty app")
    parser.add_argument("--url", required=True, help="Base URL of app")
    parser.add_argument("--deep", action="store_true", help="Run gobuster + extended checks")
    args = parser.parse_args()
    sys.exit(run_audit(args.url, args.deep))
