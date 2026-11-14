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
(OUT/'checks.json').write_text(json.dumps(result,indent=2));print(result)
