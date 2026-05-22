---
name: video-commercial-production
description: Research-backed knowledge for building effective video commercials and short-form ads using Python + ffmpeg + Pillow. Covers commercial structure, scene timing, copywriting formulas, cinematic effects, and the Liberty Emporium thrift app video generator specifically. Use whenever working on video ads, commercials, or the /generate-video-ad route.
---

# Video Commercial Production

## The Science of What Works

### The 5-Act Structure (research-backed, 2026)
Every high-performing video ad follows this structure regardless of length:

| Act | Timing (30s spot) | Job |
|-----|------------------|-----|
| **Hook** | 0–3s | Stop the scroll. Pattern interrupt. Visual novelty or bold statement. |
| **Context** | 3–7s | What is this? Who is it for? Earn the next 20 seconds. |
| **Demo / Reveal** | 7–22s | Product in its best light. Proof of value. The "wow" moment. |
| **Social proof / USP** | 22–27s | Why this store/item over everything else? |
| **CTA** | 27–30s | One clear action. Address, website, price, visit. |

**Key stat:** 73% of video ads fail in the first 3 seconds. 90% of ad recall happens in the first 6 seconds.

### Hook-Body-CTA (the short version for 15s ads)
- **Hook (0–3s):** Bold visual + one surprising/emotional line
- **Body (3–12s):** Product + price + one reason to care
- **CTA (12–15s):** Store name + location + one action

### What Makes Local TV Commercials Work
1. **USP first** — One sentence that answers "why this store?" — Liberty Emporium's USP: *unique finds, thrift prices, Liberty NC*
2. **Warm and conversational** — Not corporate. Real people talk. "Come on in."
3. **Price is the hero** — For thrift/retail, the price IS the product. Make it massive.
4. **Scarcity** — "One of a kind." "While it lasts." Thrift inventory is inherently scarce — use it.
5. **Sense of place** — Liberty, North Carolina. Local identity builds trust.
6. **Emotion > features** — "The perfect gift" beats "good condition dresser."

### Salvation Army Thrift Case Study (2026 One Show Finalist)
- Advertised **sold** items to create FOMO → drove foot traffic
- AI-styled inventory photos into editorial fashion images → 1.6% CTR (2.6x above benchmark)
- $11 cost per store visit (138% below Google Display Network average)
- **Lesson for Liberty Emporium:** Show the treasure, create urgency, lean into uniqueness

---

## Commercial Script Formula (for AI prompt)

### 15-second voiceover (45–55 words)
```
[Hook — name the item emotionally, 1 sentence]
[Context — condition + what makes it special, 1 sentence]  
[Price reveal — "Just $X"]
[Scarcity CTA — "One of a kind. Come find it at Liberty Emporium & Thrift, Liberty NC."]
```

### 30-second voiceover (80–100 words)
```
[Hook — open with "Imagine..." or "Looking for..." or the item name boldly]
[Problem/desire — 1 sentence about why someone wants this]
[Product reveal — what it is, condition, what you can do with it]
[Price + value comparison — "At just $X, that's [comparison]"]
[Scarcity — "One of a kind. Won't last long."]
[CTA — "Liberty Emporium & Thrift. 125 W Swannanoa Ave, Liberty NC. Come see us today."]
```

### OpenRouter prompt for video scripts
```python
prompt = (
    'Write a 12-second local TV commercial voiceover for a thrift store item. '
    'Sound warm, human, and conversational — like a real local commercial, not a robot. '
    'Open with a hook that names the item emotionally. Include the price. '
    'Create urgency with scarcity. End with the store name and city. '
    'NO stage directions. NO quotes. ONLY the words to be spoken. '
    '45-55 words maximum.\n\n'
    f'Item: {title}\nCondition: {condition}\nPrice: ${price}\n'
    f'Description: {description[:200]}\n'
    f'Store: Liberty Emporium & Thrift, Liberty NC\n'
)
```

---

## Scene Timing (current Liberty Emporium video)

```
INTRO_END    = VIDEO_SECS * 0.10   # Scene 1: Store splash    (0–10%)
PRODUCT_END  = VIDEO_SECS * 0.72   # Scene 2: Product shot    (10–72%)
PRICE_END    = VIDEO_SECS * 0.86   # Scene 3: Price reveal    (72–86%)
                                    # Scene 4: Outro/CTA       (86–100%)
```

