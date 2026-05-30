# Web Development Mastery — Change Log

> Auto-daily research updates by OWL for Liberty Emporium.

---

## 2026-05-30 — Design Systems Update (Run 1: Material 3, Apple HIG, Fluent UI)

### Material Design 3 — M3 Expressive
- **M3 Expressive** is the latest evolution of Google's Material Design 3, introduced at Google I/O 2026
- **14 new and updated expressive components**: Toolbars, Split Button, Progress Indicators (with customizable waveform), Button Groups (shape-shifting buttons that react to each other)
- **Motion Physics**: New spring-based motion system replacing fixed easing curves — powered by design tokens, easier to implement, more customizable transitions
- **Expanded Shape Library**: 35 new shapes for decorative visual elements, with built-in shape morph motion
- **Color**: Vibrant, expressive color palettes driven by emotion-driven UX principles
- **Typography**: Flexible typography with Google Sans Flex variable font
- **Figma M3 Design Kit** updated with all Expressive components and styles
- **Material at Google I/O 2026**: Material Android is now Compose-first
- **Adaptive components**: Components adapt to different form factors and usage contexts
- Key themes: emotion-driven UX, expressive shapes, vibrant colors, spring physics motion

### Apple Human Interface Guidelines — Liquid Glass
- **Liquid Glass** is Apple's new material system (iOS 26 / macOS 26 era), replacing the previous vibrancy/frosted glass approach
- Updated guidance across: Materials, Buttons, Toolbars, Tab Bars, Color, Motion for Liquid Glass
- Updated for **new products**: iPhone 17, iPhone Air, iPhone 17 Pro, Apple Watch Series 11, Apple Watch Ultra 3
- **visionOS**: Added Look to Scroll, Figma design kit, spatial photos/scenes guidance
- **Typography**: Added emphasized weights to Dynamic Type style specifications per platform
- **Design principles**: Hierarchy, Harmony (concentric design with hardware/software), Consistency
- **"Adopting Liquid Glass"** is the developer guidance reference
- New & updated topics: Multitasking, Menu Bar, Toolbars, Search Fields, Game Center, Generative AI guidance

### Microsoft Fluent UI 2
- Fluent 2 continues as Microsoft's cross-platform design system (Web, iOS, Android, Windows)
- **AI integration**: Dedicated "Working with AI" section in the design system — patterns for AI-assisted interfaces
- **Web tokens**: Design token system for consistent theming across platforms
- **Teams**: Major redesign leveraging Fluent 2 to boost performance and reduce complexity
- **Outlook**: Modern redesign uniting Windows and Fluent for a customizable hub experience
- **Accessibility tools**: A11y Focus Order annotation, Color Contrast Checker
- **Design resources**: Content Reel, Icon Scaling Tool, Figma UI kits
- Emphasis on tokens, component consistency, and AI-augmented workflows

### Design System Trends (Cross-Industry)
- **AI-augmented design**: All three major design systems now incorporate AI patterns — Figma has a Design Agent (on-canvas), Fluent has "Working with AI", Apple added Generative AI guidance
- **Expressive/emotional design**: Moving beyond flat/minimal — vibrant colors, shape morphing, spring physics, personality
- **Token-driven everything**: Design tokens for motion, shape, color, typography — enabling systematic theming
- **Lean design-system teams**: NN/G reports small, strategic design-system teams can scale impact beyond their size
- **CSS advancing**: `contrast-color()`, `sibling-index()`, `sibling-count()`, `::checkmark`, HTML Anchor Positioning — reducing need for JS in accessible layouts
- **Prototype honesty**: NN/G emphasizes making prototypes more honest representations to avoid misleading stakeholders

---

## 2026-06-10 — Initial Knowledge Base

- [StackShare] Top tech stacks: Uber (Go/React), Airbnb (Rails/React), Django/React most common
- [StackShare] Shopify uses Go + React + K8s, Instagram uses Django + React Native
- [GitHub Trending] Most starred: build-your-own-x (507k), freeCodeCamp (445k), nlohmann/json (49k)
- [DEV Community] Best backend frameworks 2025: FastAPI, Django, Express, NestJS, Spring Boot
- [DEV Community] Best React frameworks 2025: Next.js, Remix, Gatsby, Astro, TanStack Start
- [DEV Community] Best Node.js frameworks 2025: Express, NestJS, Hono, Elysia, Koa
- [roadmap.sh] Frontend roadmap stable: HTML → CSS → JS → React/Vue → Testing → Performance
- [Industry] Next.js 15+ stable with App Router, Server Actions, Partial Prerendering
- [Industry] React 19 stable with Server Components, use() hook, improved Suspense
- [Industry] Tailwind CSS v4 in alpha — better performance, CSS-first config
- [Industry] shadcn/ui becoming default component library pattern for new projects
- [Industry] Supabase growing as Firebase alternative (Postgres + Auth + Realtime)
- [AI Integration] FastAPI + OpenRouter is our recommended AI app stack
- [AI Integration] RAG patterns: pgvector (Postgres) or Chroma for vector search
- [Design] Bento grids, glassmorphism, dark mode first are dominant 2025 trends

