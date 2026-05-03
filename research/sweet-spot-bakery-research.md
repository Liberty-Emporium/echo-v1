# Sweet Spot Custom Cakes — Bakery Operations Research
_Researched by Echo on 2026-05-03. Scraped and studied leading bakery software platforms._
_Sources: BakeOnyx, BakeSmart, BakeryMS, FlexiBake, Streamline, CakeDino, SweetStream, Cakey, industry reports_

---

## 🏆 What the Best Bakery Software Does (That We Don't Yet)

### 1. Order Lifecycle — Inquiry → Quote → Confirmed → In Production → Ready → Delivered
**Industry standard (BakeOnyx, BakeSmart, SweetStream):**
- Orders start as **inquiries** — customer fills a public form with what they want
- Baker reviews → generates a **quote** with line items, deposits, discounts
- Customer approves → one-click converts to confirmed order
- Auto-schedules into production based on pickup date
- Customer gets email/SMS confirmations at each stage

**Sweet Spot today:** Orders jump straight to "confirmed" — no inquiry/quote phase, no automated customer emails

**Ideas for us:**
- Add an **Inquiry form** at `/inquire` — public, no login needed
- Add a **Quotes tab** — generate quotes from inquiries, convert to orders
- Add **automated email triggers**: order confirmed, order ready, pickup reminder 24h before
- Add **event type tagging**: Birthday / Wedding / Corporate / Baby Shower / Other

---

### 2. Pricing Engine — The "Price Matrix"
**Industry standard (BakeSmart Cake Matrix, BakeOnyx):**
- Define pricing rules ONCE: size × flavor × filling × frosting × add-ons
- Every order auto-calculates the correct price — no mental math, no undercharging
- Upsells (photo print topper, fondant, multi-tier) add to price automatically
- Prevents staff from accidentally under-pricing custom orders

**Sweet Spot today:** Prices are entered manually per order — risk of undercharging

**Ideas for us:**
- Build a **Cake Price Matrix**: rows = sizes (6", 8", 10", 12", Sheet), columns = flavors
- Add-on pricing table: Photo Print = +$15, Fondant = +$20, Custom Message = +$5, etc.
- Auto-calculate order total from selections instead of free-text price entry

---

### 3. Deco Tickets / Production Tickets
**Industry standard (BakeSmart, BakeOnyx):**
- Every custom order auto-generates a **Deco Ticket** — printable card for the decorator
- Contains: customer name, pickup date/time, size, flavor, filling, frosting, decoration instructions, inspiration photo URL, message on cake
- Organizes by production day — baker sees "Tuesday: 3 rounds, 2 sheets"
- Separate from the customer-facing receipt — internal use only

**Sweet Spot today:** We have the "Kitchen Production Sheet" but it's one big list — no per-order printable deco tickets

**Ideas for us:**
- Add `/orders/<id>/deco-ticket` — printable one-page ticket with all decoration details
- Add a **"Print Deco Ticket"** button on each order card in Kitchen Queue
- Add a **daily layer count report**: "Tuesday needs: 4 × 10" rounds, 2 × sheet cakes"

---

### 4. Customer Portal & Online Ordering
**Industry standard (BakeOnyx, UnifiedCommerce, BakeryMS):**
- Customers build their own cake: choose size → flavor → filling → frosting → add-ons → upload photo
- See real-time price as they customize
- Choose pickup time from available calendar slots
- Pay deposit online (Stripe) to lock in the order
- Get SMS/email reminders 24h before pickup

**Sweet Spot today:** All orders are placed by Jay or staff — no self-service customer ordering

**Ideas for us (Phase 1 — easy wins):**
- `/order-online` public form: size, flavor, occasion, message, pickup date, contact info
- Show available pickup slots (block out already-booked slots)
- Collect deposit via Stripe at submission
- Auto-send confirmation email + SMS

**Ideas for us (Phase 2):**
- Full cake builder UI: customers pick options and see price update live
- Customer can upload inspiration photo right in the form
- Account portal: customers see order status, pay balance, re-order

---

### 5. Production Scheduling & Daily Kitchen View
**Industry standard (BakeOnyx Production Scheduler, FlexiBake, Streamline):**
- System looks at all confirmed orders → generates a **production schedule** by day
- Groups orders by bake type: "All 10" rounds bake together, then sheets"
- Shows total ingredient quantities needed for the whole day (not per order)
- Flags if any ingredient is low stock before the bake day
- Oven optimization: sequences items by bake temperature to minimize oven adjustments

**Sweet Spot today:** Kitchen Queue shows orders individually but no aggregate view