### Recommended timing adjustments by style

| Style | Hook | Product | Price | CTA |
|-------|------|---------|-------|-----|
| **Urgency** (flash sale) | 5% | 60% | 25% | 10% |
| **Storytelling** (premium item) | 15% | 60% | 15% | 10% |
| **Price-first** (bargain hunter) | 8% | 50% | 30% | 12% |
| **Current default** | 10% | 62% | 14% | 14% |

---

## Python + Pillow Frame Rendering — Best Practices

### Font sizing for legibility (1080×1080)
```python
font_huge  = ImageFont.truetype(font_path, 140)  # Store name splash
font_bold  = ImageFont.truetype(font_path, 96)   # Product title
font_price = ImageFont.truetype(font_path, 148)  # Price — make it the biggest thing
font_store = ImageFont.truetype(font_path, 64)   # Taglines, CTAs
font_body  = ImageFont.truetype(font_path, 58)   # Descriptions
font_small = ImageFont.truetype(font_path, 46)   # Details, secondary info
```
**Rule:** Price should be the largest element on screen. Title second. Everything else much smaller.

### Easing functions for smooth motion
```python
def ease_out(t):
    return 1 - (1 - t) ** 3   # Fast in, slow out — natural deceleration

def ease_in(t):
    return t ** 3              # Slow in, fast out — for exits/fades

def ease_in_out(t):
    return t * t * (3 - 2*t)  # Smooth both ends — for loops/pulses
```

### Text wrapping for long product names
```python
def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines, current = [], []
    for word in words:
        test = ' '.join(current + [word])
        bbox = draw.textbbox((0,0), test, font=font)
        if bbox[2] - bbox[0] > max_width and current:
            lines.append(' '.join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append(' '.join(current))
    return lines
```

### Drop shadow for legibility on any background
```python
def shadow_text(draw, pos, text, font, fill, shadow_offset=4, shadow_alpha=180):
    sx, sy = pos[0] + shadow_offset, pos[1] + shadow_offset
    draw.text((sx, sy), text, font=font,
              fill=(0, 0, 0, shadow_alpha), anchor='mm')
    draw.text(pos, text, font=font, fill=fill, anchor='mm')
```

### Vignette overlay (darkens edges, focuses center)
```python
def vignette(img, strength=200):
    W, H = img.size
    vig = Image.new('RGBA', (W, H), (0,0,0,0))
    d = ImageDraw.Draw(vig)
    for i in range(strength):
        a = int((i / strength) ** 2 * 200)
        margin = i * 2
        d.rectangle([margin, margin, W-margin, H-margin],
                    outline=(0,0,0,a))
    return Image.alpha_composite(img.convert('RGBA'), vig)
```

---

## ffmpeg — Cinematic Encoding

### Current production command (optimized for Railway)
```bash
ffmpeg -y
  -framerate 10 -i frame_%04d.png      # 10fps source (fast render)
  -i voiceover.mp3
  -i music.mp3
  -filter_complex
    '[0:v]minterpolate=fps=30:mi_mode=blend[v];    # interpolate to smooth 30fps
     [1:a]volume=1.0[vo];
     [2:a]volume=0.12[bg];
     [vo][bg]amix=inputs=2:duration=first[aout]'
  -map [v] -map [aout]
  -c:v libx264 -preset ultrafast -crf 23
  -pix_fmt yuv420p -c:a aac -b:a 128k
  -shortest output.mp4
```

**Why 10fps source + minterpolate:** Generating 390 frames (30fps × 13s) in Python kills the gunicorn worker. 130 frames is 3x faster. ffmpeg's `minterpolate=mi_mode=blend` blends between frames for smooth 30fps output.

