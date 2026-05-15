---
name: pdf-builder
description: Build professional, multi-page PDF documents from scratch — proposals, reports, invoices, contracts, one-pagers. Use when asked to create, generate, or rebuild a PDF file. Handles layout, branding, clickable links, comparison tables, signature blocks, and payment terms. Built on WeasyPrint (HTML→PDF). Use for any request to "make a PDF", "build a proposal", "create a document", or "generate a report".
---

# PDF Builder

Build professional PDFs by writing clean HTML/CSS and rendering with WeasyPrint.

## Quick Start

```bash
# Render HTML to PDF
python3 scripts/build_pdf.py input.html output.pdf
```

The script auto-installs `weasyprint` and `pymupdf` if missing, renders the PDF, and prints a verification summary (page count + broken glyph check + links).

## Workflow

1. **Write HTML** — Use the design system in `references/design-system.md`
2. **Build** — `python3 scripts/build_pdf.py input.html output.pdf`
3. **Verify** — Script auto-checks page count and null bytes
4. **Iterate** — Adjust spacing/font sizes if pages overflow

## Page Structure (always use this shell)

```html
<div class="page">
  <div class="hdr">...</div>       <!-- pages 2+ only -->
  <div class="body">               <!-- flex:1, takes available space -->
    <!-- content here -->
  </div>
  <!-- Optional: spacer + pinned element at bottom -->
  <div style="flex:1;"></div>
  <div class="pinned-element">...</div>
  <div class="ftr">...</div>       <!-- always last -->
</div>
```

**Critical:** `.page` must have `height:11in` and `display:flex; flex-direction:column`. See `references/design-system.md` for full CSS.

## Design Reference

See `references/design-system.md` for:
- Full CSS boilerplate (page setup, typography, colors)
- All common components (cards, tables, headers, footers, access cards)
- Emoji safety notes
- Spacing reference table
- Tips for fitting content on letter-size pages

## Proposal Template

`assets/proposal-template.html` — A complete 5-page business proposal (Sweet Spot Custom Cakes). Use as a starting point for any proposal or multi-page document. Demonstrates:
- Cover page with hero + access card + promise banner
- Feature grid (12 items, 2-col)
- Module table (6-col, 3-per-row)
- Investment page (3 cards + comparison table + next steps)
- Why/signature page with sig block pinned to bottom

To reuse: copy the file, replace brand names, colors, and content. Run `build_pdf.py` to render.

## Common Patterns

### Payment Terms (always use exact dollar amounts)
```html
<div class="invest-grid">  <!-- 3-col grid -->
  <div class="inv-card inv-dark">$1,000 deposit</div>
  <div class="inv-card inv-green">$2,000 balance at $200/mo × 10 months</div>
  <div class="inv-card inv-pink">$200/mo ongoing service</div>
</div>
```

### Clickable Link Card
```html
<div class="access-card">
  <div class="ac-main">
    <div class="ac-pill">🔗 Live App — Click to Access</div>
    <a class="ac-link" href="https://example.com">example.com</a>
  </div>
  <div class="ac-sep"></div>
  <div class="ac-field">
    <div class="ac-field-label">Username</div>
    <div class="ac-field-val">user@example.com</div>
  </div>
  <div class="ac-sep"></div>
  <div class="ac-field">
    <div class="ac-field-label">Password</div>
    <div class="ac-field-val">password123</div>
  </div>
</div>
```

### Signature Block Pinned to Bottom
```html
  </div><!-- close .body -->
  <div style="flex:1;"></div>
  <div class="sig-box" style="margin:0 0.5in 0.15in;">
    <h3>✍️ Acceptance & Agreement</h3>
    <div class="sig-cols">
      <div>
        <div class="sig-line"><div class="sig-line-label">Signature</div></div>
        <div class="sig-line" style="margin-top:0.08in;"><div class="sig-line-label">Date</div></div>
      </div>
      <div>
        <div class="sig-line"><div class="sig-line-label">Authorized Signature</div></div>
        <div class="sig-line" style="margin-top:0.08in;"><div class="sig-line-label">Date</div></div>
      </div>
    </div>
  </div>
  <div class="ftr">...</div>
```

## Troubleshooting

| Problem | Fix |
|---|---|
| Page overflows (extra blank page) | Reduce `gap`, `padding`, or `font-size` on the long page |
| Broken emoji (`\x00`) | Replace with simpler emoji or plain text |
| Footer not at bottom | Ensure `.page` has `height:11in` + `display:flex; flex-direction:column` |
| GitHub blocks push | Never store API tokens in files committed to git |
| Links not clickable | Use `<a href="https://...">` — WeasyPrint auto-converts to PDF links |
