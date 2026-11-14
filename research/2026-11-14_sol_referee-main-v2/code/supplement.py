"""Extra exact checks, small census, and literal table/figure assertions."""
from verify_numbers import Audit, comps, edge, ROOT, OUT
from itertools import combinations, product
from collections import Counter, defaultdict
import subprocess, json, hashlib, math
import networkx as nx

def faces_from_rotation(line):
    n,rot=line.split(); rot=[[ord(v)-97 for v in row] for row in rot.split(',')]
    assert int(n)==len(rot)
    unseen={(v,w) for v,row in enumerate(rot) for w in row};faces=[]
    while unseen:
        start=min(unseen);v,w=start;f=[]
        while True:
            unseen.remove((v,w));f.append(v)
            v,w=w,rot[w][(rot[w].index(v)+1)%len(rot[w])]
            if (v,w)==start:break
        assert len(f)==3;faces.append(f)
    return faces

def detailed(a):
    checks=Counter();classes=defaultdict(list)
    for r,s in a.pairs:
        ds=[a.disk(c) for c in a.cycles(r,s)]
        c=len(ds);plus=sum(d['ccw'] for d in ds)
        assert (len(a.a)-c)%2==0
        assert a.sign(r,s)==(-1)**((len(a.a)+c)//2+plus)
        for d in ds:
            rr=list(r);ss=list(s)
            for j,v in enumerate(r):
                if v in d['cycle']:rr[j],ss[j]=ss[j],rr[j]
            assert (tuple(rr),tuple(ss)) in a.pairs
            assert a.sign(rr,ss)==-a.sign(r,s)
            for w in a.white:
                cut={a.dual[edge(x,y)] for x,y in zip(d['cycle'],d['cycle'][1:]+d['cycle'][:1])}
                h=a.g.copy();h.remove_edges_from(cut)
                inside=set(a.g)-nx.node_connected_component(h,a.t0)
                assert a.weight(ss,w)-a.weight(s,w)==(1 if not d['ccw'] else -1)*(w in inside)
            checks['D_reversals']+=1
        classes[tuple(sorted(edge(x,y) for x,y in zip(r,s)))].append((r,s))
    for s in a.states:
        partners=[r for r,ss in a.pairs if s==ss]
        if a.isgood(s):assert len(partners)==1
        elif partners:assert sum(a.sign(r,s) for r in partners)==0
        checks['state_partner_checks']+=1
    # All chosen-side systems, not just cycles that happen to belong to a pair.
    for s in a.states:
        choices=[sorted(set(a.f[t])-{v}) for t,v in zip(a.a,s)]
        for heads in product(*choices):
            nxt=dict(zip(s,heads));done=set()
            for start in s:
                if start in done:continue
                path=[];where={};v=start
                while v in nxt and v not in done and v not in where:
                    where[v]=len(path);path.append(v);v=nxt[v]
                if v in where:
                    d=a.disk(path[where[v]:])
                    assert d['B']==d['I']+d['ell'] and d['W']==d['B']+1 and d['h']==2*d['ell']+3
                    checks['chosen_cycles']+=1
                done.update(path)
            checks['chosen_side_systems']+=1
    # Verify the multivariate polynomial as a dictionary of monomials.
    actual=Counter(s for r,s in a.pairs for _ in [0])
    actual=Counter({s:sum(a.sign(r,ss) for r,ss in a.pairs if ss==s) for s in a.states})
    expanded=Counter()
    for pairs in classes.values():
        r,s=pairs[0];cycles=a.cycles(r,s);c=len(cycles)
        assert len(pairs)==2**c
        for signs in product([0,1],repeat=c):
            second=list(s);coef=(-1)**((len(a.a)-c)//2)
            for cyc,positive in zip(cycles,signs):
                d=a.disk(cyc)
                if not positive:coef=-coef
                for j,v in enumerate(r):
                    if v in cyc:second[j]=s[j] if d['ccw']==bool(positive) else r[j]
            expanded[tuple(second)]+=coef
    assert +actual==+expanded and {k:v for k,v in actual.items() if v}=={k:v for k,v in expanded.items() if v}
    # Every matching gives the primal-complement iff, and state recovery.
    for pm in a.matchings():
        selected={e for e,de in a.dual.items() if de in pm}
        forest=len(comps(a.v,selected))==len(a.v)-len(selected)
        h=a.g.copy();h.remove_edges_from(pm)
        assert nx.is_connected(h)==forest
        if forest:
            for prescribed in combinations(sorted(a.roots),2):
                prescribed=edge(*prescribed)
                if prescribed not in selected:continue
                q=nx.Graph();q.add_nodes_from(a.v);q.add_edges_from(selected-{prescribed})
                tail={}
                for region in nx.connected_components(q):
                    roots=set(region)&a.roots;assert len(roots)==1
                    root=next(iter(roots));dist=nx.single_source_shortest_path_length(q,root)
                    for x,y in q.subgraph(region).edges():tail[edge(x,y)]=x if dist[x]>dist[y] else y
                st=tuple(tail[next(e for e in selected if set(e)<=set(a.f[t]))] for t in a.a)
                assert st in a.states
                if st in a.good:
                    saved=a.e0;a.e0=prescribed
                    assert set(map(tuple,a.recover(st)['edges']))==selected
                    a.e0=saved
                checks['reverse_states']+=1
        checks['perfect_matching_iff_checks']+=1
    return dict(checks)

def main():
    summaries={}
    for name in ['octahedron','running']:
        d=json.loads((ROOT/f'paper/figures/{name}.json').read_text());a=Audit(d['faces'],d['t0'],d['e0'])
        summaries[name]=detailed(a)
        if name=='running':
            rows=sorted((next(x['W'] for x in [a.disk(c) for c in a.cycles(r,s)] if x['h']==7),tuple(a.disk(c)['ccw'] for c in sorted(a.cycles(r,s),key=lambda c:-len(c))),a.sign(r,s),a.weight(s),s in a.good) for r,s in a.pairs)
            expected=[]
            for L,weights in [(3,[-2,-1,1,2]),(6,[-4,-3,2,3])]:
                for orientations,w,eps in zip(product([False,True],repeat=2),weights,[1,-1,-1,1]):
                    expected.append((L,orientations,eps,w,not ((L==3 and orientations==(True,True)) or (L==6 and orientations==(True,False)))))
            assert rows==sorted(expected)
            summaries['table_and_eight_boxes']=rows
    prismfaces=[]
    for i in range(6):prismfaces.extend([(6,i,(i+1)%6),(7,(i+1)%6,i)])
    summaries['hexagonal_prism']=detailed(Audit(prismfaces,0,(0,1)))
    exe=ROOT/'workings/barnette_lab/vendor/plantri.exe'
    census=[]
    for n in range(6,13):
        p=subprocess.run([str(exe),'-b','-a',str(n)],capture_output=True,text=True,check=True)
        (OUT/f'plantri-{n}.txt').write_text(p.stdout+p.stderr,encoding='utf-8')
        roots=[]
        variations=[]
        for graph_index,line in enumerate(p.stdout.splitlines()):
            faces=faces_from_rotation(line)
            available=[]
            for t,f in enumerate(faces):
                a=Audit(faces,t,f[:2]);available.append(bool(a.pairs))
                roots.append(dict(graph_index=graph_index,root=t,pairs=len(a.pairs),states=len(a.states),good=len(a.good)))
            a=Audit(faces,0,faces[0][:2])
            variation=any(len({available[t] for t in color})>1 for color in [a.black,a.white])
            if variation:assert n>=9
            variations.append(variation)
        census.append(dict(order=n,classes=len(p.stdout.splitlines()),same_colour_root_variation=variations,rootings=roots))
    summaries['census']=census
    summaries['plantri_sha256']=hashlib.sha256(exe.read_bytes()).hexdigest()
    # The new short proofs of the two hypothesis counterexamples.
    fs=[(u,i,(i+1)%3) for u in [3,4] for i in range(3)]
    radial=nx.Graph();radial.add_nodes_from(range(5))
    for i,f in enumerate(fs):radial.add_edges_from((v,5+i) for v in f)
    assert len(radial)==11 and nx.node_connectivity(radial)==3 and nx.check_planarity(radial)[0]
    g=nx.Graph();g.add_nodes_from(range(26))
    for j in range(3):
        cube=nx.cubical_graph();u,v=next(iter(cube.edges()));cube.remove_edge(u,v)
        g.add_edges_from((8*j+x,8*j+y) for x,y in cube.edges());g.add_edge(24,8*j+u);g.add_edge(25,8*j+v)
    assert nx.is_bipartite(g) and nx.check_planarity(g)[0] and set(dict(g.degree()).values())=={3}
    assert nx.node_connectivity(g)==2
    h=g.copy();h.remove_nodes_from([24,25]);assert nx.number_connected_components(h)==3
    summaries['counterexamples']=dict(radial_order=len(radial),radial_connectivity=3,three_cubes_order=len(g),three_cubes_connectivity=2,components_after_two_deletions=3)
    # Read from the rendered gluing panels: (01,04,23,35) and (35,56,48,78).
    d=json.loads((ROOT/'paper/figures/octahedron.json').read_text())
    outer=[tuple(f) for i,f in enumerate(d['faces']) if i!=7]
    mapping={0:5,1:3,2:4,3:8,4:6,5:7}
    inner=[tuple(mapping[v] for v in f) for i,f in enumerate(d['faces']) if i!=0]
    a=Audit(outer+inner,0,(0,1))
    p1={edge(0,1),edge(0,4),edge(2,3),edge(3,5)}
    p2={edge(3,5),edge(5,6),edge(4,8),edge(7,8)}
    selected=p1|p2
    assert len(a.v)==9 and len(selected)==7
    assert all(sum(set(e)<=set(f) for e in selected)==1 for f in a.f)
    cc=comps(a.v,selected);assert cc==[[0,1,4,7,8],[2,3,5,6]]
    assert (p1&p2)=={(3,5)}
    summaries['gluing_figure']=dict(vertices=9,selected=sorted(selected),components=cc,outer=sorted(p1),inner=sorted(p2),intersection_edge=[3,5],other_intersection_vertex=4)
    (OUT/'supplement.json').write_text(json.dumps(summaries,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in summaries.items() if k not in ['census','table_and_eight_boxes']},indent=2))
    print('Census classes',[(c['order'],c['classes'],len(c['rootings'])) for c in census])
if __name__=='__main__':main()
