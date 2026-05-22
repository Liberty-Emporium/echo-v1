# HyperFrames Skill
> Write HTML. Render video. Built for agents.
> Source: https://github.com/heygen-com/hyperframes | Docs: https://hyperframes.heygen.com

HyperFrames turns HTML files into deterministic MP4 videos using headless Chrome + FFmpeg.
Use this skill whenever you need to create, edit, preview, or render a HyperFrames video composition.

---

## 1. Setup & Requirements

```bash
# Requirements: Node.js >= 22, FFmpeg
node --version   # must be >= 22
ffmpeg -version  # must be installed

# Install CLI globally (or use npx)
npm install -g hyperframes

# Verify environment
npx hyperframes doctor
# Expected: ✓ Node.js v22.x  ✓ FFmpeg 7.x  ✓ Chrome (bundled)
```

---

## 2. CLI Commands — Full Reference

### Create a project
```bash
# Agent mode (non-interactive) — --example is required
npx hyperframes init my-video --example blank
npx hyperframes init my-video --example blank --resolution portrait   # 1080x1920
npx hyperframes init my-video --example blank --resolution square     # 1080x1080
npx hyperframes init my-video --example warm-grain --video video.mp4  # with source video
npx hyperframes init my-video --example blank --tailwind              # add Tailwind CSS
npx hyperframes init my-video --example blank --skip-skills           # skip AI skills install

# Resolution aliases: landscape (1920×1080), portrait (1080×1920),
# square (1080×1080), landscape-4k, portrait-4k, square-4k, 1080p, 4k
```

### Preview (live hot reload)
```bash
cd my-video
npx hyperframes preview           # opens browser Studio with live reload
```

### Lint before rendering
```bash
npx hyperframes lint              # check for structural errors
npx hyperframes lint --json       # machine-readable output
```

### Render to MP4
```bash
npx hyperframes render --output output.mp4
npx hyperframes render --output output.mp4 --fps 24
npx hyperframes render --output output.mp4 --quality high    # draft | standard | high
npx hyperframes render --output output.mp4 --crf 18          # lower = better quality
npx hyperframes render --output output.mp4 --docker          # deterministic (CI/prod)
npx hyperframes render -c compositions/intro.html -o intro.mp4  # specific composition

# Quality presets (H.264 CRF):
#   draft    — CRF 28, fast encode  (dev/preview)
#   standard — CRF 23, balanced     (default)
#   high     — CRF 18, best quality (production)
```

### Other useful commands
```bash
npx hyperframes compositions          # list all compositions in project
npx hyperframes inspect               # check for text overflow / clipped containers
npx hyperframes snapshot              # capture key frames as PNG
npx hyperframes catalog               # browse 50+ ready-to-use blocks
npx hyperframes add flash-through-white   # install a catalog block
npx hyperframes upgrade --check --json    # check for updates
```

---

## 3. Composition HTML Schema

Every composition is an HTML file. The root element declares the canvas size and composition ID.

### Root element (required)
```html
<div id="root" data-composition-id="my-video"
     data-start="0" data-width="1920" data-height="1080">
  <!-- clips go here -->
</div>
```

### Data attributes — complete reference
| Attribute | Required | Description |
|-----------|----------|-------------|
| `id` | Yes | Unique identifier — used for CSS targeting and relative timing |
| `class="clip"` | Yes (img/div) | Enables runtime show/hide. **Omit on `<video>` and `<audio>`** |
| `data-start` | Yes | Start time in seconds (`"0"`, `"5.5"`) OR a clip ID for relative timing (`"intro"`) |
| `data-duration` | Required for `<img>` | Duration in seconds. Optional for video/audio (defaults to source length) |
| `data-track-index` | Yes | Z-order layer. Higher = in front. Clips on same track cannot overlap |
| `data-media-start` | No | Trim start of source video/audio (seconds). Default: `0` |
| `data-volume` | No | Volume 0–1. Default: `1` |
| `data-composition-id` | Yes (on `<div>` compositions) | Must match key in `window.__timelines` |
| `data-composition-src` | No | Path to external composition HTML file |
| `data-variable-values` | No | JSON object of values passed into a nested composition |
| `data-width` / `data-height` | Yes (on compositions) | Canvas dimensions in pixels |

