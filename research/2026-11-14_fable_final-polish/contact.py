"""Contact sheets of a PDF: python contact.py <pdf> <outdir> <dpi> <pages per sheet> [first last]"""
import sys
from pathlib import Path
import fitz
from PIL import Image

pdf, out, dpi, per = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
out.mkdir(parents=True, exist_ok=True)
doc = fitz.open(pdf)
lo, hi = (int(sys.argv[5]), int(sys.argv[6])) if len(sys.argv) > 6 else (1, len(doc))
ims = []
for i in range(lo - 1, hi):
    px = doc[i].get_pixmap(dpi=dpi)
    ims.append(Image.frombytes('RGB', (px.width, px.height), px.samples))
for k in range(0, len(ims), per):
    grp = ims[k:k + per]
    sheet = Image.new('RGB', (sum(im.width for im in grp) + 6 * (len(grp) - 1), max(im.height for im in grp)), (120, 120, 120))
    x = 0
    for im in grp:
        sheet.paste(im, (x, 0))
        x += im.width + 6
    sheet.save(out / f'{pdf.stem}-sheet-{lo + k:02}.png')
print(pdf.name, len(doc), 'pages')
