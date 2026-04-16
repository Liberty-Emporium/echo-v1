#!/usr/bin/env python3
"""
fix-all-forms.py — Add csrf_token hidden input to every POST form that's missing it.
Usage: python3 fix-all-forms.py <templates-dir>
"""
import os, re, sys

TEMPLATES_DIR = sys.argv[1] if len(sys.argv) > 1 else "templates"

def patch_file(path):
    content = open(path).read()
    changed = False

    # Find all <form method="POST"> or <form method="post"> that DON'T have csrf_token
    def add_csrf(m):
        form_tag = m.group(0)
        # Look ahead in content from this form's position
        return form_tag

    # Strategy: find form...> that is POST and next line doesn't have csrf
    pattern = r'(<form[^>]+method=["\'](?:POST|post)["\'][^>]*>)(\s*)(?!.*csrf_token)'
    def replacer(m):
        full = m.group(0)
        if 'csrf_token' in full:
            return full
        tag = m.group(1)
        ws  = m.group(2)
        return f'{tag}{ws}    <input type="hidden" name="csrf_token" value="{{{{ csrf_token() }}}}">{ws}'

    new = re.sub(pattern, replacer, content, flags=re.DOTALL)
    if new != content:
        content = new
        changed = True

    if changed:
        open(path, 'w').write(content)
        print(f"  ✅ {os.path.basename(path)}")
    else:
        print(f"  ⏭  {os.path.basename(path)} (no changes)")

count = 0
for fname in sorted(os.listdir(TEMPLATES_DIR)):
    if fname.endswith('.html'):
        patch_file(os.path.join(TEMPLATES_DIR, fname))
        count += 1

print(f"\n✅ Scanned {count} templates")
