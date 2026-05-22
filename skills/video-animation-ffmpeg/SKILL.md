---
name: video-animation-ffmpeg
description: Deep reference for video animation using ffmpeg + Python — drawtext animations, xfade transitions, zoompan Ken Burns, color grading, easing functions, lower thirds, commercial scene building. Use whenever building or improving video generation code.
---

# Video Animation with ffmpeg — Deep Reference

## Core Principle: Everything is an Expression

ffmpeg's filter graph accepts **math expressions** for nearly every parameter.
These expressions are re-evaluated per frame, which is how animation works.

**Key time variables in drawtext/zoompan:**
| Variable | Meaning |
|----------|---------|
| `t` | Current time in seconds (float) |
| `n` | Frame number (integer) |
| `w`, `h` | Video width / height |
| `tw`, `th` | Text width / height (drawtext only) |
| `on` | Output frame number (zoompan) |
| `zoom`, `pzoom` | Current / previous zoom level (zoompan) |
| `x`, `px` | Current / previous x position (zoompan) |

---

## TEXT ANIMATIONS (drawtext)

### Slide In from Left
```
x='lerp(-tw, (w-tw)/2, min(1, t/0.4))'
```
- Starts off-screen left (`-tw`), reaches center in 0.4s
- `lerp(start, end, progress)` — ffmpeg's built-in linear interpolation

### Slide In from Right
```
x='lerp(w, (w-tw)/2, min(1, t/0.4))'
```

### Slide In from Bottom (lower third style)
```
y='lerp(h, h-th-40, min(1, t/0.3))'
```

### Slide In from Top
```
y='lerp(-th, 40, min(1, t/0.3))'
```

### Ease-Out Slide (cubic — feels natural, not mechanical)
```
x='lerp(w, (w-tw)/2, 1-(1-min(1,t/0.4))^3)'
```
- `1-(1-p)^3` is cubic ease-out: fast start, slow finish

### Pop / Scale Bounce
ffmpeg drawtext doesn't support fontsize animation per-frame natively.
Workaround: use multiple drawtext layers with `enable='between(t,0,0.1)'` etc.
for a pop effect at defined time windows.

### Fade In
```
alpha='min(1, t/0.4)'
```

### Fade In then Hold then Fade Out
```
alpha='if(lt(t,0.3), t/0.3, if(gt(t,HOLD_END), max(0,(FADE_END-t)/0.3), 1))'
```

### Typewriter Effect (reveal one character at a time)
Use `text_h` variable and `enable` with character-by-character drawtext calls.
Simpler: use multiple overlapping drawtext calls each with `enable='gte(t,N*0.08)'`

### Moving Text (linear path from A to B)
```
x='x1+(x2-x1)*(t-t1)/(t2-t1)'
y='y1+(y2-y1)*(t-t1)/(t2-t1)'
```
Replace x1/x2/y1/y2/t1/t2 with actual values.

### Drop Shadow (always use for legibility)
```
shadowcolor=black:shadowx=6:shadowy=6
```
For glowing effect: `shadowcolor=0xD4A017:shadowx=0:shadowy=0:box=1:boxcolor=0xD4A017@0.3:boxborderw=20`

---

## LOWER THIRDS (TV commercial style)

### Classic Lower Third — Bar slides in, text fades up
```python
# Step 1: drawbox for the bar (slides in from left)
f"drawbox=x='lerp(-w,0,min(1,t/0.25))':y={bar_y}:w={W}:h={bar_h}:color=0x8B0000@0.9:t=fill,"
# Step 2: accent stripe on left edge
f"drawbox=x='lerp(-16,0,min(1,t/0.25))':y={bar_y}:w=14:h={bar_h}:color=0xD4A017@1:t=fill,"
# Step 3: text fades up inside bar
f"drawtext=fontfile='{bold}':text='{title}':fontsize=88:"
f"fontcolor=white:x=(w-tw)/2:y={bar_y+bar_h//2-44}:"
f"alpha='max(0,min(1,(t-0.1)/0.25))'"
```

### Bug/Logo Bug (persistent corner badge)
```python
f"drawtext=fontfile='{sans}':text='LIBERTY EMPORIUM':fontsize=36:"
f"fontcolor=0xD4A017@0.85:x=30:y=30:"
f"shadowcolor=black:shadowx=2:shadowy=2"
```

