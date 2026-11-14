from check import *
from families import rooted
out=None
for v in range(6,15):
 for gid,line in enumerate(subprocess.run([str(P),'-ba',str(v)],capture_output=True,check=True).stdout.decode().splitlines()):
  rot=parse(line);fs,_=faces(rot)
  for R in fs:
   A=rooted(rot,R)
   for s in states(A,R):
    for x,ns in enumerate(rot):
     if len(ns)!=4 or x in R:continue
     edges=[tuple(w for w in f if w!=s[i]) for i,f in enumerate(A) if x not in f]+[(R[0],R[1]),(R[1],R[2])];parent=list(range(v))
     def find(a):
      while parent[a]!=a:a=parent[a]
      return a
     bad=False
     for a,b in edges:
      a,b=find(a),find(b)
      if a==b:bad=True;break
      parent[a]=b
     if bad:out=dict(V=v,gid=gid,root=R,x=x,A=A,state=s,rotation=rot,outer_edges=edges);break
    if out:break
   if out:break
  if out:break
 if out:break
print(out);(BASE/'code/outer_scope_counterexample.json').write_text(json.dumps(out,indent=2))
