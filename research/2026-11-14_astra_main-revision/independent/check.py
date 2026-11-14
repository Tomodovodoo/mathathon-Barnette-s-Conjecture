"""Independent checks of the merged manuscript. No project proof code imported."""
import collections as co
import hashlib
import itertools as it
import json
import math
from pathlib import Path
import subprocess
import networkx as nx

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
C = co.Counter()

def edge(a, b): return tuple(sorted((a, b)))
def graph(vs, es):
    g = nx.Graph(); g.add_nodes_from(vs); g.add_edges_from(es); return g
def subsets(vs):
    vs = list(vs)
    for mask in range(1 << len(vs)):
        yield {v for i, v in enumerate(vs) if mask >> i & 1}
def cycles(es):
    nxt = dict(es); ans = []
    while nxt:
        start = min(nxt); a = start; cyc = []
        while a in nxt:
            cyc.append(a); a = nxt.pop(a)
        assert a == start
        ans.append(cyc)
    return ans

class M:
    def __init__(self, faces, root):
        self.f = [tuple(f) for f in faces]; self.root = root
        self.V = set().union(*map(set, faces)); self.E = {}
        self.direct = {}
        for t, f in enumerate(self.f):
            for a,b in zip(f, f[1:]+f[:1]):
                self.E.setdefault(edge(a,b), []).append(t)
                assert (a,b) not in self.direct
                self.direct[a,b] = t
        assert all(len(ts)==2 for ts in self.E.values())
        self.G = graph(range(len(faces)), self.E.values())
        colour = nx.bipartite.color(self.G)
        self.B = {t for t in self.G if colour[t]==colour[root]}
        self.W = set(self.G)-self.B; self.R = set(self.f[root]); self.X = self.V-self.R
        self.A = sorted(self.B-{root}); self.n = len(self.A)
        self.T = graph(self.V, self.E)
        assert self.n == len(self.X) and len(self.E)==3*(self.n+1)
        assert len(self.f)==2*(self.n+1) and len(self.V)==self.n+3
        self.owner = {e: next(t for t in ts if t in self.B) for e,ts in self.E.items()}
        self.paths = {}
        self.K = {}
        dist = nx.single_source_shortest_path_length(self.G,root)
        for y in sorted(self.W):
            p=[y]
            while p[-1]!=root:
                p.append(min(z for z in self.G[p[-1]] if dist[z]==dist[p[-1]]-1))
            self.paths[y]=p
            k={}
            for prev,t,nxt in zip(p,p[1:],p[2:]):
                if t not in self.A: continue
                ei=set(self.f[t]) & set(self.f[prev]); eo=set(self.f[t]) & set(self.f[nxt])
                v,=ei & eo; a,=ei-{v}; b,=eo-{v}
                f=self.f[t]; i=f.index(v)
                k[t,v] = 1 if (f[(i+1)%3], f[(i+2)%3])==(a,b) else -1
            self.K[y]=k
    def delta(self,a,b): return 1 if self.direct[a,b] in self.B else -1
    def states(self):
        ans=[]
        def rec(i,used,s):
            if i==self.n: ans.append(tuple(s)); return
            for v in sorted(set(self.f[self.A[i]]) & self.X-used): rec(i+1,used|{v},s+[v])
        rec(0,set(),[]); return ans
    def q(self,s): return {edge(*[v for v in self.f[t] if v!=x]) for t,x in zip(self.A,s)}
    def good(self,s):
        q=graph(self.V,self.q(s))
        return nx.is_forest(q) and all(len(set(vs)&self.R)==1 for vs in nx.connected_components(q))
    def eta(self,s,y): return sum(self.K[y].get((t,v),0) for t,v in zip(self.A,s))
    def weight(self,s): return sum(self.eta(s,y) for y in self.W)
    def eps(self,r,s): return math.prod(self.delta(a,b) for a,b in zip(r,s))
    def disk(self,cyc):
        es={edge(a,b) for a,b in zip(cyc,cyc[1:]+cyc[:1])}
        cut=self.G.copy(); cut.remove_edges_from(self.E[e] for e in es)
        comps=list(nx.connected_components(cut)); assert len(comps)==2
        inside=next(x for x in comps if self.root not in x)
        ccw=self.direct[cyc[0],cyc[1]] in inside
        vi=set().union(*(set(self.f[t]) for t in inside))-set(cyc)
        B=len(inside & self.B); W=len(inside & self.W)
        ell=sum(self.owner[e] in inside for e in es)
        return dict(cycle=cyc, ccw=ccw, B=B,W=W,I=len(vi),interior=sorted(vi),h=len(cyc),ell=ell,faces=sorted(inside))
    def select(self,s,e0):
        a,b=e0; c,=self.R-{a,b}; S=self.q(s)|{edge(a,c),edge(b,c)}
        Y=self.G.copy(); Y.remove_edges_from(self.E[e] for e in S)
        assert nx.is_tree(Y)
        parent={self.root:None}; todo=[self.root]
        for v in todo:
            for w in Y[v]:
                if w not in parent: parent[w]=v; todo.append(w)
        P=set()
        for t in self.B:
            child=[w for w in Y[t] if parent.get(w)==t]; assert len(child)==1
            P.add(edge(*set(self.f[t]).intersection(self.f[child[0]])))
        return P
    def selections(self):
        # Enumerate perfect matchings by black faces, with disjoint white partners.
        B=sorted(self.B); ans=[]
        def rec(i,used,P):
            if i==len(B): ans.append(frozenset(P)); return
            t=B[i]
            for e,ts in self.E.items():
                if t not in ts: continue
                y,=set(ts)-{t}
                if y not in used: rec(i+1,used|{y},P+[e])
        rec(0,set(),[]); return ans
    def recovered(self,P,e0):
        H=graph(self.V,set(P)-{e0}); ss={}
        for vs in nx.connected_components(H):
            root,=set(vs)&self.R
            for a,b in nx.bfs_edges(H,root): ss[self.owner[edge(a,b)]]=b
        return tuple(ss[t] for t in self.A)

