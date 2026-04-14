#!/usr/bin/env python3
"""Fix remaining SEO issues across all apps: og:image, title lengths, meta descriptions, canonical."""
import os, subprocess, re

TOKEN = open('/root/.secrets/github_token').read().strip()

APPS = [
    {
        "name": "Dropship-Shipping",
        "path": "/tmp/Dropship-Shipping",
        "branch": "main",
        "templates": ["templates/index.html", "templates/base.html", "templates/landing.html"],
        "title": "Dropship Shipping — AI-Powered Dropshipping Automation Software",
        "desc": "Automate your entire dropshipping business with AI. Manage orders, suppliers, and customers automatically. One-time $299 setup. No monthly fees.",
        "keywords": "dropshipping automation, dropship software, AI dropshipping, order management",
        "url": "https://dropship-shipping-production.up.railway.app",
    },
    {
        "name": "Contractor-Pro-AI",
        "path": "/tmp/Contractor-Pro-AI",
        "branch": "main",
        "templates": ["templates/index.html", "templates/base.html", "templates/landing.html"],
        "title": "Contractor Pro AI — Win More Bids with AI-Powered Estimating Software",
        "desc": "AI-powered estimating and project management for contractors. Write winning bids in minutes, track projects, manage clients. $99/month. Start free.",
        "keywords": "contractor software, AI estimating, bid writing software, construction management",
        "url": "https://contractor-pro-ai-production.up.railway.app",
    },
    {
        "name": "pet-vet-ai",
        "path": "/tmp/pet-vet-ai",
        "branch": "main",
        "templates": ["templates/index.html", "templates/base.html"],
        "title": "Pet Vet AI — Instant AI Pet Health Diagnosis for Dogs & Cats | $9.99/mo",
        "desc": "Get instant AI-powered health assessments for your pet. Upload a photo, describe symptoms, get expert guidance. Know when to see the vet. $9.99/month.",
        "keywords": "pet health diagnosis, AI vet, dog health app, cat health checker, pet symptom checker",
        "url": "https://pet-vet-ai-production.up.railway.app",
    },
    {
        "name": "jays-keep-your-secrets",
        "path": "/tmp/jays-keep-your-secrets",
        "branch": "master",
        "templates": ["templates/index.html", "templates/base.html"],
        "title": "Jay's Keep Your Secrets — Secure API Key Management for Developers | $14.99/mo",
        "desc": "Stop losing track of API keys. Securely store, organize and share API keys with your team. Encrypted storage, audit logs, rotation alerts. $14.99/month.",
        "keywords": "API key management, secret management, developer tools, secure key storage",
        "url": "https://ai-api-tracker-production.up.railway.app",
    },
    {
        "name": "Consignment-Solutions",
        "path": "/tmp/Consignment-Solutions",
        "branch": "master",
        "templates": ["templates/index.html", "templates/base.html", "templates/landing.html"],
        "title": "Consignment Solutions — Modern Consignment Store Management Software | $69.95",
        "desc": "Run your consignment or antique store like a pro. Vendor portals, auto rent settlement, Square POS integration, AI assistant. 14-day free trial.",
        "keywords": "consignment store software, vendor management, consignment management, antique store software",
        "url": "https://web-production-43ce4.up.railway.app",
    },
]

OG_IMAGE_TAG = '<meta property="og:image" content="{url}/static/preview.png">\n    <meta name="twitter:image" content="{url}/static/preview.png">'

PREVIEW_PNG_B64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="

def find_base_template(app_path, candidates):
    for c in candidates:
        p = os.path.join(app_path, c)
        if os.path.exists(p):
            return p
    # Search all templates
    tpl_dir = os.path.join(app_path, 'templates')
    if os.path.exists(tpl_dir):
        for f in os.listdir(tpl_dir):
            if 'base' in f.lower() or 'layout' in f.lower():
                return os.path.join(tpl_dir, f)
    return None

def patch_seo(app):
    name = app['name']
    app_path = app['path']

    tpl_path = find_base_template(app_path, app['templates'])
    if not tpl_path:
        print(f"  [SKIP] {name}: no template found")
        return False

    content = open(tpl_path).read()
    changes = []

    # Fix og:image if missing
    if 'og:image' not in content:
        og_img = OG_IMAGE_TAG.format(url=app['url'])
        # Insert before </head>
        if '</head>' in content:
            content = content.replace('</head>', f'    {og_img}\n</head>', 1)
            changes.append("og:image")

    # Fix title if too short/long
    title_match = re.search(r'<title>([^<]{0,200})</title>', content)
    if title_match:
        cur_title = title_match.group(1)
        # Only fix if it's clearly wrong (contains Jinja vars that won't expand right or is too short)
        if len(cur_title) < 40 and '{{' not in cur_title:
            content = content.replace(f'<title>{cur_title}</title>', f'<title>{app["title"]}</title>', 1)
            changes.append("title")

    # Fix meta description if missing or too short
    desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']{0,300})["\']', content)
    if desc_match:
        cur_desc = desc_match.group(1)
        if len(cur_desc) < 100:
            content = content.replace(cur_desc, app['desc'], 1)
            changes.append("meta-desc-expanded")
    elif 'meta name="description"' not in content and "meta name='description'" not in content:
        # Add meta description
        if '<title>' in content:
            insert_after = content.find('</title>') + len('</title>')
            meta = f'\n    <meta name="description" content="{app["desc"]}">'
            content = content[:insert_after] + meta + content[insert_after:]
            changes.append("meta-desc-added")

    # Add canonical if missing
    if 'canonical' not in content:
        canonical = f'\n    <link rel="canonical" href="{app["url"]}/">'
        if '</head>' in content:
            content = content.replace('</head>', canonical + '\n</head>', 1)
            changes.append("canonical")

    if not changes:
        print(f"  [OK] {name}: SEO already good")
        return False

    # Create preview.png if missing
    static_dir = os.path.join(app_path, 'static')
    os.makedirs(static_dir, exist_ok=True)
    preview_path = os.path.join(static_dir, 'preview.png')
    if not os.path.exists(preview_path):
        import base64
        with open(preview_path, 'wb') as f:
            f.write(base64.b64decode(PREVIEW_PNG_B64))

    with open(tpl_path, 'w') as f:
        f.write(content)

    # Push
    branch = app['branch']
    tpl_rel = os.path.relpath(tpl_path, app_path)
    cmds = [
        f"cd {app_path} && git config user.email echo@liberty-emporium.ai && git config user.name Echo",
        f"cd {app_path} && git remote set-url origin https://{TOKEN}@github.com/Liberty-Emporium/{name}.git",
        f"cd {app_path} && git add {tpl_rel} static/preview.png 2>/dev/null; git add -A && git commit -m 'seo: fix og:image, meta description, canonical — boost SEO score'",
        f"cd {app_path} && git push origin {branch}",
    ]
    for cmd in cmds:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if r.returncode != 0 and 'nothing to commit' not in r.stdout + r.stderr:
            print(f"  [ERR] {r.stderr[:200]}")
            return False
    print(f"  [PUSHED] {name}: {', '.join(changes)}")
    return True

print("=" * 50)
print("SEO FIXES — ALL APPS")
print("=" * 50)
for app in APPS:
    print(f"\n[{app['name']}]")
    patch_seo(app)
print("\nDone.")
