---
name: ai-analytics-agent
description: AI-powered business analytics and decision making for small businesses — natural language queries, predictive analytics, automated dashboards
version: 1.0.0
platforms: [linux, macos, websites]
status: UNTESTED
---

# AI Analytics Agent for Small Business

## When to use
- Analyzing business data (sales, customers, inventory)
- Creating automated dashboards
- Generating insights from data
- Predictive analytics (sales forecasting, churn prediction)
- Natural language queries ("What were last month's top products?")

## Free/Open Source Options

| Tool | Type | Free Tier | Best For |
|------|------|-----------|----------|
| **Metabase** | Open source | Self-hosted | Business intelligence |
| **Apache Superset** | Open source | Self-hosted | Data visualization |
| **Google Looker Studio** | SaaS | Free | Dashboards |
| **n8n + AI** | Open source | Self-hosted | Automated analysis |

## Implementation: Metabase (Self-Hosted)

### Steps
```bash
# Run with Docker
docker run -d -p 3000:3000 --name metabase metabase/metabase

# Access at http://localhost:3000
# Connect to your database (MySQL, PostgreSQL, SQLite)
# Create dashboards and questions
```

### Connect Data Sources
```
1. Google Sheets (via CSV import or direct connection)
2. MySQL/PostgreSQL database
3. CSV files
4. API endpoints
```

### Create Dashboards
```
- Sales overview (daily, weekly, monthly)
- Top products
- Customer acquisition
- Inventory levels
- Marketing performance
```

## Implementation: Google Looker Studio (Free, No Setup)

```
1. Go to https://lookerstudio.google.com
2. Connect data source (Google Sheets, CSV, database)
3. Create reports with drag-and-drop
4. Schedule email delivery of reports
5. Share with team
```

## Natural Language Queries

With AI integration, you can ask questions in plain English:
- "What were our top 5 products last month?"
- "Show me sales trend for the last 6 months"
- "Which customers haven't purchased in 90 days?"
- "What's our average order value?"

## Best Practices
1. **Start with key metrics** — Revenue, customers, orders
2. **Automate reporting** — Weekly email with key numbers
3. **Make it visual** — Charts > tables
4. **Keep it simple** — 5-10 key metrics max on main dashboard
5. **Review weekly** — Data is only useful if you act on it

## Pitfalls
- Don't track everything — Focus on actionable metrics
- Don't ignore data quality — Garbage in, garbage out
- Don't set and forget — Review and update dashboards
- Don't forget mobile — Check dashboards on phone

## Testing Checklist
- [ ] Dashboard loads correctly
- [ ] Data is accurate
- [ ] Charts render properly
- [ ] Filters work
- [ ] Scheduled reports send
- [ ] Mobile responsive

## Verification
```bash
# Test Metabase API
curl -s http://localhost:3000/api/session \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "admin@business.com", "password": "password"}'
```
