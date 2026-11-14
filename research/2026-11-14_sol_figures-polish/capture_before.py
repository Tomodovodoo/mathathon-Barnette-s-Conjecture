"""Reproduce initial renders from the parent of the first finishing commit.
python research/2026-11-14_sol_figures-polish/capture_before.py
"""
from pathlib import Path
import subprocess
import fitz
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).parent
(OUT/'before').mkdir(exist_ok=True)
revision='cc6d9e3^'
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',revision,'paper/figures'],cwd=ROOT,text=True).splitlines()
paths=[p for p in paths if p.endswith('.pdf') and Path(p).name[:2].isdigit()]
for p in paths:
    raw=subprocess.check_output(['git','show',revision+':'+p],cwd=ROOT)
    d=fitz.open(stream=raw,filetype='pdf');d[0].get_pixmap(dpi=150).save(OUT/'before'/Path(p).with_suffix('.png').name)
for start in range(0,len(paths),5):
    sheet=Image.new('RGB',(1500,1000),'#eeeeee');pen=ImageDraw.Draw(sheet)
    for k,p in enumerate(paths[start:start+5]):
        im=Image.open(OUT/'before'/Path(p).with_suffix('.png').name);im.thumbnail((485,460));x=k%3*500;y=k//3*500
        sheet.paste(im,(x,y+25));pen.text((x+5,y+5),Path(p).stem,fill='black')
    sheet.save(OUT/f'before-sheet-{start//5}.png')
d=fitz.open(ROOT/'papers/OpenAI-Barnette.pdf')
(OUT/'source-text.txt').write_text(''.join(p.get_text() for p in d),encoding='utf8')
for i in [6,7,8]:d[i].get_pixmap(dpi=110).save(OUT/f'source-page-{i+1}.png')
