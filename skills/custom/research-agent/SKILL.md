---
name: research-agent
description: Deep research on any topic using agentic multi-step search with reflection, planning, and synthesis. Use when Jay asks to research something, "look up", "find out about", "what's the latest on", "investigate", or when building something that requires understanding current best practices, APIs, competitors, or market info. Produces structured reports saved to research/.
---

# Research Agent

Multi-step research using the 2025 Agentic RAG pattern: plan → retrieve → evaluate → reformulate → synthesize.

## Workflow

### Step 1: Plan
Break the research question into 3-5 sub-queries:
- Core question
- Current best practices / alternatives
- Practical implementation angle
- Pitfalls / what not to do
- (Optional) Competitor/market angle

### Step 2: Retrieve
Run `web_search` for each sub-query. Use:
- `type: "neural"` for concept/best-practice queries
- `type: "fast"` for factual/recent queries  
- `contents: {summary: true}` to get synthesized summaries

### Step 3: Evaluate & Reformulate
After first round:
- Did we get actionable answers?
- Any gaps? Run 1-2 follow-up searches to fill them.
- Cross-check conflicting info with a targeted search.

### Step 4: Synthesize
Produce a structured report:

```markdown
# Research: [Topic]
Date: YYYY-MM-DD

## TL;DR (3 bullets max)
- Key finding 1
- Key finding 2  
- Key finding 3

## What's Current (2025/2026)
[What's actually being used in production right now]

## Best Approach for Jay's Stack
[Flask/Python/Railway-specific recommendations]

## Watch Out For
[Gotchas, deprecated patterns, common mistakes]

## Resources
- [Link 1](url) — what it is
- [Link 2](url) — what it is
```

### Step 5: Save
Save report to: `research/YYYY-MM-DD-[topic-slug].md`

Update MEMORY.md with a one-liner: `- Researched [topic] on YYYY-MM-DD — see research/[filename]`

## Research Quality Rules

- **Prioritize recency** — use `freshness: "year"` for fast-moving topics
- **Prefer primary sources** — official docs, arxiv, GitHub over blog summaries
- **Be skeptical of hype** — "best" claims need evidence
- **Jay's stack is Flask/Python/Railway** — always translate findings to his context
- **Don't research for its own sake** — end with actionable recommendations

## When to Use Deep vs Fast Research

**Fast (1-2 searches):** Quick facts, specific APIs, error messages, simple how-tos

**Deep (full workflow):** Architecture decisions, new tech to adopt, competitive analysis, best practices for a major feature
