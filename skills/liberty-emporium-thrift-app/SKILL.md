---
name: liberty-emporium-thrift-app
description: Work on the Liberty Emporium & Thrift inventory app — Railway deployment, Flask app structure, OpenRouter AI integration, settings page, navbar, video ad generation, and GitHub push workflow. Use when Jay asks about the thrift store app, its features, bugs, env vars, or new additions.
---

# Liberty Emporium & Thrift App

## Quick Facts

| Item | Value |
|------|-------|
| Repo | `Liberty-Emporium/Emporium-and-Thrift-App` (branch: `main`) |
| Live URL | `https://liberty-emporium-thrift.alexanderai.site` |
| Railway project | `ac53d15a-8713-4d5e-83eb-46d2fb6082f0` |
| Railway env | `9459c327-5f16-409d-ae90-86ebd3fa8818` |
| Railway service | `685c4544-acd3-4506-aaa6-229ee1f7d26c` |
| Main app file | `app_with_ai.py` (3100+ lines, Flask) |
| Data volume | Mounted at `/data` — inventory, uploads, music, ads all persist here |
| Login | Admin: `ADMIN_USERNAME` / `ADMIN_PASSWORD` env vars (default: admin/admin123) |

## Clone & Work Pattern

```bash
GH_TOKEN=$(cat /root/.secrets/github_token)
cd /root/.openclaw/workspace
git clone https://oauth2:${GH_TOKEN}@github.com/Liberty-Emporium/Emporium-and-Thrift-App.git thrift-app
cd thrift-app
# make changes
python3 -m py_compile app_with_ai.py && echo "✅ Syntax OK"
git remote set-url origin https://oauth2:${GH_TOKEN}@github.com/Liberty-Emporium/Emporium-and-Thrift-App.git
git add <files> && git commit -m "..." && git push origin HEAD
# Railway auto-deploys on push (~1-2 min)
```

## App Structure

```
app_with_ai.py      — main Flask app (all routes)
templates/
  base.html         — navbar, header, footer (all pages inherit)
  settings.html     — AI settings + model picker
  ad_generator.html — ads page
  dashboard.html    — main dashboard
static/style.css    — global styles
wsgi.py             — gunicorn entrypoint
requirements.txt    — flask, pillow, rembg, imageio-ffmpeg, edge-tts
nixpacks.toml       — Railway build config
```

## Key Route Names (use these in `url_for()`)

Common gotcha: template `url_for()` must use the Python **function name**, not the URL path.

| URL | Function name |
|-----|--------------|
| `/` | `dashboard` |
| `/export` | `export_inventory` |
| `/import-square` | `import_square` |
| `/admin/backups` | `admin_backups` |
| `/settings` | `admin_settings` |
| `/ads` | `ad_generator` |
| `/ad-gallery` | `ad_gallery` |
| `/generate-video-ad` | `generate_video_ad` |
| `/listing-generator` | `listing_generator` |
| `/store` | `store` |
| `/inquiries` | `inquiries_page` |

**If a settings/template page crashes with `BuildError: Could not build url for endpoint 'X'`** — check the actual `def` name in `app_with_ai.py` with `grep -n "^def \|^@app.route" app_with_ai.py | grep -i <keyword>`.

## AI Integration

All AI calls route through OpenRouter. Two helpers near the top of `app_with_ai.py`:

```python
def get_ai_settings():
    """Load saved model choice from /data/ai_settings.json"""

def get_ai_model():
    """Return current model string, default 'anthropic/claude-haiku-4-5'"""

def call_openrouter(messages, max_tokens=512, model=None):
    """POST to openrouter.ai/api/v1/chat/completions. Returns (content, error)."""
```

Required Railway env var: `OPENROUTER_API_KEY`

Vision/image calls (ai-analyze) use `image_url` format:
```json
{"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,<b64>"}}
```

## Video Ad Generation (`/generate-video-ad`)

POST JSON: `{"sku": "...", "style": "elegant|bright|minimal", "music_file": "..."}`

