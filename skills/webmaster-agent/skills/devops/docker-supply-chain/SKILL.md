---
name: docker-supply-chain-security
description: Docker image supply chain security — signing, scanning, SBOM generation, and multi-stage build hardening
version: 1.0.0
platforms: [linux, macos]
---

# Docker Image Supply Chain Security

## When to use
- Building production Docker images for customer deployments
- Setting up CI/CD pipelines pushing to container registries
- Auditing existing Docker images for vulnerabilities
- Securing Liberty Emporium customer machine agent deployments

## Key Principle
> "Never trust an image you didn't build, and always verify images before running them in production."

## Pipeline
```
Source → Dockerfile → Build → Scan → Sign → Push → Verify → Deploy
```

## Step 1: Harden Dockerfile
- Use multi-stage builds (build stage + minimal production stage)
- Pin base image digests (immutable references)
- Minimize layers and attack surface
- Run as non-root user
- Remove unnecessary binaries (/bin/sh, /bin/bash)

## Step 2: Docker Content Trust (DCT)
```bash
export DOCKER_CONTENT_TRUST=1
docker trust key generate my-org
docker trust signer add --key my-org.pub ci-signer my-org/app
docker trust sign my-org/app:v1.0.0
```

## Step 3: Vulnerability Scanning
- **Trivy** (recommended): `trivy image my-org/app:latest`
- **Grype**: `grype my-org/app:latest`
- Fail CI on HIGH/CRITICAL vulnerabilities

## Step 4: Image Signing with Cosign (Sigstore)
```bash
cosign generate-key-pair
cosign sign --key cosign.key my-org/app:v1.0.0
cosign verify --key cosign.pub my-org/app:v1.0.0
# Keyless signing (OIDC):
cosign sign my-org/app:v1.0.0
```

## Step 5: SBOM Generation
```bash
syft my-org/app:latest -o spdx-json > sbom.spdx.json
cosign attest --predicate sbom.spdx.json --key cosign.key my-org/app:v1.0.0
```

## Step 6: CI/CD Integration
- Build → Scan → Sign → Push → Verify before deploy
- Use GitHub Actions OIDC for registry auth
- Verify signatures before deployment

## Liberty Emporium Use Case
Securing customer machine agent deployments. Every agent Docker image should be signed and scanned.

## Source
Docker security docs + Sigstore/Cosign documentation.
Full version: `references/docker-supply-chain-full.md`
