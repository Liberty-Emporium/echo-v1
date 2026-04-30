#!/usr/bin/env python3
"""
remove_app.py — Remove a decommissioned app from EcDash
========================================================
Purges all references to an app (by name and URL) from every EcDash template
and app.py — exactly like KYS and Dropship Shipping were removed.

Usage:
  python3 remove_app.py --name "My App Name" --url "myapp.up.railway.app" [--url2 "alias.domain.com"] [--dry-run] [--no-push]

Examples:
  python3 remove_app.py --name "Pet Vet AI" --url "pet-vet-ai-production.up.railway.app"
  python3 remove_app.py --name "GymForge" --url "web-production-1c23.up.railway.app" --dry-run
"""

import re
import sys
import argparse
import subprocess
from html.parser import HTMLParser
from pathlib import Path

DASHBOARD_REPO = Path("/root/.openclaw/workspace/alexander-ai-dashboard")
TEMPLATES      = DASHBOARD_REPO / "templates"
APP_PY         = DASHBOARD_REPO / "app.py"

TARGET_FILES = [
    "dashboard.html", "apps.html", "settings.html", "investors.html",
    "index.html", "court.html", "flyer.html", "tickets.html", "tools.html",
    "testing.html", "monitoring.html",
]


# ── HTML validator ─────────────────────────────────────────────────────────────
def validate_html(html: str, label: str) -> bool:
    class Check(HTMLParser):
        def __init__(self):
            super().__init__()
            self.stack = []
            self.errors = []
        def handle_starttag(self, tag, attrs):
            void = {'area','base','br','col','embed','hr','img','input',
                    'link','meta','param','source','track','wbr'}
            if tag not in void:
                self.stack.append((tag, self.getpos()))
        def handle_endtag(self, tag):
            if self.stack and self.stack[-1][0] == tag:
                self.stack.pop()
            else:
                self.errors.append(f"Bad </{tag}> at line {self.getpos()[0]}")
    c = Check()
    c.feed(html)
    ok = not c.stack and not c.errors
    icon = "✅" if ok else "❌"
    print(f"  {icon} {label}: unclosed={len(c.stack)} errors={len(c.errors)}")
    if not ok:
        for e in c.errors[:3]:
            print(f"     {e}")
    return ok


# ── Exact-string removals (safe — no structural regex) ────────────────────────
def remove_exact(html: str, snippets: list[str]) -> str:
    for s in snippets:
        html = html.replace(s, "")
    return html


# ── Pattern-based removals for known block types ──────────────────────────────
def remove_by_patterns(html: str, name: str, urls: list[str]) -> str:
    url_pattern = "|".join(re.escape(u) for u in urls)

    # link-chip anchors (single or with sub-url div)
    html = re.sub(
        rf'\s*<a href="https?://(?:{url_pattern})[^"]*"[^>]*class="link-chip"[^>]*>.*?</a>',
        "", html, flags=re.DOTALL)

    # GitHub link-chip anchors
    html = re.sub(
        rf'\s*<a href="https://github\.com/Liberty-Emporium/[^"]*(?:{re.escape(name.replace(" ", "-"))})[^"]*"[^>]*class="link-chip"[^>]*>.*?</a>',
        "", html, flags=re.DOTALL)

    # Quick-launch tile (text-decoration:none wrapper)
    html = re.sub(
        rf'\s*<a href="https?://(?:{url_pattern})[^"]*" target="_blank" style="text-decoration:none">.*?</a>',
        "", html, flags=re.DOTALL)

    # proj-card containing the app name
    html = re.sub(
        rf'\s*<div class="proj-card">(?:(?!proj-card).)*?{re.escape(name)}.*?</div>\s*</div>',
        "", html, flags=re.DOTALL)

    # credentials card
    html = re.sub(
        rf'\s*<div class="card">\s*<div class="card-header"><div class="card-title">[^<]*{re.escape(name)}[^<]*</div></div>.*?</div>\s*</div>',
        "", html, flags=re.DOTALL)

    # support panel row
    html = re.sub(
        rf'\s*<div[^>]*>\s*<div[^>]*>(?:<span>[^<]*</span>)*\s*<span[^>]*>{re.escape(name)}</span></div>\s*<a href="mailto:[^"]*"[^>]*>Get Help ↗</a>\s*</div>',
        "", html, flags=re.DOTALL)

    # app-tile anchor
    html = re.sub(
        rf'\s*<a href="https?://(?:{url_pattern})[^"]*"[^>]*class="app-tile"[^>]*>.*?</a>',
        "", html, flags=re.DOTALL)

    # project-link anchor
    html = re.sub(
        rf'\s*<a class="project-link" href="https?://(?:{url_pattern})[^"]*"[^>]*>.*?</a>',
        "", html, flags=re.DOTALL)

    # apps.html card block (comment + div)
    html = re.sub(
        rf'\s*<!-- [0-9]+\. {re.escape(name)} -->\s*<div class="app-card"[^>]*>.*?</div>\s*</div>\s*\n',
        "\n", html, flags=re.DOTALL)

    # tickets.html option
    html = re.sub(rf'\s*<option value="{re.escape(name)}">{re.escape(name)}</option>', "", html)

    # settings.html health tuple
    html = re.sub(rf"\('[^']*','{re.escape(name)}','(?:{url_pattern})'[^)]*\),?\n?", "", html)

    # investors product card
    html = re.sub(
        rf'<div class="product-card">(?:(?!</div>\s*</div>).)*?<h3>[^<]*{re.escape(name)}[^<]*</h3>.*?</div>\s*</div>',
        "", html, flags=re.DOTALL)

    # index.html project block
    html = re.sub(
        rf'\s*<!-- [^>]*{re.escape(name)}[^>]* -->\s*<div[^>]*>.*?</div>\s*</div>',
        "", html, flags=re.DOTALL)

    # tools.html — remove from "apps:" lists
    for u in [name] + [f" · {name}", f"{name} · "]:
        html = html.replace(u, "")

    # flyer p-card
    html = re.sub(
        rf'\s*<div class="p-card">(?:(?!</div>).)*?{re.escape(name)}.*?</div>\s*</div>',
        "", html, flags=re.DOTALL)

    # court project-card
    html = re.sub(
        rf'\s*<div class="project-card">(?:(?!</div>).)*?{re.escape(name)}.*?</div>\s*</div>',
        "", html, flags=re.DOTALL)

    return html


