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
    """Decode the saved certificates without their face numbering: a black face t of the pair
    is the face of the chosen colour on the edge {r(t), s(t)}; white ids are matched through
    the cherry structure.  Then every colour class is re-checked with my own W."""
    data = json.loads(SOL.read_text())
    out = []
    for row in data['rows']:
        g = nx.Graph()
        g.add_edges_from(tuple(e) for e in row['triangulation_edges'])
        tri, idx = tri_from_nx(g)
        r, s = row['pair']
        # their A order is the order of the pair lists; recover their t ids from the edge list
        their_t = sorted({e[0] for e in row['edges']})
        assert len(their_t) == len(r)
        found = None
        for colour in (0, 1):
            tmap = {}
            for t, a, b in zip(their_t, r, s):
                fa, fb = tri.fid[idx[a], idx[b]], tri.fid[idx[b], idx[a]]
                tmap[t] = fa if tri.col[fa] == colour else fb
            left = [f for f in range(len(tri.faces)) if tri.col[f] == colour and f not in tmap.values()]
            if len(set(tmap.values())) == len(their_t) and len(left) == 1:
                found = (tmap, left[0])
                break
        assert found, row['name']
        tmap, outer = found
        inst = Rooted(tri, outer)
        rr = {tmap[t]: idx[v] for t, v in zip(their_t, r)}
        ss = {tmap[t]: idx[v] for t, v in zip(their_t, s)}
        ok_pair = (all(rr[t] != ss[t] and rr[t] in tri.faces[t] and ss[t] in tri.faces[t] for t in inst.A)
                   and sorted(rr.values()) == sorted(inst.X) == sorted(ss.values()))
        classes = {0: [], 1: []}
        spokes = set()
        phi, phi_ok = {}, True
        for (t, v, a, c), col in zip(row['edges'], row['colors']):
            T_, v_ = tmap[t], idx[v]
            spokes.add((T_, v_))
            mine = inst.wedge[T_, v_]
            classes[col].append(mine)
            # their white ids {a, c} must correspond to my {mine}; record consistent bijection
            cand = [(a, mine[0]), (c, mine[1])], [(a, mine[1]), (c, mine[0])]
            phi.setdefault(('edge', T_, v_), (a, c, mine))
        # solve phi by propagation over cherries: the shared white id of a cherry is the face across {r,s}
        for t in their_t:
            T_ = tmap[t]
            es = [e for e in row['edges'] if e[0] == t]
            shared = set(es[0][2:]) & set(es[1][2:])
            me = set(inst.wedge[T_, rr[T_]]) & set(inst.wedge[T_, ss[T_]])
            if len(shared) != 1 or len(me) != 1:
                phi_ok = False
                continue
            x, y = shared.pop(), me.pop()
            if phi.get(x, y) != y:
                phi_ok = False
            phi[x] = y
        support = {(t, rr[t]) for t in inst.A} | {(t, ss[t]) for t in inst.A}
        m = len(inst.white)
        out.append({'name': row['name'], 'V': row['V'], 'their_pass': row['pass'], 'pair_valid': ok_pair,
                    'support_matches': spokes == support, 'white_ids_consistent': phi_ok,
                    'tree0': is_spanning_tree(m, classes[0]), 'tree1': is_spanning_tree(m, classes[1])})
        print(out[-1], flush=True)
    return out


if __name__ == '__main__':
    res = {'command': 'python code/referee_sol.py',
           'part1_recount': part1() if '--skip1' not in sys.argv else 'skipped'}
    print(res['part1_recount'], flush=True)
    res['part2_certificates'] = part2()
    (OUT / 'referee_sol.json').write_text(json.dumps(res, indent=1))
