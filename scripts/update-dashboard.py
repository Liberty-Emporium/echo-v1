#!/usr/bin/env python3
"""
update-dashboard.py — EcDash updater tool
==========================================
Updates jay-portfolio/templates/dashboard.html with new daily summary cards,
stat corrections, and other content patches.

Usage:
  python3 update-dashboard.py --add-daily-card
  python3 update-dashboard.py --fix-stats
  python3 update-dashboard.py --status
  python3 update-dashboard.py --all
"""

import sys
import os
import re
import argparse
import subprocess
from datetime import datetime

# ── Config ──
DASHBOARD = os.path.expanduser(
    "/root/.openclaw/workspace/jay-portfolio/templates/dashboard.html"
)
REPO = os.path.expanduser("/root/.openclaw/workspace/jay-portfolio")


def read_dashboard():
    with open(DASHBOARD, "r") as f:
        return f.read()


def write_dashboard(html):
    with open(DASHBOARD, "w") as f:
        f.write(html)
    print("✅ Dashboard written.")


def git_push(message="EcDash: dashboard update via update-dashboard.py"):
    try:
        subprocess.run(["git", "-C", REPO, "add", "templates/dashboard.html"], check=True)
        result = subprocess.run(
            ["git", "-C", REPO, "diff", "--cached", "--stat"],
            capture_output=True, text=True
        )
        if not result.stdout.strip():
            print("ℹ️  No changes to commit.")
            return
        subprocess.run(["git", "-C", REPO, "commit", "-m", message], check=True)
        subprocess.run(["git", "-C", REPO, "push", "origin", "master"], check=True)
        print("🚀 Pushed to GitHub.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git error: {e}")


def status():
    """Print a summary of what's in the dashboard."""
    html = read_dashboard()

    # Count daily summary cards
    daily_cards = re.findall(r'📆\s*(.*?)—', html)
    print(f"\n📊 Dashboard Status")
    print(f"{'─'*50}")
    print(f"  File: {DASHBOARD}")
    print(f"  Size: {len(html):,} bytes")

    # Stat tiles
    stat_nums = re.findall(r'<div class="stat-num[^"]*">(\d+)</div>', html)
    stat_labels = re.findall(r'<div class="stat-label">([^<]+)</div>', html)
    print(f"\n📈 Stat Tiles:")
    for num, label in zip(stat_nums, stat_labels):
        print(f"    {num} — {label}")

    # Daily summary entries
    print(f"\n📅 Daily Summary Cards ({len(daily_cards)}):")
    for card in daily_cards:
        print(f"    • {card.strip()}")

    # Project cards
    proj_names = re.findall(r'<div class="proj-name">([^<]+)</div>', html)
    print(f"\n🚀 Projects Listed ({len(proj_names)}):")
    for p in proj_names:
        print(f"    • {p}")

    print()


def fix_stats(total=None, live=None, demos=None):
    """Update the 4 stat tiles in the Overview panel."""
    html = read_dashboard()

    replacements = []

    if total is not None:
        old = re.search(r'(<div class="stat-num">)\d+(</div>\s*<div class="stat-label">Total Projects)', html)
        if old:
            replacements.append((old.group(0), f'{old.group(1)}{total}{old.group(2)}'))

    if live is not None:
        old = re.search(r'(<div class="stat-num">)\d+(</div>\s*<div class="stat-label">Live Apps)', html)
        if old:
            replacements.append((old.group(0), f'{old.group(1)}{live}{old.group(2)}'))

    if demos is not None:
        old = re.search(r'(<div class="stat-num">)\d+(</div>\s*<div class="stat-label">Demos)', html)
        if old:
            replacements.append((old.group(0), f'{old.group(1)}{demos}{old.group(2)}'))

    for old_text, new_text in replacements:
        html = html.replace(old_text, new_text, 1)

    write_dashboard(html)
    print(f"✅ Stats updated: total={total}, live={live}, demos={demos}")
    return html


def add_daily_card(date_str, title, items, color="#6366f1", push=True):
    """
    Add a new daily summary card at the TOP of the daily panel list.

    Args:
        date_str: e.g. "Wed Apr 22, 2026"
        title: e.g. "Bootstrap + Dashboard Audit Session"
        items: list of (emoji, bold_label, description) tuples
        color: CSS border color hex
        push: whether to git push after writing
    """
    html = read_dashboard()

    # Build the card HTML
    items_html = "\n".join(
        f'            <li>{emoji} <strong>{label}</strong> — {desc}</li>'
        for emoji, label, desc in items
    )
    card_html = f"""
        <div class="card" style="border-left:3px solid {color}">
          <div class="card-header"><div class="card-title">📆 {date_str} — {title}</div></div>
          <ul style="font-size:.9rem;line-height:2;color:var(--muted);padding-left:1.25rem">
{items_html}
          </ul>
        </div>

        """

    # Insert at the top of the daily panel list
    insert_marker = '<div style="max-width:800px;display:flex;flex-direction:column;gap:1.25rem">'
    if insert_marker not in html:
        print("❌ Could not find daily panel insertion point.")
        return False

    html = html.replace(insert_marker, insert_marker + "\n" + card_html, 1)
    write_dashboard(html)
    print(f"✅ Daily card added: {date_str} — {title}")

    if push:
        git_push(f"EcDash: add daily summary card for {date_str}")

    return True


