from pathlib import Path
import subprocess,fitz,json
p=Path('paper/main').resolve(); out=Path('research/2026-11-14_astra_main-revision').resolve()
logs=[]
for cmd in [['pdflatex','-interaction=nonstopmode','-halt-on-error','barnette.tex'],['bibtex','barnette'],['pdflatex','-interaction=nonstopmode','-halt-on-error','barnette.tex'],['pdflatex','-interaction=nonstopmode','-halt-on-error','barnette.tex']]:
 r=subprocess.run(cmd,cwd=p,capture_output=True,text=True,errors='replace');logs.append(' '.join(cmd)+'\n'+r.stdout+r.stderr)
 if r.returncode:print(r.stdout[-3000:]);break
(out/'build.txt').write_text('\n'.join(logs),encoding='utf-8')
print('exit',r.returncode)
if r.returncode==0:
 print('pages',len(fitz.open(p/'barnette.pdf')))
 log=(p/'barnette.log').read_text(errors='replace');print('\n'.join(x for x in log.splitlines() if any(t in x for t in ['Overfull','undefined','Warning'])))
