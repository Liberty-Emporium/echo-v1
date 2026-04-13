# SKILLS.md - Echo's Skills System

This is **the most important file** for Echo's long-term growth and memory.

## The Skills Philosophy

**Echo can create skills, store them on GitHub, and use them forever.**

When Echo creates a skill:
1. Build the skill with Python files, scripts, documentation
2. Store it in `skills/custom/` on GitHub
3. Document it in this file
4. Use it anytime in the future

## Default Skills (from OpenClaw/KiloClaw)

See the KiloClaw skill registry for the full list of built-in skills.

## Custom Skills — Stored in `skills/custom/`

### Session Skills (Built 2026-04-11 to 2026-04-13)
See `skills/custom/README.md` for full descriptions.

Key skills available:
- `app-auditor` — Audit a Flask app for bugs, security issues, missing features
- `security-scan` — Scan code for secrets, SQL injection, auth flaws
- `security-shield` — Harden an app against common attack vectors
- `testing-django` / `testing-e2e` / `testing-api` — Test strategy generators
- `smoke-test` — Quick functional smoke test for a deployed URL
- `internet-researcher` — Deep research on any topic
- `legacy-whisper` — Understand and document legacy codebases
- `refactor-sense` — Identify and plan code refactors
- `visual-audit` — Screenshot + visual review of a deployed UI
- `route-audit` — Map all Flask/Django routes and check for issues
- `github-integration` — GitHub operations: push, PR, branch, commit
- `mentor-mode` — Explain code concepts to learners

### Skills Needed (Identified 2026-04-13)

Based on today's session, these skills would have made the work faster and better:

#### `pdf-extractor` (HIGH PRIORITY)
**What it does:** Downloads a PDF from any URL (Google Drive, Dropbox, direct), extracts specific pages as images, extracts text if available, returns base64 images ready for embedding.
**Why needed:** Today I had to manually: download PDF with curl, install poppler-utils, run pdftoppm, then manually base64 encode. A skill would do this in one step.
**Script:** `scripts/extract_pdf.py --url URL --pages 1-5 --output-format base64_png`

#### `railway-deploy` (HIGH PRIORITY)
**What it does:** Given a repo path, handles the full Railway deploy cycle: check current deployment status, push to correct branch (master vs main), wait for deploy, verify the URL is live, return confirmation.
**Why needed:** Today I had to: figure out the branch was `master` not `main`, push, wait, manually curl to verify. A skill wraps all of this.
**Script:** `scripts/railway_deploy.py --repo PATH --url URL --branch master`

#### `base64-image` (MEDIUM)
**What it does:** Takes any image file path or URL, converts to base64 data URI, ready to drop into HTML.
**Why needed:** Used this pattern twice today (thumbnail + QR code). Should be one command.
**Script:** `scripts/to_base64.py --input FILE_OR_URL --mime image/png`

#### `qr-generator` (MEDIUM)
**What it does:** Generates a QR code for any URL, returns as base64 PNG data URI ready for HTML embedding.
**Why needed:** Today installed python3-qrcode via apt, wrote the generation script inline. Should be a ready-made skill.
**Script:** `scripts/make_qr.py --url URL --size 300 --color "#1a1a2e"`

#### `github-token-refresh` (MEDIUM)
**What it does:** Detects when a GitHub token has expired (404 on API calls), alerts Jay immediately, stores the new token when provided.
**Why needed:** Today spent multiple failed commands before realizing the token was dead.

#### `apt-toolbox` (LOW)
**What it does:** Pre-installs common tools (poppler-utils, ghostscript, imagemagick, ffmpeg, qrcode) at session start so they're always ready.
**Why needed:** Today had to apt-get install mid-task, which delayed work.

## Skills Storage Location

All custom skills stored at:
```
https://github.com/Liberty-Emporium/echo-v1/tree/main/skills/custom/
```

## Echo's Legacy

This skills system allows Echo to:
- Build skills once, use forever
- Share skills with others
- Grow smarter over time
- Be useful 20+ years from now
- Pass knowledge to others Jay cares about

---
*Version: 1.1.0 - Updated 2026-04-13*
