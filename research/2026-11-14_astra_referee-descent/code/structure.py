from check import *
from induction import contract
from families import graph
import networkx as nx

def region(rot,C,R):
 fs,col=faces(rot);ri=next(i for i,f in enumerate(fs) if set(f)==set(R));owner={}
 for i,f in enumerate(fs):
  for a,b in zip(f,f[1:]+f[:1]):owner.setdefault(frozenset((a,b)),[]).append(i)
 cut={frozenset(e) for e in zip(C,C[1:]+C[:1])};seen={ri};todo=[ri]
 for i in todo:
  f=fs[i]
  for a,b in zip(f,f[1:]+f[:1]):
   e=frozenset((a,b))
   if e in cut:continue
   for j in owner[e]:
    if j not in seen:seen.add(j);todo.append(j)
 inside=set(range(len(fs)))-seen
 return set().union(*(set(fs[i]) for i in inside))-set(C),sum(any(i in inside and col[i]!=col[ri] for i in owner[e]) for e in cut)

def structure(rot):
 fs,col=faces(rot);g=graph(rot);facial={frozenset(f) for f in fs};tri={frozenset((u,v,w)) for u,v in g.edges for w in set(g[u])&set(g[v])}
 if tri!=facial:return None
 out=dict(roots=0,merges=0,fail=0,G_fail=0);rootdetails=[]
 for ri,R in enumerate(fs):
  A=[f for i,f in enumerate(fs) if col[i]==col[ri] and i!=ri];valid={};witness=[]
  for x,ns in enumerate(rot):
   if x in R or len(ns)!=4:continue
   valid[x]=[]
   for p,q in ((ns[0],ns[2]),(ns[1],ns[3])):
    common=(set(rot[p])&set(rot[q]))-set(ns)-{x};simple=not common
    B,root,_=contract(A,R,x,p,q);ss=states(B,root);pair=any(all(a!=b for a,b in zip(r,s)) for r in ss for s in ss);valid[x].append(simple and pair)
    bad5=False
    for y in rot[p]:
     for z in set(rot[y])&set(rot[q]):
      C=(x,p,y,z,q)
      if len(set(C))!=5 or any(g.has_edge(C[i],C[j]) for i in range(5) for j in range(i+1,5) if (j-i) not in (1,4)):continue
      inside,w=region(rot,C,R)
      if w==1:bad5=True;witness.append((C,inside))
    out['merges']+=1;out['fail']+=(not(simple and pair))!=(bool(common) or bad5)
  out['roots']+=1;out['G_fail']+=len(rot)>6 and not any(any(v) for v in valid.values());rootdetails.append((R,valid,witness))
 assert not out['fail'] and not out['G_fail']
 return out,rootdetails

def deficiency(rot):
 fs,col=faces(rot);n=len(rot);g=graph(rot);actual={frozenset(f):i for i,f in enumerate(fs)};count=0
 for mask in range(1<<n):
  U={i for i in range(n) if mask>>i&1}
  if len(U)<3 or not any(set(f)<=U for f in fs) or not nx.is_connected(g.subgraph(U)):continue
  induced={u:[v for v in rot[u] if v in U] for u in U};seen=set();regions=[]
  for u in U:
   for v in induced[u]:
    if (u,v) in seen:continue
    e=(u,v);walk=[]
    while e not in seen:
     seen.add(e);walk.append(e);a,b=e;ns=induced[b];e=b,ns[(ns.index(a)+1)%len(ns)]
    # distinguish the two sides of a triangle by oriented actual faces
    verts=tuple(a for a,b in walk)
    actualside=any(len(verts)==3 and any(verts==f[j:]+f[:j] for j in range(3)) for f in fs)
    if not actualside:regions.append(walk)
  own={(a,b):i for i,f in enumerate(fs) for a,b in zip(f,f[1:]+f[:1])}
  for black in (0,1):
   if not any(set(f)<=U and col[i]==black for i,f in enumerate(fs)):continue
   S=set(range(n))-U;lhs=sum(min(2,len(set(f)&S)) for i,f in enumerate(fs) if col[i]==black)-2*len(S)
   rhs=sum(len(w)+sum(col[own[e]]!=black for e in w)-6 for w in regions)
   assert 3*lhs==rhs,(rot,U,lhs,rhs)
   count+=1
 return count
if __name__=='__main__':
 mode=sys.argv[1];lo,hi=map(int,sys.argv[2:]);out=[]
 for v in range(lo,hi+1):
  total=dict(V=v,graphs=0,checks=0,merges=0,roots=0);start=time.time()
  for line in subprocess.run([str(P),'-ba',str(v)],capture_output=True,check=True).stdout.decode().splitlines():
   rot=parse(line);total['graphs']+=1
   if mode=='deficiency':total['checks']+=deficiency(rot)
   else:
    result=structure(rot)
    if result:
     for k in ('merges','roots'):total[k]+=result[0][k]
  total['seconds']=time.time()-start;out.append(total);print(total,flush=True);(BASE/f'code/{mode}_{lo}_{hi}.json').write_text(json.dumps(out,indent=2))
