# seo-flask

**Version:** 1.0.0
**Created:** 2026-04-18
**Author:** Echo

## Description

SEO optimization for Jay's Flask SaaS apps. Meta tags, sitemap.xml, robots.txt, Core Web Vitals, and structured data. All apps already have og:image — this covers the remaining gaps.

## Status Per App

All 7 apps have: ✅ og:image (preview.png embedded as base64)

Still needed across apps:
- [ ] sitemap.xml route
- [ ] robots.txt route
- [ ] Canonical URL meta tag
- [ ] Structured data (JSON-LD) on landing pages
- [ ] Core Web Vitals optimization (LCP, CLS, INP)

## 1. Meta Tags (base.html head block)

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- Primary SEO -->
  <title>{% block title %}{{ app_name }}{% endblock %}</title>
  <meta name="description" content="{% block description %}{{ app_description }}{% endblock %}">
  <meta name="keywords" content="{% block keywords %}{% endblock %}">
  <link rel="canonical" href="{{ request.url }}">

  <!-- Open Graph (social sharing) -->
  <meta property="og:title" content="{% block og_title %}{{ app_name }}{% endblock %}">
  <meta property="og:description" content="{% block og_description %}{{ app_description }}{% endblock %}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{{ request.url }}">
  <meta property="og:image" content="{{ og_image_b64 }}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{% block twitter_title %}{{ app_name }}{% endblock %}">
  <meta name="twitter:description" content="{% block twitter_description %}{{ app_description }}{% endblock %}">
  <meta name="twitter:image" content="{{ og_image_b64 }}">
</head>
```

## 2. sitemap.xml Route

```python
from flask import make_response, render_template_string
from datetime import datetime

SITEMAP_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{% for url in urls %}
  <url>
    <loc>{{ url.loc }}</loc>
    <lastmod>{{ url.lastmod }}</lastmod>
    <changefreq>{{ url.changefreq }}</changefreq>
    <priority>{{ url.priority }}</priority>
  </url>
{% endfor %}
</urlset>"""

@app.route('/sitemap.xml')
def sitemap():
    base = request.host_url.rstrip('/')
    today = datetime.now().strftime('%Y-%m-%d')
    urls = [
        {'loc': base + '/', 'lastmod': today, 'changefreq': 'weekly', 'priority': '1.0'},
        {'loc': base + '/wizard', 'lastmod': today, 'changefreq': 'monthly', 'priority': '0.9'},
        {'loc': base + '/login', 'lastmod': today, 'changefreq': 'monthly', 'priority': '0.5'},
        {'loc': base + '/pricing', 'lastmod': today, 'changefreq': 'weekly', 'priority': '0.8'},
    ]
    response = make_response(render_template_string(SITEMAP_TEMPLATE, urls=urls))
    response.headers['Content-Type'] = 'application/xml'
    return response
```

## 3. robots.txt Route

```python
@app.route('/robots.txt')
def robots():
    base = request.host_url.rstrip('/')
    content = f"""User-agent: *
Allow: /
Disallow: /dashboard
Disallow: /overseer
Disallow: /admin
Disallow: /api/

Sitemap: {base}/sitemap.xml
"""
    return content, 200, {'Content-Type': 'text/plain'}
```

## 4. Structured Data (JSON-LD) for Landing Page

```html
<!-- In landing page template, inside <head> -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "{{ app_name }}",
  "description": "{{ app_description }}",
  "applicationCategory": "BusinessApplication",
  "offers": {
    "@type": "Offer",
    "price": "{{ monthly_price }}",
    "priceCurrency": "USD",
    "priceValidUntil": "2027-12-31"
  },
  "operatingSystem": "Web"
}
</script>
```

## 5. Core Web Vitals Optimization

### LCP (Largest Contentful Paint) — Target: < 2.5s
```html
<!-- Preload hero image (LCP element) -->
<link rel="preload" as="image" href="{{ hero_image_url }}">

<!-- Never lazy-load above-the-fold images -->
<!-- WRONG: -->
<img loading="lazy" src="hero.webp">
<!-- RIGHT: -->
<img src="hero.webp" width="800" height="400">

<!-- Inline critical CSS (avoids render-blocking) -->
<style>
/* Only above-the-fold styles here */
body { margin: 0; font-family: sans-serif; }
.hero { background: #1a1a2e; color: white; padding: 80px 20px; }
</style>
<!-- Non-critical CSS loads after -->
<link rel="stylesheet" href="/static/style.css" media="print" onload="this.media='all'">
```

### CLS (Cumulative Layout Shift) — Target: < 0.1
```html
<!-- Always set width/height on images to prevent layout shift -->
<img src="logo.png" width="120" height="40" alt="Logo">

<!-- Reserve space for dynamic content -->
<div style="min-height: 200px">
  <!-- content loaded here -->
</div>
```

### Defer Non-Critical JavaScript
```html
<!-- WRONG: blocks render -->
<script src="/static/app.js"></script>

<!-- RIGHT: defer non-critical -->
<script src="/static/app.js" defer></script>
```

## 6. Apply to All 7 Apps Checklist

```bash
# For each app, add these routes to app.py:
# - /sitemap.xml
# - /robots.txt
# Update base.html with full meta tags block
# Add JSON-LD to landing page (index.html)
# Preload hero image
# Defer non-critical JS
# Submit sitemap to Google Search Console
```

## Per-App Target Keywords

| App | Primary Keyword |
|-----|----------------|
| Liberty Inventory | thrift store management software |
| Consignment Solutions | consignment store software |
| Contractor Pro AI | AI contractor management |
| Pet Vet AI | AI pet health diagnosis |
| Keep Your Secrets | API key management software |
| Dropship Shipping | dropshipping management software |
| AI Agent Widget | embeddable AI chat widget |
