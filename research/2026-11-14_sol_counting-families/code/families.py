"""Explicit families. Imports the lab read-only; all generated files stay here."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'workings/barnette_lab'))
import networkx as nx
from barnette_lab.core import Instance, dual_graph, glue_triangles

def tube(p,L):
    """p even, L>=0: L+1 p-cycles, alternating diagonals, two poles."""
    assert p>=4 and p%2==0 and L>=0
    g=nx.Graph()
    for j in range(L+1):
        for i in range(p): g.add_edge(j*p+i,j*p+(i+1)%p)
    for j in range(L):
        for i in range(p):
            g.add_edge(j*p+i,(j+1)*p+i)
            a,b=(i,(i+1)%p) if i%2==0 else ((i+1)%p,i)
            g.add_edge(j*p+a,(j+1)*p+b)
    g.add_edges_from(((L+1)*p,i) for i in range(p))
    g.add_edges_from(((L+1)*p+1,L*p+i) for i in range(p))
    return g

def subdivide(g):
    b=Instance(g); h=nx.Graph(); mids={}
    for u,v in g.edges(): mids[tuple(sorted((u,v)))]=len(g)+len(mids)
    for f in b.faces:
        a,c,d=f
        x=mids[tuple(sorted((a,c)))]; y=mids[tuple(sorted((c,d)))]; z=mids[tuple(sorted((d,a)))]
        for tri in ((a,x,z),(c,y,x),(d,z,y),(x,y,z)):
            h.add_edges_from(zip(tri,tri[1:]+tri[:1]))
    return h

def stack(p,q):
    base=tube(p,0); g=base.copy(); roots=set(Instance(g).faces[0])
    for _ in range(q-1):
        b0=Instance(g); k=next(i for i,f in enumerate(b0.faces) if set(f)==roots)
        b=Instance(g,k); g=glue_triangles(g,base,b.white[-1],0)
    b=Instance(g)
    return Instance(g,next(i for i,f in enumerate(b.faces) if set(f)==roots))
