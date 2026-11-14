"""Reproduce final renders: python research/2026-11-14_sol_referee-sign-free/render.py"""
from pathlib import Path
import fitz
import subprocess,sys
from PIL import Image
b=Path(__file__).resolve().parent
original='--original' in sys.argv
d=fitz.open(stream=subprocess.check_output(['git','show','7b03288:proofs/sign-free/sign-free.pdf']),filetype='pdf') if original else fitz.open(b.parent.parent/'proofs/sign-free/sign-free.pdf')
assert len(d)==11
ims=[]
for i,p in enumerate(d):
    pix=p.get_pixmap(matrix=fitz.Matrix(.85,.85))
    im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
    im.save(b/(f'page-{i+1:02d}.png' if original else f'final-{i+1:02d}.png'));ims.append(im)
    if original:(b/f'page-{i+1:02d}.txt').write_text(p.get_text(),encoding='utf-8')
for start in range(0,len(ims),6):
    out=Image.new('RGB',(1560,1500),'#aaaaaa')
    for j in range(start,min(start+6,len(ims))):out.paste(ims[j],((j-start)%3*520,(j-start)//3*750))
    out.save(b/(f'sheet-{start}.png' if original else f'final-sheet-{start}.png'))
assert not any(s in p.get_text() for p in d for s in ('Fable','Opus','PROVED-HERE','COMPUTED','CONJECTURE'))
print('11 pages; no model names or status tags')
