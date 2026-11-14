from audit import *
import sympy as sp

def pair_from_u(t,u):
    u={frozenset(f):v for f,v in u}; selected=[]
    for i in t.A:
        selected.extend([((0,i),(1,v)) for v in t.fs[i] if v!=u[frozenset(t.fs[i])]])
    h=nx.Graph(selected); assert all(d==2 for v,d in h.degree())
    r={}; s={}
    for cyc in nx.cycle_basis(h):
        assert len(cyc)%2==0
        for j,(a,b) in enumerate(zip(cyc,cyc[1:]+cyc[:1])):
            f,v=(a[1],b[1]) if a[0]==0 else (b[1],a[1])
            (r if j%2==0 else s)[f]=v
    return tuple(r[i] for i in t.A),tuple(s[i] for i in t.A)

def coordinates(t):
    R=list(t.fs[t.outer]); vs=sorted(t.X); ids={v:i for i,v in enumerate(vs)}
    L=sp.zeros(len(vs)); rhs=sp.zeros(len(vs),2)
    fixed={R[0]:(0,0),R[1]:(1,0),R[2]:(0,1)}
    for v in vs:
        j=ids[v]; L[j,j]=t.g.degree(v)
        for w in t.g[v]:
            if w in ids: L[j,ids[w]]=-1
            else:
                for k in [0,1]: rhs[j,k]+=fixed[w][k]
    sol=L.inv()*rhs
    pos={v:tuple(map(sp.Rational,p)) for v,p in fixed.items()}
    pos.update({v:tuple(sol[ids[v],k] for k in [0,1]) for v in vs})
    return pos

def cycle_test(t,r,s,matching=False):
    pos=coordinates(t); xy={(1,v):p for v,p in pos.items()}
    for f in t.A: xy[0,f]=tuple(sum(pos[v][k] for v in t.fs[f])/3 for k in [0,1])
    d=nx.DiGraph(); d.add_nodes_from(xy)
    for f,a,b in zip(t.A,r,s):
        used={a,b}
        for v in t.fs[f]:
            if matching: forward=v!=a
            else: forward=v in used
            x,y=((0,f),(1,v)) if forward else ((1,v),(0,f))
            p,q=xy[x],xy[y]; d.add_edge(x,y,area=p[0]*q[1]-p[1]*q[0])
    result={}
    for name,sign in [('has_ccw_cycle',-1),('has_cw_cycle',1)]:
        for a,b in d.edges(): d[a][b]['weight']=sign*d[a][b]['area']
        result[name]=nx.negative_edge_cycle(d,weight='weight')
        if not result[name]:
            # Source edges of weight zero ensure all vertices reachable.
            dd=d.copy(); dd.add_edges_from(('source',v,{'weight':0}) for v in d)
            dist=nx.single_source_bellman_ford_path_length(dd,'source')
            assert all(dd[a][b]['weight']+dist[a]-dist[b]>=0 for a,b in d.edges())
            result[name+'_potential']={str(v):str(dist[v]) for v in d}
    return result

