from pathlib import Path
import re,json,subprocess,hashlib
R=Path(__file__).resolve().parents[2]; O=Path(__file__).resolve().parent
def read(p): return p.read_text(encoding='utf-8')
def bib(p):
 s=read(p); starts=list(re.finditer(r'(?m)^@\w+\{([^,]+),',s))
 return {m[1]:s[m.start():starts[i+1].start() if i+1<len(starts) else len(s)].strip() for i,m in enumerate(starts)}
if __name__=='__main__':
 docs=[R/p for p in ['paper/main/barnette.tex','proofs/primal/primal.tex','proofs/involutions/involutions.tex','proofs/sign-free/sign-free.tex']]
 docs += sorted((R/'digestions/steps').glob('*.md'))+[R/'digestions/SYNTHESIS.md',R/'digestions/route-map/HOW-IT-WORKS.md',R/'digestions/atlas/atlas.tex']
 records=[]
 for p in docs:
  if not p.exists():continue
  s=read(p)
  if p.name=='atlas.tex':
   for line_no,t in enumerate(s.splitlines(),1):
    if re.match(r'^\d+ & ',t):records.append(dict(file=p.relative_to(R).as_posix(),line=line_no,kind='prose',context=t))
   continue
  for m in re.finditer(r'\\cite\w*\*?(?:\[[^\]]*\])*\{([^}]+)\}',s):
   a=s.rfind('\n\n',0,m.start())+2;b=s.find('\n\n',m.end());b=len(s) if b<0 else b
   records.append(dict(file=p.relative_to(R).as_posix(),line=s[:m.start()].count('\n')+1,kind='cite',citation=m[0],keys=m[1].split(','),context=s[a:b]))
  # Retain full paragraphs for prose citations and project references, including atlas rows.
  for m in re.finditer(r'[^\n]+(?:\n(?!\n)[^\n]+)*',s):
   t=m[0]
   if p.name=='atlas.tex':
    if 'Sources and computation' not in s[:m.start()] or '&' not in t:continue
   if re.search(r'OpenAI|\bLi\b|LIT|Stein|Alt,|Hertel|Feder|Kelmans|Tutte|Goodey|Holton|Brinkmann|Schnieders|Kardo|Thomason|Juh|K.lm|Rado|Nash.Williams|Edmonds|Schrijver|Kenyon|Ford|constructive|trees paper|\]\(|research/|\\path\{',t):
    records.append(dict(file=p.relative_to(R).as_posix(),line=s[:m.start()].count('\n')+1,kind='prose',context=t))
 (O/'inventory.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
 pdfs=list((R/'papers').rglob('*.pdf'))
 for folder in ['2026-11-14_opus_history-literature','2026-11-14_sol_machinery-literature']:pdfs+=list((R/'research'/folder/'pdf').glob('*.pdf'))
 (O/'source-text').mkdir(exist_ok=True)
 rows=[]
 for p in pdfs:
  out=O/'source-text'/(p.stem+'.txt')
  q=subprocess.run(['pdftotext','-layout',str(p),str(out)],capture_output=True)
  rows.append(dict(file=p.relative_to(R).as_posix(),text=out.relative_to(O).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size,extracted=q.returncode==0))
 (O/'pdf-inventory.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
 (O/'.gitignore').write_text('source-text/\nweb/\nbuild/\n__pycache__/\n',encoding='utf-8')
 print(len(records),'citation contexts;',len(rows),'PDFs;',sum(x['kind']=='cite' for x in records),'cite commands')
