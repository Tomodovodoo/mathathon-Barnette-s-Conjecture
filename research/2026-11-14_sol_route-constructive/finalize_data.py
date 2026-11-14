from pathlib import Path
import json,platform,sys,networkx,sympy,numpy
from barnette_lab import *
from barnette_lab.verify import export
p=Path('research/2026-11-14_sol_route-constructive')
for name in ['cube','truncated_octahedron']:
 data=json.dumps(export(Instance.from_primal(named_graphs()[name])),indent=2)
 (p/'data'/f'{name}.json').write_text(data)
 (Path('workings/barnette_lab/examples')/f'{name}.json').write_text(data)
(p/'data/environment.json').write_text(json.dumps({'python':sys.version,'platform':platform.platform(),'networkx':networkx.__version__,'sympy':sympy.__version__,'numpy':numpy.__version__},indent=2))
b=json.loads((p/'data/benchmarks.json').read_text());w=json.loads((p/'data/bad_starts.json').read_text())
print(len(b),sum(r.get('sample_tree_successes',0) for r in b),max(r['enumeration_seconds'] for r in b));print('restarts',[r['marked']['restarts'] for r in w]); print('normalized',[r['marked']['normalization_reversals'] for r in w])
