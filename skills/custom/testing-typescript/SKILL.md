---
name: testing-typescript
description: Write and run tests for TypeScript applications using Jest, Vitest, and testing-library.
metadata:
  openclaw:
    emoji: 🔷
    requires:
      bins: [npm, npx]
---

# TypeScript Testing Skill

## Usage

Write tests for TypeScript:
- Type-safe unit tests
- Integration tests
- Mocking with types

## Commands

```bash
# Run tests
npm test

# Watch mode
npm test -- --watch

# Coverage
npm test -- --coverage

# Specific file
npm test -- user.test.ts
```

## Examples

```typescript
interface User {
  id: number;
  name: string;
}

function getUserName(user: User): string {
  return user.name;
}

describe('getUserName', () => {
  it('returns user name', () => {
    const user: User = { id: 1, name: 'John' };
    expect(getUserName(user)).toBe('John');
  });
});
```
