from pathlib import Path
import sys,json,networkx as nx
p=Path(__file__).resolve().parents[1]; root=p.parents[1];sys.path.insert(0,str(root/'workings/barnette_lab'))
from barnette_lab.core import Instance

def family(m):
 g=nx.Graph(); A=0; B=1
 x=lambda i:2+3*(i%m); y=lambda i:3+3*(i%m); z=lambda i:4+3*(i%m)
 for i in range(m):
  for a,b in [(A,x(i)),(A,y(i)),(x(i),y(i)),(x(i),y(i-1)),(B,y(i)),(B,z(i)),(z(i),y(i)),(z(i),y(i-1)),(z(i),x(i))]:g.add_edge(a,b)
 probe=Instance(g); r={A,x(0),y(0)}
 return Instance(g,next(i for i,f in enumerate(probe.faces) if set(f)==r))

def covers(I):
 # Enumerate deleted corners by exact degree constraints, not state pairs.
 opts=[[(v,tuple(set(I.faces[t])-{v})) for v in I.faces[t] if not (set(I.faces[t])-{v})&I.R] for t in I.A]
 order=sorted(range(I.n),key=lambda i:len(opts[i])); degree={x:0 for x in I.X};u=[None]*I.n
 def go(k):
  if k==I.n:
   if all(v==2 for v in degree.values()):yield tuple(u)
   return
  j=order[k]
  for v,(a,b) in opts[j]:
   if degree[a]==2 or degree[b]==2:continue
   degree[a]+=1;degree[b]+=1;u[j]=v
   yield from go(k+1)
   degree[a]-=1;degree[b]-=1
 yield from go(0)

def describe(I,u):
 d=nx.Graph();d.add_nodes_from(I.X)
 for t,v in zip(I.A,u):d.add_edge(*(set(I.faces[t])-{v}))
 S=[I.dual_edges[tuple(sorted(e))] for e in d.edges()];rem=I.G.copy();rem.remove_edges_from(S)
 assert nx.number_connected_components(rem)==nx.number_connected_components(d)+1
 return sorted([sorted(c) for c in nx.connected_components(d)])
if __name__=='__main__':
 rows=[]
 for m in range(3,11):
  I=family(m);us=list(covers(I));cs=[describe(I,u) for u in us]
  triangles=sum(1 for a in I.T for b in I.T[a] for c in I.T[b] if a<b<c and I.T.has_edge(a,c))
  row={'m':m,'V':len(I.T),'covers':len(us),'counts':[len(c) for c in cs],'cycles':cs,'separating_triangles':triangles-len(I.faces),'A':[I.faces[t] for t in I.A],'u':us}
  rows.append(row);print(m,len(us),[len(c) for c in cs],cs[0],flush=True)
 (p/'data/family.json').write_text(json.dumps(rows,indent=2))
