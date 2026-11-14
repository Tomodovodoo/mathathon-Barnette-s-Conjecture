from pathlib import Path
import fitz
from PIL import Image,ImageDraw
root=Path('research/2026-11-14_astra_main-revision')
for tag,src in [('before','paper/main/history/barnette-v1.pdf')]:
 out=root/tag;out.mkdir(exist_ok=True)
 d=fitz.open(src)
 for i,p in enumerate(d):p.get_pixmap(dpi=110).save(out/f'p{i+1:02}.png')
 for k in range(0,len(d),3):
  imgs=[Image.open(out/f'p{i+1:02}.png') for i in range(k,min(k+3,len(d)))]
  sheet=Image.new('RGB',(sum(x.width for x in imgs),max(x.height for x in imgs)),'#bbb'); xx=0
  for im in imgs:sheet.paste(im,(xx,0));xx+=im.width
  sheet.save(out/f'sheet{k//3+1}.png')
print('rendered',len(d))
