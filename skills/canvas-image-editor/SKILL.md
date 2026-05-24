---
name: canvas-image-editor
description: >-
  Build, debug, extend, or fix browser-based HTML5 canvas image editors embedded in Flask/Jinja2 apps.
  Use when working on the Emporium & Thrift App image editor or any similar in-browser photo editor
  involving zoom/pan, crop overlays, pixel eraser, drawing tools, background removal via rembg,
  guided bbox removal, undo/redo, image adjustments, upload/delete/reorder, Flask upload routes,
  Railway volume persistence, or any canvas rendering bug such as blank canvas, infinite recursion,
  coordinate mapping errors, or crossOrigin taint.
---

# Canvas Image Editor Skill

## Architecture Overview

Our editor uses a **two-canvas + viewport-transform pattern**:

```
[Image File on Server]
       ↓  /uploads/<filename>  (Flask route, served from /data/uploads/ on Railway volume)
[workingCanvas]  ← off-screen, holds the pixel-manipulated image at display resolution
       ↓  redraw()
[canvas]         ← visible canvas, applies rotation/flip transforms, CSS zoom
[draw-canvas]    ← absolutely-positioned SVG/canvas overlay for non-destructive drawing
```

**Key variables:**
- `originalImage` — scaled canvas element (NOT an HTMLImageElement after load)
- `workingCanvas` / `workingCtx` — where pixel ops (erase, adjust) happen
- `canvas` / `canvasCtx` — display canvas
- `zoomLevel` — CSS `transform: scale()` on canvas element (display-only, does NOT change canvas pixel coords)
- `rotation`, `flipH`, `flipV` — applied in `redraw()` via ctx.save/translate/rotate/scale

## Critical Rules (learned the hard way)

### Never set `crossOrigin = 'anonymous'` on same-origin images
Flask serves `/uploads/` from the same domain. Setting crossOrigin causes canvas taint when server doesn't send CORS headers → blank canvas. **Remove it.**

### HEAD check needs `credentials: 'same-origin'`
Before loading an image, do a HEAD fetch with `credentials: 'same-origin'`. Without it, Flask redirects to login (302→200 HTML). Check `content-type.startsWith('image/')` — if it's `text/html` the image is missing.

### Never redefine `redraw()` as a wrapper
Adding drawing tools with `const _origRedraw = redraw; function redraw() { _origRedraw(); ... }` causes infinite recursion when the main editor gets rebuilt. Instead, put `if (drawActive) syncDrawCanvas();` at the end of the real `redraw()`.

### Store display dimensions separately from naturalWidth
After downsampling a large image: create a scaled `<canvas>` element and set it as `originalImage`. Set `originalImage.naturalWidth/Height = nw/nh` explicitly. If `redraw()` reads `originalImage.naturalWidth` from an HTMLImageElement (full-res), working canvas dimensions are wrong.

### Zoom is CSS-only — pixel coordinates must compensate
`zoomLevel` uses `canvas.style.transform = scale(${zoomLevel})`. When mapping mouse clicks to canvas pixels: `const scaleX = canvas.width / (rect.width / zoomLevel)`. All tools (eraser, crop, draw) must account for zoom.

### DATA_DIR on Railway — always auto-detect volume
```python
_vol = os.environ.get('RAILWAY_VOLUME_MOUNT_PATH', '')
DATA_DIR = os.environ.get('DATA_DIR', _vol if _vol else BASE_DIR)
UPLOAD_FOLDER = os.path.join(DATA_DIR, 'uploads')
```
Without this, uploads go to `/app/uploads/` which is wiped on every redeploy.

### `/uploads/` route — return 404 not 500 on missing files
```python
@app.route('/uploads/<filename>')
def serve_upload(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        placeholder = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=')
        return Response(placeholder, status=404, mimetype='image/png', headers={'X-Upload-Missing': filename})
    return send_from_directory(UPLOAD_FOLDER, filename)
```

## Standard Tool Implementations

See `references/tools.md` for copy-paste JS for: zoom, pixel eraser, crop overlay, drawing tools, undo/redo stack, adjustments (brightness/contrast/saturation via ImageData), guided bbox background removal.

See `references/backend.md` for Flask route patterns: upload, delete, reorder, save-image, guided-remove-bg, enhance-image (rembg).

## Common Bugs Checklist

| Symptom | Cause | Fix |
|---------|-------|-----|
| Blank/buffering canvas | crossOrigin flag or missing credentials on fetch | Remove crossOrigin; add `credentials:'same-origin'` |
| Canvas shows wrong content | HEAD fetch got login HTML (text/html), treated as image | Check `content-type.startsWith('image/')` |
| `too much recursion` in redraw | redraw() wrapper calls itself | Merge wrapper into main redraw; never use `_origRedraw` pattern |
| Erase/draw coords off after zoom | Not compensating for CSS zoom in mouse→canvas mapping | Divide rect dimensions by zoomLevel before scaling |
| Images wiped on redeploy | Uploads going to /app not /data volume | Auto-detect RAILWAY_VOLUME_MOUNT_PATH |
| `/uploads/` returns 500 | UPLOAD_FOLDER doesn't exist | Return 404 placeholder PNG with X-Upload-Missing header |
| `currentImage is not defined` | Wrong variable name (should be `originalImage`) | Global search-replace currentImage → originalImage |
| Build fails: `npm ci` lock file mismatch | package.json has package not in lock file | Run `npm install` locally, commit new package-lock.json |
| Railway using cached old layer | Build cache not busted after fix | Append comment to Dockerfile to force fresh build |

## Workflow for Adding a New Tool

1. Add button to toolbar HTML (check `setButtonsEnabled` array and add new btn id)
2. Add JS function — put it **before** `// ── Auto-load first image` comment
3. If tool needs canvas mouse events: add `canvas.addEventListener(...)` — always compensate for `zoomLevel`
4. If tool modifies pixels: modify `workingCanvas`, then call `originalImage = workingCanvas; originalImage.naturalWidth = nw; originalImage.naturalHeight = nh; redraw();`
5. If tool needs a backend route: add Flask route, JSON in/out, call `save_inventory(products)` at end
6. Commit and push — Railway auto-deploys from `main` branch
