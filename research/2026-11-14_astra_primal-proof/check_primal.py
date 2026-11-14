"""Exact finite checks using only G, its facial walks and incidence assignments.

The lab supplies graphs and faces_of, not states, signs, weights or recovery.
Run from any directory: python check_primal.py [--max-order 20]
"""
from pathlib import Path
import sys, json, argparse
from itertools import combinations
from collections import Counter, defaultdict
import networkx as nx

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / 'workings/barnette_lab'))
from barnette_lab.core import faces_of, named_graphs, plantri_graphs

def edge(a, b): return tuple(sorted((a, b)))
def mul(p, q):
    r = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q): r[i+j] += a*b
    return r
def add(p, q, sign=1):
    p += [0] * max(0, len(q)-len(p))
    for i, a in enumerate(q): p[i] += sign*a
    return p

class Primal:
    def __init__(self, g, root):
        self.g = g
        self.root = root
        ok, emb = nx.check_planarity(g)
        assert ok and nx.edge_connectivity(g) == 3
        self.faces, self.sides = faces_of(emb)
        self.inc = {v: sorted({self.sides[v,w] for w in g[v]}) for v in g}
        color = nx.bipartite.color(g)
        self.black = sorted(v for v in g if color[v] == color[root])
        self.white = sorted(set(g)-set(self.black))
        self.A = sorted(set(self.black)-{root})
        self.R = set(self.inc[root])
        self.X = sorted(set(range(len(self.faces)))-self.R)
        self.edges = sorted(edge(*e) for e in g.edges())
        self.ef = {e: (self.sides[e], self.sides[e[::-1]]) for e in self.edges}
        self.bend = {e: next(v for v in e if v in self.black) for e in self.edges}
        assert len(self.A) == len(self.X)
        assert all(len(fs) == 3 for fs in self.inc.values())
        self.transition = {}
        for e in self.edges:
            b = self.bend[e]; w = next(v for v in e if v != b)
            f, h = self.sides[b,w], self.sides[w,b]
            self.transition[f,h] = (e,1)
            self.transition[h,f] = (e,-1)
        # This is a fixed consistent sphere orientation. Reversing it changes
        # all deltas and potentials; the tested common coefficient sign stays valid.
        self.alpha = dict.fromkeys(self.edges, 0)
        for w in self.white:
            path = nx.shortest_path(g, root, w)
            for u,v in zip(path,path[1:]): self.alpha[edge(u,v)] += 1 if u in self.black else -1
        self.a = {}
        for b in self.A:
            fs = self.inc[b]; self.a[b,fs[0]] = 0
            for f in fs[1:]:
                e,d = self.transition[fs[0],f]
                self.a[b,f] = -d*self.alpha[e]
            for f,h in combinations(fs,2):
                e,d = self.transition[f,h]
                assert self.a[b,h]-self.a[b,f] == -d*self.alpha[e]

    def states(self):
        def rec(i, used, s):
            if i == len(self.A): yield tuple(s); return
            for f in self.inc[self.A[i]]:
                if f in self.X and f not in used: yield from rec(i+1,used|{f},s+[f])
        return list(rec(0,set(),[]))

    def links(self, s, r=None):
        d = nx.Graph(); d.add_nodes_from(range(len(self.faces)))
        for i,b in enumerate(self.A):
            f,h = (r[i],s[i]) if r is not None else tuple(set(self.inc[b])-{s[i]})
            e,_ = self.transition[f,h]
            d.add_edge(f,h,edge=e,b=b)
        return d

    def disk(self, circuit, state):
        es = [self.transition[f,h][0] for f,h in zip(circuit,circuit[1:]+circuit[:1])]
        h = len(es)
        g = self.g.copy(); g.remove_edges_from(es)
        parts = list(nx.connected_components(g)); assert len(parts)==2
        S = next(p for p in parts if self.root not in p)
        EA = [e for e in self.edges if set(e)&S]
        U = set().union(*(set(self.inc[v]) for v in S))
        B = set(self.black)&S
        ell = sum(self.bend[e] in S for e in es)
        assert 3*len(S)+h == 2*len(EA)
        assert 3*len(B)+h == len(EA)+ell
        assert len(S)+len(U) == len(EA)+1
        assert len(B)+h == len(U)+ell
        assert h == 2*ell+3
        assert not U & self.R
        mixed = {f for f,vs in enumerate(self.faces) if set(vs)&S and set(vs)-S}
        assert mixed == set(circuit)
        ds = sum(self.transition[f,k][1] for f,k in zip(circuit,circuit[1:]+circuit[:1]))
        assert abs(ds)==3
        slope = 0
        for f,k in zip(circuit,circuit[1:]+circuit[:1]):
            e,d = self.transition[f,k]; b=self.bend[e]
            assert state[self.A.index(b)] == f
            slope += self.a[b,k]-self.a[b,f]
        assert slope == -ds//3 * len(S&set(self.white))
        assert slope*ds < 0
        return dict(faces=circuit, edges=es, shore=sorted(S), h=h, ell=ell,
                    vertices=len(S), black=len(B), incident_edges=len(EA),
                    incident_faces=len(U), delta=ds, slope=slope)

    def recover(self, s, e0):
        q = [data['edge'] for _,_,data in self.links(s).edges(data=True)]
        removed = set(q) | {edge(self.root,v) for v in self.g[self.root] if edge(self.root,v)!=e0}
        K=self.g.copy(); K.remove_edges_from(removed)
        assert nx.is_tree(K)
        parent=dict(nx.bfs_predecessors(K,self.root))
        P={edge(w,parent[w]) for w in self.white}
        assert e0 in P
        assert all(sum(v in e for e in P)==1 for v in self.g)
        C=self.g.copy(); C.remove_edges_from(P)
        assert nx.is_connected(C) and all(d==2 for _,d in C.degree())
        selected=nx.Graph(); selected.add_nodes_from(range(len(self.faces)))
        selected.add_edges_from(self.ef[e] for e in P)
        assert nx.is_forest(selected)
        return dict(e0=e0, removed=sorted(removed), tree=sorted(edge(*e) for e in K.edges()),
                    P=sorted(P), cycle=nx.cycle_basis(C)[0])

    def check(self, counts):
        ss=self.states(); counts['states']+=len(ss); counts['rootings']+=1
        pairs=[(r,s) for r in ss for s in ss if all(x!=y for x,y in zip(r,s))]
        counts['pairs']+=len(pairs)
        n=len(self.A)
        deficit=max(2*len(S)-sum(min(2,len(set(self.inc[b])&S)) for b in self.A)
                    for mask in range(1<<n) for S in [{self.X[i] for i in range(n) if mask>>i&1}])
        assert bool(pairs)==(deficit==0)
        counts['deficit_subsets']+=1<<n
        coeff=Counter(); poly=[0]; groups={}; pairrows=[]
        for r,s in pairs:
            sign=1
            for f,h in zip(r,s): sign*=self.transition[f,h][1]
            coeff[s]+=sign
            weight=[1]
            for b,f in zip(self.A,s): weight=mul(weight,[1,self.a[b,f]])
            add(poly,weight,sign)
            d=self.links(s,r)
            key=tuple(sorted(data['edge'] for _,_,data in d.edges(data=True)))
            ds=nx.DiGraph(); ds.add_edges_from(zip(r,s))
            cycles=list(nx.simple_cycles(ds))
            disks=[self.disk(c,r) for c in cycles]
            counts['directed_disk_checks']+=len(disks)
            if key not in groups: groups[key]=disks
            pairrows.append(dict(r=r,s=s,sign=sign,disks=disks))
        for s in ss:
            mates=[r for r,t in pairs if t==s]
            if not mates: continue
            q=self.links(s); cyc=nx.cycle_basis(q)
            if cyc:
                assert coeff[s]==0
                counts['cancelled_states']+=1
                for r in mates:
                    C=cyc[0]
                    # Orient the selected circuit by the tails of r.
                    if r[self.A.index(q[C[0]][C[1]]['b'])]!=C[0]: C=list(reversed(C))
                    self.disk(C,r); counts['directed_disk_checks']+=1
                    rr=list(r)
                    for f,h in zip(C,C[1:]+C[:1]): rr[self.A.index(q[f][h]['b'])]=h
                    rr=tuple(rr); assert rr in mates
                    sg=lambda t: __import__('math').prod(self.transition[f,h][1] for f,h in zip(t,s))
                    assert sg(rr)==-sg(r)
            else:
                assert len(mates)==1 and abs(coeff[s])==1
                for w in self.g[self.root]:
                    self.recover(s,edge(self.root,w)); counts['recoveries']+=1
        if pairs:
            m=min(map(len,groups.values()))
            predicted=(-1)**((n-m)//2)*sum(__import__('math').prod(abs(c['slope']) for c in cs)
                                         for cs in groups.values() if len(cs)==m)
            assert all(x==0 for x in poly[:m]) and poly[m]==predicted!=0
            counts['nonzero_polynomials']+=1
        return dict(root=self.root, black=self.black,white=self.white,faces=self.faces,
                    edges=self.edges,incidences=self.inc,R=sorted(self.R),A=self.A,X=self.X,
                    flow=[dict(edge=e,value=a) for e,a in self.alpha.items()],
                    weights=[dict(b=b,f=f,a=a) for (b,f),a in self.a.items()],
                    states=ss,pairs=pairrows,polynomial=poly,deficit=deficit,
                    coefficients=[dict(s=s,coefficient=coeff[s]) for s in ss],
                    recovery=self.recover(next(s for s in ss if coeff[s]),edge(self.root,min(self.g[self.root]))) if pairs else None)

