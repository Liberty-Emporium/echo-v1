#!/usr/bin/env python3
"""
seo-analyzer — SEO audit for Jay's app landing pages
Usage: python3 seo_check.py --url <URL> [--keywords "thrift store inventory"]
"""
import sys
import argparse
import urllib.request
import urllib.error
import re
import json

GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BLUE   = "\033[94m"
RESET  = "\033[0m"

score_total = 0
score_max = 0
fixes = []

def check(label, passed, points, detail="", fix=""):
    global score_total, score_max
    score_max += points
    if passed:
        score_total += points
        print(f"{GREEN}[✓]{RESET} {label}" + (f" — {detail}" if detail else ""))
    else:
        print(f"{RED}[✗]{RESET} {label}" + (f" — {detail}" if detail else ""))
        if fix:
            fixes.append((points, label, fix))

def warn(label, detail="", fix="", points=0):
    global score_total, score_max
    score_max += points
    score_total += points // 2
    print(f"{YELLOW}[~]{RESET} {label}" + (f" — {detail}" if detail else ""))
    if fix:
        fixes.append((points // 2, label, fix))

def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (SEOBot/1.0)"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, r.read().decode("utf-8", errors="ignore"), dict(r.headers), len(r.read() if False else b'')
    except urllib.error.HTTPError as e:
        return e.code, "", {}, 0
    except Exception as e:
        print(f"{RED}Error fetching {url}: {e}{RESET}")
        sys.exit(1)

def extract_tag(html, tag, attr=None, attr_val=None):
    """Extract content from HTML tags."""
    if attr and attr_val:
        pattern = rf'<{tag}[^>]*{attr}=["\']?{re.escape(attr_val)}["\']?[^>]*content=["\']([^"\']*)["\']'
        m = re.search(pattern, html, re.IGNORECASE)
        if not m:
            pattern = rf'<{tag}[^>]*content=["\']([^"\']*)["\'][^>]*{attr}=["\']?{re.escape(attr_val)}["\']?'
            m = re.search(pattern, html, re.IGNORECASE)
    else:
        pattern = rf'<{tag}[^>]*>([^<]*)</{tag}>'
        m = re.search(pattern, html, re.IGNORECASE)
    return m.group(1).strip() if m else ""

def run_seo(base_url, keywords=None):
    base_url = base_url.rstrip("/")
    keywords = [k.lower() for k in (keywords or [])]

    print(f"\n{BLUE}{'='*55}")
    print(f"  SEO AUDIT: {base_url}")
    print(f"{'='*55}{RESET}\n")

    code, html, headers, _ = fetch(base_url)
    html_lower = html.lower()
    page_size = len(html.encode("utf-8"))

    # ── Title Tag ────────────────────────────────────────────────
    print(f"\n[Title & Meta]")
    title = extract_tag(html, "title")
    if title:
        t_len = len(title)
        if 50 <= t_len <= 60:
            check("Title tag length (50-60 chars)", True, 10, f'"{title}" ({t_len} chars)')
        elif t_len < 50:
            warn("Title tag too short", f'"{title}" ({t_len} chars) — aim for 50-60', "Expand title with primary keyword", 10)
        else:
            warn("Title tag too long", f'"{title}" ({t_len} chars) — keep under 60', "Shorten title", 10)
        if keywords:
            kw_in_title = any(k in title.lower() for k in keywords)
            check("Primary keyword in title", kw_in_title, 15, f"Keywords: {keywords}", "Add primary keyword to title tag")
    else:
        check("Title tag present", False, 10, "No <title> tag found", "Add <title>Your App Name | Tagline</title>")

    # ── Meta Description ─────────────────────────────────────────
    desc = extract_tag(html, "meta", "name", "description")
    if desc:
        d_len = len(desc)
        if 150 <= d_len <= 160:
            check("Meta description length (150-160 chars)", True, 10, f"({d_len} chars)")
        else:
            warn("Meta description length", f"({d_len} chars) — aim for 150-160", "Adjust meta description length", 10)
        if keywords:
            kw_in_desc = any(k in desc.lower() for k in keywords)
            check("Keyword in meta description", kw_in_desc, 5, "", "Add primary keyword to meta description")
    else:
        check("Meta description present", False, 10, "Missing", 'Add <meta name="description" content="150-160 char description">')

    # ── Open Graph ───────────────────────────────────────────────
    print(f"\n[Open Graph / Social]")
    og_title = extract_tag(html, "meta", "property", "og:title")
    check("og:title", bool(og_title), 5, og_title[:60] if og_title else "MISSING", 'Add <meta property="og:title" content="...">')
    og_desc = extract_tag(html, "meta", "property", "og:description")
    check("og:description", bool(og_desc), 5, og_desc[:60] if og_desc else "MISSING", 'Add <meta property="og:description" content="...">')
    og_image = extract_tag(html, "meta", "property", "og:image")
    check("og:image", bool(og_image), 5, og_image[:60] if og_image else "MISSING — social shares will look bad", 'Add <meta property="og:image" content="https://yourapp.com/preview.png">')

    # ── Twitter Card ─────────────────────────────────────────────
    tw_card = extract_tag(html, "meta", "name", "twitter:card")
    check("Twitter Card", bool(tw_card), 3, tw_card if tw_card else "MISSING", 'Add <meta name="twitter:card" content="summary_large_image">')

    # ── Headings ─────────────────────────────────────────────────
    print(f"\n[Content Structure]")
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.IGNORECASE | re.DOTALL)
    h1_text = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip() if h1_match else ""
    check("H1 tag present", bool(h1_text), 10, h1_text[:60] if h1_text else "MISSING", "Add one H1 tag with primary keyword")
    if h1_text and keywords:
        check("Keyword in H1", any(k in h1_text.lower() for k in keywords), 10, "", "Include primary keyword in H1")

    # ── Word count ───────────────────────────────────────────────
    text_only = re.sub(r'<[^>]+>', ' ', html)
    word_count = len(text_only.split())
    check("Word count (300+ words)", word_count >= 300, 10, f"{word_count} words", "Add more content — aim for 500+ words on landing page")

    # ── Viewport / Mobile ────────────────────────────────────────
    print(f"\n[Technical]")
    viewport = 'viewport' in html_lower
    check("Viewport meta tag (mobile-friendly)", viewport, 10, "", 'Add <meta name="viewport" content="width=device-width, initial-scale=1.0">')

    # ── Canonical ────────────────────────────────────────────────
    canonical = 'rel="canonical"' in html_lower or "rel='canonical'" in html_lower
    check("Canonical URL tag", canonical, 5, "", f'Add <link rel="canonical" href="{base_url}/">')

    # ── robots.txt ───────────────────────────────────────────────
    r_code, _, _, _ = fetch(f"{base_url}/robots.txt")
    check("robots.txt", r_code == 200, 5, f"HTTP {r_code}", "Add /robots.txt route to Flask app")

    # ── sitemap.xml ──────────────────────────────────────────────
    s_code, _, _, _ = fetch(f"{base_url}/sitemap.xml")
    check("sitemap.xml", s_code == 200, 5, f"HTTP {s_code}", "Add /sitemap.xml route to Flask app")

    # ── Page size ────────────────────────────────────────────────
    if page_size > 0:
        size_kb = page_size / 1024
        check("Page size under 200KB", size_kb < 200, 5, f"{size_kb:.1f}KB", "Reduce HTML size — minify CSS/JS, lazy-load images")
    
    # ── CTA ──────────────────────────────────────────────────────
    cta_words = ["sign up", "get started", "free trial", "start free", "try free", "learn more", "get started"]
    has_cta = any(w in html_lower for w in cta_words)
    check("Call-to-action present", has_cta, 10, "CTA text found" if has_cta else "No CTA words found", "Add clear CTA button with action words")

    # ── Summary ──────────────────────────────────────────────────
    pct = int((score_total / score_max) * 100) if score_max > 0 else 0
    color = GREEN if pct >= 80 else YELLOW if pct >= 60 else RED
    print(f"\n{'='*55}")
    print(f"SEO SCORE: {color}{score_total}/{score_max} ({pct}%){RESET}")

    if pct >= 80:
        print(f"{GREEN}Strong SEO foundation.{RESET}")
    elif pct >= 60:
        print(f"{YELLOW}Good start — fix the issues below for a big ranking boost.{RESET}")
    else:
        print(f"{RED}Needs work — these fixes will dramatically improve rankings.{RESET}")

    if fixes:
        print(f"\nTop fixes by impact:")
        for pts, label, fix in sorted(fixes, reverse=True)[:8]:
            print(f"  [{pts}pts] {label}: {fix}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--keywords", nargs="+", default=[])
    args = parser.parse_args()
    run_seo(args.url, args.keywords)
