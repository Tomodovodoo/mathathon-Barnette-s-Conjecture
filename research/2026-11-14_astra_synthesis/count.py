"""Run from repository root: python research/2026-11-14_astra_synthesis/count.py.
Inventory only, not a replay of mathematical censuses. Routes get one editorial
primary category by the explicit rules below; per-route assignments are saved.
"""
from pathlib import Path
import runpy, json, re, hashlib, datetime
from collections import Counter
import fitz
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
routes=runpy.run_path(str(ROOT/'digestions/route-map/routes.py'))['ROUTES']
kinds=['Combinatorial','Graph-theoretic / structural','Constructive / algorithmic','Algebraic / determinantal','Topological','Probabilistic','Categorical','Inductive','Lattice-theoretic','Non-planar / Pfaffian']
def kind(r):
    t=' '.join(str(r.get(k,'')) for k in ['label','text','where','arg']).lower()
    for k,pat in [(9,r'pfaffian|nonplanar|non-planar|heawood|torus|other surfaces'),(6,r'categor|temperley.lieb|belyi|boundary.pattern|trinity|operad'),(7,r'induct|contraction|degree.4|local expansion|lift criterion|three.face rotation'),(8,r'lattice|felsner|irreducible|alpha.orientation|clock order|rank.compatible'),(5,r'probabil|random|sampling|measure|lorentz|m.convex|mean load'),(3,r'determinant|algebra|polynomial|berezin|gaussian|congruence|mod p|gauge|coefficient|real stability|semidefinite|nullstellensatz|2.adic'),(4,r'topolog|morse|gauss.bonnet|turning|winding|jordan|homolog|floer'),(2,r'algorithm|walk|search|descent|marked|complexity|ppad'),(1,r'matroid|packing|hall|flow|euler|duality|spanning.tree|connectivity|gluing|separator|cut|recovery|induced|structur')]:
        if re.search(pat,t): return kinds[k]
    return kinds[0]
outcome={'LIT':'Proved','PROVED-HERE':'Proved','COMPUTED':'Computed','CONJECTURE':'Open','HUNCH':'Open','REFUTED':'Refuted'}
rows=[dict(id=r['id'],label=r['label'],kind=kind(r),status=r['status'],outcome=outcome[r['status']]) for r in routes]
(OUT/'route-classification.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
reports=sorted(ROOT.glob('research/*/REPORT.md'))
runs=sorted(p for p in (ROOT/'research').iterdir() if p.is_dir() and p.name.startswith('2026-11-14_'))
models={'astra':'GPT-6 Astra','sol':'GPT-6.1 Sol','fable':'Fable 5.2','opus':'Opus 5.5'}
pdfs={}
for base in ['paper/main','proofs/primal','proofs/involutions','proofs/blueprint','digestions/atlas']:
    for p in sorted((ROOT/base).glob('*.pdf')):
        with fitz.open(p) as doc: pdfs[p.relative_to(ROOT).as_posix()]=len(doc)
# Inventory is explicit: do not add drafts, individual atlas pages or figure PDFs to prose pages.
words={p.relative_to(ROOT).as_posix():len(re.findall(r'\b[\w]+\b',p.read_text(encoding='utf8'))) for p in (ROOT/'digestions/steps').glob('*.md')}
report_inventory=[dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in reports]
data=dict(timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),run_folders=len(runs),reports=len(reports),models=dict(Counter(models.get(p.name.split('_')[1],p.name.split('_')[1]) for p in runs)),routes=len(rows),route_status=dict(Counter(r['status'] for r in rows)),route_matrix={k:{o:sum(r['kind']==k and r['outcome']==o for r in rows) for o in ['Proved','Computed','Open','Refuted']} for k in kinds},pdf_pages=pdfs,product_pdf_pages_total=sum(pdfs.values()),step_words=words,step_words_total=sum(words.values()),report_inventory=report_inventory,pending=[p.name for p in runs if not (p/'REPORT.md').exists()])
(OUT/'counts.json').write_text(json.dumps(data,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in data.items() if k not in ['report_inventory','step_words']},indent=2))
