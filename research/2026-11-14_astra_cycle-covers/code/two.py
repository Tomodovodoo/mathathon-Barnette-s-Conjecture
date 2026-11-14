from explore import *
from collections import defaultdict
import subprocess
p=Path(__file__).resolve().parents[1];root=p.parents[1];rows=[]
for v in range(6,15):
 raw=subprocess.check_output([str(root/'workings/barnette_lab/vendor/plantri.exe'),'-b','-c4',str(v)],stderr=subprocess.DEVNULL).replace(b'\r\n',b'\n');pos=15
 while pos<len(raw):
  n=raw[pos];pos+=1;g=nx.Graph();g.add_nodes_from(range(n))
  for a in range(n):
   while raw[pos]:g.add_edge(a,raw[pos]-1);pos+=1
   pos+=1
  b=Instance(g)
  for f in range(len(b.faces)):
   I=Instance(g,f);us=list(covers(I))
   if len(us)!=2:continue
   ps=I.pairs();groups=defaultdict(set)
   for r,s in ps:
    u=tuple(next(v for v in I.faces[t] if v not in (a,b)) for t,a,b in zip(I.A,r,s));groups[u].add(s)
   assert set(groups)==set(us)
   def cycles(u):
    d=nx.Graph()
    for t,x in zip(I.A,u):d.add_edge(*(set(I.faces[t])-{x}))
    return {frozenset(tuple(sorted(e)) for e in d.subgraph(vs).edges()) for vs in nx.connected_components(d)}
   cs=[cycles(u) for u in us];c1,c2=map(len,cs);j=len(cs[0]&cs[1]);a=len(groups[us[0]]&groups[us[1]]);tm=sum(I.is_tree(s) for s in I.states())
   assert a in (0,2**j);assert tm==2**c1+2**c2-2*a;assert tm>2**min(c1,c2)
   rows.append({'V':v,'cycles':[c1,c2],'common_cycles':j,'shared_states':a,'TM':tm})
(p/'data/two-covers.json').write_text(json.dumps(rows,indent=2));print('two-cover rooted instances checked:',len(rows))
