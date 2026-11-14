"""Freeze reviewed inputs and check census summary arithmetic."""
from check import ROOT,HERE
import json,hashlib,re,platform
import networkx,sympy
published=[1,0,1,0,2,1,5,3,18,19,79,134,501,1147,3976,11055,37231,114560,384053]
rows=json.loads((ROOT/'research/2026-11-14_astra_cycle-covers/data/census.json').read_text())
total=0
for row,classes in zip(rows,published):
    text='\n'.join(row['summary']);n=row['V']
    summary=next(s for s in row['summary'] if s.startswith('SUMMARY'))
    fields={k:int(v) for k,v in re.findall(r'(\w+)=(\d+)',summary)}
    c1=next(s for s in row['summary'] if s.startswith('C1 tested'))
    f1={k:int(v) for k,v in re.findall(r'(\w+)=(\d+)',c1)}
    assert fields['graphs']==classes
    assert fields['rooted']==classes*(2*n-4)==fields['withpair']==f1['tested']
    assert f1['violations']==f1['overflow']==0
    assert f1['equality']==fields['extremes_equal']
    total+=fields['rooted']
assert total==23824742
paths=['research/BRIEF.md','README.md','papers/text/OpenAI-Barnette.txt','papers/OpenAI-Barnette.pdf','papers/text/barnette_trees.txt','proofs/primal/DICTIONARY.md','proofs/involutions/INVOLUTIONS.md','research/2026-11-14_opus_route-topology/TOPOLOGY.md','research/2026-11-14_opus_two-tree-packing/REPORT.md']
for folder in ['2026-11-14_astra_cycle-covers','2026-11-14_sol_route-probabilistic','2026-11-14_sol_counting-families']:
    paths += [str(p.relative_to(ROOT)).replace('\\','/') for p in (ROOT/'research'/folder).glob('*.md')]
for path in [ROOT/'research/2026-11-14_astra_cycle-covers/data',ROOT/'research/2026-11-14_sol_counting-families/data',ROOT/'research/2026-11-14_sol_route-probabilistic/data']:
    paths += [str(p.relative_to(ROOT)).replace('\\','/') for p in path.glob('*.json')]
hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sorted(paths)}
record=dict(python=platform.python_version(),networkx=networkx.__version__,sympy=sympy.__version__,census_summary_total=total,published_e4_counts=published,published_source='Brinkmann and McKay, Fast generation of planar graphs, Table 6, https://users.cecs.anu.edu.au/~bdm/papers/plantri-full.pdf',input_sha256=hashes)
(HERE/'provenance.json').write_text(json.dumps(record,indent=2))
print('Reviewed-input hashes saved; census summary total',total)
