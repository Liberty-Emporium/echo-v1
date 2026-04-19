# Entity Memory Schema

File: `memory/entities.json`

Stores structured facts about key entities — people, projects, services. Deduplicated and versioned.

## Schema

```json
{
  "people": [
    {
      "name": "Jay Alexander",
      "role": "Owner / Founder",
      "relationship": "My human — I work for him",
      "contact": "jay@libertyemporium.com",
      "notes": "Warm communicator, builds AI-powered SaaS apps on Railway",
      "updated": "2026-04-19"
    }
  ],
  "projects": [
    {
      "name": "Liberty Emporium Inventory",
      "repo": "Liberty-Emporium/Liberty-Emporium-Inventory-App",
      "url": "https://liberty-emporium-and-thrift-inventory-app-production.up.railway.app",
      "tech": ["Flask", "Python", "Claude AI"],
      "status": "live",
      "purpose": "Multi-tenant inventory for thrift stores with AI photo analysis",
      "updated": "2026-04-19"
    }
  ],
  "services": [
    {
      "name": "Railway",
      "purpose": "Hosting platform for all live apps",
      "url": "https://railway.app",
      "credentials": "See Railway dashboard",
      "updated": "2026-04-19"
    }
  ]
}
```

## Update Rules

1. Check for existing entry before adding — update, don't duplicate
2. Always update the `updated` date
3. For projects: keep `status` accurate (live / in-progress / archived / demo)
4. For people: only store what's relevant to working together
5. Never store passwords or tokens here — reference `/root/.secrets/` instead
