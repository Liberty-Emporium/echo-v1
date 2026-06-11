# Agent Skills Library — Index

## Webmaster Skills

| Skill | Description | Location |
|-------|-------------|----------|
| **monitoring** | Uptime monitoring, health checks, alerting | `skills/monitoring/` |
| **security** | Hardening, scanning, incident response | `skills/security/` |
| **tailscale** | Tailscale networking for agents | `skills/tailscale/` |
| **backup** | Backup and disaster recovery | `skills/backup/` |
| **skill-sharing** | Creating and sharing skills | `skills/skill-sharing/` |

## AI Agent Skills (from Django research)

| Skill | Description | Location |
|-------|-------------|----------|
| **handoffs** | Agent handoffs, multi-agent orchestration, routing | `skills/ai-agents/handoffs/` |
| **llm-resilient-api** | Retry patterns, backoff, circuit breaker, multi-provider | `skills/ai-agents/llm-resilient-api/` |

## DevOps Skills (from Django research)

| Skill | Description | Location |
|-------|-------------|----------|
| **github-actions-oidc** | OIDC for GitHub Actions — no long-lived secrets | `skills/devops/github-actions-oidc/` |
| **docker-supply-chain** | Docker signing, scanning, SBOM, hardening | `skills/devops/docker-supply-chain/` |

## Software Dev Skills (from Django research)

| Skill | Description | Location |
|-------|-------------|----------|
| **python-structured-concurrency** | ExceptionGroup, TaskGroup, structured concurrency | `skills/software-dev/python-structured-concurrency/` |
| **tailscale-agent-network** | 7-layer agent communication via Tailscale + n8n + git | `skills/tailscale-agent-network/` |

## Research Documents

| Document | Description |
|----------|-------------|
| `RESEARCH.md` | Complete webmaster research (18KB) |

## How to Use

1. Read `RESEARCH.md` for the full picture
2. Load specific skill SKILL.md when needed
3. Follow the steps in each skill
4. Report results back to the owner

## Sharing

This entire directory is designed to be shared via:
- GitHub/GitLab repository
- Tailscale file sharing
- Git over Tailscale SSH

## Created

- **Date:** June 10, 2026
- **By:** Mingo (AI Agent Research Division) + Django research contributions
- **Version:** 1.0.0
- **Total Skills:** 13 (5 webmaster + 5 AI agent + 3 from evening research)
