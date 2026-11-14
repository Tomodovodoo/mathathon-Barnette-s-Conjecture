"""Small exact trinity Tutte/hypergraph comparisons and algebra checks."""
import sys,json,itertools,math
from pathlib import Path
from collections import Counter
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'workings/barnette_lab'))
from barnette_lab.core import Instance,plantri_graphs
import networkx as nx
import sympy as sp
OUT=Path(__file__).resolve().parents[1]

def colors(b):
    c=dict(zip(b.faces[0],range(3)))
    while len(c)<len(b.T):
        old=len(c)
        for f in b.faces:
            unknown=set(f)-c.keys()
            if len(unknown)==1:c[unknown.pop()]=({0,1,2}-{c[v] for v in f if v in c}).pop()
        assert len(c)>old
    return c

def hyper(g,part):
    vs=sorted(g); edges=sorted(g.edges()); hypertrees=set()
    for inds in itertools.combinations(range(len(edges)),len(vs)-1):
        h=nx.Graph();h.add_nodes_from(vs);h.add_edges_from(edges[i] for i in inds)
        if nx.is_tree(h):hypertrees.add(tuple(h.degree(v)-1 for v in part))
    interior=Counter();exterior=Counter()
    for f in hypertrees:
        ina=exa=0
        for i in range(len(part)):
            # Internal inactivity transfers from i to a smaller index.
            ina+=any(tuple(x-int(k==i)+int(k==j) for k,x in enumerate(f)) in hypertrees for j in range(i) if f[i]>0)
            exa+=any(tuple(x+int(k==i)-int(k==j) for k,x in enumerate(f)) in hypertrees for j in range(i) if f[j]>0)
        interior[ina]+=1;exterior[exa]+=1
    return dict(hypertrees=len(hypertrees),interior=dict(interior),exterior=dict(exterior))

rows=[]
for n in (6,8,9,10):
    for j,t in enumerate(plantri_graphs(n,ROOT/'workings/barnette_lab/vendor/plantri.exe')):
        b=Instance(t); c=colors(b); graphs=[]
        for missing in range(3):
            g=t.subgraph([v for v in t if c[v]!=missing]).copy()
            x,y=sp.symbols('x y');pol=nx.tutte_polynomial(g)
            graphs.append(dict(missing=missing,edges=sorted(g.edges()),tutte=str(pol),
                evaluations={str((a,z)):int(pol.subs({x:a,y:z})) for a,z in [(1,1),(1,2),(2,1),(0,-2),(0,0)]},
                hypergraphs=[hyper(g,sorted(v for v in g if c[v]==p)) for p in range(3) if p!=missing]))
        ss=list(b.states()); pairs=b.pairs(ss)
        weights={(t,v):1+(5*t+v)%7 for t in b.A for v in set(b.faces[t])&set(b.X)}
        # Wick expectation of two determinant expansions: only same-row cross contractions survive.
        wick=0;direct=0
        sign=lambda s:(-1)**sum(a>z for i,a in enumerate(s) for z in s[i+1:])
        for r in ss:
            for s in ss:
                term=math.prod(0 if u==v else b.delta(u,v)*weights[t,v] for t,u,v in zip(b.A,r,s))
                wick+=sign(r)*sign(s)*term
        for r,s in pairs:direct+=math.prod(b.delta(u,v)*weights[t,v] for t,u,v in zip(b.A,r,s))
        assert wick==direct
        rows.append(dict(name=f'plantri_{n}_{j}',states=len(ss),trees=sum(b.is_tree(s) for s in ss),
                         signed=0,wick=wick,trinity_graphs=graphs))
        print(rows[-1]['name'],[(g['evaluations']['(1, 1)'],[h['hypertrees'] for h in g['hypergraphs']]) for g in graphs],flush=True)
(OUT/'invariants.json').write_text(json.dumps(rows,indent=2))
