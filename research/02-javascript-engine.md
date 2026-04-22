# JavaScript Engine Deep Dive (V8 Focus)
_Research compiled: 2026-04-22_

---

## 1. How V8 Executes JavaScript

V8 is Google's JS engine (Chrome, Node.js, Deno). Its pipeline:

```
Source Code
    ↓
Parser → AST (Abstract Syntax Tree)
    ↓
Ignition (Interpreter) → Bytecode
    ↓ (hot code detected via profiling)
TurboFan (Optimizing JIT Compiler) → Optimized Machine Code
    ↓ (deoptimization if assumptions violated)
Back to Ignition
```

### Ignition (Interpreter)
- Converts AST → **bytecode** (compact intermediate representation)
- Executes bytecode directly — fast startup, lower memory than compiling everything
- Collects **type feedback** while running (which types flow through which operations)

### TurboFan (JIT Compiler)
- Kicks in for **hot functions** (called many times)
- Uses type feedback to make **speculative optimizations**:
  - If a function always receives integers → compile int-optimized version
  - If it suddenly receives a string → **deoptimize** back to interpreted bytecode
- Generates highly optimized machine code for the specific hardware

### Hidden Classes (Shapes)
V8 tracks object structure with **hidden classes** to optimize property access:

```js
// GOOD — same hidden class, V8 optimizes
function Point(x, y) { this.x = x; this.y = y; }
const p1 = new Point(1, 2);
const p2 = new Point(3, 4);

// BAD — different hidden classes, deoptimizes
const a = { x: 1, y: 2 };
const b = { y: 2, x: 1 };  // different property order = different hidden class
```

**Always initialize object properties in the same order** — V8 can share the hidden class.

### Inline Caching (IC)
V8 caches the result of property lookups at call sites:
- **Monomorphic** — always same type → fastest
- **Polymorphic** — 2-4 types → still fast
- **Megamorphic** — 5+ types → cache abandoned, slow path

---

## 2. Memory Management & Garbage Collection

### V8 Heap Structure
```
V8 Heap
├── New Space (Young Generation) — ~1-8MB, short-lived objects
│   ├── Nursery (from-space)
│   └── Intermediate (to-space)
└── Old Space (Old Generation) — larger, long-lived objects
    ├── Old Object Space
    ├── Code Space (compiled code)
    ├── Map Space (hidden classes)
    └── Large Object Space (>256KB)
```

### Minor GC (Scavenge) — New Space
- Very fast (~1ms)
- **Copying collector** — live objects copied from nursery → intermediate → old space
- Objects that survive 2 scavenges are promoted to Old Space
- Runs frequently

### Major GC (Mark-Sweep-Compact) — Old Space
- **Mark phase**: traverse object graph from roots (stack, globals), mark reachable objects
- **Sweep phase**: reclaim unreachable objects
- **Compact phase**: defragment memory (optional, expensive)
- V8 uses **incremental marking** — breaks marking into small steps to avoid long pauses
- **Concurrent marking** — marking happens on background thread while JS runs

### What Causes Memory Leaks
1. **Forgotten event listeners**
   ```js
   // LEAK — listener holds reference to element, prevents GC
   const btn = document.getElementById('btn');
   btn.addEventListener('click', handler);
   // Never removed — even if btn is removed from DOM
   // FIX: btn.removeEventListener('click', handler) or use AbortController
   ```

2. **Detached DOM nodes**
   ```js
   let detached;
   function createLeak() {
     const el = document.createElement('div');
     detached = el; // reference kept after removal from DOM
     document.body.removeChild(el);
   }
   ```

3. **Closures capturing large objects**
   ```js
   function outer() {
     const hugeData = new Array(1000000);
     return function inner() {
       // even if inner never uses hugeData, it's in scope → kept alive
       return 'result';
     }
   }
   ```

4. **Global variables** — never collected
5. **Timers not cleared** — `setInterval` holds reference to callback and its closure

### WeakRef & FinalizationRegistry (ES2021)
```js
const ref = new WeakRef(bigObject);
// ... later
const obj = ref.deref(); // null if GC'd
if (obj) { /* use it */ }
```
Allows holding references without preventing GC.

---

## 3. Closures, Scopes & Execution Contexts

