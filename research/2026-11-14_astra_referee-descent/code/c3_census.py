from check import *
from covers import cover_pairs
out=[]
lo,hi=map(int,sys.argv[1:])
for v in range(lo,hi+1):
 row=dict(V=v,graphs=0,roots=0,paired_roots=0,pairs=0,good=0,strict_sinks=0,radius_over_two=0);start=time.time()
 for line in subprocess.run([str(P),'-ba',str(v)],capture_output=True,check=True).stdout.decode().splitlines():
  rot=parse(line);fs,col=faces(rot);row['graphs']+=1
  for ri,R in enumerate(fs):
   A=[f for i,f in enumerate(fs) if col[i]==col[ri] and i!=ri];pp=cover_pairs(A,R);row['roots']+=1;row['paired_roots']+=bool(pp);row['pairs']+=len(pp);qs={p:len(info(A,p)[1]) for p in pp};adj={p:list(moves(A,p)) for p in pp};seen={p for p in pp if qs[p]==0};queue=list(seen);row['good']+=len(seen)
   for p in queue:
    for z in adj[p]:
     if z not in seen and qs[z]>=qs[p]:seen.add(z);queue.append(z)
   assert len(seen)==len(pp)
   for p in pp:
    if qs[p] and all(qs[z]>=qs[p] for z in adj[p]):
     row['strict_sinks']+=1
     row['radius_over_two']+=not any(qs[w]<qs[p] for z in adj[p] for w in adj[z])
 row['seconds']=time.time()-start;out.append(row);print(row,flush=True);(BASE/f'code/c3_{lo}_{hi}.json').write_text(json.dumps(out,indent=2))
