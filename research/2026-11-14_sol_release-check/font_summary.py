"""Summarize pdffonts logs. python -B font_summary.py CLONE LOGDIR"""
from pathlib import Path
import json,fitz,sys
root=Path(sys.argv[1]);out=Path(sys.argv[2]);rows={}
for file in out.glob('*-fonts.txt'):
 lines=[x for x in file.read_text(encoding='utf8').splitlines()[4:] if x.strip()]
 rows[file.name]=dict(font_rows=len(lines),nonembedded=[x for x in lines if x.split()[-5]!='yes'],type3=[x for x in lines if 'Type 3' in x])
with fitz.open(root/'digestions/atlas/atlas.pdf') as doc:
 rows['atlas_type3_pdf_pages']=[p.number+1 for p in doc if any(f[2]=='Type3' for f in p.get_fonts())]
(out/'font-summary.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
