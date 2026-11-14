from campaign import *
from special import dual_multi
# A noncubic obstruction with bipartiteness, planarity and 3-connectivity retained.
a=nx.Graph();a.add_edges_from([(0,1),(1,2),(2,0)]+[(v,w) for v in (3,4) for w in range(3)])
_,emb=nx.check_planarity(a);fs,_=faces_of(emb);g=nx.Graph();g.add_edges_from((v,5+i) for i,f in enumerate(fs) for v in f)
assert len(g)==11 and nx.is_bipartite(g) and nx.check_planarity(g)[0] and nx.node_connectivity(g)==3
save('examples/noncubic11.json',{'edges':list(g.edges()),'bipartition':[list(range(5)),list(range(5,11))]})
# Store all missing cycles and their inverse state in the first non-surjective case.
x=json.load(open(OUT/'examples/t8_0.json'));b=Instance(nx.Graph(x['dual_edges']));cs=cycles(b.G);e=next(e for e in itertools.combinations(b.faces[0],2) if sum(b.dual_edges[edge(*e)] not in c for c in cs)>2)
image=[]
for s in b.states():
 if b.is_tree(s):
  z=b.recover(s,e);cy=z['cycle'];image.append({'state':s,'edges':sorted(edge(a,z) for a,z in zip(cy,cy[1:]+cy[:1]))})
save('examples/prism_recovery.json',{'dual_edges':list(b.T.edges()),'primal_edges':list(b.G.edges()),'outer':0,'e0':e,'forbidden_primal_edge':b.dual_edges[edge(*e)],'image':image,'all_avoiding':[sorted(c) for c in cs if b.dual_edges[edge(*e)] not in c]})
# Verify every literal adjacency certificate, independent from reference recovery.
for f in sorted((OUT/'examples').glob('t[0-9]*_*.json')):
 x=json.load(open(f));g=nx.Graph(x['primal_edges']);assert nx.is_bipartite(g) and all(d==3 for _,d in g.degree()) and nx.node_connectivity(g)==3
# The generalized disk defect is B-I-l=-1 for this witness.
x=json.load(open(OUT/'examples/nonbijective_disk.json'));b=Instance(nx.Graph(x['dual_edges']),x['outer']);c=x['cycle'];dg=b.G.copy();dg.remove_edges_from(b.dual_edges[edge(a,z)] for a,z in zip(c,c[1:]+c[:1]));inside=next(v for v in nx.connected_components(dg) if b.outer not in v)
B=len(set(b.black)&inside);W=len(inside)-B;I=len(set().union(*(set(b.faces[f]) for f in inside))-set(c));l=sum(next(f for f in (b.sides[a,z],b.sides[z,a]) if f in b.black) in inside for a,z in zip(c,c[1:]+c[:1]));save('data/disk_defect.json',{'B':B,'W':W,'I':I,'l':l,'h':len(c),'defect':B-I-l});assert (B,W,I,l)==(2,2,1,2)
event('Adjacency certificates checked; stored prism recovery failure and noncubic11')
