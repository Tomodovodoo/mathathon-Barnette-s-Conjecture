from pathlib import Path
import fitz,numpy as np,json,hashlib,shutil
from PIL import Image,ImageOps,ImageDraw
R=Path(__file__).resolve().parents[3]; O=Path(__file__).resolve().parents[1]/'outputs'; O.mkdir(exist_ok=True)
for f in ['atlas.pdf','atlas.tex','computed.json','pages.py','pages_more.py','figs_scope.py']:
 shutil.copyfile(R/'digestions/atlas'/f,O/('snapshot-'+f))
d=fitz.open(O/'snapshot-atlas.pdf')
M=np.array([[.367322,.860646,-.227968],[.280085,.672501,.047413],[-.011820,.042940,.968881]])
texts=[]
for i,p in enumerate(d):
 pix=p.get_pixmap(dpi=120); im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples); im.save(O/f'p{i:02}.png')
 a=np.asarray(im)/255; a=np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4); a=np.clip(a@M.T,0,1); a=np.where(a<=.0031308,12.92*a,1.055*a**(1/2.4)-.055)
 sim=Image.fromarray(np.uint8(np.clip(a*255,0,255))); sim.save(O/f'deut{i:02}.png'); ImageOps.grayscale(im).save(O/f'gray{i:02}.png')
 texts.append(f'\n=== PDF index {i}, route {i if 1<=i<=28 else "front/sources"} ===\n'+p.get_text())
(O/'extracted.txt').write_text('\n'.join(texts),encoding='utf8')
for mode in ['p','gray','deut']:
 for start in range(0,len(d),4):
  sheet=Image.new('RGB',(1400,2020),'#cccccc'); dr=ImageDraw.Draw(sheet)
  for k in range(start,min(start+4,len(d))):
   im=Image.open(O/f'{mode}{k:02}.png').convert('RGB'); im.thumbnail((690,975)); x=(k-start)%2*700; y=(k-start)//2*1010; sheet.paste(im,(x,y+25)); dr.text((x+10,y+5),f'PDF index {k}, route {k}',fill='black')
  sheet.save(O/f'{mode}-sheet-{start:02}.jpg')
(O/'snapshot.json').write_text(json.dumps({'sha256':hashlib.sha256((O/'snapshot-atlas.pdf').read_bytes()).hexdigest(),'pages':len(d),'dpi':120,'simulation':'Machado 2009 severity 1.0 deuteranopia matrix, linear sRGB'},indent=2))
print(O)

