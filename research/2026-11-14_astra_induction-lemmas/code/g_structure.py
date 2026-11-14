"""Test exact short-cycle obstruction and disk curvature on no-separator census.
Usage: python -B code/g_structure.py MIN MAX OUT.json
Enumerates chordless 4/5-cycles with both sides nonempty. Both colourings/all roots.
"""
from common import *
import json,collections,time,itertools

def shortcycles(rot):
    found=set()
    for start in range(len(rot)):
        def dfs(path):
            for v in rot[path[-1]]:
                if v==start:
                    if len(path) in (4,5): found.add(min(tuple(path),tuple([start]+list(reversed(path[1:])))))
                elif v>start and v not in path and len(path)<5:dfs(path+[v])
        dfs([start])
    return sorted(found)

def disks(rot,fs,col):
    ans=[]
    side=collections.defaultdict(list)
    for i,f in enumerate(fs):
        for j in range(3):side[frozenset((f[j],f[(j+1)%3]))].append(i)
    for cyc in shortcycles(rot):
        Z=set(cyc); edges={frozenset((cyc[i],cyc[(i+1)%len(cyc)])) for i in range(len(cyc))}
        if any(v in Z and frozenset((u,v)) not in edges for u in Z for v in rot[u]):continue
        adj=[[] for f in fs]
        for e,(a,b) in side.items():
            if e not in edges:adj[a].append(b);adj[b].append(a)
        a=side[next(iter(edges))][0]; seen={a}; stack=[a]
        while stack:
            for b in adj[stack.pop()]:
                if b not in seen:seen.add(b);stack.append(b)
        for region in (seen,set(range(len(fs)))-seen):
            inside={v for i in region for v in fs[i]}-Z
            if not inside:continue
            w=sum(col[next(i for i in side[e] if i in region)] for e in edges)
            signs=[col[next(i for i in side[frozenset((cyc[j],cyc[(j+1)%len(cyc)]))] if i in region)] for j in range(len(cyc))]
            changes=sum(signs[j]!=signs[j-1] for j in range(len(cyc)))
            # col=1 is white in the reference colouring.
            degD={v:len({u for i in region if v in fs[i] for u in fs[i] if u!=v}) for v in Z}
            n4=sum(len(rot[v])==4 for v in inside)
            excess=sum(len(rot[v])-6 for v in inside if len(rot[v])>=6)
            assert 2*n4==6+excess+sum(d-4 for d in degD.values())
            assert n4>=1
            assert 2*n4>=6-changes
            if len(cyc)==5 and w in (1,4):assert n4>=2
            apex={next(iter(set(fs[i])-Z)) for i in region if len(set(fs[i])&Z)==2}
            ans.append(dict(cycle=cyc,inside=inside,faces=region,w=w,n4=n4,apex=apex,degD=degD))
    return ans

out={'per_V':{},'first':{}}
def first(k,**v):
    if k not in out['first']:out['first'][k]=v
