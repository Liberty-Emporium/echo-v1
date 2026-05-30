# Web Development Mastery — Change Log

> Auto-daily research updates by OWL for Liberty Emporium.

---

## 2026-05-30 — Hosting & DevOps Platform Updates (Run 1)

### Railway

- **[Railway] V3 Platform — Faster and Cheaper (announced early 2026)**
  - Major infrastructure rewrite: simultaneously decreased cost and increased performance
  - New Architecture View for visualizing service topology
  - Focused PR environments for cleaner code review workflows

- **[Railway] $100M Series B raised (January 2026)**
  - Significant funding round signaling strong growth trajectory

- **[Railway] Railway Agent & AI Features (April–May 2026)**
  - Railway Agent: AI-powered deployment assistance and infrastructure management
  - Agent sandbox with HA static egress (May 22)
  - GitHub org guardrails for team safety (May 22)
  - Remote MCP support for agent integrations (April 17)
  - One-command skills install (April 17)
  - Agent Skill 2.0 with smart diagnosis (February 27)
  - Volume browser in CLI, in-browser shell, file browser for buckets (May 29)
  - Railway Agent in the CLI (April 17)

- **[Railway] Storage & Databases (March–May 2026)**
  - Postgres Point-in-Time Recovery (PITR) support (May 15)
  - One-click HA Postgres with read replicas (March 13, improved March 27)
  - Undoable volume deletes (May 1)
  - Zero-downtime volume resizing (January 30)
  - Buckets in CLI (March 13)
  - Queries for all databases (March 20)

- **[Railway] CLI & Developer Tools (April–May 2026)**
  - CLI metrics dashboard (May 15)
  - Railway scale TUI for resource management (May 8)
  - Skip rebuilds optimization (April 3)
  - Better CLI experience (April 3, April 17)
  - Unified template search (May 8)
  - Auto-deploy toggle (May 1)
  - Easy agent setup (May 8)
  - railway dev TUI (December 2025)

- **[Railway] Networking & Security (February–May 2026)**
  - Standard SSH support (May 1)
  - IPv6 support (April 24)
  - DDoS protection (February 20)
  - One-click CDN setup (March 27)
  - Magic domains with automatic TLS (February 6)
  - Deploy-less horizontal scaling (February 6)
  - Enforce 2FA option (January 16)
  - Network flows visibility (February 13)
  - Singapore Buckets (January 16)

- **[Railway] Dashboard & UX (January–May 2026)**
  - New dashboard layout with improved navigation (March 20)
  - DNS management built into dashboard (March 20)
  - Buy domains directly on Railway (March 6)
  - AI Agent Panel (March 6)
  - Chat with your Canvas — conversational infrastructure (February 13)
  - Login with Railway OAuth (January 30)
  - DB Metrics dashboard (February 13)
  - Smart diagnosis for troubleshooting (March 20)

### Vercel

- **[Vercel] Function Invocation Billing Change (May 29, 2026)**
  - Moving from package-based to per-unit pricing for Pro and new Enterprise customers
  - New rate: $0.0000006 per invocation (same effective rate as $0.60/1M but smoother scaling)
  - Pro teams benefit: function invocations no longer rapidly consume monthly usage credits
  - Existing customers keep current rate until end of billing cycle

- **[Vercel] Docker in Sandbox (May 29, 2026)**
  - Vercel Sandbox now supports installing and running Docker containers inside sandbox environments
  - Agents can build containers, install system packages, modify files without touching host system
  - Use cases: running Redis/Postgres as test dependencies, validating container images, previewing containerized apps
  - Persistent sandboxes carry Docker installations between sessions
  - Also added: FUSE filesystem drivers and VPN client support in sandboxes

- **[Vercel] Agentic Infrastructure (April 2026)**
  - 30% of deployments now agent-initiated (up 1000% from 6 months ago)
  - Claude Code = 75% of agent deployments, Lovable/v0 = 6%, Cursor = 1.5%
  - AI SDK 6 adds agent abstraction layer
  - Agent-deployed projects are 20x more likely to call AI inference provider than human-deployed
  - Vision: "Infrastructure that is itself agentic" — platform auto-investigates anomalies, performs root-cause analysis

- **[Vercel] Next.js Across Platforms: Adapter API (March 2026)**
  - Stable Adapter API: typed, versioned build output description that any platform can target
  - Shared test suite for every adapter, including Vercel's
  - Multi-platform collaboration with OpenNext, Netlify, Cloudflare, AWS Amplify, Google Cloud
  - Verified adapters as open-source, community-owned under the Next.js org
  - Ecosystem Working Group for coordinating changes across providers

