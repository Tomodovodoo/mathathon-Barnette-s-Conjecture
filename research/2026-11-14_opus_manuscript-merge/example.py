"""Recompute every number that paper/main/barnette.tex prints about its examples.

Orientation-dependent quantities (delta, clockwise, heights) use the oriented
faces of paper/figures/running.json through paper/figures/model.py, which is the
orientation of the figures. Orientation-free counts are cross-checked with the
independent implementation in workings/barnette_lab.

Run from the repository root:
    python research/2026-11-14_opus_manuscript-merge/example.py > research/2026-11-14_opus_manuscript-merge/example.txt
It also writes research/2026-11-14_opus_manuscript-merge/example.json, which
paper/figures/draw.py reads for the heights figure.
"""
import json
import sys
from collections import Counter
from math import prod
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'paper' / 'figures'))
sys.path.insert(0, str(ROOT / 'workings' / 'barnette_lab'))
from model import Model, und  # noqa: E402
from barnette_lab.core import Instance  # noqa: E402

OUT = {}


def say(*a):
    print(*a)


def face_paths(m):
    """For each white face a shortest path of faces to t0, ties broken by face index."""
    paths = {}
    for y in m.white:
        dist = nx.single_source_shortest_path_length(m.G, m.t0)
        path, cur = [y], y
        while cur != m.t0:
            cur = min(w for w in m.G[cur] if dist[w] == dist[cur] - 1)
            path.append(cur)
        paths[y] = path
    return paths


def kappa(m, paths):
    """kappa[y][(t, v)] = +1 if the path of y turns around v in t with v on its left,
    -1 if on its right. Combinatorial test: with a the far end of the entry side and
    b the far end of the exit side, v is on the left iff (v, a, b) is the
    counterclockwise order of the corners of t."""
    K = {}
    for y, path in paths.items():
        k = {}
        for prev, t, nxt in zip(path, path[1:], path[2:]):
            if t not in m.A:
                continue
            f = m.F[t]
            e_in = set(m.F[prev]) & set(f)
            e_out = set(f) & set(m.F[nxt])
            assert len(e_in) == 2 and len(e_out) == 2 and e_in != e_out
            (v,) = e_in & e_out
            (a,) = e_in - {v}
            (b,) = e_out - {v}
            i = f.index(v)
            ccw = (f[(i + 1) % 3], f[(i + 2) % 3]) == (a, b)   # faces stored counterclockwise
            k[t, v] = 1 if ccw else -1
        K[y] = k
    return K


