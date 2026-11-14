"""Optional independent cross-check against the shared reference implementation."""
import sys,json,networkx as nx
from pathlib import Path
sys.dont_write_bytecode=True
O=Path(__file__).parent.resolve();sys.path.insert(0,str(O.parents[1]/'workings'/'barnette_lab'))
from barnette_lab.core import Instance
from barnette_lab.verify import export
d=json.loads((O/'checked.json').read_text());T=nx.Graph(d['edges']);b=Instance(T);outer=next(i for i,f in enumerate(b.faces) if set(f)==set(d['roots']));b=Instance(T,outer)
ss=list(b.states());ps=list(b.pairs(ss));cy=[(r,s) for r,s in ps if not nx.is_forest(b.Q(s))]
assert (len(ss),len(ps),len(cy))==(15,10,2)
faceids={frozenset(f):i for i,f in enumerate(d['faces'])}
def translate(s):
 choices=dict(zip(d['A'],s));return tuple(choices[faceids[frozenset(b.faces[t])]] for t in b.A)
for r,s in [d['cyclic_pair'],d['forest_pair'],d['reversed_pair']]:
 rr,st=translate(r),translate(s);assert b.valid(rr) and b.valid(st) and all(u!=v for u,v in zip(rr,st))
s=translate(d['forest_pair'][1]);assert b.is_tree(s)
cert=b.recover(s,prescribed=tuple(d['roots'][:2]));assert {tuple(sorted(e)) for e in cert['P']}=={tuple(sorted(e)) for e in d['selected_edges']}
cycle=[faceids[frozenset(b.faces[v])] for v in cert['cycle']]
assert {tuple(sorted(e)) for e in zip(cycle,cycle[1:]+cycle[:1])}=={tuple(sorted(e)) for e in d['hamiltonian']}
print('independent counts, selected edges and Hamiltonian cycle agree')
(O/'lab-export.json').write_text(json.dumps(export(b),indent=2));(O/'lab-crosscheck.json').write_text(json.dumps(dict(status='COMPUTED',states=len(ss),pairs=len(ps),cyclic_pairs=len(cy),recovery=cert),indent=2))
