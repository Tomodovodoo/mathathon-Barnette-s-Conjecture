"""Independent referee implementation. No imports from audited or reference code."""
import ast
import json
import sys
from pathlib import Path
from itertools import combinations, product
from collections import Counter, deque
import networkx as nx

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
OPUS = ROOT / 'research/2026-11-14_opus_route-graph-theory'
ASTRA = ROOT / 'research/2026-11-14_astra_limits'

def edge(a,b): return tuple(sorted((a,b)))
def graph(n, es):
    g=nx.Graph(); g.add_nodes_from(range(n)); g.add_edges_from(es); return g
def faces_rotation(rot,darts=None):
    rot={int(v):list(ws) for v,ws in rot.items()}
    seen=set(); fs=[]
    for a,b in (darts if darts is not None else [(a,b) for a in rot for b in rot[a]]):
            if (a,b) in seen: continue
            f=[]; u,v=a,b
            while (u,v) not in seen:
                seen.add((u,v)); f.append(u)
                w=rot[v][(rot[v].index(u)-1)%len(rot[v])]; u,v=v,w
            assert (u,v)==(a,b)
            fs.append(tuple(f))
    return fs

class Tri:
    def __init__(self, rot=None, es=None, fs=None, outer=0):
        if rot is not None:
            self.rot={int(v):list(ws) for v,ws in rot.items()}
            self.g=nx.Graph((int(v),w) for v,ws in rot.items() for w in ws)
            self.fs=faces_rotation(self.rot)
        elif fs is not None:
            self.fs=[tuple(f) for f in fs]
            self.g=nx.Graph(edge(a,b) for f in self.fs for a,b in zip(f,f[1:]+f[:1]))
        else:
            self.g=nx.Graph(es); ok,emb=nx.check_planarity(self.g); assert ok
            self.rot=emb.get_data(); self.fs=faces_rotation(self.rot,list(emb.edges()))
        self.sides={}
        self.inc={}
        for i,f in enumerate(self.fs):
            assert len(f)==3 and len(set(f))==3
            for a,b in zip(f,f[1:]+f[:1]):
                self.sides[a,b]=i
                self.inc.setdefault(edge(a,b),[]).append(i)
        assert all(len(v)==2 for v in self.inc.values())
        self.dual=nx.Graph((a,b) for a,b in self.inc.values())
        assert nx.is_bipartite(self.dual)
        if not isinstance(outer,int): outer=next(i for i,f in enumerate(self.fs) if set(f)==set(outer))
        self.outer=outer; self.R=set(self.fs[outer]); self.X=set(self.g)-self.R
        col=nx.bipartite.color(self.dual)
        self.black=[i for i in range(len(self.fs)) if col[i]==col[outer]]
        self.white=[i for i in range(len(self.fs)) if col[i]!=col[outer]]
        self.A=[i for i in self.black if i!=outer]
        self.n=len(self.A)
        self.H=nx.Graph(((0,t),(1,v)) for t in self.black for v in self.fs[t])
    def states(self):
        order=sorted(range(self.n),key=lambda i:len(set(self.fs[self.A[i]])&self.X))
        s=[None]*self.n
        def rec(j,used):
            if j==self.n: yield tuple(s); return
            i=order[j]
            for v in sorted(set(self.fs[self.A[i]])&self.X-used):
                s[i]=v; yield from rec(j+1,used|{v})
        return list(rec(0,set()))
    def valid(self,s):
        return len(s)==self.n and set(s)==self.X and all(v in self.fs[t] for t,v in zip(self.A,s))
    def pairs(self,ss): return [(r,s) for r in ss for s in ss if all(a!=b for a,b in zip(r,s))]
    def Q(self,s): return graph(len(self.g),[tuple(set(self.fs[t])-{v}) for t,v in zip(self.A,s)])
    def tree(self,s):
        h=self.H.copy(); h.remove_edges_from(((0,t),(1,v)) for t,v in zip(self.A,s)); return nx.is_tree(h)
    def k(self,s):
        q=self.Q(s); return q.number_of_edges()-len(q)+nx.number_connected_components(q)
    def dc(self,r,s):
        nxt={a:(b,i) for i,(a,b) in enumerate(zip(r,s))}; seen=set(); cs=[]
        for v in sorted(nxt):
            if v in seen: continue
            c=[]; w=v
            while w not in seen:
                seen.add(w); z,i=nxt[w]; c.append(i); w=z
            assert w==v; cs.append(c)
        return cs
    def neighbors(self,p):
        r,s=p
        for c in self.dc(r,s):
            rr=list(r); ss=list(s)
            for i in c: rr[i],ss[i]=ss[i],rr[i]
            yield tuple(rr),tuple(ss)
        q=self.Q(s)
        for c in nx.cycle_basis(q):
            rr=list(r)
            for a,b in zip(c,c[1:]+c[:1]):
                i=next(i for i,t in enumerate(self.A) if set(self.fs[t])-{s[i]}=={a,b})
                rr[i]=next(iter(set(self.fs[self.A[i]])-{r[i],s[i]}))
            yield tuple(rr),s
    def W(self,s):
        w=nx.MultiGraph(); w.add_nodes_from(self.white)
        for t,v in zip(self.A,s):
            zz=[]
            for e in combinations(self.fs[t],2):
                if v in e: zz.append(next(z for z in self.inc[edge(*e)] if z!=t))
            w.add_edge(*zz,face=t)
        return w
    def construct(self,s,e0):
        w=self.W(s); assert nx.is_tree(w)
        y0=next(z for z in self.inc[e0] if z!=self.outer)
        P={e0}
        for parent,child in nx.bfs_edges(w,y0):
            t=next(iter(w[parent][child].values()))['face']; v=s[self.A.index(t)]
            P.add(next(e for e in self.inc if v in e and set(e)<=set(self.fs[t]) and child in self.inc[e]))
        return frozenset(P)
    def partitions(self,e0):
        vs=sorted(self.g); a,b=e0; c=next(iter(self.R-set(e0))); free=[v for v in vs if v not in self.R]
        for mask in range(1<<len(free)):
            U={a,b}|{v for j,v in enumerate(free) if mask>>j&1}; V=set(vs)-U
            if nx.is_tree(self.g.subgraph(U)) and nx.is_tree(self.g.subgraph(V)):
                yield frozenset(e for e in self.inc if (e[0] in U)==(e[1] in U))
    def derive(self,P,e0):
        q=self.g.edge_subgraph(set(P)-{e0}).copy(); q.add_nodes_from(self.g)
        tails={}
        for root in self.R:
            for parent,child in nx.bfs_edges(q,root): tails[edge(parent,child)]=child
        return tuple(tails[next(e for e in P if t in self.inc[e])] for t in self.A)
    def obstructed(self):
        bad=[]
        for c in combinations(sorted(self.g),3):
            if not all(self.g.has_edge(a,b) for a,b in combinations(c,2)): continue
            if any(set(f)==set(c) for f in self.fs): continue
            comps=list(nx.connected_components(self.g.subgraph(set(self.g)-set(c))))
            outside=next(cc for cc in comps if cc&(self.R-set(c)))
            inside=set(self.g)-set(c)-outside
            signs=[]
            for a,b in combinations(c,2):
                t=next(t for t in self.inc[edge(a,b)] if (set(self.fs[t])-set(c))&inside)
                signs.append(t in self.black)
            assert len(set(signs))==1
            if signs[0]: bad.append(c)
        return bad
    def flow(self):
        d=nx.DiGraph(); d.add_nodes_from(['S','Z'])
        for v in self.X: d.add_edge('S',(1,v),capacity=2)
        for t in self.A:
            d.add_edge((0,t),'Z',capacity=2)
            for v in set(self.fs[t])&self.X: d.add_edge((1,v),(0,t),capacity=1)
        return nx.maximum_flow_value(d,'S','Z')==2*self.n

