# Prediction before this test: a chain of k octahedra rooted at its end has c_min=k.
import sys,json
from pathlib import Path
import networkx as nx
R=Path(__file__).resolve().parents[3];sys.path.insert(0,str(R/'workings/barnette_lab'))
from barnette_lab.core import Instance
out=[]
for k in range(1,9):
 g=nx.Graph()
 for i in range(k+1):g.add_edges_from((3*i+j,3*i+(j+1)%3) for j in range(3))
 for i in range(k):g.add_edges_from((3*i+j,3*(i+1)+h) for j in range(3) for h in range(3) if j!=h)
 b=Instance(g);root=next(i for i,f in enumerate(b.faces) if set(f)=={0,1,2});b=Instance(g,root);ss=list(b.states());ps=b.pairs(ss);hist={}
 for r,s in ps:
  c=len(b.dcycles(r,s));hist[c]=hist.get(c,0)+1
 out.append(dict(k=k,states=len(ss),pairs=len(ps),D_cycles=hist,faces=sorted(set(dict(g.degree()).values())),root=root,edges=list(g.edges())))
Path(__file__).with_name('chains.json').write_text(json.dumps(out,indent=2));print([{k:v for k,v in x.items() if k!='edges'} for x in out])
