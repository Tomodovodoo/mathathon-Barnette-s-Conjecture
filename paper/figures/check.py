"""Compute and verify every object the figures draw.

`running()`, `octahedron()` and `gluing()` return plain dictionaries. Every
state, pair, cycle, tree and count in them is asserted here, so draw.py never
draws an unchecked object. Run as a script to write checked.json and
validation.json.
"""
import json
import math

import networkx as nx
import numpy as np

from model import HERE, Model, dual_of_cubic, und


def cross2(a, b):
    return float(a[0] * b[1] - a[1] * b[0])


def coords(name):
    L = json.loads((HERE / f'layout-{name}.json').read_text())
    return {int(k): np.array(v, float) for k, v in L['coordinates'].items()}, L


def load(name):
    d = json.loads((HERE / f'{name}.json').read_text())
    return Model(d['faces'], d['t0'], d.get('e0'))


def check_layout(m, xy, R):
    """Bounded faces counterclockwise, roots on the circle, the rest inside,
    and no two straight edges crossing."""
    for i, f in enumerate(m.F):
        if i == m.t0:
            continue
        a, b, c = (xy[v] for v in f)
        area = cross2(b - a, c - a)
        if sum(v in m.roots for v in f) < 2:
            assert area > 1e-6, f'face {f} is flipped'
    for v in m.roots:
        assert abs(np.hypot(*xy[v]) - R) < 1e-2
    for v in m.X:
        assert np.hypot(*xy[v]) < R
    straight = [e for e in m.E if not set(e) <= set(m.roots)]

    def ccw(p, q, r):
        return cross2(q - p, r - p)
    for i, (a, b) in enumerate(straight):
        for c, d in straight[i + 1:]:
            if {a, b} & {c, d}:
                continue
            p, q, r, s = xy[a], xy[b], xy[c], xy[d]
            assert not (ccw(p, q, r) * ccw(p, q, s) < 0 and ccw(r, s, p) * ccw(r, s, q) < 0), 'edges cross'


def spoke_weights(m):
    """Weights a(t, v) on the spokes of H0 with circulation one around every
    bounded face (Lemma 5.3). Returns (weights, bounded faces of H0)."""
    spokes = [(t, v) for t in m.A for v in m.F[t]]
    index = {sp: i for i, sp in enumerate(spokes)}
    H0 = nx.Graph((('t', t), ('v', v)) for t, v in spokes)
    assert nx.is_connected(H0), 'H0 is disconnected: treat components separately'
    inner_white = [w for w in m.white if all(m.black_face(a, b) != m.t0
                                             for a, b in zip(m.F[w], m.F[w][1:] + m.F[w][:1]))]
    rows = []
    for w in inner_white:
        row = np.zeros(len(spokes))
        f = m.F[w]
        for x, y in zip(f, f[1:] + f[:1]):          # counterclockwise side x -> y, via the black centre across it
            t = m.black_face(x, y)
            row[index[t, y]] += 1
            row[index[t, x]] -= 1
        rows.append(row)
    Aeq = np.array(rows)
    sol = np.linalg.lstsq(Aeq, np.ones(len(rows)), rcond=None)[0]
    assert np.allclose(Aeq @ sol, 1, atol=1e-9)
    assert len(inner_white) == H0.number_of_edges() - H0.number_of_nodes() + 1     # Euler: all bounded faces found
    return {sp: float(sol[i]) for sp, i in index.items()}, inner_white


