"""Check delivered PDFs and record the exact read-only inputs. Run after build.py."""
from pathlib import Path
import json, hashlib, re
import fitz
O=Path(__file__).resolve().parent
ROOT=O.parents[1]
manifest=json.loads((O/'manifest.json').read_text())
atlas=fitz.open(O/'atlas.pdf')
assert len(atlas)==len(manifest)==28
rows=[]
for i,item in enumerate(manifest):
    path=O/'pages'/(item['name']+'.pdf'); doc=fitz.open(path)
    assert len(doc)==1 and len(doc[0].get_images())==0
    assert 100<=item['words']<=180
    assert (O/'renders'/(item['name']+'.png')).is_file()
    assert 'Status.' in doc[0].get_text() and 'Connects to.' in doc[0].get_text()
    assert item['title'].lower().split()[0] in doc[0].get_text().lower()
    assert not re.search(r'Overfull \\[hv]box',(O/'pages'/(item['name']+'.log')).read_text())
    spans=[s for b in doc[0].get_text('dict')['blocks'] if 'lines' in b for l in b['lines'] for s in l['spans']]
    assert min(s['bbox'][0] for s in spans)>=60
    assert max(s['bbox'][2] for s in spans)<=doc[0].rect.width-60
    rows.append({'page':i+1,'name':item['name'],'vector_only':True,'words':item['words'],'size_bytes':path.stat().st_size,'minimum_font':round(min(s['size'] for s in spans),2)})
inputs=[ROOT/'paper/figures'/name for name in ['draw.py','model.py','check.py','barnette-figs.sty','running.json','layout-running.json','octahedron.json','layout-octahedron.json']]
inputs += list((ROOT/'papers').glob('*.pdf'))
inputs += [ROOT/'research'/p for p in ['2026-11-14_astra_referee-combinatorics/REFEREE.md','2026-11-14_fable_referee-determinants/SIGNIFICANCE.md','2026-11-14_sol_referee-structure/REFEREE-graph-theory.md','2026-11-14_sol_referee-structure/REFEREE-limits.md','2026-11-14_fable_referee-topology/REFEREE.md']]
hashes={str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
result={'command':'python digestions/atlas/audit.py','status':'COMPUTED','pages':rows,'total_pages':len(atlas),'all_vector':all(len(p.get_images())==0 for p in atlas),'input_sha256':hashes,'visual_review':'See QA.md. Automated checks do not replace visual or mathematical review.'}
(O/'audit.json').write_text(json.dumps(result,indent=2))
print('PASS: 28 single-page vector PDFs, 28 atlas pages, 28 renders, word limits, margins, no TeX overflows.')
