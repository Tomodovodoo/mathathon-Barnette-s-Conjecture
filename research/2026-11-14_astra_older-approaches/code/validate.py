"""Spot checks, not an independent referee or certification."""
import sys,json,itertools
from pathlib import Path
import networkx as nx
P=Path(__file__).resolve().parents[1];R=P.parents[1];sys.path.insert(0,str(R/'workings/barnette_lab'))
from barnette_lab.core import Instance,plantri_graphs
checks={'chain_band_incidence':0,'radial_dictionary_partitions':0}
for row in json.loads((P/'code/chains.json').read_text()):
 b=Instance(nx.Graph(row['edges']),row['root'])
 for t in b.A:
  levels=[v//3 for v in b.faces[t]];assert levels.count(max(levels))==2 and max(levels)-min(levels)==1
  checks['chain_band_incidence']+=1
# Enumerate all vertex subsets on every small dual and compare the two predicates.
for n in range(6,13):
 for g in plantri_graphs(n,R/'workings/barnette_lab/vendor/plantri.exe'):
  b=Instance(g)
  # Propagate unique three-colouring from a triangle.
  color=dict(zip(b.faces[0],range(3)))
  while len(color)<len(g):
   changed=False
   for f in b.faces:
    missing=[v for v in f if v not in color]
    if len(missing)==1:
     color[missing[0]]=next(iter({0,1,2}-{color[v] for v in f if v in color}));changed=True
   assert changed or len(color)==len(g)
  blue={v for v in g if color[v]==0};other=set(g)-blue
  for bits in range(1,2**n-1):
   s={v for v in g if bits>>v&1};u=s&blue;d=s&other
   independent=not g.subgraph(d).number_of_edges()
   permeates=all(s&set(f) for f in b.faces)
   lhs=independent and nx.is_tree(g.subgraph(s)) and permeates
   radial=nx.Graph();radial.add_nodes_from(s);radial.add_edges_from((a,z) for a in u for z in d if g.has_edge(a,z))
   rhs=independent and nx.is_tree(radial) and all(2*len(set(g[v])&d)==g.degree(v) for v in blue-u)
   assert lhs==rhs,(n,bits)
   checks['radial_dictionary_partitions']+=1
(P/'code/validation.json').write_text(json.dumps(checks,indent=2));print(checks)
