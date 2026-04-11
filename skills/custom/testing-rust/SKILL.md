---
name: testing-rust
description: Write and run tests for Rust applications using built-in test framework, proptest, and cargo test.
metadata:
  openclaw:
    emoji: 🦀
    requires:
      bins: [cargo, rustc]
---

# Rust Testing Skill

## Usage

Write tests for Rust:
- Unit tests
- Integration tests
- Doc tests
- Property-based tests

## Commands

```bash
# Run all tests
cargo test

# Specific test
cargo test test_name

# With output
cargo test -- --nocapture

# Test docstrings
cargo test --doc

# Coverage
cargo tarpaulin
```

## Examples

```rust
#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
    
    #[test]
    #[should_panic]
    fn it_panics() {
        panic!("This test should panic");
    }
}
```
