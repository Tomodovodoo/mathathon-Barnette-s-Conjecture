"""Independent small checks: permutation states, DSU forests, path DFS cycles."""
import sys,json,itertools
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'workings/barnette_lab'))
from barnette_lab.core import Instance
import networkx as nx
OUT=Path(__file__).resolve().parents[1]
d=json.loads((OUT/'counts.json').read_text()); checked=0; cycles=0
for row in d['graphs']:
    if row['vertices']>10:continue
    t=nx.Graph();t.add_edges_from(row['edges'])
    faces=Instance(t).faces
    remap={rr['outer']:next(i for i,f in enumerate(faces) if set(f)==set(rr['root'])) for rr in row['roots']}
    for rr in row['roots']:
        b=Instance(t,remap[rr['outer']]); trees=states=0
        for s in itertools.permutations(b.X):
            if not all(v in b.faces[f] for f,v in zip(b.A,s)):continue
            states+=1
            parent={v:v for v in t};rho=min(b.R)
            for v in b.R:parent[v]=rho
            def find(v):
                while parent[v]!=v:v=parent[v]
                return v
            good=True
            for f,v in zip(b.A,s):
                u,w=set(b.faces[f])-{v};a,z=find(u),find(w)
                if a==z:good=False;break
                parent[a]=z
            trees+=good
        assert trees==rr['trees'] and states==rr['states'];checked+=1
    g=Instance(t).G; start=min(g); counts=[]
    def walk(path,used):
        if len(path)==len(g):
            if g.has_edge(path[-1],start) and path[1]<path[-1]:
                counts.append(set(tuple(sorted(e)) for e in zip(path,path[1:]+path[:1])))
            return
        for v in g[path[-1]]:
            if v not in used:walk(path+[v],used|{v})
    walk([start],{start})
    assert len(counts)==row['primal']['hamilton']
    for e,a in row['primal']['avoidance']:
        ee=tuple(sorted(remap[v] for v in e))
        assert sum(ee not in c for c in counts)==a
    cycles+=1
result=dict(roots_independent_permutations_DSU=checked,graphs_independent_path_DFS=cycles,
            note='Author-written second implementation, not an independent referee or code certification')
if (OUT/'gauges.json').exists():
    cert=json.loads((OUT/'gauges.json').read_text())['first']
    row=next(g for g in d['graphs'] if g['name']==cert['graph'])
    t=nx.Graph();t.add_edges_from(row['edges']); fs=Instance(t).faces
    b=Instance(t,next(i for i,f in enumerate(fs) if set(f)==set(cert['root'])))
    faces=cert['faces_in_state_order']; witnesses=cert['witness']
    for w in witnesses:
        s=w['state'];assert set(s)==set(b.X)
        assert all(v in f for f,v in zip(faces,s))
        q=nx.Graph();q.add_nodes_from(t)
        for i,(f,v) in enumerate(zip(faces,s)):
            u,z=set(f)-{v};q.add_edge(u,z,index=i)
        assert q.number_of_edges()==len(faces)
        assert nx.is_forest(q)
        r=[None]*len(s)
        for comp in nx.connected_components(q):
            roots=set(comp)&b.R;assert len(roots)==1
            root=next(iter(roots))
            for parent,child in nx.bfs_edges(q,root):r[q[parent][child]['index']]=child
        assert set(r)==set(b.X)
        sign=1
        for u,v in zip(r,s):sign*=b.delta(u,v)
        assert sign==w['sign']
    assert sum(w['sign']==-1 for w in witnesses)%2
    assert all(sum(w['state'][i]==v for w in witnesses)%2==0 for i,f in enumerate(faces) for v in f)
    result['gauge_certificate_trees_and_signs_rebuilt']=len(witnesses)
(OUT/'checks.json').write_text(json.dumps(result,indent=2));print(result)
