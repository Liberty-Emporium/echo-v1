# MEMORY.md - Long-term Memory

## Rules for Building Apps

### ALWAYS Test URLs Before Deploying
- Test every feature before finishing  
- Check README files before building
- Test the URL works before telling Jay to use it

### Persistent Storage (CRITICAL!)
- Railway wipes data on every deploy
- ALWAYS add persistent volume at /data for databases
- ALWAYS create default admin account (admin/admin1)

## Key Projects (All on GitHub: github.com/Liberty-Emporium)

1. **Contractor Pro AI** - SaaS for contractors, $99/mo with token billing
   - GitHub: github.com/Liberty-Emporium/Contractor-Pro-AI
   
2. **Andy - Keep Your Secrets** - API key management with categories
   - GitHub: github.com/Liberty-Emporium/ai-api-tracker
   
3. **Liberty Inventory** - Thrift store management
   - GitHub: github.com/Liberty-Emporium/Liberty-Emporium-Inventory-App
   
4. **Pet Vet AI** - Pet health diagnosis
   - GitHub: github.com/Liberty-Emporium/pet-vet-ai
   
5. **Andy - Dropship Shipping** - Dropshipping business
   - GitHub: github.com/Liberty-Emporium/Dropship-Shipping
   
6. **Jay Portfolio** - Portfolio site
   - GitHub: github.com/Liberty-Emporium/jay-portfolio

## Pricing

- Liberty Inventory: $299 one-time + $20/mo hosting
- Andy secrets: $9/mo Pro, $40/mo Enterprise
- Contractor Pro AI: $99/mo with token billing

## Admin Credentials

- Username: admin
- Password: admin1

## KiloClaw / OpenClaw Config Notes

- **Telegram bot:** @Jays_Echo_bot (token configured, paired 2026-04-12)
- **Active model:** `openrouter/qwen/qwen3-next-80b-a3b-instruct:free`
  - `qwen/qwen3.6-plus:free` was deprecated on OpenRouter — do NOT use it
  - Replacement: `qwen/qwen3-next-80b-a3b-instruct:free` (80B, better)
- **Hosting:** KiloClaw on Fly.io

---
*Version: 1.1.0 - Updated 2026-04-12*
