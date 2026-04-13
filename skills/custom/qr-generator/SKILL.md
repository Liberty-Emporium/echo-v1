# qr-generator

**Version:** 1.0.0
**Created:** 2026-04-13
**Author:** Echo

## Description

Generate a QR code for any URL and return it as a base64 PNG data URI ready to drop directly into HTML — no file storage needed, survives Railway deploys.

Born from: building print flyers during 2026-04-13 session.

## When To Use

- Building print-ready pages that need a scannable QR code
- Need a QR code embedded directly in HTML (no static file)
- User wants flyers, printouts, court documents with QR codes

## Prerequisites

```bash
apt-get install -y python3-qrcode python3-pil
# NOTE: Do NOT use pip or pip3 — not available in this environment
```

## Usage

```python
import qrcode, base64
from io import BytesIO

url = "https://your-url-here.com"
qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=3)
qr.add_data(url)
qr.make(fit=True)
img = qr.make_image(fill_color="#1a1a2e", back_color="white")
buf = BytesIO()
img.save(buf, format='PNG')
b64 = base64.b64encode(buf.getvalue()).decode()

# Save for reuse
with open('/tmp/qr_b64.txt', 'w') as f:
    f.write(b64)

data_uri = f"data:image/png;base64,{b64}"
# Use data_uri as src= in <img> tag
```

## HTML Usage

```html
<img src="data:image/png;base64,BASE64_HERE" alt="QR Code" style="width:150px;height:150px;">
```

## Notes

- Always use `ERROR_CORRECT_H` for print quality (30% damage tolerance)
- Save b64 to `/tmp/qr_b64.txt` for reuse: avoids regenerating on each command
- `fill_color="#1a1a2e"` matches Jay's dark navy brand color
- `box_size=10, border=3` gives good quality at 150px display size
- QR codes generated this way are only ~3-4KB — tiny in HTML
