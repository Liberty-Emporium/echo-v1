#!/usr/bin/env python3
"""
build_pdf.py — Render an HTML file to PDF using WeasyPrint.
Usage: python3 build_pdf.py <input.html> <output.pdf>
"""
import sys
import subprocess

def ensure_weasyprint():
    try:
        import weasyprint
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "weasyprint", "--break-system-packages", "-q"], check=True)
        import weasyprint
    return weasyprint

def build(html_path: str, pdf_path: str):
    weasyprint = ensure_weasyprint()
    doc = weasyprint.HTML(filename=html_path)
    doc.write_pdf(pdf_path)
    print(f"[OK] PDF written to {pdf_path}")

def verify(pdf_path: str):
    try:
        import fitz
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "pymupdf", "--break-system-packages", "-q"], check=True)
        import fitz
    doc = fitz.open(pdf_path)
    pages = doc.page_count
    nulls = any("\x00" in doc[i].get_text() for i in range(pages))
    print(f"[OK] {pages} page(s) | broken_glyphs={nulls}")
    for i in range(pages):
        links = [l["uri"] for l in doc[i].get_links() if l.get("uri")]
        if links:
            print(f"  Page {i+1} links: {links}")
    if nulls:
        print("[WARN] Null bytes detected — emoji may not render. Use HTML entities or UTF-8 text.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: build_pdf.py <input.html> <output.pdf>")
        sys.exit(1)
    build(sys.argv[1], sys.argv[2])
    verify(sys.argv[2])
