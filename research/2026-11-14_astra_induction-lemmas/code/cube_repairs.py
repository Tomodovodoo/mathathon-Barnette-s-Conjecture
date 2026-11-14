"""Test entire fixed covers and tree-preserving D reversal components on saved exceptions.
Usage: python -B code/cube_repairs.py OUT.json
Input exceptions through V=18 are the complete Fable census, read without modification.
"""
from common import *
import json,gzip,collections,itertools,time
from census import forest_adj,comp_without

def rows():
    base=REPO/'research/2026-11-14_fable_induction-completion/data'
    for fn in ('exceptions_6_13.jsonl','exceptions_14_17.jsonl.gz','exceptions_18.jsonl.gz'):
        op=gzip.open if fn.endswith('.gz') else open
        with op(base/fn,'rt') as f:
            yield from map(json.loads,f)

def cls(s,d):
    x,a,p,b,q=(d[k] for k in ('x','a','v1','b','v2'));root=d['t0']
    keep,drop=(q,p) if q in root else (p,q)
    outer=[tuple(f) for f in d['outer']];mp={frozenset(f):u for f,u in s.items()};ass=[]
    for f in outer:
        u=mp[frozenset(keep if v==drop else v for v in f)]
        ass.append((keep if keep in f else drop) if u==keep else u)
    m=(set((a,p,b,q))-set(root)-set(ass)).pop()
    aa,vv1,bb,vv2=(a,p,b,q) if m==q else (b,q,a,p)
    adj=forest_adj(outer,ass,root,d['V'])
    if aa not in comp_without(adj,vv1,None):return 'L'
    g=next(f for f in outer if aa in f and vv2 in f);cc=next(v for v in g if v not in (aa,vv2))
    return 'E' if bb in comp_without(adj,vv2,(vv2,cc)) else 'R'

res={'per_V':{},'first':{}}; seen=set();start=time.time()
for d in rows():
    nv=d['V'];key=(nv,d['gid'],tuple(d['t0']),d['x'],tuple(sorted((d['v1'],d['v2']))))
    if key in seen:continue
    seen.add(key);C=res['per_V'].setdefault(nv,collections.Counter());C['contractions']+=1
    blacks=[tuple(f) for f in d['blacks']];ri=next(i for i,f in enumerate(blacks) if set(f)==set(d['t0']))
    cb,cri=et.contract(blacks,ri,d['x'],d['v1'],d['v2']);root=cb[cri]
    tms=et.tree_matchings(cb,cri,nv,True);faces=list(tms[0]);groups=collections.defaultdict(list)
    total_e=sum(cls(s,d)=='E' for s in tms)
    C['exceptions']+=total_e
    C['max_exception_fraction']=max(C['max_exception_fraction'],total_e/len(tms))
    assert 2*total_e<=len(tms)
    for s in tms:
        r=mate(s,root);u=tuple(next(v for v in f if v not in (s[f],r[f])) for f in faces)
        groups[u].append((s,r,cls(s,d)))
    for u,group in groups.items():
        if not any(k=='E' for s,r,k in group):continue
        C['exception_cubes']+=1
        e=sum(k=='E' for s,r,k in group)
        if 2*e>len(group):C['half_bound_fails_per_cube']+=1
        if e==len(group):
            C['all_TM_in_cube_exceptional']+=1
            if 'all_exception_cube' not in res['first']:res['first']['all_exception_cube']=dict(source=d,unused=u,faces=faces,states=[list(s[f] for f in faces) for s,r,k in group])
        # Flip graph on this cube's successful orientations.
        keys={tuple(s[f] for f in faces):(s,r,k) for s,r,k in group}; unseen=set(keys)
        while unseen:
            initial=next(iter(unseen));unseen.remove(initial);comp={initial};stack=[initial]
            while stack:
                sk=stack.pop();s,r,k=keys[sk];bytail={r[f]:f for f in faces};used=set()
                for v in bytail:
                    if v in used:continue
                    ff=[];z=v
                    while z not in used:used.add(z);f=bytail[z];ff.append(f);z=s[f]
                    ff=set(ff);nk=tuple(r[f] if f in ff else s[f] for f in faces)
                    if nk in unseen:unseen.remove(nk);comp.add(nk);stack.append(nk)
            if any(keys[k][2]=='E' for k in comp):
                C['exception_components']+=1
                if all(keys[k][2]=='E' for k in comp):
                    C['all_component_exceptional']+=1
                    if 'all_exception_component' not in res['first']:res['first']['all_exception_component']=dict(source=d,faces=faces,states=list(comp))
res['seconds']=round(time.time()-start,2)
Path(sys.argv[1]).write_text(json.dumps(res,indent=2));print(json.dumps({k:v for k,v in res.items() if k!='first'},indent=2))
