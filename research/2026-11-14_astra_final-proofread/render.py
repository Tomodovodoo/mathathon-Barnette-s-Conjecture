from pathlib import Path
import fitz, hashlib,json
from PIL import Image
root=Path('research/2026-11-14_astra_final-proofread')
pdf=Path('paper/main/barnette.pdf'); tex=Path('paper/main/barnette.tex')
doc=fitz.open(pdf)
meta={'command':'python research/2026-11-14_astra_final-proofread/render.py','pages':len(doc),'sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (pdf,tex)},'head':None}
(root/'source.tex').write_bytes(tex.read_bytes())
for i,p in enumerate(doc):
 pix=p.get_pixmap(matrix=fitz.Matrix(1.25,1.25),alpha=False)
 im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples).quantize(colors=64)
 im.save(root/'renders'/f'page-{i+1:02}.png',optimize=True)
(root/'pdf-text.txt').write_text('\n'.join(f'\n=== PAGE {i+1} ===\n'+p.get_text() for i,p in enumerate(doc)),encoding='utf8')
meta['render_bytes']=sum(p.stat().st_size for p in (root/'renders').glob('*.png'))
(root/'manifest.json').write_text(json.dumps(meta,indent=2))
print(meta)
