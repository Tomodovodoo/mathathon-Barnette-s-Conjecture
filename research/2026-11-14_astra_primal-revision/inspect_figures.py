import sys,json
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
p=Path('proofs/primal/figures'); imgs=[]
for f in sorted(p.glob('0*.png')):
 im=Image.open(f).convert('RGB');im.thumbnail((1000,500));canvas=Image.new('RGB',(1020,540),'white');canvas.paste(im,((1020-im.width)//2,30));ImageDraw.Draw(canvas).text((10,5),f.stem,fill='black');imgs.append(canvas)
for i in range(0,len(imgs),4):
 sheet=Image.new('RGB',(2040,1080),'white')
 for j,im in enumerate(imgs[i:i+4]):sheet.paste(im,((j%2)*1020,(j//2)*540))
 sheet.save(Path('research/2026-11-14_astra_primal-revision')/f'figures-contact-{i//4}.png')
sys.path.insert(0,'research/2026-11-14_astra_primal-revision')
import check_cancellation as cc
sys.path.insert(0,'proofs/primal/figures')
import importlib.util
spec=importlib.util.spec_from_file_location('primal_figures',p/'check.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
cc.check(mod.run['g'],'running-13')
Path('research/2026-11-14_astra_primal-revision/cancellation-running.json').write_text(json.dumps(dict(cc.C),indent=2))
