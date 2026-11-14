"""Independent lab replay of G witness and full small TM sets.
Usage: python -B code/check_certificates.py OUT.json
"""
from common import *
import json,itertools,collections
sys.path.insert(0,str(REPO/'workings/barnette_lab'))
from barnette_lab.core import Instance
import networkx as nx

def instance(blacks,root):
    g=nx.Graph();g.add_edges_from(et.edges_from_faces(blacks));I=Instance(g)
    return Instance(g,next(i for i,f in enumerate(I.faces) if set(f)==set(root)))

small=collections.Counter()
for nv in range(6,14):
    for rot in et.plantri(nv):
        for B,ri,W in et.rooted_instances(rot):
            I=instance(B,B[ri]); ss=list(I.states()); tt=[s for s in ss if I.is_tree(s)]
            own=et.tree_matchings(B,ri,nv,True)
            faces=sorted(tuple(sorted(I.faces[t])) for t in I.A)
            def key(mp):return tuple(mp[frozenset(f)] for f in faces)
            expected={key({frozenset(I.faces[t]):u for t,u in zip(I.A,s)}) for s in tt}
            actual={key({frozenset(f):u for f,u in s.items()}) for s in own}
            assert expected==actual
            small['rooted_instances']+=1;small['tree_matchings']+=len(tt)

d=json.loads((BASE/'data/g_structure_8_16.json').read_text())['first']['minimal_bad_region_no_good_inside']
rot=d['rot'];root=d['root'];B,ri,W=next(z for z in et.rooted_instances(rot) if set(z[0][z[1]])==set(root))
gout=dict(V=len(rot),root=root,black_faces=B,white_faces=W,cycle=d['cycle'],inside=d['inside'],merges=[])
for setup in et.degree4_setups(B,W,root):
    x,a,p,b,q=setup
    if x not in (5,6):continue
    for keep,drop in ((p,q),(a,b)):
        cb,cri=et.contract(B,ri,x,keep,drop);simple=et.is_simple(cb)
        record=dict(x=x,merge=[keep,drop],simple=simple,black_faces=cb,root=cb[cri])
        # independent networkx max-flow including parallel-result black centres
        roots=set(cb[cri]);A=[f for i,f in enumerate(cb) if i!=cri];X={v for f in cb for v in f}-roots;F=nx.DiGraph()
        for v in X:F.add_edge('s',('v',v),capacity=2)
        for i,f in enumerate(A):
            F.add_edge(('f',i),'t',capacity=2)
            for v in set(f)&X:F.add_edge(('v',v),('f',i),capacity=1)
        record['flow']=nx.maximum_flow_value(F,'s','t');record['required']=2*len(A)
        assert record['flow']<record['required']
        # Smallest Hall violation by cardinality.
        for size in range(1,len(X)+1):
            bad=[]
            for ss in itertools.combinations(sorted(X),size):
                val=sum(min(2,len(set(f)&set(ss))) for f in A)-2*size
                if val<0:bad.append(dict(S=ss,f=val))
            if bad:record['Hall_witness']=bad[0];break
        gout['merges'].append(record)
res=dict(small_set_validation=dict(small),G_certificate=gout)
Path(sys.argv[1]).write_text(json.dumps(res,indent=2));print(json.dumps(dict(small=small,G_merges=[{k:v for k,v in r.items() if k!='black_faces'} for r in gout['merges']]),indent=2))
