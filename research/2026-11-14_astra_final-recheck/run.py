from pathlib import Path
import subprocess,json,time,os,re,fitz,difflib
R=Path('E:/rc-sol-late'); O=Path(__file__).resolve().parent; L=O/'logs'; rows=[]
def run(args,cwd='.'):
 n=len(rows); start=time.time()
 p=subprocess.run(args,cwd=R/cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=540,env=dict(os.environ,PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1'))
 (L/f'{n:02}.txt').write_bytes(p.stdout); rows.append(dict(command=args,cwd=cwd,code=p.returncode,seconds=round(time.time()-start,2),log=f'logs/{n:02}.txt')); (L/'commands.json').write_text(json.dumps(rows,indent=2)); print(rows[-1],flush=True)
def py(path,*args):run(['python','-B',path,*args])
def info(p):
 with fitz.open(p) as d:return dict(pages=len(d),text=''.join(x.get_text() for x in d))
products=['paper/main/barnette','proofs/primal/primal','proofs/involutions/involutions','proofs/sign-free/sign-free']; comparisons={}
(L/'commit.txt').write_text(subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True))
for p in products:
 old=info(R/(p+'.pdf')); folder,stem=p.rsplit('/',1)
 for i in range(3):
  run(['pdflatex','-interaction=nonstopmode','-halt-on-error',stem+'.tex'],folder)
  if i==0 and p.startswith('paper/'):run(['bibtex',stem],folder)
 new=info(R/(p+'.pdf')); comparisons[p]=dict(committed_pages=old['pages'],rebuilt_pages=new['pages'],text_equal=old['text']==new['text'])
 (L/(stem+'-text.diff')).write_text(''.join(difflib.unified_diff(old['text'].splitlines(True),new['text'].splitlines(True))),encoding='utf8')
 if stem=='barnette':(L/'bibliography.txt').write_text(new['text'].split('References')[-1],encoding='utf8')
 (L/(stem+'-final.log')).write_bytes((R/(p+'.log')).read_bytes())
(L/'pdf-comparison.json').write_text(json.dumps(comparisons,indent=2))
for p in (R/'digestions/atlas/figs').glob('*.pdf'):p.unlink()
py('digestions/atlas/build.py');py('digestions/atlas/verify.py');py('proofs/primal/figures/check.py','--build');py('proofs/sign-free/figures/check.py');py('paper/figures/check.py');py('workings/barnette_lab/setup_plantri.py');py('workings/barnette_lab/run_tests.py','quick');py('labyrinth/lab.py','check');py('digestions/route-map/build_map.py');run(['git','diff','--','digestions/route-map'])
for script in ['scan.py','route_compare.py']:run(['python','-B',str(R/'research/2026-11-14_sol_release-check'/script),str(R),str(L)])