### Netlify

- **[Netlify] Claude Opus 4.8 in AI Gateway & Agent Runners (May 28, 2026)**
  - Anthropic's Claude Opus 4.8 now available through Netlify AI Gateway and Agent Runners
  - Zero configuration required — use Anthropic SDK directly in Netlify Functions
  - Automatic caching, rate limiting, and auth infrastructure provided
  - Available for all Function types and Agent Runners

- **[Netlify] Gemini 3.5 Flash in Agent Runners (May 20, 2026)**
  - Google's Gemini 3.5 Flash model now available via Agent Runners
  - Zero configuration required

- **[Netlify] Build Plugin Node.js Support (May 21, 2026)**
  - End of support for Node.js 18 and Node.js 20 in build plugins
  - Both versions have reached official end of life
  - Teams should upgrade to Node.js 22+ for build plugins

- **[Netlify] Nuxt Security Update (May 19, 2026)**
  - Four security vulnerabilities disclosed in Nuxt framework
  - Netlify customers advised to update Nuxt dependencies

### Render

- **[Render] Dedicated Outbound IPs (May 19, 2026)**
  - Pro workspaces and higher can create dedicated IP sets for outbound traffic
  - Each set includes 3 IPv4 addresses in a single region
  - Scope to entire workspace or specific environments
  - Cost: $100/month per IP set
  - Use case: simplify allowlisting with external providers

- **[Render] Service Repo/Image Change in Dashboard (May 11, 2026)**
  - Can now change an existing service's backing Git repo or Docker image via dashboard (previously required API)
  - Automatically triggers deploy with new source
  - Note: cannot change service type (web service ↔ static site)

- **[Render] Python Build Optimization (April 30, 2026)**
  - Median build time for Python services reduced by 27%
  - Optimizations: tuned chunk size/parallelism for image uploads, on-disk Python version caching, universal layer sharing
  - Before: 76 seconds median → After: 55 seconds median

- **[Render] Workspace Plan Updates (April 23, 2026)**
  - New workspace plans rolled out: Hobby (free), Pro, Team, Enterprise
  - Legacy plans mapped to new equivalents for scalability
  - More scalable pricing for growing teams

- **[Render] CLI & SDK Updates**
  - Render CLI v2.19.0 (May 28, 2026)
  - Python SDK BETA v0.6.1 (April 7, 2026)
  - TypeScript SDK BETA v0.5.1 (April 7, 2026)

- **[Render] Render Conference 2026**
  - Render hosting a conference in San Francisco on June 18, 2026

### Fly.io

- **[Fly.io] "Our Best Customers Are Now Robots" trend (early 2026)**
  - Significant growth in AI/automated agents deploying on Fly.io
  - Reflects shift toward autonomous infrastructure management

- **[Fly.io] Litestream v0.5.0 (early 2026)**
  - Major Litestream release: SQLite replication to S3-compatible storage
  - Litestream Writable VFS for direct SQLite sync to object storage
  - Enables durable, serverless-friendly SQLite

- **[Fly.io] Sprites platform updates (early 2026)**
  - New lightweight VM abstraction layer for faster container-to-VM conversion
  - Performance optimization for Fly's core container-to-VM pipeline
  - Design & implementation deep dive published

- **[Fly.io] MCP Server Ecosystem (early 2026)**
  - "Unfortunately, Sprites Now Speak MCP" — MCP protocol support added to Sprites
  - "Launching MCP Servers on Fly.io" — guide for deploying MCP servers
  - "Provisioning Machines using MCPs" — MCP-driven infrastructure provisioning
  - Kurt Mackey's "30 Minutes with MCP and flyctl" practical guide

- **[Fly.io] AI/ML on Fly.io (early 2026)**
  - Phoenix.new: Remote AI Runtime for Phoenix by Chris McCord
  - MorphLLM guide for building better AI agents on Fly.io
  - Trust calibration frameworks for AI software builders
  - AI Town 1-click deploy for model evaluation via simulation
  - "The Future Isn't Model Agnostic" — Daniel Botha on AI strategy

