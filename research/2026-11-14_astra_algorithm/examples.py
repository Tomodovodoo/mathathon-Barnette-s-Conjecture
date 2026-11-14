"""Generate exact worked traces. Run from repository root with python -B."""
from experiments import *
from barnette_lab.algorithms import alpha,beta,pool


def example(name,b,e0):
    out=[f'### {name}', '',f'Dual face IDs are the following ordered triples. The outer face is {b.outer}; roots are {sorted(b.R)}; the prescribed dual side is {e0}.', '', '| Face | Corners | Colour |','|---|---|---|']
    for i,f in enumerate(b.faces):out.append(f'| {i} | {f} | {"black" if i in b.black else "white"} |')
    out+=['',f'The state coordinates below are in face order A={b.A}. Nonroots are {b.X}.']
    flow=b.flow_pair();out+=['',f'An integral value-{2*b.n} flow chooses r={flow[0]} and s={flow[1]}. Each X vertex and A face has degree two in their union. All other incidence arcs carry zero. Alternating each union cycle gives these two states.']
    pairs=b.pairs();p=next((p for p in pairs if not b.is_tree(p[1])),flow)
    out+=['',f'There are {len(list(b.states()))} states and {len(pairs)} pairs by exhaustive enumeration. For a nontrivial walk when available, start instead at r={p[0]}, s={p[1]}.', '',f'Its D cycles, specified by supplying faces, are {b.dcycles(*p)}. Its Q cycles are {b.qcycles(p[1])}.']
    a=b.weights();out+=['','Nonzero spoke weights `(face,corner,weight)` are '+str([(t,v,w) for (t,v),w in sorted(a.items()) if w])+'.', '',f'The signed polynomial in these weights is {b.polynomial()}, written as exponent-to-coefficient entries.']
    phase=0
    while True:
        phase+=1;cs=b.dcycles(*p);h=len(cs)
        out+=['',f'Phase {phase}, h={h}.']
        for c in cs:
            if sum(b.delta(p[0][b.A.index(t)],p[1][b.A.index(t)]) for t in c)==3:
                p=b.reverse_d(p,c);out.append(f'Normalize D cycle {c}: r={p[0]}, s={p[1]}.')
        tokens=tuple(pool(b,p,c,True)[len(pool(b,p,c,False))] for c in cs)
        obj=(p,tokens);assert alpha(b,obj)==obj
        out.append(f'Initial excess-rank tokens are {tokens}; alpha fixes this object.')
        done=False
        while True:
            z=beta(b,obj)
            if z==obj:out.append('Beta fixes the object: the second state is good.');done=True;break
            obj=z;out.append(f'Beta: r={obj[0][0]}, s={obj[0][1]}, tokens={obj[1]}; Q cycles {b.qcycles(obj[0][1])}.')
            z=alpha(b,obj)
            if z==obj:out.append(f'Alpha fixes the endpoint, with {len(b.dcycles(*obj[0]))} D cycles. Restart.');break
            obj=z;out.append(f'Alpha: r={obj[0][0]}, s={obj[0][1]}, tokens={obj[1]}; Q cycles {b.qcycles(obj[0][1])}.')
        p=obj[0]
        if done:break
    s=p[1];cert=b.recover(s,e0)
    out+=['',f'The opposite edges Q_s are {sorted(map(lambda e:edge(*e),b.Q(s).edges()))}.', '',f'The white tree is {cert["white_tree"]}, rooted at {cert["white_root"]}.','', '| Black face | Deleted corner | White edge | Child | Selected side |','|---|---|---|---|---|']
    tree=nx.Graph(cert['white_tree']);parent={child:par for par,child in nx.bfs_edges(tree,cert['white_root'])}
    for t,v in zip(b.A,s):
        sides={next(y for y in (b.sides[v,u],b.sides[u,v]) if y in b.white):edge(v,u) for u in b.faces[t] if u!=v}
        x,y=sides;child=x if parent.get(x)==y else y
        out.append(f'| {t} | {v} | {edge(x,y)} | {child} | {sides[child]} |')
    out+=['',f'Add e0={e0}. The selected sides are {cert["P"]}. The two induced-tree classes are {cert["classes"]}.', '',f'The primal cycle, using dual face IDs, is {cert["cycle"]}, closed back to its first vertex. The omitted edge is {cert["avoided_edge"]}. Each consecutive pair shares a side in the face table, and the list contains all {len(b.G)} face IDs exactly once. The independent primal checker accepts it.', '']
    assert verify(b.G,cert['cycle'],cert['avoided_edge'])
    return '\n'.join(out),cert


if __name__=='__main__':
    cube=Instance(nx.octahedral_graph())
    d=json.loads((ROOT/'paper/figures/running.json').read_text())
    g=graph_from_faces(d['faces']);b=Instance(g);b=Instance(g,next(i for i,f in enumerate(b.faces) if set(f)==set(d['faces'][d['t0']])))
    text=['## Worked examples','', 'These are exact, reproducible arithmetic traces, with every exchange and recovery choice listed. `examples.py` generates them from the input graphs; they are computed examples, not additional existence proofs. Neither example requires separator gluing.','']
    certs={}
    for name,ins,e in [('Cube',cube,edge(*cube.faces[cube.outer][:2])),('13-vertex running triangulation',b,tuple(d['e0']))]:
        s,cert=example(name,ins,e);text.append(s);certs[name]=cert
    (BASE/'worked-examples.md').write_text('\n'.join(text),encoding='utf-8')
    (BASE/'example-certificates.json').write_text(json.dumps(certs,indent=2))
    doc=ROOT/'proofs/algorithm/ALGORITHM.md'
    old=doc.read_text(encoding='utf-8')
    contents=old.split('\n## Worked examples')[0]
    tail='\n## Implementation of the bounded-width route'+old.split('\n## Implementation of the bounded-width route',1)[1] if '\n## Implementation of the bounded-width route' in old else ''
    doc.write_text(contents+'\n\n'+'\n'.join(text)+tail,encoding='utf-8')
