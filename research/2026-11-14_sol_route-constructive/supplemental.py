"""Independent checks of region bound 3.3 and exact regrouping 5.4--5.5."""
import json
from pathlib import Path
from itertools import product
from collections import Counter,defaultdict
import networkx as nx
from barnette_lab.core import *
from barnette_lab.algorithms import pool

exe=Path('workings/barnette_lab/vendor/plantri.exe').resolve(); rows=[]
for n in range(6,15):
 for index,t in enumerate(plantri_graphs(n,exe)):
  b=Instance(t); row={'n':n,'index':index,'regions':0,'groups':0}
  if n<=10:
   for bits in product((0,1),repeat=n):
    u={v for v,bit in zip(b.T,bits) if bit}; k=b.T.subgraph(u)
    if len(u)<4 or not nx.is_connected(k): continue
    d=b.G.copy(); d.remove_edges_from(b.dual_edges[edge(v,w)] for v,w in k.edges())
    for region in nx.connected_components(d):
     length=sum(int(b.sides[v,w] in region)+int(b.sides[w,v] in region) for v,w in k.edges())
     balance=len(region&set(b.black))-len(region&set(b.white))
     signed=sum((1 if b.sides[v,w] in b.black else -1) if b.sides[v,w] in region else 0 for v,w in list(k.edges())+[(w,v) for v,w in k.edges()])
     assert 3*balance==signed
     if length>=4: assert abs(balance)<=length-4
     row['regions']+=1
  groups=defaultdict(list)
  for p in b.pairs():
   key=tuple((t,edge(r,s)) for t,r,s in zip(b.A,*p))
   groups[key].append(p)
  for ps in groups.values():
   p=ps[0]; cycles=b.dcycles(*p); expected=Counter({0:(-1)**((b.n-len(cycles))//2)})
   gaps=[]
   for c in cycles:
    plus,minus=len(pool(b,p,c,True)),len(pool(b,p,c,False)); gaps.append(plus-minus)
    nxt=Counter()
    for power,value in expected.items():
     nxt[power+plus]+=value; nxt[power+minus]-=value
    expected=nxt
   expected={k:v for k,v in expected.items() if v}
   assert expected==b.polynomial(ps)
   m=len(cycles)
   from math import comb,prod
   leading=sum(v*comb(k,m) for k,v in expected.items() if k>=m)
   assert leading==(-1)**((b.n-m)//2)*prod(gaps)
   row['groups']+=1
  rows.append(row)
Path('research/2026-11-14_sol_route-constructive/data/supplemental.json').write_text(json.dumps(rows,indent=2))
print('rows',len(rows),'regions',sum(r['regions'] for r in rows),'groups',sum(r['groups'] for r in rows))
