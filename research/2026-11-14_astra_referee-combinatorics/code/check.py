"""Independent referee implementation. No imports from the author's lab.

Run from repository root: py -3.14 -B research/2026-11-14_astra_referee-combinatorics/code/check.py --max 12
"""
from pathlib import Path
from collections import defaultdict, Counter, deque
from itertools import combinations_with_replacement, permutations
import argparse, ast, hashlib, json, math, subprocess, sys, time
import networkx as nx
import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
EXE = REPO / 'workings/barnette_lab/vendor/plantri.exe'
AUTHOR = REPO / 'research/2026-11-14_fable_route-combinatorics'

def edge(a,b): return tuple(sorted((a,b)))
def arcs(c): return list(zip(c,c[1:]+c[:1]))
def pm(g):
    if not g:
        yield ()
        return
    v = min(g, key=lambda x: (g.degree(x),x))
    for u in sorted(g[v]):
        h=g.copy(); h.remove_nodes_from((u,v))
        for m in pm(h): yield (edge(u,v),)+m

class Map:
    def __init__(self, faces):
        self.faces = [tuple(f) for f in faces]
        self.side = {ab:i for i,f in enumerate(self.faces) for ab in arcs(f)}
        self.T=nx.Graph(); self.T.add_edges_from(self.side)
        assert all(len(f)==3 for f in self.faces)
        assert all(self.side[a,b]!=self.side[b,a] for a,b in self.T.edges())
        assert self.T.number_of_edges()==3*len(self.T)-6
        assert all(d%2==0 for _,d in self.T.degree())
        self.G=nx.Graph(); self.G.add_nodes_from(range(len(faces)))
        self.dual={edge(a,b):edge(self.side[a,b],self.side[b,a]) for a,b in self.T.edges()}
        self.G.add_edges_from(self.dual.values())
        self.fc=nx.bipartite.color(self.G)
        self.hcs=[]
        for m in pm(self.G):
            h=self.G.copy(); h.remove_edges_from(m)
            if nx.is_connected(h):
                self.hcs.append(frozenset(e for e,d in self.dual.items() if d in m))

