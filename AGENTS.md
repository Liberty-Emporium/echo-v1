# AGENTS.md - Your Workspace & Rules

## Session Startup

Before doing anything else:

1. Read `SOUL.md` — this is who you are
2. Read `USER.md` — this is who you're helping  
3. Read `MEMORY.md` — your long-term memory
4. Read `memory/YYYY-MM-DD.md` for recent context

## Testing Before Deploy (IMPORTANT!)

**ALWAYS test URLs before telling the user to use them:**

1. After pushing code, test the URL with curl or web_fetch
2. Verify the page loads correctly
3. Only tell the user to try it after YOU confirm it works

## Railway App URLs

- ai-api-tracker: https://ai-api-tracker-production.up.railway.app
- contractor-pro-ai: https://contractor-pro-ai-production.up.railway.app
- pet-vet-ai: https://pet-vet-ai-production.up.railway.app
- liberty-inventory: https://liberty-emporium-and-thrift-inventory-app-production.up.railway.app

## Persistent Storage (CRITICAL!)

- Railway wipes data on every deploy
- ALWAYS add persistent volume at /data for databases
- ALWAYS create default admin account (admin1/admin1)

---
*Version: 1.0.0*
