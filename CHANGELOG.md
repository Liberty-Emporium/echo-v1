# Echo V1 — Web Dev & AI Research Changelog

---

## 2026-05-30 — Quick Web Dev Check (HN + GitHub Trending + Vercel Blog)

### Hacker News Top Stories

1. **SQLite is all you need for durable workflows** (obeli.sk) — 499 pts, 252 comments
   - Argues SQLite can replace complex workflow engines for durable execution. Lightweight, file-based, battle-tested. Strong community discussion.

2. **MCP is dead?** (quandri.io) — 200 pts, 176 comments
   - Hot take questioning whether Model Context Protocol has staying power. Sparked massive debate — MCP tooling is still early but rapidly evolving.

3. **Perry: Compiles TypeScript directly to executables using SWC + LLVM** (perryts.com) — 79 pts, 62 comments
   - New tool that bypasses Node.js entirely — compiles TS → native binaries via SWC (Rust-based TypeScript parser) + LLVM backend. Could change TS deployment story.

4. **Notes from the Mistral AI Now Summit** (koenvangilst.nl) — 357 pts, 142 comments
   - Detailed recap of Mistral's latest announcements. Covers new model releases, API changes, and Mistral's positioning vs OpenAI/Anthropic.

5. **The dead economy theory** (owenmcgrann.com) — 948 pts, 1096 comments
   - Viral HN top post about economic "zombification" — businesses that can't die or grow. Massive engagement.

6. **Algebraic Effects for the Rest of Us** (overreacted.io) — 24 pts, 10 comments
   - Dan Abramov-style deep dive on algebraic effects in programming languages. Relevant to error handling patterns in JS/TS.

7. **Snowboard Kids 2 is 100% Decompiled** (blog.chrislewis.au) — 174 pts, 64 comments
   - Retro gaming / reverse engineering win. Full N64 decompilation. Impressive preservation work.

8. **Shift will clean homes for free to train future robots** (theverge.com) — 129 pts, 183 comments
   - Robot training data via real-world home cleaning. Controversial — free labor for data collection.

9. **A new register allocator for ZJIT** (railsatscale.com) — 27 pts
   - Ruby JIT internals. Performance improvements for Rails apps.

### GitHub Trending (Today)

| Repo | Stars | Description |
|------|-------|-------------|
| harry0703/MoneyPrinterTurbo | 70.6k ⭐ (+3,567 today) | AI-powered short video generation — one-click viral videos |
| microsoft/markitdown | 130.6k ⭐ (+1,873 today) | Convert files/office docs to Markdown (Python) |
| Leonxlnx/taste-skill | 28.5k ⭐ (+2,062 today) | "Taste" skill for AI — stops generic/boring AI output |
| EveryInc/compound-engineering-plugin | 18.2k ⭐ (+353 today) | Plugin for Claude Code/Codex/Cursor — compound engineering workflow |
| twentyhq/twenty | 48.5k ⭐ (+578 today) | Open-source CRM, AI-native — Salesforce alternative |
| anthropics/claude-code | 128k ⭐ (+395 today) | Agentic coding tool in terminal — trending hard |
| cursor/plugins | 1.3k ⭐ (+134 today) | Official Cursor plugin spec + plugins |
| run-llama/liteparse | 7.5k ⭐ (+701 today) | Fast open-source document parser |
| galilai-group/stable-worldmodel | 1.3k ⭐ | Platform for world model research |

### Vercel Blog — Featured: "Agentic Infrastructure"

**Author:** Tom Occhino | **Date:** Apr 9

Key points from Vercel's vision for agentic infrastructure:
- **30% of Vercel deployments** are now initiated by coding agents (up 1000% in 6 months)
- Claude Code = 75% of agent deployments, Lovable/v0 = 6%, Cursor = 1.5%
- Three pillars: (1) Infrastructure for coding agents to deploy, (2) Infrastructure for building/running agents, (3) Infrastructure that is itself agentic
- AI SDK 6 adds agent abstraction
- AI Gateway: single endpoint for hundreds of models with routing/failover
- Fluid compute designed for AI workload shapes
- Sandbox for isolated untrusted code execution
- Observability with agent tracing + proposed auto-remediation

### Key Takeaways
- AI coding agents are no longer niche — they're 30% of deployments on Vercel
- MCP debate is heating up — protocol fatigue vs genuine utility?
- TypeScript→native compilation (Perry) could reshape TS deployment
- "Taste" skill repo trending — quality control for AI output is a growing concern
- SQLite for workflows — simplicity win over heavy orchestration
- Open-source CRM (Twenty) going AI-native — enterprise SaaS disruption
