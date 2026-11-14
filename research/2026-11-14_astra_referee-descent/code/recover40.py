from check import *
from covers import cover_pairs
from potentials import component,geometry,potential
from families import rooted
import collections
source=REPO/'research/2026-11-14_opus_conjectures/code/gen.py'
lines=subprocess.run([sys.executable,str(source),'skew','40','40','15'],capture_output=True,check=True).stdout.decode().splitlines()
(BASE/'code/regenerated40.txt').write_text('\n'.join(lines)+'\n')
out=[]
totals=dict(graphs=0,roots=0,paired_roots=0,pairs=0,good=0)
lo,hi=map(int,sys.argv[1:]);start=time.time()
for gid in range(lo,hi):
 rot=parse(lines[gid]);fs,_=faces(rot)
 for R in fs:
  A=rooted(rot,R);pp=cover_pairs(A,R);qs={p:len(info(A,p)[1]) for p in pp};adj={p:list(moves(A,p)) for p in pp}
  totals["roots"]+=1;totals["paired_roots"]+=bool(pp);totals["pairs"]+=len(pp);totals["good"]+=sum(q==0 for q in qs.values())
  reached={p for p in pp if qs[p]==0};queue=list(reached)
  for p in queue:
   for z in adj[p]:
    if z not in reached and qs[z]>=qs[p]:reached.add(z);queue.append(z)
  assert len(reached)==len(pp), "C3 counterexample"
  for p in pp:
   if qs[p]==0 or any(qs[z]<qs[p] for z in adj[p]):continue
   seen={p};front=[p];radius=None
   for depth in range(1,5):
    nxt=set(w for z in front for w in adj[z])-seen;seen.update(nxt)
    if any(qs[w]<qs[p] for w in nxt):radius=depth;break
    front=nxt
   if radius is None or radius>=4:
    row=dict(kind='radius',gid=gid,root=R,radius=radius,A=A,pair=p,rotation=rot);out.append(row);print('RADIUS',gid,R,radius,flush=True)
  if gid==21 and set(R)=={6,30,31}:
   todo=set(pp)
   while todo:
    p=next(iter(todo));ad,vals=component(A,p,geometry(rot,R));todo.difference_update(ad)
    for name in ('vq','wq','(k,vq)','(k,wq)'):
     costs={p:potential(name,v) for p,v in vals.items()};reach={p for p,v in vals.items() if v[0]==0};queue=list(reach)
     for p in queue:
      for z in ad[p]:
       if z not in reach and costs[z]>=costs[p]:reach.add(z);queue.append(z)
     bad=set(ad)-reach
     if bad:
      row=dict(kind='potential',potential=name,gid=gid,root=R,A=A,pair=next(iter(bad)),rotation=rot,trapped=len(bad));out.append(row);print('TRAP',name,len(bad),flush=True)
 totals['graphs']+=1
 (BASE/f'code/summary40_{lo}_{hi}.json').write_text(json.dumps(totals,indent=2))
 print('graph',gid,'seconds',time.time()-start,flush=True)
 (BASE/f'code/recovered40_{lo}_{hi}.json').write_text(json.dumps(out,indent=2))
