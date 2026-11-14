from pathlib import Path
import subprocess,json,shutil,time,fitz
S=Path.cwd();O=Path(__file__).resolve().parent;R=Path('E:/rc-sol-late');L=O/'logs';rows=[]
for rel in ['research/2026-11-14_astra_citation-audit/validate.py','proofs/involutions/involutions.tex']:shutil.copyfile(S/rel,R/rel)
for args,cwd in [(['python','-B','check.py'],'proofs/sign-free/figures'),(['python','-B','research/2026-11-14_astra_citation-audit/validate.py'],'.')]+[(['pdflatex','-interaction=nonstopmode','-halt-on-error','involutions.tex'],'proofs/involutions')]*3:
 t=time.time();q=subprocess.run(args,cwd=R/cwd,capture_output=True,timeout=540);name=f'fix-{len(rows)}.txt';(L/name).write_bytes(q.stdout+q.stderr);rows.append(dict(command=args,cwd=cwd,code=q.returncode,seconds=round(time.time()-t,2),log='logs/'+name))
(L/'fix-commands.json').write_text(json.dumps(rows,indent=2))
with fitz.open(R/'proofs/involutions/involutions.pdf') as d:
 (L/'fix-pages.txt').write_text(str(len(d)));assert len(d)==18
shutil.copyfile(R/'proofs/involutions/involutions.log',L/'involutions-fixed-final.log')
shutil.copyfile(R/'proofs/involutions/involutions.pdf',S/'proofs/involutions/involutions.pdf')
print(rows)
