"""Build from repository root: python research/2026-11-14_astra_manuscript-A/build.py"""
from pathlib import Path
import subprocess,re,json,hashlib
import fitz
ROOT=Path(__file__).resolve().parents[2]
DRAFT=ROOT/'paper/draft-A';OUT=Path(__file__).parent
for i,cmd in enumerate([['pdflatex','-interaction=nonstopmode','-halt-on-error','barnette.tex'],['bibtex','barnette']]+[['pdflatex','-interaction=nonstopmode','-halt-on-error','barnette.tex']]*3):
 run=subprocess.run(cmd,cwd=DRAFT,capture_output=True)
 (DRAFT/f'build-pass{i}.txt').write_bytes(run.stdout+run.stderr)
 if run.returncode:raise RuntimeError(run.stdout.decode(errors='replace'))
log=(DRAFT/'barnette.log').read_text(errors='replace')
assert 'undefined' not in log.lower()
assert 'Rerun to get cross-references right' not in log
assert not re.search(r'Overfull \\[hv]box',log)
doc=fitz.open(DRAFT/'barnette.pdf');render=OUT/'renders';render.mkdir(exist_ok=True)
for i,p in enumerate(doc):p.get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(render/f'page-{i+1:02}.png')
files=[DRAFT/'barnette.tex',DRAFT/'refs.bib',DRAFT/'barnette.pdf']+[ROOT/'paper/figures'/f'{f}.pdf' for f in re.findall(r'\\fig\{([^}]+)\}',(DRAFT/'barnette.tex').read_text())]
report={'pages':len(doc),'errors':0,'undefined_references':0,'overfull_boxes':0,'render_scale':1.5,'sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
(OUT/'build-check.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='sha256'}))