### Ken Burns zoom-pan (ffmpeg native — NO Python frames needed)
For a pure image → video with zoom effect (much faster, no Pillow loop):
```bash
ffmpeg -loop 1 -i product.jpg -t 10
  -vf "zoompan=z='min(zoom+0.0015,1.5)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=300:s=1080x1080:fps=30"
  -c:v libx264 -preset ultrafast -crf 23 -pix_fmt yuv420p
  zoom_output.mp4
```
- `z='min(zoom+0.0015,1.5)'` — slow zoom in from 1.0x to 1.5x
- `d=300` — 300 frames = 10 seconds at 30fps
- Avoids all Python frame generation — ffmpeg does everything natively

### Burn text onto video with ffmpeg drawtext
```bash
-vf "drawtext=text='${PRICE}':fontsize=120:fontcolor=gold:x=(w-tw)/2:y=(h-th)/2:shadowcolor=black:shadowx=4:shadowy=4"
```

### Better architecture (future): pure ffmpeg pipeline
Instead of Python drawing frames → ffmpeg, use ffmpeg for everything:
1. `zoompan` on product image → base video
2. `overlay` text layers with `drawtext`  
3. `fade` transitions between scenes with `fade=t=in:st=0:d=0.5`
4. Concat scenes with `concat` filter
5. Mix audio tracks
→ **Eliminates Python frame loop entirely. 10x faster. No worker timeout.**

---

## TTS Voice Options (edge-tts)

| Voice | Style | Best for |
|-------|-------|---------|
| `en-US-AriaNeural` | Warm, friendly female | Default — Liberty Emporium ✅ |
| `en-US-GuyNeural` | Confident male | Price-focused urgency ads |
| `en-US-JennyNeural` | Conversational female | Storytelling/lifestyle items |
| `en-US-DavisNeural` | Deep male | Furniture, tools, masculine items |
| `en-US-NancyNeural` | Warm older female | Collectibles, antiques, nostalgic |

Rate adjustments:
- `-5%` — slightly slower, clearer (current)
- `-10%` — TV announcer pace, deliberate
- `+5%` — energetic, deal-hunter vibe

---

## Ideas for Future Video Styles

### 1. "Before & After" (for furniture/tools)
- Scene 1: Item on plain background
- Scene 2: Item styled in a room (AI background replacement with rembg)
- Scene 3: Price + CTA

### 2. "Treasure Hunt" (thrift-specific)
- Open: "Someone's treasure is waiting for you..."
- Flash multiple items quickly (0.5s each)
- Land on the featured item with dramatic zoom
- Price + "One of a kind"

### 3. "Facebook Reel" format (9:16 vertical, 15s)
- Vertical 1080×1920 instead of square
- Hook text burned at top (large)
- Item fills center frame
- Price at bottom
- Swipe/tap CTA

### 4. "Scarcity Timer"
- Small countdown overlay: "Only 1 left"
- Pulses red every 2 seconds
- Creates FOMO

### 5. Multi-item "Haul" video
- 3–5 items, 4s each
- Same music/template throughout
- Good for weekly inventory highlights

---

## Common Bugs & Fixes (Liberty Emporium App)

| Bug | Cause | Fix |
|-----|-------|-----|
| `Server error 500` on video gen | gunicorn worker timeout (30s default) | `--timeout 300` in Procfile |
| `JSON.parse: unexpected character` | fetch() gets HTML redirect instead of JSON | Guard: `if (r.redirected) window.location.href='/login'` |
| Video generates but no AI script | `OPENROUTER_API_KEY` not set in Railway | Set env var, falls back to template script |
| Video blurry/pixelated | `crf` too high, low resolution source | Use `crf 20` for quality, ensure 1080px source |
| Audio out of sync | Generated at wrong sample rate | edge-tts output is always 24kHz/128k — ffmpeg handles it fine |
| Music too loud | Default volume | Background music: `volume=0.12` (12%), voiceover: `volume=1.0` |

---

## Checklist Before Shipping a New Video Feature

- [ ] Syntax check: `python3 -m py_compile app_with_ai.py`
- [ ] Guard all `fetch()` calls against session redirect
- [ ] Gunicorn timeout ≥ 300s in Procfile
- [ ] Test with real SKU + real image via curl
- [ ] Verify ffmpeg available: `imageio_ffmpeg.get_ffmpeg_exe()`
- [ ] Check Railway env vars: `OPENROUTER_API_KEY` set
- [ ] Push to GitHub → Railway auto-deploys
