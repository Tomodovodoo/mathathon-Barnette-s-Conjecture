from explore import *
from itertools import combinations
rows=json.loads((OUT/'data.json').read_text())
hard=json.loads((ROOT/'research/2026-11-14_sol_route-constructive/data/hard_instance.json').read_text())
rows.append(run('cyclic_mate_12',Instance(nx.Graph(hard['T_edges']),hard['outer']),True))
(OUT/'data.json').write_text(json.dumps(rows,indent=2))
checks=[]
for name in ('cube','hexagonal_prism'):
 b=Instance.from_primal(named_graphs()[name]); edges=[]
 for t in b.A:
  for v in set(b.faces[t])&set(b.X):
   w=[next(f for f in (b.sides[u,v],b.sides[v,u]) if f in b.white) for u in b.faces[t] if u!=v]
   edges.append((t,v,*w))
 count=0; total=0
 for es in combinations(edges,b.n):
  g=nx.MultiGraph();g.add_nodes_from(b.white);g.add_edges_from((a,c) for t,v,a,c in es)
  if not nx.is_tree(g):continue
  total+=1
  if len({t for t,v,a,c in es})==b.n and len({v for t,v,a,c in es})==b.n:count+=1
 assert count==sum(b.is_tree(s) for s in b.states()) and total==white_tau(b,True)
 checks.append(dict(name=name,laplacian_coefficient=count,unrestricted=total))
(OUT/'coefficient_check.json').write_text(json.dumps(checks,indent=2))
print(checks)
