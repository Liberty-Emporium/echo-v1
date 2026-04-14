#!/usr/bin/env python3
"""
app-tester — End-to-end test suite for Jay's Flask apps
Usage: python3 test_app.py --url <URL> --user <username> --pass <password>
"""
import sys
import argparse
import urllib.request
import urllib.parse
import urllib.error
import json
import time

PASS = "\033[92m[PASS]\033[0m"
FAIL = "\033[91m[FAIL]\033[0m"
WARN = "\033[93m[WARN]\033[0m"
INFO = "\033[94m[INFO]\033[0m"

results = []

def test(name, passed, detail=""):
    status = PASS if passed else FAIL
    print(f"{status} {name}" + (f" — {detail}" if detail else ""))
    results.append((name, passed, detail))

def get(url, cookies=None, follow_redirects=False, timeout=10):
    req = urllib.request.Request(url)
    if cookies:
        req.add_header("Cookie", "; ".join(f"{k}={v}" for k, v in cookies.items()))
    try:
        if follow_redirects:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.status, r.read().decode("utf-8", errors="ignore"), dict(r.headers)
        else:
            opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor())
            opener.addheaders = [("Cookie", "; ".join(f"{k}={v}" for k, v in (cookies or {}).items()))]
            # Don't follow redirects
            class NoRedirect(urllib.request.HTTPRedirectHandler):
                def redirect_request(self, *args): return None
            opener2 = urllib.request.build_opener(NoRedirect())
            with opener2.open(req, timeout=timeout) as r:
                return r.status, r.read().decode("utf-8", errors="ignore"), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="ignore"), dict(e.headers)
    except Exception as e:
        return 0, str(e), {}

def post(url, data, cookies=None, timeout=10):
    encoded = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=encoded, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    if cookies:
        req.add_header("Cookie", "; ".join(f"{k}={v}" for k, v in cookies.items()))
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

def run_tests(base_url, username, password):
    base_url = base_url.rstrip("/")
    print(f"\n{INFO} Testing: {base_url}")
    print(f"{INFO} User: {username}\n")
    print("=" * 60)

    # ── 1. Health / Uptime ────────────────────────────────────────
    print("\n[Health Checks]")
    code, body, _ = get(f"{base_url}/login")
    test("App is up (/login responds)", code == 200, f"HTTP {code}")

    code, body, _ = get(f"{base_url}/health")
    if code == 200:
        try:
            data = json.loads(body)
            test("/health endpoint", data.get("status") == "ok", body[:100])
        except Exception:
            test("/health endpoint", False, f"Non-JSON response: {body[:80]}")
    else:
        test("/health endpoint", False, f"HTTP {code} — route may not exist yet")

    code, body, _ = get(f"{base_url}/ping")
    test("/ping endpoint", code == 200, f"HTTP {code}")

    # ── 2. Security Headers ───────────────────────────────────────
    print("\n[Security Headers]")
    code, body, headers = get(f"{base_url}/login")
    h = {k.lower(): v for k, v in headers.items()}
    test("X-Frame-Options header", "x-frame-options" in h, h.get("x-frame-options", "MISSING"))
    test("X-Content-Type-Options header", "x-content-type-options" in h, h.get("x-content-type-options", "MISSING"))
    test("Content-Security-Policy header", "content-security-policy" in h, "present" if "content-security-policy" in h else "MISSING")

    # ── 3. Auth Tests ─────────────────────────────────────────────
    print("\n[Auth Tests]")

    # Bad credentials
    code, body, headers = post(f"{base_url}/login", {"username": "baduser", "password": "badpass"})
    rejected = code in (200, 401, 403) and ("invalid" in body.lower() or "incorrect" in body.lower() or code in (401, 403))
    test("Bad credentials rejected", rejected, f"HTTP {code}")

    # Good credentials
    code, body, headers = post(f"{base_url}/login", {"username": username, "password": password})
    h = {k.lower(): v for k, v in headers.items()}
    login_ok = code in (302, 303) or (code == 200 and "dashboard" in body.lower())
    test("Valid login accepted", login_ok, f"HTTP {code} location={h.get('location','')}")

    # Get session cookie
    session_cookie = None
    if "set-cookie" in h:
        for part in h["set-cookie"].split(";"):
            if "session=" in part:
                session_cookie = part.strip().replace("session=", "")
                break
    cookies = {"session": session_cookie} if session_cookie else {}

    # Access protected route without login
    code, body, headers = get(f"{base_url}/dashboard")
    h2 = {k.lower(): v for k, v in headers.items()}
    redirected = code in (301, 302, 303) and "login" in h2.get("location", "")
    test("Protected route redirects unauthenticated", redirected, f"HTTP {code} → {h2.get('location','')}")

    # ── 4. SQL Injection Quick Test ───────────────────────────────
    print("\n[SQL Injection]")
    code, body, _ = post(f"{base_url}/login", {"username": "' OR '1'='1", "password": "' OR '1'='1"})
    not_logged_in = code not in (302, 303) or "dashboard" not in body.lower()
    test("SQL injection on login blocked", not_logged_in, f"HTTP {code}")

    code, body, _ = post(f"{base_url}/login", {"username": "admin'--", "password": "x"})
    not_logged_in2 = code not in (302, 303) or "dashboard" not in body.lower()
    test("SQL comment injection blocked", not_logged_in2, f"HTTP {code}")

    # ── 5. XSS Quick Test ────────────────────────────────────────
    print("\n[XSS]")
    xss_payload = "<script>alert('xss')</script>"
    code, body, _ = post(f"{base_url}/login", {"username": xss_payload, "password": "x"})
    escaped = xss_payload not in body and "&lt;script&gt;" in body or xss_payload not in body
    test("XSS payload not reflected raw in login", escaped, "payload escaped or not reflected")

    # ── 6. Rate Limiting ─────────────────────────────────────────
    print("\n[Rate Limiting]")
    got_429 = False
    for i in range(12):
        code, _, _ = post(f"{base_url}/login", {"username": "ratelimitcheck", "password": "wrong"})
        if code == 429:
            got_429 = True
            break
        time.sleep(0.1)
    test("Rate limiting on login (429 after rapid attempts)", got_429, "429 received" if got_429 else "no 429 after 12 attempts")

    # ── 7. Admin Route Protection ────────────────────────────────
    print("\n[Admin Protection]")
    for route in ["/admin/users", "/overseer", "/admin/backups"]:
        code, body, h3 = get(f"{base_url}{route}")
        h3l = {k.lower(): v for k, v in h3.items()}
        protected = code in (301, 302, 303) or (code == 200 and "login" in body.lower()[:500])
        test(f"{route} requires auth", protected, f"HTTP {code}")

    # ── Summary ───────────────────────────────────────────────────
    print("\n" + "=" * 60)
    passed = sum(1 for _, p, _ in results if p)
    failed = sum(1 for _, p, _ in results if not p)
    print(f"\n{'PASS' if failed == 0 else 'RESULTS'}: {passed} passed, {failed} failed out of {len(results)} tests")
    if failed > 0:
        print("\nFailed tests:")
        for name, p, detail in results:
            if not p:
                print(f"  ✗ {name}: {detail}")
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test a Jay Liberty app")
    parser.add_argument("--url", required=True, help="Base URL of app")
    parser.add_argument("--user", default="admin", help="Admin username")
    parser.add_argument("--pass", dest="password", default="admin1", help="Admin password")
    args = parser.parse_args()
    sys.exit(run_tests(args.url, args.user, args.password))
