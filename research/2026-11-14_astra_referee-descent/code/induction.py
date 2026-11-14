from check import *
def good(A,R,s):
 vertices=set(R).union(*map(set,A)); parent={v:v for v in vertices}
 def find(v):
  while parent[v]!=v: v=parent[v]
  return v
 for f,v in zip(A,s):
  a,b=[w for w in f if w!=v]; a,b=find(a),find(b)
  if a==b:return False
  parent[a]=b
 return len({find(v) for v in R})==3

def contract(A,R,x,p,q):
 conv=lambda v:p if v==q else v
 inds=[i for i,f in enumerate(A) if x not in f]
 B=[tuple(conv(v) for v in A[i]) for i in inds]; root=tuple(conv(v) for v in R)
 return B,root,inds

def classify(A,R,x,p,q,s):
 B,root,inds=contract(A,R,x,p,q)
 lift=[None]*len(A)
 for i,v in zip(inds,s):
  lift[i]= q if v==p and p not in A[i] else v
 used=set(lift)-{None}; local=[i for i in range(len(A)) if i not in inds]
 poss=[]
 for choices in it.product(*[set(A[i])-set(R)-used for i in local]):
  if len(set(choices))!=len(choices):continue
  z=lift.copy()
  for i,v in zip(local,choices):z[i]=v
  poss.append(tuple(z))
 assert len(poss)==1
 z=poss[0]
 if good(A,R,z):return 'L',z,None
 # A failing lift has exactly one three-face rotation using the two local faces.
 rotations=[]
 for j in inds:
  loc=local+[j]
  for shift in (1,2):
   zz=list(z)
   for k,i in enumerate(loc):zz[i]=z[loc[(k+shift)%3]]
   if all(zz[i] in A[i] for i in loc) and zz!=list(z):rotations.append(tuple(zz))
 assert len(rotations)==1,(x,p,q,z,rotations)
 zz=rotations[0]
 return ('R' if good(A,R,zz) else 'E'),z,zz

def audit(rot):
 fs,col=faces(rot); counts=dict(roots=0,good=0,contractions=0,exceptions=0,corner_fail=0,half_fail=0,bijection_fail=0,inequality_fail=0)
 for ri,R in enumerate(fs):
  A=[f for i,f in enumerate(fs) if col[i]==col[ri] and i!=ri]; ss=states(A,R); gs=[s for s in ss if good(A,R,s)]; counts['roots']+=1;counts['good']+=len(gs)
  if gs:
   counts['corner_fail']+=sum(len({s[i] for s in gs})<2 for i in range(len(A)))
  for x,ns in enumerate(rot):
   if x in R or len(ns)!=4:continue
   data=[]
   for p,q in ((ns[0],ns[2]),(ns[1],ns[3])):
    B,root,inds=contract(A,R,x,p,q); bs=states(B,root); bg=[s for s in bs if good(B,root,s)]
    classes=[classify(A,R,x,p,q,s) for s in bg]
    exc={z for c,z,zz in classes if c=='E'}; images={zz for c,z,zz in classes if c=='E'}
    counts['contractions']+=1;counts['exceptions']+=len(exc);counts['half_fail']+=2*len(exc)>len(bg)
    data.append((len(bg),exc,images))
   l,m=data
   counts['bijection_fail']+=l[2]!=m[1] or m[2]!=l[1]
   counts['inequality_fail']+=len(gs)<l[0]+m[0]-len(l[1])-len(m[1])
 return counts
if __name__=='__main__':
 lo,hi=map(int,sys.argv[1:]); out=[]
 for v in range(lo,hi+1):
  start=time.time(); raw=subprocess.run([str(P),'-ba',str(v)],capture_output=True,check=True).stdout.decode(); total={}
  for line in raw.splitlines():
   for k,val in audit(parse(line)).items():total[k]=total.get(k,0)+val
  total.update(V=v,seconds=time.time()-start);out.append(total);print(total,flush=True)
  (BASE/f'code/induction_{lo}_{hi}.json').write_text(json.dumps(out,indent=2))
