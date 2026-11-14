"""Exact tests. Run from any cwd: python -B <this file>. Outputs ../data.json."""
import sys, json, random, math
from pathlib import Path
from collections import Counter
from itertools import product
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'workings/barnette_lab'))
from barnette_lab.core import Instance, named_graphs, glue_triangles, dual_graph
import networkx as nx
import sympy as sp
OUT=Path(__file__).resolve().parents[1]
def det(a):
    a=[list(r) for r in a]; n=len(a); sign=1; prev=1
    for k in range(n-1):
        if not a[k][k]:
            p=next((p for p in range(k+1,n) if a[p][k]),None)
            if p is None:return 0
            a[k],a[p]=a[p],a[k]; sign=-sign
        pivot=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):a[i][j]=(a[i][j]*pivot-a[i][k]*a[k][j])//prev
        for i in range(k+1,n):a[i][k]=0
        prev=pivot
    return sign*a[-1][-1] if n else 1

def matrices(b,q=2,lam=0):
    a=b.weights(); out=[]
    for t in b.A:
        out.append([[((lam if u==v else b.delta(u,v))*q**a.get((t,v),0)) if u in b.faces[t] and v in b.faces[t] else 0 for v in b.X] for u in b.X])
    return out

def mixed(ms):
    n=len(ms); total=0
    for mask in range(1<<n):
        a=[[sum(ms[t][i][j] for t in range(n) if mask>>t&1) for j in range(n)] for i in range(n)]
        total+=(-1)**(n-mask.bit_count())*det(a)
    return total

def trinity(b):
    color={v:i for i,v in enumerate(b.faces[b.outer])}
    while len(color)<len(b.T):
        for f in b.faces:
            known=[v for v in f if v in color]
            if len(known)==2:color[next(v for v in f if v not in color)]=next(iter({0,1,2}-{color[v] for v in known}))
    counts=[]
    for c in range(3):
        vs=[v for v in b.T if color[v]==c]; ix={v:i for i,v in enumerate(vs)}; l=[[0]*len(vs) for _ in vs]
        for t in b.black:
            v=next(v for v in b.faces[t] if color[v]==c); u,w=[u for u in b.faces[t] if u!=v]
            f=next(f for f in [b.sides[u,w],b.sides[w,u]] if f!=t)
            source=next(x for x in b.faces[f] if x not in (u,w))
            l[ix[v]][ix[v]]+=1;l[ix[v]][ix[source]]-=1
        root=next(v for v in b.R if color[v]==c); inds=[ix[v] for v in vs if v!=root]
        counts.append(det([[l[i][j] for j in inds] for i in inds]))
    return counts

def white_tau(b,restricted=False):
    ix={v:i for i,v in enumerate(b.white)}; l=[[0]*len(ix) for _ in ix]
    for t in (b.A if restricted else b.black):
        for v in b.faces[t]:
            if restricted and v not in b.X:continue
            sides=[]
            for u in b.faces[t]:
                if u!=v:sides.append(next(f for f in (b.sides[u,v],b.sides[v,u]) if f in ix))
            i,j=map(ix.get,sides);l[i][i]+=1;l[j][j]+=1;l[i][j]-=1;l[j][i]-=1
    return det([r[:-1] for r in l[:-1]])

def run(name,b,do_mixed=False):
    ss=list(b.states()); pairs=b.pairs(ss); a=b.weights(); omega=lambda s:sum(a.get((t,v),0) for t,v in zip(b.A,s))
    signs={s:(-1)**sum(s[i]>s[j] for i in range(b.n) for j in range(i+1,b.n)) for s in ss}
    assert len(set(signs.values()))==1 and abs(int(b.K.det()))==len(ss)
    poly=Counter(); treepoly=Counter(); groups={}; mate=Counter(s for r,s in pairs)
    for r,s in pairs:
        sg=math.prod(b.delta(u,v) for u,v in zip(r,s)); assert sg==b.sign(r,s)
        poly[omega(s)]+=sg
        if b.is_tree(s):treepoly[omega(s)]+=sg
        key=tuple(tuple(sorted((u,v))) for u,v in zip(r,s));groups[key]=(r,s)
    poly={k:v for k,v in sorted(poly.items()) if v};treepoly={k:v for k,v in treepoly.items() if v}
    assert poly==treepoly
    trees=sum(b.is_tree(s) for s in ss); assert trees==sum(mate[s]==1 for s in ss)
    m=min((len(b.dcycles(r,s)) for r,s in pairs),default=None)
    area=0
    if m is not None:
        for r,s in groups.values():
            cs=b.dcycles(r,s)
            if len(cs)!=m:continue
            area+=math.prod(abs(sum(a.get((t,s[b.A.index(t)]),0)-a.get((t,r[b.A.index(t)]),0) for t in c)) for c in cs)
        coeff=sum(v*math.comb(k,m) for k,v in poly.items())
        assert coeff==(-1)**((b.n-m)//2)*area
        assert all(sum(v*math.comb(k,j) for k,v in poly.items())==0 for j in range(m))
    else:coeff=0
    tr=trinity(b);assert tr==[len(ss)]*3
    out=dict(name=name,vertices=len(b.T),outer=b.outer,root_face=list(b.faces[b.outer]),edges=sorted(b.T.edges()),K=[list(map(int,b.K.row(i))) for i in range(b.n)],states=len(ss),pairs=len(pairs),trees=trees,trinity=tr,white_tau=white_tau(b),restricted_white_tau=white_tau(b,True),polynomial=poly,cmin=m,leading=coeff,area=area,tree_sign_sum=sum(treepoly.values()))
    if do_mixed:
        ms=matrices(b); direct=sum(v*2**k for k,v in poly.items());md=mixed(ms);assert md==direct
        naive=det([[sum(m[i][j] for m in ms) for j in range(b.n)] for i in range(b.n)])
        doubled=mixed(matrices(b,1,1));assert doubled==len(ss)
        out.update(mixed_q2=md,direct_q2=direct,naive_q2=naive,doubled_q1=doubled)
    print(name,len(b.T),len(ss),len(pairs),trees,m,coeff,flush=True)
    return out

if __name__=='__main__':
    cases=[(name,Instance.from_primal(g)) for name,g in named_graphs().items() if name!='truncated_cuboctahedron']
    rng=random.Random(14112026)
    for size in (8,9,10,11,12,13,14):
        base=nx.octahedral_graph() if size%3==0 else dual_graph(nx.circular_ladder_graph(6 if size%3==2 else 8))
        while len(base)<size:base=glue_triangles(base,nx.octahedral_graph(),rng.randrange(2*len(base)-4),0)
        for j in range(2):cases.append((f'random_{size}_{j}',Instance(base,rng.randrange(2*len(base)-4))))
    rows=[]
    for name,b in cases:
        rows.append(run(name,b,do_mixed=b.n<=8 or name=='truncated_octahedron'))
        (OUT/'data.json').write_text(json.dumps(rows,indent=2))

