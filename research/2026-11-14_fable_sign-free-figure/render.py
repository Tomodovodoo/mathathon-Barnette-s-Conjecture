"""Render every page of proofs/sign-free/sign-free.pdf to PNG.

Usage: python render.py <outdir> [zoom]     (from this folder; needs PyMuPDF)
"""
import sys
from pathlib import Path
import fitz

here = Path(__file__).resolve().parent
out = here / sys.argv[1]
zoom = float(sys.argv[2]) if len(sys.argv) > 2 else 1.6
out.mkdir(exist_ok=True)
d = fitz.open(here.parent.parent / 'proofs/sign-free/sign-free.pdf')
for i, p in enumerate(d):
    p.get_pixmap(matrix=fitz.Matrix(zoom, zoom)).save(out / ('page-%02d.png' % (i + 1)))
print(len(d), 'pages ->', out)