- **[Fly.io] Engineering Deep Dives (early 2026)**
  - "Corrosion" — Thomas Ptacek & Pavel Borzenkov's deep dive on Fly's Rust-based proxy internals
  - "Taming A Voracious Rust Proxy" by Peter Cai — production proxy tuning
  - "parking_lot" — technical writeup of Fly's core container scheduling
  - "Code And Let Live" by Kurt Mackey on system design philosophy

- **[Fly.io] Kamal 2.0 in Production (early 2026)**
  - Sam Ruby's guide to using Kamal 2.0 (DHH's deploy tool) on Fly.io
  - Alternative to Heroku-style deploys for Rails apps

### Industry Trends (Hacker News & Dev News, May 2026)

- **[Trend] MCP Protocol under scrutiny**: "MCP is dead?" post garners 201 points, 176 comments — active debate about Model Context Protocol's viability as standard
- **[Trend] SQLite resurgence**: "SQLite is all you need for durable workflows" hits #1 on HN (499 pts, 253 comments) — signals return to simplicity in infrastructure
- **[Trend] AI infrastructure in C++**: "Tiny vLLM — high performance LLM inference in C++ and CUDA" (137 pts) — demand for low-level inference optimization
- **[Trend] TypeScript native compilation**: "Perry compiles TypeScript directly to executables using SWC and LLVM" (79 pts)
- **[Trend] AI home robotics data**: "Shift cleans homes for free to train future robots" (131 pts) — real-world training data collection business models
- **[Trend] AI frontend concerns**: "Is AI causing a repeat of frontend's lost decade?" (334 pts, 288 comments) — deep community concern about AI-generated code quality
- **[Trend] Liquid AI MoE**: Liquid AI reveals 8B-A1B Mixture-of-Experts model trained on 38T tokens (182 pts)
- **[Trend] OpenRouter Hy3**: Mysterious Hy3 LLM topping OpenRouter rankings by large margin (127 pts)
- **[Trend] GTA 6 devs unionize**: Labor movement in game dev (668 pts — highest on HN that day)
- **[Trend] Ember.js 7.0**: Major version release of the veteran JS framework
- **[Trend] Open-source security cameras**: Show HN for end-to-end encrypted home security (55 pts) — privacy-focused self-hosting
- **[Trend] AI job market shifts**: "The Last Technical Interview" by Steve Yegge (104 pts) — changing hiring landscape

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

---

## 2026-05-30 — Run 2: Color, Typography & Visual Design Trends (2025–2026)

### 🎨 Color Trends

#### `contrast-color()` — The End of Manual Accessibility (Smashing, May 28, 2026)
- **70% of websites still fail basic WCAG contrast checks in 2025** — despite years of tooling
- CSS `contrast-color()` is the breakthrough: automatic, algorithmic theming that self-corrects contrast
- Eliminates the need for JS contrast libraries and manual color token definitions
- Enables **algorithmic theming engines**: define a base color, CSS handles accessible foreground/background pairs automatically
- Part of a larger CSS-native approach: `color-mix()`, `light-dark()`, and `contrast-color()` together form a complete theming toolkit

#### Pastel Colors Dominate Dribbble Curated Collections (May 2026)
- Pastel colors featured as a **top curated collection** on Dribbble with 152+ saves
- Signals a shift away from the ultra-vibrant/saturation toward softer, more refined palettes
- Trend visible in luxury branding: "Velora | Luxury Brand Identity" uses soft, pastel-forward palettes
- Reconcilable with M3 Expressive's "vibrant colors" — the trend is toward **intentionality**: either boldly expressive OR softly refined, anything in-between is fading

#### Apple's Liquid Glass Color Philosophy (2026 iOS 26 era)
- Liquid Glass propagates **Adaptive Color** through tinted glass layers
- Color is now computed dynamically from underlying content, not hard-coded
- Designers define "tint hue" and the system handles hierarchy, depth, and contrast
- Sets expectation: users will increasingly expect interfaces to **derive color from context**, not display fixed palettes

#### Fluent 2 Color Tokens (Microsoft, 2026)
- Cross-platform design token system for **adaptive color**
- AI-assisted color generation: Fluent 2 documentation shows patterns for programmatically generating accessible palettes
- Emphasis on: one token → multiple modes (light/dark/high-contrast) computed automatically

### ✒️ Typography Trends

#### Geometric Sans Serifs Dominate Behance Trending (May 2026)
- "Method — Geometric Sans Serif Font" (237 appreciations, 4,495 views) — top typography project
- "Circle NG — Geometric Sans Serif Font" (44 appreciations, 608 views)
- Geometric sans (circles-based letterforms, clean geometry) is the dominant **new type trend** for branding and UI
- Driven by: AI/tech branding needs → geometric signals "modern, intelligent, precise"