---

## ZOOMPAN — Ken Burns Effect

### Variable reference (zoompan expressions)
- `on` = output frame number (counts up from 0)
- `zoom` = current zoom level
- `pzoom` = previous zoom level
- `iw`, `ih` = input width/height (the 2x scaled source)
- Expressions evaluated per output frame

### Zoom IN (wide → close, pulls viewer toward item)
```python
f"zoompan=z='1.0+0.18*on/{total_frames}'"
f":x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2'"
f":d={total_frames}:s={W}x{H}:fps=30"
```

### Zoom OUT (close → wide, reveals context)
```python
f"zoompan=z='1.18-0.18*on/{total_frames}'"
f":x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2'"
f":d={total_frames}:s={W}x{H}:fps=30"
```

### Pan Left to Right while zoomed
```python
f"zoompan=z='1.25'"
f":x='(iw/4)+((iw/4)*on/{total_frames})'"  # moves right
f":y='(ih-ih/zoom)/2'"
f":d={total_frames}:s={W}x{H}:fps=30"
```

### Pan from Top-Left corner to Center (simulate 2nd camera angle)
```python
f"zoompan=z='1.25'"
f":x='(iw/4)*(1-on/{total_frames})'"      # starts at left offset, moves to center
f":y='(ih/4)*(1-on/{total_frames})'"      # starts at top offset, moves to center
f":d={total_frames}:s={W}x{H}:fps=30"
```

### ⚠️ Zoompan Zig-Zag Bug Fix
**Problem:** zoompan x/y expressions that change too fast cause zig-zag artifacts.
**Fix:** The x/y in zoompan are expressed as percentages of the *input* canvas (2x size).
Always anchor both x and y to the zoom level:
```
x='(iw-iw/zoom)/2'   # centered
y='(ih-ih/zoom)/2'   # centered
```
For panning, change the offset but keep zoom consistent:
```
x='(iw-iw/zoom)/2 + offset*on/total_frames'
```

---

## XFADE TRANSITIONS (between scenes)

All 56 transitions available in ffmpeg 4.3+:

**Best for commercials:**
| Transition | Effect | Best Use |
|-----------|--------|---------|
| `fade` | Simple crossfade | Safe default |
| `fadeblack` | Fades through black | Scene separator |
| `wipeleft` | Hard wipe left | Fast cut energy |
| `slideleft` | Scene slides left | Product reveal |
| `slideright` | Scene slides right | Going back/context |
| `circleopen` | Iris open | Product launch moment |
| `dissolve` | Random pixel dissolve | Dreamy/memory feel |
| `zoomin` | New scene zooms in | Impact/attention |
| `revealleft` | New scene revealed left | Dynamic, editorial |
| `horzopen` | Opens from center horizontally | Wide reveal |
| `smoothleft` | Soft slide left | Professional/smooth |

### Using xfade in filter_complex
```python
# Two scenes with xfade dissolve between them
filt = (
    f'[0:v]trim=duration={s1_dur},setpts=PTS-STARTPTS[s1];'
    f'[0:v]trim=start={s1_dur}:duration={s2_dur},setpts=PTS-STARTPTS[s2];'
    f'[s1][s2]xfade=transition=wipeleft:duration=0.2:offset={s1_dur-0.2}[vout]'
)
```

### Chaining multiple xfade transitions
```python
def chain_xfade(scenes, transition='fade', dur=0.2):
    """
    scenes = [('label', duration_secs), ...]
    Returns filter_complex string with xfade between all scenes.
    """
    parts = []
    offset = 0.0
    prev = scenes[0][0]
    for i, (label, scene_dur) in enumerate(scenes[1:], 1):
        offset += scenes[i-1][1] - dur
        out = f'xf{i}'
        parts.append(
            f'[{prev}][{label}]xfade=transition={transition}:'
            f'duration={dur}:offset={offset:.3f}[{out}]'
        )
        prev = out
    return ';'.join(parts), prev  # (filter_str, final_output_label)
```

---

## COLOR GRADING

