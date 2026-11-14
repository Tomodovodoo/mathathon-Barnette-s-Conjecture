"""Check saved outputs, then record a hash manifest. No mathematical search."""
import hashlib,json,platform,subprocess
from independent import *

slow=json.loads((OUT/'census_18.json').read_text())
fast=json.loads((OUT/'fast_census_summary.json').read_text())
by={d['V']:d for d in fast}
for row in slow:
    for k in ('graphs','roots','feasible','factors','pairs','TM','equality'):
        assert row.get(k,0)==by[row['V']][k],(row['V'],k)
totals={k:sum(r[k] for r in fast) for k in ('graphs','roots','feasible','factors','pairs','TM','equality','violations')}
assert totals['feasible']==4656948 and totals['violations']==0
v18=json.loads((OUT/'v18.json').read_text());v33=json.loads((OUT/'R2_glued_V33.json').read_text())
second=json.loads((OUT/'second_R2_glued_V33.json').read_text())
assert v18['lattice']==4 and v18['TM']==12 and v18['extreme_tree_pairs']==[0,0]
assert v33['lattice']==16 and not v33['R2'] and v33['TM']==144 and not second['R2']
r5=json.loads((OUT/'r5.json').read_text());assert r5['tree_elements']==654 and r5['lattice']==1410
path=OUT.parent
manifest={'python':platform.python_version(),'compiler':subprocess.run(['g++','--version'],capture_output=True,text=True).stdout.splitlines()[0],
          'C1_totals':totals,'sha256':{}}
files=list(path.glob('code/*.py'))+list(path.glob('code/*.cpp'))+list(OUT.glob('*.json'))
inputs=[ROOT/'papers/text/OpenAI-Barnette.txt',ROOT/'research/2026-11-14_opus_conjectures/data/c2_counterexample_V18.json',
        ROOT/'research/2026-11-14_opus_conjectures/data/r1_counterexample_V24.txt',
        ROOT/'research/2026-11-14_opus_conjectures/data/r3_counterexample_V60.txt',
        ROOT/'research/2026-11-14_opus_conjectures/code/gen.py',ROOT/'workings/barnette_lab/vendor/plantri.exe']
for p in files+inputs:
    if p.name=='provenance.json':continue
    manifest['sha256'][str(p.relative_to(ROOT)).replace('\\','/')]=hashlib.sha256(p.read_bytes()).hexdigest()
save('provenance.json',manifest)
print('Validated independent output agreement and saved provenance.',totals)
