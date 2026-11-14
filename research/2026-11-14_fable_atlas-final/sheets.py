"""Contact sheets of an atlas PDF, colour and greyscale, at low resolution.
    python research/2026-11-14_fable_atlas-final/sheets.py <atlas.pdf> <out-prefix>
"""
import sys, fitz
from PIL import Image
src, out = sys.argv[1:3]
doc = fitz.open(src)
ims = []
for pg in doc:
    px = pg.get_pixmap(dpi=42)
    ims.append(Image.frombytes('RGB', (px.width, px.height), px.samples))
w, h = ims[0].size
per = 12
for k in range(0, len(ims), per):
    chunk = ims[k:k + per]
    sheet = Image.new('RGB', (6 * w, 2 * h), 'white')
    for i, im in enumerate(chunk):
        sheet.paste(im, ((i % 6) * w, (i // 6) * h))
    sheet.save(f'{out}-colour-{k // per + 1}.jpg', quality=70)
    sheet.convert('L').save(f'{out}-grey-{k // per + 1}.jpg', quality=70)
print(len(ims), 'pages')
