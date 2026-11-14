import sys,json,time
from pathlib import Path
import networkx as nx
R=Path(__file__).resolve().parents[3];sys.path.insert(0,str(R/'workings/barnette_lab'))
from barnette_lab.core import Instance,plantri_graphs
out=[];start=time.time()
for n in range(6,17):
 for g in plantri_graphs(n,R/'workings/barnette_lab/vendor/plantri.exe'):
  if not all(d in (4,6) for _,d in g.degree()):continue
  b=Instance(g);ss=list(b.states());ps=b.pairs(ss)
  counts={}
  for r,s in ps:
   k=len(b.dcycles(r,s));counts[k]=counts.get(k,0)+1
  out.append(dict(dual_order=n,states=len(ss),pairs=len(ps),c_min=min(counts) if counts else None,counts=counts,edges=list(g.edges())))
Path(__file__).with_name('goodey.json').write_text(json.dumps(out,indent=2));print('graphs',len(out),'cmin values',sorted(set(x['c_min'] for x in out if x['c_min'] is not None)),'seconds',time.time()-start)

