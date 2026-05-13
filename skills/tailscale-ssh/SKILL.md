---
name: tailscale-ssh
description: Remote into any machine on Jay's Liberty-Emporium Tailscale network via SSH to run commands, install/uninstall software, fix problems, or do maintenance. Use when Jay asks to remote into a computer, connect to a machine, run something remotely, fix a customer machine, or do anything on a specific machine by hostname or IP. Also use for tasks like "uninstall X from my computer", "check what's running on the server", or "fix the issue on my Kali box".
---

# Tailscale SSH — Remote Machine Access

KiloClaw runs Tailscale in **userspace networking mode** — direct TCP to Tailscale IPs doesn't work. Must always route through SOCKS5 proxy at `localhost:1055`.

## Quick Reference

```bash
# Run a command on a remote machine
bash /root/.openclaw/workspace/echo-v1/skills/tailscale-ssh/scripts/remote.sh <user>@<ip> "command"

# Copy a file to remote machine
bash /root/.openclaw/workspace/echo-v1/skills/tailscale-ssh/scripts/copy_to.sh /local/file user@ip:/remote/path

# Get key-plant command for a new machine
bash /root/.openclaw/workspace/echo-v1/skills/tailscale-ssh/scripts/plant_key.sh <user> <ip>
```

## Workflow

### 1. Check Tailnet status
```bash
tailscale status
```
See `references/machines.md` for known machines and their IPs/users.

### 2. Identify the target machine
Match what Jay says ("my Kali box", "the server downstairs", "my upstairs computer") to the machines table in `references/machines.md`.

### 3. Ensure SSH key exists
```bash
ls ~/.ssh/id_ed25519 || ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N "" -C "kiloclaw@liberty-emporium.ai"
```

### 4. Ensure nc is installed
```bash
command -v nc || apt-get install -y netcat-openbsd -q
```

### 5. Connect and run
For simple commands:
```bash
bash scripts/remote.sh user@ip "command"
```

For multi-step tasks, write a script locally → SCP it over → execute it:
```bash
cat > /tmp/task.sh << 'EOF'
#!/bin/bash
# commands here
EOF
bash scripts/copy_to.sh /tmp/task.sh user@ip:/tmp/task.sh
bash scripts/remote.sh user@ip "bash /tmp/task.sh"
```

**Why scripts instead of heredocs?** SSH + heredocs with complex quoting fails silently. Always use the copy-then-execute pattern for multi-step tasks.

## First-Time Access to a New Machine

If the machine is new (not in `references/machines.md`) or SSH key not yet planted:

1. **Get Tailscale connected** — ask Jay to run:
   ```bash
   curl -fsSL https://tailscale.com/install.sh | sh
   sudo systemctl start tailscaled
   sudo tailscale up --authkey=$(cat /root/.secrets/tailscale_authkey)
   ```
2. **Start SSH** — ask Jay to run: `sudo systemctl start ssh`
3. **Plant the key** — run `plant_key.sh` to get the exact command, then ask Jay to paste it
4. **Test connection** — `bash scripts/remote.sh user@ip "whoami"`
5. **Update machines.md** with the new machine details

## Troubleshooting

**SSH times out** → Firewall blocking port 22 on tailscale0. Ask Jay:
```bash
sudo iptables -I INPUT -i tailscale0 -p tcp --dport 22 -j ACCEPT
```

**"tailscale: command not found"** → Install real Tailscale. `python3-tailscale` (Kali apt) is a fake Python library, not the actual daemon. Remove it first: `sudo apt remove python3-tailscale && sudo apt install tailscale`

**Tailscale ping works but SSH times out** → Userspace mode SOCKS5 issue. Confirm using `ProxyCommand="nc -x localhost:1055 %h %p"` in all SSH calls.

**"Permission denied (publickey)"** → Key not planted yet. Run `plant_key.sh` and have Jay add the key.

## Known Machines
See `references/machines.md` for full machine list with IPs, users, and notes.
