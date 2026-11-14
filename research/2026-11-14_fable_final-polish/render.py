"""Render a PDF to PNG pages with PyMuPDF.

usage: python render.py <pdf> <outdir> <dpi> [page numbers, 1-based ...]
"""
import sys
from pathlib import Path
import fitz

pdf, out, dpi = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
pages = [int(a) for a in sys.argv[4:]]
out.mkdir(parents=True, exist_ok=True)
doc = fitz.open(pdf)
for i, page in enumerate(doc, 1):
    if pages and i not in pages:
        continue
    page.get_pixmap(dpi=dpi).save(out / f'{pdf.stem}-p{i:02}.png')
print(pdf.name, len(doc), 'pages')
