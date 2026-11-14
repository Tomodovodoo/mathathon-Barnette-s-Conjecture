from audit import *
from functools import lru_cache
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint

def hcycles(g):
    # Enumerate perfect matchings from the definition, then connected complements.
    out=[]
    def rec(left,M):
        if not left:
            h=g.copy(); h.remove_edges_from(M)
            if nx.is_connected(h): out.append(frozenset(edge(a,b) for a,b in h.edges()))
            return
        v=min(left,key=lambda v:len(set(g[v])&left))
        for w in sorted(set(g[v])&left): rec(left-{v,w},M+[edge(v,w)])
    rec(set(g),[]); return out

def endpoint(g,a,b):
    vs=sorted(g); ids={v:i for i,v in enumerate(vs)}; adj=[sum(1<<ids[w] for w in g[v]) for v in vs]
    end=ids[b]; start=ids[a]; allmask=(1<<len(vs))-1
    @lru_cache(None)
    def rec(v,left):
        if not left: return v==end
        if v==end: return False
        choices=adj[v]&left
        while choices:
            bit=choices&-choices; choices-=bit; w=bit.bit_length()-1
            if w==end and left!=bit: continue
            if rec(w,left^bit): return True
        return False
    ans=rec(start,allmask^(1<<start)); rec.cache_clear(); return ans

