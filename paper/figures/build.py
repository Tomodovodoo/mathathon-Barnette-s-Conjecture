"""Rebuild everything: python paper/figures/build.py

Runs check.py (all assertions) and draw.py, compiles each figure and the gallery
with pdflatex, and renders every page to renders/ at 150 dpi (gallery at 100).
Stops at the first failed assertion or TeX error.
"""
import subprocess
import sys
from pathlib import Path

import fitz

O = Path(__file__).parent.resolve()
only = sys.argv[1:]
for name in ['check.py', 'draw.py']:
    subprocess.run([sys.executable, str(O / name)], cwd=O, check=True)
R = O / 'renders'
R.mkdir(exist_ok=True)
for p in sorted(O.glob('[0-9][0-9]-*.tex')) + [O / 'gallery.tex']:
    if '-body' in p.stem or (only and not any(k in p.stem for k in only)):
        continue
    for _ in range(2 if p.stem == 'gallery' else 1):
        z = subprocess.run(['pdflatex', '-interaction=nonstopmode', '-halt-on-error', p.name], cwd=O, capture_output=True, text=True, errors='replace')
        if z.returncode:
            print(z.stdout[-3000:])
            raise SystemExit(f'pdflatex failed on {p.name}')
    log = (O / (p.stem + '.log')).read_text(errors='replace')
    if 'Overfull' in log:
        print('  overfull box in', p.name)
    doc = fitz.open(O / (p.stem + '.pdf'))
    for i, page in enumerate(doc):
        page.get_pixmap(dpi=100 if p.stem == 'gallery' else 150).save(R / (f'{p.stem}-{i + 1:02}.png' if p.stem == 'gallery' else f'{p.stem}.png'))
    print('built', p.stem, len(doc), 'page(s)', flush=True)
