"""Dump what barnette_lab computes, as plain data, for comparison by compare_lab.py.

This is the only file in this folder that imports the lab. Run from the repository root:
    python -B research/2026-11-14_fable_referee-determinants/code/export_lab.py
Writes lab_export.json next to this file.
"""
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'workings/barnette_lab'))
import networkx as nx
from barnette_lab.core import Instance, named_graphs, glue_triangles
from barnette_lab.algorithms import determinant_sample, two_matroid_candidate
from barnette_lab import hamiltonian_cycle


def dump(name, b, primal=None):
    ss = list(b.states())
    pairs = b.pairs(ss)
    a = b.weights()
    trees = [s for s in ss if b.is_tree(s)]
    row = {
        'name': name,
        'T_edges': sorted(map(list, b.T.edges())),
        'root': list(b.faces[b.outer]),
        'faces': [list(f) for f in b.faces],
        'black': b.black, 'A': b.A, 'X': b.X,
        'states': [list(s) for s in ss],
        'n_pairs': len(pairs),
        'pairs_J': sorted(b.J(r, s) for r, s in pairs),
        'pair_signs': sorted(b.sign(r, s) for r, s in pairs),
        'tree_states': [list(s) for s in trees],
        'weights': [[t, v, w] for (t, v), w in sorted(a.items())],
        'delta': [[u, v, b.delta(u, v)] for u, v in b.T.edges()] + [[v, u, b.delta(v, u)] for u, v in b.T.edges()],
        'polynomial': {str(k): v for k, v in b.polynomial().items()},
        'cmin': min((len(b.dcycles(r, s)) for r, s in pairs), default=None),
    }
    if trees:
        s = b.enumerate_tree()
        cert = b.recover(s)
        row['recover'] = {'state': list(s), 'P': [list(e) for e in cert['P']], 'classes': cert['classes'],
                          'cycle_faces': [list(b.faces[i]) for i in cert['cycle']]}
    spokes, valid = two_matroid_candidate(b)
    row['two_matroid'] = {'spokes': [list(x) for x in spokes], 'valid': valid}
    if len(ss) <= 20:
        freq = {}
        for seed in range(3000):
            s = determinant_sample(b, seed)
            freq[str(list(s))] = freq.get(str(list(s)), 0) + 1
        row['sample_frequencies'] = freq
    if primal is not None:
        row['primal_edges'] = sorted(map(list, primal.edges()))
        row['hamiltonian_cycles'] = [{'forbidden': list(e), 'cycle': hamiltonian_cycle(primal, e)} for e in list(primal.edges())[:6]]
    return row


rows = []
for name, g in named_graphs().items():
    rows.append(dump(name, Instance.from_primal(g), g))
hard = json.loads((ROOT / 'research/2026-11-14_sol_route-constructive/data/hard_instance.json').read_text())
rows.append(dump('cyclic_12', Instance(nx.Graph(hard['T_edges']), hard['outer'])))
glued = glue_triangles(nx.octahedral_graph(), nx.octahedral_graph())
for i in range(14):
    rows.append(dump(f'glued_root_{i}', Instance(glued, i)))
(HERE / 'lab_export.json').write_text(json.dumps(rows, indent=1))
print('exported', len(rows), 'instances')
