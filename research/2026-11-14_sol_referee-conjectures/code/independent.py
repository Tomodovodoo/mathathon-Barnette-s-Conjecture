"""Independent referee kernel. No imports from author or earlier referee code."""
import collections as co
import itertools as it
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parents[1] / 'data'

def facial_walks(rot):
    seen, faces, left = set(), [], {}
    for a in rot:
        for b in rot[a]:
            if (a,b) in seen: continue
            e, walk = (a,b), []
            while e not in seen:
                seen.add(e); left[e] = len(faces); walk.append(e[0])
                v,w = e
                e = (w, rot[w][(rot[w].index(v)-1) % len(rot[w])])
            assert e == (a,b)
            faces.append(tuple(walk))
    return faces,left

def rotation_from_faces(faces):
    succ = co.defaultdict(dict)
    for f in faces:
        for a,b,c in zip(f, f[1:]+f[:1], f[2:]+f[:2]): succ[a][b] = c
    rot = {}
    for a,d in succ.items():
        seq = [min(d)]
        while d[seq[-1]] != seq[0]: seq.append(d[seq[-1]])
        assert len(seq) == len(d)
        rot[a] = seq
    return rot

def parse_text(line):
    v = list(map(int,line.split())); n = v[0]; p = 1; rot = {}
    for a in range(n):
        k = v[p]; rot[a] = v[p+1:p+1+k]; p += k+1
    root = tuple(v[p:p+3]) if p < len(v) else None
    return rot,root