def from_example(path):
    d=json.loads(path.read_text())
    if 'rot' in d: return Tri(rot=d['rot'],outer=d['t0']),d
    if 'faces' in d: return Tri(fs=d['faces'],outer=d.get('outer',0)),d
    if 'dual_edges' in d: return Tri(es=d['dual_edges'],outer=d.get('outer',0)),d
    return Tri(es=d['edges'],outer=d.get('outer',0)),d

def save(name,data):
    (OUT/name).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    print(name,json.dumps(data)[:500],flush=True)

def census():
    rows=[]; failures=[]; nroots=0; nimages=0; dichotomy=0; d3pairs=0
    for N in range(6,15):
        raw=json.loads((OPUS/f'code/data/eul_{N}.json').read_text())
        for gi,rot in enumerate(raw):
            base=Tri(rot=rot)
            for outer in range(len(base.fs)):
                t=Tri(rot=rot,outer=outer); ss=t.states(); pairs=t.pairs(ss); tm=[s for s in ss if t.tree(s)]
                assert bool(pairs)==t.flow()==(not t.obstructed())==bool(tm)
                assert all(sum(all(a!=b for a,b in zip(r,s)) for r in ss)==1 for s in tm)
                # Test D3 through reverse reachability in directed, non-increasing exchange graph.
                ps=set(pairs); rev={p:[] for p in ps}
                for p in pairs:
                    for q in t.neighbors(p):
                        assert q in ps
                        if t.k(q[1])<=t.k(p[1]): rev[q].append(p)
                good={p for p in ps if t.k(p[1])==0}; todo=list(good)
                while todo:
                    for p in rev[todo.pop()]:
                        if p not in good: good.add(p); todo.append(p)
                assert good==ps; d3pairs+=len(ps)
                # All partitions are independently generated from vertex subsets.
                for e0 in combinations(sorted(t.R),2):
                    e0=edge(*e0); parts=list(t.partitions(e0)); images={t.construct(s,e0) for s in tm}
                    assert len(images)==len(tm)
                    for P in parts:
                        s=t.derive(P,e0); assert t.valid(s)
                        assert (P in images)==t.tree(s)
                        assert t.tree(s) or not any(all(a!=b for a,b in zip(r,s)) for r in ss)
                        dichotomy+=1
                    for s in tm: assert t.derive(t.construct(s,e0),e0)==s
                    nimages+=len(images)
                rows.append([N,gi,outer,len(ss),len(pairs),len(tm)])
                nroots+=1
            print('census',N,gi,'roots',nroots,flush=True)
    save('census.json',{'range':'saved instances V=6..14, every facial root, every root edge','graph_counts':dict(Counter(row[0] for row in rows)), 'root_count':nroots,'images':nimages,'partitions':dichotomy,'D3_ordered_pairs':d3pairs,'rows':rows,'failures':failures})

if __name__=='__main__':
    globals()[sys.argv[1]]()
