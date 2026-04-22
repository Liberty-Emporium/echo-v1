# Compilers & Build Systems
_Research compiled: 2026-04-22_

---

## 1. How Bundlers Work

### The Problem Bundlers Solve
- Browsers historically required one file per module request (HTTP/1.1 cost)
- Node.js modules (require/CommonJS) don't run natively in browsers
- Need transformation: TypeScript → JS, JSX → JS, SCSS → CSS

### Bundler Pipeline
```
Source files (TS, JSX, CSS, images)
    ↓
Parse → AST (Abstract Syntax Tree)
    ↓
Transform (TypeScript → JS, JSX → JS, etc.)
    ↓
Dependency Graph construction
    ↓
Bundle (combine modules)
    ↓
Optimize (tree shaking, minification, dead code elimination)
    ↓
Output (dist/bundle.js, dist/bundle.css)
```

### Major Bundlers Comparison
| Bundler | Language | Speed | Config | Best For |
|---|---|---|---|---|
| **Webpack** | JS/Node | Medium | Complex | Large enterprise apps, maximum ecosystem |
| **Vite** | JS (Rollup/esbuild) | Very Fast | Simple | Modern apps, dev experience |
| **esbuild** | Go | Blazing Fast | Minimal | Libraries, tooling, speed priority |
| **Rollup** | JS | Fast | Medium | Libraries (cleaner output) |
| **Parcel** | Rust/JS | Fast | Zero-config | Simple projects, zero-config |
| **Turbopack** | Rust | Blazing | Webpack-compatible | Next.js (replaces Webpack) |

### Webpack Key Concepts
```js
// webpack.config.js
module.exports = {
  entry: './src/index.js',        // where to start building dependency graph
  output: { path: dist, filename: '[name].[contenthash].js' },
  module: {
    rules: [
      { test: /\.tsx?$/, use: 'ts-loader' },  // loaders transform files
      { test: /\.css$/, use: ['style-loader', 'css-loader'] },
    ]
  },
  plugins: [new HtmlWebpackPlugin({ template: './src/index.html' })],
  optimization: { splitChunks: { chunks: 'all' } }  // code splitting
};
```

---

## 2. Tree Shaking

Eliminates dead code — imports that are defined but never used:

```js
// utils.js
export function usedFunction() { return 'used'; }
export function unusedFunction() { return 'never called'; }

// main.js
import { usedFunction } from './utils';
usedFunction();
// After tree shaking: unusedFunction is NOT in the bundle
```

**Requirements for tree shaking:**
1. **ES Modules** (`import`/`export`) — CommonJS (`require`) is NOT tree-shakeable
2. **Pure functions** — side-effect-free (bundler must know removing it is safe)
3. **`sideEffects: false`** in package.json — tells bundler the whole package is side-effect free

**Pitfall: barrel files (index.js re-exports)**
```js
// utils/index.js — re-exports everything
export * from './string-utils';
export * from './math-utils';   // 50KB
export * from './date-utils';   // 30KB

// main.js
import { formatDate } from './utils';
// Bundler may include all utils if not configured correctly
// FIX: import directly: import { formatDate } from './utils/date-utils'
```

---

## 3. Code Splitting

Instead of one huge bundle, split into chunks loaded on demand:

### Route-based splitting (React)
```jsx
import { lazy, Suspense } from 'react';
const Dashboard = lazy(() => import('./Dashboard'));  // dynamic import = separate chunk
const Settings = lazy(() => import('./Settings'));

function App() {
  return (
    <Suspense fallback={<Spinner />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```

### Vendor splitting
Separate vendor chunk (React, lodash) from app code:
```js
// webpack
optimization: {
  splitChunks: {
    cacheGroups: {
      vendor: {
        test: /node_modules/,
        name: 'vendors',
        chunks: 'all'
      }
    }
  }
}
```
**Why:** vendor bundle changes rarely → long cache TTL. App bundle changes often → short TTL.

---

## 4. AST Parsing & Transformations

The AST (Abstract Syntax Tree) is the parsed representation of source code:

```js
// Source code: const x = 1 + 2;

// AST (simplified):
{
  type: "VariableDeclaration",
  declarations: [{
    type: "VariableDeclarator",
    id: { type: "Identifier", name: "x" },
    init: {
      type: "BinaryExpression",
      operator: "+",
      left:  { type: "Literal", value: 1 },
      right: { type: "Literal", value: 2 }
    }
  }]
}
```

