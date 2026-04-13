# base64-image

**Version:** 1.0.0
**Created:** 2026-04-13
**Author:** Echo

## Description

Convert any local image file to a base64 data URI for inline HTML embedding. Essential for Railway deployments where static files are wiped on every deploy.

Born from: PDF thumbnail returning 404 after Railway deploy during 2026-04-13 session.

## THE RULE

> **On Railway, NEVER use `/static/uploads/filename.png` for important images.**
> Railway wipes all static files on every deploy. Always embed as base64 or use external CDN.

## When To Use

- ALWAYS when embedding images in HTML templates on Railway
- After extracting PDF page thumbnails
- When a Railway static file keeps 404ing after deploy
- QR codes, thumbnails, logos, any image that must persist across deploys

## Bash Usage

```bash
B64=$(base64 -w 0 /path/to/image.png)
DATA_URI="data:image/png;base64,$B64"
```

## Python Usage

```python
import base64
with open('/path/to/image.png', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode()
data_uri = f"data:image/png;base64,{b64}"
```

## Embed in Existing HTML Template

```python
with open('templates/page.html', 'r') as f:
    html = f.read()

html = html.replace('src="/static/uploads/image.png"', f'src="{data_uri}"')

with open('templates/page.html', 'w') as f:
    f.write(html)
```

## MIME Types
- PNG:  `data:image/png;base64,...`
- JPEG: `data:image/jpeg;base64,...`
- GIF:  `data:image/gif;base64,...`
- WebP: `data:image/webp;base64,...`
- SVG:  `data:image/svg+xml;base64,...`

## Notes

- Save b64 to file for reuse: `base64 -w 0 file.png > /tmp/img_b64.txt`
- A 1.9MB PNG becomes ~2.5MB as base64 — fine for HTML
- Avoid base64 for images over 5MB (slows page load significantly)