### Clip types

#### Video clip
```html
<video
  id="el-1"
  data-start="0"
  data-duration="15"      <!-- optional — defaults to source duration -->
  data-track-index="0"
  data-media-start="0"    <!-- trim: start 5s into source with "5" -->
  data-volume="1"
  src="./assets/video.mp4"
  muted playsinline
></video>
<!-- ⚠️ Never add class="clip" to <video> — framework manages visibility directly -->
<!-- ⚠️ Never animate width/height/top/left on <video> with GSAP — wrap in <div> first -->
```

#### Image clip
```html
<img
  id="el-2"
  class="clip"             <!-- required on images -->
  data-start="5"
  data-duration="4"        <!-- required on images — no source duration to default to -->
  data-track-index="1"
  src="./assets/logo.png"
/>
```

#### Audio clip
```html
<audio
  id="bg-music"
  data-start="0"
  data-duration="30"
  data-track-index="2"
  data-volume="0.4"        <!-- 40% volume -->
  src="./assets/music.mp3"
></audio>
<!-- ⚠️ Never add class="clip" to <audio> -->
```

#### Nested composition (external file)
```html
<!-- In index.html -->
<div
  id="el-5"
  data-composition-id="intro-anim"
  data-composition-src="compositions/intro-anim.html"
  data-start="0"
  data-track-index="3"
></div>

<!-- In compositions/intro-anim.html — wrap in <template> -->
<template id="intro-anim-template">
  <div data-composition-id="intro-anim" data-width="1920" data-height="1080">
    <div class="title clip" data-start="0" data-duration="5" data-track-index="0">Hello</div>
    <script>
      const tl = gsap.timeline({ paused: true });
      tl.from(".title", { opacity: 0, y: -50, duration: 1 });
      window.__timelines["intro-anim"] = tl;
    </script>
  </div>
</template>
```

#### Composition with variables (reusable templates)
```html
<!-- In index.html — two instances of the same composition with different data -->
<div data-composition-id="card-pro"
     data-composition-src="compositions/card.html"
     data-start="0" data-track-index="1"
     data-variable-values='{"title":"Pro","color":"#ff4d4f"}'></div>

<div data-composition-id="card-enterprise"
     data-composition-src="compositions/card.html"
     data-start="card-pro"    <!-- starts after card-pro ends -->
     data-track-index="1"
     data-variable-values='{"title":"Enterprise","color":"#22c55e"}'></div>

<!-- In compositions/card.html -->
<html data-composition-variables='[
  {"id":"title","type":"string","label":"Title","default":"Fallback"},
  {"id":"color","type":"color","label":"Color","default":"#111827"}
]'>
<body>
  <div data-composition-id="card" data-width="1920" data-height="1080">
    <h1 class="title clip" data-start="0" data-duration="5" data-track-index="0"></h1>
    <script>
      const { title, color } = __hyperframes.getVariables();
      document.querySelector(".title").textContent = title;
      document.querySelector('[data-composition-id="card"]').style.setProperty("--card-color", color);
    </script>
  </div>
</body>
</html>
```

---

## 4. GSAP Animation

HyperFrames uses GSAP for all animations. Timelines must be **paused** — the framework seeks them frame-by-frame.

### Setup pattern (always)
```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
<script>
  // 1. Create paused timeline — NEVER gsap.timeline() without {paused:true}
  const tl = gsap.timeline({ paused: true });

  // 2. Add animations using position param (3rd arg) for absolute timing
  tl.from("#title", { opacity: 0, y: -50, duration: 1 }, 0);      // at t=0
  tl.to("#title",   { opacity: 0, duration: 0.5 },        4.5);   // at t=4.5s
  tl.from("#logo",  { scale: 0, duration: 0.8, ease: "back.out" }, 1.5);

  // 3. Register with composition ID
  window.__timelines = window.__timelines || {};
  window.__timelines["root"] = tl;

  // 4. If video/audio is longer than your last animation, extend the timeline:
  tl.set({}, {}, 30);   // extends to 30 seconds without affecting any elements
</script>
```