def update_ai_panel(last_session=None, skills_count=None, push=True):
    """Update the My AI panel with current session info."""
    html = read_dashboard()

    if last_session:
        # Update "Last Session" row
        old = re.search(
            r'(<span style="color:var\(--muted\)">Last Session</span><span>)([^<]+)(</span>)',
            html
        )
        if old:
            html = html.replace(old.group(0), f'{old.group(1)}{last_session}{old.group(3)}')
            print(f"✅ Last Session updated to: {last_session}")

    if skills_count:
        old = re.search(
            r'(<span style="color:var\(--muted\)">Custom Skills</span><span>)([^<]+)(</span>)',
            html
        )
        if old:
            html = html.replace(old.group(0), f'{old.group(1)}{skills_count}{old.group(3)}')
            print(f"✅ Skills count updated to: {skills_count}")

    write_dashboard(html)
    if push:
        git_push("EcDash: update AI panel metadata")


def add_project_card(
    name, desc, icon, category, tags, links,
    status="green", section="tools",
    push=True
):
    """
    Add a project card to the Projects panel.

    Args:
        name: project name
        desc: short description
        icon: emoji
        category: e.g. "SaaS · Bakery"
        tags: list of tag strings
        links: list of (label, url) tuples
        status: "green" | "yellow" | "red"
        section: "live" | "demos" | "tools"
        push: whether to push after
    """
    html = read_dashboard()

    tags_html = "".join(f'<span class="tag">{t}</span>' for t in tags)
    links_html = "".join(
        f'<a href="{url}" target="_blank">{label} ↗</a>'
        for label, url in links
    )

    card_html = f"""
        <div class="proj-card">
          <div class="proj-status"><span class="dot dot-{status}" title="Live"></span></div>
          <div class="proj-icon">{icon}</div>
          <div class="proj-category">{category}</div>
          <div class="proj-name">{name}</div>
          <div class="proj-desc">{desc}</div>
          <div class="proj-tags">{tags_html}</div>
          <div class="proj-links">{links_html}</div>
        </div>

        """

    # Section markers
    section_map = {
        "live": 'Live Apps</div>\n      <div class="grid-auto" style="margin-bottom:32px">',
        "demos": 'Demos</div>\n      <div class="grid-auto" style="margin-bottom:32px">',
        "tools": 'Tools &amp; Infrastructure</div>\n      <div class="grid-auto">',
    }

    marker = section_map.get(section)
    if not marker or marker not in html:
        # Try alternate encoding
        marker = section_map.get(section, "").replace("&amp;", "&#38;")
        if not marker or marker not in html:
            print(f"❌ Could not find section '{section}' insertion point.")
            return False

    html = html.replace(marker, marker + "\n" + card_html, 1)
    write_dashboard(html)
    print(f"✅ Project card added: {name} (section: {section})")

    if push:
        git_push(f"EcDash: add project card '{name}'")

    return True


def run_all():
    """Apply all known missing updates in one shot."""
    print("\n🔧 Running full dashboard update...\n")

    # 1. Fix stats — current count: 15+ live apps now
    # Live apps: Inventory, KYS, Pet Vet, GymForge, Contractor Pro, Dropship,
    #            Court/Portfolio, AI Widget, FloodClaim, Sweet Spot, Grace,
    #            Liberty Oil = 12 live apps + EcDash itself = 13
    # Demos: Inventory Demo, Luxury Rentals, Consignment = 3
    # Total projects in GitHub org = at least 19 repos
    print("📈 Fixing stat tiles...")
    fix_stats(total=19, live=13, demos=3)

    # 2. Update My AI panel
    print("\n🤖 Updating AI panel...")
    today = datetime.now().strftime("%B %d, %Y")
    update_ai_panel(last_session=today, skills_count="32+ built for your projects", push=False)

    # 3. Add today's daily card
    print("\n📅 Adding today's daily card...")
    add_daily_card(
        date_str="Wed Apr 22, 2026",
        title="Bootstrap + Dashboard Audit Session",
        items=[
            ("🚀", "New KiloClaw Instance", "Bootstrapped clean — all repos cloned, secrets saved, GitLab remotes configured"),
            ("✅", "All Services Healthy", "FloodClaim Pro ✅, EcDash ✅, AI Agent Widget ✅ — verified on boot"),
            ("🔒", "GitHub & GitLab Secrets", "Tokens stored in /root/.secrets/ — GitHub (primary) and GitLab (backup) both active"),
            ("🔄", "GitLab Backup Remotes", "Set for echo-v1, floodclaim-pro, AI-Agent-Widget, jay-portfolio"),
            ("🛠️", "Dashboard Audit", "Full audit of EcDash — added missing sessions (Apr 13-16), fixed stats (19 projects, 13 live), added Vendor Vault & List It Everywhere to links"),
            ("📊", "Dashboard Update Tool", "Built update-dashboard.py — add daily cards, fix stats, update AI panel, add project cards from CLI"),
        ],
        color="#22d3ee",
        push=False,
    )

    # 4. Add missing Apr 16 session card (was not in dashboard at all)
    print("\n📅 Adding missing Apr 16 session...")
    add_missing_apr16_session()

    # 5. Push everything at once
    print("\n🚀 Pushing to GitHub...")
    git_push("EcDash: full dashboard audit — stats fixed, Apr 16 session added, Apr 22 boot session added, update tool added")

    print("\n✅ All updates complete!")


