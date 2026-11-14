"""Raster proofs and contact sheets. Run from repository root after build.py."""
from pathlib import Path
import json,re
import fitz
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).parent
F=ROOT/'paper/figures'
M=np.array([[.367322,.860646,-.227968],[.280085,.672501,.047413],[-.011820,.042940,.968881]])
# Full-severity deuteranopia linear-RGB matrix, with sRGB transfer before/after.
def simulate(im):
    x=np.asarray(im,dtype=float)/255
    linear=np.where(x<=.04045,x/12.92,((x+.055)/1.055)**2.4)
    y=np.clip(linear@M.T,0,1)
    srgb=np.where(y<=.0031308,12.92*y,1.055*y**(1/2.4)-.055)
    return Image.fromarray(np.uint8(np.rint(np.clip(srgb,0,1)*255)))
files=sorted(F.glob('[0-9][0-9]-*.pdf'))
for folder in ['after','greyscale','deuteranopia']:(OUT/folder).mkdir(exist_ok=True)
for f in files:
    doc=fitz.open(f);assert len(doc)==1
    png=OUT/'after'/f.with_suffix('.png').name
    doc[0].get_pixmap(dpi=150).save(png)
    im=Image.open(png).convert('RGB')
    im.convert('L').save(OUT/'greyscale'/png.name)
    simulate(im).save(OUT/'deuteranopia'/png.name)
for folder in ['after','greyscale','deuteranopia']:
    for start in range(0,len(files),4):
        sheet=Image.new('RGB',(1600,1250),'#eee');pen=ImageDraw.Draw(sheet)
        for k,f in enumerate(files[start:start+4]):
            im=Image.open(OUT/folder/f.with_suffix('.png').name);im.thumbnail((780,585))
            x=(k%2)*800;y=(k//2)*625;sheet.paste(im,(x,y+25));pen.text((x+5,y+5),f.stem,fill='black')
        sheet.save(OUT/f'{folder}-sheet-{start//4}.png')
    final=Image.new('RGB',(1400,1650),'#eee');pen=ImageDraw.Draw(final)
    for k,name in enumerate(['01-cube','02-two-factors','03-dual','12-tree-cotree','13-selected','16-at-a-glance']):
        im=Image.open(OUT/folder/(name+'.png'));im.thumbnail((690,515));x=k%2*700;y=k//2*550
        final.paste(im,(x,y+25));pen.text((x+5,y+5),name,fill='black')
    final.save(OUT/(folder+'-final-check.png'))
    # One proof page per figure, exact physical size of the original standalone.
    doc=fitz.open()
    for f in files:
        original=fitz.open(f);rect=original[0].rect;page=doc.new_page(width=rect.width,height=rect.height)
        page.insert_image(rect,filename=str(OUT/folder/f.with_suffix('.png').name))
    doc.save(OUT/f'{folder}-proof.pdf')
# Compact gallery sheet, and independent caption line count from rendered PDF positions.
doc=fitz.open(F/'gallery.pdf');sheet=Image.new('RGB',(1800,2550),'#ddd');caps={};pages=[]
for i,page in enumerate(doc):
    im=Image.frombytes('RGB',[page.get_pixmap(dpi=65).width,page.get_pixmap(dpi=65).height],page.get_pixmap(dpi=65).samples)
    im.thumbnail((590,835));sheet.paste(im,((i%3)*600,(i//3)*850));im.save(OUT/'after'/f'gallery-{i+1:02}.png')
    lines=[]
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines',[]):
            text=''.join(s['text'] for s in l['spans'])
            lines.append((l['bbox'][1],text))
    lines.sort();starts=[(y,int(re.match(r'Figure (\d+)\.',t)[1])) for y,t in lines if re.match(r'Figure (\d+)\.',t)]
    assert 1<=len(starts)<=2
    for y,n in starts:
        stop=min([yy for yy,t in lines if yy>y+2 and t.startswith('Body text for scale.')]+[page.rect.height])
        ys=[]
        for yy,t in lines:
            if y-.2<=yy<stop-.2 and t.strip() and not re.fullmatch(r'\d+',t.strip()):
                if not any(abs(yy-old)<3 for old in ys):ys.append(yy)
        caps[n]=len(ys)
    pages.append(dict(page=i+1,figures=[n for y,n in starts]))
sheet.save(OUT/'gallery-sheet.png')
(OUT/'caption-audit.json').write_text(json.dumps(dict(lines=caps,pages=pages),indent=1))
assert all(n==1 or k<=5 for n,k in caps.items()),caps
print('caption lines',caps)
