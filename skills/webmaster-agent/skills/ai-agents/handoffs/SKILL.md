---
name: ai-agent-handoffs
description: AI agent handoffs and orchestration — multi-agent routing, input filters, human-in-the-loop escalation
version: 1.0.0
platforms: [linux, macos, windows]
---

# AI Agent Handoffs & Orchestration

## When to use
- Building multi-agent systems where tasks need routing
- Customer support automation (billing → technical → sales → human)
- Multi-step workflows requiring different expertise
- Any system where task complexity exceeds a single agent's context

## Key Concept
Handoffs are represented as **tools** to the LLM. The LLM decides when to invoke them based on the handoff description.

## Architecture
```
User Input → Triage Agent → Specialist Agent → (if stuck) → Human Escalation
```

## Implementation

### 1. Define Specialist Agents
Each agent has a narrow, well-defined role with specific tools.

### 2. Create Triage Agent with Handoffs
The triage agent determines intent and routes to specialists.

### 3. Input Filtering
Control what context passes during handoffs — filter irrelevant history.

### 4. Structured Input with Pydantic
Require structured data for handoffs (order numbers, reasons, amounts).

### 5. Human-in-the-Loop Escalation
Always have an escalation path when automated agents can't resolve.

### 6. Guardrails
Add input guardrails to prevent misuse (reject off-topic requests).

## Liberty Emporium Use Case
Customer support routing:
- **Triage** → determines intent
- **Order Agent** → order status, tracking
- **Refund Agent** → refund requests
- **FAQ Agent** → common questions
- **Escalation** → human agent handoff

## Key Patterns
- Handoffs as LLM tools (not hardcoded routing)
- Input filters to reduce context bloat
- Pydantic models for structured handoff data
- Guardrails for safety
- Human escalation as last resort

## Source
Based on OpenAI Agents Python SDK handoffs documentation.
Full version: `references/handoffs-orchestration-full.md`
