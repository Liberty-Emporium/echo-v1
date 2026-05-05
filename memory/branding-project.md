# Branding Project

## Status: LIVE

## Current State
- **EcDash web app:** https://aionui-1-production.up.railway.app
- **Repo:** https://github.com/Liberty-Emporium/AionUi-1
- **Desktop builds:** GitHub Actions workflow running (all 6 platforms)
- **Web pet widget:** ✅ Pushed and deployed via Railway

## Done
- [x] Fork AionUi → Liberty-Emporium/AionUi-1
- [x] Clone to /home/lol/Downloads/11/AionUi-branded
- [x] Full rebrand (AionUi → Alexander AI Solutions) - 916 files
- [x] Theme color #00CCFF applied everywhere
- [x] Package name: ecdash, App ID: com.libertyemporium.ecdash
- [x] ADMIN_PASSWORD env var support added to AuthService
- [x] VOLUME instruction removed (Railway fix)
- [x] Web pet widget (floating SVG companion) added for Railway
- [x] CNAME: agent.ecjayalexanderai.site → aionui-1-production.up.railway.app

## Build Status
- Railway: Live (Alexander AI Solutions branded)
- GitHub Actions: BUILD-MANUAL workflow triggered (all platforms)
  - macOS ARM64 + x64
  - Windows x64 + ARM64
  - Linux x64 + ARM64

## Target
- **Project:** AionUi (https://github.com/iOfficeAI/AionUi)
- **Goal:** Fork to Liberty-Emporium, apply Jay's branding
- **Status:** COMPLETE

## Jay's Brand
- **Primary Color:** #00CCFF (cyan)
- **Logo Card:** /home/lol/Pictures/Front of Card.png
- **Company:** Liberty-Emporium / Alexander AI Integrated Solutions
- **App Name:** EcDash (control plane), plus individual apps

## Notes
- The app is Electron-based, resources in app.asar
- Web pet widget mirrors desktop pet behavior for Railway (web) deployments
- PetEventEmitter bridges pet state machine → WebSocket → WebPetWidget