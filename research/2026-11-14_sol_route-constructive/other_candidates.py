import json,time
from pathlib import Path
from barnette_lab.core import *
from barnette_lab.algorithms import *
rows=[]
graphs=[(name,Instance.from_primal(g)) for name,g in named_graphs().items()]
hard=json.loads(Path('research/2026-11-14_sol_route-constructive/data/hard_instance.json').read_text())
graphs.append(('cyclic_20',Instance(nx.Graph(hard['T_edges']))))
for name,b in graphs:
 start=time.perf_counter(); spokes,valid=two_matroid_candidate(b)
 hits=sum(wilson_candidate(b,seed) is not None for seed in range(100))
 rows.append({'name':name,'two_matroid_size':len(spokes),'two_matroid_state_valid':valid,'spokes':spokes,'wilson_successes':hits,'wilson_trials':100,'seconds':time.perf_counter()-start})
print(rows)
Path('research/2026-11-14_sol_route-constructive/data/other_candidates.json').write_text(json.dumps(rows,indent=2))