def add_missing_apr16_session():
    """Add the Apr 16 session that was in SHORT_TERM_MEMORY but not in Daily Summary."""
    html = read_dashboard()

    # Check if Apr 16 already exists
    if "Apr 16" in html or "April 16" in html:
        print("ℹ️  Apr 16 card already exists, skipping.")
        return

    # Find the last existing card in the daily panel and insert after it
    # We want this at the BOTTOM (it's the oldest session we're adding)
    # Find the Foundation Week card and insert before it

    foundation_marker = '<div class="card" style="border-left:3px solid #10b981">'
    if foundation_marker not in html:
        print("❌ Could not find Foundation Week card to insert after.")
        return

    apr16_card = """
        <div class="card" style="border-left:3px solid #8b5cf6">
          <div class="card-header"><div class="card-title">📆 Wed Apr 16, 2026 — International Expansion + CI/CD Session</div></div>
          <ul style="font-size:.9rem;line-height:2;color:var(--muted);padding-left:1.25rem">
            <li>🌍 <strong>i18n (8 Languages)</strong> — EN/ES/FR/PT/DE/ZH/JA/AR across ALL 7 apps, auto browser-detect, RTL for Arabic</li>
            <li>📍 <strong>Pet Vet AI — Vet Finder</strong> — IP geolocation + GPS + OpenStreetMap, 50-100km radius, 3-mirror fallback</li>
            <li>🔁 <strong>CI/CD Pipelines</strong> — GitHub Actions on all 7 repos: syntax → flake8 → Railway deploy → health check</li>
            <li>🖼️ <strong>og:image</strong> — 1200×630 preview.png added to all 7 apps (social sharing)</li>
            <li>💰 <strong>Investor Page</strong> — /investors live on EcDash: $150K seed, 10% equity, $1.5M valuation pitch</li>
            <li>🏢 <strong>Rebrand</strong> — Alexander AI Digital → <strong>Alexander AI Integrated Solutions</strong></li>
            <li>🔒 <strong>KYS /health endpoint</strong> — now returns <code>{status, db}</code> JSON for monitoring</li>
            <li>🛡️ <strong>Security headers</strong> — Consignment Solutions (all 6 headers)</li>
            <li>📝 <strong>Trademark research</strong> — USPTO clear, domains appear available</li>
          </ul>
        </div>

        """

    html = html.replace(foundation_marker, apr16_card + "\n        " + foundation_marker, 1)
    write_dashboard(html)
    print("✅ Apr 16 session card added.")


def main():
    parser = argparse.ArgumentParser(description="EcDash Update Tool")
    parser.add_argument("--status", action="store_true", help="Show dashboard status")
    parser.add_argument("--fix-stats", action="store_true", help="Fix stat tile numbers")
    parser.add_argument("--total", type=int, help="Total projects count")
    parser.add_argument("--live", type=int, help="Live apps count")
    parser.add_argument("--demos", type=int, help="Demos count")
    parser.add_argument("--update-ai", action="store_true", help="Update AI panel metadata")
    parser.add_argument("--last-session", type=str, help="Last session date string")
    parser.add_argument("--skills", type=str, help="Custom skills label")
    parser.add_argument("--add-apr16", action="store_true", help="Add missing Apr 16 session")
    parser.add_argument("--all", action="store_true", help="Run all updates")
    parser.add_argument("--no-push", action="store_true", help="Don't push to GitHub")

    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
        return

    if args.status:
        status()
        return

    if args.all:
        run_all()
        return

    push = not args.no_push

    if args.fix_stats:
        fix_stats(total=args.total, live=args.live, demos=args.demos)
        if push:
            git_push("EcDash: fix stat tile numbers")

    if args.update_ai:
        update_ai_panel(
            last_session=args.last_session,
            skills_count=args.skills,
            push=push
        )

    if args.add_apr16:
        add_missing_apr16_session()
        if push:
            git_push("EcDash: add missing Apr 16 session card")


if __name__ == "__main__":
    main()
