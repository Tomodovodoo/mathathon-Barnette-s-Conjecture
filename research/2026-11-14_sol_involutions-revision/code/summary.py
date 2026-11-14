import json
from pathlib import Path
from collections import Counter
from PIL import Image,ImageOps,ImageDraw
out=Path('research/2026-11-14_sol_involutions-revision');d=json.loads((out/'verification.json').read_text());s={}
for mode in ('ray','tree','reverse-tree'):
    rows=[r for r in d['rows'] if r['mode']==mode];p=[r for r in rows if r['pairs']]
    s[mode]=dict(roots=len(rows),paired=len(p),objects=sum(r['objects'] for r in p),fixed=sum(r['F'] for r in p),max_walk=max(int(k) for r in p for k in r['walk_hist']),above_zero=sum(r['other_k'][str(r['m']+1)]==0 for r in p))
a=json.loads((out/'drawing-census.json').read_text());rr=a['rows'];s['drawings']=dict(rows=len(rr),counts=len(set(r['objects'] for r in rr)),min=min(r['objects'] for r in rr),max=max(r['objects'] for r in rr),max_walk=max(r['max_walk'] for r in rr));s['command']='python research/2026-11-14_sol_involutions-revision/code/summary.py'
(out/'summary.json').write_text(json.dumps(s,indent=1));print(json.dumps(s,indent=1))
pages=sorted(out.glob('page-*.png'))
for first in range(0,len(pages),4):
    canvas=Image.new('RGB',(1600,2300),'#dddddd');dr=ImageDraw.Draw(canvas)
    for i,p in enumerate(pages[first:first+4]):
        im=Image.open(p);im.thumbnail((790,1100));x=(i%2)*800;y=(i//2)*1150+25;canvas.paste(im,(x,y));dr.text((x+10,y-20),p.stem,fill='black')
    canvas.save(out/f'contact-{first//4}.png')
