"""Exact 3-port Hamiltonian transfer for the specified white-last stack."""
from families import *
from itertools import combinations
import json

def cycles(b):
    out=[];es=list(b.G.edges())
    def rec(left,match):
        if not left:
            h=b.G.copy();h.remove_edges_from(match)
            if nx.is_connected(h):out.append({e for e,d in b.dual_edges.items() if d in match or d[::-1] in match})
            return
        v=min(left)
        for w in b.G[v]:
            if w in left:rec(left-{v,w},match+[tuple(sorted((v,w)))])
    rec(set(b.G),[]);return out

def triangle_edges(f):return [tuple(sorted(e)) for e in zip(f,f[1:]+f[:1])]

base=tube(6,0);bb=Instance(base);local=cycles(bb);g=base;root=set(bb.faces[0]);records=[]
host=bb;exit=host.white[-1];hes=triangle_edges(host.faces[exit]);vec=[sum(e in c for c in local) for e in hes]
for q in range(2,9):
    incoming=host.faces[exit];mapping=dict(zip(bb.faces[0],incoming));nxt=max(g)+1
    for v in base:
        if v not in mapping:mapping[v]=nxt;nxt+=1
    oldes=triangle_edges(incoming)
    inv={v:k for k,v in mapping.items()}
    inlocal=[tuple(sorted((inv[a],inv[b]))) for a,b in oldes]
    invector=[sum(e in c for c in local) for e in inlocal]
    total=sum(x*y for x,y in zip(vec,invector))
    g=glue_triangles(g,base,exit,0);b0=Instance(g);host=Instance(g,next(i for i,f in enumerate(b0.faces) if set(f)==root));exit=host.white[-1]
    outes=triangle_edges(host.faces[exit]);assert all(v in inv for e in outes for v in e)
    outlocal=[tuple(sorted((inv[a],inv[b]))) for a,b in outes]
    matrix=[[sum(e in c and f in c for c in local) for f in outlocal] for e in inlocal]
    newvec=[sum(vec[i]*matrix[i][j] for i in range(3)) for j in range(3)]
    records.append({'q':q,'incoming_vector':vec,'incoming_local_edges':inlocal,'outgoing_local_edges':outlocal,'matrix':matrix,'HC':total,'outgoing_vector':newvec})
    vec=newvec
print(json.dumps(records,indent=2))
(Path(__file__).resolve().parents[1]/'data'/'stack-HC-transfer.json').write_text(json.dumps({'base_cycles_as_avoided_dual_edges':[sorted(c) for c in local],'steps':records},indent=2))
