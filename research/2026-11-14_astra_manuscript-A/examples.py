"""Recompute manuscript examples using the reference implementation.
Run from repository root: python research/2026-11-14_astra_manuscript-A/examples.py
"""
import sys,json
sys.dont_write_bytecode=True
from pathlib import Path
from collections import Counter
import networkx as nx
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'workings/barnette_lab'))
from barnette_lab.core import Instance,check_cycle
OUT=Path(__file__).parent
result={}
for name in ['cube','truncated_octahedron']:
 data=json.loads((ROOT/f'workings/barnette_lab/examples/{name}.json').read_text())
 b=Instance(nx.Graph(data['T_edges']))
 # Translate by corner sets, so face indices need not agree.
 fmap={i:next(j for j,f in enumerate(b.faces) if set(f)==set(face)) for i,face in enumerate(data['faces'])}
 b=Instance(b.T,outer=fmap[data['outer']])
 s0=dict(zip([fmap[t] for t in data['A']],data['tree_matching']))
 s=tuple(s0[t] for t in b.A)
 cert=b.recover(s,tuple(data['certificate']['P'][0]))
 assert check_cycle(b.G,cert['cycle'],cert['avoided_edge'])
 result[name]={'states':len(list(b.states())),'pairs':len(b.pairs()),'certificate':cert}
shared=json.loads((ROOT/'paper/figures/checked.json').read_text())
for name in ['octahedron','running']:
 d=shared[name];mod=d['model'];edges={tuple(sorted((u,v))) for f in mod['faces'] for u,v in zip(f,f[1:]+f[:1])}
 b=Instance(nx.Graph(sorted(edges)))
 fmap={i:next(j for j,f in enumerate(b.faces) if set(f)==set(face)) for i,face in enumerate(mod['faces'])}
 b=Instance(b.T,outer=fmap[mod['t0']]);inv={v:k for k,v in fmap.items()}
 def trans(s):
  sd=dict(zip([fmap[t] for t in mod['A']],s));return tuple(sd[t] for t in b.A)
 r,s=trans(d['r']),trans(d['s']); assert b.valid(r) and b.valid(s)
 # Reference delta may use the mirror embedding. Use the supplied oriented faces for paper J.
 black_sides={(u,v) for t in mod['A'] for u,v in zip(mod['faces'][t],mod['faces'][t][1:]+mod['faces'][t][:1])}
 def jj(r,s): return sum(1 if (u,v) in black_sides else -1 for u,v in zip(r,s))//3
 states=list(b.states());pairs=b.pairs(states)
 forest=s if name=='octahedron' else r
 cert=b.recover(forest,tuple(mod['e0']))
 cert['cycle']=[inv[f] for f in cert['cycle']]
 result[name+'_figure']={'A':mod['A'],'r':d['r'],'s':d['s'],'states':len(states),'pairs':len(pairs),'forest_pairs':sum(b.is_tree(s) for r,s in pairs),'minimum_cycles':min(len(b.dcycles(r,s)) for r,s in pairs),'J':jj(r,s),'certificate':cert}
 if name=='running':
  r2,s2=b.reverse_q((r,s),b.qcycles(s)[0]);assert s2==s and b.valid(r2)
  result[name+'_figure'].update(J_reversed=jj(r2,s2),r_reversed=[r2[b.A.index(fmap[t])] for t in mod['A']],Q_cycle=nx.cycle_basis(b.Q(s)))
  assert set(map(tuple,map(sorted,cert['P'])))==set(map(tuple,d['rec']['P']))
# Independently count the displayed disk by deleting its crossed dual edges.
  C=[1,2,3,9,10,11,6]; cut={tuple(sorted((u,v))) for u,v in zip(C,C[1:]+C[:1])}
  dual=b.G.copy();dual.remove_edges_from(b.dual_edges[e] for e in cut)
  inside=next(set(c) for c in nx.connected_components(dual) if b.outer not in c)
  Bs=len(inside&set(b.black));Ws=len(inside&set(b.white))
  vv=set().union(*(set(b.faces[f]) for f in inside));ii=len(vv-set(C))
  ell=sum(next(f for f in b.dual_edges[e] if f in b.black) in inside for e in cut)
  assert (Bs,Ws,ii,len(C),ell)==(5,6,3,7,2)
  for pp in pairs:
   for qc in b.qcycles(pp[1]):
    rr,ss=b.reverse_q(pp,qc)
    assert b.valid(rr) and ss==pp[1] and b.sign(rr,ss)==-b.sign(*pp)
    assert b.reverse_q((rr,ss),qc)==pp
  result[name+'_figure']['disk']={'B':Bs,'W':Ws,'I':ii,'h':len(C),'ell':ell}
  import sympy as sp
  b1,b2=sp.symbols('b1 b2')
  assert sp.expand(sum((-1)**(u+v)*(b1+u)*(b2+u+v) for u in [0,1] for v in [0,1]))==1
(OUT/'examples.json').write_text(json.dumps(result,indent=2))
for k,v in result.items(): print(k,{a:b for a,b in v.items() if a!='certificate'})
