from remaining import *
# Hall obstruction fixture and gluing-cycle counts.
c=C['pairs']['obstruction'];f,v,e,t,l,g,b,a,xx,w=setup(c['faces'],c['t0']);st=enum(f,a,xx);prs=[(u,z) for u in st for z in st if all(k!=h for k,h in zip(u,z))];ck('separating triangle obstruction',[len(st),len(prs),sum(min(2,len(set(c['S'])&set(f[t]))) for t in a)],[4,0,5])
# The displayed rainbow exchange is still a spanning tree, with doubled/missed face.
r=tuple(C['running']['states'][C['running']['r']]);sel=set(zip(A,r));newsel=sel-{tuple(C['rainbow']['remove'])}|{tuple(C['rainbow']['add'])};hh=H.copy();hh.remove_edges_from((('t',t),('v',v)) for t,v in newsel);ck('exchanged spoke complement tree',nx.is_tree(hh),True);ck('exchanged face counts',[sum(tt==t for tt,v in newsel) for t in A],C['rainbow']['counts_after']);ck('exchanged point counts',[sum(vv==v for t,vv in newsel) for v in X],[1]*len(X))
# Independently enumerate every compatible lift of each smaller good state.
x0=2;merge=3;gone=1;ret=[i for i,f in enumerate(F) if x0 not in f];fs=[tuple(merge if v==gone else v for v in F[i]) for i in ret];idx=next(i for i,f in enumerate(fs) if set(f)==roots);f,v,e,t,l,g,b,a,xx,w=setup(fs,idx);ss=enum(f,a,xx);sg=[z for z in ss if nx.is_forest(qgraph(z,f,a,v)) and all(len(set(cc)&roots)==1 for cc in nx.connected_components(qgraph(z,f,a,v)))];lifts=[]
for z in sg:
 candidates=[]
 for zz in S:
  ch=dict(zip(A,zz));ok=True
  for ti,vv in zip(a,z):
   old=ret[ti];val=merge if ch[old]==gone else ch[old]
   if val!=vv:ok=False
  if ok:candidates.append(zz)
 assert len(candidates)==1;lifts.append(candidates[0])
ck('contraction good/successful lifts',[len(sg),sum(map(good,lifts))],[4,3]);bad=next(z for z in lifts if not good(z));repairs=[]
for zz in S:
 diff=[t for t,u,vv in zip(A,bad,zz) if u!=vv]
 if len(diff)==3 and good(zz) and any(set(diff)=={next(t for t in B if {u,v}<=set(F[t])) for u,v in zip(F[w],F[w][1:]+F[w][:1])} for w in W):repairs.append(zz)
ck('failed lift white-face repair exists',bool(repairs),True)
(O/'final-checks.json').write_text(json.dumps(dict(checks=checks,lifts=lifts,repairs=repairs),indent=2,default=str));print('checks',len(checks),'failed',sum(not c['ok'] for c in checks))
