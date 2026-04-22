# WebAssembly & Low-Level Web
_Research compiled: 2026-04-22_

---

## 1. How WebAssembly Works

WebAssembly (WASM) is a **binary instruction format** for a stack-based virtual machine. It runs in browsers (and Node.js, Deno, edge runtimes) at near-native speed.

### Key Properties
- **Binary format** — compact, fast to decode (faster than parsing JS)
- **Stack machine** — instructions operate on a virtual stack
- **Sandboxed** — strict memory isolation, no direct OS access
- **Typed** — statically typed (`i32`, `i64`, `f32`, `f64`, `v128`)
- **Linear memory** — flat byte array, WASM code can only touch its own memory
- **Deterministic** — same input → same output, no undefined behavior
- **Language-agnostic** — compile from C, C++, Rust, Go, Zig, AssemblyScript, etc.

### WASM in the Browser
WASM runs in the same JS engine (V8, SpiderMonkey) but in a separate module:
```
Source (C++/Rust) → WASM binary (.wasm)
                        ↓
JS: WebAssembly.instantiateStreaming(fetch('lib.wasm'))
                        ↓
    WASM module exposed as JS-callable functions
```

### Memory Model
WASM has a **linear memory** — a contiguous block of bytes accessed via indices:
```js
// Allocate 1 page (64KB) of memory
const memory = new WebAssembly.Memory({ initial: 1 });
const buf = new Uint8Array(memory.buffer);
// Both JS and WASM can read/write this shared buffer
```

---

## 2. Compiling & Interfacing with JavaScript

### Rust → WASM (Most Ergonomic Path)
```rust
// lib.rs
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn fibonacci(n: u32) -> u32 {
    match n {
        0 => 0,
        1 => 1,
        _ => fibonacci(n-1) + fibonacci(n-2),
    }
}
```

```bash
# Install tools
cargo install wasm-pack
# Build
wasm-pack build --target web
```

```js
// Use in browser
import init, { fibonacci } from './pkg/mylib.js';
await init();
console.log(fibonacci(40)); // ~3x faster than pure JS
```

### C/C++ → WASM (Emscripten)
```bash
# Compile
emcc mylib.c -O3 -o mylib.js -s EXPORTED_FUNCTIONS="['_my_function']"
```

### Data Passing: The Bridge Cost
JS ↔ WASM boundary crossing has overhead. Numbers are cheap; complex data costs:
```js
// CHEAP — passing numbers
const result = wasmModule.exports.add(1, 2);

// EXPENSIVE — passing strings (must copy to WASM linear memory)
const str = "hello";
const ptr = wasmModule.exports.allocate(str.length);
const mem = new Uint8Array(wasmModule.exports.memory.buffer);
new TextEncoder().encodeInto(str, mem.subarray(ptr));
const result = wasmModule.exports.processString(ptr, str.length);
wasmModule.exports.free(ptr);
```

With `wasm-bindgen` (Rust) or Emscripten's Embind, this boilerplate is auto-generated.

### WASM Component Model (Emerging Standard)
Allows WASM modules from different languages to call each other with rich types — solving the data passing friction. Still maturing.

---

## 3. When to Use WASM vs Not

### Use WASM When:
- **CPU-intensive computation** — image/video processing, audio codecs, physics simulation
- **Porting existing C/C++ code** — game engines (Doom, Unity), codecs (ffmpeg), scientific libs
- **Consistent performance** — avoiding JS JIT deoptimizations
- **Cryptography** — constant-time implementations (prevent timing attacks)
- **Code reuse** — share library between native + web

### Real-World WASM Use Cases
- **Figma** — rendering engine in Rust/WASM (critical path perf)
- **Google Earth** — C++ codebase compiled to WASM
- **Autodesk AutoCAD** — CAD engine in WASM
- **SQLite in the browser** — `sql.js` (C→WASM)
- **Video transcoding** — ffmpeg.wasm
- **Image processing** — Squoosh (Google's image optimizer uses WASM codecs)

### Don't Use WASM When:
- **DOM manipulation** — WASM can't access DOM directly; every DOM op goes through JS bridge
- **Simple string operations** — JS string handling is highly optimized
- **Async I/O** — WASM doesn't have native async (though WASI is adding it)
- **Startup-critical code** — WASM download + compile time; use JS for initial render
- **Small utility functions** — JS call overhead makes WASM slower for tiny operations

### Performance Expectations
WASM is typically:
- **10-20% slower than native** compiled C (JIT + memory model overhead)
- **1.5-3x faster than JS** for compute-intensive tasks
- **Faster than JS** for predictable, hot, type-stable code
- **Possibly slower than JS** for DOM-heavy work (bridge cost dominates)

---

## 4. WASM Beyond the Browser

### WASI (WebAssembly System Interface)
Standard API for WASM outside the browser:
- File system access, network sockets, random, clock
- Capability-based security — explicitly grant permissions
- Runtime-agnostic: Wasmtime, WasmEdge, WAMR

### WASM at the Edge
Cloudflare Workers, Fastly Compute@Edge run WASM modules:
```rust
// Cloudflare Worker in Rust → WASM
use worker::*;
#[event(fetch)]
pub async fn main(req: Request, env: Env, _ctx: Context) -> Result<Response> {
    Response::ok("Hello from WASM edge!")
}
```
Benefits over Node.js workers:
- Microsecond cold starts (vs 50-400ms for Node containers)
- Smaller memory footprint (share memory, not full V8 instance)
- True isolation (each WASM module sandboxed)

### WASM Threads & SIMD
- **Threads** (SharedArrayBuffer + `wasm32-unknown-unknown` + Atomics) — shared memory parallelism
- **SIMD** (Single Instruction, Multiple Data) — process multiple values at once
  ```wasm
  ;; v128 SIMD — add 4 floats at once
  v128.add f32x4
  ```
  Used in image processing, ML inference for significant speedups.

---

## Key Takeaways
1. **WASM is not a JS replacement** — it's a complement for CPU-intensive work
2. **Best candidates**: image/video processing, crypto, physics, ported C/C++ libs
3. **Minimize bridge crossings** — batch data, avoid per-pixel JS↔WASM calls
4. **Rust + wasm-bindgen** — best developer experience for new WASM code
5. **Profile first** — WASM isn't always faster; measure before migrating
6. **Edge WASM** (Cloudflare Workers) — microsecond cold starts, great for middleware
7. **WASI** — watch this space; WASM is becoming a universal compute substrate

---
_Sources: WebAssembly specification, MDN WASM docs, Lin Clark's WASM cartoons, Rust WASM book, Cloudflare Workers docs_
