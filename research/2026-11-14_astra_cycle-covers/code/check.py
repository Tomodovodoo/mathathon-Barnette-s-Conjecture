from pathlib import Path
import sys,json,networkx as nx
from collections import defaultdict
from explore import family,covers,describe,Instance
p=Path(__file__).resolve().parents[1];root=p.parents[1]
rows=[]
for m in range(2,7):
 I=family(m);ss=list(I.states());pairs=I.pairs(ss);us=list(covers(I))
 assert len(us)==1
 u=us[0];cs=describe(I,u);assert len(cs)==m-1
 assert len(pairs)==2**(m-1);assert sum(I.is_tree(s) for s in ss)==len(pairs)
 w=I.weights();om=lambda s:sum(w[t,v] for t,v in zip(I.A,s))
 poly=defaultdict(int)
 for r,s in pairs:poly[om(s)]+=I.sign(r,s)
 from math import factorial
 lead=sum(v*k**(m-1) for k,v in poly.items())//factorial(m-1)
 assert abs(lead)==2
 rows.append({'m':m,'states':len(ss),'pairs':len(pairs),'cmin':len(cs),'lead':lead,'polynomial':dict(poly)})
 print(rows[-1],flush=True)
# Previously saved four-element square; verify adjacency by a directed single-cycle reversal.
f=root/'research/2026-11-14_opus_conjectures/data/c2_counterexample_V18.json'
a=json.loads(f.read_text());T=nx.Graph(a['edges']);b=Instance(T);I=Instance(T,next(i for i,f in enumerate(b.faces) if set(f)==set(a['roots'])))
us=list(covers(I));cnt=[len(describe(I,u)) for u in us];edges=[]
for i,u in enumerate(us):
 for j,v in enumerate(us[:i]):
  delta=nx.Graph()
  for t,x,y in zip(I.A,u,v):
   if x!=y:delta.add_edges_from([(('t',t),('v',x)),(('t',t),('v',y))])
  if len(delta) and nx.is_connected(delta) and all(d==2 for _,d in delta.degree()):edges.append([j,i])
assert sorted(cnt)==[1,1,3,3]
assert len(edges)==4 and all(cnt[i]!=cnt[j] for i,j in edges)
(p/'data/check.json').write_text(json.dumps({'family':rows,'level_counterexample':{'source':str(f),'cycles':cnt,'flip_edges':edges,'u':us}},indent=2))
print('Every simple directed-cycle flip gives the square:',cnt,edges)
