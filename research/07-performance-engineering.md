# Performance Engineering
_Research compiled: 2026-04-22_

---

## 1. Core Web Vitals (Google's User Experience Metrics)

### The Three Core Vitals
| Metric | What It Measures | Good | Needs Work | Poor |
|---|---|---|---|---|
| **LCP** (Largest Contentful Paint) | Load speed — when main content appears | < 2.5s | 2.5-4s | > 4s |
| **INP** (Interaction to Next Paint) | Responsiveness — delay from click to visual response | < 200ms | 200-500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | Visual stability — how much layout shifts unexpectedly | < 0.1 | 0.1-0.25 | > 0.25 |

**INP replaced FID (First Input Delay) in March 2024.**

### LCP Optimization
LCP element is usually: hero image, large text block, video poster.

```
LCP breakdown:
├── Time to First Byte (TTFB) — server response time
├── Resource load delay — when LCP resource starts loading
├── Resource load time — how long it takes to load
└── Element render delay — time from loaded to painted
```

Fixes:
- `<link rel="preload" as="image" href="hero.jpg">` — start fetching LCP image ASAP
- Use CDN — reduce TTFB
- Optimize images: WebP/AVIF, proper sizing, no oversized images
- Remove render-blocking resources before LCP element

### CLS Optimization
Common causes:
- Images/videos without `width`/`height` attributes → browser doesn't know size before load
- Ads/embeds inserted dynamically above content
- Web fonts causing FOIT/FOUT → text relayout

Fixes:
```html
<!-- Always set dimensions -->
<img src="hero.jpg" width="800" height="600" alt="">
<!-- Or use aspect-ratio CSS -->
<style>.hero { aspect-ratio: 4/3; }</style>

<!-- Reserve space for dynamic content -->
<div style="min-height: 250px"><!-- ad goes here --></div>

<!-- font-display: optional prevents FOUT for non-critical fonts -->
@font-face { font-display: swap; }
```

### INP Optimization
- Keep event handlers fast (< 50ms total)
- Defer non-critical work: `setTimeout(fn, 0)` or `scheduler.yield()`
- Avoid synchronous layout reads in handlers
- Use `requestAnimationFrame` for visual updates

---

## 2. Profiling & Benchmarking

### Chrome DevTools Performance Panel
1. Record a trace during interaction
2. Key things to look for:
   - **Long tasks** (red bar in Main thread) — > 50ms blocks main thread
   - **Layout/Reflow** — watch for purple "Layout" blocks triggered repeatedly
   - **Forced Synchronous Layout** — red warning in timeline
   - **Scripting** — JS parse + execute time
   - **Rendering** — style + layout
   - **Painting** — pixel painting
   - **Composite Layers** — GPU

### JavaScript Profiling
```js
// Browser built-in
console.time('myOperation');
doExpensiveWork();
console.timeEnd('myOperation');

// More precise
const start = performance.now();
doWork();
const duration = performance.now() - start;

// User Timing API (shows in DevTools traces)
performance.mark('workStart');
doWork();
performance.mark('workEnd');
performance.measure('work', 'workStart', 'workEnd');
```

### Node.js Profiling
```bash
# V8 built-in profiler
node --prof app.js
node --prof-process isolate-*.log

# Clinic.js (best tool for Node perf)
npx clinic doctor -- node app.js
npx clinic flame -- node app.js    # flamegraph
npx clinic bubbleprof -- node app.js  # async profiling
```

### Python Profiling
```python
import cProfile, pstats
with cProfile.Profile() as pr:
    my_function()
stats = pstats.Stats(pr)
stats.sort_stats('cumulative')
stats.print_stats(20)
```

---

## 3. Memory Leaks & Long Tasks

### Detecting Memory Leaks in Browser
1. Chrome DevTools → Memory → Take Heap Snapshot
2. Do action that should not leak memory
3. Take another snapshot
4. Compare — look for growing object counts
5. "Detached DOM nodes" — removed from DOM but JS still holds reference

