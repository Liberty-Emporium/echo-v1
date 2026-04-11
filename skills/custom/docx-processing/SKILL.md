---
name: docx-processing
description: Create, edit, analyze Word documents with python-docx. Use when you need to generate reports, contracts, or edit documents with tracked changes.
---

# DOCX Processing

## Install

```bash
pip install python-docx
```

## Create Document

```python
from docx import Document

doc = Document()
doc.add_heading('Report Title', 0)
doc.add_paragraph('Introduction text')
doc.add_heading('Section 1', 1)
doc.save('report.docx')
```

## Edit Document

```python
doc = Document('existing.docx')

# Add paragraphs
doc.add_paragraph('New content')

# Find and replace
for p in doc.paragraphs:
    if 'old' in p.text:
        p.text = p.text.replace('old', 'new')

doc.save('updated.docx')
```

## Tables

```python
table = doc.add_table(rows=2, cols=3)
table.cell(0, 0).text = 'Header'
table.cell(1, 0).text = 'Data'
```

## Read Document

```python
doc = Document('report.docx')
for p in doc.paragraphs:
    print(p.text)
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            print(cell.text)
```

## Best Practices

- Use styles, not raw formatting
- Save frequently
- Handle missing files gracefully