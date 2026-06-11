---
name: ai-content-seo-agent
description: AI-powered content generation and SEO optimization for small business websites — automated blog posts, keyword research, AI visibility tracking
version: 1.0.0
platforms: [linux, macos, websites]
status: UNTESTED
---

# AI Content & SEO Agent for Small Business

## When to use
- Generating blog posts and website content
- Optimizing existing content for SEO
- Automating social media content
- Tracking AI engine visibility (how AI cites your content)

## Key Stat
The average small business uses a median of 5 AI tools in 2026, with content generation being the #1 use case (SBE Council).

## Free/Open Source Options

| Tool | Type | Free Tier | Best For |
|------|------|-----------|----------|
| **Google AI Studio** | SaaS | Free | Content generation |
| **Surfer SEO** | SaaS | Free trial | Content optimization |
| **Schema.org** | Standard | Free | Structured data |
| **n8n + AI** | Open source | Self-hosted | Content automation |

## Implementation Pattern

### Step 1: Keyword Research
```bash
# Use Google Trends (free)
# Use Google Search Console (free)
# Use AnswerThePublic (free tier)
# Compile list of target keywords
```

### Step 2: Content Generation
```
Input: Target keyword + business info
  → AI generates blog post outline
  → AI writes first draft
  → Human reviews and edits
  → AI optimizes for SEO
  → Publish to website
```

### Step 3: SEO Optimization
```html
<!-- Essential meta tags -->
<title>Primary Keyword - Business Name</title>
<meta name="description" content="Compelling description with keyword (155 chars max)">

<!-- Structured data (Schema.org) -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Your Business",
  "address": {...},
  "telephone": "..."
}
</script>
```

### Step 4: AI Visibility Tracking
- Monitor how AI engines (ChatGPT, Claude, Perplexity) cite your content
- Track AI referral traffic in Google Analytics
- Optimize content for AI citations (clear, factual, well-structured)

## Best Practices
1. **Quality over quantity** — 1 great post/week > 5 mediocre ones
2. **Target long-tail keywords** — Less competition, higher conversion
3. **Update old content** — Refresh posts every 6 months
4. **Use structured data** — Helps AI understand your content
5. **Write for humans first** — AI optimization second

## Pitfalls
- Don't publish AI-generated content without human review
- Don't keyword stuff — Google penalizes this
- Don't ignore mobile — 60%+ of traffic is mobile
- Don't forget internal links — They help SEO significantly

## Testing Checklist
- [ ] Content generates without errors
- [ ] SEO score > 80 (Surfer or similar)
- [ ] Structured data validates (Google Rich Results Test)
- [ ] Mobile-friendly (Google Mobile-Friendly Test)
- [ ] Page speed < 3 seconds

## Verification
```bash
# Validate structured data
# Visit: https://search.google.com/test/rich-results

# Check page speed
lighthouse https://yoursite.com/blog/post --output json | jq '.categories.performance.score'
```
