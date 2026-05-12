# Installer Reference — Liberty Agent Service Blocks

These are the exact code blocks to add to each installer when setting up Liberty Agent.
Copy-paste into the installer at the "Done" section, before the final success message.

---

## Hermes Linux/Mac (install.sh — bash)

```bash
# ─── Liberty Agent ────────────────────────────────────────────────────────────
cyan "→ Installing Liberty Agent (Alexander AI remote support)…"
LIBERTY_SCRIPT="$HOME/liberty_agent.py"
LIBERTY_URL="https://raw.githubusercontent.com/Liberty-Emporium/Hermes-Workspace-Alexander-AI/main/liberty_agent.py"

curl -fsSL "$LIBERTY_URL" -o "$LIBERTY_SCRIPT"
chmod +x "$LIBERTY_SCRIPT"
green "  Liberty Agent downloaded ✓"

python3 -m pip install "python-socketio[client]" websocket-client --quiet --break-system-packages 2>/dev/null || \
  python3 -m pip install "python-socketio[client]" websocket-client --quiet 2>/dev/null || true
green "  Python deps installed ✓"

# systemd (Linux)
if command -v systemctl &>/dev/null; then
  SVC_DIR="$HOME/.config/systemd/user"
  mkdir -p "$SVC_DIR"
  cat > "$SVC_DIR/liberty-agent.service" <<SYSTEMD_EOF
[Unit]
Description=Liberty Agent — Alexander AI Remote Support
After=network-online.target

[Service]
Type=simple
ExecStart=$(which python3) $LIBERTY_SCRIPT
Restart=always
RestartSec=15
Environment=LIBERTY_AGENT_TYPE=hermes
Environment=LIBERTY_PORTAL_URL=https://agent.install.alexanderai.site

[Install]
WantedBy=default.target
SYSTEMD_EOF
  systemctl --user daemon-reload 2>/dev/null
  systemctl --user enable liberty-agent 2>/dev/null
  systemctl --user restart liberty-agent 2>/dev/null && green "  Liberty Agent service started ✓" || true
fi

# Fallback: always ensure running now
if ! pgrep -f liberty_agent.py >/dev/null 2>&1; then
  mkdir -p "$HOME/.liberty-agent"
  nohup python3 "$LIBERTY_SCRIPT" >> "$HOME/.liberty-agent/agent.log" 2>&1 &
  green "  Liberty Agent running in background (PID: $!) ✓"
fi
```

---

## Hermes Windows (install-hermes-windows.ps1 — PowerShell)

```powershell
# -- Liberty Agent ------------------------------------------------------------
Write-Step "Installing Liberty Agent (Alexander AI remote support)..."
$libertyScript = "$env:USERPROFILE\liberty_agent.py"
$libertyUrl = "https://raw.githubusercontent.com/Liberty-Emporium/Hermes-Workspace-Alexander-AI/main/liberty_agent.py"
Invoke-WebRequest -Uri $libertyUrl -OutFile $libertyScript -UseBasicParsing
Write-OK "Liberty Agent downloaded"

pip install "python-socketio[client]" websocket-client --quiet 2>$null
Write-OK "Python deps installed"

$taskName = "LibertyAgent-AlexanderAI"
$pythonPath = (Get-Command python -ErrorAction SilentlyContinue)?.Source
if (-not $pythonPath) { $pythonPath = "python" }
$action   = New-ScheduledTaskAction -Execute $pythonPath -Argument $libertyScript
$trigger  = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit ([TimeSpan]::Zero) -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1)
try {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -RunLevel Highest -Force | Out-Null
    Write-OK "Liberty Agent scheduled task registered"
} catch { Write-Warn "Task failed - starting manually" }

$logDir = "$env:USERPROFILE\.liberty-agent"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }
$proc = Start-Process -FilePath $pythonPath -ArgumentList $libertyScript `
    -RedirectStandardOutput "$logDir\agent.log" -RedirectStandardError "$logDir\agent-err.log" `
    -WindowStyle Hidden -PassThru
Write-OK "Liberty Agent running in background (PID: $($proc.Id))"
```

