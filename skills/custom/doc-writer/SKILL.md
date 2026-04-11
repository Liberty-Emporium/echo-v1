---
name: doc-writer
description: Auto-generate documentation for code. Use when you need to: create README, document APIs, write docstrings.
---

# Doc Writer

## README Template

```markdown
# Project Name

One sentence description.

## Setup
\`\`\`bash
pip install -r requirements.txt
\`\`\`

## Usage
\`\`\`python
from project import main
main()
\`\`\`

## API

| Endpoint | Method | Description |
|-----------|--------|-------------|
| /api/... | GET | ... |
```

## Docstrings

```python
def function(param: str) -> bool:
    """Short one-liner.
    
    Longer description if needed.
    
    Args:
        param: What it does
        
    Returns:
        What it returns
        
    Raises:
        Error: When it fails
    """
```

## Auto-Gen

```bash
# Auto docstrings
pip install autodoc
autodoc project/
```