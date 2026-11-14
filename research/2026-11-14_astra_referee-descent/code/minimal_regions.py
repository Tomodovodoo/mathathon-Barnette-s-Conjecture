from structure import *
out=[];first={}
for v in range(8,17):
 counts=dict(four=0,five=0,blocked_five=0)
 for gid,line in enumerate(subprocess.run([str(P),'-ba',str(v)],capture_output=True,check=True).stdout.decode().splitlines()):
  rot=parse(line);result=structure(rot)
  if result is None:continue
  _,details=result
  for R,valid,ws in details:
   bad4=[]
   for x in valid:
    ns=rot[x]
    for p,q in ((ns[0],ns[2]),(ns[1],ns[3])):
     for y in (set(rot[p])&set(rot[q]))-set(ns)-{x}:
      C=(x,p,y,q);I,w=region(rot,C,R);bad4.append((C,I))
   for name,pool in [('four',bad4),('five',ws),('blocked_five',[(C,I) for C,I in ws if not any(valid[C[0]] )])]:
    for C,I in pool:
     deg4=[x for x in I if len(rot[x])==4]
     if not deg4 or any(any(valid[x]) for x in deg4):continue
     if any(J<I for _,J in pool):continue
     counts[name]+=1
     first.setdefault(name,dict(V=v,gid=gid,root=R,cycle=C,inside=sorted(I)))
 row=dict(V=v,**counts);out.append(row);print(row,flush=True);(BASE/'code/minimal_regions.json').write_text(json.dumps(dict(counts=out,first=first),indent=2))
