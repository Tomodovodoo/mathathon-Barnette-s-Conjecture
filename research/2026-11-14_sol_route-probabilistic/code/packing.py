"""Test half-pair via explicit partition into two trees. Positive certificates checked directly."""
from explore import *
from barnette_lab.core import glue_triangles

def partition(b,r,s):
    used={(t,v) for t,v in zip(b.A,r)}|{(t,v) for t,v in zip(b.A,s)}
    es=[e for e in white_edges(b) if e[:2] in used];color={}
    assert len(es)==2*b.n
    def forest(c):
        h=nx.Graph();h.add_nodes_from(b.white)
        for i,d in color.items():
            if d==c:h.add_edge(es[i][2],es[i][3],idx=i)
        return h
    for start in range(len(es)):
        queue=[start];parent={start:None};terminal=None;F=[forest(0),forest(1)]
        for e in queue:
            u,v=es[e][2:]
            for c in (0,1):
                if color.get(e)==c:continue
                if not nx.has_path(F[c],u,v):terminal=(e,c);break
                path=nx.shortest_path(F[c],u,v)
                for a,d in zip(path,path[1:]):
                    f=F[c][a][d]['idx']
                    if f not in parent:parent[f]=(e,c);queue.append(f)
            if terminal:break
        if terminal is None:return {'pass':False,'failed_edge':start,'reached':list(parent),'edges':es}
        e,c=terminal
        while True:
            color[e]=c
            if parent[e] is None:break
            e,c=parent[e]
    # Parallel edges are retained by IDs; independent verification uses MultiGraph.
    for c in (0,1):
        h=nx.MultiGraph();h.add_nodes_from(b.white);h.add_edges_from(es[i][2:] for i in color if color[i]==c)
        assert nx.is_tree(h)
    return {'pass':True,'edges':es,'colors':[color[i] for i in range(len(es))]}

rng=random.Random(48014);cases=[]
for p in (4,6,8,10):
    for L in (2,5,10):cases.append((f'tube{p}_{L}',Instance(tube(p,L))))
for p in (4,6):cases.append((f'subdiv{p}',Instance(subdivide(tube(p,2)))))
for q in (5,10,20):cases.append((f'chain{q}',stack(6,q)))
for rep in range(10):
    b=Instance(nx.octahedral_graph());root=b.R
    for j in range(20):
        g=glue_triangles(b.T,dual_graph(nx.circular_ladder_graph(rng.choice((4,6,8)))),rng.choice(b.white),0)
        bb=Instance(g);b=Instance(g,next(i for i,f in enumerate(bb.faces) if set(f)==root))
    cases.append((f'random_sum{rep}',b))
rows=[]
for name,b in cases:
    deadline();p=b.flow_pair();ans=partition(b,*p)
    rows.append({'name':name,'V':len(b.T),'triangulation_edges':list(b.T.edges()),'outer':b.outer,'pair':p,**ans})
    print(name,len(b.T),ans['pass'],flush=True)
(OUT/'data/packing.json').write_text(json.dumps({'seed':48014,'rows':rows,'seconds':time.monotonic()-START},indent=2))
