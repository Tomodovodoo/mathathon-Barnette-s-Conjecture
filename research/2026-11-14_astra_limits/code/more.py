from special import *
from scipy.optimize import milp,Bounds,LinearConstraint
import numpy as np
h=json.load(open(OUT/'data/hog954.json'));g=nx.Graph({i:a for i,a in enumerate(h['adjacencyList'])});save('examples/BBL38.json',{'edges':list(g.edges()),'source':'https://houseofgraphs.org/api/graphs/954'})
out=[]
for name in ['K4','BBL38','Tutte46']:
 g=nx.Graph(json.load(open(OUT/f'examples/{name}.json'))['edges']);nv=len(g);es=list(g.edges());mat=[];ub=[]
 for j,(u,v) in enumerate(es):
  r=np.zeros(nv+len(es));r[nv+j]=1;r[u]=-1;r[v]=-1;mat.append(r);ub.append(0)
  r=np.zeros(nv+len(es));r[nv+j]=1;r[u]=1;r[v]=1;mat.append(r);ub.append(2)
 res=milp(np.r_[np.zeros(nv),-np.ones(len(es))],integrality=np.ones(nv+len(es)),bounds=Bounds(0,1),constraints=LinearConstraint(mat,-np.inf,ub),options={'time_limit':60})
 assert res.success
 col=np.rint(res.x[:nv]).astype(int).tolist();d,fs,corners=dual_multi(g)
 out.append({'name':name,'maximum_cut':round(-res.fun),'mip_gap':res.mip_gap,'coloring':col,'monochromatic_edges':[list(e) for e in es if col[e[0]]==col[e[1]]],'odd_dual_vertices':[v for v,k in d.degree() if k%2]})
save('data/nonbipartite.json',out)
# Test a natural overstrengthening on the smallest Barnette graph.
b=Instance(nx.octahedral_graph());cs=cycles(b.G);bad=None
for start in b.G:
 def walk(p):
  if len(p)==5:
   yield p;return
  for v in b.G[p[-1]]:
   if v not in p:yield from walk(p+[v])
 for p in walk([start]):
  if not any(set(edge(a,z) for a,z in zip(p,p[1:]))<=c for c in cs):bad=p;break
 if bad:break
save('examples/P5_cube.json',{'primal_edges':list(b.G.edges()),'path':bad,'all_hamiltonian_cycles':[sorted(c) for c in cs]})
# Zero weights and relaxed torus states.
b=Instance(nx.octahedral_graph());save('data/zero_weights.json',{'pairs':[{'r':r,'s':s,'J':b.J(r,s),'sign':b.sign(r,s)} for r,s in b.pairs()],'sum_signs':sum(b.sign(r,s) for r,s in b.pairs())})
t=json.load(open(OUT/'examples/torus_3x3.json'));black=t['black_faces'];r=[f[0] for f in black];s=[f[1] for f in black];assert len(set(r))==len(set(s))==9
q=nx.Graph();q.add_nodes_from(range(9));q.add_edges_from(tuple(set(f)-{v}) for f,v in zip(black,s));save('data/torus_states.json',{'unrooted_r':r,'unrooted_s':s,'Q_edges':list(q.edges()),'Q_cycles':nx.cycle_basis(q),'original_A':8,'original_X':6})
event('Maximum-cut relaxations solved for K4, BBL38, Tutte46; torus unrooted pair and zero-weight cancellation checked')
print(out);print('P5',bad)
