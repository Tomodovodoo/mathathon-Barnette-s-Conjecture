from check import *
import re,collections
exec((BASE/'code/witnesses.py').read_text().split('out=[]')[0].split('import re')[0]) if False else None

def geometry(rot,R):
 fs,col=faces(rot); ri=next(i for i,f in enumerate(fs) if set(f)==set(R)); owner={}
 for i,f in enumerate(fs):
  for a,b in zip(f,f[1:]+f[:1]):owner[a,b]=i
 def area(C):
  edges=list(zip(C,C[1:]+C[:1])); cut={frozenset(e) for e in edges}; seed=owner[edges[0]]; seen={seed};todo=[seed]
  for i in todo:
   f=fs[i]
   for a,b in zip(f,f[1:]+f[:1]):
    if frozenset((a,b)) in cut:continue
    j=owner[b,a]
    if j not in seen:seen.add(j);todo.append(j)
  if ri in seen:return -sum(col[i]!=col[ri] for i in range(len(fs)) if i not in seen)
  return sum(col[i]!=col[ri] for i in seen)
 return area

def component(A,p,area,cap=100000):
 heights={p:(0,0)};todo=[p]; adj={}; values={}
 for z in todo:
  u,Q,D=info(A,z); om,psi=heights[z]; nxt=list(moves(A,z));adj[z]=nxt
  values[z]=(len(Q),len(D),sum(map(len,Q)),sum(abs(area(C)) for C in Q),sum(abs(area(C)) for C in D),om,psi)
  for j,w in enumerate(nxt):
   h=(om-area(D[j]),psi) if j<len(D) else (om,psi-area(Q[j-len(D)]))
   if w in heights:assert heights[w]==h
   else:
    heights[w]=h;todo.append(w)
    if len(todo)>cap:raise RuntimeError('cap')
 return adj,values

def potential(name,v):
 k,c,vq,wq,wd,om,psi=v
 # Our facial walk uses the opposite orientation to the report labels.
 om,psi=-om,-psi
 expr=name.replace('+psi','psi').replace('+om','om')
 return eval(expr,{'__builtins__':{}},dict(k=k,c=c,vq=vq,wq=wq,wd=wd,om=om,psi=psi))

def run(line):
 fields=line.split(' | ');head=fields[0];rot=parse(fields[1]);R=tuple(map(int,re.search(r't0=(\d+,\d+,\d+)',head)[1].split(',')))
 fs,col=faces(rot);ri=next(i for i,f in enumerate(fs) if set(f)==set(R));A=[f for i,f in enumerate(fs) if col[i]==col[ri] and i!=ri]
 ab=[tuple(map(int,s.split('>'))) for s in fields[-1][5:].split()]
 if len(fields)==4:A=[tuple(map(int,s.split(','))) for s in fields[2][6:].split()]
 else:A=[next(f for f in A if a in f and b in f) for a,b in ab]
 p=tuple(zip(*ab));adj,vals=component(A,p,geometry(rot,R));name=re.search(r'pot=([^ ]+)',head)[1];cost={z:potential(name,v) for z,v in vals.items()}
 L=2 if 'TRAP2' in head else 1
 near={z:set(ws) for z,ws in adj.items()}
 if L==2:
  near={z:set(ws).union(*(set(adj[w]) for w in ws)) for z,ws in adj.items()}
 reached={p};todo=[p]
 for z in todo:
  for w in near[z]:
   if w not in reached and cost[w]<=cost[z]:reached.add(w);todo.append(w)
 return dict(header=head,component=len(adj),reachable=len(reached),good_reachable=sum(vals[z][0]==0 for z in reached),strict_lower=sum(cost[w]<cost[p] for w in near[p]))
if __name__=='__main__':
 out=[]
 for line in (REPO/'research/2026-11-14_fable_descent/data/witnesses.txt').read_text().splitlines():
  if 'pot=' not in line or 'SIGNEDRHO' in line or ' | pair ' not in line:continue
  r=run(line);out.append(r);print(r,flush=True)
 (BASE/'code/potentials.json').write_text(json.dumps(out,indent=2))
