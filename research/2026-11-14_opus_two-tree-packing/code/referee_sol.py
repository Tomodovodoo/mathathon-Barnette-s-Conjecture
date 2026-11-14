"""Referee replay of the probabilistic folder's packing evidence, with independent code.

1. Recount the 278 nonvacuous rooted cases (V=6..14 with lab face 0; V=16 with lab faces
   0 and 1) and test every pair support there with tp.py.
2. Re-verify the 27 saved two-tree certificates in
   research/2026-11-14_sol_route-probabilistic/data/packing.json: rebuild W from the saved
   triangulation with tp.py, check that (r, s) is a pair, that the coloured edges are exactly
   its support, and that each colour class is a spanning tree of W.
The lab Instance is used only to decode the folder's face numbering (face id -> vertex set).
Usage: python referee_sol.py   (writes data/referee_sol.json)"""
import json, sys
from pathlib import Path
import networkx as nx
from tp import Tri, Rooted, plantri, check_packing, is_spanning_tree, ROOT

sys.path.insert(0, str(ROOT / 'workings/barnette_lab'))
from barnette_lab.core import Instance, plantri_graphs  # decoding only

OUT = Path(__file__).resolve().parents[1] / 'data'
SOL = ROOT / 'research/2026-11-14_sol_route-probabilistic/data/packing.json'


def tri_from_nx(g):
    ok, emb = nx.check_planarity(g)
    assert ok
    nodes = sorted(g)
    idx = {v: i for i, v in enumerate(nodes)}
    rot = [[idx[w] for w in emb.neighbors_cw_order(v)] for v in nodes]
    return Tri(rot), idx


def rooted_like_lab(g, lab_outer):
    lab = Instance(g, lab_outer)
    tri, idx = tri_from_nx(g)
    fset = frozenset(idx[v] for v in lab.faces[lab_outer])
    f = next(i for i, F in enumerate(tri.faces) if frozenset(F) == fset)
    return lab, tri, idx, Rooted(tri, f)


def part1():
    exe = ROOT / 'workings/barnette_lab/vendor/plantri.exe'
    rows = {'first_batch': [0, 0, 0], 'V16_batch': [0, 0, 0]}  # cases, nonvacuous, failures
    for V in range(6, 15):
        for g in plantri_graphs(V, exe):
            _, _, _, inst = rooted_like_lab(g, 0)
            us = inst.two_factors()
            rows['first_batch'][0] += 1
            rows['first_batch'][1] += bool(us)
            for u in us:
                if check_packing(len(inst.white), [e[2:] for e in inst.support(u)])[0] != 'pack':
                    rows['first_batch'][2] += 1
    for g in plantri_graphs(16, exe):
        for outer in (0, 1):
            _, _, _, inst = rooted_like_lab(g, outer)
            us = inst.two_factors()
            rows['V16_batch'][0] += 1
            rows['V16_batch'][1] += bool(us)
            for u in us:
                if check_packing(len(inst.white), [e[2:] for e in inst.support(u)])[0] != 'pack':
                    rows['V16_batch'][2] += 1
    return rows


def part2():
    data = json.loads(SOL.read_text())
    out = []
    for row in data['rows']:
        g = nx.Graph()
        g.add_edges_from(tuple(e) for e in row['triangulation_edges'])
        lab, tri, idx, inst = rooted_like_lab(g, row['outer'])
        fmap = {}  # lab face id -> my face id
        for i, F in enumerate(lab.faces):
            s = frozenset(idx[v] for v in F)
            fmap[i] = next(j for j, G in enumerate(tri.faces) if frozenset(G) == s)
        r, s = row['pair']
        A = [fmap[t] for t in lab.A]
        assert sorted(A) == sorted(inst.A)
        rr = {fmap[t]: idx[v] for t, v in zip(lab.A, r)}
        ss = {fmap[t]: idx[v] for t, v in zip(lab.A, s)}
        ok_pair = (all(rr[t] != ss[t] and rr[t] in tri.faces[t] and ss[t] in tri.faces[t] for t in inst.A)
                   and sorted(rr.values()) == sorted(inst.X) == sorted(ss.values()))
        # coloured edges in my numbering, recomputing their W-ends from my own W
        classes = {0: [], 1: []}
        spokes = set()
        ends_match = True
        for (t, v, a, c), col in zip(row['edges'], row['colors']):
            T_, v_ = fmap[t], idx[v]
            spokes.add((T_, v_))
            mine = inst.wedge[T_, v_]
            theirs = {inst.widx[fmap[a]], inst.widx[fmap[c]]}
            ends_match &= set(mine) == theirs
            classes[col].append(mine)
        support = {(t, rr[t]) for t in inst.A} | {(t, ss[t]) for t in inst.A}
        m = len(inst.white)
        out.append({'name': row['name'], 'V': row['V'], 'pair_valid': ok_pair,
                    'support_matches': spokes == support, 'ends_match': ends_match,
                    'tree0': is_spanning_tree(m, classes[0]), 'tree1': is_spanning_tree(m, classes[1])})
        print(out[-1], flush=True)
    return out


if __name__ == '__main__':
    res = {'command': 'python code/referee_sol.py', 'part1_recount': part1()}
    print(res['part1_recount'], flush=True)
    res['part2_certificates'] = part2()
    (OUT / 'referee_sol.json').write_text(json.dumps(res, indent=1))