### Warm cinematic (product shots, thrift items)
```
colorchannelmixer=rr=1.05:gg=0.98:bb=0.92
eq=contrast=1.15:brightness=0.02:saturation=1.2
```

### Cool/editorial (detail shots, close-ups)
```
colorchannelmixer=rr=0.97:gg=0.99:bb=1.04
eq=contrast=1.2:brightness=-0.01:saturation=1.15
```

### Dark dramatic (blurred bg scenes, price reveal, outro)
```
colorchannelmixer=rr=0.15:gg=0.15:bb=0.15
```
(Equivalent to ~85% brightness reduction — true near-black)

### Vintage/sepia
```
colorchannelmixer=rr=0.9:rg=0.1:rb=0.02:gr=0.05:gg=0.85:gb=0.05:br=0.02:bg=0.05:bb=0.7
eq=saturation=0.6:brightness=0.02
```

### Gaussian blur (for background scenes)
```
boxblur=luma_radius=20:luma_power=2   # medium
boxblur=luma_radius=26:luma_power=3   # heavy/dreamy
```

---

## EASING FUNCTIONS (in ffmpeg expressions)

ffmpeg has `lerp(a, b, t)` built in but no easing. Simulate with:

| Easing | Expression |
|--------|-----------|
| Linear | `t` |
| Ease-out cubic | `1-(1-t)^3` |
| Ease-in cubic | `t^3` |
| Ease-in-out | `if(lt(t,0.5), 4*t^3, 1-(-2*t+2)^3/2)` |
| Bounce | Complex — use `lerp` with overshoot: `lerp(a, b*1.08, t)` then back |

### Using in drawtext alpha:
```
alpha='1-(1-min(1,t/0.4))^3'   # ease-out fade-in over 0.4s
```

### Using in x position (slide with ease-out):
```
x='lerp(w, (w-tw)/2, 1-(1-min(1,t/0.35))^3)'
```

---

## SCENE BUILDING PATTERNS

### Pattern 1: Product reveal (wide → close → price)
```python
scenes = [
    ('intro',   2.0),   # Store splash
    ('wide',    3.5),   # Product full frame, zoom in
    ('closeup', 3.5),   # Detail crop, pan
    ('price',   2.5),   # Dark bg, price hero
    ('cta',     2.0),   # "Come In Today!"
    ('outro',   1.5),   # Store name + address
]
total = sum(d for _,d in scenes)  # = 15s
```

### Pattern 2: Quick cuts (high energy, bargain vibe)
```python
scenes = [
    ('flash1',  0.8),   # Product flash
    ('flash2',  0.8),   # Different crop
    ('flash3',  0.8),   # Another angle
    ('price',   2.0),   # PRICE
    ('cta',     1.5),   # Store
]
# Use xfade=transition=wipeleft:duration=0.1 between each
```

### Simulating multiple camera angles from ONE image
Key insight: crop different REGIONS of the 2x source image:
```python
W, H = 1080, 1080
# Wide shot: center crop
crop_wide   = f'crop={W}:{H}:{W//2}:{H//2}'
# Close-up top-left: different region
crop_close  = f'crop={W}:{H}:0:0'
# Side detail: right half
crop_side   = f'crop={W}:{H}:{W}:0'
# High angle: bottom portion
crop_high   = f'crop={W}:{H}:{W//2}:{H}'
```
Each crop + different zoom/pan + different color grade = 4 distinct "camera shots"
from a single product photo. This is the core trick of the Liberty Emporium video generator.

---

## COMPLETE COMMERCIAL TEMPLATE (Python function)

