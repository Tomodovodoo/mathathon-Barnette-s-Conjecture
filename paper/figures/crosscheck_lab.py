"""Independent check of the running example against workings/barnette_lab.

python paper/figures/crosscheck_lab.py
Uses the lab's own Instance (its own face enumeration, states, pairs, Q and
recover) and compares with check.running(). Faces are matched by vertex sets.
Reads the lab, never writes to it. Writes lab-crosscheck.json.
"""
import json
import sys
from pathlib import Path

import networkx as nx

sys.dont_write_bytecode = True
O = Path(__file__).parent.resolve()
sys.path.insert(0, str(O.parents[1] / 'workings' / 'barnette_lab'))
from barnette_lab.core import Instance  # noqa: E402

import check  # noqa: E402

run = check.running()
m = run['model']
b = Instance(m.T)
outer = next(i for i, f in enumerate(b.faces) if set(f) == set(m.roots))
b = Instance(m.T, outer)
ss = list(b.states())
ps = list(b.pairs(ss))
cy = [(r, s) for r, s in ps if not nx.is_forest(b.Q(s))]
ours = run['counts']
assert (len(ss), len(ps), len(cy)) == (ours['states'], ours['pairs'], ours['cyclic_pairs'])
face_id = {frozenset(f): i for i, f in enumerate(m.F)}


def translate(state):
    choice = dict(zip(m.A, state))
    return tuple(choice[face_id[frozenset(b.faces[t])]] for t in b.A)


r, s, r2 = (translate(x) for x in (run['r'], run['s'], run['r2']))
for x in (r, s, r2):
    assert b.valid(x)
assert (r, s) in cy and (r2, s) in cy and len(cy) == 2
assert b.is_tree(r) and not b.is_tree(s)
cert = b.recover(r, prescribed=tuple(m.e0))
assert {tuple(sorted(e)) for e in cert['P']} == {tuple(e) for e in run['rec']['P']}
cyc = [face_id[frozenset(b.faces[v])] for v in cert['cycle']]
assert {tuple(sorted(e)) for e in zip(cyc, cyc[1:] + cyc[:1])} == {tuple(e) for e in run['rec']['hamiltonian']}
(O / 'lab-crosscheck.json').write_text(json.dumps(dict(
    status='COMPUTED', states=len(ss), pairs=len(ps), cyclic_pairs=len(cy),
    agrees=['state, pair and cyclic-pair counts', 'displayed states are valid', 'the two cyclic pairs',
            'Q_r tree test', 'selected edges P', 'Hamiltonian cycle']), indent=1))
print('barnette_lab agrees: counts', len(ss), len(ps), len(cy), '; P and the Hamiltonian cycle match')