### Execution Context
Every time code runs, an execution context is created:
- **Global Execution Context** — one per program, `this` = window/global
- **Function Execution Context** — one per function call
- **Eval Execution Context** — rare

Each context has:
1. **Variable Environment** — `var` declarations, function declarations
2. **Lexical Environment** — `let`, `const`, block scope
3. **`this` binding**
4. **Outer environment reference** — link to enclosing scope (forms scope chain)

### The Scope Chain
When a variable is referenced:
1. Check current execution context's lexical environment
2. Follow outer reference up the chain
3. Reach global — if not found → ReferenceError

```js
const x = 'global';
function outer() {
  const x = 'outer';
  function inner() {
    console.log(x); // 'outer' — found in outer's scope via chain
  }
  inner();
}
```

### Closures
A closure = a function + its lexical environment (the scope chain at time of creation).

```js
function makeCounter() {
  let count = 0;          // lives in makeCounter's LE
  return {
    inc: () => ++count,   // closure over count
    get: () => count,
  };
}
const c = makeCounter();
c.inc(); c.inc();
console.log(c.get()); // 2
```

V8 optimizes closures — only variables actually referenced by inner functions are kept in the **context object** (heap-allocated). Others stay on the stack.

### `var` vs `let`/`const`
- `var` — function-scoped, hoisted (declaration only, not init), goes on Variable Environment
- `let`/`const` — block-scoped, temporal dead zone (TDZ) until declaration, Lexical Environment

---

## 4. Async Internals — Promises & async/await Under the Hood

### Promises
A Promise is an object with internal state: `pending` → `fulfilled` | `rejected`.

```
Promise.resolve(val)
    ↓
.then(callback) — schedules callback as MICROTASK when resolved
```

**The crucial part**: `.then()` callbacks are always async — they go into the **microtask queue**, never run synchronously even if the promise is already resolved.

```js
const p = Promise.resolve(42);
p.then(v => console.log('then:', v)); // async microtask
console.log('sync');
// Output: 'sync', then: 42
```

### async/await Desugaring
`async/await` is syntactic sugar over Promises + generator-style control flow:

```js
async function fetchData() {
  const res = await fetch(url);  // suspends here
  return res.json();
}

// Roughly equivalent to:
function fetchData() {
  return fetch(url).then(res => res.json());
}
```

**What `await` actually does:**
1. Evaluates the expression to the right
2. Wraps it in `Promise.resolve()` if not already a Promise
3. **Suspends the async function** (saves execution context)
4. Returns control to the caller
5. When promise resolves → schedules resumption as **microtask**

**Cost of await**: Each `await` = at minimum 1 microtask tick. In tight loops, this adds up.

```js
// SLOW — sequential, each await waits for previous
async function slow() {
  const a = await fetchA();
  const b = await fetchB(); // waits for A to finish first
}

// FAST — parallel
async function fast() {
  const [a, b] = await Promise.all([fetchA(), fetchB()]);
}
```

### Unhandled Promise Rejections
```js
// Crashes Node.js process in modern versions!
async function bad() { throw new Error('oops'); }
bad(); // no .catch(), no try/catch around await

// Always handle:
bad().catch(err => console.error(err));
// or
try { await bad(); } catch(e) { console.error(e); }
```

### Promise.allSettled vs Promise.all
- `Promise.all` — fails fast on first rejection
- `Promise.allSettled` — waits for all, returns array of `{status, value/reason}`
- `Promise.race` — resolves/rejects with first settled promise
- `Promise.any` — resolves with first fulfilled (ignores rejections)

---

## Key Takeaways for Writing Better Code
1. **Consistent object shapes** — same property init order, same constructor
2. **Avoid megamorphic call sites** — don't mix types through the same function
3. **Remove event listeners** — use AbortController for easy bulk cleanup
4. **Avoid closure-captured large objects** — break closures up
5. **Parallel async with Promise.all** — not sequential awaits
6. **Always handle rejections** — unhandled rejections crash Node
7. **Microtasks over macrotasks** — for chained async work, Promise chains are faster than setTimeout

---
_Sources: V8 blog (v8.dev), Node.js docs, ECMAScript specification, Jake Archibald's event loop talk_
