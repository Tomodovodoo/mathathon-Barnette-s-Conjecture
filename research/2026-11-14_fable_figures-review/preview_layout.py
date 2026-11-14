"""Quick raster preview of a saved disk layout (scratch tool, not part of the build).
python research/2026-11-14_fable_figures-review/preview_layout.py running out.png"""
import json, sys, math
from pathlib import Path
from PIL import Image, ImageDraw
ROOT = Path(__file__).resolve().parents[2]; FIG = ROOT/'paper'/'figures'
sys.path.insert(0, str(FIG))
from model import Model
name, out = sys.argv[1], sys.argv[2]
d = json.loads((FIG/f'{name}.json').read_text()); L = json.loads((FIG/f'layout-{name}.json').read_text())
m = Model(d['faces'], d['t0'], d.get('e0')); xy = {int(k): v for k, v in L['coordinates'].items()}
S = 60; C = 6.2
def P(p): return ((p[0]+C)*S, (C-p[1])*S)
im = Image.new('RGB', (int(2*C*S), int(2*C*S)), 'white'); dr = ImageDraw.Draw(im)
dr.ellipse([P((-5,5)), P((5,-5))], outline='black', fill=None)
roots = set(m.roots)
for i in m.black:
    if i != m.t0: dr.polygon([P(xy[v]) for v in m.F[i]], fill=(215,215,215))
for a, b in m.E:
    if not (a in roots and b in roots): dr.line([P(xy[a]), P(xy[b])], fill='black', width=1)
for v, p in xy.items():
    x, y = P(p); dr.ellipse([x-3, y-3, x+3, y+3], fill='black'); dr.text((x+5, y-14), str(v), fill='red')
im.save(out)