def rotation_faces(line):
    count,code=line.split(); rot=[[ord(c)-97 for c in row] for row in code.split(',')]
    assert len(rot)==int(count)
    seen=set(); fs=[]
    for u,row in enumerate(rot):
        for v in row:
            if (u,v) in seen: continue
            a,b=u,v; f=[]
            while (a,b) not in seen:
                seen.add((a,b)); f.append(a)
                row=rot[b]; a,b=b,row[(row.index(a)+1)%len(row)]
            assert (a,b)==(u,v) and len(f)==3
            fs.append(f)
    return fs

def check_model(m, full=True):
    ss=m.states(); good={s for s in ss if m.good(s)}
    pairs=[(r,s) for r in ss for s in ss if all(a!=b for a,b in zip(r,s))]
    pairset=set(pairs); C['rootings']+=1; C['states']+=len(ss); C['pairs']+=len(pairs)
    classes=co.defaultdict(list); bys=co.defaultdict(list)
    for r,s in pairs:
        es=list(zip(r,s)); cs=cycles(es); disks=[m.disk(c) for c in cs]
        c=len(cs); plus=sum(d['ccw'] for d in disks)
        assert m.n%2==c%2
        assert m.eps(r,s)==(-1)**((m.n+c)//2+plus)
        assert (1j)**(sum(m.delta(a,b) for a,b in es)//3)==(1j)**(-m.n)*m.eps(r,s)
        classes[frozenset(edge(a,b) for a,b in es)].append((r,s,disks))
        bys[s].append(r)
        for cyc,d in zip(cs,disks):
            h=d['h']; assert h==2*d['ell']+3 and d['W']==d['B']+1
            assert sum(m.delta(a,b) for a,b in zip(cyc,cyc[1:]+cyc[:1]))==(-3 if d['ccw'] else 3)
            ids=[i for i,(a,b) in enumerate(es) if a in cyc]
            rr=list(r); st=list(s)
            for i in ids: rr[i],st[i]=st[i],rr[i]
            rr,st=tuple(rr),tuple(st); assert (rr,st) in pairset
            assert m.eps(rr,st)==-m.eps(r,s)
            for y in m.W:
                jump=m.eta(st,y)-m.eta(s,y)
                assert jump==(1 if y in d['faces'] else 0)*(1 if not d['ccw'] else -1)
            C['D_reversals']+=1
        q=graph(m.V,m.q(s))
        for vs in nx.connected_components(q):
            sub=q.subgraph(vs); gamma=len(set(vs)&m.R)
            assert sub.number_of_edges()==len(vs)-gamma and gamma<=1
        for cyc in nx.cycle_basis(q):
            es={edge(a,b) for a,b in zip(cyc,cyc[1:]+cyc[:1])}
            rr=list(r)
            for i,t in enumerate(m.A):
                if edge(*[v for v in m.f[t] if v!=s[i]]) in es:
                    rr[i],=set(m.f[t])-{r[i],s[i]}
            rr=tuple(rr); assert (rr,s) in pairset and m.eps(rr,s)==-m.eps(r,s)
            C['Q_reversals']+=1
    for s in ss:
        assert len(bys[s])==1 if s in good else sum(m.eps(r,s) for r in bys[s])==0
        assert (s in good)==(len(bys[s])>0 and nx.is_forest(graph(m.V,m.q(s))))
        if full:
            for choices in it.product((0,1),repeat=m.n):
                es=[]
                for t,v,choice in zip(m.A,s,choices):
                    w=sorted(set(m.f[t])-{v})[choice]; es.append((v,w))
                H=nx.DiGraph(es); H.add_nodes_from(m.V)
                assert all(d<=1 for _,d in H.out_degree())
                for cyc in nx.cycle_basis(H.to_undirected()):
                    if H.has_edge(cyc[0],cyc[1]): pass
                    else: cyc=cyc[::-1]
                    assert all(H.has_edge(a,b) for a,b in zip(cyc,cyc[1:]+cyc[:1]))
                    d=m.disk(cyc)
                    assert d['B']+d['W']==2*d['I']+d['h']-2
                    assert 3*(d['B']-d['W'])==2*d['ell']-d['h']
                    assert d['B']==d['I']+d['ell']
                    assert d['W']==d['B']+1 and d['h']==2*d['ell']+3
                    assert not(set(d['interior']) & m.R)
                    C['chosen_cycles']+=1
                for vs in nx.connected_components(H.to_undirected()):
                    gamma=sum(H.out_degree(v)==0 for v in vs)
                    assert H.subgraph(vs).number_of_edges()==len(vs)-gamma and gamma<=1
                C['chosen_side_systems']+=1
    if pairs:
        minimum=min(len(v[0][2]) for v in classes.values())
        expect=(-1)**((m.n-minimum)//2)*math.factorial(minimum)*sum(math.prod(d['W'] for d in v[0][2]) for v in classes.values() if len(v[0][2])==minimum)
        actual=sum(m.eps(r,s)*m.weight(s)**minimum for r,s in pairs)
        assert actual==expect and actual!=0 and good
        for j in range(minimum): assert sum(m.eps(r,s)*m.weight(s)**j for r,s in pairs)==0
        for v in classes.values(): assert len(v)==2**len(v[0][2])
    sels=m.selections(); acyclic=[]
    for P in sels:
        H=graph(m.V,P); dual=m.G.copy(); dual.remove_edges_from(m.E[e] for e in P)
        assert nx.is_connected(dual)==nx.is_forest(H)
        assert all(d==2 for _,d in dual.degree())
        if not nx.is_forest(H): continue
        acyclic.append(P); assert nx.number_connected_components(H)==2
        comp={v:i for i,vs in enumerate(nx.connected_components(H)) for v in vs}
        assert all((e in P)==(comp[e[0]]==comp[e[1]]) for e in m.E)
        for e0 in set(P)&{edge(a,b) for a,b in it.combinations(m.R,2)}:
            st=m.recovered(P,e0); assert st in ss
            if st in good: assert m.select(st,e0)==P
            C['reverse_states']+=1
        C['acyclic_selections']+=1
    for e0 in map(lambda e:edge(*e),it.combinations(m.R,2)):
        emitted=[]
        for s in good:
            P=frozenset(m.select(s,e0)); assert P in acyclic and e0 in P
            assert m.recovered(P,e0)==s
            emitted.append(P); C['recoveries']+=1
        assert len(set(emitted))==len(emitted)
    face_sets={frozenset(f) for f in m.f}
    seps=[tuple(vs) for vs in it.combinations(sorted(m.V),3) if all(edge(a,b) in m.E for a,b in it.combinations(vs,2)) and frozenset(vs) not in face_sets]
    for S in subsets(m.X):
        U=m.V-S; e=sum(set(e)<=U for e in m.E); b=sum(set(m.f[t])<=U for t in m.B)
        hall=sum(min(2,len(set(m.f[t])&S)) for t in m.A)-2*len(S)
        assert hall==2*len(U)-4-e+b
        if not seps: assert hall>=0
        C['density_subsets']+=1
    if not seps: assert pairs
    for tri in seps:
        d=m.disk(list(tri)); inn=set(d['faces']); other=set(m.G)-inn
        pieces=[]
        for region in (inn,other):
            colour=[next(t for t in m.E[edge(a,b)] if t in region) in m.B for a,b in zip(tri,tri[1:]+tri[:1])]
            assert len(set(colour))==1
            oriented=tri if m.direct[tri[0],tri[1]] not in region else tri[::-1]
            p=M([m.f[t] for t in sorted(region)]+[oriented],len(region))
            assert len(p.V)<len(m.V) and len(p.V)>=4 and nx.is_connected(p.T)
            pieces.append(p)
        for a in pieces[0].selections():
            if not nx.is_forest(graph(pieces[0].V,a)): continue
            for b in pieces[1].selections():
                if a & set(it.starmap(edge,it.combinations(tri,2))) != b & set(it.starmap(edge,it.combinations(tri,2))): continue
                if not nx.is_forest(graph(pieces[1].V,b)): continue
                P=a|b; assert P in acyclic
                C['glued_pairs']+=1
        C['separators']+=1
    return dict(vertices=len(m.V),faces=len(m.f),edges=len(m.E),black=len(m.B),white=len(m.W),A=[list(m.f[t]) for t in m.A],states=ss,good=sorted(good),pairs=[dict(r=r,s=s,eps=m.eps(r,s),weight=m.weight(s),cycles=ds) for vs in classes.values() for r,s,ds in vs],paths={str(y):p for y,p in m.paths.items()},heights={str(s):{str(y):m.eta(s,y) for y in m.W} for s in ss},avoiding={str(e):sum(e in P for P in acyclic) for e in map(lambda x:edge(*x),it.combinations(m.R,2))},selections_acyclic=[sorted(P) for P in acyclic])

def main():
    run=json.loads((ROOT/'paper/figures/running.json').read_text())
    result=check_model(M(run['faces'],run['t0']),full=False)
    assert len(result['states'])==12 and len(result['good'])==6 and len(result['pairs'])==8
    assert [sum(p['eps']*p['weight']**j for p in result['pairs']) for j in range(3)]==[0,0,18]
    assert result['avoiding']['(0, 4)']==6
    (OUT/'running.json').write_text(json.dumps(result,indent=2))
    totals={4:0,5:0}; exe=ROOT/'workings/barnette_lab/vendor/plantri.exe'
    for n in range(6,13):
        gen=subprocess.run([str(exe),'-b','-a',str(n)],capture_output=True,text=True,check=True)
        (OUT/f'plantri-{n}.txt').write_text(gen.stdout+gen.stderr)
        lines=gen.stdout.splitlines(); totals[n]=len(lines)
        for line in lines:
            fs=rotation_faces(line)
            for root in range(len(fs)):
                check_model(M(fs,root))
        print('completed order',n,'classes',len(lines),flush=True)
    # The labelled cube in the figure has opposite vertex pairs 03,14,25.
    g=nx.complete_multipartite_graph(2,2,2)
    fs=rotation_faces(subprocess.run([str(exe),'-b','-a','6'],capture_output=True,text=True,check=True).stdout.strip())
    (OUT/'cube.json').write_text(json.dumps(check_model(M(fs,0)),indent=2))
    # Hexagonal bipyramid, equator 0..5 and apices 6,7.
    fs=[]
    for a in range(6):
        b=(a+1)%6; fs.extend([[6,a,b],[7,b,a]])
    prism=check_model(M(fs,0)); assert len(prism['states'])==3 and len(prism['good'])==2
    assert sorted(prism['avoiding'].values())==[2,2,4]
    (OUT/'prism.json').write_text(json.dumps(prism,indent=2))
    (OUT/'census.json').write_text(json.dumps(dict(classes=totals,checks=C,plantri_sha256=hashlib.sha256(exe.read_bytes()).hexdigest()),indent=2))
    print(json.dumps(dict(classes=totals,checks=C),indent=2))

if __name__=='__main__': main()
