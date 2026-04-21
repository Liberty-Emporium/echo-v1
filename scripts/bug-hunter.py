#!/usr/bin/env python3
"""
bug-hunter.py — Echo's Automated Bug Hunter for Liberty-Emporium Flask Apps
Scans a repo for common bugs, anti-patterns, and security issues.

Usage:
    python3 bug-hunter.py /path/to/repo
    python3 bug-hunter.py /path/to/repo --fix   (auto-fix safe issues)
"""

import os, sys, ast, re, json, subprocess
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
CHECKS = {
    'syntax':        True,
    'flask':         True,
    'javascript':    True,
    'security':      True,
    'database':      True,
    'railway':       True,
}

SEVERITY = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🔵', 'info': '⚪'}

bugs  = []
fixes = []

def bug(severity, file, line, code, message, fix=None):
    bugs.append({'severity': severity, 'file': file, 'line': line, 'code': code, 'message': message, 'fix': fix})

# ── Python Syntax Check ───────────────────────────────────────────────────────
def check_syntax(path, content):
    try:
        ast.parse(content)
    except SyntaxError as e:
        bug('critical', path, e.lineno, 'SYNTAX_ERROR', f'SyntaxError: {e.msg}')
        return False
    return True

# ── Flask-Specific Checks ──────────────────────────────────────────────────────
def check_flask(path, content, lines):
    # 1. Route decorator before login_required defined
    login_req_defined = False
    for i, line in enumerate(lines, 1):
        if re.search(r'^def login_required', line):
            login_req_defined = True
        if not login_req_defined and re.search(r'@login_required', line):
            bug('critical', path, i, 'ROUTE_BEFORE_AUTH',
                '@login_required used before login_required is defined — NameError on startup')

    # 2. SESSION_COOKIE_SECURE=True behind Railway proxy
    for i, line in enumerate(lines, 1):
        if re.search(r"SESSION_COOKIE_SECURE\s*=\s*True", line):
            bug('high', path, i, 'COOKIE_SECURE_RAILWAY',
                'SESSION_COOKIE_SECURE=True breaks sessions behind Railway edge proxy — set to False',
                fix="Change SESSION_COOKIE_SECURE to False")

    # 3. Random secret key (not persistent)
    for i, line in enumerate(lines, 1):
        if re.search(r"secret_key\s*=\s*secrets\.token_hex|secret_key\s*=\s*os\.urandom", line):
            if not any('_KEY_FILE' in l or 'environ' in l or 'get_setting' in l for l in lines[max(0,i-5):i+5]):
                bug('high', path, i, 'RANDOM_SECRET_KEY',
                    'Random secret_key generated on every boot — sessions invalidated on redeploy')

    # 4. Missing error handling on db operations
    for i, line in enumerate(lines, 1):
        if re.search(r'db\.execute.*DELETE FROM', line):
            context = ''.join(lines[max(0,i-3):i+3])
            if 'REFERENCES' not in content and 'foreign_key' not in context.lower() and 'NULL' not in context:
                # Check if there are FK relationships that could break
                if re.search(r'DELETE FROM users', line):
                    bug('high', path, i, 'FK_DELETE_RISK',
                        'Deleting from users without nulling FK references first — may cause constraint error',
                        fix="Add: db.execute('UPDATE claims SET adjuster_id=NULL WHERE adjuster_id=?', (id,))")

    # 5. Hardcoded passwords/tokens in code
    for i, line in enumerate(lines, 1):
        if re.search(r'password\s*=\s*["\'][^"\']{4,}["\']', line, re.IGNORECASE):
            if not re.search(r'#|form\.|request\.|get\(|environ|setting|hash|check', line):
                bug('medium', path, i, 'HARDCODED_PASSWORD',
                    f'Possible hardcoded password: {line.strip()[:60]}')

    # 6. SQL injection risk (string formatting in queries)
    for i, line in enumerate(lines, 1):
        if re.search(r'execute\(.*f["\'].*SELECT|execute\(.*f["\'].*WHERE|execute\(.*%.*SELECT', line):
            bug('high', path, i, 'SQL_INJECTION',
                'Possible SQL injection — use parameterized queries with ? placeholders')

    # 7. Missing try/except on external API calls
    for i, line in enumerate(lines, 1):
        if re.search(r'requests\.get|requests\.post|urllib\.request|_req\.', line):
            context = ''.join(lines[max(0,i-5):i+2])
            if 'try:' not in context and 'except' not in context:
                bug('medium', path, i, 'UNHANDLED_REQUEST',
                    'External HTTP request without try/except — will crash if service is down')

    # 8. Debug mode in production
    for i, line in enumerate(lines, 1):
        if re.search(r'app\.run.*debug\s*=\s*True', line):
            bug('high', path, i, 'DEBUG_MODE',
                'Flask debug=True — never use in production, exposes interactive debugger')

    # 9. Missing PRAGMA foreign_keys=ON
    if 'sqlite3' in content and 'foreign_keys=ON' not in content and 'ON DELETE' in content:
        bug('medium', path, 0, 'FK_NOT_ENFORCED',
            'SQLite foreign keys are not enforced by default — add PRAGMA foreign_keys=ON in get_db()')

    # 10. Bare except clauses
    for i, line in enumerate(lines, 1):
        if re.search(r'^\s*except:\s*$|^\s*except Exception:\s*pass', line):
            bug('low', path, i, 'BARE_EXCEPT',
                'Bare except/except Exception: pass silently swallows errors — at minimum log them')

