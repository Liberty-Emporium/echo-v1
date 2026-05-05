# Skill: github-actions-desktop-build

## Purpose
Build cross-platform desktop installers (Windows, macOS, Linux) using GitHub Actions.

## Trigger Phrases
- "Build for Windows", "Build for Mac", "Build desktop apps"
- "Download the app installer", "Get me the .exe"
- "Build failed on macOS", "Fix the GitHub build"
- "Create release", "Publish desktop app"

## When to Use
- User wants native desktop installers for an Electron app
- GitHub Actions build failed and needs fixing
- Need to trigger builds for all platforms or specific platform
- Build artifacts need to be published as a GitHub release

## Steps

### Step 1: Check Existing Workflow
```bash
# Look for existing workflow
ls .github/workflows/
cat .github/workflows/build-and-release.yml
```

### Step 2: Trigger the Build
```bash
# Via GitHub CLI (if authenticated)
gh workflow run BUILD-WORKFLOW-NAME --repo OWNER/REPO

# Via API
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Content-Type: application/vnd.github+json" \
  "https://api.github.com/repos/OWNER/REPO/actions/workflows/WORKFLOW_ID/dispatches" \
  -d '{"ref":"main","inputs":{"branch":"main","platform":"all","skip_code_quality":true}}'

# Via tag push (if workflow triggers on tags)
git tag v1.0.0 && git push origin v1.0.0
```

### Step 3: Monitor Build Progress
```bash
# Check run status
gh run list --repo OWNER/REPO --limit=5

# Watch a specific run
gh run watch RUN_ID --repo OWNER/REPO

# Get job details
gh api repos/OWNER/REPO/actions/runs/RUN_ID/jobs
```

### Step 4: Common Build Failures

**macOS fails with "electron-builder" error:**
- Usually missing code signing credentials
- Fix: Set `MAC_CERTIFICATE` and `KEYCHAIN_PASSWORD` secrets in repo settings
- OR: Use `--mac.sign=false` flag in electron-builder args

**Linux ARM64 fails:**
- Check if target architecture is supported by the base image
- Try `--linux.target=deb` only (skip AppImage)

**Build succeeds but artifacts missing:**
- Artifacts only downloadable after creating a GitHub Release
- Create release from workflow or manually after build

### Step 5: Download Build Artifacts
1. Go to: `https://github.com/OWNER/REPO/actions`
2. Click the run → Artifacts section
3. Download `.zip` for your platform

### Step 6: Publish as GitHub Release
```bash
# Create a release from a tag
gh release create v1.0.0 \
  --title "Your App v1.0.0" \
  --notes "Release notes" \
  --repo OWNER/REPO
```

## Build Platforms (Electron)
| Platform | Output |
|----------|--------|
| Windows x64 | `.exe` (NSIS installer) |
| Windows ARM64 | `.exe` |
| macOS x64 | `.dmg` |
| macOS ARM64 | `.dmg` |
| Linux x64 | `.deb`, `.AppImage` |
| Linux ARM64 | `.deb`, `.AppImage` |

## Build Commands Reference
```bash
# Electron build
bun run build:electron

# electron-builder (package for distribution)
electron-builder --mac --linux --win

# Single platform
electron-builder --mac
electron-builder --win
electron-builder --linux

# With options
electron-builder --mac --mac.sign=false
```

## GitHub Actions Workflow Structure
```yaml
jobs:
  build:
    strategy:
      matrix:
        include:
          - platform: macos-arm64
          - platform: macos-x64
          - platform: windows-x64
          - platform: windows-arm64
          - platform: linux-x64
          - platform: linux-arm64
    runs-on: ${{ matrix.platform }}
    steps:
      - uses: actions/checkout@v4
      - uses: oven/bun@v1
        with: bun-version: 1.26.0
      - run: bun install
      - run: bun run build:electron
      - run: bunx electron-builder --${{ matrix.platform }}
```

## Notes
- Build runs on GitHub-hosted runners (no local machine needed)
- macOS builds need Apple Developer credentials for signed builds
- Linux ARM64 builds may fail on some GitHub runner images
- Build time: ~15-20 min for all platforms

## Related Skills
- `branding-rebrand-app` — for applying branding before build
- `railway-deploy-fix` — for web deployment issues