#!/usr/bin/env python3
"""
Multi-Tenant Isolation Auditor
Scans a Flask app.py for tenant data leak risks.

Usage: python3 audit_tenant_isolation.py <path_to_app.py>
"""
import sys, re, pathlib

SEVERITY = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}

def audit(filepath):
    path = pathlib.Path(filepath)
    if not path.exists():
        print(f"ERROR: {filepath} not found")
        sys.exit(1)

    code  = path.read_text()
    lines = code.splitlines()
    issues = []
    passes = []

    def check(label, passed, sev, detail=''):
        if passed:
            passes.append(label)
        else:
            issues.append((label, sev, detail))

    # ── Isolation model detection ─────────────────────────────────────────────
    is_silo = 'CUSTOMERS_DIR' in code or 'tenant_dir' in code or 'customers_dir' in code
    is_pool = 'store_slug' in code and 'WHERE' in code

    print(f"\n{'='*60}")
    print(f"  🔍 Tenant Isolation Audit: {path.name}")
    print(f"  Model detected: {'Silo (file-based)' if is_silo else 'Pool (shared DB)' if is_pool else 'Unknown'}")
    print(f"{'='*60}\n")

    # ── Check 1: get_slug() or equivalent used ────────────────────────────────
    has_get_slug = 'get_slug' in code or 'current_slug' in code
    check("Tenant slug helper function exists", has_get_slug, 'HIGH',
          "No get_slug() found — slug may come from unvalidated input")

    # ── Check 2: slug sanitization / validation ───────────────────────────────
    has_sanitize = ('sanitize' in code.lower() or 'reserved' in code.lower()
                    or '_sanitize_slug' in code or 'RESERVED' in code)
    check("Slug sanitization/validation", has_sanitize, 'HIGH',
          "No slug sanitization — path traversal risk")

    # ── Check 3: No raw user input as slug ────────────────────────────────────
    bad_slug_patterns = re.findall(
        r"request\.(args|form|json)\.get\(['\"]slug['\"]",
        code, re.IGNORECASE
    )
    check("No raw user input used as tenant slug",
          len(bad_slug_patterns) == 0, 'CRITICAL',
          f"Found {len(bad_slug_patterns)} places: slug taken from request — tenant isolation bypass risk")

    # ── Check 4: Pool model — WHERE store_slug on queries ────────────────────
    if is_pool and not is_silo:
        execute_calls = re.findall(r'\.execute\s*\(\s*["\']SELECT.*?["\']', code, re.DOTALL)
        unscoped = [q for q in execute_calls if 'store_slug' not in q.lower()]
        check("Pool model: all SELECT queries scoped to store_slug",
              len(unscoped) == 0, 'CRITICAL',
              f"{len(unscoped)} SELECT queries may lack tenant filter")
    elif not is_pool:
        passes.append("Pool model scoping (N/A — silo model)")

    # ── Check 5: Silo model — tenant_file() for all file paths ───────────────
    if is_silo:
        raw_paths = re.findall(
            r'os\.path\.join\s*\([^)]*(?:request|session|form|args)[^)]*\)',
            code
        )
        check("Silo model: no raw user input in file paths",
              len(raw_paths) == 0, 'CRITICAL',
              f"{len(raw_paths)} file paths include request/session input directly")

    # ── Check 6: Trial gate decorator ────────────────────────────────────────
    has_trial_gate = 'trial_gate' in code or '_trial_gate' in code
    check("Trial gate decorator exists", has_trial_gate, 'MEDIUM',
          "No trial_gate — expired trials can access all features")

    # ── Check 7: Overseer impersonation cleared on exit ───────────────────────
    has_impersonate = 'impersonating_slug' in code
    has_exit        = ('overseer/exit' in code or 'impersonating_slug' in code
                       and 'pop' in code)
    if has_impersonate:
        check("Overseer impersonation has exit route", has_exit, 'MEDIUM',
              "Impersonation set but no clear exit path found")
    else:
        passes.append("Overseer impersonation (N/A)")

    # ── Check 8: login_required on tenant routes ──────────────────────────────
    has_login_req = 'login_required' in code
    check("login_required decorator used", has_login_req, 'HIGH',
          "No login_required — tenant routes may be publicly accessible")

    # ── Check 9: Secret key not hardcoded ────────────────────────────────────
    bad_secret = re.search(
        r"secret_key\s*=\s*['\"][a-zA-Z0-9_\-]{8,}['\"]",
        code, re.IGNORECASE
    )
    check("No hardcoded secret key fallback", not bad_secret, 'HIGH',
          f"Hardcoded secret key found — session forgery risk")

    # ── Check 10: Plan/feature limits enforced ────────────────────────────────
    has_plan_check = ('plan_allows' in code or 'feature_gate' in code
                      or 'PLAN_LIMITS' in code or "plan ==" in code)
    check("Plan/feature limits enforced", has_plan_check, 'MEDIUM',
          "No plan enforcement found — all users get all features")

    # ── Check 11: Tenant rate limiting ───────────────────────────────────────
    has_tenant_rl = ('tenant_rate' in code or '_tenant_calls' in code)
    check("Per-tenant rate limiting", has_tenant_rl, 'LOW',
          "No per-tenant rate limiting — noisy neighbor risk")

    # ── Check 12: Tenant data export capability ───────────────────────────────
    has_export = 'export' in code.lower() and ('zipfile' in code or 'zip' in code.lower())
    check("Tenant data export", has_export, 'LOW',
          "No data export — GDPR/data portability concern")

    # ── Print results ─────────────────────────────────────────────────────────
    for label in passes:
        print(f"  ✅  {label}")
    for label, sev, detail in sorted(issues, key=lambda x: SEVERITY.get(x[1], 9)):
        print(f"  ❌  [{sev}] {label}")
        if detail:
            print(f"        ↳ {detail}")

    print(f"\n{'='*60}")
    print(f"  Score: {len(passes)}/{len(passes)+len(issues)} checks passed")
    if issues:
        crit = [i for i in issues if i[1] == 'CRITICAL']
        high = [i for i in issues if i[1] == 'HIGH']
        if crit:
            print(f"\n  🚨 {len(crit)} CRITICAL issue(s) — potential data leaks between tenants!")
        if high:
            print(f"  ⚠️  {len(high)} HIGH issue(s) — fix before going to production")
    else:
        print(f"\n  🎉 All isolation checks passed!")
    print(f"{'='*60}\n")

    return len([i for i in issues if i[1] in ('CRITICAL', 'HIGH')])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 audit_tenant_isolation.py <path_to_app.py>")
        sys.exit(1)
    sys.exit(1 if audit(sys.argv[1]) > 0 else 0)