def running():
    m = load('running')
    xy, L = coords('running')
    check_layout(m, xy, L['R'])
    out = dict(model=m, xy=xy, R=L['R'])

    # The stored triangulation is the dual of the stored cubic graph, and has the
    # properties the theorem needs.
    G = nx.read_adjlist(HERE / 'running-primal.adjlist', nodetype=int)
    assert nx.is_isomorphic(G, m.G)
    assert all(d == 3 for _, d in G.degree()) and nx.is_bipartite(G) and nx.node_connectivity(G) == 3
    assert all(d % 2 == 0 for _, d in m.T.degree())
    tri = {tuple(sorted(c)) for c in nx.enumerate_all_cliques(m.T) if len(c) == 3}
    assert tri == {tuple(sorted(f)) for f in m.F}, 'there is a separating triangle'
    assert nx.is_isomorphic(nx.Graph(und(*e) for f in dual_of_cubic(G) for e in zip(f, f[1:] + f[:1])), m.T)

    states = m.states()
    pairs = m.pairs(states)
    assert all(m.is_pair(r, s) for r, s in pairs)
    cyclic = [(r, s) for r, s in pairs if not m.Q_is_forest(s)]
    out['counts'] = dict(vertices=len(m.V), faces=len(m.F), states=len(states), pairs=len(pairs),
                         cyclic_pairs=len(cyclic), forest_pairs=len(pairs) - len(cyclic))

    # Lemma 4.1 on every directed cycle the example offers.
    for r, s in pairs:
        for c in m.directed_cycles(m.D(r, s)) + m.directed_cycles(m.Q_directed(r, s)):
            k = m.disk(c)
            assert k['B'] + k['W'] == 2 * k['I'] + k['h'] - 2
            assert 3 * (k['B'] - k['W']) == 2 * k['l'] - k['h']
            assert k['B'] == k['I'] + k['l']
            assert k['delta_sum'] == (-3 if k['ccw'] else 3)

    # The displayed pair: Q_s cyclic, Q_r a forest, and a cycle of D with interior vertices.
    pick = [(r, s) for r, s in cyclic if m.Q_is_forest(r)
            and any(m.disk(c)['I'] >= 1 for c in m.directed_cycles(m.D(r, s)))]
    assert len(pick) == 1, 'the selection rule no longer gives a unique pair'
    r, s = pick[0]
    out['r'], out['s'] = r, s
    out['D_cycles'] = [m.disk(c) for c in m.directed_cycles(m.D(r, s))]
    out['D_cycles'].sort(key=lambda k: -k['h'])
    big = out['D_cycles'][0]
    assert big['I'] >= 1 and min(big['B'], big['W'], big['l']) >= 1
    out['disk'] = big
    # facts the captions state in words
    assert [k['h'] for k in out['D_cycles']] == [7, 3] and big['ccw'] and not out['D_cycles'][1]['ccw']
    assert (len(m.A), len(m.X), len(m.white), len(m.E), len(m.F)) == (10, 10, 11, 33, 22) and sorted(m.roots) == [0, 4, 5]
    # which state matches each black face of the disk (the proof of B = I + l)
    rr = dict(zip(m.A, r))
    out['disk_matching'] = {t: rr[t] for t in big['black']}
    assert sorted(out['disk_matching'].values()) == sorted(
        big['interior'] + [a for a, b in big['inner_black_edges']])

    # Lemma 5.2: reversing the cycle of Q_s changes r only and flips the phase.
    qc = m.directed_cycles(m.Q_directed(r, s))
    assert len(qc) == 1
    r2 = m.reverse_Q_cycle(r, s, qc[0])
    assert m.is_pair(r2, s) and r2 != r
    qc2 = m.directed_cycles(m.Q_directed(r2, s))
    assert len(qc2) == 1 and sorted(qc2[0]) == sorted(qc[0])
    assert m.reverse_Q_cycle(r2, s, qc2[0]) == r
    assert abs(m.J(r2, s) - m.J(r, s)) == 2
    assert {x for x in cyclic if x[1] == s} == {(r, s), (r2, s)}
    out.update(r2=r2, Q_cycle=qc[0], Q_cycle_rev=qc2[0], J=m.J(r, s), J2=m.J(r2, s),
               changed=[t for t, a, b in zip(m.A, r, r2) if a != b])
    assert sum(1j ** m.J(a, b) for a, b in cyclic) == 0

    # Section 5.3: unit circulations, L+ - L- on each cycle of D.
    a, inner_white = spoke_weights(m)
    out['spoke_weights'] = a
    face_of = {und(x, y): m.black_face(x, y) for x, y in m.E}
    for k in out['D_cycles']:
        cyc = k['cycle'] if k['ccw'] else k['cycle'][::-1]
        arcs = list(zip(cyc, cyc[1:] + cyc[:1]))
        Lp = sum(a[face_of[und(x, y)], y] for x, y in arcs)
        Lm = sum(a[face_of[und(x, y)], x] for x, y in arcs)
        k['ccw_cycle'] = cyc
        k['L_diff'] = round(Lp - Lm, 9)
        # the spoke polygon encloses exactly the white faces of the disk
        assert abs((Lp - Lm) - k['W']) < 1e-9 and k['W'] > 0
        poly = []
        for x, y in arcs:
            poly += [xy[x], sum(xy[v] for v in m.F[face_of[und(x, y)]]) / 3]
        area = sum(cross2(p, q) for p, q in zip(poly, poly[1:] + poly[:1])) / 2
        assert area > 0
    # Z(x) grouped by D: every group has the same number of cycles here.
    groups = {}
    for p, q in pairs:
        groups.setdefault(frozenset(und(x, y) for x, y in zip(p, q)), []).append((p, q))
    out['groups'] = [dict(size=len(g), cycles=len(m.directed_cycles(m.D(*g[0])))) for g in groups.values()]
    assert all(g['size'] == 2 ** g['cycles'] for g in out['groups'])

    # Section 6 with the same two states in the other order: (s, r) has Q_r a forest.
    assert m.is_pair(s, r) and m.Q_is_forest(r)
    qg = m.Q_graph(r)
    comps = list(nx.connected_components(qg))
    assert len(comps) == 3 and all(len(set(c) & set(m.roots)) == 1 for c in comps)
    out['Q_components'] = [sorted(c) for c in comps]
    rec = m.recover(r)
    out['rec'] = rec
    two = m.two_factors(components=2)
    assert two
    # choose the disconnected 2-factor whose smaller cycle is as long as possible (easier to see)
    two.sort(key=lambda es: -min(len(c) for c in nx.connected_components(nx.Graph(es))))
    out['two_factor'] = two[0]
    assert all(d == 2 for _, d in nx.Graph(two[0]).degree()) and len(nx.Graph(two[0])) == len(m.F)

    # Proposition 3.1: the cut inequality for every S, and r + s as a degree-two subgraph of B.
    import itertools as it
    worst = None
    for k in range(len(m.X) + 1):
        for S in it.combinations(m.X, k):
            lhs, rhs = m.cut_inequality(S)
            assert lhs >= rhs
            if S and (worst is None or lhs - rhs < worst[0] or (lhs - rhs == worst[0] and len(S) < len(worst[1]))):
                worst = (lhs - rhs, S)
    out['tight_cut'] = dict(slack=worst[0], S=list(worst[1]))
    B = m.incidence_graph()
    two_b = nx.Graph([(('t', t), ('v', v)) for t, v in zip(m.A, r)] + [(('t', t), ('v', v)) for t, v in zip(m.A, s)])
    assert all(B.has_edge(*e) for e in two_b.edges()) and all(d == 2 for _, d in two_b.degree())
    out['B_edges'] = B.number_of_edges()
    return out


