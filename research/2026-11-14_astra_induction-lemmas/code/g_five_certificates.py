"""Replay refined five-cycle counterexamples with independent NetworkX flow.
Usage: python -B code/g_five_certificates.py OUT.json
"""
from common import *
import json,itertools,networkx as nx
data=json.loads((BASE/'data/g_structure_8_19.json').read_text())['first'];out=[]
for key in ('minimal_bad_five_region_no_good_inside','minimal_blocked_source_five_no_good_inside'):
    d=data[key];rot=d['rot'];root=d['root'];inside=set(d['inside']);cyc=d['cycle'];Z=set(cyc)
    B,ri,W=next(z for z in et.rooted_instances(rot) if set(z[0][z[1]])==set(root))
    graph=nx.Graph((v,u) for v,nb in enumerate(rot) for u in nb)
    assert inside in list(nx.connected_components(graph.subgraph(set(graph)-Z)))
    actual={frozenset(f) for f in B+W}
    assert all(frozenset(t) in actual for t in itertools.combinations(graph,3) if all(graph.has_edge(a,b) for a,b in itertools.combinations(t,2)))
    signs=[]
    for a,b in zip(cyc,cyc[1:]+cyc[:1]):
        ff=[f for f in B+W if {a,b}.issubset(f) and (set(f)-{a,b}).issubset(inside)]
        assert len(ff)==1
        signs.append('B' if ff[0] in B else 'W')
    assert signs.count('W')==1
    checks=[]; blocked=[]
    for setup in et.degree4_setups(B,W,root):
        x,a,p,b,q=setup
        if x not in inside|Z:continue
        flows=[]
        for keep,drop in ((p,q),(a,b)):
            cb,cri=et.contract(B,ri,x,keep,drop);A=[f for i,f in enumerate(cb) if i!=cri];X={v for f in cb for v in f}-set(cb[cri]);F=nx.DiGraph()
            for v in X:F.add_edge('s',('v',v),capacity=2)
            for i,f in enumerate(A):
                F.add_edge(('f',i),'t',capacity=2)
                for v in set(f)&X:F.add_edge(('v',v),('f',i),capacity=1)
            flow=nx.maximum_flow_value(F,'s','t');flows.append(flow)
            checks.append(dict(x=x,merge=[keep,drop],simple=et.is_simple(cb),flow=flow,required=2*len(A)))
        if max(flows)<2*len(A):blocked.append(x)
        if x in inside:assert x in blocked
    if key.startswith('minimal_blocked'):assert set(blocked)&Z
    out.append(dict(kind=key,source=d,boundary_colours=signs,blocked_vertices=blocked,flow_checks=checks,black_faces=B,white_faces=W))
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps([{k:v for k,v in z.items() if k not in ('source','black_faces','white_faces')} for z in out],indent=2))
