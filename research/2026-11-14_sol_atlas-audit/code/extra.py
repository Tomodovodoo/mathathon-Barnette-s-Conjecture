from independent import *
# Disk from dual flood-fill after blocking its directed boundary.
cycle=C['disk']['cycle'];blocked={tuple(sorted(e)) for e in zip(cycle,cycle[1:]+cycle[:1])};dg=G.copy();dg.remove_edges_from((left[a,b],left[b,a]) for a,b in blocked);shore=next(set(c) for c in nx.connected_components(dg) if j['t0'] not in c);ib=shore&set(B);iw=shore&set(W);iv=set().union(*(set(F[f]) for f in shore))-set(cycle);ell=sum(left[a,b] in ib or left[b,a] in ib for a,b in blocked);ell=sum(next(t for t in B if {a,b}<=set(F[t])) in shore for a,b in blocked)
ck('disk census',[len(ib),len(iw),len(iv),len(cycle),ell],[5,6,3,7,2]);r=tuple(C['running']['states'][C['running']['r']]);turns=[3-sum(1 if f in W else (5 if r[A.index(f)]==v else -1) for f in shore if v in F[f]) for v in cycle];ck('disk turns',turns,C['disk']['turns'])
# Validate every displayed recovery edge independently of the recovery implementation.
pe=[tuple(e) for e in C['recovery']['P']];pg=nx.Graph();pg.add_nodes_from(V);pg.add_edges_from(pe);ps=list(map(set,nx.connected_components(pg)));assert len(ps)==2 and all(nx.is_tree(T.subgraph(u)) for u in ps);assert set(pe)<=E
ham=[(left[a,b],left[b,a]) for a,b in E if (a in ps[0])!=(b in ps[0])];hg=nx.Graph(ham);ck('recovered Hamiltonian graph',[len(hg),hg.number_of_edges(),nx.is_connected(hg),sorted(set(dict(hg.degree()).values()))],[22,22,True,[2]])
ck('recovery selected edge per black face',[sum(set(e)<=set(F[t]) for e in pe) for t in B],[1]*len(B))
for z in S:
 hh=H.copy();hh.remove_edges_from((('t',t),('v',v)) for t,v in zip(A,z));ck('spoke complement s'+str(names[z]),nx.is_tree(hh),good(z))
# Full overlay table recomputed in display-name order.
ordered=sorted(S,key=names.get);tab=[[sum(a==b for a,b in zip(r,s)) for s in ordered] for r in ordered];ck('144 shared-spoke entries',tab,C['dimers']['shared'])
# Recover the two unused-corner maps and height difference without toolkit cycle code.
covers={tuple(next(v for v in F[t] if v not in (r[i],s[i])) for i,t in enumerate(A)) for r,s in P};ck('cover count',len(covers),2)
cv=list(covers);diff=list(map(int,M.gauss_jordan_solve(vec(cv[0])-vec(cv[1]))[0]));ck('cover step absolute height',sorted(map(abs,diff)),[0]*7+[1])
# Heawood torus incidence permutations, independent of atlas figure function.
black=[(i,(i+1)%7,(i+3)%7) for i in range(7)];ss=[p for p in it.permutations(range(7)) if all(p[i] in black[i] for i in range(7))];pp=[(a,b) for a in ss for b in ss if all(u!=v for u,v in zip(a,b))];sm=Counter();cancel=defaultdict(int)
for a,b in pp:
 signs=[1 if black[i][(black[i].index(a[i])+1)%3]==b[i] else -1 for i in range(7)];sm[sum(signs)]+=1;cancel[b]+=math.prod(signs);d=nx.DiGraph(zip(a,b));assert nx.is_strongly_connected(d)
ck('Heawood states/pairs',[len(ss),len(pp)],[24,48]);ck('Heawood signs',dict((str(k),v) for k,v in sm.items()),C['pfaffian']['delta_sums']);ck('Heawood cancellation',set(cancel.values())=={0},True)
# Prism counts via independent partitions, direct states, and pair counts.
import sys
sys.path.insert(0,str(R/'workings/barnette_lab'))
from barnette_lab.core import dual_graph,faces_of
prisms=[]
for p in [4,6,8,10,12]:
 tt=dual_graph(nx.circular_ladder_graph(p));_,em=nx.check_planarity(tt);fs,_=faces_of(em);ff,vv,ee,t,l,g,bb,aa,xx,ww=setup(fs,0);sts=enum(ff,aa,xx);prs=[(a,b) for a in sts for b in sts if all(u!=v for u,v in zip(a,b))];rr=set(ff[0]);goodn=sum(nx.is_forest(qgraph(z,ff,aa,vv)) and all(len(set(c)&rr)==1 for c in nx.connected_components(qgraph(z,ff,aa,vv))) for z in sts)
 # Hamilton cycles counted via omitted perfect matchings in cubic primal graph.
 gg=nx.circular_ladder_graph(p);match=[]
 def pm(rem,es):
  if not rem:
   hh=gg.copy();hh.remove_edges_from(es)
   if nx.is_connected(hh):match.append(es)
   return
  u=min(rem)
  for v in gg[u]:
   if v in rem:pm(rem-{u,v},es+[(u,v)])
 pm(set(gg),[]);prisms.append([p,len(sts),len(prs),goodn,len(match)]);ck('prism '+str(p),prisms[-1],[p,p//2,2,2,p+2])
(O/'extra.json').write_text(json.dumps(dict(checks=checks,prisms=prisms,disk_faces=sorted(shore)),indent=2,default=str));print('total checks',len(checks),'failed',sum(not c['ok'] for c in checks))
