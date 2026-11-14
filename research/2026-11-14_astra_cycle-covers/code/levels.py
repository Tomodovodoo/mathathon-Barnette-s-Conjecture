from explore import *
import subprocess,time
from itertools import combinations
p=Path(__file__).resolve().parents[1];root=p.parents[1]
checked=0;out=None
for v in range(6,19):
 raw=subprocess.check_output([str(root/'workings/barnette_lab/vendor/plantri.exe'),'-b','-c4',str(v)],stderr=subprocess.DEVNULL);raw=raw.replace(bytes([13,10]),bytes([10]));pos=15;ng=0
 while pos<len(raw):
  n=raw[pos];pos+=1;g=nx.Graph();g.add_nodes_from(range(n))
  for a in range(n):
   while raw[pos]:g.add_edge(a,raw[pos]-1);pos+=1
   pos+=1
  b=Instance(g);ng+=1
  for f in range(len(b.faces)):
   I=Instance(g,f);us=list(covers(I));cnt=[len(describe(I,u)) for u in us];checked+=1
   if len(us)<2:continue
   fl=nx.Graph();fl.add_nodes_from(range(len(us)))
   for i,j in combinations(range(len(us)),2):
    d=nx.Graph()
    for t,x,y in zip(I.A,us[i],us[j]):
     if x!=y:d.add_edges_from([(('t',t),('v',x)),(('t',t),('v',y))])
    if nx.is_connected(d) and all(de==2 for _,de in d.degree()):fl.add_edge(i,j)
   for c in set(cnt):
    nodes=[i for i,k in enumerate(cnt) if k==c]
    if len(nodes)>1 and not nx.is_connected(fl.subgraph(nodes)):
     out={'V':v,'graph_index':ng,'root':I.faces[f],'edges':list(g.edges()),'A':[I.faces[t] for t in I.A],'u':us,'cycle_counts':cnt,'flip_edges':list(fl.edges()),'disconnected_level':c,'checked':checked};break
   if out:break
  if out:break
 if out:break
 print('completed',v,checked,flush=True)
(p/'data/levels.json').write_text(json.dumps(out or {'checked':checked},indent=2));print(out)


