from pathlib import Path
import sys,json,re,math
import networkx as nx
root=Path('research/2026-11-14_astra_final-proofread')
sys.path.insert(0,str(Path('paper/figures').resolve()))
from model import Model
j=json.loads(Path('paper/figures/running.json').read_text()); m=Model(j['faces'],j['t0'],j['e0'])
ss=m.states(); pairs=m.pairs(ss)
a=(1,3,7,2,9,11,6,12,8,10); b=(6,2,8,1,3,10,11,7,12,9)
assert m.is_state(a) and m.is_state(b)
dist=nx.single_source_shortest_path_length(m.G,m.t0); weights={}; paths={}
for y in m.white:
 p=[y]
 while p[-1]!=m.t0: p.append(min(v for v in m.G[p[-1]] if dist[v]==dist[p[-1]]-1))
 paths[y]=p
 for prev,t,nxt in zip(p,p[1:],p[2:]):
  if t not in m.A: continue
  ent=set(m.F[prev])&set(m.F[t]); out=set(m.F[t])&set(m.F[nxt]); v,=ent&out; av,=ent-{v}; bv,=out-{v}; f=m.F[t]; i=f.index(v)
  weights[t,v]=weights.get((t,v),0)+(1 if f[(i+1)%3]==av else -1)
rows=[]
for r,s in pairs:
 cycles=list(nx.simple_cycles(nx.DiGraph(m.D(r,s)))); disks=sorted((m.disk(c) for c in cycles),key=lambda d:-d['h'])
 rows.append(dict(r=r,s=s,L=[d['W'] for d in disks],ccw=[d['ccw'] for d in disks],sign=math.prod(m.delta(u,v) for u,v in zip(r,s)),weight=sum(weights.get((t,v),0) for t,v in zip(m.A,s)),good=m.Q_is_forest(s)))
rows.sort(key=lambda r:(-r['L'][0],r['ccw']))
# Independently enumerate primal perfect matchings, then connected complements.
def matchings(left,edges):
 if not left: yield edges; return
 u=min(left)
 for v in m.G[u]:
  if v in left: yield from matchings(left-{u,v},edges+[(u,v)])
hc=0
for matching in matchings(set(m.G),[]):
 if tuple(sorted(m.dual[m.e0])) not in [tuple(sorted(e)) for e in matching]: continue
 g=m.G.copy(); g.remove_edges_from(matching)
 hc+=nx.is_connected(g)
out={'command':'python research/2026-11-14_astra_final-proofread/check.py','vertices':len(m.V),'edges':len(m.E),'faces':len(m.F),'black':len(m.black),'white':len(m.white),'states':len(ss),'pairs':len(pairs),'good_states':sum(m.Q_is_forest(s) and all(len(set(c) & set(m.roots))==1 for c in nx.connected_components(m.Q_graph(s))) for s in ss),'hamiltonian_avoiding_e':hc,'Q_beta_components':[sorted(c) for c in nx.connected_components(m.Q_graph(b))],'P_beta':m.recover(b)['parts'],'disk':m.disk([1,2,3,9,10,11,6]),'rows':rows,'moments':[sum(r['sign']*r['weight']**k for r in rows) for k in range(3)]}
assert (len(ss),len(pairs),out['good_states'],hc)==(12,8,6,6)
assert out['moments']==[0,0,18]
assert [r['weight'] for r in rows]==[-4,-3,2,3,-2,-1,1,2]
(root/'checks.json').write_text(json.dumps(out,indent=2))
tex=(root/'source.tex').read_text(); labels=re.findall(r'\\label\{([^}]+)\}',tex); refs=re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',tex)
assert set(refs)<=set(labels) and len(labels)==len(set(labels))
(root/'crossrefs.txt').write_text('\n'.join(f'{i}: {line}' for i,line in enumerate(tex.splitlines(),1) if re.search(r'\\(?:eqref|ref|label|cite)\b',line)))
print({k:v for k,v in out.items() if k not in ('rows','disk')}); print('Reference occurrences',len(refs),'labels',len(labels))

