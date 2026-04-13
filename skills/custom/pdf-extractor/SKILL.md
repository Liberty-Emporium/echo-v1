# pdf-extractor

**Version:** 1.0.0
**Created:** 2026-04-13
**Author:** Echo

## Description

Download a PDF from any URL (Google Drive, Dropbox, direct link), extract specific pages as PNG images, attempt text extraction, and return base64-encoded images ready for HTML embedding.

Born from: manually doing this 3 different ways during the 2026-04-13 court page session.

## When To Use

- User shares a Google Drive PDF link and wants content extracted
- Need a thumbnail of a PDF first page for display in HTML
- Need to read scanned document content as images
- Need to embed a PDF page preview in HTML without file storage

## Prerequisites

```bash
apt-get update && apt-get install -y poppler-utils
```

## Steps

1. **Detect URL type** — Google Drive share URL vs direct PDF
2. **Download:** `curl -L "https://drive.google.com/uc?export=download&id=FILE_ID" -o /tmp/doc.pdf`
3. **Extract pages:** `pdftoppm -r 150 -f 1 -l 1 -png /tmp/doc.pdf /tmp/pages`
4. **Try text:** `pdftotext /tmp/doc.pdf /tmp/text.txt` (empty if scanned)
5. **Base64 encode:** `base64 -w 0 /tmp/pages-01.png > /tmp/img_b64.txt`
6. **Embed in HTML:** `data:image/png;base64,$(cat /tmp/img_b64.txt)`

## Google Drive URL Patterns

- Share URL: `https://drive.google.com/file/d/FILE_ID/view`
- Download URL: `https://drive.google.com/uc?export=download&id=FILE_ID`
- Extract FILE_ID from the `/d/FILE_ID/` part of the share URL

## Notes

- Scanned PDFs have ZERO text — always read extracted PNG images with model vision
- For large files, extract only needed pages (use -f and -l flags for first/last page)
- 150dpi = good thumbnail quality; 300dpi = print quality
- Pages are named: `/tmp/pages-01.png`, `/tmp/pages-02.png`, etc.
