"""Test avoidance, local patterns, mate and D-cycle repairs, all roots.
Usage: python -B code/x_hypotheses.py MIN MAX OUT.json
"""
from common import *
import json,time,collections
from census import pattern_leaves,forest_adj,comp_without

def classify(outer,assign,root,nv,setup):
    x,a,v1,b,v2=setup
    missing=set((a,v1,b,v2))-set(root)-set(assign)
    assert len(missing)==1
    m=missing.pop()
    adj=forest_adj(outer,assign,root,nv)
    C1=comp_without(adj,v1,None)
    assert v2 not in C1
    if m==v2: aa,vv1,bb,vv2=a,v1,b,v2
    else: aa,vv1,bb,vv2=b,v2,a,v1
    if aa not in comp_without(adj,vv1,None):return 'L'
    g=next(f for f in outer if aa in f and vv2 in f)
    cc=next(v for v in g if v not in (aa,vv2))
    assert assign[outer.index(g)]==aa
    return 'E' if bb in comp_without(adj,vv2,(vv2,cc)) else 'R'

def lift_outer(s,outer,keep,drop):
    byface={frozenset(f):u for f,u in s.items()}
    ans=[]
    for f in outer:
        ff=frozenset(keep if v==drop else v for v in f)
        u=byface[ff]
        if u==keep: u=keep if keep in f else drop
        ans.append(u)
    return ans

result={'per_V':{},'first':{}}
def first(name,**kw):
    if name not in result['first']:result['first'][name]=kw
for nv in range(int(sys.argv[1]),int(sys.argv[2])+1):
    start=time.time(); C=collections.Counter()
    for gid,rot in enumerate(et.plantri(nv)):
        C['graphs']+=1
        for blacks,ri,whites in et.rooted_instances(rot):
            t0=blacks[ri]; tms=et.tree_matchings(blacks,ri,nv,collect=True)
            if not tms: continue
            C['rooted_with_TM']+=1
            for f in tms[0]:
                vals={s[f] for s in tms}
                C['black_faces']+=1
                if len(vals)==1:
                    C['frozen_faces']+=1
                    first('frozen',V=nv,gid=gid,root=t0,face=f,choices=list(vals))
            tmkeys={tuple(s[f] for f in tms[0]) for s in tms}
            for s in tms:
                C['TMs']+=1
                r=mate(s,t0)
                if tuple(r[f] for f in tms[0]) not in tmkeys:
                    C['mate_not_TM']+=1
                    first('mate_not_TM',V=nv,gid=gid,root=t0,faces=list(s),s=list(s.values()),r=[r[f] for f in s])
            for setup in et.degree4_setups(blacks,whites,t0):
                x,a,v1,b,v2=setup
                f1=next(f for f in blacks if set(f)=={x,a,v1}); f2=next(f for f in blacks if set(f)=={x,b,v2})
                feasible={(x,v2),(v1,x),(x,b),(a,x)}
                feasible={p for p in feasible if not set(p)&set(t0)}
                patterns={(s[f1],s[f2]) for s in tms}
                C['vertices']+=1
                if patterns!=feasible:
                    C['not_all_feasible_patterns']+=1
                    first('missing_pattern',V=nv,gid=gid,root=t0,setup=setup,patterns=sorted(patterns),feasible=sorted(feasible),rot=rot)
                C['minimum_patterns_'+str(len(patterns))]+=1
                for setup2 in (setup,(x,v1,a,v2,b)):
                    xx,aa,p,bb,q=setup2
                    cb,cri=et.contract(blacks,ri,x,p,q)
                    if not et.is_simple(cb):continue
                    # Reuse directly enumerated outer states for exception identification.
                    outer,leaves=pattern_leaves(blacks,ri,nv,x,(aa,p,bb,q),True)
                    keep,drop=(q,p) if q in t0 else (p,q)
                    ct0=cb[cri]
                    for m,c,assign in leaves:
                        if m not in (p,q) or c[1]==c[3]:continue
                        cls=classify(outer,assign,t0,nv,setup2)
                        if cls!='E':continue
                        C['exceptions']+=1
                        sf={tuple(keep if v==drop else v for v in f):(keep if u==drop else u) for f,u in zip(outer,assign)}
                        rr=mate(sf,ct0)
                        rtree=tree(rr,ct0)
                        rc=classify(outer,lift_outer(rr,outer,keep,drop),t0,nv,setup2) if rtree else 'not_TM'
                        C['exception_mate_'+rc]+=1
                        if rc in ('E','not_TM'):
                            first('mate_repair_fails',V=nv,gid=gid,root=t0,setup=setup2,outer=outer,assign=assign,mate_class=rc)
                        # Reverse each cycle of D(r,s), i.e. exchange r and s on it.
                        bytail={rr[f]:f for f in sf}; seen=set(); successes=0; details=[]; critical=[]
                        for u in bytail:
                            if u in seen:continue
                            cyc=[]; z=u
                            while z not in seen:
                                seen.add(z); f=bytail[z]; cyc.append(f); z=sf[f]
                            new=dict(sf)
                            for f in cyc:new[f]=rr[f]
                            ok=tree(new,ct0)
                            nc=classify(outer,lift_outer(new,outer,keep,drop),t0,nv,setup2) if ok else 'not_TM'
                            successes+=nc in ('L','R'); details.append(nc)
                            if any(keep in (rr[f],sf[f]) for f in cyc):critical.append(nc)
                        if critical:
                            C['merged_vertex_cycle_'+critical[0]]+=1
                        if not successes:
                            C['no_single_D_cycle_repair']+=1
                            first('single_D_cycle_repair_fails',V=nv,gid=gid,root=t0,setup=setup2,outer=outer,assign=assign,cycle_results=details,rot=rot)
    C['seconds']=round(time.time()-start,2)
    result['per_V'][nv]=dict(C); print(nv,dict(C),flush=True)
    Path(sys.argv[3]).write_text(json.dumps(result,indent=2))
