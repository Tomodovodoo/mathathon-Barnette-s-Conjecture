from audit import *
from counterexamples import pair_from_u,coordinates,cycle_test

def euler():
    nchecks=0; regiontypes=Counter()
    for N in range(6,13):
        for gi,rot in enumerate(json.loads((OPUS/f'code/data/eul_{N}.json').read_text())):
            t=Tri(rot=rot); vs=sorted(t.g)
            for mask in range(1,1<<N):
                U={v for j,v in enumerate(vs) if mask>>j&1}
                if len(U)<3: continue
                K=t.g.subgraph(U)
                if not nx.is_connected(K): continue
                cutdual=t.dual.copy(); cutdual.remove_edges_from(tuple(t.inc[edge(a,b)]) for a,b in K.edges())
                b=0; rhs=0; regions=[]
                for comp in nx.connected_components(cutdual):
                    if len(comp)==1 and set(t.fs[next(iter(comp))])<=U:
                        b+=next(iter(comp)) in t.black; continue
                    d=sum(z in comp for a,b0 in K.edges() for z in t.inc[edge(a,b0)])
                    beta=sum(1 if z in t.black else -1 for z in comp)
                    assert abs(3*beta)<=d and (beta-d)%2==0
                    rhs+=beta-(d-4); regiontypes[d,beta]+=1; regions.append([d,beta])
                assert 2*(len(K.edges())-b-2*len(U)+4)==rhs
                nchecks+=1
            print('Euler',N,gi,nchecks,flush=True)
    save('euler.json',{'connected_induced_subgraphs_checked':nchecks,'range':'all saved V=6..12 instances, all connected induced subsets of size at least 3','region_types':[[d,beta,n] for (d,beta),n in sorted(regiontypes.items())]})

def alpha_small():
    rows=[]; count=0
    for N in range(6,15):
        for gi,rot in enumerate(json.loads((OPUS/f'code/data/eul_{N}.json').read_text())):
            base=Tri(rot=rot)
            for outer in range(len(base.fs)):
                t=Tri(rot=rot,outer=outer); pairs=t.pairs(t.states())
                factor={tuple(next(iter(set(t.fs[f])-{a,b})) for f,a,b in zip(t.A,r,s)):(r,s) for r,s in pairs}
                demand={v:sum(v in t.fs[f] for f in t.A)-(0 if v in t.R else 2) for v in t.g}
                out=[]
                def rec(j,cur):
                    if j==t.n:
                        assert all(v==0 for v in demand.values()); out.append(tuple(cur)); return
                    f=t.A[j]
                    for v in t.fs[f]:
                        if demand[v]>0:
                            demand[v]-=1; rec(j+1,cur+[v]); demand[v]+=1
                rec(0,[]); assert set(out)==set(factor)
                extremes=[]
                if factor:
                    for u,(r,s) in factor.items():
                        ex=cycle_test(t,r,s)
                        if not ex['has_ccw_cycle'] or not ex['has_cw_cycle']:
                            trees=0
                            cs=t.dc(r,s)
                            for bits in range(1<<len(cs)):
                                ss=list(s)
                                for j,c in enumerate(cs):
                                    if bits>>j&1:
                                        for i in c: ss[i]=r[i]
                                trees+=t.tree(ss)
                            extremes.append({'no_ccw':not ex['has_ccw_cycle'],'no_cw':not ex['has_cw_cycle'],'trees':trees})
                    assert sum(e['no_ccw'] for e in extremes)==sum(e['no_cw'] for e in extremes)==1
                    assert any(e['trees'] for e in extremes)
                count+=len(factor); rows.append([N,gi,outer,len(factor),extremes])
            print('alpha small',N,gi,flush=True)
    save('alpha-small.json',{'factors':count,'roots':len(rows),'O6_joint_failures':0,'rows':rows})

def true_extreme(t,p,sign):
    pos=coordinates(t); xy={(1,v):p for v,p in pos.items()}
    for f in t.A: xy[0,f]=tuple(sum(pos[v][k] for v in t.fs[f])/3 for k in [0,1])
    r,s=p; d=nx.DiGraph(); d.add_nodes_from(xy)
    for f,a,b in zip(t.A,r,s):
        for v in t.fs[f]:
            x,y=((0,f),(1,v)) if v in [a,b] else ((1,v),(0,f)); d.add_edge(x,y)
    flips=0
    while True:
        for a,b in d.edges(): d[a][b]['weight']=sign*(xy[a][0]*xy[b][1]-xy[a][1]*xy[b][0])
        if not nx.negative_edge_cycle(d,weight='weight'): break
        for source in d:
            try: c=nx.find_negative_cycle(d,source,weight='weight'); break
            except nx.NetworkXError: pass
        es=list(zip(c,c[1:])); assert sum(d[a][b]['weight'] for a,b in es)<0
        d.remove_edges_from(es); d.add_edges_from((b,a) for a,b in es); flips+=1
        assert flips<10000
    u=[(list(t.fs[f]),next(v for v in t.fs[f] if d.has_edge((1,v),(0,f)))) for f in t.A]
    r,s=pair_from_u(t,u); cs=t.dc(r,s); assert len(cs)<=18
    trees=0
    for bits in range(1<<len(cs)):
        ss=list(s)
        for j,c in enumerate(cs):
            if bits>>j&1:
                for i in c: ss[i]=r[i]
        trees+=t.tree(ss)
    return {'flips':flips,'D_cycle_lengths':list(map(len,cs)),'tree_seconds':trees,'u':u}

def alpha_large():
    rows=[]
    for path in sorted((OPUS/'code/data').glob('alpha_*fail*.json')):
        t,d=from_example(path); p=pair_from_u(t,d['u'])
        ex1=true_extreme(t,p,-1); ex2=true_extreme(t,p,1)
        rows.append({'name':path.stem,'V':len(t.g),'minimum':ex1,'maximum':ex2})
        assert ex1['tree_seconds'] or ex2['tree_seconds']
        print('true extremes',path.stem,ex1['tree_seconds'],ex2['tree_seconds'],flush=True)
    save('alpha-large.json',{'instances':rows,'joint_failures':0})

if __name__=='__main__': globals()[sys.argv[1]]()
