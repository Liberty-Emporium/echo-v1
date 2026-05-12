# Tailscale — Echo KiloClaw Remote Access
_Last updated: 2026-05-12_

## Overview
Tailscale is installed on the KiloClaw machine so I (Echo KiloClaw) can reach Jay's
computer(s) directly — and Jay's machines can reach me — over an encrypted private network.

## The Problem We Solved
Tailscale binaries don't survive container recreation (apt packages live on ephemeral
filesystem). State CAN persist if saved to `/root/.tailscale-state` (on the persistent
`/root` volume). But if the container is fully rebuilt from scratch, we need to re-auth.

## Solution: Self-Healing Setup

### Files
| Path | Purpose |
|------|---------|
| `/root/.secrets/tailscale_authkey` | Auth key for `tailscale up` (survives reboots) |
| `/root/.tailscale-state/` | Tailscale state dir (persistent volume) |
| `/usr/local/bin/tailscaled-start.sh` | Start script: installs if missing, starts daemon, re-auths if needed |
| Cron job `tailscaled-watchdog` | Runs every 60s — calls the start script, silent if OK |

### Watchdog Cron
- **Job ID:** da839d43-46df-4f52-a896-04d6eb3191db (may change on recreate)
- **Schedule:** Every 60 seconds
- **Mode:** isolated subagent, no delivery (silent)
- **What it does:** Runs `bash /usr/local/bin/tailscaled-start.sh`

### The Start Script Logic
1. If `tailscaled` binary missing → `curl https://tailscale.com/install.sh | sh`
2. If `tailscaled` process not running → start with userspace networking + statedir
3. If `tailscale status` shows "Logged out" → `tailscale up --authkey=$(cat authkey file)`

## Tailnet Info
- **Tailnet name:** tail5f8e8b.ts.net
- **Account:** Liberty-Emporium@github
- **This machine (KiloClaw):** `100.120.23.109` (hostname: `17812601a011e8` or similar)
- **Jay's Linux machine:** `100.123.226.4` (hostname: `mingo-to-be-filled-by-o-e-m`)
- **DERP region:** iad (Washington DC area)

## Auth Key Note
The auth key `tskey-auth-kwJBbBAg4P11CNTRL-...` is a **reusable** key tied to
Jay's Liberty-Emporium@github Tailscale account. It's stored at
`/root/.secrets/tailscale_authkey`. If it ever expires, Jay needs to generate
a new one from https://login.tailscale.com/admin/settings/keys and drop it in that file.

## Bootstrap Integration
On a fresh boot/container:
1. `bash /root/.openclaw/workspace/echo-v1/scripts/bootstrap.sh` runs
2. It calls `tailscaled-start.sh` (or the watchdog does within 60s)
3. Tailscale is back up with the same IP (if state persisted) or a new one

## What I Can Do Once Connected
- `tailscale ping 100.123.226.4` — confirm Jay's machine is reachable
- `ssh` into Jay's machine (if SSH is running there and port is open on Tailnet)
- Any TCP/UDP connection over the Tailnet to Jay's machine IP

## Session History
- **2026-05-12 ~04:00 EDT:** First setup — installed, connected as Liberty-Emporium@github, IP 100.64.184.111
- **2026-05-12 ~00:53 EDT:** Container recreated, binaries lost. Reinstalled. New IP: 100.120.23.109. Auth key stored persistently. Watchdog cron recreated.
