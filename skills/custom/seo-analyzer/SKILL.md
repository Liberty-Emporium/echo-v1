# seo-analyzer

Analyze and score any of Jay's app landing pages for SEO.
Checks meta tags, keywords, page speed signals, content quality, and gives a fix list.

## Usage

```
SEO check: <URL>
```

## What It Checks

### Technical SEO
- Title tag (length, keywords)
- Meta description (length, keywords)
- Open Graph tags (og:title, og:description, og:image)
- Twitter Card tags
- Canonical URL
- robots.txt present
- sitemap.xml present
- H1 tag present and correct
- Image alt tags

### Content SEO
- Keyword density for target terms
- Word count (landing pages need 300+ words)
- Internal links
- CTA presence

### Performance Signals
- Page size
- Render-blocking resources
- Mobile viewport meta tag

## Output

Scores each category 0-100 and gives specific fixes ranked by impact.

## Script

`scripts/seo_check.py`

## Example

```bash
python3 skills/custom/seo-analyzer/scripts/seo_check.py \
  --url https://liberty-emporium-and-thrift-inventory-app-production.up.railway.app
```
