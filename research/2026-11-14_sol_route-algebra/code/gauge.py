"""Test signed incidence gauges, retaining an exact GF2 inconsistency certificate."""
import sys,json,math
from pathlib import Path
from collections import defaultdict
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[3]; OUT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'workings/barnette_lab'))
from barnette_lab.core import Instance
import networkx as nx
d=json.loads((OUT/'counts.json').read_text());rows=[]
for g in d['graphs']:
    t=nx.Graph();t.add_edges_from(g['edges']); faces=Instance(t).faces
    for rr in g['roots']:
        outer=next(i for i,f in enumerate(faces) if set(f)==set(rr['root']))
        b=Instance(t,outer);ss=list(b.states());mates=defaultdict(list)
        for r,s in b.pairs(ss):mates[s].append(r)
        trees=[s for s in ss if len(mates[s])==1]
        incidences=[(f,v) for f in b.A for v in b.X if v in b.faces[f]]
        ix={e:i for i,e in enumerate(incidences)};basis={};witness=None
        for j,s in enumerate(trees):
            r=mates[s][0]; sign=math.prod(b.delta(u,v) for u,v in zip(r,s))
            mask=sum(1<<ix[e] for e in zip(b.A,s));rhs=int(sign==-1);prov=1<<j
            while mask:
                p=mask.bit_length()-1
                if p not in basis: basis[p]=(mask,rhs,prov);break
                a,z,pr=basis[p];mask^=a;rhs^=z;prov^=pr
            if not mask and rhs:
                inds=[k for k in range(len(trees)) if prov>>k&1]
                witness=[dict(state=trees[k],sign=math.prod(b.delta(u,v) for u,v in zip(mates[trees[k]][0],trees[k]))) for k in inds]
                assert sum(w['sign']==-1 for w in witness)%2
                assert all(sum(s['state'][i]==v for s in witness)%2==0 for i,f in enumerate(b.A) for v in b.faces[f])
                break
        rows.append(dict(graph=g['name'],outer=rr['outer'],root=rr['root'],trees=len(trees),consistent=witness is None,witness=witness,
                         faces_in_state_order=[b.faces[f] for f in b.A] if witness else None))
    print(g['name'],len(rows),flush=True) if not g['name'].startswith('plantri_') else None
out=dict(cases=len(rows),inconsistent=sum(not r['consistent'] for r in rows),first=next((r for r in rows if not r['consistent']),None),results=rows)
(OUT/'gauges.json').write_text(json.dumps(out,indent=2));print({k:v for k,v in out.items() if k!='results'})
