# SKILL: video-slideshow
**How to build image slideshows into videos using Python + ffmpeg**
_Researched and written by Echo — 2026-05-22_

---

## Core Concept

A video slideshow is built from individual image clips that are stitched together with transition effects. There are two solid approaches:

1. **Frame-rendering (PIL)** — render every frame yourself, write JPEGs, encode with ffmpeg. Full control, slower.
2. **ffmpeg xfade filter** — let ffmpeg do all the work via a filter graph. Much faster, fewer files, less disk I/O.

For the Emporium-and-Thrift-App ad generator, **approach 2 is better** because:
- We already have product images as files on disk
- We want snappy Ken Burns motion on each slide
- xfade handles transitions natively with zero extra code

---

## Approach 2: ffmpeg xfade (recommended)

### The offset formula (critical — this is the gotcha)

```
offset_N = N * (clip_duration - fade_duration)
```

Example: 4s clips, 1s fade → offsets are 3, 6, 9, 12…

For N images with clip_dur and fade_dur:
```python
offsets = [i * (clip_dur - fade_dur) for i in range(1, len(images))]
total_duration = len(images) * clip_dur - (len(images) - 1) * fade_dur
```

### xfade filter graph for N images

For 2 images:
```
[0:v][1:v]xfade=transition=fade:duration=1:offset=3[v]
```

For 3 images:
```
[0:v][1:v]xfade=transition=fade:duration=1:offset=3[out1];
[out1][2:v]xfade=transition=fade:duration=1:offset=6[v]
```

For N images (Python builder):
```python
def build_xfade_filter(n_images, clip_dur=4.0, fade_dur=0.8, transitions=None):
    """
    Returns (filter_string, final_label, total_seconds).
    transitions: list of xfade transition names, or None for random variety.
    """
    import random
    NICE_TRANSITIONS = [
        'fade', 'fadeblack', 'fadewhite',
        'wipeleft', 'wiperight', 'wipeup', 'wipedown',
        'slideleft', 'slideright', 'slideup', 'slidedown',
        'smoothleft', 'smoothright',
        'circlecrop', 'circleopen', 'circleclose',
        'pixelize', 'dissolve', 'radial',
    ]
    parts = []
    prev = '[0:v]'
    for i in range(1, n_images):
        trans = (transitions[i-1] if transitions and i-1 < len(transitions)
                 else random.choice(NICE_TRANSITIONS))
        offset = round(i * (clip_dur - fade_dur), 3)
        label  = f'[xf{i}]' if i < n_images - 1 else '[vout]'
        parts.append(f'{prev}[{i}:v]xfade=transition={trans}:duration={fade_dur}:offset={offset}{label}')
        prev = label
    total = n_images * clip_dur - (n_images - 1) * fade_dur
    return '; '.join(parts), '[vout]', round(total, 3)
```

### ffmpeg command for N images with xfade

```python
def build_slideshow_cmd(images, clip_dur, fade_dur, output_path, ffmpeg_bin,
                        audio_path=None, fps=30, transitions=None):
    """
    images: list of file paths (all must be same resolution for xfade)
    Returns: subprocess command list
    """
    filter_str, final_label, total = build_xfade_filter(
        len(images), clip_dur, fade_dur, transitions)

    cmd = [ffmpeg_bin, '-y']
    for img in images:
        cmd += ['-loop', '1', '-framerate', str(fps), '-t', str(clip_dur), '-i', img]

    if audio_path:
        cmd += ['-i', audio_path]

    cmd += ['-filter_complex', filter_str,
            '-map', final_label]

    if audio_path:
        cmd += ['-map', f'{len(images)}:a']

    cmd += ['-c:v', 'libx264', '-preset', 'fast', '-crf', '22',
            '-pix_fmt', 'yuv420p', '-shortest', output_path]
    return cmd
```

⚠️ **xfade requires all inputs to be the same resolution.** Pre-resize with PIL first.

---

## Adding Ken Burns (zoom/pan) to each slide