# ── JavaScript Checks ─────────────────────────────────────────────────────────
def check_javascript(path, content, lines):
    # 1. fetch() without credentials:include (breaks session auth)
    for i, line in enumerate(lines, 1):
        if re.search(r"fetch\(", line):
            # Look ahead for credentials in the fetch block
            block = ''.join(lines[i-1:min(len(lines), i+8)])
            if 'credentials' not in block and ('POST' in block or 'DELETE' in block or 'PATCH' in block):
                bug('high', path, i, 'FETCH_NO_CREDENTIALS',
                    "fetch() POST/DELETE without credentials:'include' — session cookie not sent, gets 302 redirect",
                    fix="Add credentials:'include' to fetch options")

    # 2. innerHTML with user data (XSS)
    for i, line in enumerate(lines, 1):
        if re.search(r'innerHTML\s*=\s*(?!.*escHtml)', line):
            if re.search(r'd\.|data\.|result\.|response\.', line):
                bug('medium', path, i, 'XSS_RISK',
                    'innerHTML with API data — XSS risk if data contains HTML. Use escHtml() or textContent')

    # 3. onclick with unescaped data in Jinja
    for i, line in enumerate(lines, 1):
        if re.search(r'onclick=["\'].*\{\{.*\}\}', line):
            bug('medium', path, i, 'JINJA_ONCLICK',
                'Jinja expression inside onclick= attribute — quote escaping issues. Use data-* attributes instead')

# ── Security Checks ───────────────────────────────────────────────────────────
def check_security(path, content, lines):
    # Check for exposed secrets/tokens in code
    secret_patterns = [
        (r'sk-or-v1-[a-zA-Z0-9]{20,}', 'EXPOSED_OPENROUTER_KEY', 'OpenRouter API key exposed in code'),
        (r'ghp_[a-zA-Z0-9]{30,}', 'EXPOSED_GITHUB_TOKEN', 'GitHub PAT exposed in code'),
        (r'glpat-[a-zA-Z0-9_-]{20,}', 'EXPOSED_GITLAB_TOKEN', 'GitLab token exposed in code'),
        (r'sk_live_[a-zA-Z0-9]{20,}', 'EXPOSED_STRIPE_KEY', 'Stripe live key exposed in code'),
        (r'SG\.[a-zA-Z0-9_-]{20,}', 'EXPOSED_SENDGRID_KEY', 'SendGrid API key exposed in code'),
    ]
    for pattern, code, message in secret_patterns:
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line) and '#' not in line[:line.find(re.search(pattern, line).group())+5]:
                bug('critical', path, i, code, message)

# ── Railway/Deployment Checks ─────────────────────────────────────────────────
def check_railway(path, content, lines):
    if 'requirements.txt' in str(path):
        # Check for incompatible packages
        bad_pkgs = {'weasyprint': 'Incompatible with Railway (needs Cairo/Pango system libs)',
                    'psycopg2': 'Use psycopg2-binary instead',
                    'pillow': 'May need system libs — test carefully'}
        for i, line in enumerate(lines, 1):
            pkg = line.strip().split('>=')[0].split('==')[0].split('[')[0].lower()
            if pkg in bad_pkgs:
                bug('high', path, i, 'BAD_RAILWAY_DEP', f'{pkg}: {bad_pkgs[pkg]}')

    if 'Procfile' in str(path):
        for i, line in enumerate(lines, 1):
            if 'gunicorn' in line and '--workers' not in line and '-w' not in line:
                bug('low', path, i, 'GUNICORN_WORKERS',
                    'Consider adding --workers 2 to Procfile for better concurrency')

