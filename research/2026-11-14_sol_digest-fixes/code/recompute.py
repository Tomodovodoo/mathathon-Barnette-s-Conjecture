from pathlib import Path
import sys,json,collections
ROOT=Path.cwd(); OUT=ROOT/'research/2026-11-14_sol_digest-fixes'
sys.path.insert(0,str(ROOT/'workings/barnette_lab'))
from barnette_lab.core import Instance,plantri_graphs
import networkx as nx
rows=[]
for v in range(6,13):
 graphs=list(plantri_graphs(v,ROOT/'workings/barnette_lab/vendor/plantri.exe'))
 cyclic=0; example=None
 for gid,g in enumerate(graphs):
  for f in range(len(Instance(g).faces)):
   b=Instance(g,f); ss=list(b.states()); ps=b.pairs(ss)
   bad={s for r,s in ps if not nx.is_forest(b.Q(s))}
   cyclic+=len(bad)
   if bad and example is None: example=dict(gid=gid,root=f,state=list(sorted(bad)[0]),edges=list(g.edges()))
 rows.append(dict(V=v,graphs=len(graphs),partnered_cyclic_states=cyclic,witness=example))
 print(v,len(graphs),cyclic)
assert all(r['partnered_cyclic_states']==0 for r in rows[:-1]) and rows[-1]['partnered_cyclic_states']>0
(OUT/'recompute.json').write_text(json.dumps(rows,indent=2)+'\n')
