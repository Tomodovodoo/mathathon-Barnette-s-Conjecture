"""Audit saved X counterexample, using lab and all direction choices.
Usage: python -B code/repair_witness.py OUT.json
"""
from common import *
import json,itertools,collections
sys.path.insert(0,str(REPO/'workings/barnette_lab'))
from barnette_lab.core import Instance
import networkx as nx

d=json.loads((BASE/'data/x_hypotheses_17_18.json').read_text())['first']['single_D_cycle_repair_fails']
if '--cube' in sys.argv:
    saved=json.loads((BASE/'data/cube_repairs.json').read_text())['first']['all_exception_cube']
    old=saved['source']
    d=dict(V=old['V'],gid=old['gid'],root=old['t0'],setup=[old[k] for k in ('x','a','v1','b','v2')],
           outer=old['outer'],assign=old['assign'],rot=et.plantri(old['V'])[old['gid']])
    kp,dp=(old['v2'],old['v1']) if old['v2'] in old['t0'] else (old['v1'],old['v2'])
    sm={frozenset(f):u for f,u in zip(saved['faces'],saved['states'][0])}; ass=[]
    for f in d['outer']:
        u=sm[frozenset(kp if v==dp else v for v in f)]
        ass.append((kp if kp in f else dp) if u==kp else u)
    d['assign']=ass
nv=d['V'];rot=d['rot'];root=tuple(d['root']);setup=d['setup'];x,a,p,b,q=setup
blacks,ri,whites=next(z for z in et.rooted_instances(rot) if z[0][z[1]]==root)
cb,cri=et.contract(blacks,ri,x,p,q); keep,drop=(q,p) if q in root else (p,q)
outer=[tuple(f) for f in d['outer']]; assign=d['assign']
start={tuple(keep if v==drop else v for v in f):(keep if u==drop else u) for f,u in zip(outer,assign)}
G=nx.Graph();G.add_edges_from(et.edges_from_faces(cb));lab=Instance(G)
lab=Instance(G,next(i for i,f in enumerate(lab.faces) if set(f)==set(cb[cri])))
bykey={frozenset(f):u for f,u in start.items()};ss=tuple(bykey[frozenset(lab.faces[t])] for t in lab.A)
states=list(lab.states());pairs=lab.pairs(states);tms=[s for s in states if lab.is_tree(s)]
partners=[r for r,s in pairs if s==ss];assert len(partners)==1;rr=partners[0]
cycles=lab.dcycles(rr,ss)

def outer_assign(s):
    mp={frozenset(lab.faces[t]):u for t,u in zip(lab.A,s)};ans=[]
    for f in outer:
        u=mp[frozenset(keep if v==drop else v for v in f)]
        ans.append((keep if keep in f else drop) if u==keep else u)
    return ans

def classify(s):
    if not lab.is_tree(s):return 'not_TM'
    ass=outer_assign(s);m=(set((a,p,b,q))-set(root)-set(ass)).pop()
    full=dict(zip(outer,ass));bf=[f for f in blacks if x in f]
    for f in bf:full[f]=m if m in f else x
    if tree(full,root):return 'L'
    aa,vv1,bb,vv2=(a,p,b,q) if m==q else (b,q,a,p)
    g=next(f for f in outer if aa in f and vv2 in f)
    full[g]=vv2
    for f in bf:full[f]=aa if aa in f else x
    return 'R' if tree(full,root) else 'E'

cube=[]
for bits in itertools.product((0,1),repeat=len(cycles)):
    pp=(rr,ss)
    for bit,c in zip(bits,cycles):
        if bit:pp=lab.reverse_d(pp,c)
    cube.append(dict(bits=bits,s=pp[1],classification=classify(pp[1]),qcycles=lab.qcycles(pp[1])))

# D-cycle reversal graph restricted to tree matchings. For each TM its mate is unique.
neighbors={}
for s in tms:
    r=next(r for r,s2 in pairs if s2==s)
    neighbors[s]=[lab.reverse_d((r,s),c)[1] for c in lab.dcycles(r,s)]
    neighbors[s]=[s2 for s2 in neighbors[s] if s2 in tms]
seen={ss};queue=collections.deque([ss]);dist={ss:0};paths={ss:[ss]}
while queue:
    s=queue.popleft()
    for s2 in neighbors[s]:
        if s2 not in seen:
            seen.add(s2);queue.append(s2);dist[s2]=dist[s]+1;paths[s2]=paths[s]+[s2]
esc=[s for s in seen if classify(s)!='E']
best=min(esc,key=dist.get) if esc else None
res=dict(source=d,contracted_faces=[lab.faces[t] for t in lab.A],contracted_root=lab.faces[lab.outer],
         states=len(states),pairs=len(pairs),tree_matchings=len(tms),start=ss,mate=rr,
         cycles=cycles,cube=cube,tm_classes=dict(collections.Counter(classify(s) for s in tms)),
         tree_component_size=len(seen),tree_component_classes=dict(collections.Counter(classify(s) for s in seen)),
         shortest_repair_distance=dist[best] if best else None,shortest_repair_path=paths[best] if best else None,
         original_has_separating_triangle=bool(et.separating_triangles(blacks,whites,root)))
Path(sys.argv[1]).write_text(json.dumps(res,indent=2));print(json.dumps({k:v for k,v in res.items() if k not in ('source','contracted_faces','cube')},indent=2))