### Supported GSAP methods
| Method | Description |
|--------|-------------|
| `tl.to(target, vars, position)` | Animate to values |
| `tl.from(target, vars, position)` | Animate from values |
| `tl.fromTo(target, fromVars, toVars, position)` | Animate from → to |
| `tl.set(target, vars, position)` | Set instantly (no tween) |

### Supported animatable properties
`opacity`, `x`, `y`, `scale`, `scaleX`, `scaleY`, `rotation`, `width`, `height`,
`visibility`, `color`, `backgroundColor`, and any CSS-animatable property.

### ❌ What NOT to do
```javascript
// WRONG: playing media in scripts
document.getElementById("el-video").play();
audio.currentTime = 5;

// WRONG: non-paused timeline
const tl = gsap.timeline();  // missing { paused: true }!

// WRONG: animate dimensions directly on <video>
tl.to("#el-video", { width: 500 }, 5);  // wrap in <div> first

// WRONG: manually nesting sub-timelines
masterTL.add(window.__timelines["intro-anim"], 0);  // framework does this automatically
```

---

## 5. Catalog Blocks (50+ ready-to-use)

Install any block with one command:
```bash
npx hyperframes add <block-name>
```

### Shader transitions (between scenes)
| Block | Effect |
|-------|--------|
| `flash-through-white` | White flash crossfade |
| `cinematic-zoom` | Dramatic zoom blur |
| `chromatic-radial-split` | Chromatic aberration radial split |
| `glitch` | Digital glitch artifacts |
| `light-leak` | Cinematic light leak |
| `ripple-waves` | Concentric ripple distortion |
| `swirl-vortex` | Swirling vortex |
| `domain-warp-dissolve` | Fractal noise dissolve |
| `cross-warp-morph` | Cross-warped morphing |
| `sdf-iris` | Iris reveal |

### Social overlays
| Block | Effect |
|-------|--------|
| `instagram-follow` | Animated IG follow card |
| `tiktok-follow` | TikTok follow overlay |
| `reddit-post` | Reddit post card |
| `spotify-card` | Spotify now-playing card |
| `macos-notification` | macOS notification banner |

### UI / data
| Block | Effect |
|-------|--------|
| `data-chart` | Animated bar + line chart |
| `flowchart` | Animated decision tree |
| `logo-outro` | Cinematic logo reveal with glow |
| `app-showcase` | Floating smartphone screens |

---

## 6. Complete Example — Product Ad (1080×1080 square)

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { overflow: hidden; }

    #root { position: relative; width: 1080px; height: 1080px; background: #0d0d0d; }

    #product-img { width: 1080px; height: 1080px; object-fit: cover; position: absolute; }

    #scrim { position: absolute; inset: 0;
             background: linear-gradient(to top, rgba(0,0,0,0.85) 40%, transparent 100%); }

    #store-name { position: absolute; top: 80px; left: 0; right: 0;
                  text-align: center; color: #D4A017; font-family: serif;
                  font-size: 52px; font-weight: bold; opacity: 0; }

    #product-title { position: absolute; bottom: 200px; left: 60px; right: 60px;
                     color: white; font-family: serif; font-size: 64px;
                     font-weight: bold; line-height: 1.2; opacity: 0; }

    #price { position: absolute; bottom: 100px; left: 60px;
             color: #D4A017; font-family: sans-serif; font-size: 72px;
             font-weight: 900; opacity: 0; }

    #cta { position: absolute; bottom: 40px; right: 60px;
           color: rgba(255,255,255,0.8); font-family: sans-serif; font-size: 28px;
           opacity: 0; }
  </style>