class Instance:
    def __init__(self, rot, root=None):
        self.rot = rot; self.N = len(rot)
        self.faces,self.left = facial_walks(rot)
        assert len(self.faces) == 2*self.N-4 and all(len(f)==3 for f in self.faces)
        self.rootid = 0 if root is None else next(i for i,f in enumerate(self.faces) if set(f)==set(root))
        self.R = set(self.faces[self.rootid]); self.X = set(rot)-self.R
        colors = {self.rootid:0}; todo = [self.rootid]
        for i in todo:
            f = self.faces[i]
            for a,b in zip(f,f[1:]+f[:1]):
                j = self.left[b,a]
                if j in colors: assert colors[j] != colors[i]
                else: colors[j] = 1-colors[i]; todo.append(j)
        self.A = [f for i,f in enumerate(self.faces) if colors[i]==0 and i!=self.rootid]
        self.white = [i for i in colors if colors[i]==1]
        self.n = len(self.A)
        self.aface = {frozenset(f):i for i,f in enumerate(self.A)}
        # Build H0 rotation independently from triangular wedges.
        hr = {v:[] for v in rot}
        for v,ns in rot.items():
            for a,b in zip(ns,ns[1:]+ns[:1]):
                k = self.aface.get(frozenset((v,a,b)))
                if k is not None: hr[v].append(self.N+k)
        for k,f in enumerate(self.A): hr[self.N+k] = list(f)
        self.hfaces,self.hleft = facial_walks(hr)
        self.outer = max(range(len(self.hfaces)),key=lambda k:len(self.hfaces[k]))
        assert len(self.hfaces[self.outer]) == 12
        self.hr = hr

    def states(self, forbidden=None):
        opts = [set(f)&self.X for f in self.A]
        if forbidden is not None: opts = [o-{forbidden[i]} for i,o in enumerate(opts)]
        yield from assignments(opts, {v:1 for v in self.X})

    def factors(self):
        cap = {v:sum(v in f for f in self.A)-(2 if v in self.X else 0) for v in self.rot}
        yield from assignments([set(f) for f in self.A],cap)

    def u_of(self,r,s): return tuple(next(v for v in f if v not in (r[i],s[i])) for i,f in enumerate(self.A))

    def cycles(self,u):
        adj = co.defaultdict(list)
        for k,f in enumerate(self.A):
            a,b = [v for v in f if v!=u[k]]
            adj[a].append((b,k)); adj[b].append((a,k))
        assert set(adj)==self.X and all(len(x)==2 for x in adj.values())
        seen,cycles = set(),[]
        for a in sorted(adj):
            if a in seen: continue
            c=[]; v=a; last=-1
            while v not in seen:
                seen.add(v)
                w,k = next((w,k) for w,k in adj[v] if k!=last)
                c.append((v,w,k)); v,last=w,k
            assert v==a
            cycles.append(c)
        return cycles

    def decompositions(self,u):
        cs=self.cycles(u)
        for bits in it.product((0,1),repeat=len(cs)):
            r=[None]*self.n; s=r.copy()
            for bit,c in zip(bits,cs):
                for a,b,k in c:
                    r[k],s[k]=(a,b) if bit==0 else (b,a)
            yield tuple(r),tuple(s)

    def forest(self,s):
        par = {v:v for v in self.rot}
        def find(v):
            while v!=par[v]: v=par[v]
            return v
        for k,f in enumerate(self.A):
            a,b=[v for v in f if v!=s[k]]; a,b=find(a),find(b)
            if a==b: return False
            par[a]=b
        return True

    def criterion(self,u,r):
        # F has u->centre->r. Suppressing centres gives u(t)->r(t).
        adj=co.defaultdict(list); indeg=co.Counter()
        for a,b in zip(u,r): adj[a].append(b); indeg[b]+=1
        q=co.deque(v for v in self.rot if indeg[v]==0); count=0
        while q:
            a=q.popleft(); count+=1
            for b in adj[a]:
                indeg[b]-=1
                if indeg[b]==0:q.append(b)
        return count==self.N

    def potential(self,u,base):
        adj=co.defaultdict(list)
        for k,f in enumerate(self.A):
            t=self.N+k
            for v in f:
                a,b=(v,t) if base[k]==v else (t,v)
                l,r=self.hleft[a,b],self.hleft[b,a]
                val=-int((u[k]==v)!=(base[k]==v))
                adj[l].append((r,val)); adj[r].append((l,-val))
        phi={self.outer:0}; q=[self.outer]
        for a in q:
            for b,w in adj[a]:
                if b not in phi: phi[b]=phi[a]+w; q.append(b)
                else: assert phi[b]==phi[a]+w
        assert len(phi)==len(self.hfaces)
        return tuple(phi[k] for k in range(len(phi)))

    def shortest_extremes(self,base):
        adj=co.defaultdict(list); rev=co.defaultdict(list)
        for k,f in enumerate(self.A):
            for v in f:
                a,b=(v,self.N+k) if v==base[k] else (self.N+k,v)
                l,r=self.hleft[a,b],self.hleft[b,a]
                adj[l].append((r,0)); adj[r].append((l,1))
                rev[r].append((l,0)); rev[l].append((r,1))
        def dist(g):
            d=[10**9]*len(self.hfaces); d[self.outer]=0; q=co.deque([self.outer])
            while q:
                a=q.popleft()
                for b,w in g[a]:
                    if d[b]>d[a]+w:
                        d[b]=d[a]+w
                        if w:q.append(b)
                        else:q.appendleft(b)
            return d
        return tuple(-x for x in dist(rev)),tuple(dist(adj))

    def sign(self,r,s):
        z=1
        for k,f in enumerate(self.A):
            z *= 1 if f[(f.index(r[k])+1)%3]==s[k] else -1
        return z

    def spoke_weights(self):
        # Antisymmetric edge weights with unit circulation on every bounded H0 face.
        adj=co.defaultdict(list)
        for a,ns in self.hr.items():
            for b in ns:
                l,r=self.hleft[a,b],self.hleft[b,a]
                if l!=r:adj[l].append((r,a,b))
        parent={self.outer:None}; q=[self.outer]
        for f in q:
            for g,a,b in adj[f]:
                if g not in parent:parent[g]=(f,b,a);q.append(g)
        w=co.Counter()
        for f in parent:
            while f!=self.outer:
                g,a,b=parent[f]
                w[a,b]+=1;w[b,a]-=1;f=g
        for j,f in enumerate(self.hfaces):
            val=sum(w[a,b] for a,b in zip(f,f[1:]+f[:1]))
            assert val==(1 if j!=self.outer else 1-len(self.hfaces))
        return {(k,v):w[self.N+k,v] for k,f in enumerate(self.A) for v in f}

def assignments(opts,cap):
    """Complete constraint DFS, choosing the tightest face or vertex, no author code."""
    n=len(opts); result=[None]*n
    def rec(todo):
        if not todo:
            assert not any(cap.values())
            yield tuple(result);return
        avail={i:[v for v in opts[i] if cap[v]>0] for i in todo}
        if any(not vs for vs in avail.values()):return
        incidence=co.defaultdict(list)
        for i,vs in avail.items():
            for v in vs:incidence[v].append(i)
        for v,c in cap.items():
            if c>len(incidence[v]):return
        i=min(todo,key=lambda j:len(avail[j]))
        # Saturated vertex implies all its remaining incident faces choose it.
        forced=next(((v,js) for v,js in incidence.items() if cap[v]==len(js) and cap[v]>0),None)
        if forced:
            v,js=forced
            for j in js:result[j]=v
            cap[v]-=len(js)
            yield from rec(todo-set(js))
            cap[v]+=len(js)
        else:
            for v in avail[i]:
                result[i]=v;cap[v]-=1
                yield from rec(todo-{i})
                cap[v]+=1
    yield from rec(set(range(n)))

def leq(a,b):return all(x<=y for x,y in zip(a,b))

