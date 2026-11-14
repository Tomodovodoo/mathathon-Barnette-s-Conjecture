from final_checks import *
import numpy as np
# Independent implementation of a seeded loop-erased random-walk tree sampler.
rng=np.random.default_rng(2026);nodes=list(H);hist=Counter();first=None
want={v:H.degree(v)-(0 if (v[0]=='t' and v[1]==j['t0']) or (v[0]=='v' and v[1] in roots) else 1) for v in H}
for _ in range(4000):
 done={nodes[0]};par={}
 for start in nodes:
  cur=start
  while cur not in done:
   ns=list(H[cur]);par[cur]=ns[int(rng.integers(len(ns)))];cur=par[cur]
  cur=start
  while cur not in done:done.add(cur);cur=par[cur]
 es=[(v,par[v]) for v in nodes[1:]];deg=Counter(v for e in es for v in e);wrong=sum(deg[v]!=want[v] for v in nodes);hist[wrong]+=1
 if first is None and wrong>=6:first=es
ck('4000-tree seed histogram',{str(k):v for k,v in sorted(hist.items())},C['random']['wrong_points_histogram'])
# Read the backwards state directly from each prism induced-tree partition.
c=C['produced'];f,v,e,t,l,g,b,a,xx,w=setup(c['faces'],c['t0']);rr=set(f[c['t0']]);edge0=tuple(c['e0']);res=[]
for bits in range(1,1<<(len(v)-1)):
 U={v[i] for i in range(len(v)-1) if bits>>i&1};Z=set(v)-U
 if not U or not nx.is_tree(t.subgraph(U)) or not nx.is_tree(t.subgraph(Z)):continue
 if (edge0[0] in U)!=(edge0[1] in U):continue
 selected=[edge for edge in e if (edge[0] in U)==(edge[1] in U)];forest=nx.Graph();forest.add_nodes_from(v);forest.add_edges_from(ed for ed in selected if ed!=edge0);state=[]
 assert nx.is_forest(forest)
 for ti in a:
  ed=next(ed for ed in selected if ed!=edge0 and set(ed)<=set(f[ti]));root=next(r for r in rr if nx.has_path(forest,r,ed[0]));dist=nx.single_source_shortest_path_length(forest,root);state.append(max(ed,key=dist.get))
 q=qgraph(state,f,a,v);rootsep=nx.is_forest(q) and all(len(set(cc)&rr)==1 for cc in nx.connected_components(q));res.append(dict(state=state,good=rootsep,acyclic=nx.is_forest(q),root_paths=[nx.shortest_path(q,u,z) for u,z in it.combinations(rr,2) if nx.has_path(q,u,z)]))
ck('four backward prism states',len(res),4);ck('backward prism good count',sum(z['good'] for z in res),2);ck('backward prism ordinary forests',sum(z['acyclic'] for z in res),4)
(O/'closing-checks.json').write_text(json.dumps(dict(checks=checks,backwards=res,sample_histogram=hist),indent=2,default=str));print('checks',len(checks),'failed',sum(not c['ok'] for c in checks))
