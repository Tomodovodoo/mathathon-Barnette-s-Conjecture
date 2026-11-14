"""Independent recomputation of the worked example of draft B.

Uses workings/barnette_lab (core.Instance) and brute force written here.
Does not import or run research/2026-11-14_opus_manuscript-B/example.py.

Run from the repository root:
    python research/2026-11-14_fable_review-draft-B/recompute.py > research/2026-11-14_fable_review-draft-B/recompute.txt
"""
import json
import sys
from collections import Counter, defaultdict
from itertools import combinations

import networkx as nx

sys.path.insert(0, 'workings/barnette_lab')
from barnette_lab.core import Instance, edge  # noqa: E402


def build(faces, t0_vertices):
    t = nx.Graph()
    for f in faces:
        for a, b in zip(f, f[1:] + f[:1]):
            t.add_edge(a, b)
    probe = Instance(t, 0)
    outer = next(i for i, f in enumerate(probe.faces) if set(f) == set(t0_vertices))
    return Instance(t, outer)


def good(inst, s):
    """Definition 3.5 checked directly: Q_s is a forest, one root per component."""
    q = inst.Q(s)
    if q.number_of_edges() != inst.n or not nx.is_forest(q):
        return False
    return all(len(set(c) & inst.R) == 1 for c in nx.connected_components(q))


def hamiltonian_cycles_avoiding(inst, e0):
    """All perfect matchings of G containing the dual of e0 with connected complement."""
    g = inst.G
    forced = inst.dual_edges[edge(*e0)]
    nodes = sorted(g)
    found = []

    def rec(free, chosen):
        if not free:
            h = g.copy()
            h.remove_edges_from(chosen)
            if nx.is_connected(h):
                found.append(frozenset(chosen))
            return
        v = min(free)
        for w in g[v]:
            if w in free:
                rec(free - {v, w}, chosen + [edge(v, w)])

    rec(set(nodes) - set(forced), [forced])
    return found


def signed_area(coords, cyc):
    return sum(coords[a][0] * coords[b][1] - coords[b][0] * coords[a][1]
               for a, b in zip(cyc, cyc[1:] + cyc[:1])) / 2


def point_in_polygon(p, poly):
    x, y = p
    inside = False
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            inside = not inside
    return inside


