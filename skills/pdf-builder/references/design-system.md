# PDF Design System Reference

A battle-tested CSS + HTML design system for professional PDFs with WeasyPrint.

## Page Setup

```css
@page { size: letter; margin: 0; }

.page {
  width: 8.5in;
  height: 11in;              /* Fixed height — critical for WeasyPrint */
  display: flex;
  flex-direction: column;    /* Enables flex children: header, body, footer */
  page-break-after: always;
  overflow: hidden;
}
.page:last-child { page-break-after: avoid; }
```

**Critical rules:**
- Always set `height: 11in` (not `min-height`) — WeasyPrint needs a fixed height for flex layout
- Use `display:flex; flex-direction:column` on `.page` so footer can be pinned with `margin-top:auto`
- Set `overflow:hidden` to prevent content from bleeding onto the next page

## Content Area

```css
.body {
  flex: 1;                   /* Takes all available space between header and footer */
  padding: 0.3in 0.5in 0.2in;
  overflow: hidden;
}
```

## Pinning Footer to Bottom

```css
.footer {
  margin-top: auto;          /* Pushes footer to bottom of flex column */
  flex-shrink: 0;
  background: #0f172a;
  padding: 0.07in 0.5in;
}
```

To pin a **signature block** or any element to the bottom of the page:
1. Close the `.body` div before it
2. Add a `<div style="flex:1;"></div>` spacer
3. Place the element after the spacer, before `.footer`

```html
  </div><!-- end .body -->
  <div style="flex:1;"></div>  <!-- spacer -->
  <div class="sig-box" style="margin: 0 0.5in 0.15in;">...</div>
  <div class="footer">...</div>
```

## Typography

```css
body {
  font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
  font-size: 9pt;
  line-height: 1.5;
  color: #1e293b;
}
/* Import Google Fonts at top of <style> — WeasyPrint fetches them */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
```

## Color Palette (Professional Dark/Pink Theme)

```
Navy dark:   #0f172a   (backgrounds, headers)
Navy mid:    #1e3a5f   (gradients)
Pink:        #ec4899   (accents, CTAs, links)
Pink dark:   #be185d   (hover, borders)
White:       #ffffff
Gray text:   #374151 / #64748b
Light bg:    #f8fafc
Border:      #e2e8f0
Green:       #10b981 (checkmarks, success)
Red:         #ef4444 (X marks, errors)
Amber:       #f59e0b (warnings, partial)
```

## Common Components

### Header Band (pages 2+)
```html
<div class="hdr">
  <div class="hdr-brand">Company Name</div>
  <div class="hdr-title">Document Title</div>
</div>
```
```css
.hdr {
  background: linear-gradient(90deg, #0f172a, #1e3a5f);
  padding: 0.1in 0.5in;
  display: flex; justify-content: space-between; align-items: center;
  flex-shrink: 0;
}
.hdr-brand { color: #ec4899; font-size: 7.5pt; font-weight: 800; letter-spacing: 0.18em; text-transform: uppercase; }
.hdr-title { color: rgba(255,255,255,0.5); font-size: 7pt; }
```

### Section Title
```css
.sec-title {
  font-size: 14pt; font-weight: 800; color: #0f172a;
  border-bottom: 2.5px solid #ec4899;
  padding-bottom: 0.05in; margin-bottom: 0.15in;
  display: flex; align-items: center; gap: 7px;
}
```

### Card Grid (2-col or 3-col)
```css
.card-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;   /* or repeat(3, 1fr) */
  gap: 0.09in;
}
.card {
  background: #f8fafc; border: 1px solid #e2e8f0;
  border-radius: 8px; padding: 0.1in 0.12in;
}
```

### Gradient Card (dark/pink)
```css
.card-dark { background: linear-gradient(135deg, #0f172a, #1e3a5f); color: #fff; border-radius: 10px; padding: 0.14in 0.16in; }
.card-pink { background: linear-gradient(135deg, #ec4899, #be185d); color: #fff; border-radius: 10px; padding: 0.14in 0.16in; }
```

### Comparison Table
```css
.cmp-table { width: 100%; border-collapse: collapse; font-size: 7.5pt; }
.cmp-table th { padding: 6px 8px; font-weight: 700; text-align: center; }
.cmp-table td { padding: 5px 8px; border-bottom: 0.5px solid #f1f5f9; text-align: center; }
.cmp-table td:first-child { text-align: left; font-weight: 500; }
.ck { color: #10b981; font-weight: 800; }   /* checkmark */
.cx { color: #ef4444; font-weight: 800; }   /* X */
.cp { color: #f59e0b; font-size: 7.5pt; font-weight: 600; }  /* partial */
```

### Clickable Link Card (for credentials/CTAs)
```css
.access-card {
  background: linear-gradient(135deg, #0f172a, #1e3a5f);
  border: 2px solid #ec4899; border-radius: 12px;
  padding: 0.16in 0.25in;
  display: flex; align-items: center; gap: 0.2in;
}
.ac-link { color: #fff; font-size: 13pt; font-weight: 900; text-decoration: underline; text-decoration-color: #ec4899; }
```

### Footer
```html
<div class="ftr">
  <span>Company Name &nbsp;·&nbsp; tagline</span>
  <span><a href="mailto:email@example.com">email</a> &nbsp;·&nbsp; website</span>
</div>
```
```css
.ftr { background: #0f172a; padding: 0.07in 0.5in; display: flex; justify-content: space-between; align-items: center; flex-shrink: 0; }
.ftr span { color: rgba(255,255,255,0.45); font-size: 6.5pt; white-space: nowrap; }
.ftr a { color: #ec4899; text-decoration: none; font-size: 6.5pt; }
```

## Emoji Handling

WeasyPrint may render some emoji as `\x00` null bytes depending on the font stack.

**Safe:** Standard Unicode emoji rendered via DejaVuSans or Noto fonts (⚠️ ✅ ✓ ✗ ★)
**Risky:** Complex ZWJ sequences (👩‍🍳) and newer emoji — test before using

**To verify after build:**
```python
import fitz
doc = fitz.open("output.pdf")
for i in range(doc.page_count):
    if "\x00" in doc[i].get_text():
        print(f"Page {i+1} has broken glyphs")
```

## Spacing Reference

| Padding/gap | Use |
|---|---|
| `0.5in` | Page side margins |
| `0.3in` | Body top padding |
| `0.2in` | Body bottom padding |
| `0.15in` | Between sections |
| `0.09in–0.12in` | Card gaps |
| `0.07in` | Footer padding |

## Sizing That Fits on Letter Paper

Page height = 11in. Typical usable body height after header + footer ≈ 9.5in.

**Pages that tend to overflow and need compact sizing:**
- Feature grids (12 cards) → use `gap: 0.09in`, `padding: 0.09in`, `font-size: 7.8pt`
- Module tables (3-col, 6 cols × 10 rows) → use `font-size: 7.4pt`, `padding: 6px 10px`
- Investment + comparison table + next steps → tight but fits with `font-size: 7.5pt` table rows

## Clickable Links in PDF

WeasyPrint automatically converts `<a href="...">` tags to clickable PDF links.
Always use full URLs (`https://...`) for external links to ensure they work when emailed.