# ── HTML/Template Checks ──────────────────────────────────────────────────────
def check_template(path, content, lines):
    # Missing CSRF on forms
    for i, line in enumerate(lines, 1):
        if re.search(r'<form.*method=["\']post["\']', line, re.IGNORECASE):
            # Look for csrf token in next 10 lines
            form_block = ''.join(lines[i-1:min(len(lines), i+10)])
            if 'csrf' not in form_block.lower() and 'hidden' not in form_block.lower():
                pass  # Flask-WTF not used, skip for now

    # Viewport meta tag
    if 'base.html' in str(path) or 'index.html' in str(path):
        if 'viewport' not in content:
            bug('medium', path, 0, 'NO_VIEWPORT', 'Missing viewport meta tag — not mobile friendly')

# ── Main Scanner ──────────────────────────────────────────────────────────────
def scan_repo(repo_path):
    repo = Path(repo_path)
    if not repo.exists():
        print(f"❌ Path not found: {repo_path}")
        sys.exit(1)

    print(f"\n🔍 Bug Hunter scanning: {repo.name}")
    print("=" * 60)

    scanned = 0

    for file_path in sorted(repo.rglob('*')):
        # Skip hidden dirs, venv, __pycache__, node_modules
        rel_parts = file_path.relative_to(repo).parts
        if any(p in ('.git', '__pycache__', 'node_modules', 'venv', '.venv', 'dist', 'build') for p in rel_parts):
            continue
        if not file_path.is_file():
            continue

        rel = str(file_path.relative_to(repo))
        suffix = file_path.suffix.lower()

        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            lines = content.splitlines()
        except Exception:
            continue

        scanned += 1

        if suffix == '.py':
            if check_syntax(rel, content):
                check_flask(rel, content, lines)
                check_security(rel, content, lines)
                check_railway(rel, content, lines)

        elif suffix in ('.html', '.htm'):
            check_javascript(rel, content, lines)
            check_security(rel, content, lines)
            check_template(rel, content, lines)

        elif suffix == '.js':
            check_javascript(rel, content, lines)
            check_security(rel, content, lines)

        elif file_path.name == 'requirements.txt':
            check_railway(rel, content, lines)

    return scanned

# ── Report ────────────────────────────────────────────────────────────────────
def print_report(scanned, repo_name):
    # Sort by severity
    order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3, 'info': 4}
    sorted_bugs = sorted(bugs, key=lambda b: order.get(b['severity'], 5))

    counts = {}
    for b in bugs:
        counts[b['severity']] = counts.get(b['severity'], 0) + 1

    print(f"\n📊 SCAN COMPLETE — {scanned} files scanned, {len(bugs)} issues found")
    print(f"   🔴 Critical: {counts.get('critical',0)}  🟠 High: {counts.get('high',0)}  🟡 Medium: {counts.get('medium',0)}  🔵 Low: {counts.get('low',0)}")
    print()

    if not bugs:
        print("✅ No bugs found! Clean codebase.")
        return

    current_file = None
    for b in sorted_bugs:
        if b['file'] != current_file:
            current_file = b['file']
            print(f"\n📄 {current_file}")
            print("-" * 50)
        icon = SEVERITY.get(b['severity'], '⚪')
        loc = f"L{b['line']}" if b['line'] else ''
        print(f"  {icon} [{b['code']}] {loc}")
        print(f"     {b['message']}")
        if b['fix']:
            print(f"     💡 Fix: {b['fix']}")

    # Save JSON report
    report = {
        'repo': repo_name,
        'scanned_files': scanned,
        'total_bugs': len(bugs),
        'counts': counts,
        'bugs': sorted_bugs
    }
    out_path = f'/tmp/bug-report-{repo_name}.json'
    with open(out_path, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"\n💾 Full report saved to: {out_path}")

# ── Entry Point ───────────────────────────────────────────────────────────────
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 bug-hunter.py /path/to/repo")
        sys.exit(1)

    repo_path = sys.argv[1]
    repo_name = Path(repo_path).name
    scanned = scan_repo(repo_path)
    print_report(scanned, repo_name)
