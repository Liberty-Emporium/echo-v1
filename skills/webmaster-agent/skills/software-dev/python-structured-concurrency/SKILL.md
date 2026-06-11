---
name: python-structured-concurrency
description: Python ExceptionGroup and asyncio.TaskGroup — structured concurrency that collects ALL failures, not just the first
version: 1.0.0
platforms: [linux, macos, windows]
---

# Python ExceptionGroup & Structured Concurrency

## When to use
- Running multiple concurrent API calls where you need ALL failures
- Health checks that test multiple endpoints simultaneously
- Any async code where silent failure is unacceptable
- Liberty Emporium: health check system reporting all failing services

## Key Insight
Traditional `asyncio.gather()` returns the first exception and hides the rest. `TaskGroup` collects ALL failures as an `ExceptionGroup`.

## Core Concepts

### ExceptionGroup
A container for multiple unrelated exceptions. Created with:
```python
eg = ExceptionGroup("multiple failures", [
    ConnectionError("API timeout"),
    ValueError("Invalid response"),
])
```

### except* — Selective Handling
Catches only specific exception types from a group:
```python
try:
    raise ExceptionGroup("errors", [ValueError("bad"), TypeError("wrong")])
except* ValueError as errs:
    # Catches only ValueError instances
    print(f"Value errors: {len(errs.exceptions)}")
```

### asyncio.TaskGroup — Structured Concurrency
```python
async with asyncio.TaskGroup() as tg:
    task1 = tg.create_task(fetch(url1))
    task2 = tg.create_task(fetch(url3))
    task3 = tg.create_task(fetch(url3))
# All tasks completed if we reach here
# Or ExceptionGroup is raised with ALL failures
```

## Replacing gather() with TaskGroup

### Before (gather — loses errors):
```python
results = await asyncio.gather(*tasks, return_exceptions=True)
# Must manually filter exceptions from results
```

### After (TaskGroup — reports all failures):
```python
async with asyncio.TaskGroup() as tg:
    tasks = {url: tg.create_task(check(url)) for url in urls}
# All succeeded, or ExceptionGroup raised
```

## Health Check Pattern
Build a health checker that reports ALL failing services, not just the first:
1. Create TaskGroup
2. Add check tasks for each endpoint
3. Catch ExceptionGroup
4. Report all failures with response times

## Requirements
- Python 3.11+ (for ExceptionGroup and TaskGroup)
- All code tested on Python 3.11.15 ✅

## Source
Python 3.14 asyncio documentation.
Full version with code: `references/python-exceptiongroup-full.md`