def clean_orphan_divs(html: str) -> str:
    """Remove simple orphan closing div patterns left by block removals."""
    # Repeated pass to catch cascading orphans
    for _ in range(3):
        html = re.sub(r'\n\s*</div>\n(\s*</div>\n\s*\n\s*</div><!-- /)', r'\n\1', html)
        html = re.sub(r'\n\s+</div>\n(\s*</div><!-- /)', r'\n\1', html)
    return html


# ── app.py ─────────────────────────────────────────────────────────────────────
def remove_from_app_py(name: str, urls: list[str]) -> bool:
    with open(APP_PY) as f:
        content = f.read()

    original = content
    url_pattern = "|".join(re.escape(u) for u in urls)

    # APPS_REGISTRY line
    content = re.sub(
        rf"\s*\{{'name': '{re.escape(name)}'[^}}]*\}},\n",
        "", content)

    # APP_TEST_SUITES block
    content = re.sub(
        rf"\s*\{{\s*\n\s*'name': '{re.escape(name)}',\s*'url': 'https?://(?:{url_pattern})[^']*',.*?\]\s*\}},",
        "", content, flags=re.DOTALL)

    changed = content != original
    with open(APP_PY, "w") as f:
        f.write(content)
    return changed


# ── git commit & push ──────────────────────────────────────────────────────────
def git_push(name: str):
    try:
        subprocess.run(["git", "-C", str(DASHBOARD_REPO), "add", "-A"], check=True)
        result = subprocess.run(
            ["git", "-C", str(DASHBOARD_REPO), "diff", "--cached", "--stat"],
            capture_output=True, text=True)
        if not result.stdout.strip():
            print("ℹ️  No changes to commit.")
            return
        subprocess.run([
            "git", "-C", str(DASHBOARD_REPO), "commit", "-m",
            f"Remove {name} from EcDash — app decommissioned"
        ], check=True)
        subprocess.run(["git", "-C", str(DASHBOARD_REPO), "push", "origin", "master"], check=True)
        print("🚀 Pushed to GitHub.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git error: {e}")


# ── main ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Remove a decommissioned app from EcDash")
    parser.add_argument("--name",    required=True, help="App display name (e.g. 'Pet Vet AI')")
    parser.add_argument("--url",     required=True, help="Primary app URL (without https://)")
    parser.add_argument("--url2",    default=None,  help="Alternate URL / domain alias")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change, don't write")
    parser.add_argument("--no-push", action="store_true", help="Skip git commit/push")
    args = parser.parse_args()

    urls = [args.url]
    if args.url2:
        urls.append(args.url2)

    print(f"\n🗑️  Removing '{args.name}' (URLs: {', '.join(urls)}) from EcDash")
    print(f"   Dry run: {args.dry_run}\n")

    all_valid = True

    # Templates
    for fname in TARGET_FILES:
        fpath = TEMPLATES / fname
        if not fpath.exists():
            continue

        with open(fpath) as f:
            original = f.read()

        updated = remove_by_patterns(original, args.name, urls)
        updated = clean_orphan_divs(updated)

        if updated == original:
            print(f"  ⏩ {fname} — no changes")
            continue

        if fname.endswith(".html"):
            valid = validate_html(updated, fname)
            all_valid = all_valid and valid
        else:
            print(f"  ✅ {fname}")

        if not args.dry_run:
            with open(fpath, "w") as f:
                f.write(updated)

    # app.py
    if not args.dry_run:
        changed = remove_from_app_py(args.name, urls)
        print(f"  {'✅' if changed else '⏩'} app.py — {'updated' if changed else 'no changes'}")
    else:
        print(f"  🔍 app.py — (dry run, skipped)")

    if not all_valid:
        print("\n⚠️  HTML validation errors detected. Review before pushing.")
        if not args.dry_run and not args.no_push:
            print("   Skipping push due to validation errors.")
            return

    if not args.dry_run and not args.no_push:
        git_push(args.name)

    print(f"\n✅ Done — '{args.name}' removed from EcDash.")


if __name__ == "__main__":
    main()