def check_cuts(g, counts):
    # Every size-three cut is a bond. Check caps independently of rootings.
    bad=[]
    for es in combinations(list(g.edges()),3):
        h=g.copy(); h.remove_edges_from(es)
        parts=list(nx.connected_components(h))
        if len(parts)==1: continue
        assert len(parts)==2
        counts['three_cuts']+=1
        if min(map(len,parts))==1: continue
        bad.append(es)
        colors=nx.bipartite.color(g)
        capcycles=[]
        for S in parts:
            ends=[next(v for v in e if v in S) for e in es]
            assert len(set(ends))==3 and len({colors[v] for v in ends})==1
            cap=g.subgraph(S).copy(); z=max(g)+1
            cap.add_edges_from((z,v) for v in ends)
            assert nx.is_bipartite(cap) and all(d==3 for _,d in cap.degree())
            assert nx.check_planarity(cap)[0] and nx.edge_connectivity(cap)==3
            counts['caps']+=1
            cycles=[]
            for P in perfect_matchings(cap):
                C=cap.copy(); C.remove_edges_from(P)
                if nx.is_connected(C):
                    unused=next(v for v in ends if edge(z,v) in P)
                    index=next(i for i,e in enumerate(es) if unused in e)
                    cycles.append((index,{edge(*e) for e in C.edges() if z not in e}))
            assert {i for i,_ in cycles}=={0,1,2}
            capcycles.append(cycles)
        for i,C in capcycles[0]:
            for j,D in capcycles[1]:
                if i!=j: continue
                h=nx.Graph(); h.add_nodes_from(g)
                h.add_edges_from(C|D|{edge(*e) for k,e in enumerate(es) if k!=i})
                assert nx.is_connected(h) and all(d==2 for _,d in h.degree())
                counts['glued_cycles']+=1
    return bad

