# PureClaw Connect — Installation & Usage Guide

## Prerequisites

- A PureClaw server (provisioned with a `gateway_token`)
- PureClaw backend running with Pipedream credentials configured

## How It Works

Your PureClaw server already has a `gateway_token` — that's all the skill needs. No extra setup, no API keys to generate, no config files to create. The backend resolves the token to your server and handles all Pipedream communication.

## Installation

Copy the `pureclaw-connect` skill folder to your PureClaw server's skills directory:

```bash
mkdir -p /path/to/skills
cp -r pureclaw-connect /path/to/skills/pureclaw-connect
```

The directory should contain:

```
pureclaw-connect/
  SKILL.md
  INSTALL.md
  _meta.json
```

## Running the Skill

The skill is instruction-based — the agent reads `SKILL.md` and uses its commands via `curl` against your PureClaw backend. The agent needs two environment variables from the server config:

```bash
export BACKEND_URL="https://be.paioclaw.ai"
export GATEWAY_TOKEN="mWPzkdOSV37FK0RWKS3YFSbHkaUAYscifD7UyJgvVLXTldyS"
```

These are already available on every provisioned PureClaw server.

## First-Time Usage: Connect an App

Once the skill is installed, tell the agent:

> "Connect my Gmail account"

The agent will:
1. Call `POST /api/connectors/token?app=gmail` with your gateway token
2. Get back an OAuth authorization link
3. Show you the link — click it, authorize Gmail in your browser
4. Verify the connection with `GET /api/connectors/accounts?app=gmail`

Done. Gmail is now connected to this server.

## Everyday Usage

After apps are connected, just talk naturally:

> "Send a Slack message to #general saying the deploy is done"

> "Read my latest Gmail emails"

> "Create a row in my Google Sheet"

> "What apps do I have connected?"

The agent handles the rest — finding the right tool, calling the API, returning the result.

## Multi-Server Isolation

Each PureClaw server has its own set of connected accounts. If you have Server A and Server B, connecting Gmail on Server A does NOT affect Server B. They are completely independent.

## Troubleshooting

**401 errors on any call:** The gateway token is invalid or the server doesn't exist. Check that the server is provisioned and active.

**"pipedream_not_configured" error:** The PureClaw backend doesn't have Pipedream credentials set. Contact your admin to configure `PIPEDREAM_CLIENT_ID`, `PIPEDREAM_CLIENT_SECRET`, `PIPEDREAM_PROJECT_ID`, and `PIPEDREAM_PROJECT_ENVIRONMENT`.

**OAuth link expired:** OAuth links last 4 hours. Ask the agent to generate a fresh one.

**App not showing in accounts after authorization:** Wait a moment and re-check. If it still doesn't appear, generate a new OAuth link and try again.

## Uninstall

```bash
rm -rf /path/to/skills/pureclaw-connect
```

This removes the skill only. Connected Pipedream accounts remain active on the backend until revoked.
