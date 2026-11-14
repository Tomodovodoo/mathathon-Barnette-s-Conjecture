import itertools as it, json, subprocess, sys, time, pathlib
BASE=pathlib.Path(__file__).resolve().parents[1]
REPO=BASE.parents[1]
P=REPO/'workings/barnette_lab/vendor/plantri.exe'
def parse(line):
 n, rest=line.strip().split(' ',1)
 if ',' in rest: return [[ord(c)-97 for c in s] for s in rest.split(',')]
 a=list(map(int,rest.split())); rot=[]
 for i in range(int(n)):
  d=a.pop(0); rot.append(a[:d]); del a[:d]
 return rot
def faces(rot):
 seen=set(); fs=[]
 for u,ns in enumerate(rot):
  for v in ns:
   if (u,v) in seen: continue
   f=[]; edge=(u,v)
   while edge not in seen:
    seen.add(edge); a,b=edge; f.append(a); ns=rot[b]; edge=(b,ns[(ns.index(a)+1)%len(ns)])
   assert len(f)==3
   fs.append(tuple(f))
 owners={}
 for i,f in enumerate(fs):
  for a,b in zip(f,f[1:]+f[:1]): owners.setdefault(tuple(sorted((a,b))),[]).append(i)
 adj=[[] for f in fs]
 for ids in owners.values():
  assert len(ids)==2
  a,b=ids; adj[a].append(b); adj[b].append(a)
 color={0:0}; todo=[0]
 for a in todo:
  for b in adj[a]:
   if b not in color: color[b]=1-color[a]; todo.append(b)
   assert color[b]!=color[a]
 return fs,color
def states(A,R):
 opts=[set(f)-set(R) for f in A]; s=[None]*len(A); ans=[]
 def rec(left,used):
  if not left: ans.append(tuple(s)); return
  i=min(left,key=lambda i:len(opts[i]-used))
  for v in opts[i]-used: s[i]=v; rec(left-{i},used|{v})
 rec(set(range(len(A))),set()); return ans
def cycles(f):
 seen=set(); out=[]
 for x in f:
  if x in seen: continue
  path=[]; loc={}
  while x in f and x not in seen and x not in loc:
   loc[x]=len(path); path.append(x); x=f[x]
  if x in loc: out.append(tuple(path[loc[x]:]))
  seen.update(path)
 return out
def info(A,p):
 r,s=p; u=tuple(next(v for v in f if v!=a and v!=b) for f,a,b in zip(A,r,s))
 return u,cycles(dict(zip(r,u))),cycles(dict(zip(r,s)))
def moves(A,p):
 r,s=p; u,Q,D=info(A,p)
 for C in D:
  inds=[i for i,v in enumerate(r) if v in C]; rr=list(r); ss=list(s)
  for i in inds: rr[i],ss[i]=ss[i],rr[i]
  yield (tuple(rr),tuple(ss))
 for C in Q:
  rr=tuple(u[i] if v in C else v for i,v in enumerate(r)); yield rr,s

def check(A,R):
 ss=states(A,R); pp=[(r,s) for r in ss for s in ss if all(a!=b for a,b in zip(r,s))]
 ks={p:len(info(A,p)[1]) for p in pp}; adj={p:list(moves(A,p)) for p in pp}
 good=[p for p in pp if ks[p]==0]; reached=set(good); queue=list(good)
 for p in queue:
  for q in adj[p]:
   assert q in ks and p in adj[q]
   if ks[q]>=ks[p] and q not in reached: reached.add(q); queue.append(q)
 sinks=sum(ks[p]>0 and all(ks[q]>=ks[p] for q in adj[p]) for p in pp)
 assert len(reached)==len(pp), 'C3 failure'
 return dict(states=len(ss),pairs=len(pp),good=len(good),sinks=sinks,paired=bool(pp))
def census(lo,hi):
 out=[]
 for v in range(lo,hi+1):
  start=time.time(); raw=subprocess.run([str(P),'-ba',str(v)],capture_output=True,check=True).stdout.decode()
  total=dict(V=v,graphs=0,roots=0,states=0,pairs=0,good=0,sinks=0,paired=0)
  for line in raw.splitlines():
   rot=parse(line); fs,col=faces(rot); total['graphs']+=1
   for j,R in enumerate(fs):
    A=[f for i,f in enumerate(fs) if col[i]==col[j] and i!=j]
    res=check(A,R); total['roots']+=1
    for k,val in res.items(): total[k]+=val
  total['seconds']=time.time()-start; out.append(total); print(total,flush=True)
  (BASE/f'code/census_{lo}_{hi}.json').write_text(json.dumps(out,indent=2))
if __name__=='__main__': census(*map(int,sys.argv[1:]))