def examples():
    result={}
    p=ASTRA/'examples'
    for q in range(1,7):
        t,d=from_example(p/f'rarity_{q}.json'); ss=t.states(); tm=[s for s in ss if t.tree(s)]
        assert len(ss)==3**q and len(tm)==2**q
        result[f'rarity_{q}']={'dual_V':len(t.g),'states':len(ss),'tree_matchings':len(tm),'root':list(t.R)}
        if q==1: result['local_prism']={'root':t.fs[t.outer],'bounded_black_faces':[t.fs[f] for f in t.A],'states':ss,'tree_flags':[t.tree(s) for s in ss]}
    t,d=from_example(p/'prism_recovery.json'); e0=edge(*d['e0']); ss=t.states(); tm=[s for s in ss if t.tree(s)]
    images={t.construct(s,e0) for s in tm}; parts=list(t.partitions(e0))
    result['prism']={'bounded_black_faces':[t.fs[f] for f in t.A],'states':ss,'tree_matchings':tm,'Q_forest':[nx.is_forest(t.Q(s)) for s in ss], 'Q_components':[[sorted(c) for c in nx.connected_components(t.Q(s))] for s in ss], 'images':len(images),'all_avoiding':len(parts),'e0':e0,'root':list(t.R)}
    assert len(images)==2 and len(parts)==4
    primal=nx.Graph(d['primal_edges']); forbidden=edge(*d['forbidden_primal_edge']); avoiding=[c for c in hcycles(primal) if forbidden not in c]
    assert set(map(frozenset,primal.edges()))==set(map(frozenset,t.dual.edges()))
    saved={frozenset(edge(*e) for e in c) for c in d['all_avoiding']}
    assert set(avoiding)==saved and len(avoiding)==4
    recovered={frozenset(edge(*t.inc[e]) for e in set(t.inc)-set(P)) for P in images}
    assert recovered=={frozenset(edge(*e) for e in rec['edges']) for rec in d['image']}
    result['prism']['saved_cycles_independently_verified']=True
    cube,_=from_example(p/'t6_0.json'); cps=cube.pairs(cube.states()); Js=[sum(1 if cube.sides[a,b] in cube.black else -1 for a,b in zip(r,s))//3 for r,s in cps]
    assert sorted(Js)==[-1,1] and sum((1j)**J for J in Js)==0
    result['zero_weights_cube']={'pairs':len(cps),'J':Js,'zero_sum':True,'constant_spoke_weights_give_equal_state_weights':True}
    d=json.loads((p/'P5_cube.json').read_text()); g=nx.Graph(d['primal_edges']); cs=hcycles(g); path=d['path']; pe={edge(a,b) for a,b in zip(path,path[1:])}
    assert not any(pe<=c for c in cs)
    result['P5_cube']={'hamiltonian_cycles':len(cs),'path':path,'vertex_5_neighbors':list(g[5]),'containing_cycles':0}
    # Non-bijective disk: recompute the signed boundary and disk face data.
    t,d=from_example(p/'nonbijective_disk.json'); cyc=d['cycle']; a={int(f):v for f,v in d['assignment'].items()}
    sigma=0; blocked=[]
    for u,v in zip(cyc,cyc[1:]+cyc[:1]):
        f=next(f for f in t.inc[edge(u,v)] if f in t.black)
        assert a[f]==u; sigma+=1 if t.sides[u,v] in t.black else -1
        blocked.append(edge(u,v))
    dual=t.dual.copy(); dual.remove_edges_from(tuple(t.inc[e]) for e in blocked)
    outside=nx.node_connected_component(dual,t.outer); disk=set(dual)-outside
    B=sum(f in t.black for f in disk); W=len(disk)-B
    verts=set(v for f in disk for v in t.fs[f]); I=len(verts-set(cyc)); ell=sum(next(f for f in t.inc[e] if f in t.black) in disk for e in blocked)
    result['nonbijective']={'delta_sum':sigma,'B':B,'W':W,'I':I,'ell':ell,'h':len(cyc),'repeated_values':[v for v,c in Counter(a.values()).items() if c>1]}
    assert sigma==0 and [B,W,I,ell]==[2,2,1,2]
    # Torus uses its supplied cellular faces, never a plane embedding.
    d=json.loads((p/'torus_3x3.json').read_text()); fs=d['black_faces']+d['white_faces']; g=nx.Graph(d['edges']); dual=nx.Graph(d['primal_edges']); cs=hcycles(dual)
    sidefaces={}; darts=Counter()
    for i,f in enumerate(fs):
        for a,b in zip(f,f[1:]+f[:1]): sidefaces.setdefault(edge(a,b),[]).append(i); darts[a,b]+=1
    assert set(sidefaces)=={edge(a,b) for a,b in g.edges()}
    assert all(len(owners)==2 and (owners[0]<9)!=(owners[1]<9) for owners in sidefaces.values())
    assert all(darts[a,b]==darts[b,a]==1 for a,b in sidefaces)
    assert {edge(a,b) for a,b in dual.edges()}=={edge(*owners) for owners in sidefaces.values()}
    for v in g:
        link=nx.Graph(tuple(w for w in f if w!=v) for f in fs if v in f)
        assert nx.is_connected(link) and set(dict(link.degree()).values())=={2}
    parts=[]
    for mask in range(1<<8):
        U={0}|{v for v in range(1,9) if mask>>(v-1)&1}; V=set(g)-U
        if V and nx.is_tree(g.subgraph(U)) and nx.is_tree(g.subgraph(V)): parts.append(sorted(U))
    assert not parts and len(cs)==36
    r=[f[0] for f in d['black_faces']]; s=[f[1] for f in d['black_faces']]
    assert len(set(r))==len(set(s))==9 and all(a!=b for a,b in zip(r,s))
    result['torus']={'V':len(g),'E':len(g.edges()),'F':len(fs),'degrees':sorted(dict(g.degree()).values()),'two_tree_partitions':len(parts),'dual_HCs':len(cs),'rooted_A':8,'rooted_X':6,'rootfree_Q_edges':9}
    # Noncubic example and theta separator.
    d=json.loads((p/'noncubic11.json').read_text()); g=nx.Graph(d['edges']); cc=nx.bipartite.color(g); size=Counter(cc.values())
    assert nx.check_planarity(g)[0] and nx.node_connectivity(g)==3 and sorted(size.values())==[5,6]
    result['noncubic']={'V':len(g),'E':len(g.edges()),'connectivity':3,'color_class_sizes':sorted(size.values())}
    d=json.loads((p/'theta_cube_26.json').read_text()); g=nx.Graph(d['edges']); h=g.copy(); h.remove_nodes_from([0,1]); assert nx.number_connected_components(h)==3
    assert nx.is_bipartite(g) and nx.check_planarity(g)[0] and nx.node_connectivity(g)==2 and set(dict(g.degree()).values())=={3}
    rootrows=[]
    triangles={int(v):list(f) for v,f in d['dual_triangles'].items()}; cc=nx.bipartite.color(g)
    for root in g:
        A=sorted(v for v in g if cc[v]==cc[root] and v!=root); X=set(v for f in triangles.values() for v in f)-set(triangles[root]); choices=[]
        def rec(i,used,s):
            if i==len(A): choices.append(tuple(s)); return
            for v in set(triangles[A[i]])&X-used: rec(i+1,used|{v},s+[v])
        rec(0,set(),[])
        pairs=sum(all(a!=b for a,b in zip(r,s)) for r in choices for s in choices)
        assert len(choices)==8 and pairs==0
        cycle_ranks=[]
        for s in choices:
            H=nx.Graph(((0,f),(1,v)) for f in triangles if cc[f]==cc[root] for v in triangles[f]); H.remove_edges_from(((0,f),(1,v)) for f,v in zip(A,s))
            assert not nx.is_connected(H); cycle_ranks.append(len(H.edges())-len(H)+nx.number_connected_components(H))
        row={'root':root,'states':8,'pairs':0,'cycle_ranks':cycle_ranks}
        if root==0:
            S=set(range(6,15)); assert S<=X
            deficit=2*len(S)-sum(min(2,len(set(triangles[f])&S)) for f in A)
            row['author_named_S']=sorted(S); row['named_S_deficit_with_saved_triangle_labels']=deficit
            cuts=[]; xx=sorted(X)
            for mask in range(1<<len(xx)):
                S={v for j,v in enumerate(xx) if mask>>j&1}
                cuts.append((2*len(S)-sum(min(2,len(set(triangles[f])&S)) for f in A),sorted(S)))
            best=max(v for v,S in cuts); row['maximum_capacity_deficit']=best; row['deficient_S']=next(S for v,S in cuts if v==best)
        rootrows.append(row)
    result['theta']={'connectivity':2,'components_after_0_1':3,'roots':rootrows}
    d=json.loads((p/'t9_0.json').read_text()); rootrows=[]
    for outer in [0,2]:
        t=Tri(fs=d['faces'],outer=outer); ss=t.states(); ps=t.pairs(ss)
        rootrows.append({'outer':outer,'root_face':t.fs[outer],'states':len(ss),'pairs':len(ps),'tree_matchings':sum(t.tree(s) for s in ss),'black_faces':t.black})
    assert rootrows[0]['black_faces']==rootrows[1]['black_faces']
    assert [(r['states'],r['pairs'],r['tree_matchings']) for r in rootrows]==[(4,4,4),(4,0,0)]
    result['root_dependence_t9']=rootrows
    save('limits-examples.json',result)

def reduction():
    rows=[]
    for name,path,key in [('cube','P5_cube.json','primal_edges'),('prism','prism_recovery.json','primal_edges'),('theta','theta_cube_26.json','edges')]:
        g=nx.Graph(json.loads((ASTRA/'examples'/path).read_text())[key]); cs=hcycles(g)
        tested=[]
        for a,b in g.edges():
            K=g.copy(); K.remove_edge(a,b); found=[]
            def rec(left,M):
                if not left:
                    h=K.copy(); h.remove_edges_from(M)
                    if nx.is_tree(h): found.append(M)
                    return
                v=min(left,key=lambda v:len(set(K[v])&left))
                for w in set(K[v])&left: rec(left-{v,w},M+[edge(v,w)])
            rec(set(K),[])
            assert bool(found)==any(edge(a,b) in c for c in cs)
            tested.append([edge(a,b),len(found)])
        rows.append({'name':name,'hamiltonian_cycles':len(cs),'edge_deletion_tests':tested})
    save('NP-reduction-small.json',rows)

def maxcuts():
    rows=[]
    for name in ['K4','BBL38','Tutte46']:
        d=json.loads((ASTRA/f'examples/{name}.json').read_text()); g=nx.Graph(d['edges']); vs=sorted(g); es=list(g.edges()); ids={v:i for i,v in enumerate(vs)}; n=len(vs); m=len(es)
        # Binary labels z_v and binary cut indicators y_e, y <= z_u+z_v and y <= 2-z_u-z_v.
        A=np.zeros((2*m,n+m)); upper=np.zeros(2*m)
        for j,(u,v) in enumerate(es):
            A[2*j,ids[u]]=A[2*j,ids[v]]=-1; A[2*j,n+j]=1
            A[2*j+1,ids[u]]=A[2*j+1,ids[v]]=1; A[2*j+1,n+j]=1; upper[2*j+1]=2
        obj=np.r_[np.zeros(n),-np.ones(m)]
        sol=milp(obj,integrality=np.ones(n+m),bounds=Bounds(0,1),constraints=LinearConstraint(A,-np.inf,upper),options={'time_limit':90,'mip_rel_gap':0})
        assert sol.success
        vals={v:int(round(sol.x[ids[v]])) for v in vs}; mono=[edge(u,v) for u,v in es if vals[u]==vals[v]]
        rows.append({'name':name,'maximum_cut':m-len(mono),'solver_gap':sol.mip_gap,'monochromatic_edges':mono,'coloring':vals})
    assert [r['maximum_cut'] for r in rows]==[4,50,60]; save('maxcuts.json',rows)

def strengthenings():
    rows=[]
    for path in sorted((ASTRA/'examples').glob('t[0-9]*_[0-9]*.json')):
        d=json.loads(path.read_text()); g=nx.Graph(d['primal_edges']); cs=hcycles(g); claimed=next(r for r in json.loads((ASTRA/'data/strengthenings.json').read_text()) if r['name']==path.stem)
        assert len(cs)==claimed['hamiltonian_cycles']
        es={edge(a,b) for a,b in g.edges()}; bad=[]
        for e in es:
            for f in es-{e}:
                if not any(e in c and f not in c for c in cs): bad.append([e,f])
        p4=[]
        for a in g:
            for b in g[a]:
                for c in set(g[b])-{a}:
                    for d0 in set(g[c])-{a,b}:
                        ps={edge(a,b),edge(b,c),edge(c,d0)}
                        if not any(ps<=C for C in cs): p4.append([a,b,c,d0])
        colors=nx.bipartite.color(g); ep=[]
        for a in g:
            for b in g:
                if colors[a]==0 and colors[b]==1 and not endpoint(g,a,b): ep.append([a,b])
        assert not bad and not p4 and not ep
        rows.append({'name':path.stem,'V':len(g),'HC':len(cs),'include_avoid_failures':bad,'P4_failures':p4,'opposite_endpoint_failures':ep})
        print('strengthening',path.stem,'done',flush=True)
    assert len(rows)==55; save('strengthenings.json',rows)

if __name__=='__main__': globals()[sys.argv[1]]()
