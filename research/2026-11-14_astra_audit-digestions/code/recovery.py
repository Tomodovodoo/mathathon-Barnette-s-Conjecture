from verify import ROOT,OUT,instance
import json
import networkx as nx
D=json.loads((ROOT/'research/2026-11-14_fable_digestions/data/examples.json').read_text());report={}
for name in ['octahedron','running']:
 d=D[name];b=instance(d['faces'],d['t0']);by={frozenset(f):i for i,f in enumerate(d['faces'])};idx={t:i for i,t in enumerate(d['A'])}
 src=(3,4,5) if name=='octahedron' else (6,2,8,1,3,10,11,7,12,9)
 s=tuple(src[idx[by[frozenset(b.faces[t])]]] for t in b.A)
 rec=b.recover(s,(0,1) if name=='octahedron' else (0,4))
 expected=[(0,1),(1,3),(2,4),(4,5)] if name=='octahedron' else [(0,2),(0,4),(0,6),(1,9),(3,9),(5,11),(6,7),(7,8),(9,10),(10,11),(11,12)]
 assert set(rec['P'])==set(expected)
 assert all(nx.is_tree(b.T.subgraph(c)) for c in rec['classes'])
 rec['cycle_source_faces']=[by[frozenset(b.faces[t])] for t in rec['cycle']];report[name]=rec
# Nonbijective disk, recompute through the lab dual cut.
d=D['nonbijective_disk'];b=instance(d['faces'],d['outer']);c=d['disk']['cycle'];edges=[tuple(sorted(e)) for e in zip(c,c[1:]+c[:1])];g=b.G.copy();g.remove_edges_from(b.dual_edges[e] for e in edges);inside=set(g)-nx.node_connected_component(g,b.outer);B=len(inside&set(b.black));W=len(inside&set(b.white));I=len(set(v for t in inside for v in b.faces[t])-set(c));assert (B,W,I)==(2,2,1);report['nonbijective']={'B':B,'W':W,'I':I,'h':len(c)}
# Gluing certificates are vertex classes; verify inducedness in the full lab graph.
d=D['double_octahedron'];b=instance(d['faces'],1);classes=[{2,3,5,8},{0,1,4,6,7}];assert all(nx.is_tree(b.T.subgraph(c)) for c in classes);assert set.union(*classes)==set(b.T)
mixed=[b.dual_edges[tuple(sorted((u,v)))] for u,v in b.T.edges() if (u in classes[0])!=(v in classes[0])];h=nx.Graph(mixed);assert nx.is_connected(h) and len(h)==14 and all(v==2 for _,v in h.degree());assert b.dual_edges[(0,1)] not in mixed
report['gluing']={'classes':[sorted(c) for c in classes],'cycle_order':len(h),'avoids_01_dual':True}
(OUT/'recovery.json').write_text(json.dumps(report,indent=2));print('Recovery, nonbijective disk and gluing passed.')
