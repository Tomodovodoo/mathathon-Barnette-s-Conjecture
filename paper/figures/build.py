import subprocess,sys,fitz
from pathlib import Path
O=Path(__file__).parent.resolve()
for name in ['model.py','check.py','draw.py']:
 subprocess.run([sys.executable,str(O/name)],cwd=O,check=True)
for p in sorted(O.glob('[0-9][0-9]-*.tex'))+[O/'gallery.tex']:
 if '-body' in p.stem:continue
 z=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error',p.name],cwd=O,capture_output=True,text=True)
 if z.returncode: print(z.stdout[-4000:]);raise SystemExit(z.returncode)
 print('built',p.stem,flush=True)
R=O/'renders';R.mkdir(exist_ok=True)
for p in sorted(O.glob('*.pdf')):
 doc=fitz.open(p)
 for i,page in enumerate(doc):page.get_pixmap(matrix=fitz.Matrix(1.4,1.4)).save(R/f'{p.stem}-{i+1:02}.png')
