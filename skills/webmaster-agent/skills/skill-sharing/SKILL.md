---
name: agent-skill-sharing
description: How to create, share, and maintain AI agent skills across multiple agents using git and Tailscale
version: 1.0.0
platforms: [linux, macos, windows]
---

# Agent Skill Sharing Skill

## When to use
- Creating a new skill to share with other agents
- Setting up a shared skill repository
- Distributing skills across machines via Tailscale
- Version controlling agent knowledge

## The SKILL.md Format

Every skill starts with a SKILL.md file:

```markdown
---
name: skill-name
description: One-line description of what this does
version: 1.0.0
platforms: [linux, macos, windows]
---

# Skill Title

## When to use
Trigger conditions — when should an agent load this skill?

## Steps
1. First step with exact commands
2. Second step
3. Third step

## Pitfalls
- What goes wrong
- How to avoid common mistakes

## Verification
How to confirm the skill worked correctly
```

## Skill Repository Structure

```
agent-skills/
├── README.md                    # Index of all skills
├── webmaster/
│   ├── SKILL.md                 # Main skill file
│   ├── skills/
│   │   ├── monitoring/SKILL.md
│   │   ├── security/SKILL.md
│   │   ├── backup/SKILL.md
│   │   └── tailscale/SKILL.md
│   ├── scripts/
│   │   ├── health-check.sh
│   │   ├── backup.sh
│   │   └── security-scan.sh
│   └── references/
│       └── nginx-hardening.md
├── development/
│   ├── SKILL.md
│   └── scripts/
└── monitoring/
    ├── SKILL.md
    └── scripts/
```

## Method 1: GitHub/GitLab (Recommended)

### Setup
```bash
# Create repository on GitHub/GitLab first, then:
git clone https://github.com/your-org/agent-skills.git
cd agent-skills

# Add skills
git add .
git commit -m "Add webmaster monitoring skill"
git push origin main
```

### Agent Pull Updates
```bash
cd ~/agent-skills
git pull origin main
```

### Agent Push New Skill
```bash
cd ~/agent-skills
cp -r /path/to/new-skill ./skills/
git add .
git commit -m "Add new skill: skill-name"
git push origin main
```

## Method 2: Tailscale File Sharing

```bash
# On the machine hosting skills:
tailscale serve --bg file:///home/agent/skills/

# On other machines, access via:
curl http://skill-server.tailnet.ts.net:443/webmaster/SKILL.md
```

## Method 3: Git Over Tailscale SSH

```bash
# Clone directly between machines on the same tailnet
git clone agent@skill-server:~/agent-skills.git

# Push updates
git push agent@skill-server:~/agent-skills.git main
```

## Skill Quality Checklist

Before sharing a skill, verify:

- [ ] YAML frontmatter is valid (name, description, version)
- [ ] "When to use" section is clear
- [ ] Steps are numbered and have exact commands
- [ ] Pitfalls section covers common mistakes
- [ ] Verification section tells how to confirm success
- [ ] No hardcoded secrets (use environment variables)
- [ ] Scripts are tested on a clean system
- [ ] README updated with new skill

## Versioning

Use semantic versioning in SKILL.md frontmatter:
- **1.0.0** — Initial release
- **1.1.0** — Added new features, backward compatible
- **2.0.0** — Breaking changes

## Pitfalls
- Don't share skills with hardcoded credentials
- Always test on a clean system before publishing
- Keep skills focused — one skill = one capability
- Document dependencies (what tools need to be installed)
- Use relative paths in scripts, not absolute

## Verification
```bash
# Validate YAML frontmatter
python3 -c "
import yaml, sys
with open('SKILL.md') as f:
    content = f.read()
    _, fm, _ = content.split('---', 2)
    data = yaml.safe_load(fm)
    print(f'Name: {data.get(\"name\")}')
    print(f'Version: {data.get(\"version\")}')
    print(f'Valid: OK')
"

# Test all scripts in skill
bash -n scripts/health-check.sh  # Syntax check
```
