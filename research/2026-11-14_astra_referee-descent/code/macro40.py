from check import *
from covers import cover_pairs
from potentials import component,geometry,potential
from families import rooted
names=['(k,'+a+'om,'+b+'psi)' for a in ('+','-') for b in ('+','-')]+['(k,'+a+'psi,'+b+'om)' for a in ('+','-') for b in ('+','-')]
lines=(BASE/'code/regenerated40.txt').read_text().splitlines();found={}
for gid in [3]+[i for i in range(40) if i!=3]:
 rot=parse(lines[gid]);fs,_=faces(rot)
 for R in fs:
  A=rooted(rot,R);pp=cover_pairs(A,R);todo={p for p in pp if info(A,p)[1]}
  while todo:
   ad,vals=component(A,next(iter(todo)),geometry(rot,R));todo.difference_update(ad)
   near={p:set(ws).union(*(set(ad[w]) for w in ws)) for p,ws in ad.items()}
   for name in names:
    if name in found:continue
    costs={p:potential(name,v) for p,v in vals.items()};bad=[p for p,v in vals.items() if v[0] and all(costs[w]>=costs[p] for w in near[p])]
    if bad:found[name]=dict(gid=gid,root=R,rotation=rot,A=A,pair=bad[0]);print('found',name,gid,R,flush=True)
   (BASE/'code/macro40.json').write_text(json.dumps(found,indent=2))
  if len(found)>=7:break
 if len(found)>=7:break
print('total',len(found))

subprocess.run([sys.executable,str(BASE/'code/finalize_macro.py')],check=True)