def report(name, faces, t0_vertices, e0, coords=None):
    inst = build(faces, t0_vertices)
    print(f'== {name}: |V(T)|={len(inst.T)}, faces={len(inst.faces)}, n={inst.n}, '
          f't0={sorted(inst.R)}, e0={tuple(e0)}')
    states = list(inst.states())
    pairs = inst.pairs(states)
    goods = [s for s in states if good(inst, s)]
    lab_trees = [s for s in states if inst.is_tree(s)]
    assert set(goods) == set(lab_trees), 'Definition 3.5 and the lab spoke-tree test disagree'
    partnered = {s for _, s in pairs}
    print(f'states {len(states)}, ordered pairs {len(pairs)}, good states {len(goods)}, '
          f'good states with a partner {len(set(goods) & partnered)}')
    a = inst.weights()
    omega = {s: sum(a[t, v] for t, v in zip(inst.A, s)) for s in states}
    groups = defaultdict(list)
    for r, s in pairs:
        groups[frozenset(edge(x, y) for x, y in zip(r, s))].append((r, s))
    ncyc = {k: len(inst.dcycles(*v[0])) for k, v in groups.items()}
    if pairs:
        m = min(ncyc.values())
        print(f'groups by undirected D: {len(groups)}, sizes {sorted(len(v) for v in groups.values())}, '
              f'cycle counts {sorted(ncyc.values())}, m={m}')
        for j in range(m + 1):
            tot = sum(inst.sign(r, s) * omega[s] ** j for r, s in pairs)
            print(f'  sum eps*omega^{j} = {tot}')
        # L(C): white faces inside each D-cycle, from the weights (difference of omega under reversal)
        for k, members in groups.items():
            r, s = members[0]
            ls = []
            for cyc in inst.dcycles(r, s):
                r2, s2 = inst.reverse_d((r, s), cyc)
                d = abs(omega[s2] - omega[s])
                h = len(cyc)
                ls.append((h, d))
            print(f'  group with {len(members)} pairs: (cycle length, |omega jump|) = {sorted(ls)}')
        cyc_states = sorted({s for _, s in pairs if not good(inst, s)})
        for s in cyc_states:
            q = inst.Q(s)
            cb = [sorted(c) for c in nx.cycle_basis(q)]
            part = [(r, inst.J(r, s), inst.sign(r, s)) for r, s2 in pairs if s2 == s]
            print(f'  second state with cyclic Q_s: cycles {cb}; partners (J, eps) = '
                  f'{[(j, e) for _, j, e in part]}; sum eps = {sum(e for _, _, e in part)}')
        sig = Counter(inst.sign(r, s) for r, s in pairs if good(inst, s))
        print(f'  signs of pairs with good second state: {dict(sig)}')
        print('  pair table (J, eps, omega(s) up to an additive constant, good second state):')
        for r, s in pairs:
            print(f'    r={r} s={s} J={inst.J(r, s):+d} eps={inst.sign(r, s):+d} '
                  f'omega={omega[s]} good={good(inst, s)}')
    hcs = hamiltonian_cycles_avoiding(inst, e0)
    print(f'Hamiltonian cycles of G avoiding the dual of e0 (brute force): {len(hcs)}')
    rec = set()
    for s in goods:
        out = inst.recover(s, prescribed=e0)
        p = frozenset(inst.dual_edges[edge(*x)] for x in out['P'])
        assert p in set(hcs), 'recovered selection is not a Hamiltonian complement'
        rec.add(p)
        if coords is None:
            continue
    print(f'distinct Hamiltonian cycles recovered from good states: {len(rec)}')
    # states read off the Hamiltonian cycles (Lemma 3.1)
    back = Counter()
    for p in hcs:
        sel = [e for e, d in inst.dual_edges.items() if d in p]
        forest = nx.Graph()
        forest.add_nodes_from(inst.T)
        forest.add_edges_from(sel)
        forest.remove_edge(*e0)
        st = {}
        for comp in nx.connected_components(forest):
            root = next(iter(set(comp) & inst.R))
            dist = nx.single_source_shortest_path_length(forest, root)
            for u, v in forest.subgraph(comp).edges():
                tail = u if dist[u] > dist[v] else v
                black = next(f for f in (inst.sides[u, v], inst.sides[v, u]) if f in inst.black)
                st[black] = tail
        s = tuple(st[t] for t in inst.A)
        assert inst.valid(s)
        back[s] += 1
    print(f'states read off those cycles (Lemma 3.1): {len(back)} distinct; '
          f'multiplicities {sorted(back.values())}; '
          f'good {sum(1 for s in back if good(inst, s))}; '
          f'with a partner {sum(1 for s in back if s in partnered)}')
    if coords is not None and pairs:
        print('  geometry check against the figure layout:')
        # The figure layout draws the three sides of t0 as circular arcs, so the
        # straight-line centroid test is wrong for faces with a root corner. Such
        # faces are never inside a cycle of D (roots are outside), so skip them.
        white_centroids = {y: tuple(sum(coords[v][i] for v in inst.faces[y]) / 3 for i in (0, 1))
                           for y in inst.white if not set(inst.faces[y]) & inst.R}
        seen = set()
        for r, s in pairs:
            d = {x: y for x, y in zip(r, s)}
            todo = set(d)
            while todo:
                x = min(todo)
                cyc = [x]
                while d[cyc[-1]] != x:
                    cyc.append(d[cyc[-1]])
                todo -= set(cyc)
                key = tuple(cyc)
                if key in seen:
                    continue
                seen.add(key)
                area = signed_area(coords, cyc)
                poly = [coords[v] for v in cyc]
                inside = [y for y, c in white_centroids.items() if point_in_polygon(c, poly)]
                inside_b = [t for t in inst.black if not set(inst.faces[t]) & inst.R
                            and point_in_polygon(tuple(sum(coords[v][i] for v in inst.faces[t]) / 3
                                                      for i in (0, 1)), poly)]
                print(f'    cycle {cyc}: {"ccw" if area > 0 else "cw"}, h={len(cyc)}, '
                      f'W={len(inside)}, B={len(inside_b)}')
        # Example 3.8: components of P_s for the good state of Figure 4(b)
        for r, s in pairs:
            if not good(inst, s):
                partner_good = [r2 for r2, s2 in pairs if s2 == s]
                for r2 in partner_good:
                    if good(inst, r2):
                        out = inst.recover(r2, prescribed=e0)
                        print(f'    cyclic state s={s}; disjoint good state r={r2}; '
                              f'P_r classes {out["classes"]}')
    print()


def bipyramid(k):
    """Faces of the k-gonal bipyramid, k even: equator 0..k-1, apexes k and k+1."""
    faces = []
    for i in range(k):
        j = (i + 1) % k
        faces.append([i, j, k])
        faces.append([j, i, k + 1])
    return faces


if __name__ == '__main__':
    run = json.load(open('paper/figures/running.json'))
    lay = json.load(open('paper/figures/layout-running.json'))
    coords = {int(k): tuple(v) for k, v in lay['coordinates'].items()}
    report('running example', run['faces'], run['faces'][run['t0']], run['e0'], coords)
    # hexagonal prism = dual of the hexagonal bipyramid; t0 = face (0, 1, 6)
    faces = bipyramid(6)
    report('hexagonal bipyramid, e0 = equatorial side (0,1)', faces, [0, 1, 6], (0, 1))
    report('hexagonal bipyramid, e0 = apex side (0,6)', faces, [0, 1, 6], (0, 6))
    report('hexagonal bipyramid, e0 = apex side (1,6)', faces, [0, 1, 6], (1, 6))