def perfect_matchings(g):
    def rec(left,chosen):
        if not left: yield set(chosen); return
        v=min(left)
        for w in sorted(set(g[v])&left):
            yield from rec(left-{v,w},chosen+[edge(v,w)])
    return rec(set(g),[])

def general_checks(g,counts):
    p=Primal(g,min(g)); V=set(g)
    if len(g)<=12:
        for mask in range(1,1<<(len(g)-1)):
            S={v for v in g if mask>>v&1}
            if not nx.is_connected(g.subgraph(S)) or not nx.is_connected(g.subgraph(V-S)): continue
            es=[e for e in p.edges if len(set(e)&S)==1]
            links=nx.Graph(); links.add_edges_from(p.ef[e] for e in es)
            assert nx.is_connected(links) and all(d==2 for _,d in links.degree())
            U=set().union(*(set(p.inc[v]) for v in S))
            EA=[e for e in p.edges if set(e)&S]
            assert len(S)+len(U)==len(EA)+1
            assert {f for f,vs in enumerate(p.faces) if set(vs)&S and set(vs)-S}==set(links)
            counts['general_bonds']+=1
    avoided=set()
    for P in perfect_matchings(g):
        counts['primal_perfect_matchings']+=1
        C=g.copy(); C.remove_edges_from(P)
        parts=list(nx.connected_components(C))
        if len(parts)==1: avoided|=P
        for mask in range(1,1<<len(parts)):
            S=set().union(*(parts[i] for i in range(len(parts)) if mask>>i&1))
            es=[e for e in p.edges if len(set(e)&S)==1]
            assert set(es)<=P
            assert len(es)==2*sum(p.bend[e] in S for e in es)
            counts['matching_cut_balances']+=1
    assert avoided==set(p.edges)

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--max-order',type=int,default=20)
    args=parser.parse_args(); counts=Counter(); manifest=[]; examples={}
    graphs=[('cube',named_graphs()['cube'])]
    # Generation may use triangulations, but every tested object below is rebuilt
    # from G. No lab proof function or dual state object is used.
    exe=ROOT/'workings/barnette_lab/vendor/plantri.exe'
    if exe.exists():
        for v in range(6,args.max_order//2+3):
            for j,t in enumerate(plantri_graphs(v,exe)):
                _,emb=nx.check_planarity(t); fs,sides=faces_of(emb)
                g=nx.Graph(); g.add_nodes_from(range(len(fs)))
                g.add_edges_from((sides[u,w],sides[w,u]) for u,w in t.edges())
                graphs.append((f'plantri_faces_{v}_{j}',g))
    else:
        graphs += [(f'prism_{k}',nx.circular_ladder_graph(k)) for k in range(6,args.max_order//2+1,2)]
    for name,gg in graphs:
        g=nx.convert_node_labels_to_integers(gg)
        general_checks(g,counts)
        cuts=check_cuts(g,counts)
        counts['graphs']+=1
        for root in g:
            p=Primal(g,root); result=p.check(counts)
            if not cuts: assert result['pairs']
            if name=='cube' and root==0: examples['cube']=result
            if 'cancellation' not in examples and any(c['coefficient']==0 and any(row['s']==c['s'] for row in result['pairs']) for c in result['coefficients']):
                examples['cancellation']=result; examples['cancellation']['name']=name
        manifest.append(dict(name=name,order=len(g),edges=sorted(edge(*e) for e in g.edges()),nontrivial_cuts=len(cuts)))
        print(name,len(g),dict(counts),flush=True)
    (HERE/'outputs').mkdir(exist_ok=True)
    (HERE/'outputs/summary.json').write_text(json.dumps(dict(command=f'python research/2026-11-14_astra_primal-proof/check_primal.py --max-order {args.max_order}',counts=counts,manifest=manifest),indent=2))
    for name,data in examples.items(): (HERE/f'outputs/{name}.json').write_text(json.dumps(data,indent=2))
    assert 'cancellation' in examples, 'Increase the generation range to include cancellation'

if __name__=='__main__': main()