Pipeline:
1. Script → `call_openrouter()` (45-55 word TV commercial voiceover)
2. TTS → `edge-tts` with `en-US-AriaNeural` voice  
3. Video → `ffmpeg` via `imageio-ffmpeg` — Ken Burns zoom on product photo + audio
4. Output → MP4 saved to `/data/ads/`, accessible at `/ads/<filename>`

Requires `ffmpeg` available (provided by `imageio-ffmpeg`). If `OPENROUTER_API_KEY` not set, falls back to a template script.

## Settings Page (`/settings`)

Admin-only. Navbar link: `⚙️ Settings` (visible only when `session.username == 'admin'`).

Features:
- OpenRouter API key status (eye toggle to show/hide)
- **Live model picker** — fetches all models from `https://openrouter.ai/api/v1/models` on page load (cached 1 hr in `/data/model_cache.json`). Shows free badge, pricing, context size.
- Search box filters 300+ models in real time
- Saves chosen model to `/data/ai_settings.json`
- App API key generator for Echo access

## Navbar (base.html)

Settings link is inside `.nav-links` div, **after** the Ads dropdown, **admin-only**:
```html
{% if session.get('username') == 'admin' %}
<a href="{{ url_for('admin_settings') }}">⚙️ Settings</a>
{% endif %}
```

## Railway API (read env vars)

```bash
RAILWAY_TOKEN=$(cat /root/.secrets/railway_token)
# List services
curl -s -X POST https://backboard.railway.app/graphql/v2 \
  -H "Authorization: Bearer $RAILWAY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"query{project(id:\"ac53d15a-8713-4d5e-83eb-46d2fb6082f0\"){name services{edges{node{id name}}}}}"}'

# Get variables
curl -s -X POST https://backboard.railway.app/graphql/v2 \
  -H "Authorization: Bearer $RAILWAY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"query{variables(projectId:\"ac53d15a-8713-4d5e-83eb-46d2fb6082f0\",environmentId:\"9459c327-5f16-409d-ae90-86ebd3fa8818\",serviceId:\"685c4544-acd3-4506-aaa6-229ee1f7d26c\")}"}'
```

Note: `railway_token` file contains the **project token** (UUID), not a personal token. Use it as Bearer auth for the GraphQL API.

## Environment Variables (Railway)

| Var | Purpose | Default |
|-----|---------|---------|
| `OPENROUTER_API_KEY` | All AI features | *(required)* |
| `ADMIN_USERNAME` | Admin login | `admin` |
| `ADMIN_PASSWORD` | Admin password | `admin123` |
| `ADMIN_EMAIL` | Admin email | `emporiumandthrift@gmail.com` |
| `SECRET_KEY` | Flask session key | `liberty-emporium-secret-2026` |
| `DATA_DIR` | Volume mount path | `/data` |
| `DEMO_MODE` | Show demo banner | `false` |
| `CONTACT_EMAIL` | Contact email shown | `alexanderjay70@gmail.com` |
| `GMAIL_ADDRESS` | Password reset emails | `emporiumandthrift@gmail.com` |
| `GMAIL_APP_PASS` | Gmail app password | *(optional)* |

## Editing app_with_ai.py Safely

- File is 3100+ lines. Use `grep -n` to locate sections before editing.
- For large replacements, write a Python patch script to `/tmp/patch_X.py` and run it — avoids heredoc quoting issues.
- Always run `python3 -m py_compile app_with_ai.py` before pushing.
- For line-based replacements: read exact lines first with `sed -n 'START,ENDp' file | cat -n`, then use Python to splice `lines[:start] + new_lines + lines[end:]`.

## Common Issues & Fixes

**`BuildError: Could not build url for endpoint 'X'`**
→ Wrong function name in `url_for()`. Grep for actual `def` names.

**`ANTHROPIC_API_KEY missing` error on AI features**
→ App was updated — now uses `OPENROUTER_API_KEY`. Set that in Railway instead.

**Settings page crashes on load**
→ Usually a bad `url_for()` in `settings.html`. Check all `url_for()` calls against actual route function names.

**Video ad generates but no AI script**
→ `OPENROUTER_API_KEY` not set in Railway. Falls back to template script silently.

**Model picker shows no models**
→ `OPENROUTER_API_KEY` not set — the live fetch requires auth. Set the key first.