---

## Agent Zero Linux/Mac (scripts/install-alexander-ai.sh — bash)

Same as Hermes Linux/Mac block above, but change:
- `LIBERTY_URL` → `https://raw.githubusercontent.com/Liberty-Emporium/Agent-Zero-Alexander-AI/main/liberty_agent.py`
- `LIBERTY_AGENT_TYPE=agent-zero` in the systemd unit

Also add macOS LaunchAgent block:
```bash
if [[ "$(uname)" == "Darwin" ]]; then
  PLIST_DIR="$HOME/Library/LaunchAgents"
  mkdir -p "$PLIST_DIR"
  cat > "$PLIST_DIR/ai.alexanderai.liberty-agent.plist" <<PLIST_EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key><string>ai.alexanderai.liberty-agent</string>
    <key>ProgramArguments</key>
    <array>
        <string>$(which python3)</string>
        <string>$LIBERTY_SCRIPT</string>
    </array>
    <key>EnvironmentVariables</key>
    <dict>
        <key>LIBERTY_AGENT_TYPE</key><string>agent-zero</string>
        <key>LIBERTY_PORTAL_URL</key><string>https://agent.install.alexanderai.site</string>
    </dict>
    <key>RunAtLoad</key><true/>
    <key>KeepAlive</key><true/>
</dict>
</plist>
PLIST_EOF
  launchctl load "$PLIST_DIR/ai.alexanderai.liberty-agent.plist" 2>/dev/null && green "  LaunchAgent loaded ✓" || true
fi
```

---

## OpenRouter Key Block (bash — for Linux/Mac installers)

```bash
# ─── OpenRouter API key ───────────────────────────────────────────────────────
cyan "→ Setting up OpenRouter API key…"
if grep -qE "^OPENROUTER_API_KEY=sk-or" "$INSTALL_DIR/.env" 2>/dev/null; then
  green "  OpenRouter API key already set ✓"
else
  echo ""
  yellow "  OpenRouter lets Hermes/Agent Zero talk to 100+ AI models (free tier available)."
  yellow "  Get your key at: https://openrouter.ai/keys"
  echo ""
  printf "  Paste your OpenRouter API key (or press Enter to skip): "
  read -r OR_KEY
  if [[ -n "$OR_KEY" ]]; then
    ensure_env_key "$INSTALL_DIR/.env" "OPENROUTER_API_KEY" "$OR_KEY"
    green "  OpenRouter API key saved ✓"
  else
    yellow "  Skipped — add later: echo 'OPENROUTER_API_KEY=sk-or-...' >> $INSTALL_DIR/.env"
  fi
fi
```

---

## OpenRouter Key Block (PowerShell — for Windows installers)

```powershell
Write-Step "Setting up OpenRouter API key..."
$envFile = "$installDir\.env"
$orAlreadySet = $false
if (Test-Path $envFile) {
    if ((Get-Content $envFile -Raw) -match "OPENROUTER_API_KEY=sk-or") {
        $orAlreadySet = $true; Write-OK "OpenRouter API key already set"
    }
}
if (-not $orAlreadySet) {
    Write-Warn "Get your key at: https://openrouter.ai/keys"
    $orKey = Read-Host "  Paste your OpenRouter API key (or press Enter to skip)"
    if ($orKey -ne "") {
        if (Test-Path $envFile) {
            $lines = Get-Content $envFile | Where-Object { $_ -notmatch "^OPENROUTER_API_KEY=" }
            $lines + "OPENROUTER_API_KEY=$orKey" | Set-Content $envFile
        } else { "OPENROUTER_API_KEY=$orKey" | Set-Content $envFile }
        Write-OK "OpenRouter API key saved"
    } else { Write-Warn "Skipped - add later in $envFile" }
}
```
