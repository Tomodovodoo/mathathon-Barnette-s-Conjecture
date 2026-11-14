import fitz,json
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
O=Path(__file__).parent; files=sorted(O.glob('[0-9][0-9]-*.pdf'))+[O/'gallery.pdf'];rows=[]
for p in files:
 d=fitz.open(p);rows.append(dict(file=p.name,pages=len(d),fonts=sorted({f[3] for page in d for f in page.get_fonts()}),raster_images=sum(len(page.get_images()) for page in d)))
 assert all(not page.get_images() for page in d)
 assert len(d)==(14 if p.stem=='gallery' else 1)
 if p.stem in ['05-pair-D','08-cancellation','10-white-tree','11-selected-Jordan']:
  d[0].get_pixmap(matrix=fitz.Matrix(1.5,1.5),colorspace=fitz.csGRAY).save(O/'renders'/f'{p.stem}-gray.png')
 assert 'Overfull' not in (O/(p.stem+'.log')).read_text(errors='replace')
(O/'qa.json').write_text(json.dumps(rows,indent=2))
ims=[]
for i in range(1,15):
 im=Image.open(O/'renders'/f'gallery-{i:02}.png').convert('RGB');im.thumbnail((280,396));ims.append(im)
out=Image.new('RGB',(280*4,396*4),'#ddd')
for i,im in enumerate(ims):out.paste(im,((i%4)*280,(i//4)*396))
out.save(O/'renders'/'gallery-contact.png')
