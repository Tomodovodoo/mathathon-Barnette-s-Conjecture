from families import *
def split_random(rot,rng):
 v=rng.randrange(len(rot));ns=rot[v];i=rng.randrange(len(ns));ns=ns[i:]+ns[:i];j=rng.choice(list(range(2,len(ns)-1,2)));a,b=ns[0],ns[j];q=len(rot);x=q+1;g=graph(rot)
 for z in ns[j+1:]:g.remove_edge(v,z);g.add_edge(q,z)
 for z in (a,b):g.add_edge(q,z)
 for z in (a,v,b,q):g.add_edge(x,z)
 rr=rotation(g);assert all(len(n)%2==0 for n in rr);faces(rr);return rr
if __name__=='__main__':
 rng=random.Random(714992);out=[]
 for v in (26,30,34):
  for j in range(5):
   rot=tube(4,0)
   while len(rot)<v:rot=split_random(rot,rng)
   fs,_=faces(rot);R=rng.choice(fs);res=check(rooted(rot,R),R);row=dict(V=v,sample=j,root=R,rotation=rot,**res);out.append(row);print({k:v for k,v in row.items() if k!='rotation'},flush=True)
   (BASE/'code/random.json').write_text(json.dumps(out,indent=2))
