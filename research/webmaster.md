# Webmaster Skills — Research Notes
**Researched:** 2026-04-14 | Echo's Self-Education Session

---

## The 9 Fundamental Webmaster Skills

1. **HTML/CSS** — Structure + style. Building blocks.
2. **JavaScript** — Interactivity, dynamic content
3. **SEO Knowledge** — Ranking, visibility, meta tags, site structure
4. **CMS Platforms** — WordPress, Joomla (know them even if we don't use them)
5. **Server Management** — Hosting environments, databases, uptime
6. **Security Best Practices** — SSL, firewalls, updates
7. **Analytics & Reporting** — Google Analytics, conversion tracking
8. **Responsive Design** — Mobile-first, works on all devices
9. **Basic Graphic Design** — Image editing, visual consistency

## 11 Secondary Webmaster Skills

1. **Version Control** (Git) — We already do this ✅
2. **Basic PHP** — Useful for WordPress/CMS work
3. **Email Marketing** — Newsletters, drip campaigns
4. **UX/UI Principles** — User-friendly navigation, clear CTAs
5. **Social Media Integration** — Share buttons, feeds
6. **Basic SQL** — Query databases ✅ (we use SQLite)
7. **Performance Optimization** — Speed = conversions
8. **Accessibility Standards** — WCAG 2.1, screen readers
9. **API Integration** — Payment gateways, third-party tools ✅
10. **Backup and Recovery** — Always have a recovery plan
11. **Basic Python** — Automation, data processing ✅

---

## Core Web Vitals — The SEO Speed Metrics That Matter

Google ranks sites based on these 3 scores. Pass = ranking boost. Fail = ranking penalty.

### The 3 Core Vitals
| Metric | What It Measures | Good Score |
|--------|-----------------|------------|
| **LCP** (Largest Contentful Paint) | How fast main content loads | < 2.5 seconds |
| **INP** (Interaction to Next Paint) | How fast page responds to clicks | < 200ms |
| **CLS** (Cumulative Layout Shift) | How much page jumps around | < 0.1 |

### Image Optimization Checklist
- [ ] Resize to match on-screen dimensions (50%+ file size reduction)
- [ ] Use WebP/AVIF formats (25-50% smaller than JPEG)
- [ ] Lazy load below-the-fold images (`loading="lazy"`)
- [ ] **NEVER** lazy load the LCP image (will destroy score)
- [ ] Preload LCP image with `fetchpriority="high"`
- [ ] Always set width + height attributes (prevents layout shift)
- [ ] Strip EXIF metadata
- [ ] Use `decoding="async"` on non-critical images

### Font Optimization
- [ ] Use `font-display: swap` — shows fallback while font loads
- [ ] Self-host fonts — avoid Google Fonts external requests
- [ ] Preload critical fonts
- [ ] Match fallback font dimensions to avoid layout shift on swap

### JavaScript Performance
- [ ] Defer non-critical scripts (`defer` attribute)
- [ ] Avoid render-blocking scripts in `<head>`
- [ ] Minify and compress JS
- [ ] Split code — only load what the page needs
- [ ] Remove unused JavaScript

### Server Response Times
- [ ] TTFB (Time to First Byte) < 800ms
- [ ] Use CDN for static assets
- [ ] Enable gzip/brotli compression
- [ ] Cache static assets (Cache-Control headers)
- [ ] Database queries must be indexed

### CSS Optimization
- [ ] Inline critical CSS (above-the-fold styles)
- [ ] Defer non-critical CSS
- [ ] Minify CSS
- [ ] Remove unused CSS (PurgeCSS)

---

## SEO Fundamentals Checklist

### Technical SEO (Foundation)
- [ ] HTTPS (SSL cert) — ranking factor
- [ ] Fast load time (Core Web Vitals passing)
- [ ] Mobile responsive
- [ ] Clean URL structure (`/products/name` not `/p?id=123`)
- [ ] sitemap.xml submitted to Google Search Console
- [ ] robots.txt configured
- [ ] No broken links (404s)
- [ ] Canonical tags (prevent duplicate content)
- [ ] Structured data / schema markup

### On-Page SEO (Per Page)
- [ ] Title tag: 50-60 chars, keyword first
- [ ] Meta description: 150-160 chars, compelling CTA
- [ ] H1 tag: exactly one per page, contains keyword
- [ ] H2/H3 tags: organize content, secondary keywords
- [ ] Image alt text: descriptive, keyword where natural
- [ ] Internal linking: link to related pages
- [ ] URL: short, descriptive, hyphen-separated

### Content SEO
- [ ] Target one primary keyword per page
- [ ] Use LSI keywords (related terms) naturally
- [ ] Content length: >1,000 words for competitive terms
- [ ] Update old content regularly
- [ ] Answer the user's question directly at the top

### What Matters Most in 2025
- **E-E-A-T** (Experience, Expertise, Authority, Trust) — Google's quality signal
- **Core Web Vitals** — Direct ranking factor
- **Mobile-first** — Google indexes mobile version
- **AI-generated content** — Fine if helpful, penalized if spam
- **Page experience signals** — Bounce rate, dwell time, engagement

---

## Landing Page Best Practices for Our SaaS Apps

Every app needs a killer landing page. Here's the formula:

### Above the Fold (What they see first)
1. **Headline** — What it does in 1 sentence. Benefit, not feature.
2. **Sub-headline** — Who it's for + main benefit
3. **CTA button** — "Start Free Trial" or "Get Started Free"
4. **Hero image/demo** — Show the product working

### Below the Fold (Convince them)
1. **Social proof** — Testimonials, logos, user count
2. **Features/Benefits** — 3-6 key selling points, icons
3. **How it works** — 3-step process
4. **Pricing** — Clear, transparent
5. **FAQ** — Objection handling
6. **Final CTA** — Repeat the button

### Conversion Optimization
- Single CTA per page — don't confuse visitors
- CTA button: contrasting color, action verb
- Remove navigation on landing pages (reduces distraction)
- Use urgency: "14-day free trial", "No credit card required"
- Mobile: big tap targets (min 44px), readable font (16px+)

---

## Analytics — What to Track for SaaS

### Acquisition Metrics
- Where are visitors coming from? (Google, Direct, Referral, Social)
- Which pages get the most traffic?
- Bounce rate per page

### Conversion Metrics
- Trial signup rate (visitors → trials)
- Trial → paid conversion rate
- Pricing page view → signup rate
- CTA click rate

### Retention Metrics
- Monthly Active Users (MAU)
- Churn rate (% of users who cancel)
- Net Revenue Retention (NRR)

### Tools
- Google Analytics 4 (GA4) — free, industry standard
- Google Search Console — SEO performance
- Hotjar / Microsoft Clarity — heatmaps, session recordings (free)
- PostHog — open source product analytics (can self-host)
