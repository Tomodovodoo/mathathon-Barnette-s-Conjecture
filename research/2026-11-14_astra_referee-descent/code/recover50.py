from check import *
from covers import cover_pairs
from potentials import component,geometry,potential
from families import rooted
source=REPO/'research/2026-11-14_opus_conjectures/code/gen.py'
raw=subprocess.run([sys.executable,str(source),'skew','50','12','6'],capture_output=True,check=True).stdout.decode().splitlines()[11];rot=parse(raw);R=(5,15,14);A=rooted(rot,R);pp=cover_pairs(A,R);todo=set(pp);out=[]
while todo:
 ad,vals=component(A,next(iter(todo)),geometry(rot,R));todo.difference_update(ad)
 near={p:set(ws).union(*(set(ad[w]) for w in ws)) for p,ws in ad.items()}
 for name in ('vq','wq','(k,vq)','(k,wq)'):
  costs={p:potential(name,v) for p,v in vals.items()};reach={p for p,v in vals.items() if v[0]==0};queue=list(reach)
  for p in queue:
   for z in near[p]:
    if z not in reach and costs[z]>=costs[p]:reach.add(z);queue.append(z)
  bad=set(ad)-reach
  if bad:out.append(dict(potential=name,root=R,rotation=rot,A=A,pair=next(iter(bad)),component=len(ad),trapped=len(bad)));print(name,len(bad),flush=True)
(BASE/'code/recovered50.json').write_text(json.dumps(out,indent=2))
