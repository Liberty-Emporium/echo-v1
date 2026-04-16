#!/usr/bin/env python3
"""
add-aos.py — Inject AOS (Animate On Scroll) into any app's landing/base template.
Adds CDN links to <head> and data-aos attributes to feature cards, stats, testimonials.
Usage: python3 add-aos.py <path-to-templates-dir>
"""
import os, re, sys

TEMPLATES_DIR = sys.argv[1] if len(sys.argv) > 1 else "templates"

AOS_CSS = '<link rel="stylesheet" href="https://unpkg.com/aos@2.3.1/dist/aos.css">'
AOS_JS  = '''<script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
<script>document.addEventListener('DOMContentLoaded',function(){AOS.init({duration:600,once:true,offset:80});});</script>'''

SWAL_JS = '<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>'

def patch_template(path):
    content = open(path).read()
    changed = False

    # Add AOS CSS before </head>
    if 'aos@2.3.1' not in content and '</head>' in content:
        content = content.replace('</head>', f'  {AOS_CSS}\n</head>', 1)
        changed = True

    # Add SweetAlert2 + AOS JS before </body>
    if 'sweetalert2' not in content and '</body>' in content:
        content = content.replace('</body>', f'{SWAL_JS}\n{AOS_JS}\n</body>', 1)
        changed = True

    # Add data-aos to feature cards (common class patterns)
    patterns = [
        (r'(<div class="[^"]*feature[^"]*")', r'\1 data-aos="fade-up"'),
        (r'(<div class="[^"]*testimonial[^"]*")', r'\1 data-aos="fade-up"'),
        (r'(<div class="[^"]*stat-card[^"]*")', r'\1 data-aos="zoom-in"'),
        (r'(<div class="[^"]*pricing-card[^"]*")', r'\1 data-aos="fade-up"'),
        (r'(<div class="[^"]*how-step[^"]*")', r'\1 data-aos="fade-up"'),
        (r'(<div class="[^"]*faq-item[^"]*")', r'\1 data-aos="fade-up"'),
    ]
    for pattern, replacement in patterns:
        new = re.sub(pattern, replacement, content)
        if new != content:
            content = new
            changed = True

    # Replace confirm() with SweetAlert2
    if 'onsubmit="return confirm(' in content:
        def replace_confirm(m):
            msg = re.search(r"confirm\('([^']+)'\)", m.group(0))
            if not msg:
                return m.group(0)
            txt = msg.group(1)
            return (
                f'onsubmit="event.preventDefault();'
                f'Swal.fire({{title:\'{txt}\',icon:\'warning\','
                f'showCancelButton:true,confirmButtonColor:\'#e74c3c\','
                f'confirmButtonText:\'Yes, do it!\'}}).then(r=>{{if(r.isConfirmed)this.submit()}});return false;"'
            )
        new = re.sub(r'onsubmit="return confirm\([^)]+\)"', replace_confirm, content)
        if new != content:
            content = new
            changed = True

    if changed:
        open(path, 'w').write(content)
        print(f"  ✅ Patched: {path}")
    else:
        print(f"  ⏭  Skipped (already patched or no matches): {path}")

targets = ['landing.html', 'base.html', 'index.html']
patched = 0
for tmpl in targets:
    path = os.path.join(TEMPLATES_DIR, tmpl)
    if os.path.exists(path):
        patch_template(path)
        patched += 1

print(f"\n✅ Done — patched {patched} templates in {TEMPLATES_DIR}")
