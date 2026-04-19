#!/usr/bin/env python3
"""
validate-flask-app.py — Pre-push sanity check for Flask app.py files
Catches the @login_required-before-definition crash before it hits Railway.

Usage: python3 validate-flask-app.py <path/to/app.py>
Exit 0 = clean, Exit 1 = broken
"""
import ast, sys

def validate(path):
    with open(path) as f:
        src = f.read()
    lines = src.split('\n')
    errors = []

    # 1. AST parse check
    try:
        ast.parse(src)
    except SyntaxError as e:
        print(f"❌ Syntax error at line {e.lineno}: {e.msg}")
        return False

    # 2. Find definition line for login_required
    login_def = next((i+1 for i,l in enumerate(lines) if 'def login_required' in l), None)
    if login_def is None:
        print("⚠️  No login_required function found — skipping order check")
    else:
        # Check no actual @login_required decorator appears before definition
        bad = [(i+1, l.strip()) for i,l in enumerate(lines)
               if l.strip() == '@login_required' and i+1 < login_def]
        if bad:
            for lineno, line in bad:
                errors.append(f"  Line {lineno}: @login_required used before defined at line {login_def}")

    # 3. Check for raw tokens (safety net)
    token_patterns = ['ghp_', 'glpat-', 'sk-or-v1-', 'sk_live_', 'SG.']
    for i, line in enumerate(lines):
        for pat in token_patterns:
            if pat in line and not line.strip().startswith('#'):
                errors.append(f"  Line {i+1}: Possible raw token ({pat}...) — use env vars instead")

    if errors:
        print(f"❌ {len(errors)} issue(s) found in {path}:")
        for e in errors:
            print(e)
        return False

    print(f"✅ {path} looks clean (AST OK, decorator order OK, no raw tokens)")
    return True

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'app.py'
    sys.exit(0 if validate(path) else 1)
