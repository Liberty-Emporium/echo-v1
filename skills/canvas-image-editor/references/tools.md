# Canvas Image Editor — Tool Reference

## Zoom (CSS transform approach)
```js
let zoomLevel = 1.0;
const ZOOM_MIN = 0.1, ZOOM_MAX = 8.0;

function zoomIn()    { zoomLevel = Math.min(ZOOM_MAX, +(zoomLevel * 1.25).toFixed(3)); applyZoom(); }
function zoomOut()   { zoomLevel = Math.max(ZOOM_MIN, +(zoomLevel / 1.25).toFixed(3)); applyZoom(); }
function zoomReset() { zoomLevel = 1.0; applyZoom(); }

function applyZoom() {
  canvas.style.transform = `scale(${zoomLevel})`;
  canvas.style.transformOrigin = 'top left';
  document.getElementById('btn-zoom-reset').textContent = Math.round(zoomLevel * 100) + '%';
}

// Mouse wheel zoom
document.getElementById('canvas-wrap').addEventListener('wheel', e => {
  if (!originalImage) return;
  e.preventDefault();
  e.deltaY < 0 ? zoomIn() : zoomOut();
}, { passive: false });
```

## Coordinate Mapping (accounts for CSS zoom)
```js
// Always use this when mapping mouse position to canvas pixel coords:
function getCanvasCoords(e) {
  const rect = canvas.getBoundingClientRect();
  const scaleX = canvas.width  / (rect.width  / zoomLevel);
  const scaleY = canvas.height / (rect.height / zoomLevel);
  return {
    x: ((e.clientX - rect.left) / zoomLevel) * scaleX,
    y: ((e.clientY - rect.top)  / zoomLevel) * scaleY
  };
}
```

## Pixel Eraser (destination-out on workingCanvas)
```js
let eraseMode = false, erasing = false, eraseSize = 30;

function toggleEraseMode() {
  eraseMode = !eraseMode;
  const btn = document.getElementById('btn-erase');
  btn.classList.toggle('primary', eraseMode);
  btn.textContent = eraseMode ? '🗑 Erasing…' : '🗑 Erase';
  canvas.style.cursor = eraseMode ? 'cell' : 'crosshair';
}

function doErase(e) {
  if (!eraseMode || !erasing || !originalImage) return;
  const {x, y} = getCanvasCoords(e);
  workingCtx.save();
  workingCtx.globalCompositeOperation = 'destination-out';
  workingCtx.beginPath();
  workingCtx.arc(x, y, eraseSize / 2, 0, Math.PI * 2);
  workingCtx.fill();
  workingCtx.restore();
  // Re-sync originalImage source
  originalImage = workingCanvas;
  originalImage.naturalWidth = workingCanvas.width;
  originalImage.naturalHeight = workingCanvas.height;
  redraw();
}

canvas.addEventListener('mousedown', e => { if (eraseMode) { erasing = true; doErase(e); }});
canvas.addEventListener('mousemove', e => { if (eraseMode && erasing) doErase(e); });
canvas.addEventListener('mouseup',   () => { erasing = false; });
```

## Crop Overlay (SVG overlay pattern)
```js
let cropActive = false, cropBox = null, cropDragging = false, cropStart = null;

function toggleCrop() {
  cropActive = !cropActive;
  // Create/remove SVG overlay (same pattern as guided BG remove overlay)
  if (cropActive) startCropDraw(); else cancelCrop();
}

function applyCrop() {
  if (!cropBox || !originalImage) return;
  // cropBox is {x, y, w, h} in canvas pixel coords (already zoom-compensated)
  const tmp = document.createElement('canvas');
  tmp.width = cropBox.w; tmp.height = cropBox.h;
  tmp.getContext('2d').drawImage(workingCanvas, cropBox.x, cropBox.y, cropBox.w, cropBox.h, 0, 0, cropBox.w, cropBox.h);
  workingCanvas.width = cropBox.w; workingCanvas.height = cropBox.h;
  workingCtx.drawImage(tmp, 0, 0);
  originalImage = workingCanvas;
  originalImage.naturalWidth = cropBox.w;
  originalImage.naturalHeight = cropBox.h;
  cancelCrop();
  redraw();
}
```

