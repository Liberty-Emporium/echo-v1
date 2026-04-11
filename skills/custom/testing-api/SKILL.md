---
name: testing-api
description: Write and run API and integration tests using Postman, Supertest, and curl. Test REST APIs, GraphQL, and webhooks.
metadata:
  openclaw:
    emoji: 🌐
    requires:
      bins: [curl, npm]
---

# API/Integration Testing Skill

## Usage

Test APIs:
- REST APIs
- GraphQL
- Webhooks
- Authentication

## Commands

```bash
# Test endpoint
curl -X GET https://api.example.com/users

# With auth
curl -H "Authorization: Bearer TOKEN" ...

# Run Postman collection
newman run collection.json
```

## Examples (Supertest)

```javascript
const request = require('supertest')
const app = require('../app')

describe('API', () => {
  test('GET /users', async () => {
    const res = await request(app).get('/users')
    expect(res.status).toBe(200)
    expect(res.body).toHaveProperty('users')
  })
})
```
