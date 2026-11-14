from barnette_lab.core import *
from barnette_lab.algorithms import *
from collections import Counter
from pathlib import Path
import time,json
rows=[]
for equator in [4,8,12,16,24,32,48]:
 t=nx.cycle_graph(equator); t.add_edges_from((h,v) for h in [equator,equator+1] for v in range(equator))
 g=truncate(t); b=Instance.from_primal(g)
 stat=Counter(); start=time.perf_counter(); s=b.enumerate_tree(stat); enum=time.perf_counter()-start
 start=time.perf_counter(); p=b.flow_pair(); flow=time.perf_counter()-start
 start=time.perf_counter(); result,mstat=marked_walk(b,p,cap=100000); marked=time.perf_counter()-start
 cert=b.recover(s); assert check_cycle(g,cert['cycle_original'],cert['avoided_edge_original'])
 rows.append({'family':'truncated_even_bipyramid','equator':equator,'N':len(g),'n':b.n,'enumeration_seconds':enum,'flow_seconds':flow,'marked_seconds_excluding_flow':marked,'prefix_stats':dict(stat),'marked_stats':mstat})
 print(rows[-1],flush=True)
Path('research/2026-11-14_sol_route-constructive/data/growing_family.json').write_text(json.dumps(rows,indent=2))
