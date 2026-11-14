import networkx as nx, numpy as np, itertools as it, json
from pathlib import Path
OUT=Path(__file__).parent

def faces(G):
 ok,emb=nx.check_planarity(G); assert ok
 seen=set(); fs=[]
 for u,v in emb.edges():
  if (u,v) not in seen: fs.append(emb.traverse_face(u,v,seen))
 return fs

def model(G):
 gf=faces(G); T=nx.Graph(); T.add_nodes_from(range(len(gf)))
 for i,j in it.combinations(range(len(gf)),2):
  if len(set(gf[i])&set(gf[j]))==2:T.add_edge(i,j)
 fs=faces(T); assert all(len(f)==3 for f in fs)
 adj=nx.Graph(); adj.add_nodes_from(range(len(fs)))
 for i,j in it.combinations(range(len(fs)),2):
  if len(set(fs[i])&set(fs[j]))==2:adj.add_edge(i,j)
 col=nx.bipartite.color(adj); black=[i for i in adj if col[i]==col[0]]; white=[i for i in adj if i not in black]
 roots=fs[0]; A=[i for i in black if i!=0]; X=sorted(set(T)-set(roots)); states=[]
 def rec(s,used):
  if len(s)==len(A):states.append(s.copy()); return
  t=A[len(s)]
  for v in fs[t]:
   if v in X and v not in used:rec(s+[v],used|{v})
 rec([],set())
 def q(s):
  Q=nx.Graph();Q.add_nodes_from(T)
  Q.add_edges_from(tuple(v for v in fs[t] if v!=x) for t,x in zip(A,s));return Q
 pairs=[(r,s) for r in states for s in states if all(a!=b for a,b in zip(r,s))]
 cyclic=[(r,s) for r,s in pairs if not nx.is_forest(q(s))]
 good=[(r,s) for r,s in pairs if nx.is_forest(q(s))]
 print(len(T),len(states),len(pairs),len(cyclic),'cyclic',flush=True)
 return T,fs,black,white,roots,A,X,states,pairs,cyclic,good,q
if __name__=='__main__':
 pts=sorted(set(it.permutations((0,1,2))))
 pts=sorted(set(tuple(a*s for a,s in zip(p,sgn)) for p in pts for sgn in it.product((-1,1),repeat=3)))
 G=nx.Graph();G.add_nodes_from(range(len(pts)))
 G.add_edges_from((i,j) for i,j in it.combinations(G,2) if sum((a-b)**2 for a,b in zip(pts[i],pts[j]))==2)
 G=nx.read_adjlist(OUT/'running-primal.adjlist',nodetype=int)
 m=model(G)
 T,fs,black,white,roots,A,X,states,pairs,cyclic,good,q=m
 r,s=cyclic[0];rg,sg=good[0]
 xy={roots[0]:np.array([0.,0.]), roots[1]:np.array([12.,0.]),roots[2]:np.array([6.,10.392])}
 L=nx.laplacian_matrix(T,nodelist=X+roots).toarray();sol=np.linalg.solve(L[:len(X),:len(X)],-L[:len(X),len(X):]@np.array([xy[v] for v in roots]))
 xy.update(dict(zip(X,sol)))
 data=dict(vertices=list(T),edges=list(T.edges()),faces=fs,black=black,white=white,roots=roots,A=A,X=X,cyclic_pair=[r,s],forest_pair=[rg,sg],coordinates={str(v):p.tolist() for v,p in xy.items()},counts=dict(states=len(states),pairs=len(pairs),cyclic_pairs=len(cyclic)))
 if (OUT/'layout.json').exists(): data['coordinates']=json.loads((OUT/'layout.json').read_text())
 (OUT/'example.json').write_text(json.dumps(data,indent=2))


