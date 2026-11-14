import json,itertools as it,networkx as nx,numpy as np
from pathlib import Path
O=Path(__file__).parent; d=json.loads((O/'example.json').read_text()); T=nx.Graph(d['edges']);F=d['faces'];A=d['A'];W=d['white'];roots=d['roots'];xy={int(k):np.array(v) for k,v in d['coordinates'].items()}; c={i:sum((xy[v] for v in f))/3 for i,f in enumerate(F)}
def edge(u,v):return tuple(sorted((u,v)))
def q(s):
 g=nx.Graph();g.add_nodes_from(T);g.add_edges_from(tuple(v for v in F[t] if v!=x) for t,x in zip(A,s));return g
r,s=d['cyclic_pair'];rg,sg=d['forest_pair'];Q=q(s); C=nx.cycle_basis(Q)[0]; ce={edge(u,v) for u,v in zip(C,C[1:]+C[:1])}
def flip(r,s):return [next(v for v in F[t] if v not in [x,y]) if edge(*[v for v in F[t] if v!=y]) in ce else x for t,x,y in zip(A,r,s)]
r2=flip(r,s);assert flip(r2,s)==r and sorted(r2)==d['X'];assert all(x!=y for x,y in zip(r2,s))
def delta(u,v):
 t=next(i for i in d['black'] if u in F[i] and v in F[i]); z=next(vv for vv in F[t] if vv not in [u,v]); val=np.cross(xy[v]-xy[u],xy[z]-xy[u]);return (1 if val>0 else -1)*(-1 if t==0 else 1)
def J(r,s):return sum(delta(u,v) for u,v in zip(r,s))//3
assert abs(J(r2,s)-J(r,s))==2
# White tree edges cross the deleted spokes.
WT=nx.Graph();WT.add_nodes_from(W);links=[]
for t,x in zip(A,sg):
 sides=[edge(x,v) for v in F[t] if v!=x]; ws=[next(w for w in W if set(e)<=set(F[w])) for e in sides];WT.add_edge(*ws);links.append((t,x,ws,sides))
assert nx.is_tree(WT)
e0=edge(*roots[:2]);y0=next(w for w in W if set(e0)<=set(F[w]));dep=nx.single_source_shortest_path_length(WT,y0);P=[e0]
for t,x,ws,sides in links:P.append(sides[int(dep[ws[1]]>dep[ws[0]])])
PF=nx.Graph();PF.add_nodes_from(T);PF.add_edges_from(P);assert nx.is_forest(PF) and nx.number_connected_components(PF)==2
parts=[sorted(z) for z in nx.connected_components(PF)];assert all(nx.is_tree(T.subgraph(z)) for z in parts)
G=nx.Graph();G.add_nodes_from(range(len(F)));cross={}
for i,j in it.combinations(G,2):
 e=tuple(sorted(set(F[i])&set(F[j])))
 if len(e)==2:G.add_edge(i,j);cross[edge(i,j)]=e
HC=nx.Graph();HC.add_nodes_from(G);HC.add_edges_from(e for e,v in cross.items() if v not in P);assert nx.is_connected(HC) and all(v==2 for _,v in HC.degree())
# Find a disconnected 2-factor by enumerating perfect matchings of the cubic dual.
match=[]
def rec(left,es):
 if not left:
  h=G.copy();h.remove_edges_from(es)
  if not nx.is_connected(h):match.append(list(h.edges()))
  return bool(match)
 u=min(left)
 for v in G[u]:
  if v in left and rec(left-{u,v},es+[(u,v)]):return True
 return False
assert rec(set(G),[])
# Bounded disk of a D cycle, flood fill without crossing its sides.
D=nx.DiGraph(zip(r,s));cycles=list(nx.simple_cycles(D));cy=max(cycles,key=len);cedges={edge(u,v) for u,v in zip(cy,cy[1:]+cy[:1])}
bar=G.copy();bar.remove_edges_from(e for e,v in cross.items() if v in cedges);outside=nx.node_connected_component(bar,0);inside=set(G)-outside
B=len(inside&set(d['black']));WW=len(inside&set(W));I=len(set(v for f in inside for v in F[f])-set(cy));h=len(cy);ell=sum(any(set(e)<=set(F[b]) for b in inside&set(d['black'])) for e in cedges)
assert B+WW==2*I+h-2 and 3*(B-WW)==2*ell-h and B==I+ell
# Area weights implement positive circulation on every simple spoke polygon.
weights={str(t):{str(v):float(np.linalg.det(np.array([c[t],xy[v]]))/2) for v in F[t]} for t in A}
circs=[]
for cycle in cycles:
 area=sum(float(np.linalg.det(np.array([xy[u],xy[v]])))/2 for u,v in zip(cycle,cycle[1:]+cycle[:1]))
 if area<0:cycle=list(reversed(cycle))
 circ=0
 for u,v in zip(cycle,cycle[1:]+cycle[:1]):
  t=next(t for t in A if u in F[t] and v in F[t]);circ+=weights[str(t)][str(v)]-weights[str(t)][str(u)]
 assert circ>0;circs.append(circ)
d.update(reversed_pair=[r2,s],Q_cycle=C,white_tree=list(WT.edges()),white_root=y0,selected_edges=P,parts=parts,hamiltonian=list(HC.edges()),two_factor=match[0],dual_edges=list(G.edges()),dual_crossings=[[*e,*v] for e,v in cross.items()],disk=dict(cycle=cy,faces=sorted(inside),B=B,W=WW,I=I,h=h,l=ell),spoke_weights=weights,circulations=circs,J=[J(r,s),J(r2,s)],D_cycles=cycles)
(O/'checked.json').write_text(json.dumps(d,indent=2)); print(d['counts'],d['disk'],'J',d['J'],'circulation',circs)