**Ideas for us:**
- Add a **"Today's Bake Summary"** at the top of Kitchen Queue:
  - Total cakes by size: "3 × 10", 2 × 8", 1 × sheet"
  - Total ingredient pulls: "Flour: 12 cups, Butter: 3 lbs, Eggs: 24..."
  - Total estimated bake time
- **Prep Timeline**: auto-generate a start time for each item based on pickup time + bake/cool/decorate time
- **Day-before alert**: notify baker of tomorrow's orders at 4pm today

---

### 6. Demand Forecasting & Waste Reduction
**Industry standard (BakeOnyx, FoodForecast, echelon-advising):**
- AI studies order history → predicts demand by day of week, season, holidays
- Tells baker: "Saturday usually needs 8 cakes — book up to 10"
- Reduces overproduction waste by 20-30%
- For standard items (cookies, cupcakes): auto-suggests daily bake quantities
- Custom cakes are always make-to-order — no forecasting needed there

**Industry stats:**
- AI forecasting achieves 85-95% accuracy after 3-4 weeks of data
- Reduces waste $800-$3,000/month for a small bakery
- Saves 45-60 min/day on production planning

**Ideas for us:**
- Track which days of week generate most orders → show in dashboard
- Holiday rush mode: "Mother's Day is in 2 weeks — here are your bookings"
- Low-stock warning 3 days before a busy weekend

---

### 7. Inventory Automation
**Industry standard (BakeOnyx, Streamline, FlexiBake):**
- When an order is placed, inventory is automatically decremented based on recipe ingredients
- Par-level alerts: "Butter below 2 lbs — reorder"
- Auto-generates draft purchase orders when stock hits reorder point
- FIFO enforcement: use oldest stock first
- Tracks waste separately from usage

**Sweet Spot today:** Inventory exists but is manually managed — no auto-decrement from orders

**Ideas for us:**
- When order is moved to "In Production": auto-deduct recipe ingredients from inventory
- Add **reorder levels** to each ingredient: alert when stock falls below threshold
- Add a **"Shopping List"** button: generates purchase list for all orders due this week

---

### 8. VIP Loyalty & Customer Intelligence
**Industry standard (BakeOnyx, Cakey):**
- Points-based loyalty: earn points per dollar spent
- Tiers: Bronze → Silver → Gold → Platinum
- Birthday alerts: "Jay Alexander's birthday is in 3 weeks — send a promo"
- Churn prediction: "This customer hasn't ordered in 90 days — send a win-back offer"
- Customer Lifetime Value tracking

**Sweet Spot today:** Has VIP Loyalty section in nav — check what's built

**Ideas for us:**
- Birthday field on customer profile → auto-email promo 2 weeks before
- "You ordered a Rich Chocolate 10" last year — want to order again?" (anniversary re-order prompt)
- Points display on customer-facing receipts

---

### 9. Staff Scheduling & Payroll Prep
**Industry standard (BakeOnyx Scale, Homebase):**
- Weekly shift grid: drag-and-drop scheduling
- Staff availability management
- Shift swap requests
- Labor cost tracking with overtime alerts
- Time clock: clock in/out from the app

**Sweet Spot today:** Has Employees and Payroll in nav — check what's built there

**Ideas for us:**
- Shift schedule that ties to kitchen workload: "Saturday has 6 orders — schedule 2 bakers"
- Labor cost vs revenue tracking per shift

---

### 10. PDF Documents & Professional Branding
**Industry standard (BakeOnyx, SweetStream, BakeSmart):**
- **Invoice PDF**: customer-facing, branded, shows deposit paid/balance due
- **Deco Ticket PDF**: internal, one per order, for the decorator
- **Production Summary PDF**: daily bake sheet for the baker
- **Recipe Card PDF**: ingredient list + steps for a specific recipe

**Sweet Spot today:** "Full Sheet" button exists — check if it's printable/PDF-ready

**Ideas for us:**
- `?format=print` on Kitchen Order page → CSS print stylesheet → clean printable output
- Auto-email invoice PDF to customer when order is confirmed
- Deco ticket page at `/orders/<id>/deco-ticket` (printable, no nav)

---

## 🎯 Priority Feature Roadmap for Sweet Spot

### Tier 1 — High Impact, Relatively Easy (build next)
| Feature | Impact | Why |
|---------|--------|-----|
| Automated customer emails (confirm, ready, pickup reminder) | 🔥🔥🔥 | Eliminates manual calls, reduces no-shows |
| Deco Tickets (printable per-order card) | 🔥🔥🔥 | Decorator efficiency, fewer mistakes |
| Price Matrix / auto-pricing by size+flavor+add-ons | 🔥🔥🔥 | Stop undercharging custom orders |
| Daily Bake Summary (aggregate ingredients + cake count) | 🔥🔥 | Baker sees total workload at a glance |
| Inquiry/Quote flow before confirmed order | 🔥🔥 | Professional workflow, reduce wasted consults |

