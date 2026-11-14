from barnette_lab.core import *
from pathlib import Path
import json
exe=Path('workings/barnette_lab/vendor/plantri.exe').resolve()
rows=[]
for n in range(6,19):
 gs=list(plantri_graphs(n,exe)); cyclic=0; first=None
 for i,g in enumerate(gs):
  b=Instance(g); ss=list(b.states()); ps=b.pairs(ss)
  bad=[p for p in ps if not b.is_tree(p[1])]
  if bad:
   cyclic+=1
   if first is None: first=i
   Path('research/2026-11-14_sol_route-constructive/data/hard_instance.json').write_text(json.dumps({'T_edges':list(g.edges()),'outer':b.outer,'pair':bad[0]}))
   print('FOUND',n,i,len(ss),len(ps),len(bad),flush=True)
   break
 rows.append({'n':n,'classes':len(gs),'first_cyclic_pair_graph':first})
 print(n,len(gs),first,flush=True)
 if cyclic: break
Path('research/2026-11-14_sol_route-constructive/data/plantri_scan.json').write_text(json.dumps(rows,indent=2))