def main():
    run = json.load(open(ROOT / 'paper/figures/running.json'))
    m = Model(run['faces'], run['t0'], run['e0'])
    say('running example: |V| =', len(m.V), ' faces =', len(m.F), ' edges =', len(m.E),
        ' black =', len(m.black), ' white =', len(m.white), ' roots =', m.roots, ' e0 =', m.e0)
    n = len(m.A)
    states = m.states()
    pairs = m.pairs(states)
    good = [s for s in states if m.Q_is_forest(s) and
            all(len(set(c) & set(m.roots)) == 1 for c in nx.connected_components(m.Q_graph(s)))]
    with_partner = {s for _, s in pairs}
    say('n =', n, ' states =', len(states), ' pairs =', len(pairs), ' good states =', len(good),
        ' good states with a partner =', len([s for s in good if s in with_partner]))
    cyclic_second = sorted({s for r, s in pairs if not m.Q_is_forest(s)})
    say('second states with cyclic Q_s:', cyclic_second)

    # sign as a product of local signs, against (-1)^((n+J)/2)
    def eps(r, s):
        return prod(m.delta(a, b) for a, b in zip(r, s))
    for r, s in pairs:
        J = m.J(r, s)
        assert eps(r, s) == (-1) ** ((n + J) // 2)
    say('eps = prod delta equals (-1)^((n+J)/2) on all', len(pairs), 'pairs')

    # the two named states: alpha has cyclic Q, beta is good, (beta, alpha) a pair
    (alpha,) = cyclic_second
    betas = [r for r, s in pairs if s == alpha and m.Q_is_forest(r)
             and any(m.disk(c)['I'] >= 1 for c in m.directed_cycles(m.D(r, s)))]
    assert len(betas) == 1
    beta = betas[0]
    assert m.is_pair(alpha, beta)
    lab = {t: sorted(m.F[t]) for t in m.A}
    say('faces A (sorted corners):', [lab[t] for t in m.A])
    say('alpha =', alpha)
    say('beta  =', beta)
    OUT['alpha'], OUT['beta'] = list(alpha), list(beta)
    OUT['A'] = m.A
    OUT['faces_A'] = [lab[t] for t in m.A]
    say('Q_alpha cycles:', [c for c in nx.cycle_basis(m.Q_graph(alpha))])
    comps = [sorted(c) for c in nx.connected_components(m.Q_graph(beta))]
    say('Q_beta components:', comps)

    # D(beta, alpha)
    dc = [m.disk(c) for c in m.directed_cycles(m.D(beta, alpha))]
    for k in dc:
        say('D(beta,alpha) cycle', k['cycle'], 'ccw' if k['ccw'] else 'cw', 'h =', k['h'], 'B =', k['B'], 'W =', k['W'],
            'I =', k['I'], 'interior =', k['interior'], 'l =', k['l'], 'delta-sum =', k['delta_sum'])
    OUT['D_cycles'] = [dict(cycle=k['cycle'], ccw=k['ccw'], h=k['h'], B=k['B'], W=k['W'], I=k['I'], l=k['l'],
                            white=k['white']) for k in dc]

    # cancellation: the two partners of alpha
    partners = [r for r, s in pairs if s == alpha]
    say('partners of alpha:', partners, ' eps:', [eps(r, alpha) for r in partners])
    qc = m.directed_cycles(m.Q_directed(beta, alpha))
    assert len(qc) == 1
    beta2 = m.reverse_Q_cycle(beta, alpha, qc[0])
    changed = [(lab[t], a, b) for t, a, b in zip(m.A, beta, beta2) if a != b]
    say('reversing the Q_alpha cycle', qc[0], 'changes beta at', changed)
    OUT['beta_tilde'] = list(beta2)

    # face-path heights
    paths = face_paths(m)
    K = kappa(m, paths)

    def eta(s, y):
        return sum(K[y].get((t, v), 0) for t, v in zip(m.A, s))

    def omega(s):
        return sum(eta(s, y) for y in m.white)

    # Lemma: reversing a clockwise cycle C of D(r, s) raises eta(y) by [y inside C]
    nrev = 0
    for r, s in pairs:
        for c in m.directed_cycles(m.D(r, s)):
            k = m.disk(c)
            on = {(a, b) for a, b in zip(c, c[1:] + c[:1])}
            r2 = tuple(b if (a, b) in on else a for a, b in zip(r, s))
            s2 = tuple(a if (a, b) in on else b for a, b in zip(r, s))
            assert m.is_pair(r2, s2)
            for y in m.white:
                d = eta(s2, y) - eta(s, y)
                want = (1 if y in k['white'] else 0) * (-1 if k['ccw'] else 1)
                assert d == want, (r, s, c, y, d, want)
            nrev += 1
    say('height lemma checked on', nrev, 'reversals of D-cycles, all white faces')

    # classes and the table
    cls = {}
    for r, s in pairs:
        key = frozenset(und(a, b) for a, b in zip(r, s))
        cls.setdefault(key, []).append((r, s))
    rows = []
    for key, members in cls.items():
        cyc0 = [m.disk(c) for c in m.directed_cycles(m.D(*members[0]))]
        Ls = sorted((k['W'] for k in cyc0), reverse=True)
        for r, s in members:
            cy = sorted((m.disk(c) for c in m.directed_cycles(m.D(r, s))), key=lambda k: -k['h'])
            rows.append(dict(L=Ls, orient=['ccw' if k['ccw'] else 'cw' for k in cy], eps=eps(r, s), omega=omega(s),
                             good=s in good, second=s == alpha, r=r, s=s))
    rows.sort(key=lambda d: (-d['L'][0], d['orient']))
    say('pairs (class L, orientations of long cycle and triangle, eps, omega(s), second state):')
    for d in rows:
        say('  L =', d['L'], d['orient'], 'eps =', d['eps'], 'omega =', d['omega'],
            'good' if d['good'] else 'cycle in Q_s', 'r =', d['r'], 's =', d['s'])
    OUT['rows'] = [{k: (list(v) if isinstance(v, tuple) else v) for k, v in d.items()} for d in rows]
    for j in range(4):
        say('sum eps * omega^%d =' % j, sum(eps(r, s) * omega(s) ** j for r, s in pairs))
    mmin = min(len(m.directed_cycles(m.D(r, s))) for r, s in pairs)
    say('m =', mmin, ' predicted (-1)^((n-m)/2) m! sum prod L =',
        (-1) ** ((n - mmin) // 2) * 2 * sum(d['L'][0] * d['L'][1] for d in rows) // 4)

    # the heights figure: white face {1,8,9}
    y = next(w for w in m.white if sorted(m.F[w]) == [1, 8, 9])
    path = paths[y]
    say('path of faces from {1,8,9} to t0:', [sorted(m.F[f]) for f in path])
    turns = [(sorted(m.F[t]), v, s_) for (t, v), s_ in K[y].items()]
    say('turned corners (face, corner, +1 left / -1 right):', turns)
    long_ = next(k for k in dc if k['h'] == 7)
    on = {(a, b) for a, b in zip(long_['cycle'], long_['cycle'][1:] + long_['cycle'][:1])}
    # pair with the 7-cycle clockwise: reverse it in (beta, alpha)
    rcw = tuple(b if (a, b) in on else a for a, b in zip(beta, alpha))
    scw = tuple(a if (a, b) in on else b for a, b in zip(beta, alpha))
    say('second state with the 7-cycle clockwise:', scw, ' eta(y) =', eta(scw, y))
    say('second state alpha (7-cycle counterclockwise):', alpha, ' eta(y) =', eta(alpha, y))
    OUT['heights'] = dict(y=y, path=path, turns=[[t, v, s_] for (t, v), s_ in K[y].items()],
                          s_cw=list(scw), r_cw=list(rcw), eta_cw=eta(scw, y), eta_ccw=eta(alpha, y))

    # recovery from beta
    rec = m.recover(beta)
    say('P_beta components:', rec['parts'], ' |P| =', len(rec['P']))
    # Hamiltonian cycles of G avoiding the edge across e0
    forced = next(g for g, te in m.cross.items() if und(*te) == m.e0)
    hcs = []

    def recm(free, chosen):
        if not free:
            h = m.G.copy()
            h.remove_edges_from(chosen)
            if nx.is_connected(h):
                hcs.append(frozenset(chosen))
            return
        v = min(free)
        for w in m.G[v]:
            if w in free:
                recm(free - {v, w}, chosen + [und(v, w)])
    recm(set(m.G) - set(forced), [und(*forced)])
    produced = set()
    for s in good:
        P = m.recover(s)['P']
        produced.add(frozenset(g for g, te in m.cross.items() if und(*te) in P))
    say('Hamiltonian cycles avoiding the edge across e0:', len(hcs), ' produced from good states:', len(produced),
        ' all produced:', produced == set(hcs))

    # independent cross-check with barnette_lab
    t = nx.Graph()
    for f in run['faces']:
        for a, b in zip(f, f[1:] + f[:1]):
            t.add_edge(a, b)
    probe = Instance(t, 0)
    outer = next(i for i, f in enumerate(probe.faces) if set(f) == {0, 4, 5})
    inst = Instance(t, outer)
    ls = list(inst.states())
    lp = inst.pairs(ls)
    lt = [s for s in ls if inst.is_tree(s)]
    w = inst.weights()
    lom = {s: sum(w[tt, v] for tt, v in zip(inst.A, s)) for s in ls}
    say('barnette_lab: states', len(ls), 'pairs', len(lp), 'tree states', len(lt),
        'sum sign*omega^2 (lab weights)', sum(inst.sign(r, s) * lom[s] ** 2 for r, s in lp))

    # cube = octahedron
    oc = json.load(open(ROOT / 'paper/figures/octahedron.json'))
    om = Model(oc['faces'], oc['t0'], oc.get('e0'))
    ost = om.states()
    op = om.pairs(ost)
    say('octahedron: roots', om.roots, 'states', ost, 'pairs', len(op),
        'Q forests', [om.Q_is_forest(s) for s in ost], 'faces A', [sorted(om.F[t]) for t in om.A])

    # hexagonal prism = dual of the hexagonal bipyramid
    faces = []
    k = 6
    for i in range(k):
        j = (i + 1) % k
        faces.append([i, j, k])
        faces.append([j, i, k + 1])
    bt = nx.Graph()
    for f in faces:
        for a, b in zip(f, f[1:] + f[:1]):
            bt.add_edge(a, b)
    probe = Instance(bt, 0)
    for e0 in [(0, 1), (0, 6), (1, 6)]:
        o = next(i for i, f in enumerate(probe.faces) if set(f) == {0, 1, 6})
        ins = Instance(bt, o)
        st = list(ins.states())
        trees = [s for s in st if ins.is_tree(s)]
        g = ins.G
        forced = ins.dual_edges[tuple(sorted(e0))]
        cnt = []

        def rec2(free, chosen):
            if not free:
                h = g.copy()
                h.remove_edges_from(chosen)
                if nx.is_connected(h):
                    cnt.append(1)
                return
            v = min(free)
            for w2 in g[v]:
                if w2 in free:
                    rec2(free - {v, w2}, chosen + [tuple(sorted((v, w2)))])
        rec2(set(g) - set(forced), [tuple(sorted(forced))])
        say('hexagonal prism, t0 = {0,1,6}, e0 =', e0, ': states', len(st), 'good', len(trees),
            'pairs', len(ins.pairs(st)), 'Hamiltonian cycles avoiding the edge', len(cnt))

    # two octahedra glued along a face: pairs for each choice of outer face
    import check  # paper/figures/check.py
    gl = check.gluing()
    gT = gl['T']
    res = Counter()
    for t0 in range(len(gT.F)):
        mm = Model(gT.F, t0)
        tri = {tuple(sorted(c)) for c in nx.enumerate_all_cliques(mm.T) if len(c) == 3}
        seps = [c for c in tri if c not in {tuple(sorted(f)) for f in mm.F}]
        npairs = len(mm.pairs())
        res[(t0 in gT.black, npairs > 0)] += 1
    say('two octahedra glued (9 vertices): separating triangles', seps,
        '; outer faces by (same colour as original t0, has a pair):', dict(res))

    # the 11-vertex incidence graph of the triangular bipyramid
    bf = [(0, 1, 3), (1, 2, 3), (2, 0, 3), (1, 0, 4), (2, 1, 4), (0, 2, 4)]
    I = nx.Graph()
    for i, f in enumerate(bf):
        for v in f:
            I.add_edge(('v', v), ('f', i))
    planar, _ = nx.check_planarity(I)
    say('bipyramid incidence graph: vertices', I.number_of_nodes(), 'edges', I.number_of_edges(), 'planar', planar,
        'bipartite classes', sorted(len(c) for c in nx.bipartite.sets(I)), 'connectivity', nx.node_connectivity(I))

    (Path(__file__).parent / 'example.json').write_text(json.dumps(OUT, indent=1, default=list))


if __name__ == '__main__':
    main()
