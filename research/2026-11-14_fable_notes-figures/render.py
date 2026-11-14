"""Render the figure pages of both notes. Usage: python render.py <outdir> [dpi]"""
import sys, fitz
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
dpi = int(sys.argv[2]) if len(sys.argv) > 2 else 150
for note in ['primal', 'involutions']:
    doc = fitz.open(ROOT / 'proofs' / note / (note + '.pdf'))
    print(note, 'pages', len(doc))
    for i, page in enumerate(doc):
        txt = page.get_text()
        if 'Figure' in txt and (len(page.get_drawings()) > 40):
            page.get_pixmap(dpi=dpi).save(out / f'{note}-p{i+1:02d}.png')
            print(' page', i + 1, 'drawings', len(page.get_drawings()))
