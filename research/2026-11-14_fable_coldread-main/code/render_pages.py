"""Render a PDF page by page to PNG, as used for the cold read.

Run from the repository root:
    python research/2026-11-14_fable_coldread-main/code/render_pages.py paper/main/barnette.pdf research/2026-11-14_fable_coldread-main/pages 130
The PNGs of the cold read are committed in pages/; this command reproduces them.
"""
import sys
from pathlib import Path

import fitz

pdf, out, dpi = sys.argv[1], Path(sys.argv[2]), int(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)
doc = fitz.open(pdf)
for i, page in enumerate(doc, 1):
    page.get_pixmap(dpi=dpi).save(out / f"p{i:02d}.png")
print(len(doc), "pages ->", out)
