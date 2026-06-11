---
name: ai-website-builder
description: AI-powered website building for small businesses — generate professional sites in minutes, compare free AI builders, optimize for SEO
version: 1.0.0
platforms: [linux, macos, websites]
status: UNTESTED
---

# AI Website Builder for Small Business

## When to use
- Building a new small business website quickly
- Comparing AI website builders
- Optimizing an existing site with AI
- Adding AI features to an existing website

## Key Stat
AI website builders can generate a professional website in 30 seconds, with built-in SEO, analytics, and e-commerce (2026).

## Free AI Website Builders Comparison

| Tool | Free Tier | AI Quality | Customization | Best For |
|------|-----------|-----------|---------------|----------|
| **Zylo** | Generous free | High | Medium | Full AI generation |
| **Bookipi** | Free | Medium | Low | 30-second sites |
| **Wix** | Free tier | High | High | Design flexibility |
| **SITE123** | Free | Medium | Low | Simplicity |

## Implementation Pattern

### Step 1: Generate with AI
```
Input: Business name, type, description, target audience
  → AI generates site structure
  → AI creates design and layout
  → AI writes content for each page
  → AI optimizes for SEO
  → Review and customize
  → Publish
```

### Step 2: Optimize
```
- Add custom domain (free with some builders)
- Set up Google Analytics
- Add structured data (Schema.org)
- Optimize images
- Set up contact form
- Add social media links
```

### Step 3: Maintain
```
- Update content monthly
- Monitor analytics
- Refresh design annually
- Add new features as business grows
```

## Best Practices
1. **Start with AI, customize after** — Don't accept the first draft
2. **Mobile-first** — Most visitors are on mobile
3. **Fast loading** — Compress images, minimize code
4. **Clear CTA** — Every page should have a call to action
5. **SEO from day one** — Meta titles, descriptions, structured data

## Pitfalls
- Don't use AI content without review — It may be generic
- Don't forget about accessibility — Alt text, contrast, keyboard nav
- Don't ignore page speed — Slow sites lose customers
- Don't skip the domain — Free subdomains look unprofessional

## Testing Checklist
- [ ] Site generates without errors
- [ ] Mobile responsive
- [ ] Page speed < 3 seconds
- [ ] SEO meta tags present
- [ ] Contact form works
- [ ] Analytics tracking works
- [ ] SSL certificate active

## Verification
```bash
# Test page speed
lighthouse https://yoursite.com --output json | jq '.categories.performance.score'

# Test mobile friendly
# Visit: https://search.google.com/test/mobile-friendly

# Test SSL
curl -I https://yoursite.com | grep -i "strict-transport"
```