### Tier 2 — Medium Impact (build after Tier 1)
| Feature | Impact | Why |
|---------|--------|-----|
| Online ordering form with pickup time slots | 🔥🔥🔥 | Customers self-serve, Jay doesn't need to take every order by phone |
| Stripe deposit collection on order form | 🔥🔥🔥 | No deposit = no commitment = lots of no-shows |
| Inventory auto-deduct when order goes to production | 🔥🔥 | Know what you need before you run out |
| Shopping List (weekly ingredient pull from orders) | 🔥🔥 | Prep shopping before the weekend rush |
| Prep Timeline (auto start times based on pickup) | 🔥🔥 | Baker knows when to start each item |

### Tier 3 — Growth Features (build when scaling)
| Feature | Impact | Why |
|---------|--------|-----|
| Customer online ordering portal (full cake builder) | 🔥🔥🔥 | Scale without adding staff |
| Birthday promo automation | 🔥🔥 | Repeat business engine |
| Demand forecasting / busy day alerts | 🔥 | Nice to have once order volume is high |
| Staff scheduling tied to order load | 🔥 | Once you have multiple staff |
| Multi-location support | 🔥 | Future expansion |

---

## 🔍 Competitors to Watch

| Platform | Who it's for | Key differentiator |
|----------|-------------|-------------------|
| **BakeOnyx** (bakeonyx.ai) | Custom cake shops | AI storefront, inquiry→quote→order workflow, production scheduler |
| **BakeSmart** (bakesmart.com) | Mid-size retail bakeries | Cake Matrix pricing, Deco Tickets, production reports |
| **CakeDino** (cakedino.com) | Small cake studios | Simple, order pipeline, production calendar |
| **SweetStream** (sweetstream.app) | Solo cake makers | Minimal, enquiry management, Stripe deposits |
| **Cakey** (cakey.app) | Home bakers scaling up | Recipe costing, automated invoicing |
| **FlexiBake** (flexibake.com) | Wholesale/commercial | Full ERP, standing orders, route management |
| **BakeryMS** (bakeryms.com) | Multi-location factories | Label-based production tracking, AI invoice parsing |

**Sweet Spot's niche:** Custom cake shop, single location, Jay + small team. 
**Best comparable:** BakeOnyx / BakeSmart — but we're building our own, which means we can customize exactly for how Jay works.

---

## 💡 Quick Wins to Build Right Now

### 1. Automated Customer Emails (2-3 hours to build)
Trigger emails at:
- Order confirmed → "Your order #SS-XXXX is confirmed! Pickup: [date/time]"
- Order status → "In Production" → "We're baking your [item] now! 🎂"
- Order ready → "Your order is ready for pickup!"
- 24h before pickup → reminder with order details

### 2. Printable Deco Ticket (1-2 hours)
New route: `/orders/<id>/deco-ticket`
- No navbar, print-friendly
- Shows: order ID, customer name + phone, pickup date/time, each item with full custom details (size, flavor, occasion, message, add-ons), reference photos, notes
- Print button

### 3. Daily Bake Summary Header in Kitchen Queue (2-3 hours)
At top of `/kitchen` page, add a summary card:
```
📊 Today's Production (3 orders)
├── Cakes: 2 × 10" Round  |  1 × Sheet
├── Ingredients needed: Flour 8c, Butter 2lb, Eggs 18, Sugar 4c
├── Total bake time: ~4h 30min
└── All orders ready by: 5:00 PM
```

### 4. Price Matrix (3-4 hours)
New admin page: `/admin/pricing`
- Grid: Size (rows) × Base Price
- Add-on table: Photo Print, Fondant, Multi-tier, Custom Message
- When creating an order: select size → price auto-fills from matrix

---

## 📊 Industry Stats Worth Knowing

- Custom cakes: **60-75% gross margin** (vs 50-60% for everyday baked goods) — highest margin product
- AI demand forecasting: **85-95% accuracy** after 3-4 weeks of data
- Waste reduction from automation: **20-30%** = $800-$3,000/month for small bakeries
- No-show reduction from automated reminders: **29%** fewer no-shows
- Production scheduling automation: saves **35-40% of manual planning time**
- Online self-ordering increases average order value by **40%** (customers explore options freely)
- Automated customer reminders pay back within **1.5 weeks**

---

_This research is stored permanently in echo-v1/research/ for continuity across reboots._
_Next step: Jay reviews Tier 1 priorities and we decide what to build first._
