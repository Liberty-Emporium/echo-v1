---
name: test-strategy
description: Know what to test and how to test it. Use when you need to: write tests, determine coverage, know what's critical.
---

# Test Strategy

## What to Test (Priority)

1. **Critical paths** - Login, payments, core features
2. **Edge cases** - Empty, wrong input, timeouts
3. **Error handling** - What happens on failure
4. **Integration** - Things talk to each other

## What NOT to Test

- Simple getters/setters
- Known stable code
- UI details (unless critical)

## Test Pyramid

```
       /\
      /  \    E2E (few)
     /----\   
    /      \  Integration (some)
   /--------\ Unit (many)
```

## What Each Level Tests

- **Unit**: Individual functions
- **Integration**: Two pieces working together  
- **E2E**: Full user journey

## Quick Test Template

```python
def test_function():
    # Arrange
    input_data = ...
    
    # Act
    result = my_function(input_data)
    
    # Assert
    assert result == expected
```

## Coverage Target

- Critical paths: 100%
- Business logic: 80%+