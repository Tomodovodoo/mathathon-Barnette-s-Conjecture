"""Cross-check dig.py against workings/barnette_lab, and compute the gluing example of step 08.

Run from the repository root:
    python research/2026-11-14_fable_digestions/code/crosscheck.py
Writes ../data/crosscheck.json.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'workings', 'barnette_lab'))
import networkx as nx  # noqa: E402
from barnette_lab import Instance  # noqa: E402
from dig import Tri, summary  # noqa: E402

OUT = {}


def lab_counts(T):
    g = nx.Graph()
    g.add_edges_from(T.E)
    probe = Instance(g)
    outer = next(i for i, f in enumerate(probe.faces) if set(f) == set(T.faces[T.t0]))
    b = Instance(g, outer)
    ss = list(b.states())
    ps = b.pairs(ss)
    trees = [s for s in ss if b.is_tree(s)]
    poly = b.polynomial(ps) if ps else {}
    return {'states': len(ss), 'pairs': len(ps), 'tree_matchings': len(trees),
            'J_multiset': sorted(abs(b.J(r, s)) for r, s in ps), 'lab_polynomial': poly}, b


def compare(name, T):
    info = summary(T)[0]
    lab, b = lab_counts(T)
    mine = {k: info[k] for k in ('states', 'pairs', 'tree_matchings')}
    mine['J_multiset'] = sorted(abs(T.J(r, s)) for r, s in T.pairs())
    ok = all(mine[k] == lab[k] for k in mine)
    print(name, 'mine', mine, 'lab', {k: lab[k] for k in mine}, 'polynomial (lab)', lab['lab_polynomial'], 'AGREE' if ok else 'DIFFER')
    assert ok
    OUT[name] = {'mine': mine, 'lab': {k: lab[k] for k in mine}, 'lab_polynomial': {str(k): v for k, v in lab['lab_polynomial'].items()}}
    return b


def induced_tree(T, cls):
    cls = set(cls)
    edges = [e for e in T.E if e[0] in cls and e[1] in cls]
    comps, cyc = T.components(edges)
    comps = [c for c in comps if c[0] in cls]
    return cyc == 0 and len(comps) == 1 and len(edges) == len(cls) - 1


def main():
    d = json.load(open(os.path.join(ROOT, 'paper', 'figures', 'octahedron.json')))
    compare('octahedron', Tri(d['faces'], d['t0']))
    faces = []
    for i in range(6):
        j = (i + 1) % 6
        faces += [(6, i, j), (7, j, i)]
    compare('prism', Tri(faces, 0))
    d = json.load(open(os.path.join(ROOT, 'paper', 'figures', 'running.json')))
    compare('running', Tri(d['faces'], d['t0']))

    # ---- gluing example: 9 vertices, rooted at a face with no pair --------------------------
    octa = [(0, 2, 1), (0, 1, 5), (1, 2, 3), (2, 0, 4), (1, 3, 5), (2, 4, 3), (0, 5, 4), (3, 4, 5)]
    inner = [(3, 4, 8), (4, 5, 6), (5, 3, 7), (3, 8, 7), (4, 6, 8), (5, 7, 6), (6, 7, 8)]
    T9 = Tri(octa[:-1] + inner, 1)                      # t0 = (0, 1, 5): no pair
    assert not T9.pairs()
    e0 = (0, 1)
    # outer piece: the octahedron, cap (3, 4, 5), same root and same prescribed edge
    Tout = Tri(octa, 1)
    s_out = [s for s in Tout.states() if Tout.is_tree_matching(s)][0]
    rec_out = Tout.recover(s_out, e0)
    cls_out = rec_out['classes']
    cap = [3, 4, 5]
    same = next(c for c in cls_out if len(set(c) & set(cap)) == 2)
    e1 = tuple(sorted(set(same) & set(cap)))
    # inner piece: the inner faces plus the cap (5, 4, 3), rooted at the cap
    faces_in = inner + [(5, 4, 3)]
    Tin = Tri(faces_in, len(faces_in) - 1)
    tms_in = [s for s in Tin.states() if Tin.is_tree_matching(s)]
    rec_in = Tin.recover(tms_in[0], e1)
    cls_in = rec_in['classes']
    # rename the inner labels to agree on the cap, then take unions
    a_out = same
    b_out = next(c for c in cls_out if c is not same)
    a_in = next(c for c in cls_in if set(e1) <= set(c))
    b_in = next(c for c in cls_in if c is not a_in)
    U1, U2 = sorted(set(a_out) | set(a_in)), sorted(set(b_out) | set(b_in))
    assert sorted(U1 + U2) == T9.V
    ok = induced_tree(T9, U1) and induced_tree(T9, U2)
    # the Hamiltonian cycle: faces of T9 adjacent across edges with ends in different classes
    lab = {v: 0 for v in U1}
    lab.update({v: 1 for v in U2})
    gadj = {f: [] for f in range(len(T9.faces))}
    for a, b in T9.E:
        if lab[a] != lab[b]:
            f, g = T9.left[a, b], T9.left[b, a]
            gadj[f].append(g)
            gadj[g].append(f)
    assert all(len(v) == 2 for v in gadj.values())
    cycle, prev, cur = [0], None, 0
    while True:
        nxt = next(g for g in gadj[cur] if g != prev)
        if nxt == 0:
            break
        cycle.append(nxt)
        prev, cur = cur, nxt
    assert len(cycle) == len(T9.faces)
    e0_dual = sorted((T9.left[0, 1], T9.left[1, 0]))
    uses_e0 = any({a, b} == set(e0_dual) for a, b in zip(cycle, cycle[1:] + cycle[:1]))
    print('gluing: outer state', s_out, 'classes', cls_out, 'same-label cap edge', e1)
    print('        inner tree matchings', len(tms_in), 'state', tms_in[0], 'classes', cls_in)
    print('        glued classes', U1, U2, 'both induce trees:', ok)
    print('        Hamiltonian cycle through all', len(cycle), 'faces:', cycle, 'uses e0*:', uses_e0)
    assert ok and not uses_e0
    OUT['gluing'] = {'faces': T9.faces, 't0': 1, 'e0': e0, 'outer_state': s_out, 'outer_classes': cls_out,
                     'cap_edge': e1, 'inner_state': tms_in[0], 'inner_classes': cls_in, 'glued_classes': [U1, U2],
                     'cycle': cycle, 'avoids_dual_of_e0': not uses_e0}
    with open(os.path.join(HERE, '..', 'data', 'crosscheck.json'), 'w') as f:
        json.dump(OUT, f, indent=1, default=str)


if __name__ == '__main__':
    main()
