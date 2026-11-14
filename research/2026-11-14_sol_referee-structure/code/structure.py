from audit import *
import numpy as np
import sympy as sp

def matroids():
    rows=[]; mismatch=None
    for N in [6,8]:
        t=Tri(rot=json.loads((OPUS/f'code/data/eul_{N}.json').read_text())[0])
        es=[(f,v) for f in t.black for v in sorted(t.fs[f])]
        ct=Counter(); witnesses={}
        for S in combinations(es,t.n):
            pc={f for f,v in S}==set(t.A); pv={v for f,v in S}==t.X
            h=t.H.copy(); h.remove_edges_from(((0,f),(1,v)) for f,v in S)
            cg=nx.is_tree(h)
            q=nx.MultiGraph(); q.add_nodes_from([-1]+sorted(t.X))
            for f,v in S:
                a,b=set(t.fs[f])-{v}; q.add_edge(-1 if a in t.R else a,-1 if b in t.R else b)
            gr=nx.is_tree(q)
            if cg!=gr and mismatch is None and all(f in t.A and v in t.X for f,v in S): mismatch={'V':N,'spokes':S,'cographic':cg,'graphic_opposites':gr,'faces':{f:list(t.fs[f]) for f,v in S},'root':list(t.R)}
            for key,val in [('pc_pv',pc and pv),('cg_pc',cg and pc),('cg_pv',cg and pv),('gr_pc',gr and pc),('gr_pv',gr and pv),('TM',cg and pc and pv)]:
                if val: ct[key]+=1
            for name,ok in [('drop_cographic',pc and pv and not cg),('drop_centre',cg and pv and not pc),('drop_vertex',cg and pc and not pv)]:
                if ok and name not in witnesses: witnesses[name]=S
        rows.append({'V':N,'counts':dict(ct),'witnesses':witnesses})
    save('matroids.json',{'rows':rows,'not_a_matroid_isomorphism':mismatch})

def lp():
    # Read only the literal saved input, never the author's solver or code.
    line=next(l for l in (OPUS/'code/data/lp_13.txt').read_text().splitlines() if 'example fractional' in l)
    text=line.split('example fractional point: ',1)[1].replace('np.float64(0.5)','0.5')
    N,rot,t0,support=ast.literal_eval(text); t=Tri(rot=rot,outer=t0)
    es=[(f,v) for f in t.A for v in sorted(set(t.fs[f])&t.X)]
    idx={(frozenset(t.fs[f]),v):j for j,(f,v) in enumerate(es)}
    x=[sp.Rational(0)]*len(es)
    for (f,v),val in support: x[idx[frozenset(f),v]]=sp.Rational(1,2)
    wed=[]
    for f,v in es:
        zz=[next(z for z in t.inc[edge(v,a)] if z!=f) for a in t.fs[f] if a!=v]; wed.append(zz)
    # The author's dump records only fractional coordinates, omitting the 1s.
    # Recover a feasible integral completion independently by finite search.
    fracfaces={f for (face,v),val in support for f in t.A if set(t.fs[f])==set(face)}
    outside=[f for f in t.A if f not in fracfaces]
    feasible=[]
    for vals in product(*[sorted(set(t.fs[f])&t.X) for f in outside]):
        xx=x[:]
        for f,v in zip(outside,vals): xx[es.index((f,v))]=sp.Rational(1)
        if any(sum(xx[j] for j,(f,w) in enumerate(es) if w==v)!=1 for v in t.X): continue
        if any(sum(xx[j] for j,(a,b) in enumerate(wed) if a in S and b in S)>len(S)-1 for S in [{v for j,v in enumerate(t.white) if bits>>j&1} for bits in range(1,1<<len(t.white))]): continue
        feasible.append(xx)
    assert feasible
    x=feasible[0]
    active=[]; labels=[]
    for f in t.A:
        row=[int(ff==f) for ff,v in es]; assert sum(a*b for a,b in zip(row,x))==1
        active.append(row); labels.append(['centre',list(t.fs[f])])
    for v in sorted(t.X):
        row=[int(vv==v) for f,vv in es]; assert sum(a*b for a,b in zip(row,x))==1
        active.append(row); labels.append(['vertex',v])
    for j,v in enumerate(x):
        if not v:
            active.append([int(i==j) for i in range(len(es))]); labels.append(['zero',j])
    total=0; tight=0; minslack=None
    for bits in range(1,1<<len(t.white)):
        S={v for j,v in enumerate(t.white) if bits>>j&1}
        row=[int(a in S and b in S) for a,b in wed]
        slack=len(S)-1-sum(a*b for a,b in zip(row,x)); assert slack>=0
        minslack=slack if minslack is None else min(minslack,slack); total+=1
        if slack==0:
            active.append(row); labels.append(['white_subset',sorted(S)]); tight+=1
    rank=sp.Matrix(active).rank(); assert rank==len(es)
    ss=t.states(); supp=[s for s in ss if all(x[es.index((f,v))]>0 for f,v in zip(t.A,s))]
    print('LP support states',len(supp),'tree flags',[t.tree(s) for s in supp], 'feasible completions',len(feasible))
    assert len(supp)==2
    piv=sp.Matrix(active).T.rref()[1]
    completions=[{'integral_ones':[[list(t.fs[f]),v] for (f,v),val in zip(es,xx) if val==1],'support_tree_flags':[t.tree(s) for s in t.states() if all(xx[es.index((f,v))]>0 for f,v in zip(t.A,s))]} for xx in feasible]
    save('lp-certificate.json',{'V':N,'root_face':list(t.fs[t.outer]),'feasible_completions_of_missing_integral_coordinates':len(feasible),'all_integral_completions':completions,'bounded_black_faces':[t.fs[f] for f in t.A],'variables':[[list(t.fs[f]),v] for f,v in es], 'x':[str(v) for v in x], 'white_faces':{z:list(t.fs[z]) for z in t.white},'dual_edges':wed,'subset_inequalities_checked':total,'tight_subsets':tight,'active_rank':rank,'dimension':len(es),'independent_active_rows':[{'label':labels[i],'row':active[i]} for i in piv], 'support_states':supp,'support_states_are_tree':[t.tree(s) for s in supp]})

