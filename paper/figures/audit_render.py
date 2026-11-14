import fitz,pathlib
out=pathlib.Path('research/2026-11-14_astra_figures/source-renders')
for p in pathlib.Path('papers').glob('*.pdf'):
 d=fitz.open(p)
 for i,page in enumerate(d):
  if page.get_drawings() and len(page.get_drawings())>15:
   page.get_pixmap(matrix=fitz.Matrix(1.25,1.25)).save(out/f'{p.stem}-{i+1}.png')
   print(p.name,i+1,len(page.get_drawings()))
