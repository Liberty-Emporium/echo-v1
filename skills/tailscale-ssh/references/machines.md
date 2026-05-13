# Liberty-Emporium Tailnet — Known Machines

## How to Check Current Status
```bash
tailscale status
```

## Known Machines

| IP | Hostname | User | OS | Notes |
|----|----------|------|----|-------|
| 100.89.104.22 | kiloclaw-echo | root | Linux | KiloClaw itself |
| 100.120.23.109 | hermes-server | root | Linux | Hermes Docker container |
| 100.123.226.4 | jay-upstairs | - | - | Jay's main machine (upstairs) — offline when not in use |
| 100.88.205.44 | kali | lol | Kali Linux | Jay's Kali machine (downstairs/browser-test-env) |
| 100.100.48.77 | unknown-1 | - | Linux | Offline — identity TBD |
| 100.64.184.111 | unknown-2 | - | Linux | Offline — identity TBD |

## SSH Connection Method

KiloClaw runs Tailscale in **userspace networking mode** — direct TCP to Tailscale IPs doesn't work.
Must route through the SOCKS5 proxy at `localhost:1055`.

```bash
ssh -o ProxyCommand="nc -x localhost:1055 %h %p" \
    -o StrictHostKeyChecking=no \
    -i ~/.ssh/id_ed25519 \
    <user>@<tailscale-ip> "<command>"
```

## First-Time Setup on a New Machine

1. Install Tailscale: `curl -fsSL https://tailscale.com/install.sh | sh`
2. Start daemon: `sudo systemctl start tailscaled`
3. Authenticate: `sudo tailscale up --authkey=<key from /root/.secrets/tailscale_authkey>`
4. Start SSH: `sudo systemctl start ssh`
5. Open firewall: `sudo iptables -I INPUT -i tailscale0 -p tcp --dport 22 -j ACCEPT`
6. Plant key: have user run the command from `plant_key.sh`

## Firewall Gotcha (Kali Linux)

Kali blocks SSH on tailscale0 by default. If SSH times out:
```bash
sudo iptables -P INPUT ACCEPT && sudo iptables -F INPUT
```
Or more targeted:
```bash
sudo iptables -I INPUT -i tailscale0 -p tcp --dport 22 -j ACCEPT
```

## Common Tasks

### Run a command remotely
```bash
bash scripts/remote.sh lol@100.88.205.44 "your command here"
```

### Copy a script over and run it
```bash
cat > /tmp/task.sh << 'EOF'
#!/bin/bash
# your commands here
EOF
bash scripts/copy_to.sh /tmp/task.sh lol@100.88.205.44:/tmp/task.sh
bash scripts/remote.sh lol@100.88.205.44 "bash /tmp/task.sh"
```

### Check what's installed
```bash
bash scripts/remote.sh lol@100.88.205.44 "which hermes && hermes --version || echo not installed"
```
