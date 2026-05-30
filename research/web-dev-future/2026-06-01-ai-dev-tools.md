# AI-Powered Dev Tools — Research Notes

**Date:** 2026-06-01  
**Run:** 3  
**Topic:** AI-Powered Development Tools  
**Sources:** Vercel Blog, The New Stack, Hacker News, dev.to (front page trend analysis)

---

## Executive Summary

The AI dev tool landscape in mid-2026 has shifted from "AI-assisted coding" to **agentic infrastructure** — platforms designed for AI agents to build, test, and deploy software autonomously. The era of Copilot-style autocomplete is giving way to full agentic workflows where Claude Code, Cursor, and Vercel's own agent tools are building entire applications with minimal human intervention.

---

## 1. The Agentic Deployments Surge

### Key Stat: 30% of Vercel deployments now come from AI agents
- Up **1000% from six months ago**
- Claude Code dominates agentic deployment share at **75%**
- Lovable and v0 account for **6%**
- Cursor accounts for **1.5%**
- Vercel projects deployed by coding agents are **20x more likely** to call AI inference providers than human-deployed projects

### Implication for Client Projects
When building SaaS apps for clients, we should architect for **agent-first development**: agent-friendly CLIs, programmatic deployment surfaces, preview URLs on every commit, and agent-readable configuration files (like AGENTS.md).

---

## 2. Agentic Infrastructure — The Three-Layer Model (Vercel)

Vercel's Tom Occhino outlined a three-layer model for agentic infrastructure:

### Layer 1: Infrastructure for Coding Agents to Deploy To
- **Immutable deployments** with preview URLs on every commit
- **Instant rollbacks** as prerequisites for machine-driven development
- Vercel CLI, API, MCP servers, and git integration give agents native deployment access
- Agents can: generate code → open PR → get preview URL → verify output → ship to production, all without human involvement

### Layer 2: Infrastructure for Building and Running Agents
- **AI SDK 6+** adds agent abstraction — define an agent once, reuse across interfaces
- **Chat SDK** makes agents available across dozens of chat apps from a single codebase
- **AI Gateway** — single endpoint for hundreds of models, with budgets, monitoring, routing, retries, fallbacks
- **Fluid Compute** — designed for AI workloads where latency, concurrency, and idle waiting all matter
- **Workflows & Queues** — agents can pause, resume, retry, maintain state, offload background work
- **Sandbox** — isolated execution environments for untrusted code
- **Observability** — trace what agents are doing and where they go wrong

### Layer 3: Infrastructure That Is Itself Agentic
- Unified platform provides complete visibility across every layer in real time
- Agents can autonomously monitor production, investigate anomalies, query logs, inspect source code
- Root-cause analysis and fix proposals in isolated sandboxes
- Currently with human approval; trending toward autonomous operation

---

## 3. Inference Theft — A New Security Threat

### The Problem
- AI inference is **1 million times more expensive** than regular HTTP requests ($2/prompt vs $2/million requests)
- Attackers wrap AI endpoints in OpenAI/Anthropic-compatible adapters and resell tokens
- **Chipotlai Max** — a forked coding agent that turned Chipotle's support chatbot into an OpenAI-compatible endpoint
- Openly soliciting help porting the same approach to Home Depot, Lowe's, Target, Starbucks

### The Attack Pattern
- Attacker's adapter sits between downstream users and the victim's API
- Users authenticate to the adapter, not the victim's endpoint
- Residential proxies bypass IP-based rate limits
- Per-session checks get amortized across thousands of stolen calls

### The Defense
- **Per-request verification** (not per-session) — Vercel uses BotID deep analysis
- Traditional CAPTCHAs are bypassed by the same AI models
- BotID uses client-side ML to distinguish humans from bots without visible challenges
- **Key lesson for client projects**: Any AI endpoint exposed to the internet needs per-request bot verification

---

## 4. Vercel Workflows — GA (April 16, 2026)

### Key Facts
- Processed **100M+ runs** and **500M+ steps** across **1,500+ customers** in beta
- **200K+ npm downloads/week**
- Python SDK now in beta
- **Workflows 5** in development with native concurrency controls, global deployment, snapshot-based runtime

### Programming Model
```typescript
// Workflows is ordinary TypeScript — agent-friendly
import { workflow, step } from '@vercel/workflows';

export const myWorkflow = workflow(async () => {
  const data = await step('fetch-data', async () => {
    return await fetchData();
  });
  
  const result = await step('process', async () => {
    return await processData(data);
  });
  
  return result;
});
```