class Root:
    def __init__(self, M, outer):
        self.M=M; self.o=outer; self.R=set(M.faces[outer])
        self.X=sorted(set(M.T)-self.R)
        self.black={f for f in M.G if M.fc[f]==M.fc[outer]}
        self.white=set(M.G)-self.black; self.A=sorted(self.black-{outer}); self.n=len(self.A)
        self.inner=sorted(self.white-set(M.G[outer]))
        assert len(self.inner)==self.n-2
        self.ss=[]
        def search(i,s,used):
            if i==self.n: self.ss.append(tuple(s)); return
            for v in sorted(set(M.faces[self.A[i]])-self.R-used):
                search(i+1,s+[v],used|{v})
        search(0,[],set())
        self.pp=[(r,s) for r in self.ss for s in self.ss if all(a!=b for a,b in zip(r,s))]
        self.partners={s:[r for r,t in self.pp if t==s] for s in self.ss}
        self.qq={s:self.Q(s) for s in self.ss}
        self.tm=[s for s in self.ss if nx.is_forest(self.qq[s]) and self.partners[s]]
        self.hs=self.heights()
        self.rank={s:sum(self.hs[s]) for s in self.ss}
        self.groups=defaultdict(list)
        for r,s in self.pp: self.groups[tuple(sorted(edge(a,b) for a,b in zip(r,s)))].append((r,s))
        self.m=min((len(self.cycles(r,s)) for r,s in self.pp),default=None)

    def delta(self,a,b): return 1 if self.M.side[a,b] in self.black else -1
    def eps(self,r,s):
        d=sum(self.delta(a,b) for a,b in zip(r,s)); assert d%3==0
        j=d//3; assert (self.n+j)%2==0
        return (-1)**((self.n+j)//2)
    def Q(self,s):
        q=nx.Graph(); q.add_nodes_from(self.M.T)
        for t,v in zip(self.A,s):
            a,b=set(self.M.faces[t])-{v}; q.add_edge(a,b,t=t)
        return q
    def cycles(self,r,s):
        nxt=dict(zip(r,s)); unused=set(r); out=[]
        while unused:
            c=[]; v=min(unused)
            while v not in c: c.append(v); unused.remove(v); v=nxt[v]
            assert v==c[0] and len(c)>=3
            out.append(c)
        return out
    def disk(self,c):
        g=self.M.G.copy(); g.remove_edges_from(self.M.dual[edge(a,b)] for a,b in arcs(c))
        outside=nx.node_connected_component(g,self.o)
        inside=set(g)-outside
        assert len(list(nx.connected_components(g)))==2
        ccw=self.M.side[c[0],c[1]] in inside
        return inside,ccw
    def disk_check(self,c):
        ins,ccw=self.disk(c); B=len(ins&self.black); W=len(ins&self.white)
        ell=sum((self.M.side[a,b] if self.M.side[a,b] in self.black else self.M.side[b,a]) in ins for a,b in arcs(c))
        assert W==B+1 and len(c)-2*ell==3
        assert sum(self.delta(a,b) for a,b in arcs(c))==(-3 if ccw else 3)
        assert W>0 and ins&self.white<=set(self.inner)
        return ins&self.white,ccw
    def heights(self):
        # Full spoke dual has white faces as vertices. Removing the outer
        # black center merges its three neighbouring white faces into OUT.
        boundary=set(self.M.G[self.o]); OUT=-1
        adj=defaultdict(list)
        for t in self.A:
            f=self.M.faces[t]
            for i,v in enumerate(f):
                left=self.M.side[f[(i+1)%3],v]
                right=self.M.side[v,f[(i-1)%3]]
                left=OUT if left in boundary else left
                right=OUT if right in boundary else right
                adj[left].append((right,(t,v),1)); adj[right].append((left,(t,v),-1))
        ks=[]
        for w in self.inner:
            prev={w:None}; todo=deque([w])
            while OUT not in prev:
                u=todo.popleft()
                for v,spoke,sgn in sorted(adj[u]):
                    if v not in prev: prev[v]=(u,spoke,sgn); todo.append(v)
            k=Counter(); v=OUT
            while prev[v] is not None:
                u,spoke,sgn=prev[v]; k[spoke]+=sgn; v=u
            ks.append(k)
        self.ks=ks
        return {s:tuple(sum(k[t,v] for t,v in zip(self.A,s)) for k in ks) for s in self.ss}

    def check(self, thorough=True):
        counts=Counter(roots=1,states=len(self.ss),pairs=len(self.pp),tree_matchings=len(self.tm),hc=len(self.M.hcs))
        # Propagate vertex colours using delta, independently of any geometric winding.
        col={min(self.M.T):0}; todo=deque(col)
        while todo:
            a=todo.popleft()
            for b in self.M.T[a]:
                x=(col[a]+self.delta(a,b))%3
                if b not in col: col[b]=x; todo.append(b)
                assert col[b]==x
        sigs={(-1)**sum(s[i]>s[j] for i in range(self.n) for j in range(i+1,self.n)) for s in self.ss}
        assert len(sigs)==1; sigma=next(iter(sigs))
        z=np.exp(1j*np.pi/6); om=np.exp(2j*np.pi/3)
        for s in self.ss:
            q=self.qq[s]; mu=sum(self.eps(r,s) for r in self.partners[s])
            assert mu==(self.eps(self.partners[s][0],s) if s in self.tm else 0)
            N=np.zeros((self.n,self.n),dtype=complex); d=np.zeros((self.n,self.n),dtype=int); rho=[]
            for i,(t,v) in enumerate(zip(self.A,s)):
                a,b=sorted(set(self.M.faces[t])-{v},key=lambda x:(col[x]-col[v])%3)
                rho.append(z**self.delta(a,v)*om**col[a])
                for x,sgn in ((a,1),(b,-1)):
                    if x in self.X:
                        j=self.X.index(x); d[i,j]=sgn; N[i,j]=z**self.delta(x,v)
            assert np.max(np.abs(N@np.diag([om**col[x] for x in self.X])-np.diag(rho)@d))<1e-10
            detd=int(sp.det(sp.Matrix(d.tolist())))
            detN=np.linalg.det(N)
            partner_sum=sum((1j)**(sum(self.delta(a,b) for a,b in zip(r,s))//3) for r in self.partners[s])
            assert abs(sigma*detN-partner_sum)<1e-8
            assert abs(detd)==int(s in self.tm)
            counts['determinants']+=1
            if self.partners[s]:
                k=len(nx.cycle_basis(q)); assert len(self.partners[s])==2**k
                for r in self.partners[s]:
                    tails={edge(a,next(iter(set(self.M.faces[t])-{a,b}))):a for t,a,b in zip(self.A,r,s)}
                    for c in nx.cycle_basis(q):
                        if tails[edge(c[0],c[1])]!=c[0]: c=list(reversed(c))
                        assert all(tails[edge(a,b)]==a for a,b in arcs(c))
                        self.disk_check(c); counts['Q_cycles']+=1
        for r,s in self.pp:
            cs=self.cycles(r,s); total=0
            for c in cs:
                inside,ccw=self.disk_check(c); total+=-1 if ccw else 1
                inds=[i for i,(a,b) in enumerate(zip(r,s)) if a in c]
                rr=list(r); ss=list(s)
                for i in inds: rr[i],ss[i]=ss[i],rr[i]
                rr,ss=tuple(rr),tuple(ss); assert (rr,ss) in self.pp
                expected=tuple((1 if ccw else -1)*int(w in inside) for w in self.inner)
                assert tuple(a-b for a,b in zip(self.hs[s],self.hs[ss]))==expected
                assert self.rank[s]-self.rank[ss]==(1 if ccw else -1)*len(inside)
                assert self.eps(rr,ss)==-self.eps(r,s)
                counts['D_cycles']+=1
            assert sum(self.delta(a,b) for a,b in zip(r,s))==3*total
        if self.pp:
            assert len(self.tm)>=2*self.m and len(self.tm)>=2**self.m
            for j in range(self.m+1):
                for ws in combinations_with_replacement(range(len(self.inner)),j):
                    lhs=sum(self.eps(self.partners[s][0],s)*math.prod(self.hs[s][w] for w in ws) for s in self.tm)
                    rhs=0
                    if j==self.m:
                        for group in self.groups.values():
                            cs=self.cycles(*group[0])
                            if len(cs)!=self.m: continue
                            interiors=[self.disk(c)[0] for c in cs]
                            rhs+=sum(all(self.inner[w] in interiors[k] for w,k in zip(ws,p)) for p in permutations(range(j)))
                        rhs*=(-1)**((self.n-self.m)//2)
                    assert lhs==rhs,('B',j,ws,lhs,rhs)
                    counts['height_monomials']+=1
        # Enumerated independently as complements of all dual perfect matchings.
        inverse_counts={e:Counter() for e in map(lambda ab:edge(*ab),arcs(self.M.faces[self.o]))}
        for P in self.M.hcs:
            e0=next(e for e in P if set(e)<=self.R)
            p=nx.Graph(); p.add_nodes_from(self.M.T); p.add_edges_from(P-{e0})
            assert nx.is_forest(p)
            tail={}
            for component in nx.connected_components(p):
                roots=component&self.R; assert len(roots)==1
                for parent,child in nx.bfs_edges(p,next(iter(roots))): tail[edge(parent,child)]=child
            s=tuple(tail[next(e for e in P if self.M.dual[e][0]==t or self.M.dual[e][1]==t)] for t in self.A)
            assert s in self.ss
            assert not self.partners[s] or s in self.tm
            inverse_counts[e0][s]+=1; counts['HC_states']+=1
        for e0,tab in inverse_counts.items():
            assert all(tab[s]==1 for s in self.tm)
            counts['nonimage_HC_states']+=sum(v for s,v in tab.items() if s not in self.tm)
        assert 3*len(self.tm)<=len(self.M.hcs)
        self.inverse_counts=inverse_counts
        return counts

def planar_faces(g):
    ok,emb=nx.check_planarity(g); assert ok
    seen=set(); fs=[]
    for a,b in emb.edges():
        if (a,b) not in seen: fs.append(tuple(emb.traverse_face(a,b,seen)))
    return fs

def generated(v):
    run=subprocess.run([str(EXE),'-ba',str(v)],capture_output=True,text=True,check=True,timeout=120)
    for line in run.stdout.splitlines():
        n,data=line.split(); g=nx.Graph()
        for a,ns in enumerate(data.split(',')):
            g.add_edges_from((a,ord(b)-97) for b in ns)
        assert len(g)==int(n)
        yield Map(planar_faces(g))

def witness(R):
    partnered=[s for s in R.ss if R.partners[s]]
    if not partnered:return {}
    high=max(R.rank[s] for s in partnered); low=min(R.rank[s] for s in partnered)
    gap=max(R.rank[s]-R.rank[r] for r,s in R.pp)
    def pack(s):return {'s':s,'rank':R.rank[s],'Q_cycles':nx.cycle_basis(R.qq[s])}
    out={'states':len(R.ss),'pairs':len(R.pp),'TM':len(R.tm),'cmin':R.m,
         'top_bad':[pack(s) for s in partnered if R.rank[s]==high and s not in R.tm],
         'bottom_bad':[pack(s) for s in partnered if R.rank[s]==low and s not in R.tm],
         'max_gap_bad':[{'r':r,**pack(s)} for r,s in R.pp if R.rank[s]-R.rank[r]==gap and s not in R.tm],
         'ccw_min_bad':[],'cw_min_bad':[],'bad_covers':[],
         'rank_signs':sorted((R.rank[s],R.eps(R.partners[s][0],s)) for s in R.tm)}
    for key,group in R.groups.items():
        if all(s not in R.tm for r,s in group): out['bad_covers'].append({'edges':key,'states':[pack(s) for r,s in group]})
        for r,s in group:
            cs=R.cycles(r,s)
            if len(cs)==R.m and s not in R.tm:
                turns=[R.disk(c)[1] for c in cs]
                if all(turns):out['ccw_min_bad'].append(pack(s))
                if not any(turns):out['cw_min_bad'].append(pack(s))
    out['rank_parity_bad']=len({sgn*(-1)**rk for rk,sgn in out['rank_signs']})>1
    out['top_unpartnered']=any(not R.partners[s] for s in R.ss if R.rank[s]==max(R.rank.values()))
    z=sp.Symbol('z'); base=min(R.rank[s] for s in R.tm)
    poly=sum(R.eps(R.partners[s][0],s)*z**(R.rank[s]-base) for s in R.tm)
    quo,rem=sp.div(poly,(z-1)**R.m); assert rem==0
    out['Z_shifted']=str(sp.expand(poly)); out['quotient']=str(quo)
    co=sp.Poly(quo,z).all_coeffs(); out['quotient_mixed']=bool(min(co)<0<max(co))
    out['HC_noninjective']=any(any(v>1 for v in tab.values()) for tab in R.inverse_counts.values())
    return out

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--max',type=int,default=12); ap.add_argument('--examples',action='store_true'); a=ap.parse_args()
    start=time.time(); totals=Counter(); rows=[]; witnesses={}; classes={}
    if a.examples:
        lines=(AUTHOR/'data/counterexamples.txt').read_text().splitlines()
        maps=[]
        for i,line in enumerate(lines):
            if line.startswith('   [('):
                fs=ast.literal_eval(line.strip()); root=int(lines[i+1].split('face ')[1].split()[0]); maps.append((Map(fs),root))
        for i,(M,o) in enumerate(maps):
            R=Root(M,o); counts=R.check(); totals.update(counts)
            witnesses[str(i)]={'faces':M.faces,'root':o,'results':witness(R)}
        name='examples'
    else:
        for v in range(6,a.max+1):
            maps=list(generated(v)); classes[v]=len(maps)
            for ci,M in enumerate(maps):
                for o in range(len(M.faces)):
                    R=Root(M,o); counts=R.check(); totals.update(counts)
                    rows.append({'V':v,'class':ci,'root':o,**dict(counts),'cmin':R.m})
                    w=witness(R)
                    for key in ('top_bad','bottom_bad','max_gap_bad','ccw_min_bad','cw_min_bad','bad_covers','rank_parity_bad','top_unpartnered','quotient_mixed','HC_noninjective'):
                        if w.get(key) and key not in witnesses:witnesses[key]={'faces':M.faces,'root':o,'results':w}
                    if R.m and R.m>1 and 'cmin_gt_one' not in witnesses:witnesses['cmin_gt_one']={'faces':M.faces,'root':o,'results':w}
            print(v,len(maps),dict(totals),flush=True)
        name=f'up_to_{a.max}'
    output={'command':' '.join(sys.argv),'python':sys.version,'seconds':time.time()-start,'plantri_sha256':hashlib.sha256(EXE.read_bytes()).hexdigest(),'classes':classes,'totals':dict(totals),'rows':rows,'witnesses':witnesses}
    (HERE/(name+'.json')).write_text(json.dumps(output,indent=2))
    print(name,dict(totals),'seconds',output['seconds'],flush=True)

if __name__=='__main__': main()
