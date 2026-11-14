import sys,json
from pathlib import Path
import networkx as nx
R=Path(__file__).resolve().parents[3];sys.path.insert(0,str(R/'workings/barnette_lab'))
from barnette_lab.core import Instance,dual_graph
out=[]
for name,t in [('octahedron',nx.octahedral_graph()),('hexagonal_bipyramid',dual_graph(nx.circular_ladder_graph(6)))]:
 b=Instance(t); mids={tuple(sorted(e)):len(t)+i for i,e in enumerate(t.edges())};g=nx.Graph()
 for u,v in t.edges():g.add_edges_from([(u,mids[tuple(sorted((u,v)))]),(v,mids[tuple(sorted((u,v)))])])
 for a,c,d in b.faces:
  vs=[mids[tuple(sorted(e))] for e in [(a,c),(c,d),(d,a)]];g.add_edges_from([(vs[0],vs[1]),(vs[1],vs[2]),(vs[2],vs[0])])
 b=Instance(g); ss=list(b.states());ps=b.pairs(ss);hist={};thist={}
 for r,s in ps:
  k=len(b.dcycles(r,s));hist[k]=hist.get(k,0)+1
  if b.is_tree(s):thist[k]=thist.get(k,0)+1
 out.append(dict(name=name,dual_vertices=len(g),primal_vertices=len(b.G),face_sizes=sorted(set(dict(g.degree()).values())),states=len(ss),pairs=len(ps),D_cycles=hist,tree_D_cycles=thist,edges=list(g.edges())))
Path(__file__).with_name('refined.json').write_text(json.dumps(out,indent=2));print([{k:v for k,v in x.items() if k!='edges'} for x in out])
