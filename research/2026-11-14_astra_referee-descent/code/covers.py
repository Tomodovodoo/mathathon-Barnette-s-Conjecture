from check import *
def cover_pairs(A,R):
 X=sorted(set().union(*map(set,A))-set(R));caps={v:2 for v in X};opts=[list(it.combinations(sorted(set(f)-set(R)),2)) for f in A];selected=[None]*len(A);out=[]
 def rec(left):
  if not left:
   assert all(v==0 for v in caps.values());adj={v:[] for v in X}
   for i,(a,b) in enumerate(selected):adj[a].append((b,i));adj[b].append((a,i))
   seen=set();cs=[]
   for v in X:
    if v in seen:continue
    C=[];u=v;last=-1
    while u not in seen:
     seen.add(u);w,i=next(e for e in adj[u] if e[1]!=last);C.append((u,w,i));u=w;last=i
    cs.append(C)
   for bits in it.product((0,1),repeat=len(cs)):
    r=[None]*len(A);s=r.copy()
    for bit,C in zip(bits,cs):
     for a,b,i in C:r[i],s[i]=(b,a) if bit else (a,b)
    out.append((tuple(r),tuple(s)))
   return
  poss={i:[ab for ab in opts[i] if all(caps[v]>0 for v in ab)] for i in left}
  if any(not op for op in poss.values()):return
  availability={v:0 for v in X}
  for op in poss.values():
   for v in set().union(*map(set,op)):availability[v]+=1
  if any(caps[v]>availability[v] for v in X):return
  i=min(left,key=lambda i:len(poss[i]))
  for ab in poss[i]:
   selected[i]=ab
   for v in ab:caps[v]-=1
   rec(left-{i})
   for v in ab:caps[v]+=1
 rec(set(range(len(A))));return out
if __name__=='__main__':
 total=0
 for v in range(6,17):
  for line in subprocess.run([str(P),'-ba',str(v)],capture_output=True,check=True).stdout.decode().splitlines():
   rot=parse(line);fs,col=faces(rot)
   for ri,R in enumerate(fs):
    A=[f for i,f in enumerate(fs) if col[i]==col[ri] and i!=ri];ss=states(A,R);expected={(r,s) for s in ss for r in states(A,R,s)};got=set(cover_pairs(A,R));assert got==expected;total+=len(got)
 print(total);(BASE/'code/covers_validation.json').write_text(json.dumps(dict(Vmax=16,pairs=total)))