### Durable Streams
- `getWritable()` gives persistent streams that multiple clients can connect/disconnect/reconnect
- Flight booking agent example: streams itinerary updates as it searches
- User closes browser mid-search → workflow continues → reconnect and resume exactly where left off
- No Redis or custom pub/sub required

### Key Integrations
- **Mux**: media intelligence pipelines with durable video/AI inference
- **Durable**: website creation for 3M+ small businesses, dozens of parallel AI steps in <30 seconds
- **Flora**: creative AI agents across 50+ image models, no queues/state machines
- AI SDK v7 introduces **WorkflowAgent** — fully native implementation

---

## 5. AI Tool Landscape — What's Trending

### Claude Code
- Dominant agentic deployment tool (75% share on Vercel)
- Researcher experiment: "gave Claude Code 'ADHD' (interrupt-driven attention switching) and it thinks 2x better"
- Anthropic hired **Andrej Karpathy** (OpenAI co-founder) to lead Claude pre-training research
- **Claude Opus 4.8**: effort controls, dynamic workflows, cheaper fast mode, better honesty, less deception

### Replit & Vibe Coding
- Replit's vibe coding platform got a **Visa-backed identity layer for AI agents**
- Changes how agents spend money — agents can now have financial identity
- Fivetran's CPO: "Closed data stacks won't survive the agent era"
- "AI agents need to spend money — Stripe and iWallet are building the rails"

### Cursor
- 1.5% of agentic deployments on Vercel
- Still growing but trail Claude Code significantly

### MCP (Model Context Protocol)
- **WebMCP** turns any Chrome web page into an MCP server for AI agents
- DocuSign building MCP server for agentic agreement enterprise
- MCP + synthetic data reshaping compliance in agentic era
- "The API portal is the clearest signal of whether your company can handle AI agents"

### Governance & Security
- **AC/DC framework** helps teams govern AI coding agents
- "There is no accountability: AI coding agents are installing packages no one owns"
- WebAssembly could solve AI agents' most dangerous security gap
- "CI wasn't built for coding agents — here's what comes next"
- "The agent code explosion is here — we need to rethink our pipelines, fast"
- "As agentic dev tools boom, workflow auditability becomes the constraint"
- "Why AI agents need a Context Lake"
- Chainguard has a fix for the open source packages AI agents keep grabbing

### Google & Expo
- Google wants to make the web agent-ready
- Expo bets big on React Native's agentic future

---

## 6. Key Findings for Client Projects

### For Liberty Emporium / AAIS Clients

1. **AI-agent-first development is the default now.** Every new project should have:
   - AGENTS.md for coding agent context
   - Programmatic deployment (Vercel CLI/API integration)
   - Preview URLs on every commit
   - Agent-friendly configuration

2. **Security for AI endpoints is critical:**
   - Per-request bot verification (BotID or equivalent) on any AI endpoint
   - Monitor for inference theft — especially for customer-facing AI features
   - Rate limit per-session is NOT sufficient

3. **Use Vercel Workflows for any long-running process:**
   - Customer onboarding flows
   - Payment processing
   - ETL pipelines
   - Multi-step AI operations

4. **AI SDK + AI Gateway pattern:**
   - Single endpoint for multiple AI models
   - Built-in budget controls, monitoring, retries, fallbacks
   - Don't manage provider adapters manually