---

## 2026-05-30 — Run 1: Frontend Framework Ecosystem Updates

### Next.js 16.2 (March 2026)
- **~400% faster dev startup**: `next dev` startup is ~87% faster compared to 16.1
- **~50% faster rendering**: React Server Components payload deserialization up to 350% faster via new two-step JSON.parse approach
- **Turbopack improvements**: Server Fast Refresh, Subresource Integrity support, tree shaking of dynamic imports, 200+ bug fixes
- **AI/agent improvements**: `create-next-app` now generates `AGENTS.md`, browser log forwarding to terminal, experimental Agent DevTools (`next-browser`)
- **Dev experience**: Redesigned 500 error page, hydration diff indicator, Server Function logging in dev terminal, `--inspect` flag for `next start`

### Next.js Across Platforms: Adapter API (March 2026)
- **Stable Adapter API**: Typed, versioned build output description that any platform can target
- **Shared test suite**: Correctness tests for every adapter, including Vercel's
- **Multi-platform collaboration**: Built with OpenNext, Netlify, Cloudflare, AWS Amplify, Google Cloud
- **Verified adapters**: Open-source, community-owned adapters under the Next.js org
- **Ecosystem Working Group**: Standing forum for coordinating changes across providers

### Vercel: Agentic Infrastructure (April 2026)
- **30% of deployments now agent-initiated** (up 1000% from 6 months ago)
- Claude Code = 75% of agent deployments, Lovable/v0 = 6%, Cursor = 1.5%
- **AI SDK 6** adds agent abstraction layer
- **Vercel's agent stack**: AI SDK, Chat SDK, AI Gateway, Fluid Compute, Workflows/Queues, Sandbox, Observability
- Agent-deployed projects are **20x more likely** to call AI inference provider than human-deployed
- Vision: "Infrastructure that is itself agentic" — platform auto-investigates anomalies, performs root-cause analysis

### Svelte: May 2026 Updates
- **SvelteKit supports TypeScript 6.0** (v2.56.0)
- **Svelte CLI Community Add-ons**: Experimental community plugin system for `npx sv`
- **Remote functions improvements**: `field.as(type, default)` for form defaults, hydratable transport for richer data types
- **Svelte featured in ThoughtWorks Technology Radar**
- **Integrated observability**: SvelteKit apps can now emit OpenTelemetry traces via `instrumentation.server.ts`
- New community tools: Blossom Color Picker, sveltednd, phantom-ui, Svelte Spell UI, Motion Core, Stately, Sveltia I18n

### Vue.js Ecosystem
- **Vue 3.5** latest stable release
- **VitePress 1.0** released (Vue-powered static site generator)
- Vue 2 reached End of Life — migration to Vue 3 is critical
- Volar (Vue language tools) at 1.0 "Nika"

### Tailwind CSS v4.3 (May 2026)
- **First-party scrollbar styling** utilities
- **More logical property utilities** for RTL/LTR support
- **New zoom and tab-size utilities**
- **Better @variant support**
- Tailwind Plus now includes **vanilla JavaScript support** for UI blocks (dialogs, dropdowns, command palettes)

### GitHub Trending (May 30, 2026)
- **MoneyPrinterTurbo** (70.6k ⭐, +3,567 today): AI-powered short video generation
- **microsoft/markitdown** (130.6k ⭐, +1,873 today): Convert files/office docs to Markdown
- **EveryInc/compound-engineering-plugin** (18.2k ⭐): Claude Code/Codex/Cursor plugin
- **twentyhq/twenty** (48.5k ⭐): Open-source Salesforce alternative, AI-designed
- **anthropics/claude-code** (128k ⭐): Agentic coding tool in terminal
- **Leonxlnx/taste-skill** (28.5k ⭐, +2,062 today): AI quality/skill plugin
- **cursor/plugins** (1.3k ⭐): Cursor plugin spec and official plugins
- **run-llama/liteparse** (7.5k ⭐): Fast open-source document parser

### Hacker News Top Stories (May 30, 2026)
1. "The dead economy theory" (948 points, 1096 comments)
2. "SQLite is all you need for durable workflows" (499 points, 252 comments)
3. "Notes from the Mistral AI Now Summit" (357 points, 142 comments)
4. "Shift will clean homes for free to train future robots" (129 points)
5. "MCP is dead?" (200 points, 176 comments)

### Key Industry Trends Observed
- **AI agents are reshaping infrastructure**: Vercel reports 30% of deployments from agents; framework teams (Next.js, Svelte) adding agent-first features
- **Verification-first AI coding**: Devs moving away from "generate-and-pray" to agentic loops with verification steps
- **Platform portability**: Next.js Adapter API formalizes multi-cloud deployment
- **Ghostty** (terminal emulator) leaving GitHub — signals growing discontent with Microsoft's GitHub platform
- **AI slop critique growing**: Community pushing back on low-quality AI-generated frontend code

