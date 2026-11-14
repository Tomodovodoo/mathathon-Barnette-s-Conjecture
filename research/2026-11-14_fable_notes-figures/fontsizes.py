"""List the text sizes on the figure pages of both notes (PyMuPDF spans).
Usage: python fontsizes.py   -> prints, per page, the count of characters per font size."""
import fitz, collections
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
PAGES = {'primal': [12, 13, 14, 15], 'involutions': [9, 10]}
for note, pages in PAGES.items():
    doc = fitz.open(ROOT / 'proofs' / note / (note + '.pdf'))
    for n in pages:
        c = collections.Counter(); ex = collections.defaultdict(list)
        for b in doc[n - 1].get_text('dict')['blocks']:
            for l in b.get('lines', []):
                for s in l['spans']:
                    if s['text'].strip():
                        k = round(s['size'], 1); c[k] += len(s['text'].strip())
                        if len(ex[k]) < 6: ex[k].append(s['text'].strip()[:12])
        print(note, 'page', n, {k: (c[k], ex[k]) for k in sorted(c)})
