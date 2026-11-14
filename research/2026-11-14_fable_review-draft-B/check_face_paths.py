"""Check of the combinatorial height proposed in REFEREE.md (section 5, item S1).

Height by a path of faces, with no spokes and no winding numbers:
for a white face w take a path of faces w = f_0, f_1, ..., f_k = t0 in G
(consecutive faces share a side). When the path passes through a black face t
of A it enters by one side and leaves by another; the two sides meet at one
corner v of t. Put kappa_w(t, v) = +1 or -1 according to the sense in which the
path turns around v, and kappa_w(t, .) = 0 at the other two corners.
h_s(w) = sum_t kappa_w(t, s(t)),  omega(s) = sum_w h_s(w).

Claim checked: for every pair and every cycle C of D(r, s), reversing C changes
omega(s) by +-L(C), where L(C) is the jump of the lab's spoke-circulation weight
(= number of white faces inside C), with one global sign per instance tied to the
orientation of C. Also sum eps * omega^j = 0 for j < m and the value for j = m
agrees with the lab weights.

Run from the repository root:
    python research/2026-11-14_fable_review-draft-B/check_face_paths.py > research/2026-11-14_fable_review-draft-B/check_face_paths.txt
"""
import json
import sys
from collections import Counter

import networkx as nx

sys.path.insert(0, 'workings/barnette_lab')
sys.path.insert(0, 'research/2026-11-14_fable_review-draft-B')
from barnette_lab.core import Instance, edge, generated  # noqa: E402
from recompute import build, bipyramid  # noqa: E402


def face_path_kappa(inst):
    kappa = Counter()
    for w in inst.white:
        path = nx.shortest_path(inst.G, w, inst.outer)
        for prev, t, nxt in zip(path, path[1:], path[2:]):
            if t not in inst.A:
                continue
            f = inst.faces[t]
            e_in = set(inst.faces[prev]) & set(f)
            e_out = set(f) & set(inst.faces[nxt])
            assert len(e_in) == 2 and len(e_out) == 2 and e_in != e_out
            (v,) = e_in & e_out
            i = f.index(v)
            x = f[(i + 1) % 3]
            # sides at v are {v, x} and {y, v}; sign = +1 if the path leaves by {v, x}
            kappa[t, v] += 1 if e_out == {v, x} else -1
    return kappa


def check(name, inst):
    states = list(inst.states())
    pairs = inst.pairs(states)
    if not pairs:
        return None
    kap = face_path_kappa(inst)
    a = inst.weights()
    om_new = {s: sum(kap[t, v] for t, v in zip(inst.A, s)) for s in states}
    om_lab = {s: sum(a[t, v] for t, v in zip(inst.A, s)) for s in states}
    ratios = set()
    ncyc = 0
    for r, s in pairs:
        for cyc in inst.dcycles(r, s):
            r2, s2 = inst.reverse_d((r, s), cyc)
            d_lab = om_lab[s2] - om_lab[s]
            d_new = om_new[s2] - om_new[s]
            assert d_lab != 0 and abs(d_new) == abs(d_lab), (name, d_lab, d_new)
            ratios.add(d_new // d_lab)
            ncyc += 1
    assert len(ratios) == 1, (name, ratios)
    m = min(len(inst.dcycles(r, s)) for r, s in pairs)
    c = ratios.pop()
    for j in range(m + 1):
        t_new = sum(inst.sign(r, s) * om_new[s] ** j for r, s in pairs)
        t_lab = sum(inst.sign(r, s) * om_lab[s] ** j for r, s in pairs)
        assert t_new == c ** j * t_lab, (name, j, t_new, t_lab)
        if j < m:
            assert t_new == 0
    return len(pairs), ncyc, m, sum(inst.sign(r, s) * om_new[s] ** m for r, s in pairs)


if __name__ == '__main__':
    run = json.load(open('paper/figures/running.json'))
    inst = build(run['faces'], run['faces'][run['t0']])
    print('running example: pairs, D-cycle reversals checked, m, sum eps*omega^m =', check('running', inst))
    inst = build(bipyramid(6), [0, 1, 6])
    print('hexagonal bipyramid:', check('bipyramid6', inst))
    total = Counter()
    seen = 0
    for t in generated(12):
        nfaces = len(Instance(t).faces)
        for outer in range(nfaces):
            inst = Instance(t, outer)
            res = check(f'generated/{len(t)}/{outer}', inst)
            seen += 1
            if res:
                total['rootings with a pair'] += 1
                total['pairs'] += res[0]
                total['D-cycle reversals'] += res[1]
    print('lab generated family up to 12 dual vertices: rootings', seen, dict(total))
    print('all assertions passed')
