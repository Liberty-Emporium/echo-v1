# Emporium & Thrift App Skill
> Everything Echo knows about the Liberty Emporium & Thrift app.

---

## App Overview

- **Repo:** `Liberty-Emporium/Emporium-and-Thrift-App`
- **Live URL:** `https://liberty-emporium-thrift.alexanderai.site`
- **Hosted on:** Railway (Docker)
- **Stack:** Python/Flask + HyperFrames (Node) + Chromium + FFmpeg
- **Main file:** `app_with_ai.py` (~4000 lines)
- **Templates:** `templates/` (Jinja2)
- **Static:** `static/style.css`

---

## Architecture

```
Flask app (gunicorn)
├── Inventory management (CSV-based)
├── AI listing generator (OpenRouter)
├── Image editor + background removal (rembg)
├── Ad generator
│   ├── Image ads (PIL → HTML)
│   └── Video ads (HyperFrames → Chromium → ffmpeg → MP4)
├── TTS voiceover (edge-tts)
├── User auth (users.json, pending_users.json)
└── EcDash bridge (/api/echo-bridge)
```

---

## Video Ad Pipeline

### Flow
1. POST `/generate-video-ad` → returns `job_id` immediately (async)
2. Background thread runs `_generate_video_ad_impl(data)`
3. Frontend polls `/video-ad-status/<job_id>` every 3s
4. Result served from `/ads/<filename>`

### `_generate_video_ad_impl` steps
1. Load product from inventory CSV
2. Generate TTS script via OpenRouter
3. Run `edge_tts` to create voiceover MP3
4. Jinja2-render `templates/hf_ad_composition.html` → `tmpdir/index.html`
5. Copy all product images to `tmpdir/assets/product_0.jpg`, `product_1.jpg`, etc.
6. Run HyperFrames: `node_modules/.bin/hyperframes render --fps 24 --quality standard`
7. Mix audio with ffmpeg if needed
8. Copy output to `ADS_FOLDER`, return result dict

### Image handling (IMPORTANT)
```python
# Get ALL valid images for the product
_raw_imgs = product.get('Images', '').split(',')
valid_images = [fn for fn in _raw_imgs if os.path.exists(os.path.join(UPLOAD_FOLDER, fn))]

# Selected image goes FIRST, others follow — never collapse to just one
if image_file and os.path.exists(os.path.join(UPLOAD_FOLDER, image_file)):
    others = [fn for fn in valid_images if fn != image_file]
    valid_images = [image_file] + others

# Pass ALL to template (up to 5)
_img_assets = [f'./assets/product_{i}.jpg' for i in range(len(valid_images[:5]))]
```

### HyperFrames binary path
```python
HF_BIN = (
    os.path.join(BASE_DIR, 'node_modules', '.bin', 'hyperframes')  # primary
    or '/app/node_modules/.bin/hyperframes'                          # Railway Docker
)
```

---

## hf_ad_composition.html — Template Structure

6 scenes with GSAP animations (all timelines `{ paused: true }`):

| Scene | Time % | Content |
|-------|--------|---------|
| Intro | 0–3.5s | Store name + location, centered |
| Reveal | 3.5–38% | Product title + condition/category, bottom bar |
| Close-up | 38–65% | Condition pill, category pill, price at bottom |
| Price Pop | 65–82% | Big centered price with "Just" label |
| CTA | 82–91% | "Come In Today!" with urgency text |
| Outro | 91–100% | Store name, address, website, QR code |

**Multi-image slideshow:** All images cycle equally, crossfade 0.6s, Ken Burns alternates zoom-in/out.

**NO heavy scrims** — images stay bright. Use:
- Radial vignette for centered scenes (intro, price)
- Bottom gradient bar only for text at bottom (reveal, closeup)
- Left-side gradient for outro (QR stays visible on right)
- `text-shadow` for all text readability

**Supported formats:** `square` (1080×1080), `vertical` (1080×1920), `wide` (1920×1080)

---

## TTS Voices (edge-tts) — Current Valid en-US Voices (2026)

**Dead voices (removed by Microsoft — do NOT use):**
- `en-US-NancyNeural` ❌
- `en-US-DavisNeural` ❌

**Live voices:**
```
en-US-EmmaMultilingualNeural  # DEFAULT — Cheerful, clear
en-US-AriaNeural              # Warm female
en-US-JennyNeural             # Friendly female
en-US-MichelleNeural          # Pleasant female
en-US-AndrewNeural            # Authoritative male
en-US-BrianNeural             # Deep male
en-US-ChristopherNeural       # Reliable male
en-US-GuyNeural               # Confident male
```

**Fallback chain:** Emma → Aria → Jenny

---

## User Authentication

- Admin: `ADMIN_USERNAME` / `ADMIN_PASSWORD` env vars on Railway
- Other users: stored in `users.json` (ephemeral without a volume!)
- Pending requests: `pending_users.json`
- **Direct create route:** `POST /admin/create-user` — admin can create accounts instantly
- **CRITICAL:** Without a Railway Volume, all user accounts reset on every deploy

### Creating accounts that survive deploys
1. Add Railway Volume mounted at `/data`
2. Set env var `DATA_DIR=/data`
3. All JSON files (users, inventory, etc.) will persist across deploys

---

## Mobile Layout Key Points

### base.html hamburger
- Must have visible background + border: `background: rgba(255,255,255,0.15); border: 2px solid rgba(255,255,255,0.6)`
- Use `position: fixed` full-screen overlay for mobile nav (not absolute dropdown)
- Lock body scroll when menu open: `document.body.style.overflow = 'hidden'`
- Mobile dropdowns: show sub-items inline (hover doesn't work on touch)

### ad_generator.html
- `action-row` buttons: `min-width: 0` not `min-width: 220px` (prevents overflow)
- `selection-bar`: flex-direction column on mobile
- `settings-row`: single column on mobile (`grid-template-columns: 1fr`)
- `result-actions`: full-width stacked buttons on mobile

---

## Key File Paths

```
app_with_ai.py              # Main Flask app
templates/
  base.html                 # Global nav/header/footer
  ad_generator.html         # /ads page
  hf_ad_composition.html    # HyperFrames video template
  admin_users.html          # Team management page
static/
  style.css                 # Global styles + mobile breakpoints
Dockerfile                  # Python 3.11 + Node 22 + Chromium + FFmpeg
package.json                # hyperframes dependency
nixpacks.toml               # DELETED — using Dockerfile instead
```

---

## Environment Variables (Railway)

```
ADMIN_USERNAME      admin
ADMIN_PASSWORD      (set securely)
OPENROUTER_API_KEY  (for AI listing + TTS scripts)
DATA_DIR            /data  (requires Volume)
SECRET_KEY          (Flask session key)
STORE_URL           https://liberty-emporium-thrift.alexanderai.site/store
```

---

## Diagnostics

- **`/video-diag`** — health check endpoint (must be logged in): shows ffmpeg, pillow, disk, memory, pipe test
- **Railway logs** — check for `[hf_install]` lines to see if HyperFrames binary was found
- **Syntax check:** `python3 -c "import ast; ast.parse(open('app_with_ai.py').read()); print('OK')"`
