---
name: ai-inventory-agent
description: AI-powered inventory management for small businesses — demand forecasting, automated reordering, anomaly detection, supplier integration
version: 1.0.0
platforms: [linux, macos, websites]
status: UNTESTED
---

# AI Inventory Agent for Small Business

## When to use
- Managing product inventory for a small business
- Predicting demand and automating reorders
- Detecting anomalies (theft, spoilage, errors)
- Optimizing stock levels to reduce carrying costs

## Key Stat
AI inventory management systems enable real-time tracking with up-to-the-minute insights, reducing overstock by 30% and stockouts by 40% (2026).

## Free/Open Source Options

| Tool | Type | Free Tier | Best For |
|------|------|-----------|----------|
| **Google Sheets + AI** | DIY | Free | Simple inventory (< 100 SKUs) |
| **inFlow** | SaaS | Free trial | Small business |
| **Sortly** | SaaS | Free tier | Visual inventory |
| **Snipe-IT** | Open source | Self-hosted | Asset tracking |

## Implementation: Google Sheets + AI (Free, DIY)

### Step 1: Set Up Inventory Spreadsheet
```
Sheet: Inventory
| SKU | Product | Current Stock | Min Threshold | Max Capacity | Reorder Qty | Supplier | Cost | Last Updated |
|---------|---------|---------------|---------------|--------------|-------------|----------|------|--------------|
| SKU001 | Widget A| 45 | 20 | 100 | 50 | SupplierX | $5.00 | 2026-06-10 |
| SKU002 | Widget B| 12 | 15 | 80 | 40 | SupplierY | $8.00 | 2026-06-10 |
```

### Step 2: Add AI Formulas
```
// Days of stock remaining (based on avg daily sales)
=Current_Stock / AVERAGE(Daily_Sales_Range)

// Reorder flag
=IF(Current_Stock <= MinThreshold, "REORDER", "OK")

// Reorder quantity needed
=IF(Current_Stock <= MinThreshold, MaxCapacity - Current_Stock, 0)

// Estimated days until stockout
=Current_Stock / AVERAGE(Last_30_Days_Sales)
```

### Step 3: Set Up Automated Alerts
```javascript
// Google Apps Script (free)
function checkInventory() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Inventory');
  const data = sheet.getDataRange().getValues();
  
  for (let i = 1; i < data.length; i++) {
    const [sku, product, current, minThreshold] = data[i];
    
    if (current <= minThreshold) {
      // Send alert email
      MailApp.sendEmail({
        to: 'owner@business.com',
        subject: `REORDER ALERT: ${product} (${sku})`,
        body: `Stock for ${product} is at ${current} units.\nThreshold: ${minThreshold}\nPlease reorder immediately.`
      });
    }
  }
}

// Set trigger: Daily at 8 AM
```

### Step 4: Demand Forecasting (Simple)
```
// 30-day moving average
=AVERAGE(B2:B31)

// Trend detection (increasing/decreasing)
=SLOPE(B2:B31, A2:A31)

// Seasonal adjustment (if you have year-over-year data)
=FORECAST.LINEAR(date, sales_range, date_range)
```

## Implementation: Snipe-IT (Self-Hosted, Full Control)

### Steps
```bash
# Clone Snipe-IT
git clone https://github.com/snipe/snipe-it.git
cd snipe-it

# Copy environment
cp .env.example .env

# Configure database, mail, etc.
# Edit .env

# Install dependencies
composer install
php artisan key:generate

# Run migrations
php artisan migrate --seed

# Start server
php artisan serve
```

## Integration Patterns

### Pattern 1: Automated Reorder
```
Daily check → AI analyzes inventory
  → Stock < threshold? → Generate purchase order
  → Email supplier with order details
  → Update expected delivery date
  → Alert owner for approval (if > $X)
```

### Pattern 2: Anomaly Detection
```
AI monitors inventory changes
  → Sudden drop? → Flag as potential theft
  → Slow movement? → Flag as overstock
  → Seasonal spike? → Adjust forecast
  → Supplier delay? → Find alternative
```

### Pattern 3: Demand Forecasting
```
Historical sales → AI model
  → Predict next 30 days demand
  → Adjust reorder points
  → Optimize stock levels
  → Reduce carrying costs
```

## Best Practices
1. **Start simple** — Google Sheets works for < 100 SKUs
2. **Set thresholds carefully** — Too low = stockouts, too high = waste
3. **Review weekly** — AI helps but humans make final decisions
4. **Track everything** — Every sale, return, and adjustment
5. **Integrate with POS** — Automatic inventory updates

## Pitfalls
- Don't trust AI forecasts blindly — review and adjust
- Don't set and forget thresholds — review monthly
- Don't ignore slow movers — they tie up capital
- Don't forget safety stock — for unexpected demand

## Testing Checklist
- [ ] Inventory spreadsheet tracks all products
- [ ] Reorder alerts trigger correctly
- [ ] Demand forecast is reasonable
- [ ] Email notifications work
- [ ] Mobile access works
- [ ] Data backup configured

## Verification
```bash
# Test Google Apps Script trigger
# Run manually in Apps Script editor, check email

# Test Snipe-IT
curl -s http://localhost:8000/api/v1/hardware | python3 -m json.tool
```
