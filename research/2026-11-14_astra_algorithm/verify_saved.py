"""Independent primal certificate replay and direct small-prefix enumeration.

Does not call any lab checker, matching enumerator or recovery method.
"""
import json, itertools
from pathlib import Path
import networkx as nx
BASE=Path(__file__).resolve().parent


def primal(case):
    # Rebuild the same face IDs from the recorded edge insertion order.
    t=nx.Graph(case['edges']);ok,emb=nx.check_planarity(t)
    if not ok:raise AssertionError('nonplanar')
    seen=set();faces=[];side={}
    for u,v in emb.edges():
        if (u,v) in seen:continue
        f=emb.traverse_face(u,v,seen);i=len(faces);faces.append(f)
        for a,b in zip(f,f[1:]+f[:1]):side[a,b]=i
    edges={frozenset((side[u,v],side[v,u])) for u,v in t.edges()}
    return set(range(len(faces))),edges


def check(vertices,edges,cycle,forbidden):
    if len(cycle)!=len(vertices) or set(cycle)!=vertices:raise AssertionError('vertex certificate')
    es=[frozenset((a,b)) for a,b in zip(cycle,cycle[1:]+cycle[:1])]
    if not all(e in edges for e in es) or frozenset(forbidden) in es:raise AssertionError('edge certificate')


counts={}
for campaign in ('census','families','hybrid','hunt'):
    path=BASE/f'{campaign}.jsonl'
    if not path.exists():continue
    cases={c['name']:c for c in json.loads((BASE/f'{campaign}-instances.json').read_text())}
    count=0
    for line in path.read_text().splitlines():
        row=json.loads(line)
        if row['status']!='ok':continue
        vertices,edges=primal(cases[row['name']]);check(vertices,edges,row['cycle'],row['forbidden']);count+=1
    counts[campaign]=count
if (BASE/'marked-chains.jsonl').exists():
    cases={c['name']:c for c in json.loads((BASE/'marked-chain-instances.json').read_text())}
    records=[json.loads(s) for s in (BASE/'marked-chains.jsonl').read_text().splitlines()]
    if (BASE/'marked-chain-eight.json').exists():records.append(json.loads((BASE/'marked-chain-eight.json').read_text()))
    count=0
    for row in records:
        if row['status']!='ok':continue
        vertices,edges=primal(cases[row['name']]);check(vertices,edges,row['cycle'],row['forbidden']);count+=1
    counts['marked-chains']=count
for fn in ('prefix-counterexample.json','filtered-prefix-counterexample.json'):
    d=json.loads((BASE/fn).read_text());faces=d['faces'];A=d['A'];R=set(faces[d['root']]);X=set(sum(faces,[]))-R
    h=nx.Graph((('f',t),('v',v)) for t in A+[d['root']] for v in faces[t])
    choices=[set(faces[t])&X for t in A];ss=[];good=[];k=len(d['prefix'])
    for s in itertools.product(*choices):
        if len(set(s))!=len(X):continue
        ss.append(s);hh=h.copy();hh.remove_edges_from((('f',t),('v',v)) for t,v in zip(A,s))
        if nx.is_tree(hh):good.append(s)
    assert set(good)==set(map(tuple,d['good_states']))
    extensions=[s for s in ss if list(s[:k])==d['prefix']]
    assert extensions and not any(list(s[:k])==d['prefix'] for s in good)
    h.remove_edges_from((('f',t),('v',v)) for t,v in zip(A,d['prefix']))
    assert nx.is_connected(h)
    filtered=[]
    for s in extensions:
        if all(nx.is_connected(nx.restricted_view(h,[],[(('f',t),('v',v))])) for t,v in zip(A[k:],s[k:])):filtered.append(s)
    if fn.startswith('filtered'):assert filtered
    counts[fn]=dict(states=len(ss),good=len(good),extensions=extensions,individually_compatible_extensions=filtered)
(BASE/'independent-checks.json').write_text(json.dumps(counts,indent=2));print(json.dumps(counts,indent=2))