def large():
    names=['ef_fail_40_40','alpha_min_fail_40_41','alpha_max_fail_80_83','strongviol_50_seed50','deeptrap_50_1']
    results=[]
    for name in names:
        t,d=from_example(OPUS/f'code/data/{name}.json')
        if 'u' in d: r,s=pair_from_u(t,d['u'])
        else:
            rmap={frozenset(f):v for f,v in d['r']}; smap={frozenset(f):v for f,v in d['s']}
            r=tuple(rmap[frozenset(t.fs[f])] for f in t.A); s=tuple(smap[frozenset(t.fs[f])] for f in t.A)
        assert t.valid(r) and t.valid(s) and all(a!=b for a,b in zip(r,s))
        cs=t.dc(r,s); row={'name':name,'V':len(t.g),'separating_black_triangles':t.obstructed(),'D_cycle_lengths':list(map(len,cs)),'k_s':t.k(s),'k_r':t.k(r)}
        if 'u' in d:
            candidates=[]
            for mask in range(1<<len(cs)):
                rr=list(r); ss=list(s)
                for j,c in enumerate(cs):
                    if mask>>j&1:
                        for i in c: rr[i],ss[i]=ss[i],rr[i]
                candidates.append((tuple(rr),tuple(ss)))
            row['orientations']=len(candidates); row['tree_seconds']=sum(t.tree(ss) for rr,ss in candidates)
            row['exact_cycle_extremality']=cycle_test(t,r,s)
            assert row['tree_seconds']==0
        else:
            # Q components determine every mate. Enumerate by independent tail assignment.
            q=t.Q(s); cb=nx.cycle_basis(q); mates=[]
            for bits in range(1<<len(cb)):
                rr=list(r)
                for j,c in enumerate(cb):
                    if bits>>j&1:
                        for a,b in zip(c,c[1:]+c[:1]):
                            i=next(i for i,f in enumerate(t.A) if set(t.fs[f])-{s[i]}=={a,b})
                            rr[i]=next(iter(set(t.fs[t.A[i]])-{r[i],s[i]}))
                mates.append(tuple(rr))
            moves=[]; details=[]; cycverts=set(v for c in nx.cycle_basis(q) for v in c)
            for rr in mates:
                for c in t.dc(rr,s):
                    ss=list(s)
                    for i in c: ss[i]=rr[i]
                    moves.append(t.k(ss))
                    details.append({'D_length':len(c),'meets_Q_cycle':bool({rr[i] for i in c}&cycverts),'new_k':t.k(ss),'current_mate':rr==r})
            row['mates']=len(mates); row['all_swap_k']=moves
            row['swap_details']=details
            if name.startswith('deep'):
                assert min(moves)==row['k_s']
                start=(r,s); todo=deque([(start,0)]); seen={start}; found=None
                while todo:
                    p,dist=todo.popleft()
                    if t.k(p[1])==0: found=dist; break
                    if dist==5: continue
                    for pp in t.neighbors(p):
                        if pp not in seen and t.k(pp[1])<=t.k(p[1]): seen.add(pp); todo.append((pp,dist+1))
                row['nonincreasing_distance_at_most_5']=found
        results.append(row); save('large-counterexamples.json',results)

def lattice():
    rows=[]
    for N in [10,12]:
        for gi,rot in enumerate(json.loads((OPUS/f'code/data/eul_{N}.json').read_text())):
            base=Tri(rot=rot)
            for outer in range(len(base.fs)):
                t=Tri(rot=rot,outer=outer); ss=t.states()
                if not t.flow(): continue
                extrema=[]
                for s in ss:
                    tests=cycle_test(t,s,s,matching=True)
                    if not tests['has_ccw_cycle'] or not tests['has_cw_cycle']:
                        extrema.append({'state':s,'tree':t.tree(s),'no_ccw':not tests['has_ccw_cycle'],'no_cw':not tests['has_cw_cycle']})
                if any(not e['tree'] for e in extrema):
                    rows.append({'V':N,'graph':gi,'outer':outer,'rot':rot,'root_face':t.fs[t.outer],'bounded_black_faces':[t.fs[f] for f in t.A],'extremes':extrema})
        save('matching-extremes.json',rows)

def fable():
    text=(ROOT/'research/2026-11-14_fable_route-combinatorics/data/counterexamples.txt').read_text()
    part=text.split('E3 refuted: a cycle cover D with no forest pair among its orientations')[1]
    fs=ast.literal_eval(part.split('faces (counterclockwise):\n')[1].splitlines()[0].strip())
    t=Tri(fs=fs,outer=8); ss=t.states(); pairs=t.pairs(ss)
    factors={}
    for r,s in pairs:
        u=tuple(next(iter(set(t.fs[f])-{a,b})) for f,a,b in zip(t.A,r,s))
        factors.setdefault(u,[]).append((r,s))
    bad=[p for ps in factors.values() if not any(t.tree(s) for r,s in ps) for p in ps]
    assert len(bad)==2
    rev={p:[] for p in pairs}
    for p in pairs:
        for q in t.neighbors(p):
            if t.k(q[1])<=t.k(p[1]): rev[q].append(p)
    good={p for p in pairs if t.k(p[1])==0}; todo=list(good)
    while todo:
        for p in rev[todo.pop()]:
            if p not in good: good.add(p); todo.append(p)
    assert len(good)==len(pairs)
    save('fable16.json',{'V':16,'faces':fs,'outer':8,'states':len(ss),'pairs':len(pairs),'tree_matchings':sum(t.tree(s) for s in ss),'factors':len(factors),'bad_factor_orientations':[{'r':r,'s':s,'k_s':t.k(s),'D_lengths':list(map(len,t.dc(r,s)))} for r,s in bad],'D3_all_pairs_pass':True})

if __name__=='__main__': globals()[sys.argv[1]]()