</head>
<body>
<div id="root" data-composition-id="product-ad"
     data-start="0" data-width="1080" data-height="1080">

  <!-- Background image -->
  <img id="product-img" class="clip"
       data-start="0" data-duration="15" data-track-index="0"
       src="./assets/product.jpg" />

  <!-- Dark scrim overlay -->
  <div id="scrim" class="clip"
       data-start="0" data-duration="15" data-track-index="1"
       style="opacity:0;"></div>

  <!-- Store name (top) -->
  <div id="store-name" class="clip"
       data-start="0" data-duration="15" data-track-index="2">
    Liberty Emporium & Thrift
  </div>

  <!-- Product title -->
  <div id="product-title" class="clip"
       data-start="1" data-duration="13" data-track-index="2">
    Vintage Oak Chair
  </div>

  <!-- Price -->
  <div id="price" class="clip"
       data-start="2.5" data-duration="11.5" data-track-index="2">
    $24.99
  </div>

  <!-- CTA -->
  <div id="cta" class="clip"
       data-start="4" data-duration="10" data-track-index="2">
    liberty-emporium-thrift.alexanderai.site
  </div>

  <!-- Background music -->
  <audio id="music" data-start="0" data-duration="15"
         data-track-index="3" data-volume="0.15"
         src="./assets/music.mp3"></audio>

  <script>
    const tl = gsap.timeline({ paused: true });

    // Scrim fades in
    tl.to("#scrim",        { opacity: 1, duration: 1.5 },          0);
    // Store name slides down from top
    tl.fromTo("#store-name", { opacity: 0, y: -30 }, { opacity: 1, y: 0, duration: 0.8 }, 0.3);
    // Product title slides up
    tl.fromTo("#product-title", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.9, ease: "power2.out" }, 1.0);
    // Price pops in
    tl.fromTo("#price",    { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.6, ease: "back.out(1.7)" }, 2.5);
    // CTA fades in
    tl.to("#cta",          { opacity: 1, duration: 0.8 },           4.0);
    // Everything fades out at end
    tl.to(["#product-title","#price","#cta"], { opacity: 0, duration: 1 }, 13.5);

    // Extend timeline to match 15s duration
    tl.set({}, {}, 15);

    window.__timelines = window.__timelines || {};
    window.__timelines["product-ad"] = tl;
  </script>
</div>
</body>
</html>
```

Render it:
```bash
npx hyperframes render --output product-ad.mp4 --fps 24 --quality standard
```

---

## 7. Project Structure (recommended)
```
my-video/
  index.html               ← root composition
  compositions/
    intro.html             ← reusable nested compositions
    outro.html
    lower-third.html
  assets/
    product.jpg            ← images, videos, audio
    music.mp3
    logo.png
  renders/
    output.mp4             ← render output (auto-created)
```

---

## 8. Rendering Pipeline — How It Works

1. **Puppeteer** loads `index.html` in headless Chrome
2. Framework seeks GSAP timelines to `frame / fps` seconds per frame
3. Chrome's `beginFrame` API captures each frame as a screenshot
4. Frames pipe directly to **FFmpeg** (image2pipe → libx264)
5. Audio is mixed in separately by FFmpeg at the end

This is seek-driven and deterministic — same HTML always produces identical output.

---

## 9. Integration With Emporium-and-Thrift-App (Future V2)

When migrating the Flask video generator to HyperFrames:

1. Flask generates an `index.html` from a Jinja template with product data injected as variables
2. Flask calls `npx hyperframes render --output <path> --non-interactive` in a subprocess
3. The rendered MP4 is served as before from `/ads/<filename>`

Benefits over current PIL pipeline:
- CSS animations look much better than PIL text rendering
- Real fonts, gradients, drop shadows, border-radius — full browser CSS
- GSAP easing is smoother than manual ease functions
- Catalog blocks (logo outro, social overlays) usable out of the box
- No per-frame PIL image processing — Chrome renders the whole frame natively

Caveat: Railway deployment needs `node >= 22` added to `nixpacks.toml`:
```toml
[phases.setup]
nixPkgs = ["ffmpeg", "nodejs_22"]
```

---

## 10. Common Mistakes & Fixes

| Mistake | Fix |
|---------|-----|
| Video cuts off early | Timeline too short — add `tl.set({}, {}, <total_seconds>)` |
| Animation out of sync | Missing `{ paused: true }` on timeline |
| Black frames in video | GSAP animating `<video>` directly — wrap in `<div>` |
| Sub-composition not showing | Missing `class="clip"` on overlay divs |
| Media not playing | Calling `.play()` in script — remove it, framework handles it |
| `window.__timelines` key mismatch | Key must exactly match `data-composition-id` |

---

*Skill built from: https://github.com/heygen-com/hyperframes — Apache 2.0*
*Last researched: 2026-05-22 | Version at time of research: v0.6.0-alpha.9*
