"""Record the full v1/v2 source diff and grey print proofs of key figures."""
from pathlib import Path
import subprocess
import fitz
from PIL import Image

root = Path(__file__).resolve().parent
repo = root.parents[1]
run = subprocess.run(['git','diff','--no-index','--',
    'paper/main/history/barnette-v1.tex','paper/main/barnette.tex'],
    cwd=repo, capture_output=True, text=True, errors='replace')
assert run.returncode in (0,1)
(root/'proof-comparison.diff').write_text(run.stdout, encoding='utf-8')
doc = fitz.open(repo/'paper/main/barnette.pdf')
out = root/'greyscale'
out.mkdir(exist_ok=True)
for n in [2,10,13,15,17]:
    doc[n-1].get_pixmap(dpi=110,colorspace=fitz.csGRAY).save(out/f'p{n:02}.png')
for name, pages in [('states',[2,10,13]),('flow-gluing',[15,17])]:
    imgs = [Image.open(out/f'p{n:02}.png') for n in pages]
    sheet = Image.new('RGB',(sum(im.width for im in imgs),max(im.height for im in imgs)),'#bbb')
    x=0
    for im in imgs:
        sheet.paste(im,(x,0));x+=im.width
    sheet.save(out/f'{name}.png')
print('Saved complete source comparison and five grey print proofs.')
