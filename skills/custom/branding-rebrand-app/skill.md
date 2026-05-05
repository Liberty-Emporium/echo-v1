# Skill: branding-rebrand-open-source-app

## Purpose
Fork an open-source app, apply custom branding (name, colors, logos), and deploy it.

## Trigger Phrases
- "Rebrand this app", "Apply branding", "Put my logo on the app"
- "Change the name", "Replace the logo everywhere"
- "This app still has old branding"

## When to Use
- User wants to take an open-source project and make it their own
- Custom logo, name, colors need replacing throughout the codebase
- Project is deployed but still shows original branding

## Steps

### Phase 1: Fork & Clone
1. Fork the source repo to the target org via GitHub API:
   ```bash
   curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
     "https://api.github.com/repos/$OWNER/$REPO/forks"
   ```
2. Clone the fork locally:
   ```bash
   git clone "https://ghp_TOKEN@github.com/$OWNER/$REPO.git" project-branded
   ```

### Phase 2: Identify Branding Hotspots
Run this to find all branding references:
```bash
grep -ri "OLD_NAME\|oldlogo\|oldcolor\|olddomain" --include="*.ts" --include="*.tsx" --include="*.css" --include="*.html" --include="*.json" .
```

Common places branding hides:
- `package.json` — name, productName, author, description
- `electron-builder.yml` — appId, productName, executableName, copyright
- `src/renderer/index.html` — title, meta tags, theme-color
- `src/renderer/assets/` — logo PNG files
- `public/pwa/` — PWA icons
- `public/pet-states/` — animated mascot SVGs
- `src/renderer/components/layout/Layout.tsx` — sidebar logo (often inline SVG!)
- `src/renderer/components/layout/Titlebar/` — titlebar logo
- `src/renderer/pages/login/` — login page logo
- `.github/workflows/` — build workflow owner/repo references
- `resources/app-update.yml` — update server owner/repo
- `docs/` — documentation clone URLs

### Phase 3: Replace User-Facing Text
Do NOT replace internal technical identifiers (env vars, class names, MCP server names, file paths with old name in them) — only user-facing text:
- App title/name
- Brand colors (#OLD_COLOR → #NEW_COLOR)
- Author/company name
- URLs pointing to old domain
- Copyright notices

### Phase 4: Replace Visual Assets
1. **Logo PNGs**: Find `brand/app.png` or similar in `src/renderer/assets/` and replace with your logo (match dimensions)
2. **PWA Icons**: Replace `public/pwa/icon-*.png` with your logo resized to 180x180, 192x192, 512x512
3. **Inline SVGs**: Search for inline SVG logo code and replace with `<img src={loginLogo}>` using your PNG
4. **Favicon**: Replace `public/favicon.ico`
5. **Banner/hero images**: Replace gradient banners with your logo on brand color

### Phase 5: Update Build Configuration
```json
// package.json
{
  "name": "your-app-name",
  "productName": "Your App Name",
  "description": "Your app description"
}
```

```yaml
# electron-builder.yml
appId: com.yourcompany.yourapp
productName: Your App Name
executableName: YourApp
copyright: Copyright © 2024 Your Company
```

### Phase 6: Push
```bash
git add -A
git commit -m "feat: full rebrand to Your Brand Name"
git push origin main
```

### Phase 7: Deploy
```bash
# Railway
railway up

# GitHub Actions (if workflow exists)
git tag v1.0.0 && git push origin v1.0.0
```

## Branding Checklist
- [ ] package.json name, productName, description, author
- [ ] electron-builder.yml appId, productName, protocol
- [ ] src/renderer/index.html title, meta theme-color
- [ ] src/renderer/assets/logos/brand/app.png
- [ ] public/pwa/icon-*.png
- [ ] public/favicon.ico
- [ ] Inline SVG logos in Layout.tsx, Titlebar/index.tsx
- [ ] resources/app-update.yml owner/repo
- [ ] .github/workflows/ owner/repo references
- [ ] docs clone URLs
- [ ] README.md title and clone URL

## Notes
- **Keep internal identifiers alone** — env vars like `OLD_NAME_PORT`, class names `OldNameClient`, file paths `~/.oldname/`, repo names `aionui/hub` should NOT be changed or the app breaks
- **Theme color**: Search for `#OLD_COLOR` and replace with your brand color (e.g., `#00CCFF`)
- **GitHub Actions**: If the workflow hard-codes the old org/repo, update those references too

## Related Skills
- `railway-deploy` — for Railway deployment specifics
- `github-actions-build` — for triggering desktop builds via GitHub Actions