"""Predictions in ../TESTS.md; all results are T4, independently unreviewed."""
import sys,json,itertools,time
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'workings/barnette_lab'))
from barnette_lab.core import Instance,plantri_graphs,named_graphs,edge,hamiltonian_cycle,faces_of
from barnette_lab.algorithms import separators
out={}; start=time.time()
census=[]; examples=[]
for n in range(6,13):
 row=dict(n=n,graphs=0,roots=0,pair_obstruction_failures=0,separator_parity_disagreements=0)
 for g in plantri_graphs(n,ROOT/'workings/barnette_lab/vendor/plantri.exe'):
  row['graphs']+=1
  for root in range(len(Instance(g).faces)):
   b=Instance(g,root); sep=separators(b); row['roots']+=1
   bad=any(x[2] for x in sep)
   row['pair_obstruction_failures']+=((b.flow_pair() is None)!=bad)
   for tri,comps,black in sep:
    inside=next(c for c in comps if not c&b.R)
    if (len(inside)%2==1)!=black:
     row['separator_parity_disagreements']+=1
     if len(examples)<3: examples.append(dict(n=n,root=root,tri=tri,inside=sorted(inside),black=black,edges=list(g.edges())))
 census.append(row)
out['census']=census;out['same_T_parity_counterexamples']=examples
rows=[]
for name,g in named_graphs().items():
 b=Instance.from_primal(g); row={'name':name,'vertices':len(g),'separators':len(separators(b))}
 if name!='truncated_cuboctahedron':
  ss=list(b.states()); pp=b.pairs(ss); ts=[s for s in ss if b.is_tree(s)]
  counts={}; treecounts={}
  for r,s in pp:
   k=len(b.dcycles(r,s)); counts[k]=counts.get(k,0)+1
   if b.is_tree(s):treecounts[k]=treecounts.get(k,0)+1
  row.update(states=len(ss),pairs=len(pp),trees=len(ts),D_cycles=counts,tree_pair_D_cycles=treecounts)
  frequencies={str(e):0 for e in b.G.edges()}
  for s in ts:
   cy=b.recover(s)['cycle']; es={edge(u,v) for u,v in zip(cy,cy[1:]+cy[:1])}
   for e in b.G.edges():frequencies[str(e)]+=edge(*e) in es
  row['fixed_root_edge_counts']=frequencies
 # Force every edge by avoiding another incident edge.
 successes=0
 for u,v in g.edges():
  w=next(w for w in g[u] if w!=v);cy=hamiltonian_cycle(g,(u,w));es={edge(a,z) for a,z in zip(cy,cy[1:]+cy[:1])}
  assert edge(u,v) in es;successes+=1
 row['forced_edges']=successes;rows.append(row)
out['named']=rows
# Contract the square faces in the truncated octahedron.
g=named_graphs()['truncated_octahedron'];fs,_=faces_of(nx.check_planarity(g)[1]); squares=[f for f in fs if len(f)==4];owner={v:i for i,f in enumerate(squares) for v in f}
r=nx.Graph();r.add_nodes_from(range(len(squares)))
for u,v in g.edges():
 if owner[u]!=owner[v]:r.add_edge(owner[u],owner[v])
out['contracted_counterexample']={'R_edges':list(r.edges()),'is_octahedron':nx.is_isomorphic(r,nx.octahedral_graph()),'outer_triangle_interior':len(r)-3,'original_dual_separators':len(separators(Instance.from_primal(g)))}
# Independent matching-complement Hamiltonian enumeration, valid for cubic graphs.
def matchings(g):
 def go(left,es):
  if not left:yield es;return
  u=min(left)
  for v in g[u]:
   if v in left:yield from go(left-{u,v},es+[edge(u,v)])
 yield from go(set(g),[])
def nonplanar(g):
 ms=list(matchings(g));hs=[]
 for m in ms:
  h=g.copy();h.remove_edges_from(m)
  if nx.is_connected(h):hs.append(set(map(lambda e:edge(*e),h.edges())))
 es=list(g.edges());extend=all(any(edge(*a) in m and edge(*b) in m for m in ms) for a,b in itertools.combinations(es,2) if len(set(a+b))==4)
 paths={tuple(p) for p in nx.all_simple_paths(g,0,1,cutoff=3) if len(p)==4} # full P4 test below
 missing=0;total=0
 for a,b in g.edges():
  for x in g[a]:
   for y in g[b]:
    if len({x,a,b,y})==4:
     total+=1; wanted={edge(x,a),edge(a,b),edge(b,y)};missing+=not any(wanted<=h for h in hs)
 return dict(vertices=len(g),edges=list(g.edges()),planar=nx.check_planarity(g)[0],connectivity=nx.node_connectivity(g),brace_by_two_extendability=extend,perfect_matchings=len(ms),Hamiltonian_cycles=len(hs),P4_tests=total,P4_failures=missing)
cube=nx.cubical_graph();face=next(f for f in faces_of(nx.check_planarity(cube)[1])[0] if len(f)==4)
trisum=nx.Graph()
for k in range(3):
 mapping={v:face.index(v) if v in face else 4+k*4+list(sorted(set(cube)-set(face))).index(v) for v in cube}
 trisum=nx.compose(trisum,nx.relabel_nodes(cube,mapping))
trisum.remove_edges_from((i,(i+1)%4) for i in range(4))
out['nonplanar']={'Heawood':nonplanar(nx.heawood_graph()),'cube_trisum':nonplanar(trisum),'K33_control':nonplanar(nx.complete_bipartite_graph(3,3))}
out['seconds']=time.time()-start
Path(__file__).with_name('results.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:v for k,v in out.items() if k in ['census','contracted_counterexample','seconds']},indent=2))
