---
name: github-actions-oidc
description: GitHub Actions OIDC security — eliminate long-lived secrets from CI/CD pipelines using short-lived JWT tokens
version: 1.0.0
platforms: [linux, macos, windows]
---

# GitHub Actions OIDC Security

## When to use
- Deploying from GitHub Actions to AWS, Azure, GCP, or Railway
- Any workflow currently using long-lived secrets (AWS keys, etc.)
- Securing deployment pipelines for customer apps

## Key Benefit
No secrets to rotate, no credentials to leak. OIDC tokens are short-lived (minutes) and scoped to a specific workflow run.

## How OIDC Works
```
GitHub Actions → requests OIDC token → GitHub OIDC Provider
→ issues JWT (short-lived, scoped) → Cloud Provider validates
→ checks: repo, branch, workflow, environment
→ issues temporary credentials → deployment
```

## Setup Steps

### AWS OIDC
1. Create OIDC Identity Provider in AWS IAM
2. Create IAM Role with trust policy (scope to specific repo/branch)
3. Use `aws-actions/configure-aws-credentials@v4` in workflow

### Azure OIDC
1. Create App Registration
2. Use `azure/login@v2` with client/tenant/subscription IDs
3. These are public identifiers, not secrets

### GCP OIDC
1. Create Workload Identity Pool
2. Use `google-github-actions/auth@v2`

## Key Security Points
- Tokens are scoped to specific repo, branch, environment
- No long-lived secrets in GitHub
- Trust policies can restrict which workflows get access
- Tokens auto-expire after minutes

## Liberty Emporium Use Case
Secure deployment pipelines for customer apps. Replace all hardcoded API keys with OIDC.

## Source
GitHub Actions security hardening documentation.
Full version: `references/github-actions-oidc-full.md`
