---
name: testing-django
description: Write and run tests for Django applications. Use when: writing Django tests, testing models/views/forms, running pytest-django, coverage reports.
metadata:
  openclaw:
    emoji: 🦄
    requires:
      bins: [pytest, python]
      pip: [pytest-django, coverage]
---

# Django Testing Skill

## Usage

Write tests for Django apps:
- Model tests
- View tests  
- Form tests
- API tests
- Integration tests

## Commands

```bash
# Run tests
pytest

# With coverage
pytest --cov=myapp --cov-report=html

# Specific file
pytest tests/test_models.py

# With verbose
pytest -v
```

## Examples

```python
from django.test import TestCase
from myapp.models import MyModel

class MyModelTest(TestCase):
    def test_create(self):
        obj = MyModel.objects.create(name="test")
        self.assertEqual(obj.name, "test")
```
