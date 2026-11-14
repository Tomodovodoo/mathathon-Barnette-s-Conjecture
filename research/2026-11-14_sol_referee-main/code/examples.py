"""Verify every explicitly labelled state, cycle, row, and auxiliary example."""
from check import *

def main():
    raw=json.loads((ROOT/'paper/figures/running.json').read_text()); m=M(raw['faces'],raw['t0'])
    ss=m.states(); labels=[tuple(sorted(m.f[t])) for t in m.A]
    printed=[(0,1,6),(0,2,3),(1,7,8),(1,2,9),(3,4,9),(4,10,11),(5,6,11),(6,7,12),(8,11,12),(8,9,10)]
    assert labels==printed
    alpha=(1,3,7,2,9,11,6,12,8,10); beta=(6,2,8,1,3,10,11,7,12,9)
    assert alpha in ss and beta in ss and m.good(beta) and not m.good(alpha)
    assert sorted(sorted(c) for c in nx.connected_components(graph(m.V,m.q(beta))))==[[0,1,3,7],[2,4,8,9,10,11],[5,6,12]]
    assert {frozenset(c) for c in nx.cycle_basis(graph(m.V,m.q(alpha)))}=={frozenset([1,8,9])}
    P=m.select(beta,(0,4))
    assert sorted(sorted(c) for c in nx.connected_components(graph(m.V,P)))==[[0,2,4,6,7,8],[1,3,5,9,10,11,12]]
    d=m.disk([6,1,2,3,9,10,11]); assert [d[k] for k in ['ccw','h','I','B','W','ell']]==[True,7,3,5,6,2]
    assert d['interior']==[7,8,12]
    tri=m.disk([8,7,12]); assert not tri['ccw'] and tri['W']==1
    pairs=[(r,s) for r in ss for s in ss if all(a!=b for a,b in zip(r,s))]
    rows=[]
    for r,s in pairs:
        ds=sorted((m.disk(c) for c in cycles(list(zip(r,s)))),key=lambda x:-x['h'])
        rows.append([ds[0]['W'],ds[1]['W'],ds[0]['ccw'],ds[1]['ccw'],m.eps(r,s),m.weight(s),m.good(s),s==alpha,s==beta])
    expected=[
        [6,1,False,False,1,-4,True,False,False],
        [6,1,False,True,-1,-3,True,False,True],
        [6,1,True,False,-1,2,False,True,False],
        [6,1,True,True,1,3,True,False,False],
        [3,1,False,False,1,-2,True,False,False],
        [3,1,False,True,-1,-1,True,False,False],
        [3,1,True,False,-1,1,True,False,False],
        [3,1,True,True,1,2,False,True,False]]
    assert sorted(rows)==sorted(expected)
    tilde=list(beta)
    for f,v,w in [((1,7,8),8,1),((1,2,9),1,9),((8,9,10),9,8)]:
        i=labels.index(f); assert tilde[i]==v; tilde[i]=w
    assert tuple(tilde) in ss and set(r for r,s in pairs if s==alpha)=={beta,tuple(tilde)}
    y=next(t for t,f in enumerate(m.f) if set(f)=={1,8,9})
    assert [set(m.f[t]) for t in m.paths[y]]==[{1,8,9},{1,7,8},{1,6,7},{0,1,6},{0,5,6},{0,4,5}]
    st=list(alpha)
    for i,v in enumerate(beta):
        if v in d['cycle']: st[i]=v
    assert m.eta(tuple(st),y)==-1 and m.eta(alpha,y)==0
    assert sum(min(2,len(set(m.f[t])&{2})) for t in m.A)==2
    Z=co.Counter()
    for r,s in pairs: Z[m.weight(s)]+=m.eps(r,s)

    raw=json.loads((ROOT/'paper/figures/octahedron.json').read_text()); oc=M(raw['faces'],raw['t0'])
    css=oc.states(); assert len(css)==2 and all(oc.good(s) for s in css)
    cp=[oc.select(s,(0,1)) for s in css]
    target={edge(3,5),edge(2,3),edge(0,4),edge(0,1)}
    assert target in cp
    cst=css[cp.index(target)]
    assert all(e in target for e in [(3,5),(2,3),(0,4)])
    assert sorted(sorted(c) for c in nx.connected_components(graph(oc.V,target)))==[[0,1,4],[2,3,5]]
    # Verify face-by-face rather than only the union.
    assert all(next(e for e in target if set(e)<=set(f))==e for f,e in [((1,3,5),(3,5)),((2,3,4),(2,3)),((0,4,5),(0,4))])

    # The two proof-of-necessity examples in the closing remarks.
    tri_bipyramid=nx.complete_multipartite_graph(2,1,1,1)
    ok,emb=nx.check_planarity(tri_bipyramid); assert ok
    seen=set(); faces=[]
    for a,b in emb.edges():
        if (a,b) not in seen: faces.append(emb.traverse_face(a,b,seen))
    incidence=nx.Graph()
    for t,f in enumerate(faces): incidence.add_edges_from((('v',v),('f',t)) for v in f)
    assert len(incidence)==11 and len(faces)==6 and nx.is_bipartite(incidence)
    assert nx.check_planarity(incidence)[0] and nx.node_connectivity(incidence)==3
    theta=nx.Graph(); theta.add_nodes_from(['a','b'])
    for j in range(3):
        cube=nx.cubical_graph(); cube.remove_edge(0,1)
        theta.add_edges_from(((j,u),(j,v)) for u,v in cube.edges())
        theta.add_edges_from([('a',(j,0)),('b',(j,1))])
    assert len(theta)==26 and all(d==3 for _,d in theta.degree())
    assert nx.is_bipartite(theta) and nx.check_planarity(theta)[0] and nx.node_connectivity(theta)==2
    assert nx.number_connected_components(theta.subgraph([v for v in theta if v not in ['a','b']]))==3
    # Roots with/without a pair in the 9-vertex double octahedron.
    fs=rotation_faces((OUT/'plantri-9.txt').read_text().splitlines()[0]); roots=[]
    for r in range(len(fs)):
        t=M(fs,r); states=t.states(); pp=[(a,b) for a in states for b in states if all(x!=y for x,y in zip(a,b))]
        roots.append(dict(root=r,black=sorted(t.B),pairs=len(pp)))
    assert any(a['black']==b['black'] and bool(a['pairs'])!=bool(b['pairs']) for a in roots for b in roots)
    # No smaller generated triangulation has a separating triangle.
    for n in [6,8]:
        fs=rotation_faces((OUT/f'plantri-{n}.txt').read_text().splitlines()[0]); t=M(fs,0)
        assert all(frozenset(c) in {frozenset(f) for f in fs} for c in it.combinations(t.V,3) if all(edge(a,b) in t.E for a,b in it.combinations(c,2)))
    result=dict(table2=expected,alpha=alpha,beta=beta,tilde_beta=tilde,figure5=d,figure9_heights=[-1,0],Q_beta=sorted(m.q(beta)),P_beta=sorted(P),signed_moments=[sum(m.eps(r,s)*m.weight(s)**j for r,s in pairs) for j in range(3)],Laurent_coefficients={str(k):v for k,v in sorted(Z.items()) if v},cube_state=cst,cube_selection=sorted(target),double_octahedron_roots=roots,necessity_examples=dict(incidence_vertices=11,incidence_classes=[5,6],theta_vertices=26,theta_connectivity=2))
    (OUT/'examples.json').write_text(json.dumps(result,indent=2)); print('Every explicit table entry, state, cycle, height, and auxiliary finite example checked.')

if __name__=='__main__': main()
