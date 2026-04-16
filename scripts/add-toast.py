#!/usr/bin/env python3
"""
add-toast.py — Replace static flash message banners with slide-in toast notifications.
Patches base.html in a given templates directory.
Usage: python3 add-toast.py <templates-dir>
"""
import os, re, sys

TEMPLATES_DIR = sys.argv[1] if len(sys.argv) > 1 else "templates"

TOAST_CSS = """
<style>
#toast-container { position:fixed; bottom:1.5rem; right:1.5rem; z-index:9999; display:flex; flex-direction:column; gap:0.5rem; pointer-events:none; }
.toast { pointer-events:all; display:flex; align-items:center; gap:0.75rem; padding:0.85rem 1.25rem; border-radius:12px; font-size:0.9rem; font-weight:600; box-shadow:0 8px 24px rgba(0,0,0,0.15); min-width:280px; max-width:400px; transform:translateX(120%); transition:transform 0.3s cubic-bezier(0.34,1.56,0.64,1); }
.toast.show { transform:translateX(0); }
.toast.success { background:#fff; border-left:4px solid #10b981; color:#065f46; }
.toast.error   { background:#fff; border-left:4px solid #ef4444; color:#b91c1c; }
.toast.warning { background:#fff; border-left:4px solid #f59e0b; color:#92400e; }
.toast.info    { background:#fff; border-left:4px solid #6366f1; color:#3730a3; }
.toast .toast-icon { font-size:1.1rem; flex-shrink:0; }
.toast .toast-close { margin-left:auto; background:none; border:none; cursor:pointer; color:inherit; opacity:0.6; font-size:1rem; padding:0; flex-shrink:0; }
.toast .toast-close:hover { opacity:1; }
</style>
"""

TOAST_JS = """
<div id="toast-container"></div>
<script>
function showToast(msg, type) {
  type = type || 'info';
  var icons = {success:'✅', error:'❌', warning:'⚠️', info:'ℹ️'};
  var c = document.getElementById('toast-container');
  var t = document.createElement('div');
  t.className = 'toast ' + type;
  t.innerHTML = '<span class="toast-icon">' + (icons[type]||'ℹ️') + '</span><span class="toast-msg">' + msg + '</span><button class="toast-close" onclick="this.parentElement.remove()">✕</button>';
  c.appendChild(t);
  requestAnimationFrame(function(){ requestAnimationFrame(function(){ t.classList.add('show'); }); });
  setTimeout(function(){ t.classList.remove('show'); setTimeout(function(){ if(t.parentElement) t.remove(); }, 350); }, 4500);
}
// Auto-show Flask flash messages as toasts
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('[data-flash-msg]').forEach(function(el) {
    showToast(el.dataset.flashMsg, el.dataset.flashCat || 'info');
    el.remove();
  });
});
</script>
"""

FLASH_DATA_ATTRS = """
{%% for cat, msg in get_flashed_messages(with_categories=true) %%}
<span data-flash-msg="{{ msg }}" data-flash-cat="{{ cat }}" style="display:none;"></span>
{%% endfor %%}
"""

def patch_base(path):
    content = open(path).read()
    changed = False

    # Add toast CSS before </head>
    if 'toast-container' not in content and '</head>' in content:
        content = content.replace('</head>', TOAST_CSS + '\n</head>', 1)
        changed = True

    # Add toast JS + container before </body>
    if 'showToast' not in content and '</body>' in content:
        content = content.replace('</body>', TOAST_JS + '\n</body>', 1)
        changed = True

    # Add invisible flash span tags right after <body> (if not already data-flash pattern)
    if 'data-flash-msg' not in content:
        # Find existing flash block and replace it, or add data attrs version
        old_flash = re.search(
            r'\{%-?\s*for\s+\w+\s*,\s*\w+\s+in\s+get_flashed_messages.*?endfor\s*-?%\}',
            content, re.DOTALL
        )
        if old_flash:
            cats = re.findall(r"'(\w+)'", old_flash.group(0)[:100])
            cat_var = cats[0] if cats else 'cat'
            content = content[:old_flash.start()] + \
                "{%% for cat, msg in get_flashed_messages(with_categories=true) %%}\n" \
                '<span data-flash-msg="{{ msg }}" data-flash-cat="{{ cat }}" style="display:none;"></span>\n' \
                "{%% endfor %%}" + \
                content[old_flash.end():]
            changed = True

    if changed:
        open(path, 'w').write(content)
        print(f"  ✅ Patched: {path}")
    else:
        print(f"  ⏭  No changes needed: {path}")

base = os.path.join(TEMPLATES_DIR, 'base.html')
if os.path.exists(base):
    patch_base(base)
else:
    print(f"❌ base.html not found in {TEMPLATES_DIR}")