def lattice_analysis(I,us=None,detail=False):
    us=list(I.factors()) if us is None else list(us)
    if not us:return {'V':I.N,'lattice':0}
    phis=[I.potential(u,us[0]) for u in us]
    lo,hi=I.shortest_extremes(us[0]); assert lo in phis and hi in phis
    assert tuple(map(min,zip(*phis)))==lo and tuple(map(max,zip(*phis)))==hi
    lower=[[] for _ in us];upper=[[] for _ in us]
    # Exact covers by testing only currently maximal strict predecessors.
    order=sorted(range(len(us)),key=lambda k:sum(phis[k]))
    for i in order:
        candidates=[j for j in reversed(order[:order.index(i)]) if leq(phis[j],phis[i])]
        for j in candidates:
            if not any(leq(phis[j],phis[k]) for k in lower[i]):lower[i].append(j);upper[j].append(i)
    rank=[0]*len(us); ideals=[set() for _ in us]
    ji=[i for i in order if len(lower[i])==1]
    for i in order:
        ranks={rank[j]+1 for j in lower[i]};assert len(ranks)<=1
        if ranks:rank[i]=ranks.pop()
        ideals[i]={j for j in ji if leq(phis[j],phis[i])}
        assert rank[i]==len(ideals[i])
    weights=I.spoke_weights(); entries=[]; signed=co.Counter();pairs=tm=0
    for i,u in enumerate(us):
        tp=0;poly=co.Counter();cs=I.cycles(u)
        for r,s in I.decompositions(u):
            good=I.forest(s);assert good==I.criterion(u,r)
            tp+=good;pairs+=1
            w=sum(weights[k,v] for k,v in enumerate(s));poly[w]+=I.sign(r,s)
        tm+=tp;signed.update(poly)
        entries.append({'u':u,'phi':phis[i],'rank':rank[i],'ideal':sorted(ideals[i]),'lower':lower[i],'upper':upper[i],
                        'cycles':[len(c) for c in cs],'tree_pairs':tp,'signed':dict(sorted((k,v) for k,v in poly.items() if v))})
    low,high=phis.index(lo),phis.index(hi)
    candidates={low,high}|{i for i in range(len(us)) if len(lower[i])==1 or len(upper[i])==1}
    result={'V':I.N,'root':sorted(I.R),'lattice':len(us),'pairs':pairs,'TM':tm,
            'c_min':min(len(I.cycles(u)) for u in us),'tree_elements':sum(e['tree_pairs']>0 for e in entries),
            'lo':low,'hi':high,'extreme_tree_pairs':[entries[j]['tree_pairs'] for j in (low,high)],
            'R2':any(entries[i]['tree_pairs'] for i in candidates),'R2_candidates':sorted(candidates),
            'rank_polynomial':dict(sorted(co.Counter(rank).items())),
            'join_irreducibles':ji,'signed':dict(sorted((k,v) for k,v in signed.items() if v))}
    if detail:result.update(entries=entries,faces_A=I.A,hfaces=I.hfaces,join_order=[[j,i] for i in ji for j in ji if i!=j and leq(phis[j],phis[i])])
    return result

def save(name,data):
    OUT.mkdir(exist_ok=True);(OUT/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf8')

def plantri(n):
    p=subprocess.run([str(ROOT/'workings/barnette_lab/vendor/plantri.exe'),'-ab',str(n)],capture_output=True,text=True,check=True)
    for line in p.stdout.splitlines():
        N,s=line.split();yield {i:[ord(c)-97 for c in ns] for i,ns in enumerate(s.split(','))}

if __name__=='__main__':
    d=json.loads((ROOT/'research/2026-11-14_opus_conjectures/data/c2_counterexample_V18.json').read_text())
    rot,root=parse_text(d['line']);I=Instance(rot,root)
    states=list(I.states());brute=[(r,s) for r in states for s in states if all(a!=b for a,b in zip(r,s))]
    us=sorted({I.u_of(r,s) for r,s in brute});assert set(us)==set(I.factors())
    assert set(brute)=={(r,s) for u in us for r,s in I.decompositions(u)}
    result=lattice_analysis(I,us,True)
    result['states']=len(states);result['brute_pairs']=[{'r':r,'s':s,'u':I.u_of(r,s),'forest':I.forest(s),'criterion':I.criterion(I.u_of(r,s),r)} for r,s in brute]
    # Connectivity checked by deleting every subset of at most three vertices.
    bad=[]
    for k in range(4):
        for deleted in it.combinations(rot,k):
            remain=set(rot)-set(deleted);seen={min(remain)};q=list(seen)
            for a in q:
                for b in rot[a]:
                    if b in remain and b not in seen:seen.add(b);q.append(b)
            if seen!=remain:bad.append(deleted)
    result['disconnecting_sets_size_le3']=bad;assert not bad
    save('v18.json',result)
    print({k:v for k,v in result.items() if k not in ('entries','brute_pairs','hfaces','faces_A','join_order')})