```python
def build_commercial(img_path, title, price_str, condition, category,
                     store_name, address, website, video_secs=15,
                     style='elegant', ffmpeg_bin='ffmpeg',
                     audio_path=None, music_path=None,
                     out_path='commercial.mp4'):
    """
    Build a cinematic 6-scene commercial from a single product image.
    No Python frame loop — pure ffmpeg filter_complex.
    """
    import subprocess, uuid, os

    W = H = 1080
    themes = {
        'elegant': {'acc': 'D4A017', 'txt': 'FFFFFF'},
        'bright':  {'acc': 'FF7800', 'txt': 'FFFFFF'},
        'minimal': {'acc': '003087', 'txt': '141414'},
        'vintage': {'acc': 'C9A84C', 'txt': 'F5E6C8'},
    }
    th = themes.get(style, themes['elegant'])
    acc, txt = th['acc'], th['txt']

    def ft(s):
        return s.replace("\\","\\\\").replace("'","\\'").replace(':','\\:').replace('%','\\%')

    bold = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
    sans = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

    # Scene durations
    d = {
        'intro':  video_secs * 0.12,
        'wide':   video_secs * 0.22,
        'close':  video_secs * 0.22,
        'price':  video_secs * 0.18,
        'cta':    video_secs * 0.12,
    }
    d['outro'] = video_secs - sum(d.values())
    fps = 30
    wide_f  = int(d['wide']  * fps)
    close_f = int(d['close'] * fps)

    scenes = []

    # Scene 1: Store intro
    scenes.append(
        f'[0:v]scale={W*2}:{H*2},setsar=1,'
        f'boxblur=luma_radius=24:luma_power=3,'
        f'colorchannelmixer=rr=0.2:gg=0.2:bb=0.2,'
        f'crop={W}:{H}:{W//2}:{H//2},'
        f'trim=duration={d["intro"]:.2f},setpts=PTS-STARTPTS,'
        f'fade=t=in:st=0:d=0.25,fade=t=out:st={d["intro"]-0.25:.2f}:d=0.25,'
        f'drawbox=x=0:y={H//2-160}:w={W}:h=8:color=0x{acc}@1:t=fill,'
        f'drawbox=x=0:y={H//2+155}:w={W}:h=8:color=0x{acc}@1:t=fill,'
        f"drawtext=fontfile='{bold}':text='{ft(store_name)}':fontsize=130:"
        f"fontcolor=0x{acc}:x=(w-tw)/2:y=(h/2)-90:shadowcolor=black:shadowx=6:shadowy=6:"
        f"alpha='min(1,t/0.3)',"
        f"drawtext=fontfile='{sans}':text='Liberty\\, North Carolina':fontsize=62:"
        f"fontcolor=white:x=(w-tw)/2:y=(h/2)+65:shadowcolor=black:shadowx=4:shadowy=4:"
        f"alpha='max(0\\,min(1\\,(t-0.15)/0.35))'"
        f'[s1]'
    )

    # Scene 2: Wide shot, zoom in, warm grade
    scenes.append(
        f'[0:v]scale={W*2}:{H*2},setsar=1,'
        f'colorchannelmixer=rr=1.05:gg=0.98:bb=0.92,'
        f'eq=contrast=1.15:brightness=0.02:saturation=1.2,'
        f"zoompan=z='1.0+0.18*on/{wide_f}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':"
        f'd={wide_f}:s={W}x{H}:fps={fps},'
        f'trim=duration={d["wide"]:.2f},setpts=PTS-STARTPTS,'
        f'fade=t=in:st=0:d=0.2,fade=t=out:st={d["wide"]-0.2:.2f}:d=0.2,'
        f'drawbox=x=0:y={int(H*0.72)}:w={W}:h={int(H*0.28)}:color=black@0.82:t=fill,'
        f'drawbox=x=0:y={int(H*0.72)}:w=16:h={int(H*0.28)}:color=0x{acc}@1:t=fill,'
        f"drawtext=fontfile='{bold}':text='{ft(title[:32])}':fontsize=96:"
        f"fontcolor=white:x=(w-tw)/2:y={int(H*0.755)}:shadowcolor=black:shadowx=5:shadowy=5:"
        f"alpha='max(0\\,min(1\\,(t-0.1)/0.25))'"
        f'[s2]'
    )

    # Scene 3: Close-up, pan from TL to center, cool grade
    scenes.append(
        f'[0:v]scale={W*2}:{H*2},setsar=1,'
        f'colorchannelmixer=rr=0.97:gg=0.99:bb=1.04,'
        f'eq=contrast=1.2:saturation=1.15,'
        f"zoompan=z='1.25':x='(iw/4)*(1-on/{close_f})':y='(ih/4)*(1-on/{close_f})':"
        f'd={close_f}:s={W}x{H}:fps={fps},'
        f'trim=duration={d["close"]:.2f},setpts=PTS-STARTPTS,'
        f'fade=t=in:st=0:d=0.18,fade=t=out:st={d["close"]-0.18:.2f}:d=0.18,'
        f"drawtext=fontfile='{sans}':text='{ft(condition)}':fontsize=52:"
        f"fontcolor=0x{acc}:x=40:y=40:shadowcolor=black:shadowx=3:shadowy=3:"
        f"alpha='max(0\\,min(1\\,(t-0.15)/0.25))'"
        f'[s3]'
    )

    # Scene 4: Price hero
    scenes.append(
        f'[0:v]scale={W*2}:{H*2},setsar=1,'
        f'boxblur=luma_radius=20:luma_power=2,'
        f'colorchannelmixer=rr=0.15:gg=0.15:bb=0.15,'
        f'crop={W}:{H}:{W//2}:{H//2},'
        f'trim=duration={d["price"]:.2f},setpts=PTS-STARTPTS,'
        f'fade=t=in:st=0:d=0.15,fade=t=out:st={d["price"]-0.2:.2f}:d=0.2,'
        f"drawtext=fontfile='{sans}':text='JUST':fontsize=72:"
        f"fontcolor=0x{acc}:x=(w-tw)/2:y={H//2-240}:shadowcolor=black:shadowx=5:shadowy=5:"
        f"alpha='min(1,t/0.2)',"
        f"drawtext=fontfile='{bold}':text='{ft(price_str)}':fontsize=210:"
        f"fontcolor=white:x=(w-tw)/2:y={H//2-100}:shadowcolor=black:shadowx=8:shadowy=8:"
        f"alpha='min(1,t/0.15)'"
        f'[s4]'
    )

    # Scene 5: CTA
    scenes.append(
        f'[0:v]scale={W*2}:{H*2},setsar=1,'
        f'boxblur=luma_radius=16:luma_power=2,'
        f'colorchannelmixer=rr=0.22:gg=0.22:bb=0.22,'
        f'crop={W}:{H}:{W//2}:{H//2},'
        f'trim=duration={d["cta"]:.2f},setpts=PTS-STARTPTS,'
        f'fade=t=in:st=0:d=0.15,fade=t=out:st={d["cta"]-0.2:.2f}:d=0.2,'
        f"drawtext=fontfile='{bold}':text='Come In Today!':fontsize=120:"
        f"fontcolor=0x{acc}:x=(w-tw)/2:y={H//2-80}:shadowcolor=black:shadowx=6:shadowy=6:"
        f"alpha='min(1,t/0.25)',"
        f"drawtext=fontfile='{sans}':text='While supplies last':fontsize=60:"
        f"fontcolor=white:x=(w-tw)/2:y={H//2+70}:shadowcolor=black:shadowx=4:shadowy=4:"
        f"alpha='max(0\\,min(1\\,(t-0.15)/0.25))'"
        f'[s5]'
    )

    # Scene 6: Outro
    scenes.append(
        f'[0:v]scale={W*2}:{H*2},setsar=1,'
        f'boxblur=luma_radius=26:luma_power=3,'
        f'colorchannelmixer=rr=0.12:gg=0.12:bb=0.12,'
        f'crop={W}:{H}:{W//2}:{H//2},'
        f'trim=duration={d["outro"]:.2f},setpts=PTS-STARTPTS,'
        f'fade=t=in:st=0:d=0.3,fade=t=out:st={d["outro"]-0.5:.2f}:d=0.5,'
        f'drawbox=x=0:y={H//2-185}:w={W}:h=10:color=0x{acc}@1:t=fill,'
        f'drawbox=x=0:y={H//2+178}:w={W}:h=10:color=0x{acc}@1:t=fill,'
        f"drawtext=fontfile='{bold}':text='{ft(store_name)}':fontsize=120:"
        f"fontcolor=0x{acc}:x=(w-tw)/2:y={H//2-110}:shadowcolor=black:shadowx=6:shadowy=6:"
        f"alpha='min(1,t/0.35)',"
        f"drawtext=fontfile='{sans}':text='{ft(address)}':fontsize=56:"
        f"fontcolor=white:x=(w-tw)/2:y={H//2+35}:shadowcolor=black:shadowx=4:shadowy=4:"
        f"alpha='max(0\\,min(1\\,(t-0.15)/0.35))',"
        f"drawtext=fontfile='{sans}':text='{ft(website)}':fontsize=46:"
        f"fontcolor=0x{acc}:x=(w-tw)/2:y={H//2+110}:shadowcolor=black:shadowx=4:shadowy=4:"
        f"alpha='max(0\\,min(1\\,(t-0.25)/0.4))'"
        f'[s6]'
    )

    filter_complex = ';'.join(scenes) + ';[s1][s2][s3][s4][s5][s6]concat=n=6:v=1:a=0[vout]'

    # Build audio mix
    if audio_path and music_path:
        filter_complex += ';[1:a]volume=1.0[vo];[2:a]volume=0.12[bg];[vo][bg]amix=inputs=2:duration=first[aout]'
        cmd = [ffmpeg_bin, '-y', '-loop', '1', '-i', img_path,
               '-i', audio_path, '-i', music_path,
               '-filter_complex', filter_complex,
               '-map', '[vout]', '-map', '[aout]',
               '-c:v', 'libx264', '-preset', 'fast', '-crf', '20',
               '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k',
               '-shortest', out_path]
    elif audio_path:
        cmd = [ffmpeg_bin, '-y', '-loop', '1', '-i', img_path, '-i', audio_path,
               '-filter_complex', filter_complex,
               '-map', '[vout]', '-map', '1:a',
               '-c:v', 'libx264', '-preset', 'fast', '-crf', '20',
               '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k',
               '-shortest', out_path]
    else:
        cmd = [ffmpeg_bin, '-y', '-loop', '1', '-i', img_path,
               '-filter_complex', filter_complex,
               '-map', '[vout]',
               '-c:v', 'libx264', '-preset', 'fast', '-crf', '20',
               '-pix_fmt', 'yuv420p', '-an',
               '-t', str(int(video_secs) + 1), out_path]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=240)
    return result.returncode == 0, result.stderr[-500:] if result.returncode != 0 else ''
```