5. **Agent tool selection for client SaaS:**
   - Claude Code for complex development workflows
   - Vercel deployment for Next.js projects
   - Workflows SDK for backend processes
   - AI Gateway for any AI feature (don't hardcode one provider)

6. **The "Context Lake" concept** — centralized context management for agents:
   - Structured context files agents can read
   - Product specs, API docs, deployment info in agent-readable format
   - Avoid tribal knowledge that only humans know

---

## 7. Sources

- Vercel Blog — "Agentic Infrastructure" (May 29, 2026)
- Vercel Blog — "Protecting Against Inference Theft" (May 29, 2026)
- Vercel Blog — "A New Programming Model for Durable Execution" (Apr 16, 2026)
- Vercel Blog — "Zo Computer Case Study: 20x Reliability" (Apr 16, 2026)
- The New Stack — Various articles (May 2026)
- Hacker News Front Page (May 30, 2026)
# AI-Powered Dev Tools — Research Notes

**Date:** 2026-06-01
**Run:** 3
**Topic:** AI-Powered Development Tools
**Sources:** Vercel Blog, The New Stack, Hacker News, dev.to

---

## Executive Summary

The AI dev tool landscape in mid-2026 has shifted from "AI-assisted coding" to **agentic infrastructure** — platforms designed for AI agents to build, test, and deploy software autonomously. The era of Copilot-style autocomplete is giving way to full agentic workflows where Claude Code, Cursor, and Vercel's own agent tools are building entire applications with minimal human intervention.

---

## 1. The Agentic Deployments Surge

### Key Stat: 30% of Vercel deployments now come from AI agents
- Up **1000% from six months ago**
- Claude Code dominates agentic deployment share at **75%**
- Lovable and v0 account for **6%**
- Cursor accounts for **1.5%**
- Vercel projects deployed by coding agents are **20x more likely** to call AI inference providers than human-deployed projects

### Implication for Client Projects
When building SaaS apps for clients, we should architect for **agent-first development**: agent-friendly CLIs, programmatic deployment surfaces, preview URLs on every commit, and agent-readable configuration files (like AGENTS.md).

---

## 2. Agentic Infrastructure — The Three-Layer Model (Vercel)

Vercel's Tom Occhino outlined a three-layer model for agentic infrastructure:

### Layer 1: Infrastructure for Coding Agents to Deploy To
- **Immutable deployments** with preview URLs on every commit
- **Instant rollbacks** as prerequisites for machine-driven development
- Vercel CLI, API, MCP servers, and git integration give agents native deployment access
- Agents can: generate code → open PR → get preview URL → verify output → ship to production, all without human involvement

### Layer 2: Infrastructure for Building and Running Agents
- **AI SDK 6+** adds agent abstraction — define an agent once, reuse across interfaces
- **Chat SDK** makes agents available across dozens of chat apps from a single codebase
- **AI Gateway** — single endpoint for hundreds of models, with budgets, monitoring, routing, retries, fallbacks
- **Fluid Compute** — designed for AI workloads where latency, concurrency, and idle waiting all matter
- **Workflows & Queues** — agents can pause, resume, retry, maintain state, offload background work
- **Sandbox** — isolated execution environments for untrusted code
- **Observability** — trace what agents are doing and where they go wrong

### Layer 3: Infrastructure That Is Itself Agentic
- Unified platform provides complete visibility across every layer in real time
- Agents can autonomously monitor production, investigate anomalies, query logs, inspect source code
- Root-cause analysis and fix proposals in isolated sandboxes
- Currently with human approval; trending toward autonomous operation

---

## 3. Inference Theft — A New Security Threat

### The Problem
- AI inference is **1 million times more expensive** than regular HTTP requests ($2/prompt vs $2/million requests)
- Attackers wrap AI endpoints in OpenAI/Anthropic-compatible adapters and resell tokens
- **Chipotlai Max** — a forked coding agent that turned Chipotle's support chatbot into an OpenAI-compatible endpoint
- Openly soliciting help porting the same approach to Home Depot, Lowe's, Target, Starbucks

### The Attack Pattern
- Attacker's adapter sits between downstream users and the victim's API
- Users authenticate to the adapter, not the victim's endpoint
- Residential proxies bypass IP-based rate limits
- Per-session checks get amortized across thousands of stolen calls

### The Defense
- **Per-request verification** (not per-session) — Vercel uses BotID deep analysis
- Traditional CAPTCHAs are bypassed by the same AI models
- BotID uses client-side ML to distinguish humans from bots without visible challenges
- **Key lesson for client projects**: Any AI endpoint exposed to the internet needs per-request bot verification

---

## 4. Vercel Workflows — GA (April 16, 2026)

### Key Facts
- Processed **100M+ runs** and **500M+ steps** across **1,500+ customers** in beta
- **200K+ npm downloads/week**
- Python SDK now in beta
- **Workflows 5** in development with native concurrency controls, global deployment, snapshot-based runtime

### Programming Model
```typescript
// Workflows is ordinary TypeScript — agent-friendly
import { workflow, step } from '@vercel/workflows';

export const myWorkflow = workflow(async () => {
  const data = await step('fetch-data', async () => {
    return await fetchData();
  });

  const result = await step('process', async () => {
    return await processData(data);
  });

  return result;
});
```

### Durable Streams
- `getWritable()` gives persistent streams that multiple clients can connect/disconnect/reconnect
- Example: flight booking agent streams itinerary updates as it searches
- User closes browser mid-search → workflow continues → reconnect and resume exactly where left off
- No Redis or custom pub/sub required

### Key Integrations
- **Mux**: media intelligence pipelines with durable video/AI inference
- **Durable**: website creation for 3M+ small businesses, dozens of parallel AI steps in <30 seconds
- **Flora**: creative AI agents across 50+ image models, no queues/state machines
- AI SDK v7 introduces **WorkflowAgent** — fully native implementation

---

## 5. AI Tool Landscape — What's Trending

### Claude Code
- Dominant agentic deployment tool (75% share on Vercel)
- Researcher experiment: "gave Claude Code 'ADHD' (interrupt-driven attention switching) and it thinks 2x better"
- Anthropic hired **Andrej Karpathy** (OpenAI co-founder) to lead Claude pre-training research
- **Claude Opus 4.8**: effort controls, dynamic workflows, cheaper fast mode, better honesty, less deception

### Replit & Vibe Coding
- Replit's vibe coding platform got a **Visa-backed identity layer for AI agents**
- Changes how agents spend money — agents can now have financial identity
- Fivetran's CPO: "Closed data stacks won't survive the agent era"
- "AI agents need to spend money — Stripe and iWallet are building the rails"

### Cursor
- 1.5% of agentic deployments on Vercel
- Still growing but trails Claude Code significantly

### MCP (Model Context Protocol)
- **WebMCP** turns any Chrome web page into an MCP server for AI agents
- DocuSign building MCP server for agentic agreement enterprise
- MCP + synthetic data reshaping compliance in agentic era
- "The API portal is the clearest signal of whether your company can handle AI agents"

### Governance & Security
- **AC/DC framework** helps teams govern AI coding agents
- "There is no accountability: AI coding agents are installing packages no one owns"
- WebAssembly could solve AI agents' most dangerous security gap
- "CI wasn't built for coding agents — here's what comes next"
- "The agent code explosion is here — we need to rethink our pipelines, fast"
- "As agentic dev tools boom, workflow auditability becomes the constraint"
- "Why AI agents need a Context Lake"
- Chainguard has a fix for the open source packages AI agents keep grabbing

### Google & Expo
- Google wants to make the web agent-ready
- Expo bets big on React Native's agentic future

---

## 6. Key Findings for Client Projects

### For Liberty Emporium / AAIS Clients

1. **AI-agent-first development is the default now.** Every new project should have:
   - AGENTS.md for coding agent context
   - Programmatic deployment (Vercel CLI/API integration)
   - Preview URLs on every commit
   - Agent-friendly configuration

2. **Security for AI endpoints is critical:**
   - Per-request bot verification (BotID or equivalent) on any AI endpoint
   - Monitor for inference theft — especially for customer-facing AI features
   - Rate limit per-session is NOT sufficient

3. **Use Vercel Workflows for any long-running process:**
   - Customer onboarding flows
   - Payment processing
   - ETL pipelines
   - Multi-step AI operations

4. **AI SDK + AI Gateway pattern:**
   - Single endpoint for multiple AI models
   - Built-in budget controls, monitoring, retries, fallbacks
   - Don't manage provider adapters manually

5. **Agent tool selection for client SaaS:**
   - Claude Code for complex development workflows
   - Vercel deployment for Next.js projects
   - Workflows SDK for backend processes
   - AI Gateway for any AI feature (don't hardcode one provider)

6. **The "Context Lake" concept** — centralized context management for agents:
   - Structured context files agents can read
   - Product specs, API docs, deployment info in agent-readable format
   - Avoid tribal knowledge that only humans know

---

## 7. Sources

- Vercel Blog — "Agentic Infrastructure" (May 29, 2026)
- Vercel Blog — "Protecting Against Inference Theft" (May 29, 2026)
- Vercel Blog — "A New Programming Model for Durable Execution" (Apr 16, 2026)
- Vercel Blog — "Zo Computer Case Study: 20x Reliability" (Apr 16, 2026)
- The New Stack — Various articles (May/June 2026)
  - Why agent harnesses fail inside cloud-native systems
  - Replit's Visa-backed identity layer for AI agents
  - WebMCP turns any Chrome page into an MCP server
  - Claude Opus 4.8 release
  - Claude Code "ADHD" experiment
  - Agent governance frameworks
  - Inference theft patterns
- Hacker News Front Page (May 30, 2026)