xfade handles transitions *between* slides. Ken Burns motion *within* a slide is a separate layer.
Best approach: pre-render each slide as a short MP4 clip with PIL (zoom+pan), then chain those clips through xfade.

```python
def render_slide_clip(img_path, out_path, ffmpeg_bin, W, H, dur=4.0, fps=30,
                      motion='zoom_in', blur=0, darken=1.0):
    """
    Renders a single image as a Ken Burns motion clip.
    motion: 'zoom_in' | 'zoom_out' | 'pan_left' | 'pan_right' | 'pan_up'
    """
    import tempfile, os, subprocess
    from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps

    def _eo(t): return 1 - (1 - max(0.0, min(1.0, t))) ** 3  # ease-out cubic

    pi = Image.open(img_path)
    pi = ImageOps.exif_transpose(pi).convert('RGB')
    # Scale-to-fill at 2x canvas
    scale = max(W*2/pi.width, H*2/pi.height)
    nw, nh = int(pi.width*scale), int(pi.height*scale)
    pi = pi.resize((nw, nh), Image.LANCZOS)
    cx0 = (nw - W*2) // 2; cy0 = (nh - H*2) // 2
    src = pi.crop((cx0, cy0, cx0+W*2, cy0+H*2))  # 2x canvas
    src = ImageEnhance.Contrast(src).enhance(1.12)
    src = ImageEnhance.Color(src).enhance(1.08)

    tmpdir = tempfile.mkdtemp()
    nf = int(dur * fps)
    for fi in range(nf):
        p = _eo(fi / max(1, nf-1))
        if motion == 'zoom_in':
            zoom = 1.0 + 0.40 * p
        elif motion == 'zoom_out':
            zoom = 1.40 - 0.40 * p
        elif motion == 'pan_left':
            zoom = 1.40; cw = int(W*2/zoom)
            max_cx = W*2 - cw; cx = int(max_cx*(1.0-p)); cy = (H*2-int(H*2/zoom))//2
            crop = src.crop((cx, cy, cx+cw, cy+int(H*2/zoom))).resize((W, H), Image.LANCZOS)
            if blur: crop = crop.filter(ImageFilter.GaussianBlur(blur))
            if darken < 1.0: crop = ImageEnhance.Brightness(crop).enhance(darken)
            crop.save(os.path.join(tmpdir, f'{fi:05d}.jpg'), quality=88)
            continue
        elif motion == 'pan_right':
            zoom = 1.40; cw = int(W*2/zoom)
            max_cx = W*2 - cw; cx = int(max_cx*p); cy = (H*2-int(H*2/zoom))//2
            crop = src.crop((cx, cy, cx+cw, cy+int(H*2/zoom))).resize((W, H), Image.LANCZOS)
            if blur: crop = crop.filter(ImageFilter.GaussianBlur(blur))
            if darken < 1.0: crop = ImageEnhance.Brightness(crop).enhance(darken)
            crop.save(os.path.join(tmpdir, f'{fi:05d}.jpg'), quality=88)
            continue
        else:
            zoom = 1.0
        cw = int(W*2/zoom); ch = int(H*2/zoom)
        cx = (W*2-cw)//2; cy = (H*2-ch)//2
        crop = src.crop((cx, cy, cx+cw, cy+ch)).resize((W, H), Image.LANCZOS)
        if blur:  crop = crop.filter(ImageFilter.GaussianBlur(blur))
        if darken < 1.0: crop = ImageEnhance.Brightness(crop).enhance(darken)
        crop.save(os.path.join(tmpdir, f'{fi:05d}.jpg'), quality=88)

    r = subprocess.run([
        ffmpeg_bin, '-y', '-framerate', str(fps),
        '-i', os.path.join(tmpdir, '%05d.jpg'),
        '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '20',
        '-pix_fmt', 'yuv420p', '-an', out_path
    ], capture_output=True, timeout=120)
    import shutil; shutil.rmtree(tmpdir, ignore_errors=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.decode()[-400:])
    return out_path
```