def contractions():
    counts=Counter(); reverse=[]; failed_lifts=[]; rootcases=0
    for N in range(8,14):
        for gi,rot in enumerate(json.loads((OPUS/f'code/data/eul_{N}.json').read_text())):
            base=Tri(rot=rot)
            for outer in range(len(base.fs)):
                t=Tri(rot=rot,outer=outer)
                for x in sorted(t.X):
                    if t.g.degree(x)!=4: continue
                    ns=list(map(int,t.rot[x]))
                    for j in [0,1]:
                        v1,a,v2,b=[ns[(i+j)%4] for i in range(4)]
                        if {v1,v2}&t.R:
                            rootcases+=1; continue
                        rename=lambda v:v1 if v==v2 else v
                        es={edge(rename(u),rename(v)) for u,v in t.g.edges() if x not in [u,v] and rename(u)!=rename(v)}
                        g=nx.Graph(es)
                        if len(g)!=N-2 or len(es)!=3*len(g)-6 or any(d%2 for v,d in g.degree()): continue
                        # Tri graph helper permits nonconsecutive vertex labels; Q is not used here.
                        small=Tri(es=es,outer=t.fs[outer]); ss=small.states()
                        blacknew=[f for f in t.A if x in t.fs[f]]; assert len(blacknew)==2
                        old=[f for f in t.A if f not in blacknew]
                        look={frozenset(small.fs[f]):i for i,f in enumerate(small.A)}
                        for sp0 in ss:
                            s=[None]*t.n
                            for f in old:
                                v=sp0[look[frozenset(rename(v) for v in t.fs[f])]]
                                s[t.A.index(f)]=v2 if v==v1 and v2 in t.fs[f] else v
                            unused=set(t.X)-set(s); assert len(unused)==2
                            options=[]
                            for vals in product(*[sorted(set(t.fs[f])&unused-{a,b}) for f in blacknew]):
                                if set(vals)==unused: options.append(vals)
                            assert len(options)==1
                            for f,v in zip(blacknew,options[0]): s[t.A.index(f)]=v
                            assert t.valid(s); counts['state_lifts']+=1
                            smalltree=small.tree(sp0); bigtree=t.tree(s)
                            if bigtree and not smalltree:
                                counts['tree_lift_from_nontree']+=1
                                if not reverse: reverse.append({'V':N,'rot':rot,'t0':list(t.fs[t.outer]),'x':x,'merge':[v1,v2],'small_faces':[small.fs[f] for f in small.A],'small_state':sp0,'large_faces':[t.fs[f] for f in t.A],'large_state':s})
                            if smalltree and not bigtree:
                                counts['failed_tree_lifts']+=1
                                if not failed_lifts: failed_lifts.append({'V':N,'rot':rot,'t0':list(t.fs[t.outer]),'x':x,'merge':[v1,v2],'small_faces':[small.fs[f] for f in small.A],'small_state':sp0,'large_faces':[t.fs[f] for f in t.A],'large_state':s})
                            if smalltree:
                                # Independent split-tree component test, including a fixed root path.
                                qe=nx.Graph(); qe.add_nodes_from(t.g)
                                for f in old:
                                    qe.add_edge(*tuple(set(t.fs[f])-{s[t.A.index(f)]}))
                                rr=sorted(t.R); qe.add_edges_from(zip(rr,rr[1:]))
                                chosenface=next(f for f in old if s[t.A.index(f)] in [v1,v2]); star=s[t.A.index(chosenface)]; other=v2 if star==v1 else v1
                                fx=next(f for f in blacknew if s[t.A.index(f)]==x); c2=next(v for v in t.fs[fx] if v not in [x,v1,v2])
                                side=nx.has_path(qe,c2,other)
                                assert side==bigtree; counts['conditional_iff_pass']+=1
                print('contract',N,gi,dict(counts),flush=True)
    save('contractions.json',{'counts':dict(counts),'root_merge_cases_excluded':rootcases,'counterexample_to_reverse_implication':reverse,'failed_tree_lift':failed_lifts})

if __name__=='__main__': globals()[sys.argv[1]]()
