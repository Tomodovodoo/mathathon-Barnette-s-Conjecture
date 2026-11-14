"""Render every final page and record text bounds and figure label sizes.

Run from the repository root: python research/2026-11-14_astra_main-revision/render_final.py
"""
from pathlib import Path
import json
import fitz
from PIL import Image

root = Path(__file__).resolve().parent
repo = root.parents[1]
out = root / 'after-v2'
out.mkdir(exist_ok=True)
doc = fitz.open(repo / 'paper/main/barnette.pdf')
metrics = []
for i, page in enumerate(doc, 1):
    page.get_pixmap(dpi=130).save(out / f'p{i:02}.png')
    spans = [s for b in page.get_text('dict')['blocks'] if b['type'] == 0
             for line in b['lines'] for s in line['spans']]
    body = [s for s in spans if 75 < s['bbox'][1] < 770]
    metrics.append({'page': i,
                    'last_text_y': round(max(s['bbox'][3] for s in body), 2),
                    'text_sizes': sorted(set(round(s['size'], 2) for s in body)),
                    'captions': [s['text'] for s in spans if s['text'].startswith('Figure ')]})
for k in range(0, len(doc), 3):
    imgs = [Image.open(out / f'p{i+1:02}.png') for i in range(k, min(k+3, len(doc)))]
    sheet = Image.new('RGB', (sum(x.width for x in imgs), max(x.height for x in imgs)), '#bbb')
    x = 0
    for im in imgs:
        sheet.paste(im, (x, 0))
        x += im.width
    sheet.save(out / f'sheet{k//3+1}.png')
(root / 'page-metrics.json').write_text(json.dumps(metrics, indent=2), encoding='utf-8')
print('Rendered', len(doc), 'pages to', out)
print('Last body-text positions:', [(p['page'], p['last_text_y']) for p in metrics])
