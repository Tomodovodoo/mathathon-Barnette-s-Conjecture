from audit import *
from functools import lru_cache

def gluing():
    calls=Counter()
    @lru_cache(None)
    def solve(es,root,e0):
        t=Tri(es=es,outer=root); bad=t.obstructed(); calls['pieces']+=1
        if not bad:
            P=next(t.partitions(e0)); h=t.g.edge_subgraph(P).copy(); h.add_nodes_from(t.g)
            return frozenset(nx.node_connected_component(h,e0[0]))
        c=set(bad[0]); comps=list(nx.connected_components(t.g.subgraph(set(t.g)-c)))
        outside=next(C for C in comps if C&(t.R-c)); inside=set(t.g)-c-outside
        og=t.g.subgraph(outside|c); ig=t.g.subgraph(inside|c)
        U=solve(tuple(sorted(edge(a,b) for a,b in og.edges())),tuple(sorted(root)),e0)
        mono=next(edge(a,b) for a,b in combinations(c,2) if (a in U)==(b in U))
        W=solve(tuple(sorted(edge(a,b) for a,b in ig.edges())),tuple(sorted(c)),mono)
        if mono[0] not in U: W=frozenset(ig)-W
        whole=U|W
        assert nx.is_tree(t.g.subgraph(whole)) and nx.is_tree(t.g.subgraph(set(t.g)-whole))
        calls['glued']+=1
        return whole
    roots=0
    for N in range(6,15):
        for rot in json.loads((OPUS/f'code/data/eul_{N}.json').read_text()):
            t=Tri(rot=rot); es=tuple(sorted(edge(a,b) for a,b in t.g.edges()))
            for f in t.fs:
                for e0 in combinations(sorted(f),2):
                    U=solve(es,tuple(sorted(f)),edge(*e0)); V=set(t.g)-U
                    assert set(e0)<=U and next(v for v in f if v not in e0) in V
                    assert nx.is_tree(t.g.subgraph(U)) and nx.is_tree(t.g.subgraph(V)); roots+=1
    save('gluing.json',{'prescriptions_checked':roots,'unique_recursive_calls':dict(calls),'base_solver':'fresh exhaustive induced-tree partition enumeration, not the source matching constructor'})

def weights():
    import random
    rng=random.Random(1492)
    for rot in json.loads((OPUS/'code/data/eul_14.json').read_text()):
        base=Tri(rot=rot)
        for outer in range(len(base.fs)):
            t=Tri(rot=rot,outer=outer); ss=t.states(); ps=t.pairs(ss)
            if not ps or min(len(t.dc(r,s)) for r,s in ps)!=1: continue
            es=[(f,v) for f in t.A for v in set(t.fs[f])&t.X]
            trees=[]
            for s in ss:
                if not t.tree(s): continue
                r=next(r for r,sp in ps if sp==s)
                J=sum(1 if t.sides[a,b] in t.black else -1 for a,b in zip(r,s))//3
                sign=1 if ((J-t.n)//2)%2==0 else -1; trees.append((s,sign))
            linear=[sum(sign for s,sign in trees if s[t.A.index(f)]==v) for f,v in es]
            if not any(linear): continue
            pivot=next(j for j,v in enumerate(linear) if v)
            for trial in range(60):
                raw=[rng.randint(-3,3) for e in es]; w=[v*linear[pivot] for v in raw]
                w[pivot]=-sum(linear[j]*raw[j] for j in range(len(es)) if j!=pivot)
                poly=Counter()
                for s,sign in trees: poly[sum(w[es.index((f,v))] for f,v in zip(t.A,s))]+=sign
                poly={ex:co for ex,co in poly.items() if co}
                if poly:
                    assert sum(poly.values())==sum(ex*co for ex,co in poly.items())==0
                    allpoly=Counter()
                    for r,s in ps:
                        J=sum(1 if t.sides[a,b] in t.black else -1 for a,b in zip(r,s))//3
                        sign=1 if ((J-t.n)//2)%2==0 else -1
                        allpoly[sum(w[es.index((f,v))] for f,v in zip(t.A,s))]+=sign
                    assert {ex:co for ex,co in allpoly.items() if co}==poly
                    save('weights-leading-zero.json',{'V':14,'rot':rot,'outer':outer,'root':t.fs[outer],'cmin':1,'spoke_weights':[[list(t.fs[f]),v,w0] for (f,v),w0 in zip(es,w) if w0],'normalized_Z_laurent_coefficients':poly,'constant_Taylor_coefficient':0,'linear_Taylor_coefficient':0,'Z_is_identically_zero':False})
                    return
    raise AssertionError('No witness found')

if __name__=='__main__': globals()[sys.argv[1]]()
