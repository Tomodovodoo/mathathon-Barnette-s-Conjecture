from verify import ROOT,OUT,instance
import json
import networkx as nx
from collections import Counter
from itertools import combinations
D=json.loads((ROOT/'research/2026-11-14_fable_digestions/data/examples.json').read_text());out={}
for name,d in D.items():
 if 'info' not in d:continue
 b=instance(d['faces'],d['t0']);faceid={i:next(j for j,f in enumerate(d['faces']) if set(f)==set(b.faces[i])) for i in range(len(b.faces))};A=d['A'];ix={t:i for i,t in enumerate(A)}
 def state(s):return tuple(s[ix[faceid[t]]] for t in b.A)
 ori={}
 for t,f in enumerate(d['faces']):
  for u,v in zip(f,f[1:]+f[:1]):ori[u,v]=t
 black=set(A)|{d['t0']}
 def sign(r,s):
  ans=1
  for u,v in zip(r,s):ans*=1 if ori[u,v] in black else -1
  return ans
 ss=list(b.states());ps=b.pairs(ss);counter=0;poly=Counter();linear=Counter()
 weights={tuple(map(int,k.split(','))):v for k,v in d['spoke_weights'].items()}
 for row in d['states']:
  s=state(row['s']);assert s in ss
  partners=[r for r,t in ps if t==s];assert set(partners)=={state(r) for r in row['partners']}
  assert b.is_tree(s)==row['tree_matching']
  q=b.Q(s);assert sorted(len(set(c)&b.R) for c in nx.connected_components(q))==sorted(row['roots_per_component'])
  omega=sum(weights.get((t,v),0) for t,v in zip(A,row['s']));assert omega==row['omega']
 for cover in d['covers']:
  for c in cover['cycles']:
   cyc=c['cycle'];barrier={tuple(sorted((u,v))) for u,v in zip(cyc,cyc[1:]+cyc[:1])};g=b.G.copy();g.remove_edges_from(b.dual_edges[e] for e in barrier);inside=set(g)-nx.node_connected_component(g,b.outer)
   oldinside={faceid[t] for t in inside};verts=set(v for t in inside for v in b.faces[t])-set(cyc)
   vals={'B':len(oldinside&black),'W':len(oldinside-black),'I':len(verts),'h':len(cyc),'l':sum((ori[u,v] if ori[u,v] in black else ori[v,u]) in oldinside for u,v in zip(cyc,cyc[1:]+cyc[:1]))}
   for k,v in vals.items():assert c[k]==v,(name,k)
   assert sorted(verts)==c['inner_vertices'];assert sorted(oldinside-black)==c['white_inside'];counter+=1
  for row in cover['pairs']:
   r,s=row['r'],row['s'];assert (state(r),state(s)) in ps
   J=sum(1 if ori[u,v] in black else -1 for u,v in zip(r,s))//3
   assert J==row['J'] and sign(r,s)==row['eps']
   ws=[weights.get((t,v),0) for t,v in zip(A,s)];assert sum(ws)==row['omega_s']
   poly[sum(ws)]+=sign(r,s)
   coeff=[1]
   for w in ws:
    nxt=coeff+[0]
    for i,a in enumerate(coeff):nxt[i+1]+=w*a
    coeff=nxt
   for i,v in enumerate(coeff):linear[i]+=sign(r,s)*v
 expected={int(k):v for k,v in d['P_coefficients'].items()} if isinstance(d['P_coefficients'],dict) else dict(enumerate(d['P_coefficients']))
 assert {k:v for k,v in linear.items() if v}=={k:v for k,v in expected.items() if v},(name,linear,expected)
 out[name]={'disks':counter,'signed_polynomial':{k:v for k,v in poly.items() if v},'linear_polynomial':{k:v for k,v in linear.items() if v},'states_checked':len(ss),'ordered_pairs_checked':len(ps)}
(OUT/'detail-checks.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