def octahedron():
    m = load('octahedron')
    xy, L = coords('octahedron')
    check_layout(m, xy, L['R'])
    assert nx.is_isomorphic(m.G, nx.cubical_graph()) and nx.is_isomorphic(m.T, nx.octahedral_graph())
    states = m.states()
    pairs = m.pairs(states)
    assert len(states) == 2 and len(pairs) == 2 and all(m.Q_is_forest(s) for _, s in pairs)
    r, s = pairs[0]
    rec = m.recover(s)
    two = m.two_factors(components=2)
    assert two
    return dict(model=m, xy=xy, R=L['R'], r=r, s=s, rec=rec, two_factor=two[0],
                counts=dict(states=len(states), pairs=len(pairs)))


def gluing():
    """Two octahedra glued along a triangle: the nested picture. Piece 1 is the
    octahedron with its central face as cap; piece 2 fills that face."""
    oc = octahedron()
    m1, xy1 = oc['model'], oc['xy']
    cap_index = next(i for i, f in enumerate(m1.F) if not set(f) & set(m1.roots))
    cap = m1.F[cap_index]                                   # (3, 4, 5)
    new = {cap[0]: 6, cap[1]: 7, cap[2]: 8}                 # new[v] is the inner vertex opposite v
    a, b, c = cap
    inner = [(a, b, new[c]), (b, c, new[a]), (c, a, new[b]),
             (a, new[c], new[b]), (b, new[a], new[c]), (c, new[b], new[a]), (new[a], new[b], new[c])]
    facesT = [f for i, f in enumerate(m1.F) if i != cap_index] + inner
    T = Model(facesT, m1.t0, m1.e0)
    assert len(T.V) == 9 and all(d % 2 == 0 for _, d in T.T.degree())
    tri = {tuple(sorted(c)) for c in nx.enumerate_all_cliques(T.T) if len(c) == 3}
    assert tri - {tuple(sorted(f)) for f in T.F} == {tuple(sorted(cap))}      # exactly one separating triangle
    n_pairs = len(T.pairs())
    # piece 1: the octahedron itself, with the cap as a face
    rec1 = oc['rec']
    lab = {v: k for k, part in enumerate(rec1['parts']) for v in part}
    same = [e for e in zip(cap, cap[1:] + cap[:1]) if lab[e[0]] == lab[e[1]]]
    assert len(same) == 1                                    # both labels occur on the cap
    e1 = und(*same[0])
    # piece 2: cap outside, prescribed edge e1
    faces2 = [tuple(reversed(cap))] + inner
    m2 = Model(faces2, 0, e1)
    st2 = [s for r, s in m2.pairs() if m2.Q_is_forest(s)]
    rec2 = m2.recover(st2[0])
    lab2 = {v: k for k, part in enumerate(rec2['parts']) for v in part}
    flip = lab2[e1[0]] != lab[e1[0]]
    for v in list(lab2):
        lab2[v] = lab2[v] ^ flip
    assert all(lab2[v] == lab[v] for v in cap)
    lab.update(lab2)
    parts = [sorted(v for v in lab if lab[v] == k) for k in (0, 1)]
    for p in parts:
        assert nx.is_tree(T.T.subgraph(p)), 'glued class is not an induced tree'
    assert set(T.e0) <= set(parts[0])
    P = sorted(e for e in T.E if lab[e[0]] == lab[e[1]])
    assert all(sum(und(x, y) in P for x, y in zip(f, f[1:] + f[:1])) == 1 for f in T.F)
    # coordinates: inner triangle of piece 2 inside the cap
    xy = dict(xy1)
    cen = sum(xy1[v] for v in cap) / 3
    for v in cap:
        opp = [u for u in cap if u != v]
        xy[new[v]] = cen + 0.42 * ((xy1[opp[0]] + xy1[opp[1]]) / 2 - cen) / 0.5 * 0.5
    check_layout(T, xy, oc['R'])
    # piece 2 on its own, drawn in the standard disk with the cap as outer face
    ang = {m2.e0[0]: 210, m2.e0[1]: 330}
    if m2.left[m2.e0[0], m2.e0[1]] == m2.t0:
        ang = {m2.e0[1]: 210, m2.e0[0]: 330}
    third = next(v for v in cap if v not in e1)
    ang[third] = 90
    R = oc['R']
    xy2 = {v: R * np.array([math.cos(math.radians(t)), math.sin(math.radians(t))]) for v, t in ang.items()}
    rho = float(np.hypot(*xy1[cap[0]]))
    for v in cap:
        xy2[new[v]] = -xy2[v] / R * rho
    check_layout(m2, xy2, R)
    return dict(T=T, n_pairs=n_pairs, xy=xy, R=R, m1=m1, xy1=xy1, m2=m2, xy2=xy2, cap=cap, e1=e1, parts=parts, P=P,
                parts1=rec1['parts'], P1=rec1['P'],
                parts2=[sorted(v for v in lab2 if lab2[v] == k) for k in (0, 1)], P2=rec2['P'])