### Detecting Memory Leaks in Node.js
```bash
# Enable heap snapshots on demand
node --inspect app.js
# In DevTools → Memory → Take Heap Snapshot

# Or programmatically
const v8 = require('v8');
const snap = v8.writeHeapSnapshot();
```

### Long Task Detection
```js
// PerformanceObserver for long tasks
const observer = new PerformanceObserver((list) => {
  list.getEntries().forEach(entry => {
    console.warn(`Long task: ${entry.duration.toFixed(2)}ms`);
    // entry.attribution tells you where it came from
  });
});
observer.observe({ entryTypes: ['longtask'] });
```

### Breaking Up Long Tasks
```js
// BAD — single long task
function processItems(items) {
  items.forEach(item => expensiveProcess(item));
}

// GOOD — yield to event loop between chunks
async function processItems(items) {
  const CHUNK_SIZE = 50;
  for (let i = 0; i < items.length; i += CHUNK_SIZE) {
    const chunk = items.slice(i, i + CHUNK_SIZE);
    chunk.forEach(item => expensiveProcess(item));
    await scheduler.yield();  // or: await new Promise(r => setTimeout(r, 0));
  }
}
```

---

## 4. Lighthouse & Performance Tools

### Lighthouse Scoring
Composite score 0-100 from weighted metrics:
- LCP: 25%
- INP: 10% (as of 2024)
- CLS: 15%
- FCP: 10%
- Time to Interactive: 10%
- Speed Index: 10%
- Total Blocking Time: 30%

**Run Lighthouse:**
```bash
npx lighthouse https://mysite.com --output html --output-path report.html
# Or Chrome DevTools → Lighthouse tab
```

### Other Tools
- **WebPageTest** (webpagetest.org) — real browsers, real locations, waterfall charts
- **PageSpeed Insights** — Google's tool using real Chrome User Experience Report (CrUX) data
- **Chrome UX Report** — real field data from Chrome users
- **Core Web Vitals in Search Console** — your site's real-user CWV data

### Key Lighthouse Opportunities
| Opportunity | What to do |
|---|---|
| Eliminate render-blocking resources | defer/async scripts, inline critical CSS |
| Properly size images | responsive images, correct format |
| Defer offscreen images | lazy loading (`loading="lazy"`) |
| Remove unused CSS/JS | tree shaking, code splitting |
| Enable text compression | gzip/brotli on server |
| Serve images in next-gen formats | WebP, AVIF |
| Reduce initial server response time | CDN, DB optimization, caching |

---

## 5. Image Optimization (Huge Win)

```html
<!-- Responsive images -->
<picture>
  <source srcset="hero.avif" type="image/avif">
  <source srcset="hero.webp" type="image/webp">
  <img src="hero.jpg" width="800" height="600"
       loading="lazy"
       decoding="async"
       alt="Hero image">
</picture>

<!-- For LCP image: preload + fetchpriority -->
<link rel="preload" as="image" href="hero.avif" fetchpriority="high">
<img src="hero.avif" fetchpriority="high" loading="eager">
```

Format comparison: `AVIF > WebP > JPEG` for quality/size ratio.

---

## Key Takeaways
1. **Measure first** — profile before optimizing. Gut instinct is often wrong.
2. **LCP is most impactful** — preload hero image, CDN, optimize TTFB
3. **Always set image dimensions** — eliminates CLS
4. **Keep event handlers < 50ms** — yield with scheduler.yield for long work
5. **Break long tasks** — chunk work, yield to event loop
6. **Lighthouse CI** — run in CI pipeline, fail builds on performance regression
7. **Use WebP/AVIF** — 30-50% smaller than JPEG at same quality

---
_Sources: web.dev/vitals, Chrome DevTools docs, Lighthouse docs, WebPageTest docs_
