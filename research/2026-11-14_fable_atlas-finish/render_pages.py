"""Render every page of an atlas PDF for inspection, and make contact sheets.

    python research/2026-11-14_fable_atlas-finish/render_pages.py <atlas.pdf> <outdir> [dpi]

Writes <outdir>/full/NN-colour.png, NN-grey.png, NN-deut.png (deuteranopia simulation, Machado,
Oliveira and Fernandes 2009, severity 1, applied in linear RGB) and contact sheets
<outdir>/sheet-{colour,grey,deut}-K.jpg at 42 dpi, twelve pages per sheet.
The full-size renders are scratch and are not committed; the sheets are.
"""
import sys, fitz
from pathlib import Path
import numpy as np
from PIL import Image
src, out = sys.argv[1], Path(sys.argv[2])
dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 130
full = out / 'full'
full.mkdir(parents=True, exist_ok=True)
M = np.array([[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]])


def deut(im):
    a = np.asarray(im, float) / 255
    lin = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
    lin = np.clip(lin @ M.T, 0, 1)
    b = np.where(lin <= 0.0031308, lin * 12.92, 1.055 * lin ** (1 / 2.4) - 0.055)
    return Image.fromarray((np.clip(b, 0, 1) * 255 + .5).astype('uint8'))


doc = fitz.open(src)
small = {'colour': [], 'grey': [], 'deut': []}
for i, pg in enumerate(doc):
    px = pg.get_pixmap(dpi=dpi)
    im = Image.frombytes('RGB', (px.width, px.height), px.samples)
    vers = {'colour': im, 'grey': im.convert('L'), 'deut': deut(im)}
    for k, v in vers.items():
        v.save(full / f'{i:02d}-{k}.png')
        w = round(v.width * 42 / dpi)
        small[k].append(v.convert('RGB').resize((w, round(v.height * 42 / dpi)), Image.LANCZOS))
w, h = small['colour'][0].size
for k, ims in small.items():
    for j in range(0, len(ims), 12):
        sheet = Image.new('RGB', (6 * w, 2 * h), 'white')
        for i, im in enumerate(ims[j:j + 12]):
            sheet.paste(im, ((i % 6) * w, (i // 6) * h))
        sheet.save(out / f'sheet-{k}-{j // 12 + 1}.jpg', quality=70)
print(len(doc), 'pages at', dpi, 'dpi')
