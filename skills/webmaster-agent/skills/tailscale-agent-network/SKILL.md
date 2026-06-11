---
name: tailscale-agent-network
description: Complete agent-to-agent communication system using Tailscale — combines SSH, Serve, file sharing, git sync, n8n workflows, and skill distribution across a Tailnet
version: 1.0.0
platforms: [linux, macos, windows]
---

# Tailscale Agent Network — Complete Communication System

## When to use
- Setting up agent-to-agent communication across separate machines
- Sharing skills, files, and research between agents
- Coordinating multi-agent work across a Tailnet
- Automating cross-machine workflows

## Overview

This skill combines research from two sources:
1. **Tailscale research** — SSH, Serve, ACLs, identity-based access
2. **Agent framework research** — n8n automation, CrewAI patterns, skill sharing, structured communication

The result: a complete system for agents to communicate, share knowledge, and coordinate work across any network.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    TAILSCALE TAILNET                      │
│                                                          │
│  ┌──────────┐    Tailscale SSH     ┌──────────┐         │
│  │  MINGO   │◄────────────────────►│  DJANGO  │         │
│  │ (Ubuntu) │                      │ (Ubuntu) │         │
│  └────┬─────┘                      └────┬─────┘         │
│       │                                  │               │
│       │  ┌──────────────────────────┐    │               │
│       └──┤   SHARED RESOURCES       ├────┘               │
│          │                          │                     │
│          │  • Git repo (skills)     │                     │
│          │  • n8n workflows         │                     │
│          │  • File share (Serve)    │                     │
│          │  • Telegram (Jay ↔ All)  │                     │
│          └──────────────────────────┘                     │
└─────────────────────────────────────────────────────────┘
```

## Layer 1: Direct Agent Communication (Tailscale SSH)

### Enable on All Machines
```bash
sudo tailscale set --ssh
```

### Agent-to-Agent Command Execution
```bash
# Mingo asks Django to run a command
tailscale ssh django@django-machine "cd /project && git status"

# Django shares research findings
tailscale ssh mingo@mingo-machine "cat /home/mingo/reports/latest.md"
```

### ACL Policy (Tailscale Admin Console)
```json
{
  "ssh": [
    {
      "action": "accept",
      "src": ["group:agents"],
      "dst": ["tag:servers"],
      "users": ["autogroup:nonroot", "root"]
    }
  ],
  "acls": [
    {
      "action": "accept",
      "src": ["group:agents"],
      "dst": ["tag:servers:*"]
    }
  ],
  "tagOwners": {
    "tag:servers": ["group:agents"],
    "tag:agents": ["group:agents"]
  }
}
```

## Layer 2: Skill Sharing (Git-Based)

### Shared Skill Repository Structure
```
agent-skills/                          # Git repo (GitHub or GitLab)
├── README.md                          # Index of all skills
├── webmaster/
│   ├── monitoring/SKILL.md
│   ├── security/SKILL.md
│   ├── tailscale/SKILL.md
│   ├── backup/SKILL.md
│   └── skill-sharing/SKILL.md
├── ai-agents/
│   ├── handoffs/SKILL.md
│   ├── llm-resilient-api/SKILL.md
│   └── multi-agent-coordination/SKILL.md
├── devops/
│   ├── github-actions-oidc/SKILL.md
│   └── docker-supply-chain/SKILL.md
└── software-dev/
    └── python-structured-concurrency/SKILL.md
```

### Sync Protocol
```bash
# Agent pushes new skill
cd ~/agent-skills
cp -r /path/to/new-skill ./skills/
git add . && git commit -m "Add skill: name"
git push origin main

# Other agent pulls updates
cd ~/agent-skills && git pull origin main
```

### Conflict Resolution
- Never edit the same skill simultaneously
- Use branches for major changes: `git checkout -b skill-update`
- Merge via pull request (review by other agent)

## Layer 3: File Sharing (Tailscale Serve)

### Share Research Reports
```bash
# On the machine hosting reports:
tailscale serve --bg file:///home/mingo/reports/

# Other agents access via:
curl http://mingo.tailnet.ts.net:443/latest-report.md
```

### Share Manim Renders
```bash
tailscale serve --bg file:///home/mingo/trifecta-light/media/
# Access: http://mingo.tailnet.ts.net:443/videos/animation/480p15/
```

## Layer 4: Automated Workflows (n8n)

### Deploy n8n (Self-Hosted, Free)
```bash
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  --restart unless-stopped \
  n8nio/n8n
```

### Connect n8n to Telegram
1. Create Telegram bot via @BotFather
2. Add Telegram Trigger node in n8n
3. Add AI Agent node (with memory)
4. Connect to OpenRouter API (free tier)

### n8n Workflow: Agent Task Routing
```
Telegram Message → n8n Webhook → AI Agent Node
  → Analyze intent
  → Route to correct agent via Tailscale SSH
  → Execute task
  → Return result to Telegram
```

### n8n Workflow: Skill Distribution
```
New skill created → Git push trigger
  → n8n webhook receives event
  → Notify other agent via Tailscale SSH
  → Other agent pulls update
  → Confirm sync via Telegram
