---
name: proposal-builder
description: Build a complete, professional business proposal PDF for a potential client of Alexander AI Integrated Solutions. Use when asked to "make a proposal", "write a proposal", "build a proposal for [client]", or "create a pitch document". Combines the pdf-builder skill with business-specific templates and pricing logic.
---

# Proposal Builder

Generate a polished, client-ready PDF proposal for Alexander AI Integrated Solutions.

## Standard Proposal Structure (5 pages)

1. **Cover** — Client name, date, valid-through date, live app access card, promise banner, challenge/solution
2. **What's Included** — Core features grid (12 features, 2-col)
3. **Full Platform** — All modules (6 columns, 3-per-row)
4. **Investment** — Payment terms + comparison table + next steps
5. **Why Us + Signature** — Why Alexander AI (6 cards) + sig block pinned to bottom

## Information to Collect Before Building

Ask the user for:
1. **Client name** (business name)
2. **Client industry** (bakery, restaurant, retail, salon, etc.)
3. **Total project fee** (default: $3,000)
4. **Deposit amount** (default: $1,000)
5. **Monthly rate** (default: $200/mo)
6. **Balance** = Total - Deposit (default: $2,000 = 10 months)
7. **Valid-through date** (default: 30 days from today)
8. **Live app URL** (if already built/demoed)
9. **Login credentials** for the demo app (if applicable)
10. **Prepared by** (default: Jay Alexander)
11. **Any custom features** specific to this client

## Pricing Logic

```
Standard Package:   $3,000 project fee
Deposit:            $1,000 due at signing
Balance:            $2,000
Monthly payments:   $200/mo × 10 months (balance)
Ongoing service:    $200/mo after payoff (hosting + AI + support)

Custom add-ons (suggest pricing):
  +$500  Extra integrations (QuickBooks, Doordash, etc.)
  +$500  Custom mobile app (PWA wrapper)
  +$250  Additional AI training / custom knowledge base
  +$300  Advanced analytics / custom reporting
  +$200  SMS notifications module
```

## Template File

Use `../pdf-builder/assets/proposal-template.html` as the base.

Steps:
1. Copy `../pdf-builder/assets/proposal-template.html` to `/tmp/proposal-[clientname].html`
2. Do a global find/replace for:
   - `Sweet Spot Custom Cakes` → client name
   - `May 2026` → current month/year
   - `May 30, 2026` → valid-through date
   - `$3,000` / `$1,000` / `$2,000` / `$200` → actual amounts
   - `sweet-spot-cakes.up.railway.app` → actual app URL
   - `info@sweetspotcustomcakes.com` → actual login
   - `sweetspot2026` → actual password
   - Feature descriptions → client-specific content if needed
3. Run `python3 ../pdf-builder/scripts/build_pdf.py /tmp/proposal-[clientname].html /tmp/proposal-[clientname].pdf`
4. Verify 5 pages, no nulls, clickable link on page 1
5. Copy to `/root/.openclaw/workspace/docs/proposal-[clientname].pdf`
6. Push to GitHub

## Industry Customizations

### Bakery / Cake Shop
- Keep all Sweet Spot content — it was purpose-built
- AI assistant name: Cakely
- Key features to highlight: custom orders, decoration tickets, pickup calendar, birthday marketing

### Restaurant / Café
- AI assistant name: suggest "TableBot" or "[Name]AI"
- Swap: "custom cakes" → "menu items", "pickup scheduling" → "reservation management"
- Add: table management, waitlist, tip tracking

### Retail Shop
- AI assistant name: suggest "[Name]Assist"
- Swap: kitchen/prep → warehouse/fulfillment
- Add: barcode scanning, product catalog, reorder alerts

### Salon / Spa
- AI assistant name: suggest "[Name]Book"
- Swap: orders → appointments, kitchen → treatment rooms
- Add: stylist scheduling, service menu, retail product sales

### Service Business (contractor, cleaner, etc.)
- AI assistant name: suggest "[Name]Dispatch"
- Swap: orders → service requests, kitchen → job queue
- Add: route optimization, job photos, invoice generation

## Output

Final PDF saved to:
`/root/.openclaw/workspace/docs/proposal-[clientname-lowercase].pdf`

Push to brain repo after every proposal.
