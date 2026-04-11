---
name: refactor-sense
description: Improve code quality without breaking functionality. Use when you need to: clean up messy code, extract functions, rename things, simplify logic.
---

# Refactor Sense

## Safe Refactors

- Extract repeated code → function
- Rename variables → clearer names
- Add type hints
- Remove dead code
- Simplify conditionals

## Red Flags (Don't Touch)

- Working complex logic you don't fully understand
- Business logic you can't test
- Code with no tests

## Workflow

1. Read and understand
2. Write tests if none exist
3. Make small changes
4. Test after each change
5. Commit working state

## Commands

```bash
# Find duplicates
grep -rn "same_code" *.py

# Find long functions
awk 'NF>50' *.py | head

# Find magic numbers
grep -rn "[0-9]\{3,\}" *.py | grep -v "version\|year"
```