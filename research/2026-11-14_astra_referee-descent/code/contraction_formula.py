from check import *
from induction import contract
out=[]
def f(A,S):return sum(min(2,len(set(t)&S)) for t in A)-2*len(S)
for v in range(6,15):
 checks=0;start=time.time()
 for line in subprocess.run([str(P),'-ba',str(v)],capture_output=True,check=True).stdout.decode().splitlines():
  rot=parse(line);fs,col=faces(rot)
  for ri,R in enumerate(fs):
   A=[t for i,t in enumerate(fs) if col[i]==col[ri] and i!=ri]
   for x,ns in enumerate(rot):
    if x in R or len(ns)!=4:continue
    for p,q in ((ns[0],ns[2]),(ns[1],ns[3])):
     B,RR,_=contract(A,R,x,p,q);vs=sorted(set().union(*map(set,B))-set(RR));a,b=[y for y in ns if y not in (p,q)]
     for mask in range(1<<len(vs)):
      S={y for j,y in enumerate(vs) if mask>>j&1};rhs=f(A,(S-{p})|{p,q,x}) if p in S else f(A,S)-(a in S)-(b in S)
      assert f(B,S)==rhs;checks+=1
 row=dict(V=v,checks=checks,seconds=time.time()-start);out.append(row);print(row,flush=True);(BASE/'code/contraction_formula.json').write_text(json.dumps(out,indent=2))
