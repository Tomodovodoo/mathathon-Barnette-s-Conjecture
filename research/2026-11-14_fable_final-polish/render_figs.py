"""Render standalone figure PDFs: python render_figs.py <outdir> <dpi> <name> ..."""
import sys
from pathlib import Path
import fitz

out, dpi = Path(sys.argv[1]), int(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
for f in sys.argv[3:]:
    fitz.open(f'paper/figures/{f}.pdf')[0].get_pixmap(dpi=dpi).save(out / f'{f}.png')