```

## Layer 5: Structured Communication Protocol

### Message Format (Agent-to-Agent)
```
[FROM: Mingo] [TO: Django] [TYPE: research_share]
[TIMESTAMP: 2026-06-10T10:30:00-04:00]
[TOPIC: tailscale_network_optimization]

BODY:
Finding: Tailscale SSH reduces agent communication latency by 40%
compared to traditional SSH (no key management overhead).
Recommendation: Enable Tailscale SSH on all agent machines.

VERIFICATION: Tested on mingo → django-machine (2ms latency)
```

### Message Types
| Type | Purpose | Response Expected |
|------|---------|-------------------|
| `research_share` | Share research findings | Acknowledgment |
| `task_request` | Ask another agent to do work | Status update |
| `skill_update` | Notify of new/updated skill | Pull confirmation |
| `alert` | Urgent issue requiring attention | Immediate action |
| `status` | Routine status update | None required |

### Coordination Rules (from CrewAI research)
1. **One speaker per message** — If your name is mentioned, you respond. Others stay silent.
2. **Tag your sender** — Always mark which agent produced work.
3. **No duplicate work** — Before starting a task, check if another agent is already doing it.
4. **Shared state is in pinned messages** — Important context lives in Telegram pins.
5. **When in doubt, ask** — Don't guess about what another agent is doing.

## Layer 6: Monitoring & Health (Cross-Machine)

### Health Check All Agents
```bash
#!/bin/bash
# Run on any machine to check all agents in tailnet

AGENTS=("mingo@mingo-machine" "django@django-machine")

for agent in "${AGENTS[@]}"; do
  echo "=== $agent ==="
  tailscale ssh "$agent" "
    uptime | awk '{print \"Uptime:\" \$NF}'
    df -h / | tail -1 | awk '{print \"Disk:\" \$5}'
    free -m | grep Mem | awk '{printf \"Memory: %d/%dMB (%.0f%%)\", \$3, \$2, \$3/\$2*100}'
    echo ""
    systemctl is-active nginx 2>/dev/null && echo \"nginx: active\" || echo \"nginx: inactive\"
    systemctl is-active docker 2>/dev/null && echo \"docker: active\" || echo \"docker: inactive\"
  " 2>/dev/null
  echo ""
done
```

### UptimeRobot Integration (Free)
- Monitor each agent's gateway endpoint
- Alert via Telegram when agent goes down
- 50 free monitors (enough for 50 endpoints)

## Layer 7: Security

### Security Rules for Agent Communication
1. **Tailscale SSH only** — Never expose SSH to public internet
2. **ACLs enforced** — Only agents group can access servers group
3. **No secrets in transit** — All traffic encrypted via WireGuard
4. **Credential files only** — Read API tokens from ~/Desktop/credentials/
5. **No hardcoded secrets** — Use environment variables for everything
6. **Audit trail** — Log all agent-to-agent commands

### Security Scanning (from Django's research)
```bash
# Run on each agent machine weekly
sudo apt install lynis
sudo lynis audit system

# Docker security (if using Docker)
docker scout cves my-org/app:latest
```

## Implementation Checklist

### Initial Setup (One-Time)
- [ ] Install Tailscale on all agent machines
- [ ] Enable Tailscale SSH: `sudo tailscale set --ssh`
- [ ] Configure ACL policies in Tailscale admin
- [ ] Create shared Git repo for skills
- [ ] Clone skill repo on all machines
- [ ] Set up n8n (optional, for workflow automation)
- [ ] Test agent-to-agent SSH connectivity
- [ ] Test skill sync via git

### Ongoing Operations
- [ ] Daily: `git pull` on skill repo (all agents)
- [ ] Weekly: Security scan on all machines
- [ ] Weekly: Review and update ACL policies
- [ ] Monthly: Rotate Tailscale node keys
- [ ] As needed: Create and share new skills

## Research Sources

### Tailscale Research (Mingo)
- Tailscale SSH documentation
- Tailscale Serve/Funnel documentation
- OpenClaw + Tailscale integration guide
- Agent-to-agent communication patterns

### Agent Framework Research (Django)
- n8n workflow automation (34K+ GitHub stars)
- CrewAI role-based multi-agent patterns
- AutoGen (Microsoft) enterprise multi-agent
- LangGraph stateful agent workflows
- OpenClaw skill-based architecture (150K+ stars)
- SOL framework (self-initiated open world learning)
- LLM resilient API patterns (retry, backoff, circuit breaker)
- Docker supply chain security (Trivy, Cosign, SBOM)
- GitHub Actions OIDC (eliminate long-lived secrets)
- Python structured concurrency (ExceptionGroup, TaskGroup)

## Pitfalls
- Don't enable Tailscale SSH without ACLs — anyone in the tailnet could access
- Don't store credentials in git — use environment variables
- Don't run n8n exposed to public internet — use Tailscale Serve
- Don't let agents edit the same skill file simultaneously
- Always test ACL changes before applying to production
- Monitor Tailscale status — if Tailscale goes down, agent communication stops

## Verification
```bash
# Test Tailscale connectivity
tailscale status
tailscale ping django-machine

# Test SSH between agents
tailscale ssh django@django-machine "echo 'Agent communication OK'"

# Test skill sync
cd ~/agent-skills && git pull && echo "Skills synced"

# Test file sharing
curl -I http://django-machine.tailnet.ts.net:443/README.md
```
