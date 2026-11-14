"""Secondary tests after exact.json: root locations, LP witnesses and chain drift."""
from explore import *
from scipy.optimize import linprog, minimize

def tests():
    first_nonreal=None;first_offcircle=None;first_linear=None;rows=[]
    for V in range(6,15):
        for k,g in enumerate(plantri_graphs(V,ROOT/'workings/barnette_lab/vendor/plantri.exe')):
            b=Instance(g);ss=list(b.states());ps=b.pairs(ss)
            if not ps:continue
            z=sp.Symbol('z');a=b.weights();poly=b.polynomial(ps);P=sum(v*z**j for j,v in poly.items());P=sp.cancel(P/z**min(poly))
            linear=sp.expand(sum(b.sign(r,s)*sp.prod(1+z*a[t,v] for t,v in zip(b.A,s)) for r,s in ps))
            def nonreal(p):
                return any(abs(v.imag)>1e-6 for v in np.roots([float(v) for v in sp.Poly(p,z).all_coeffs()]))
            if first_nonreal is None and nonreal(P):first_nonreal={'V':V,'index':k,'factor':str(sp.factor(P))}
            rr=np.roots([float(v) for v in sp.Poly(P,z).all_coeffs()])
            if first_offcircle is None and any(abs(abs(v)-1)>1e-5 for v in rr):first_offcircle={'V':V,'index':k,'factor':str(sp.factor(P)),'edges':list(g.edges())}
            if first_linear is None and nonreal(linear):first_linear={'V':V,'index':k,'factor':str(sp.factor(linear)),'edges':list(g.edges())}
            rows.append({'V':V,'index':k,'factor':str(sp.factor(P)),'linear':str(sp.factor(linear))})
    out={'first_nonreal':first_nonreal,'first_offcircle':first_offcircle,'first_linear_nonreal':first_linear,'rows':rows}
    (OUT/'data/roots.json').write_text(json.dumps(out,indent=2));print({k:v for k,v in out.items() if k!='rows'})
    # Explicit convex mixture of white trees giving half-pair expectations, cube/prism.
    lp=[]
    for name,b in [('cube',Instance.from_primal(nx.cubical_graph())),('hexagonal_prism',Instance.from_primal(nx.circular_ladder_graph(6)))]:
        es=white_edges(b);ss=list(b.states());r,s=b.pairs(ss)[0];used={(t,v) for t,v in zip(b.A,r)}|{(t,v) for t,v in zip(b.A,s)}
        support=[e for e in es if e[:2] in used];trees=[]
        for ids in itertools.combinations(range(len(support)),b.n):
            h=nx.MultiGraph();h.add_nodes_from(b.white);h.add_edges_from((support[i][2],support[i][3]) for i in ids)
            if nx.is_tree(h):trees.append(ids)
        M=np.array([[int(i in ids) for ids in trees] for i in range(len(support))]+[[1]*len(trees)])
        res=linprog(np.zeros(len(trees)),A_eq=M,b_eq=[.5]*len(support)+[1],bounds=(0,None),method='highs')
        lp.append({'name':name,'edges':support,'feasible':res.success,'mixture':[{'prob':float(p),'indices':ids} for p,ids in zip(res.x,trees) if p>1e-8]})
    (OUT/'data/lp.json').write_text(json.dumps(lp,indent=2))
if __name__=='__main__':tests()
