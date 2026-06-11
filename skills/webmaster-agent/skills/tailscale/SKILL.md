---
name: tailscale-agent
description: Tailscale networking for AI agents — secure remote access, SSH, and cross-network coordination
version: 1.0.0
platforms: [linux, macos, windows]
---

# Tailscale Agent Networking Skill

## When to use
- Setting up secure remote access between machines
- Managing SSH across multiple servers
- Connecting agents across different networks
- Exposing agent gateways securely

## What is Tailscale?

Tailscale creates a **private encrypted mesh network** (Tailnet) between devices using WireGuard. For AI agents, it's the backbone of secure cross-machine operations.

**Key concepts:**
- **Tailnet** — Your private network of devices
- **MagicDNS** — Automatic DNS names for devices (e.g., `server.tailnet-name.ts.net`)
- **Tailscale SSH** — Identity-based SSH (no keys to manage)
- **ACLs** — Access control policies
- **Serve/Funnel** — Expose services on the tailnet

## Installation

```bash
# Linux
curl -fsSL https://tailscale.com/install.sh | sh

# Start and authenticate
sudo tailscale up

# Check status
tailscale status
```

## Tailscale SSH (Recommended for Agents)

### Enable on Host
```bash
sudo tailscale set --ssh
```

### Connect from Another Machine
```bash
# Using Tailscale SSH (identity-based, no keys)
tailscale ssh user@hostname

# Or via regular SSH through Tailscale IP
ssh user@100.x.x.x
```

### ACL Policy for Agent Access

Add to your tailnet policy (ACLs page in Tailscale admin):

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

## Tailscale Serve (Expose Agent Gateway)

```json5
// In gateway.yaml or agent config
{
  gateway: {
    bind: "loopback",
    tailscale: {
      mode: "serve",
      resetOnExit: true
    }
  }
}
```

Access at: `https://hostname.tailnet-name.ts.net/`

## Agent-to-Agent Communication Pattern

### Method 1: Tailscale SSH
```bash
# From Agent A to Agent B
tailscale ssh agent@machine-b "cd /project && git pull && npm run build"
```

### Method 2: Git-Based Sync
```bash
# Shared skill repository
git clone https://github.com/your-org/agent-skills.git
# Agents push/pull skills as needed
```

### Method 3: Tailscale File Sharing
```bash
# Serve a directory
tailscale serve --bg file:///home/agent/shared/

# Access from another machine
curl http://machine.tailnet-name.ts.net:443/skills/webmaster/SKILL.md
```

## Multi-Machine Monitoring

```bash
#!/bin/bash
# Monitor all machines in tailnet

MACHINES=("web-server" "db-server" "backup-server")

for machine in "${MACHINES[@]}"; do
  echo "=== $machine ==="
  tailscale ssh agent@$machine "uptime && df -h / && free -m" 2>/dev/null
  echo ""
done
```

## Best Practices

1. **Use tags** to group machines (tag:web, tag:db, tag:agents)
2. **Use groups** to manage access (group:agents, group:admins)
3. **Set `resetOnExit: true`** for Serve mode
4. **Use `check` action** for sensitive SSH (requires re-auth)
5. **Never use Funnel** for agent-to-agent communication
6. **Monitor Tailscale status** — include in daily health checks
7. **Keep Tailscale updated** — `sudo tailscale up --accept-routes`

## Troubleshooting

```bash
# Check status
tailscale status

# Check DNS
tailscale dns status

# Ping a peer
tailscale ping hostname

# Check routes
tailscale routes list

# Restart
sudo tailscale down && sudo tailscale up

# Debug
tailscale bugreport
```

## Pitfalls
- Don't enable Tailscale SSH on production without testing ACLs first
- `check` mode breaks automation — use `accept` for agent-to-agent
- Tailscale Funnel only works on ports 443, 8443, 10000
- MagicDNS requires HTTPS enabled on tailnet
- Always test access after changing ACLs

## Verification
```bash
# Verify Tailscale is running
tailscale status

# Test SSH to a peer
tailscale ssh user@hostname "echo connected"

# Test Serve mode
curl -I https://hostname.tailnet-name.ts.net/
```
