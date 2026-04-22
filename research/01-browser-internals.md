# Browser Internals & Rendering Pipeline
_Research compiled: 2026-04-22_

---

## 1. How Browsers Parse HTML/CSS → DOM & CSSOM

### HTML Parsing → DOM
The browser receives HTML as a byte stream and processes it in stages:

1. **Bytes → Characters** — raw bytes decoded using charset (UTF-8 etc.)
2. **Characters → Tokens** — HTML tokenizer produces StartTag, EndTag, Text tokens
3. **Tokens → Nodes** — each token becomes a node object
4. **Nodes → DOM** — nodes arranged into tree structure

The parser is **incremental** — it starts building the DOM before the full HTML arrives. This is why putting `<script>` at the bottom matters.

Key insight: HTML parsing is **error-tolerant** by spec. Malformed HTML is corrected, not rejected.

### Parser-Blocking vs Async Resources
- **`<script>` without async/defer** → **parser-blocking** — HTML parsing stops until script downloads + executes
- **`<script async>`** → downloads in parallel, executes when ready (may interrupt parsing)
- **`<script defer>`** → downloads in parallel, executes after DOM complete (in order)
- **`<link rel="stylesheet">`** → doesn't block HTML parsing but **blocks rendering** (CSSOM must be built)

### CSS Parsing → CSSOM
CSS is parsed separately into the **CSS Object Model (CSSOM)** — a tree of style rules.
- CSSOM cannot be built incrementally (CSS is order-dependent — later rules override earlier ones)
- This is why CSS blocks rendering: the browser needs the **complete** CSSOM before it can style anything
- Inline styles are added to the CSSOM at parse time

---

## 2. Critical Rendering Path (CRP)

The sequence from receiving bytes to pixels on screen:

```
HTML bytes → DOM
CSS bytes  → CSSOM
DOM + CSSOM → Render Tree → Layout → Paint → Composite
```

### What Blocks Rendering
1. **CSS** — always render-blocking. Until CSSOM is built, nothing paints.
2. **Synchronous JS** — parser-blocking AND potentially render-blocking (JS can modify DOM/CSSOM)
3. **Web fonts** — can cause FOIT (Flash of Invisible Text) or FOUT (Flash of Unstyled Text)

### Optimization Techniques
- `<link rel="preload">` — fetch critical resources early
- Media queries on stylesheets: `<link media="print">` — non-matching CSS is non-blocking
- Inline critical CSS — avoid render-blocking stylesheet load for above-the-fold content
- `font-display: swap` — avoid FOIT

### Time to First Byte (TTFB) vs First Contentful Paint (FCP) vs LCP
- **TTFB** — server response time, pure network/server
- **FCP** — first pixel of any content painted
- **LCP** — largest content element painted (key Core Web Vital)

---

## 3. Render Tree Construction

The Render Tree is built by combining DOM + CSSOM:
- Only **visible** nodes included (e.g. `display:none` nodes excluded, `visibility:hidden` included)
- Each render tree node = DOM node + computed styles
- Pseudo-elements (`::before`, `::after`) ARE in render tree even though not in DOM

---

## 4. Layout (Reflow)

Layout calculates the **exact position and size** of every element.

- Triggered by: DOM changes, style changes that affect geometry, window resize, font load
- **Reflow is expensive** — cascades through the tree
- **Forced synchronous layout (FSL)** — reading layout properties (offsetWidth, getBoundingClientRect) after writing styles forces immediate reflow:
  ```js
  // BAD — forces FSL in a loop
  for (let el of elements) {
    el.style.width = el.offsetWidth + 10 + 'px'; // read after write = FSL
  }
  // GOOD — batch reads then writes
  const widths = elements.map(el => el.offsetWidth);
  elements.forEach((el, i) => el.style.width = widths[i] + 10 + 'px');
  ```

---

## 5. Paint

After layout, the browser paints pixels into layers:
- Text, colors, images, borders, shadows
- Some CSS properties create new **paint layers**: `transform`, `opacity`, `will-change`, `position:fixed`
- **Stacking contexts** determine paint order

### What Triggers Repaint
- Color/background changes
- `visibility` changes
- Box shadow changes

### What Triggers Reflow + Repaint
- Adding/removing DOM nodes
- Changing dimensions, margins, padding
- Changing font size
- `display` changes

---

## 6. Compositing

Modern browsers split content into **compositor layers** that can be moved/transformed by the **GPU** without touching the CPU paint pipeline.

**GPU-accelerated properties (no reflow, no repaint):**
- `transform: translateX()`
- `opacity`
- `filter`

These only trigger the **composite** stage — the GPU just moves the pre-painted layer. This is why `transform` animations are smooth at 60fps while `left`/`top` animations stutter.

**`will-change: transform`** — hints to browser to promote element to its own compositor layer ahead of time. Use sparingly — each layer consumes GPU memory.

---

## 7. Event Loop, Microtasks vs Macrotasks

### The Event Loop
JavaScript is single-threaded. The event loop coordinates:
1. **Call Stack** — currently executing code
2. **Task Queue (Macrotask Queue)** — setTimeout, setInterval, I/O, UI events
3. **Microtask Queue** — Promise callbacks, queueMicrotask, MutationObserver
4. **Render Pipeline** — requestAnimationFrame, layout, paint

### Execution Order (one loop iteration):
```
1. Execute one macrotask (e.g. script, setTimeout callback)
2. Drain entire microtask queue (ALL microtasks run before next macrotask)
3. Render update (if needed — browser decides)
4. Back to step 1
```

### Key Implications
```js
console.log('1');
setTimeout(() => console.log('2'), 0);  // macrotask
Promise.resolve().then(() => console.log('3'));  // microtask
console.log('4');
// Output: 1, 4, 3, 2
```

**Microtasks run before the next render** — this means:
- Long microtask chains can delay paint
- `await` in async functions creates microtask checkpoints

### requestAnimationFrame
- Runs AFTER microtasks, BEFORE paint
- Correct place for DOM mutations that need to sync with render cycle
- ~16.7ms budget at 60fps

### Long Tasks & Jank
Any task > 50ms is a "long task" (Lighthouse flags these). They block the main thread and cause dropped frames. Solutions:
- `setTimeout(fn, 0)` to yield to event loop between chunks
- `scheduler.yield()` (new API)
- Move heavy work to Web Workers

---

## Key Takeaways for Development
1. **CSS before JS** in `<head>` — CSSOM needed before scripts run
2. **Defer/async scripts** — never block parser
3. **Batch DOM writes** — avoid FSL loops
4. **Animate with transform/opacity** — GPU compositing, no reflow
5. **Use will-change sparingly** — layer memory cost
6. **Keep tasks < 50ms** — yield with setTimeout or scheduler.yield
7. **Preload critical resources** — fonts, hero images, critical CSS

---
_Sources: MDN Web Docs, web.dev, Chrome DevTools documentation, HTML Living Standard_