for nv in range(int(sys.argv[1]),int(sys.argv[2])+1):
    start=time.time(); C=collections.Counter()
    for gid,rot in enumerate(et.plantri(nv)):
        fs=et.faces_of(rot); col=et.two_colour(fs)
        B=[f for f,c in zip(fs,col) if c==0]; W=[f for f,c in zip(fs,col) if c==1]
        if et.separating_triangles(B,W,B[0]):continue
        C['graphs']+=1
        ds=disks(rot,fs,col)
        for d in ds:
            C['disks_'+str(len(d['cycle']))]+=1
            if all(v in d['apex'] for v in d['inside'] if len(rot[v])==4):
                C['all_degree4_vertices_are_apices']+=1
                first('all_apices',V=nv,gid=gid,cycle=d['cycle'],inside=sorted(d['inside']),rot=rot)
        for fi,t0 in enumerate(fs):
            bc=col[fi]; blacks=[f for f,c in zip(fs,col) if c==bc]; whites=[f for f,c in zip(fs,col) if c!=bc];ri=blacks.index(t0)
            C['rooted']+=1; good={}; witnesses={}
            for setup in et.degree4_setups(blacks,whites,t0):
                x,a,p,b,q=setup; good[x]=[]
                for keep,drop in ((p,q),(a,b)):
                    cb,cri=et.contract(blacks,ri,x,keep,drop)
                    simple=et.is_simple(cb); pair=et.has_pair_flow(cb,cri)
                    good[x].append(simple and pair)
                    ws=[]
                    for di,d in enumerate(ds):
                        cyc=d['cycle']; L=len(cyc)
                        if x not in cyc or fi in d['faces']:continue
                        j=cyc.index(x)
                        if {cyc[j-1],cyc[(j+1)%L]}!={keep,drop}:continue
                        w=d['w'] if bc==0 else L-d['w']
                        if L==4 or w==1:ws.append(di)
                    assert bool(ws)==(not simple or not pair),(nv,gid,t0,setup,keep,drop,ws)
                    C['merges']+=1;C['bad_merges']+=bool(ws)
                    if simple and not pair:
                        C['simple_bad_merges']+=1
                        first('simple_bad_5cycle',V=nv,gid=gid,root=t0,setup=setup,merge=[keep,drop],cycle=ds[ws[0]]['cycle'],inside=sorted(ds[ws[0]]['inside']),rot=rot)
                    witnesses[(x,keep,drop)]=ws
            if nv>6:assert any(any(v) for v in good.values())
            badregions=set(i for ws in witnesses.values() for i in ws)
            badsource5={i for (xx,pp,qq),ws in witnesses.items() if not any(good[xx]) for i in ws if len(ds[i]['cycle'])==5}
            for i in badsource5:
                ins=ds[i]['inside'];hasgood=any(any(good.get(v,[])) for v in ins)
                C['five_regions_from_blocked_vertices']+=1
                if not hasgood:
                    C['blocked_source_five_no_good_inside']+=1
                    first('blocked_source_five_no_good_inside',V=nv,gid=gid,root=t0,cycle=ds[i]['cycle'],inside=sorted(ins),good=good,rot=rot)
                if not any(ds[j]['inside']<ins for j in badsource5):
                    C['minimal_blocked_source_five']+=1
                    if not hasgood:
                        C['minimal_blocked_source_five_no_good_inside']+=1
                        first('minimal_blocked_source_five_no_good_inside',V=nv,gid=gid,root=t0,cycle=ds[i]['cycle'],inside=sorted(ins),good=good,rot=rot)
            for i in badregions:
                d=ds[i]; ins=d['inside']; hasgood=any(any(good.get(v,[])) for v in ins)
                C['bad_regions']+=1
                if len(d['cycle'])==5:
                    C['bad_five_regions']+=1
                    minimal5=not any(len(ds[j]['cycle'])==5 and ds[j]['inside']<ins for j in badregions)
                    if minimal5:C['minimal_bad_five_regions']+=1
                    if not hasgood:
                        C['bad_five_region_no_good_inside']+=1
                        first('bad_five_region_no_good_inside',V=nv,gid=gid,root=t0,cycle=d['cycle'],inside=sorted(ins),good=good,rot=rot)
                        if minimal5:
                            C['minimal_bad_five_region_no_good_inside']+=1
                            first('minimal_bad_five_region_no_good_inside',V=nv,gid=gid,root=t0,cycle=d['cycle'],inside=sorted(ins),good=good,rot=rot)
                if not hasgood:
                    C['bad_region_no_good_inside']+=1
                    first('bad_region_no_good_inside',V=nv,gid=gid,root=t0,cycle=d['cycle'],inside=sorted(ins),good=good,rot=rot)
                minimal=not any(ds[j]['inside']<ins for j in badregions)
                if minimal:
                    C['minimal_bad_regions']+=1
                    if not hasgood:
                        C['minimal_bad_region_no_good_inside']+=1
                        first('minimal_bad_region_no_good_inside',V=nv,gid=gid,root=t0,cycle=d['cycle'],inside=sorted(ins),good=good,rot=rot)
    C['seconds']=round(time.time()-start,2);out['per_V'][nv]=dict(C)
    print(nv,dict(C),flush=True);Path(sys.argv[3]).write_text(json.dumps(out,indent=2))
