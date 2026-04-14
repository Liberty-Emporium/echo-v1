# AGENTS.md - Your Workspace & Rules

## Session Startup

Before doing anything else:
1. Read `SOUL.md` — this is who you are
2. Read `USER.md` — this is who you're helping
3. Read `MEMORY.md` — your long-term memory
4. Read `memory/YYYY-MM-DD.md` for recent context

## Automation (CRITICAL)

**exec.ask must always be "off".** If command approval prompts appear:
1. Run `gateway restart` via the gateway tool immediately
2. Do NOT keep asking Jay to approve commands
3. The config already has `tools.exec.ask: "off"` — a restart fixes it

## Testing Before Deploy (IMPORTANT!)

**ALWAYS test URLs before telling the user to use them:**
1. After pushing code, test with curl or web_fetch
2. Verify the page loads correctly
3. Only tell the user to try it after YOU confirm it works

## Railway Deployment Rules

- Railway wipes ALL static files on every deploy
- NEVER reference `/static/uploads/` for images — embed as base64 inline or use external CDN
- ALWAYS add persistent volume at /data for SQLite databases
- ALWAYS create default admin account (admin/admin1)
- **Branch:** jay-portfolio uses `master` NOT `main` — check with `git branch` before pushing

## GitHub Token Handling

- Always read from `/root/.secrets/github_token`
- Tokens are rotated by Jay after each session
- If a push returns 404/401: ask Jay for a fresh token immediately
- Set remote URL: `git remote set-url origin https://$(cat /root/.secrets/github_token)@github.com/Liberty-Emporium/<repo>.git`

## Image Handling for Railway Apps

- Scanned PDFs / images: use `pdftoppm` (install via `apt-get install -y poppler-utils`)
- Embed thumbnails as base64 data URIs — never as file paths
- QR codes: use `python3-qrcode` + `python3-pil` (install via apt-get, not pip)

## PDF Handling

- Download from Google Drive: `curl -L "https://drive.google.com/uc?export=download&id=FILE_ID" -o file.pdf`
- Extract pages as images: `pdftoppm -r 150 -f 1 -l 1 -png file.pdf /tmp/output`
- Text extraction (if not scanned): `pdftotext file.pdf output.txt`
- Scanned PDFs will have 0 words — read the extracted PNG images directly

## Railway App URLs
- ai-api-tracker: https://ai-api-tracker-production.up.railway.app
- contractor-pro-ai: https://contractor-pro-ai-production.up.railway.app
- pet-vet-ai: https://pet-vet-ai-production.up.railway.app
- liberty-inventory: https://liberty-emporium-and-thrift-inventory-app-production.up.railway.app
- liberty-demo: https://liberty-emporium-inventory-demo-app-production.up.railway.app
- jay-portfolio: https://jay-portfolio-production.up.railway.app
- dropship-shipping: https://dropship-shipping-production.up.railway.app
- consignment-solutions: https://web-production-43ce4.up.railway.app

## Persistent Storage (CRITICAL!)
- Railway wipes data on every deploy
- ALWAYS add persistent volume at /data for SQLite databases
- ALWAYS create default admin account (admin/admin1)

---
*Version: 1.1.0 - Updated 2026-04-13*