#### Warm Soft Serifs Counter-Trend
- "Softcore — Warm Soft Serif Font" (63 appreciations, 1,054 views) on Behance
- Represents a growing **serif revival** for brands wanting warmth, humanity, and premium feel
- Particularly strong in: editorial, luxury, wellness, food/beverage verticals
- The trend is: **serifs for emotion, sans-serifs for clarity** → purposeful type pairing

#### Apple HIG 2026: Emphasized Dynamic Type
- Added **emphasized weights** to Dynamic Type specifications per platform
- Designers can now semantically emphasize text without changing font size → better accessibility
- Variable fonts (especially Google Sans Flex in M3) enable **fluid typography scales** that adapt to screen size

#### Typography-Driven CSS
- CSS `letter-spacing` creative text effects (Revealing Text, May 2026 CSS-Tricks) shows renewed interest in **micro-typography control**
- The missing `::nth-letter()` pseudo-element remains highly requested — signals the community wants per-character CSS control
- `::first-letter` and `letter-spacing` workarounds are the current state-of-the-art
- **Variable fonts** becoming the default: Flex axes allow one font file to serve multiple weights, widths, and optical sizes

### 🖥️ 2025–2026 Visual Design Trends Summary

#### From the Awwwards Sites of the Day (May 2026)
- **ZettaJoule** (Site of the Day, May 30): WebGL-heavy, immersive, dark theme, electric/high-contrast
- **Cartier Watches & Wonders 2026**: Spatial 3D, cinematic scroll-triggered animations, ultra-premium
- **Razorpay Sprint 26**: Clean SaaS aesthetic, subtle gradients, modern dashboard patterns
- **Travel Guide iOS App**: Mobile-first, clean card layouts, generous whitespace
- Key pattern: **extremes** — sites are going either **very immersive/luxury** or **very clean/functional**

#### The Immersive vs. Functional Split
- Top web design is polarizing into two camps:
  1. **Immersive/Cinematic**: WebGL, 3D, scroll-driven narratives, spatial interactions
  2. **Clean/Functional**: Bento grids, card layouts, whitespace, fast-loading
- Middle-ground "corporate bland" is being replaced by strong personality in either direction
- Framer (advertising on Dribbble) positions itself as the tool for the immersive camp

#### Bento Grids Evolving
- Apple-style bento grids remain dominant but are **maturing**: from novelty → standard
- New pattern: **bento + asymmetry** — mixing grid sizes unpredictably for visual interest
- Combined with **internal carousels** inside bento cells for dense information display

#### Glass & Depth Evolution
- Glassmorphism (2021–2023) evolved into **Liquid Glass** (Apple) and **Expressive Depth** (Material)
- 2026 approach: depth layers are **physically simulated** (refraction, light bending) not just blur
- Performance cost is managed via `backdrop-filter: blur()` with carefully bounded rendering areas

#### Scroll-Linked Narratives
- Figma Make expansion (May 28, 2026): designing with code locally → signals **generated/parametric layouts** are coming to mainstream
- CSS scroll-timeline and view-timeline are reaching production readiness
- Cross-document View Transitions (CSS-Tricks, May 2026): **scaling page transitions across hundreds of elements**
- Config 2026 speakers interrogating "craft, quality, and intention" in AI-powered world

#### Color in AI-Generated Design
- NNG: "Practical Interface Patterns for AI Transparency (Part 2)" (May 2026) — interface patterns for AI systems
- **AI-augmented design is now embedded in all major tools** (Figma Design Agent, Fluent AI patterns, AI SDK 6)
- Color trend impact: AI systems need **systematic color** (tokens, not magic numbers) to produce coherent generate output
- The more AI generates UIs, the more important design-system color tokens become

#### Minimalism ≠ Boring (2026 Evolution)
- NN/G's "Small by Design: The Strength of Lean Design-System Teams" (May 15, 2026) → lean, focused design systems
- CSS `sibling-index()` and `sibling-count()` (May 2026 Smashing) → complex layouts from minimal CSS, no JS
- Trend: **less tooling, more CSS-native power** → simpler codebases, more expressive results
- 70% WCAG failure rate suggests teams are still **under-investing in basic accessibility** while chasing visual trends
