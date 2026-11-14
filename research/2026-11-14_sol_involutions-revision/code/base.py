"""Independent Li maps. Uses the existing census generator only as input.
Run: python research/2026-11-14_sol_li-completion/verify.py 14
"""
import sys, json, math, time
from pathlib import Path
from itertools import combinations
from collections import Counter
import networkx as nx
import sympy as sp
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/2026-11-14_fable_route-combinatorics/lab'))
from tri import enumerate_classes, from_code, Tri

class Check:
    def __init__(self, faces, root):
        self.f=faces; self.root=root
        self.side={(u,v):i for i,f in enumerate(faces) for u,v in zip(f,f[1:]+f[:1])}
        dual=nx.Graph((i,self.side[v,u]) for (u,v),i in self.side.items())
        col=nx.bipartite.color(dual)
        self.a=sorted(i for i in dual if col[i]==col[root] and i!=root)
        self.w=sorted(i for i in dual if col[i]!=col[root])
        self.roots=set(faces[root]); self.x=sorted(set(sum((list(f) for f in faces),[]))-self.roots)
        self.n=len(self.x); assert self.n==len(self.a)
        self.g=nx.Graph(list(self.side))
        fixed=dict(zip(faces[root],[(0,0),(100,0),(0,100)]))
        lap=sp.Matrix([[self.g.degree(u) if u==v else -int(self.g.has_edge(u,v)) for v in self.x] for u in self.x])
        rhs=sp.Matrix([[sum(fixed[v][k] for v in self.g[u] if v in fixed) for k in (0,1)] for u in self.x])
        sol=lap.inv()*rhs
        pos=fixed|{u:tuple(sol[i,k] for k in (0,1)) for i,u in enumerate(self.x)}
        cen={t:tuple(sum(pos[v][k] for v in f)/3 for k in (0,1)) for t,f in enumerate(faces) if t!=root}
        for shear in range(1,10000):
            p={v:(z[0]+shear*z[1],z[1]) for v,z in pos.items()}
            c={t:(z[0]+shear*z[1],z[1]) for t,z in cen.items()}
            if all(c[w][0]!=z[0] for w in self.w for z in list(p.values())+[c[t] for t in self.a]): break
        else: raise AssertionError('general position')
        self.pos=p; self.cen=c
        # Orient delta by actual embedding, independently of input orientation.
        t=self.a[0]; u,v,z=faces[t]
        cross=(p[v][0]-p[u][0])*(p[z][1]-p[u][1])-(p[v][1]-p[u][1])*(p[z][0]-p[u][0])
        self.orientation=1 if cross>0 else -1
        def rec(i,used,s):
            if i==len(self.a): yield tuple(s); return
            for v in sorted(set(faces[self.a[i]])&set(self.x)-used): yield from rec(i+1,used|{v},s+[v])
        self.states=list(rec(0,set(),[]))
        self.pairs=[(r,s) for r in self.states for s in self.states if all(u!=v for u,v in zip(r,s))]
        self.cache={}

    def data(self,p):
        if p in self.cache:return self.cache[p]
        r,s=p; perm=dict(zip(r,s)); face=dict(zip(r,range(self.n))); remaining=set(r); cs=[]
        while remaining:
            v=min(remaining); c=[]
            while v in remaining: remaining.remove(v); c.append(face[v]); v=perm[v]
            cs.append(tuple(sorted(c)))
        cs.sort()
        q=nx.Graph(); q.add_nodes_from(self.g)
        for i,t in enumerate(self.a):
            u,v=set(self.f[t])-{s[i]}; q.add_edge(u,v,i=i)
        qs=sorted(tuple(sorted(q[u][v]['i'] for u,v in zip(c,c[1:]+c[:1]))) for c in nx.cycle_basis(q))
        delta=lambda u,v:self.orientation*(1 if self.side[u,v] in self.a+[self.root] else -1)
        J=sum(delta(u,v) for u,v in zip(r,s))//3
        assert all(abs(sum(delta(r[i],s[i]) for i in c))==3 for c in cs)
        hits={}
        for c in cs:
            for w in self.w:
                wx,wy=self.cen[w]; h=[]
                for i in c:
                    ax,ay=self.cen[self.a[i]]
                    for k,state in enumerate(p):
                        bx,by=self.pos[state[i]]
                        if min(ax,bx)<wx<max(ax,bx):
                            y=ay+(by-ay)*(wx-ax)/(bx-ax)
                            if y>wy:h.append((y,i,k))
                hits[c,w]=tuple(sorted(h))
        val=(tuple(cs),tuple(qs),J,hits);self.cache[p]=val;return val

    def swap(self,p,c,both=True):
        r,s=map(list,p)
        for i in c:
            if both:r[i],s[i]=s[i],r[i]
            else:r[i]=next(iter(set(self.f[self.a[i]])-{r[i],s[i]}))
        return tuple(r),tuple(s)

    def sign(self,o):
        p,M=o; J=self.data(p)[2]
        return (-1)**(J//2+sum(int(bool(self.pos[p[1][i]][0]<self.cen[self.a[i]][0])) for w,i in M))

    def one(self,o):
        p,M=o; qs=self.data(p)[1]
        return (self.swap(p,qs[0],False),M) if qs else o

    def two(self,o):
        p,M=o; cs,_,_,hits=self.data(p)
        empty=next((c for c in cs if not any(i in c for w,i in M)),None)
        if empty is not None:return self.swap(p,empty),M
        assert len(cs)==len(M)
        entries=[]
        for c in cs:
            w,i=next((w,i) for w,i in M if i in c);h=hits[c,w]
            j=next(j for j,(_,ii,k) in enumerate(h) if ii==i and k==1)
            entries.append((c,w,i,h,j))
        e=next((e for e in entries if len(e[3])%2==0),None)
        if e is None:e=next((e for e in entries if e[4]>0),None)
        if e is None:return o
        c,w,i,h,j=e
        jj=j^1 if len(h)%2==0 else ((j-1)^1)+1
        _,ii,k=h[jj]; MM=tuple(sorted((set(M)-{(w,i)})|{(w,ii)}))
        return (self.swap(p,c) if k==0 else p),MM

    def objects(self,m):
        for p in self.pairs:
            cs,_,_,h=self.data(p)
            pool=sorted((w,i) for c in cs for w in self.w for _,i,k in h[c,w] if k==1)
            yield from ((p,M) for M in combinations(pool,m))

    def run(self,listing=False):
        if not self.pairs:return dict(states=len(self.states),pairs=0)
        m=min(len(self.data(p)[0]) for p in self.pairs)
        objs=list(self.objects(m)); objset=set(objs); fixed=[]; sf=0; count=0; rows=[]
        index={o:i for i,o in enumerate(objs)}
        for o in objs:
            a,b=self.one(o),self.two(o)
            assert a in objset and b in objset
            assert self.one(a)==o and self.two(b)==o
            assert a==o or self.sign(a)==-self.sign(o)
            assert b==o or self.sign(b)==-self.sign(o)
            assert (a==o)==(not self.data(o[0])[1])
            if b==o:fixed.append(o);assert self.sign(o)==(-1)**(m//2)
            sf+=self.sign(o);count+=1
            if listing:rows.append(dict(id=index[o],pair=o[0],marks=o[1],sign=self.sign(o),iota1=index[a],iota2=index[b]))
        # Independent coefficient via signed powers of total signed ray counts.
        moments=[]
        for j in range(m+1):
            total=0
            for p in self.pairs:
                cs,_,J,h=self.data(p)
                height=sum((1 if self.pos[p[1][i]][0]>self.cen[self.a[i]][0] else -1) for c in cs for w in self.w for _,i,k in h[c,w] if k==1)
                total+=(-1)**((self.n+J)//2)*height**j
            moments.append(total)
        assert moments[:m]==[0]*m
        # ray sign differs from epsilon by a constant depending only on n.
        phase=(-1)**((self.n+1)//2)
        assert moments[m]==phase*sf*math.factorial(m)
        # Area product from odd crossing parity, independently of maps.
        covers={}
        for p in self.pairs:
            cs,_,_,h=self.data(p)
            key=tuple(sorted(tuple(sorted((self.a[i],min(p[0][i],p[1][i]),max(p[0][i],p[1][i])) for i in c)) for c in cs))
            if len(cs)==m:covers[key]=math.prod(sum(len(h[c,w])%2 for w in self.w) for c in cs)
        assert len(fixed)==sum(covers.values()) and fixed
        lengths=[]
        for start in fixed:
            o=start;visited=set();steps=0
            while True:
                assert o not in visited;visited.add(o)
                q=self.one(o)
                if q==o:break
                steps+=1;o=q;q=self.two(o)
                assert q!=o
                steps+=1;o=q
            lengths.append(steps)
        result=dict(states=len(self.states),pairs=len(self.pairs),m=m,objects=count,fixed2=len(fixed),signed_count=sf,lowest_coefficient=moments[m]//math.factorial(m),walk_hist=dict(Counter(lengths)),max_walk=max(lengths))
        if listing:(OUT/'running-objects.json').write_text(json.dumps(rows,indent=2));(OUT/'running-geometry.json').write_text(json.dumps(dict(pos={str(k):list(map(str,v)) for k,v in self.pos.items()},centers={str(k):list(map(str,v)) for k,v in self.cen.items()}),indent=2))
        return result

