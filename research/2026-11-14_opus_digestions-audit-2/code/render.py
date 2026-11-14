"""Render the paper figures whose committed PNG renders are older than their PDFs
(05-state, 11-spokes, 12-tree-cotree), plus the face-path heights figure, into
digestions/steps/img/ at 150 dpi.

    python research/2026-11-14_opus_digestions-audit-2/code/render.py
"""
from pathlib import Path

import fitz  # PyMuPDF

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'digestions' / 'steps' / 'img'
JOBS = {
    'paper-05-state.png': ROOT / 'paper' / 'figures' / '05-state.pdf',
    'paper-11-spokes.png': ROOT / 'paper' / 'figures' / '11-spokes.pdf',
    'paper-12-tree-cotree.png': ROOT / 'paper' / 'figures' / '12-tree-cotree.pdf',
    'paper-17-heights.png': ROOT / 'paper' / 'figures' / '17-heights.pdf',
}
OUT.mkdir(exist_ok=True)
for name, pdf in JOBS.items():
    doc = fitz.open(pdf)
    pix = doc[0].get_pixmap(dpi=150, alpha=False)
    pix.save(OUT / name)
    print(name, pix.width, 'x', pix.height, 'from', pdf.relative_to(ROOT))