def jsonable(x):
    if isinstance(x, Model):
        return dict(faces=x.F, t0=x.t0, e0=x.e0, roots=x.roots, A=x.A, X=x.X, black=x.black, white=x.white)
    if isinstance(x, dict):
        return {str(k): jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple, set, frozenset)):
        return [jsonable(v) for v in x]
    if isinstance(x, np.ndarray):
        return [round(float(v), 4) for v in x]
    if isinstance(x, (np.floating, float)):
        return round(float(x), 6)
    if isinstance(x, (np.integer,)):
        return int(x)
    return x


CHECKS = [
    'layouts: bounded faces counterclockwise, no crossing edges, roots on the circle',
    'running example: primal graph cubic, bipartite, 3-connected; dual Eulerian; no separating triangle',
    'all states and ordered pairs enumerated; every pair is two disjoint bijections A -> X',
    'disk identity (4.1), (4.2) and delta-sum -3/+3 on every directed cycle of D and of Q_s, over all pairs',
    'displayed pair is the unique pair with Q_s cyclic, Q_r a forest and a D-cycle enclosing a vertex',
    'B = I + l bijection on the displayed disk, face by face',
    'reversal of the Q_s cycle is an involution on the partners of s and changes J by 2; the cyclic terms sum to 0',
    'unit spoke circulations exist on H0; L+ - L- equals the number of white faces inside each D-cycle',
    'pairs grouped by undirected D: each group has 2^(cycles) members',
    'Q_r is a forest with one root per component; H - r is a tree; white-face tree; one selected edge per face',
    'P is a forest with two components; both classes induce trees; complementary dual is one Hamiltonian cycle',
    'a 2-factor of G with exactly two components exists',
    'cut inequality (3.1) for every subset S of X; r + s is a degree-two subgraph of the incidence graph',
    'octahedron: dual of the cube, 2 states, 2 pairs, recovery succeeds',
    'gluing example: one separating triangle, partitions of the two pieces agree on the cap and glue to two induced trees',
]

if __name__ == '__main__':
    run, oc, gl = running(), octahedron(), gluing()
    from geometry_check import verify
    geometry = verify([('running',run,run['r']),('octahedron',oc,oc['s'])])
    (HERE / 'geometry-validation.json').write_text(json.dumps(geometry,indent=1))
    (HERE / 'checked.json').write_text(json.dumps(jsonable(dict(running=run, octahedron=oc, gluing=gl)), indent=1))
    (HERE / 'validation.json').write_text(json.dumps(dict(status='COMPUTED', counts=run['counts'], checks=CHECKS), indent=1))
    k = run['disk']
    print('running', run['counts'])
    print('pair r', run['r'], 's', run['s'], 'J', run['J'], 'reversed r', run['r2'], 'J', run['J2'])
    print('disk', {x: k[x] for x in 'BWIhl'}, 'ccw', k['ccw'], '| L+-L-', [c['L_diff'] for c in run['D_cycles']])
    print('tight cut', run['tight_cut'], '| D groups', run['groups'])
    print('parts', run['rec']['parts'], '| gluing parts', gl['parts'], 'e1', gl['e1'])