## Undo/Redo Stack
```js
const MAX_HISTORY = 40;
let history = [], historyIndex = -1;

function pushHistory() {
  history = history.slice(0, historyIndex + 1);
  if (history.length >= MAX_HISTORY) history.shift();
  const snap = document.createElement('canvas');
  snap.width = workingCanvas.width; snap.height = workingCanvas.height;
  snap.getContext('2d').drawImage(workingCanvas, 0, 0);
  history.push(snap);
  historyIndex = history.length - 1;
}

function undo() {
  if (historyIndex <= 0) return;
  historyIndex--;
  restoreHistory();
}

function redo() {
  if (historyIndex >= history.length - 1) return;
  historyIndex++;
  restoreHistory();
}

function restoreHistory() {
  const snap = history[historyIndex];
  workingCanvas.width = snap.width; workingCanvas.height = snap.height;
  workingCtx.drawImage(snap, 0, 0);
  originalImage = workingCanvas;
  originalImage.naturalWidth = snap.width;
  originalImage.naturalHeight = snap.height;
  redraw();
}
// Call pushHistory() before any destructive operation (erase, crop, adjustments)
// Keyboard: document.addEventListener('keydown', e => { if(e.ctrlKey&&e.key==='z') undo(); if(e.ctrlKey&&e.key==='y') redo(); });
```

## Image Adjustments (brightness/contrast/saturation via ImageData)
```js
function applyAdjustments(brightness=0, contrast=0, saturation=0) {
  // brightness: -100 to 100, contrast: -100 to 100, saturation: -100 to 100
  const src = document.createElement('canvas');
  src.width = originalImage.naturalWidth; src.height = originalImage.naturalHeight;
  src.getContext('2d').drawImage(originalImage, 0, 0);
  const ctx2 = src.getContext('2d');
  const data = ctx2.getImageData(0, 0, src.width, src.height);
  const d = data.data;
  const bFactor = brightness / 100 * 255;
  const cFactor = (100 + contrast) / 100;
  const sFactor = (100 + saturation) / 100;
  for (let i = 0; i < d.length; i += 4) {
    let r = d[i], g = d[i+1], b = d[i+2];
    // Brightness
    r = Math.min(255, Math.max(0, r + bFactor));
    g = Math.min(255, Math.max(0, g + bFactor));
    b = Math.min(255, Math.max(0, b + bFactor));
    // Contrast
    r = Math.min(255, Math.max(0, (r - 128) * cFactor + 128));
    g = Math.min(255, Math.max(0, (g - 128) * cFactor + 128));
    b = Math.min(255, Math.max(0, (b - 128) * cFactor + 128));
    // Saturation (luminance-based)
    const lum = 0.299*r + 0.587*g + 0.114*b;
    d[i]   = Math.min(255, Math.max(0, lum + (r - lum) * sFactor));
    d[i+1] = Math.min(255, Math.max(0, lum + (g - lum) * sFactor));
    d[i+2] = Math.min(255, Math.max(0, lum + (b - lum) * sFactor));
  }
  ctx2.putImageData(data, 0, 0);
  workingCanvas.width = src.width; workingCanvas.height = src.height;
  workingCtx.drawImage(src, 0, 0);
  originalImage = workingCanvas;
  originalImage.naturalWidth = src.width; originalImage.naturalHeight = src.height;
  redraw();
}
```

## Image Load Pattern (correct)
```js
function loadImageFromUrl(src) {
  showSpinner(true);
  fetch(src, { method: 'HEAD', credentials: 'same-origin', redirect: 'follow' })
    .then(r => {
      const ct = r.headers.get('content-type') || '';
      if (!r.ok || r.headers.get('X-Upload-Missing') || !ct.startsWith('image/')) {
        showSpinner(false);
        showNoImageMessage('Image not found on server — upload a new photo below');
        return;
      }
      _doLoadImage(src);
    })
    .catch(() => _doLoadImage(src));
}

function _doLoadImage(src) {
  const img = new Image();
  // DO NOT set img.crossOrigin — same-origin images don't need it; it causes canvas taint
  img.onload = () => {
    const MAX = 2400;
    let nw = img.naturalWidth, nh = img.naturalHeight;
    if (nw > MAX || nh > MAX) {
      const s = MAX / Math.max(nw, nh);
      nw = Math.round(nw * s); nh = Math.round(nh * s);
    }
    // Store scaled canvas as originalImage (not the HTMLImageElement)
    const scaled = document.createElement('canvas');
    scaled.width = nw; scaled.height = nh;
    scaled.getContext('2d').drawImage(img, 0, 0, nw, nh);
    originalImage = scaled;
    originalImage.naturalWidth = nw; originalImage.naturalHeight = nh;
    workingCanvas.width = nw; workingCanvas.height = nh;
    workingCtx.drawImage(scaled, 0, 0);
    rotation = 0; flipH = false; flipV = false;
    pushHistory();  // initial state
    redraw();
    setButtonsEnabled(true);
    showSpinner(false);
  };
  img.onerror = () => { showSpinner(false); showNoImageMessage('Failed to load image — try uploading again'); };
  img.src = src.includes('?') ? src : src + '?t=' + Date.now();
}
```