### AST Tools
- **acorn** / **@babel/parser** — parse JS to AST
- **estree** — standard AST format for JS
- **@babel/traverse** — walk the AST
- **@babel/generator** — convert AST back to code
- **ast-types** — type-safe AST manipulation
- **astexplorer.net** — interactive AST explorer (essential tool)

### Writing a Babel Plugin (Transform Example)
Remove console.log calls from production:
```js
// babel-plugin-remove-console.js
module.exports = function({ types: t }) {
  return {
    visitor: {
      CallExpression(path) {
        if (
          t.isMemberExpression(path.node.callee) &&
          t.isIdentifier(path.node.callee.object, { name: 'console' })
        ) {
          path.remove();  // delete the node
        }
      }
    }
  };
};
```

### Codemods (Automated Code Migration)
```js
// jscodeshift codemod: rename function foo → bar
module.exports = function(fileInfo, api) {
  const j = api.jscodeshift;
  return j(fileInfo.source)
    .find(j.Identifier, { name: 'foo' })
    .replaceWith(j.identifier('bar'))
    .toSource();
};
// Run: npx jscodeshift -t rename-codemod.js src/
```

---

## 5. Writing a Simple Compiler/Transpiler

A minimal transpiler has 3 phases:

### Phase 1: Lexer (Tokenizer)
```python
# Tokenize: "3 + 4 * 2"
def tokenize(source):
    tokens = []
    i = 0
    while i < len(source):
        if source[i].isdigit():
            j = i
            while j < len(source) and source[j].isdigit():
                j += 1
            tokens.append(('NUMBER', int(source[i:j])))
            i = j
        elif source[i] in '+-*/':
            tokens.append(('OP', source[i]))
            i += 1
        elif source[i] == ' ':
            i += 1
    return tokens
# [('NUMBER', 3), ('OP', '+'), ('NUMBER', 4), ('OP', '*'), ('NUMBER', 2)]
```

### Phase 2: Parser → AST
```python
# Recursive descent parser
def parse_expression(tokens, pos=0):
    left, pos = parse_term(tokens, pos)
    while pos < len(tokens) and tokens[pos][1] in '+-':
        op = tokens[pos][1]
        right, pos = parse_term(tokens, pos + 1)
        left = ('BinaryExpr', op, left, right)
    return left, pos
```

### Phase 3: Code Generator
```python
def codegen(node):
    if isinstance(node, tuple):
        kind = node[0]
        if kind == 'BinaryExpr':
            _, op, left, right = node
            return f"({codegen(left)} {op} {codegen(right)})"
    elif isinstance(node, int):
        return str(node)
```

This is exactly how Babel, TypeScript compiler, and all transpilers work at their core.

---

## 6. Modern Tooling Landscape

### Vite (Why It's Fast)
- **Dev mode**: no bundling — serves ES modules directly via native browser ESM
- Browser imports from dev server, Vite transforms on-demand
- Only transforms files the browser actually requests
- **Production**: uses Rollup for optimized bundle

### esbuild (Why It's 100x Faster than Webpack)
- Written in **Go** — native binary, not Node.js
- Parallelizes parsing, transformation, linking across all CPU cores
- No caching needed — fast enough to rebuild from scratch each time
- Does **not** do type checking — just strips types (pair with tsc for type safety)

### SWC (Rust-based JS Compiler)
- Drop-in Babel replacement
- 20-70x faster than Babel
- Used by Next.js, Parcel 2, Deno
- Also handles JSX, TypeScript, decorators

---

## Key Takeaways
1. **Use Vite for new projects** — best dev experience + fast builds
2. **Tree shaking requires ES Modules** — avoid CommonJS in libraries
3. **Code split at route boundaries** — lazy() for major routes
4. **Separate vendor chunks** — different cache strategies
5. **Learn AST** — understanding it unlocks codemods, custom linting, transforms
6. **astexplorer.net** — bookmark it, use it constantly
7. **esbuild/SWC** for tooling speed — use in custom build scripts
8. **`sideEffects: false`** in package.json for libraries you publish

---
_Sources: Webpack docs, Vite docs, Babel plugin handbook, esbuild docs, Crafting Interpreters (Nystrom), astexplorer.net_
