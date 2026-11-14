"""Exact counts, all facial roots, installed plantri corpus. No source writes."""
import sys, json, math, argparse
from pathlib import Path
from collections import Counter
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT/'workings/barnette_lab'))
from barnette_lab.core import Instance, plantri_graphs, named_graphs
import networkx as nx
OUT = Path(__file__).resolve().parents[1]
MODS = [2,3,4,5,7,11]

def perfect(g):
    def rec(left, edges):
        if not left:
            yield tuple(edges); return
        u = min(left)
        for v in sorted(set(g[u]) & left):
            yield from rec(left-{u,v}, edges+[(u,v)])
    yield from rec(set(g), [])

def primal_counts(g):
    edges = sorted(tuple(sorted(e)) for e in g.edges())
    avoid = Counter(); hamilton = 0; tait = 0; matchings = 0
    for m in perfect(g):
        matchings += 1
        q = g.copy(); q.remove_edges_from(m)
        c = nx.number_connected_components(q)
        tait += 2**c
        if c == 1:
            hamilton += 1
            avoid.update(tuple(sorted(e)) for e in m)
    assert all((hamilton-avoid[e]) % 2 == 0 for e in edges)
    return dict(hamilton=hamilton, tait=tait, primal_matchings=matchings,
                avoidance=[[list(e),avoid[e]] for e in edges])

def rooted(t, outer, pc):
    b=Instance(t,outer); ss=list(b.states()); mates=Counter(); signs=Counter()
    for r in ss:
        for s in ss:
            if all(u!=v for u,v in zip(r,s)):
                mates[s]+=1
                signs[s]+=math.prod(b.delta(u,v) for u,v in zip(r,s))
    trees=[s for s in ss if b.is_tree(s)]
    assert set(trees)=={s for s in ss if mates[s]==1}
    assert all(signs[s]==0 for s in ss if s not in trees)
    sg=Counter(signs[s] for s in trees)
    assert sg[1]==sg[-1]
    forest_pairs=sum(mates[s] for s in trees)
    assert forest_pairs==len(trees)
    values=dict(states=len(ss),pairs=sum(mates.values()),trees=len(trees),
                forest_pairs=forest_pairs,signed=sum(signs.values()))
    for i,e in enumerate(zip(b.faces[outer],b.faces[outer][1:]+b.faces[outer][:1])):
        de=b.dual_edges[tuple(sorted(e))]
        values['avoid'+str(i)]=dict((tuple(e),n) for e,n in pc['avoidance'])[de]
    return dict(outer=outer,root=list(b.faces[outer]),**values,
                residues={k:[v%p for p in MODS] for k,v in values.items()},
                mate_hist=dict(Counter(mates[s] for s in ss)), signs=dict(sg))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--max',type=int,default=12); args=ap.parse_args()
    rows=[]
    exe=ROOT/'workings/barnette_lab/vendor/plantri.exe'
    for n in range(6,args.max+1):
        graphs=list(plantri_graphs(n,exe))
        for j,t in enumerate(graphs):
            b=Instance(t); pc=primal_counts(b.G)
            roots=[rooted(t,o,pc) for o in range(len(b.faces))]
            rows.append(dict(name=f'plantri_{n}_{j}',vertices=n,edges=sorted(t.edges()),
                             primal=pc,roots=roots))
        print(n,len(graphs),'graphs',sum(len(r['roots']) for r in rows),'roots',flush=True)
        (OUT/'counts.json').write_text(json.dumps(dict(moduli=MODS,graphs=rows),indent=2))
    # Named larger examples, all roots, but primal counting remains modest here.
    for name,g in named_graphs().items():
        if name in ('cube','hexagonal_prism'): continue
        b=Instance.from_primal(g); pc=primal_counts(b.G)
        roots=[rooted(b.T,o,pc) for o in range(len(b.faces))]
        rows.append(dict(name=name,vertices=len(b.T),edges=sorted(b.T.edges()),primal=pc,roots=roots))
        print(name, len(roots),flush=True)
        (OUT/'counts.json').write_text(json.dumps(dict(moduli=MODS,graphs=rows),indent=2))
    events=OUT/'events.jsonl'
    with events.open('a') as f:
        f.write(json.dumps(dict(type='computed',summary='Exact counts completed',graphs=len(rows),roots=sum(len(r['roots']) for r in rows),tier='T4',review='unreviewed'))+'\n')

if __name__=='__main__': main()
