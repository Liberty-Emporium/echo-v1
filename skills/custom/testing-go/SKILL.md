---
name: testing-go
description: Write and run tests for Go applications using the built-in testing package, testify, and ginkg.
metadata:
  openclaw:
    emoji: 🔷
    requires:
      bins: [go]
---

# Go Testing Skill

## Usage

Write tests for Go:
- Unit tests
- Integration tests
- Table-driven tests
- Benchmark tests

## Commands

```bash
# Run tests
go test ./...

# Verbose
go test -v

# Specific test
go test -run TestName

# Coverage
go test -coverprofile=coverage.out

# Benchmark
go test -bench=.
```

## Examples

```go
func TestAdd(t *testing.T) {
    result := Add(2, 3)
    if result != 5 {
        t.Errorf("Add(2, 3) = %d; want 5", result)
    }
}

// Table-driven
func TestAddTable(t *testing.T) {
    tests := []struct {
        a, b, want int
    }{
        {1, 2, 3},
        {0, 0, 0},
        {-1, 1, 0},
    }
    for _, tt := range tests {
        t.Run(fmt.Sprintf("%d+%d", tt.a, tt.b), func(t *testing.T) {
            if got := Add(tt.a, tt.b); got != tt.want {
                t.Errorf("Add() = %d, want %d", got, tt.want)
            }
        })
    }
}
```
