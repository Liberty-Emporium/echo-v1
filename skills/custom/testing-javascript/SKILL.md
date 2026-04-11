---
name: testing-javascript
description: Write and run tests for JavaScript and Node.js applications using Jest, Mocha, and Chai.
metadata:
  openclaw:
    emoji: 📜
    requires:
      bins: [npm, node]
---

# JavaScript/Node.js Testing Skill

## Usage

Write tests for JavaScript/Node.js:
- Unit tests
- Integration tests
- API tests
- Mocking

## Commands

```bash
# Run tests
npm test

# Watch mode
npm test -- --watch

# Coverage
npm test -- --coverage

# Run specific suite
npm test -- user.test.js
```

## Examples

```javascript
const { add } = require('./math')

describe('math', () => {
  test('adds numbers', () => {
    expect(add(2, 3)).toBe(5)
  })
})
```
