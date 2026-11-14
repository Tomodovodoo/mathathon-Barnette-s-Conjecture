from check import *
from covers import cover_pairs
from potentials import component,geometry,potential
out=[];names=['(k,'+a+'om,'+b+'psi)' for a in ('+','-') for b in ('+','-')]+['(k,'+a+'psi,'+b+'om)' for a in ('+','-') for b in ('+','-')]
for v in range(6,18):
 counts={name:0 for name in names};pairs=good=roots=0;start=time.time()
 for line in subprocess.run([str(P),'-ba',str(v)],capture_output=True,check=True).stdout.decode().splitlines():
  rot=parse(line);fs,col=faces(rot)
  for ri,R in enumerate(fs):
   A=[f for i,f in enumerate(fs) if col[i]==col[ri] and i!=ri];pp=cover_pairs(A,R);roots+=bool(pp);pairs+=len(pp);bad={p for p in pp if info(A,p)[1]};good+=len(pp)-len(bad)
   while bad:
    ad,vals=component(A,next(iter(bad)),geometry(rot,R));bad.difference_update(ad)
    for name in names:
     costs={p:potential(name,val) for p,val in vals.items()}
     counts[name]+=sum(val[0]>0 and all(costs[w]>=costs[p] for w in ad[p]) for p,val in vals.items())
 row=dict(V=v,pairs=pairs,good=good,paired_roots=roots,strict_sinks=counts,seconds=time.time()-start);out.append(row);print(row,flush=True);(BASE/'code/height_minimality.json').write_text(json.dumps(out,indent=2))
