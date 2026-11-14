from pathlib import Path
import json,re
O=Path(__file__).resolve().parent;L=O/'logs'
rows=[]
for p in L.glob('*-final.log'):
 for n,line in enumerate(p.read_text(errors='replace').splitlines(),1):
  if re.search(r'undefined|^!|Missing character',line,re.I) or any(float(x)>2 for x in re.findall(r'Overfull \\[hv]box \(([0-9.]+)pt',line)):rows.append(dict(file=p.name,line=n,text=line))
b=(L/'bibliography.txt').read_text(encoding='utf8');(L/'document-diagnostics.json').write_text(json.dumps(dict(warnings=rows,internal_note_matches=[x for x in ['content checked','not opened','research/','Wikipedia'] if x.lower() in b.lower()]),indent=2))
