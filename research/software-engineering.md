# Software Engineering — Research Notes
**Researched:** 2026-04-14 | Echo's Self-Education Session

---

## The 2025 SE Roadmap: What Actually Matters

### Foundation Layer (Must Have)
- **Data Structures & Algorithms** — Big-O notation, hash tables, trees, graphs, sorting/searching, dynamic programming, recursion
- **Design Patterns** — 3 categories:
  - Creational: Factory, Singleton (manage object creation)
  - Structural: Proxy, Facade (simplify complex structures)
  - Behavioral: Observer, Iterator (object communication)
- **Git & Version Control** — Daily weapon. Push everything. Every project = portfolio proof.
- **Testing** — Non-negotiable:
  - Unit (Jest/Pytest — individual functions)
  - Integration (modules working together)
  - E2E (Playwright/Cypress — real user flows)
  - API testing (Postman)
  - TDD: write tests BEFORE code

### AI-Powered Development (2025 Standard)
Engineers who skip AI tools will be replaced by those who don't.
- ChatGPT/Claude/Gemini — boilerplate, optimization, error detection
- GitHub Copilot — AI pair programmer, auto-suggestions while coding
- Cursor AI / Windsurf — advanced editors that generate whole features
- Bolt.new / v0.dev — project generators from prompts
- AI in CI/CD — predicts failures, optimizes pipeline execution

### Cloud & DevOps
- AWS/Azure/GCP basics — how major providers operate
- Compute: EC2, Lambda (serverless), App Engine
- Storage: S3, Blob Storage
- **CI/CD Pipelines**: GitHub Actions, Jenkins, GitLab CI/CD
- Environments: dev → staging → QA → production

### What Gartner Says for 2025
- Platform engineering is the focus
- Pervasive AI integration in all workflows
- Productivity-driven modernization
- Continuous rightskilling (never stop learning)

---

## Core Principles of a Good Software Engineer

1. **Separation of Concerns** — Business logic ≠ route handlers ≠ database queries
2. **Don't Repeat Yourself (DRY)** — Extract reusable code into services/utilities
3. **Single Responsibility** — Each function/class does ONE thing well
4. **Test before you ship** — Not optional
5. **Document as you go** — Comments, README, SKILL.md
6. **Version control everything** — If it's not in git, it doesn't exist
7. **Make it work → make it right → make it fast** (in that order)

---

## Lessons Directly Applicable to Our Stack

- We should add CI/CD to our Railway deploys (GitHub Actions → auto deploy on push)
- Our apps lack formal service layers — business logic mixed with routes
- We should add unit tests to all auth and billing logic
- Design patterns we already use: Factory-ish (create_app), Singleton-ish (db instance)
- We should adopt TDD for new features in SaaS apps going forward

---

## Key Metrics Good Engineers Track
- Code coverage (% of code tested)
- Cyclomatic complexity (how many code paths exist)
- Technical debt (shortcuts taken that need revisiting)
- Mean Time to Recovery (MTTR) from failures
- Deployment frequency (how often you ship)