Then chain the pre-rendered clips through xfade using the same `build_slideshow_cmd` above, but pass MP4 clips instead of images (remove `-loop 1 -framerate -t` flags since the clips already have duration).

---

## All xfade transitions (ffmpeg 7+)

| Category    | Transitions |
|-------------|-------------|
| Fades       | `fade`, `fadeblack`, `fadewhite`, `fadegrays`, `dissolve` |
| Wipes       | `wipeleft`, `wiperight`, `wipeup`, `wipedown`, `wipetl`, `wipetr`, `wipebl`, `wipebr` |
| Slides      | `slideleft`, `slideright`, `slideup`, `slidedown` |
| Smooth      | `smoothleft`, `smoothright`, `smoothup`, `smoothdown` |
| Circle      | `circlecrop`, `circleopen`, `circleclose` |
| Vert/Horiz  | `vertopen`, `vertclose`, `horzopen`, `horzclose` |
| Diagonal    | `diagtl`, `diagtr`, `diagbl`, `diagbr` |
| Special     | `pixelize`, `radial`, `rectcrop`, `distance` |

**Recommended for product/retail ads:** `fade`, `dissolve`, `wipeleft`, `smoothleft`, `circleopen`

---

## Integration into Emporium-and-Thrift-App ad generator

When a product has **multiple images**, cycle through them as a slideshow instead of using just the first image.

```python
# In generate_video_ad():
valid_images = [os.path.join(UPLOAD_FOLDER, fn)
                for fn in (product.get('Images','').split(','))
                if fn.strip() and os.path.exists(os.path.join(UPLOAD_FOLDER, fn.strip()))]

if len(valid_images) > 1:
    # Multi-image: render Ken Burns clip per image, chain with xfade
    motions = ['zoom_in','pan_right','zoom_out','pan_left','zoom_in']
    slide_clips = []
    slide_dur = VIDEO_SECS / len(valid_images)  # distribute time evenly
    for i, img_path in enumerate(valid_images):
        clip_path = os.path.join(tmpdir, f'slide_{i}.mp4')
        render_slide_clip(img_path, clip_path, ffmpeg_bin, W, H,
                          dur=slide_dur + 0.8,  # +fade overlap
                          motion=motions[i % len(motions)])
        slide_clips.append(clip_path)
    # Build concat list for slide clips, then xfade chain...
else:
    # Single image: use existing Ken Burns scene pipeline
    ...
```

---

## Gotchas & lessons learned

1. **xfade requires same resolution inputs** — pre-resize all images to W×H before encoding clips
2. **offset formula must be exact** — off-by-one causes hard cuts or missing frames
3. **clip_dur must be > fade_dur** — fade_dur=1.0, clip_dur must be ≥ 1.5 at minimum
4. **`-shortest` is essential** — without it, audio mismatch makes the video loop
5. **PIL crop trick for scale-to-fill**: `scale = max(target_w/img_w, target_h/img_h)` then crop centre
6. **asyncio.run() conflicts with Flask** — always use `new_event_loop()` for TTS in Flask handlers
7. **Ken Burns zoom range** — 1.0→1.45× looks great; anything below 1.22× is barely visible
8. **Frame quality** — JPEG quality=88 for slide frames hits the right speed/quality balance; don't go below 80

---

## Quick reference: single image → 5s clip

```bash
ffmpeg -loop 1 -framerate 30 -i photo.jpg -t 5 \
       -c:v libx264 -pix_fmt yuv420p -crf 22 clip.mp4
```

## Quick reference: 3-image slideshow with xfade

```bash
ffmpeg \
  -loop 1 -framerate 30 -t 4 -i img1.jpg \
  -loop 1 -framerate 30 -t 4 -i img2.jpg \
  -loop 1 -framerate 30 -t 4 -i img3.jpg \
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=1:offset=3[x1];[x1][2:v]xfade=transition=wipeleft:duration=1:offset=6[vout]" \
  -map "[vout]" -c:v libx264 -pix_fmt yuv420p slideshow.mp4
```

---
_Skill written: 2026-05-22 | Echo KiloClaw | Liberty Emporium_