---

## ANIMATION DESIGN PRINCIPLES (from research)

### The 12 Principles applied to video ads
1. **Staging** — One focal element per scene. Don't compete. Product → Price → Store.
2. **Ease In/Out** — Never use linear motion. Always cubic ease-out for entrances.
3. **Anticipation** — Brief pause before action (small delay before text appears).
4. **Follow Through** — Let elements settle slightly past target before resting.
5. **Appeal** — Strong design first. Motion enhances good design, can't rescue bad.
6. **Timing** — Fast for energy (0.15–0.25s), slow for elegance (0.4–0.6s).

### Golden timing rules for commercials
- **Hard cut between scenes:** 0.15–0.2s fade
- **Soft cut / emotional beat:** 0.3–0.4s fade through black
- **Text entrance:** 0.25–0.35s ease-out
- **Price reveal:** 0.12–0.15s (near-instant = impact)
- **Final outro:** 0.4–0.5s fade to black (closure)
- **Scene durations:** min 1.5s per scene, max 4s for product shot

### Attention curve rule
Viewers disengage after 2.5s of no new stimulus.
Every scene needs at least ONE new element appearing within 2.5s of start.

---

## TROUBLESHOOTING

| Problem | Cause | Fix |
|---------|-------|-----|
| Zig-zag zoom | zoompan x/y changing non-linearly | Lock to `(iw-iw/zoom)/2` for centering |
| Text not showing | Font path wrong | Use absolute path + `fontfile=` param |
| Text too small | 1080×1080 needs large fonts | Min 46px, price 180–210px |
| Scene flicker | `trim` without `setpts` | Always add `setpts=PTS-STARTPTS` after `trim` |
| Audio out of sync | Multiple inputs wrong map | Use `-map [vout] -map [aout]` explicitly |
| Worker timeout (500) | ffmpeg running too long in gunicorn | Set `--timeout 300` in Procfile |
| xfade offset wrong | Offset = cumulative time − transition overlap | Recalculate: `offset += prev_dur - xfade_dur` |
| `No such filter` error | Old ffmpeg version | Check `ffmpeg -version`, zoompan needs 3.0+, xfade needs 4.3+ |
