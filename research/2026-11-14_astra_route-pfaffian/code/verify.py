"""Separate DFS cycle enumeration and replay of categorical four-cut census."""
import sys,json,pathlib,contextlib,time
sys.dont_write_bytecode=True
import networkx as nx
P=pathlib.Path(__file__).resolve().parents[1]; repo=P.parents[1]
r=json.loads((P/'data/results.json').read_text()); out=[]
for row in r['graphs']:
 g=nx.Graph(); g.add_edges_from(row['edges']); start=min(g); count=[0]; paths=set()
 def dfs(path,used):
  u=path[-1]
  if len(path)==len(g):
   if g.has_edge(u,start) and path[1]<path[-1]:
    count[0]+=1
    for i in range(len(path)):
     q=tuple(path[(i+j)%len(path)] for j in range(4)); paths.add(min(q,q[::-1]))
   return
  for v in g[u]:
   if v not in used: dfs(path+[v],used|{v})
 dfs([start],{start})
 assert count[0]==row['hamiltonian_cycles']; assert len(paths)==row['paths']
 brace=True
 es=list(g.edges)
 for i,(a,b) in enumerate(es):
  for c,d in es[i+1:]:
   if len({a,b,c,d})<4: continue
   h=g.copy(); h.remove_nodes_from([a,b,c,d])
   if len(nx.max_weight_matching(h,maxcardinality=True))*2!=len(h): brace=False
 out.append({'name':row['name'],'dfs_hamiltonian_cycles':count[0],'covered_P4':len(paths),'two_extendable':brace})
(P/'data/verification.json').write_text(json.dumps(out,indent=2)); print(out)
sys.path.insert(0,str(repo/'research/2026-11-14_fable_route-categorical/code'))
import cuts
with (P/'data/categorical_replay.txt').open('w') as f, contextlib.redirect_stdout(f):
 cuts.run_four(11,str(P/'data/categorical_four11.json'))
print((P/'data/categorical_replay.txt').read_text())
