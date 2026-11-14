from random_sample import split_random
from families import *
from covers import cover_pairs

def separator_free(rot):
 fs,_=faces(rot);facial={frozenset(f) for f in fs};ns=list(map(set,rot))
 return all(frozenset((a,b,c)) in facial for a in range(len(rot)) for b in ns[a] if b>a for c in ns[a]&ns[b] if c>b)

if __name__=='__main__':
 rng=random.Random(714993);out=[];start=time.time()
 for v in (26,30,34,40):
  for sample in range(5):
   rot=tube(4,0);attempts=0
   while len(rot)<v:
    trial=split_random(rot,rng);attempts+=1
    if separator_free(trial):rot=trial
    assert attempts<10000
   fs,col=faces(rot);results=[]
   for ri in rng.sample(range(len(fs)),8):
    R=fs[ri];A=[f for i,f in enumerate(fs) if col[i]==col[ri] and i!=ri];pp=cover_pairs(A,R)
    assert pp
    qs={p:len(info(A,p)[1]) for p in pp};adj={p:list(moves(A,p)) for p in pp};seen={p for p in pp if qs[p]==0};queue=list(seen)
    for p in queue:
     for z in adj[p]:
      assert z in qs and p in adj[z]
      if z not in seen and qs[z]>=qs[p]:seen.add(z);queue.append(z)
    assert len(seen)==len(pp),'C3 failure'
    sinks=[p for p in pp if qs[p] and all(qs[z]>=qs[p] for z in adj[p])]
    radius_over_two=sum(not any(qs[w]<qs[p] for z in adj[p] for w in adj[z]) for p in sinks)
    results.append(dict(root=R,pairs=len(pp),good=sum(q==0 for q in qs.values()),strict_sinks=len(sinks),radius_over_two=radius_over_two))
   row=dict(V=v,sample=sample,attempts=attempts,rotation=rot,roots=results);out.append(row)
   print(v,sample,'pairs',sum(r['pairs'] for r in results),'elapsed',round(time.time()-start,2),flush=True)
   (BASE/'code/random_separator_free.json').write_text(json.dumps(out,indent=2))
   if time.time()-start>480:raise SystemExit('saved partial sample at time cap')
