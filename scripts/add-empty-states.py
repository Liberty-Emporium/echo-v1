#!/usr/bin/env python3
"""
add-empty-states.py — Replace plain "No items" text with illustrated empty states.
Patches templates that have bare empty-list messages.
Usage: python3 add-empty-states.py <templates-dir>
"""
import os, re, sys

TEMPLATES_DIR = sys.argv[1] if len(sys.argv) > 1 else "templates"

EMPTY_STATE_CSS = """
<style>
.empty-state { text-align:center; padding:3rem 1.5rem; color:#94a3b8; }
.empty-state .empty-icon { font-size:3.5rem; margin-bottom:1rem; filter:grayscale(0.3); }
.empty-state h3 { font-size:1.15rem; font-weight:700; color:#475569; margin:0 0 0.5rem; }
.empty-state p  { font-size:0.9rem; margin:0 0 1.25rem; max-width:280px; margin-left:auto; margin-right:auto; }
.empty-state .btn-empty { display:inline-flex; align-items:center; gap:0.4rem; background:#6366f1; color:white; border:none; border-radius:10px; padding:0.65rem 1.25rem; font-weight:700; font-size:0.9rem; cursor:pointer; text-decoration:none; transition:background .2s; }
.empty-state .btn-empty:hover { background:#4f46e5; }
</style>
"""

EMPTY_STATES = {
    "products": ("📦", "No products yet", "Add your first item to get started tracking your inventory."),
    "inventory": ("📦", "No inventory yet", "Start adding products to build your inventory."),
    "orders": ("📋", "No orders yet", "Orders will appear here once customers start buying."),
    "users": ("👤", "No users yet", "Add users to give your team access."),
    "leads": ("🎯", "No leads yet", "Leads will show up here when customers contact you."),
    "bids": ("📝", "No bids yet", "Create your first bid to start winning jobs."),
    "backups": ("💾", "No backups yet", "Backups will appear here after your first save."),
    "keys": ("🔑", "No API keys yet", "Add your first API key to get started."),
    "vendors": ("🏪", "No vendors yet", "Add your first vendor to start managing consignments."),
    "items": ("🏷️", "No items yet", "Add items to start tracking your consignment inventory."),
    "default": ("🗂️", "Nothing here yet", "Get started by adding your first entry."),
}

def get_empty_state(context, cta_url=None, cta_label="Get Started"):
    icon, title, desc = EMPTY_STATES.get(context, EMPTY_STATES["default"])
    cta = ""
    if cta_url:
        cta = f'<a href="{cta_url}" class="btn-empty">➕ {cta_label}</a>'
    return (
        f'<div class="empty-state">'
        f'<div class="empty-icon">{icon}</div>'
        f'<h3>{title}</h3>'
        f'<p>{desc}</p>'
        f'{cta}'
        f'</div>'
    )

# Patterns to replace in templates
REPLACEMENTS = [
    # "No products." / "No items." etc bare text
    (r'<p[^>]*>\s*No (products?|items?|orders?|users?|leads?|bids?|backups?|keys?|vendors?)[.\s]*</p>',
     lambda m: get_empty_state(m.group(1).rstrip('s').lower())),
    # {% if not items %}...No items...{% endif %} patterns - handled case by case
]

files_patched = 0
for fname in os.listdir(TEMPLATES_DIR):
    if not fname.endswith('.html'):
        continue
    path = os.path.join(TEMPLATES_DIR, fname)
    content = open(path).read()
    changed = False

    for pattern, replacement in REPLACEMENTS:
        if callable(replacement):
            new = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        else:
            new = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        if new != content:
            content = new
            changed = True

    if changed:
        # Add CSS if not present
        if 'empty-state' not in content and '</head>' in content:
            content = content.replace('</head>', EMPTY_STATE_CSS + '</head>', 1)
        open(path, 'w').write(content)
        print(f"  ✅ {fname}")
        files_patched += 1

print(f"\n✅ Patched {files_patched} templates")
