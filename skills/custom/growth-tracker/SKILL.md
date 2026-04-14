# growth-tracker

Track signups, conversions, churn and revenue across all Jay's apps.
Pulls metrics, spots trends, flags problems, suggests actions.

## Usage

```
Growth report: [all|<app-name>] [--period week|month]
```

## What It Tracks

### Acquisition
- New signups per day/week/month
- Trial starts
- Traffic sources (if analytics available)

### Conversion
- Trial → paid conversion rate (target: 20%+)
- Time to convert
- Features used before converting

### Retention
- Active users (logged in last 7/30 days)
- Churn rate (target: <5%/mo)
- Session frequency

### Revenue
- MRR (Monthly Recurring Revenue)
- ARR (Annual Run Rate)
- Revenue per app

## Revenue Targets (Jay's Portfolio)
| App | Price | Target Users | Target MRR |
|-----|-------|-------------|-----------|
| Liberty Inventory | $20/mo | 50 | $1,000 |
| Consignment Solutions | $20/mo | 50 | $1,000 |
| Contractor Pro AI | $99/mo | 20 | $1,980 |
| Dropship Shipping | $299 startup | 20/mo | $5,980 |
| Pet Vet AI | $9.99/mo | 200 | $1,998 |
| Keep Your Secrets | $14.99/mo | 100 | $1,499 |
| **TOTAL** | | | **$13,457 MRR** |

## Script

`scripts/growth_report.py`

## Example

```bash
python3 skills/custom/growth-tracker/scripts/growth_report.py \
  --app liberty-inventory \
  --db /data/liberty.db
```
