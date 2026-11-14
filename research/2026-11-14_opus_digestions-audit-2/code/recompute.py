"""Recompute every number quoted in digestions/steps/01-08 for the worked examples.

Run from the repository root:
    python research/2026-11-14_opus_digestions-audit-2/code/recompute.py

Orientation-dependent quantities (delta, clockwise/counterclockwise, J, eps,
heights) use paper/figures/model.py, whose stored face order is the paper's
counterclockwise drawing. Counts that do not depend on orientation (states,
pairs, good states, Q_s, recovery) are recomputed a second time with
workings/barnette_lab, which builds its own embedding. Heights are implemented
here from the definition in paper/main/barnette.tex, Section 4 ("Heights"):
shortest paths of faces in G from each white face to t0, ties broken by the
smallest face index, kappa = +1 if the turned corner is on the left of the path.

Writes ../outputs/recompute.json and prints a log (saved as ../outputs/recompute.txt).
"""
import itertools as it
import json
import math
import sys
from collections import Counter
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[3]
sys.dont_write_bytecode = True
sys.path[:0] = [str(ROOT / 'paper' / 'figures'), str(ROOT / 'workings' / 'barnette_lab')]
from model import Model, und, oriented_faces  # noqa: E402
from barnette_lab.core import Instance  # noqa: E402

OUT = {}


def say(*a):
    print(*a)


def check(cond, msg):
    if not cond:
        raise AssertionError(msg)
    return True


def name(m, t):
    return '.'.join(map(str, sorted(m.F[t])))


def eps(m, r, s):
    return math.prod(m.delta(a, b) for a, b in zip(r, s))


def good(m, s):
    Q = m.Q_graph(s)
    return nx.is_forest(Q) and all(len(set(c) & set(m.roots)) == 1 for c in nx.connected_components(Q))


def face_paths(m):
    dist = nx.single_source_shortest_path_length(m.G, m.t0)
    paths = {}
    for y in m.white:
        p = [y]
        while p[-1] != m.t0:
            p.append(min(w for w in m.G[p[-1]] if dist[w] == dist[p[-1]] - 1))
        paths[y] = p
    return paths


def kappa(m, paths):
    K = {}
    for y, p in paths.items():
        k = {}
        for a, t, b in zip(p, p[1:], p[2:]):
            if t not in m.A:
                continue
            f = m.F[t]
            ein, eout = set(m.F[a]) & set(f), set(f) & set(m.F[b])
            (v,) = ein & eout
            (fa,) = ein - {v}
            (fb,) = eout - {v}
            i = f.index(v)
            k[t, v] = 1 if (f[(i + 1) % 3], f[(i + 2) % 3]) == (fa, fb) else -1
        K[y] = k
    return K


def eta(m, K, s, y):
    return sum(K[y].get((t, v), 0) for t, v in zip(m.A, s))


def omega(m, K, s):
    return sum(eta(m, K, s, y) for y in m.white)


def two_factors(G):
    """Perfect matchings of a cubic graph, and the cycle count of each complement."""
    out = []
    E = sorted(G.edges())
    nodes = sorted(G)

    def rec(free, chosen):
        if not free:
            H = G.copy()
            H.remove_edges_from(chosen)
            out.append((tuple(chosen), nx.number_connected_components(H)))
            return
        u = min(free)
        for v in sorted(G[u]):
            if v in free:
                rec(free - {u, v}, chosen + [und(u, v)])
    rec(frozenset(nodes), [])
    return out


def lab_counts(m):
    b = Instance(m.T)
    b = Instance(m.T, next(i for i, f in enumerate(b.faces) if set(f) == set(m.roots)))
    ss = list(b.states())
    ps = b.pairs(ss)
    goods = [s for s in ss if b.is_tree(s)]
    return len(ss), len(ps), len(goods)


def summary(m, label):
    ss = m.states()
    ps = m.pairs(ss)
    partners = Counter(s for _, s in ps)
    goods = [s for s in ss if good(m, s)]
    forest = [s for s in ss if m.Q_is_forest(s)]
    lab = lab_counts(m)
    check(lab == (len(ss), len(ps), len(goods)), f'{label}: lab disagrees {lab}')
    check(all(partners[s] == 1 for s in goods), 'good state has one partner')
    check(all(good(m, s) for s in ss if partners[s] and m.Q_is_forest(s)), 'partnered forest is good')
    d = dict(V=len(m.V), faces=len(m.F), k=len(m.black), n=len(m.A), states=len(ss), pairs=len(ps),
             states_with_partner=len(partners), good=len(goods), forest_Q=len(forest),
             cyclic_second_states=sorted(set(s for _, s in ps if not m.Q_is_forest(s))))
    say(f'[{label}]', {k: v for k, v in d.items() if k != 'cyclic_second_states'}, 'lab agrees on states/pairs/good')
    return ss, ps, goods, d


def covers(m, ps, K):
    cl = {}
    for r, s in ps:
        cl.setdefault(frozenset(und(a, b) for a, b in zip(r, s)), []).append((r, s))
    res = []
    for key, members in cl.items():
        r, s = members[0]
        cyc = [m.disk(c) for c in m.directed_cycles(m.D(r, s))]
        rows = []
        for r_, s_ in members:
            ds = [m.disk(c) for c in m.directed_cycles(m.D(r_, s_))]
            rows.append(dict(r=r_, s=s_, ccw=sorted((k['h'], k['ccw']) for k in ds), J=m.J(r_, s_),
                             eps=eps(m, r_, s_), omega=omega(m, K, s_) if K else None,
                             good=good(m, s_)))
        res.append(dict(c=len(cyc), cycles=[dict(h=k['h'], W=k['W'], B=k['B'], I=k['I'], l=k['l'])
                                            for k in sorted(cyc, key=lambda k: -k['h'])], pairs=rows))
    return res


def disk_checks(m, ps):
    n = 0
    for r, s in ps:
        for c in m.directed_cycles(m.D(r, s)) + m.directed_cycles(m.Q_directed(r, s)):
            k = m.disk(c)
            check(k['W'] == k['B'] + 1 and k['h'] == 2 * k['l'] + 3 and k['B'] == k['I'] + k['l'], 'disk identity')
            check(k['delta_sum'] == (-3 if k['ccw'] else 3), 'delta sum convention')
            n += 1
    return n


def hamiltonian_counts(m):
    tf = two_factors(m.G)
    hist = Counter(c for _, c in tf)
    e0g = m.dual[m.e0]
    ham = [pm for pm, c in tf if c == 1]
    avoid = [pm for pm in ham if e0g in pm]
    return len(tf), dict(sorted(hist.items())), len(ham), len(avoid)


def sign_formula(m, ps):
    n = len(m.A)
    for r, s in ps:
        ds = [m.disk(c) for c in m.directed_cycles(m.D(r, s))]
        c, cp = len(ds), sum(k['ccw'] for k in ds)
        check((n - c) % 2 == 0, 'n = c mod 2')
        check(eps(m, r, s) == (-1) ** ((n + c) // 2) * (-1) ** cp, 'Lemma 4.4 sign formula')
        check(m.J(r, s) == (c - cp) - cp, 'J = #cw - #ccw')
        check(eps(m, r, s) == (-1) ** ((n + m.J(r, s)) // 2), 'eps = (-1)^((n+J)/2)')


# ---------------------------------------------------------------- running example
def running():
    data = json.loads((ROOT / 'paper' / 'figures' / 'running.json').read_text())
    m = Model(data['faces'], data['t0'], data['e0'])
    ss, ps, goods, d = summary(m, 'running')
    K = face_paths(m)
    K = kappa(m, K)
    paths = face_paths(m)
    fid = {frozenset(f): i for i, f in enumerate(m.F)}
    names = [name(m, t) for t in m.A]
    alpha = dict(zip(['0.1.6', '0.2.3', '1.7.8', '1.2.9', '3.4.9', '4.10.11', '5.6.11', '6.7.12', '8.11.12', '8.9.10'],
                     [1, 3, 7, 2, 9, 11, 6, 12, 8, 10]))
    beta = dict(zip(alpha, [6, 2, 8, 1, 3, 10, 11, 7, 12, 9]))
    a = tuple(alpha[x] for x in names)
    b = tuple(beta[x] for x in names)
    check(a in ss and b in ss and (b, a) in ps and (a, b) in ps, 'alpha, beta are states and form pairs')
    check(not m.Q_is_forest(a) and good(m, b), 'Q_alpha cyclic, beta good')
    qa = [sorted(c) for c in nx.cycle_basis(m.Q_graph(a))]
    qb = sorted(sorted(c) for c in nx.connected_components(m.Q_graph(b)))
    say('Face order of A in running.json:', list(zip(m.A, names)))
    say('alpha as tuple in A order:', a, ' beta:', b)
    say('Q_alpha cycles:', qa, ' Q_beta components:', qb)
    Dba = sorted((m.disk(c) for c in m.directed_cycles(m.D(b, a))), key=lambda k: -k['h'])
    for k in Dba:
        say('D(beta,alpha) cycle', k['cycle'], 'ccw' if k['ccw'] else 'cw', 'h', k['h'], 'l', k['l'], 'I', k['I'],
            'interior', k['interior'], 'B', k['B'], 'W', k['W'], 'delta-sum', k['delta_sum'])
    E7 = (3 * (Dba[0]['B'] + Dba[0]['W']) + Dba[0]['h']) // 2
    say('edges of R_Z for the 7-cycle:', E7, ' Euler V-E+F:', Dba[0]['I'] + Dba[0]['h'] - E7 + Dba[0]['B'] + Dba[0]['W'] + 1)
    # the cancelling partner
    qc = m.directed_cycles(m.Q_directed(b, a))
    bt = m.reverse_Q_cycle(b, a, qc[0])
    changed = [(name(m, t), x, y) for t, x, y in zip(m.A, b, bt) if x != y]
    say('Q-cycle of alpha directed by beta:', qc, '; beta~ =', bt, 'changes', changed)
    say('eps(beta,alpha) =', eps(m, b, a), 'J =', m.J(b, a), '; eps(beta~,alpha) =', eps(m, bt, a), 'J =', m.J(bt, a))
    Dbt = sorted((m.disk(c) for c in m.directed_cycles(m.D(bt, a))), key=lambda k: -k['h'])
    for k in Dbt:
        say('D(beta~,alpha) cycle', k['cycle'], 'ccw' if k['ccw'] else 'cw', 'h', k['h'], 'l', k['l'], 'I', k['I'],
            'B', k['B'], 'W', k['W'])
    cv = covers(m, ps, K)
    for c in cv:
        say('cover with', c['c'], 'cycles', [(x['h'], x['W']) for x in c['cycles']])
        for p in sorted(c['pairs'], key=lambda p: p['omega']):
            tag = 'alpha' if p['s'] == a else ('beta' if p['s'] == b else '')
            say('   ', p['ccw'], 'J', p['J'], 'eps', p['eps'], 'omega', p['omega'], 'good' if p['good'] else 'cycle in Q_s', tag)
    Sig = sum(eps(m, r, s) * omega(m, K, s) ** 2 for r, s in ps)
    S0 = sum(eps(m, r, s) for r, s in ps)
    S1 = sum(eps(m, r, s) * omega(m, K, s) for r, s in ps)
    say('sum eps =', S0, ' sum eps*omega =', S1, ' Sigma = sum eps*omega^2 =', Sig)
    poly = Counter()
    for r, s in ps:
        poly[omega(m, K, s)] += eps(m, r, s)
    poly = {k: v for k, v in sorted(poly.items()) if v}
    say('integer Laurent polynomial sum eps z^omega:', poly)
    # linear substitution w = 1 + x kappa, kappa = sum_y kappa_y
    import sympy as sp
    x = sp.Symbol('x')
    kap = Counter()
    for y in m.white:
        for key, val in K[y].items():
            kap[key] += val
    Px = sp.expand(sum(eps(m, r, s) * sp.prod([1 + x * kap[t, v] for t, v in zip(m.A, s)]) for r, s in ps))
    say('P(x) = sum eps prod (1 + x kappa(t,s(t))) =', Px)
    # heights example of Figure 10
    y = fid[frozenset({1, 8, 9})]
    say('path of y={1,8,9}:', [sorted(m.F[f]) for f in paths[y]], ' turns:', [(name(m, t), v, sg) for (t, v), sg in K[y].items()])
    cw7 = [p for c in cv for p in c['pairs'] if p['ccw'] == [(3, False), (7, False)] and c['cycles'][0]['W'] == 6][0]
    say('eta at y for the all-clockwise pair of the (6,1) cover:', eta(m, K, cw7['s'], y), '; eta_alpha(y) =', eta(m, K, a, y))
    # heights version with chosen faces: y1 inside the 7-cycle only, y2 inside the triangle
    for c in cv:
        r0, s0 = c['pairs'][0]['r'], c['pairs'][0]['s']
        for cyc in m.directed_cycles(m.D(r0, s0)):
            k = m.disk(cyc)
            say('   white faces inside', sorted(k['cycle']), ':', k['white'], [sorted(m.F[w]) for w in k['white']])
    for ys in [(8, 18), (18, 18)]:
        SF = sum(eps(m, r, s) * math.prod(eta(m, K, s, yy) for yy in ys) for r, s in ps)
        say('heights version: sum eps * prod eta_s(y) for y =', ys, [sorted(m.F[yy]) for yy in ys], '=', SF)
    # recovery
    rec = m.recover(b)
    say('P_beta =', rec['P'], ' parts:', rec['parts'])
    say('Hamiltonian cycle (faces in order from t0):', rec['cycle_order'])
    tf, hist, ham, avoid = hamiltonian_counts(m)
    say('2-factors of G:', tf, 'by number of cycles', hist, '; Hamiltonian cycles', ham, '; avoiding e0*', avoid)
    nd = disk_checks(m, ps)
    sign_formula(m, ps)
    say('disk identity and sign formulas asserted on', nd, 'directed cycles')
    # flow tight set
    tight = [S for k in range(1, 4) for S in it.combinations(m.X, k)
             if sum(min(2, len(set(m.F[t]) & set(S))) for t in m.A) == 2 * len(S)]
    say('tight sets S with |S|<=3 in (5.1):', tight)
    goods_omega = sorted((omega(m, K, s), [eps(m, r, s2) for r, s2 in ps if s2 == s][0]) for s in goods)
    say('good states (omega, sign of their pair):', goods_omega)
    OUT['running'] = dict(summary=d, alpha=a, beta=b, beta_tilde=bt, Q_alpha_cycles=qa, Q_beta_components=qb,
                          D_beta_alpha=[{k: v for k, v in x.items() if k in ('cycle', 'ccw', 'h', 'l', 'I', 'interior', 'B', 'W', 'delta_sum')} for x in Dba],
                          eps_beta_alpha=eps(m, b, a), eps_betatilde_alpha=eps(m, bt, a),
                          covers=cv, Sigma=Sig, sum_eps=S0, sum_eps_omega=S1, laurent=poly, P_linear=str(Px),
                          P_beta=rec['P'], parts=rec['parts'], cycle_order=rec['cycle_order'],
                          two_factors=tf, two_factor_hist=hist, hamiltonian=ham, avoiding=avoid, tight=tight)


# ---------------------------------------------------------------- cube
def cube():
    data = json.loads((ROOT / 'paper' / 'figures' / 'octahedron.json').read_text())
    m = Model(data['faces'], data['t0'], data['e0'])
    ss, ps, goods, d = summary(m, 'cube')
    say('A =', [(t, m.F[t]) for t in m.A], 'X =', m.X, 'roots', m.roots)
    say('states:', ss, ' Q:', [m.Q(s) for s in ss])
    for r, s in ps:
        ds = [m.disk(c) for c in m.directed_cycles(m.D(r, s))]
        say('pair', (r, s), 'D cycles', [(k['cycle'], 'ccw' if k['ccw'] else 'cw', k['W'], k['delta_sum']) for k in ds],
            'J', m.J(r, s), 'eps', eps(m, r, s))
    K = kappa(m, face_paths(m))
    say('omega of the two states:', [omega(m, K, s) for s in ss])
    for s in ss:
        rec = m.recover(s)
        say('recover', s, 'P', rec['P'], 'parts', rec['parts'], 'white tree', rec['white_tree'], 'y0', rec['y0'],
            'cycle', rec['cycle_order'])
    tf, hist, ham, avoid = hamiltonian_counts(m)
    say('cube 2-factors', tf, hist, 'Hamiltonian', ham, 'avoiding e0*', avoid)
    bad = [pm for pm, c in two_factors(m.G) if c > 1]
    say('cube disconnected 2-factors (omitted matchings):', bad)
    sign_formula(m, ps)
    OUT['cube'] = dict(summary=d, states=ss, two_factors=tf, hist=hist, hamiltonian=ham, avoiding=avoid, bad=bad)


# ---------------------------------------------------------------- hexagonal prism
def prism():
    T = nx.Graph()
    for i in range(6):
        T.add_edges_from([(i, (i + 1) % 6), (6, i), (7, i)])
    faces = oriented_faces(T)
    t0 = next(i for i, f in enumerate(faces) if set(f) == {6, 0, 1})
    res = {}
    for e0 in [(0, 1), (0, 6), (1, 6)]:
        m = Model(faces, t0, e0)
        ss, ps, goods, d = summary(m, f'prism e0={e0}')
        tf, hist, ham, avoid = hamiltonian_counts(m)
        res[str(e0)] = dict(summary=d, hamiltonian=ham, avoiding=avoid, good=len(goods))
        say('   2-factors', tf, hist, 'Hamiltonian', ham, 'avoiding e0*', avoid)
        if e0 == (0, 1):
            third = [s for s in ss if not good(m, s)]
            for s in third:
                comps = [sorted(c) for c in nx.connected_components(m.Q_graph(s))]
                say('   non-good state', dict(zip([tuple(m.F[t]) for t in m.A], s)), 'Q', m.Q(s),
                    'forest', m.Q_is_forest(s), 'components', comps, 'partners', sum(1 for _, x in ps if x == s))
            # which avoiding cycles are produced
            produced = set()
            for s in goods:
                rec = m.recover(s)
                produced.add(frozenset(map(tuple, rec['hamiltonian'])))
            say('   cycles produced by recovery:', len(produced))
            res[str(e0)]['tf_hist'] = hist
            res[str(e0)]['two_factors'] = tf
    OUT['prism'] = res


# ---------------------------------------------------------------- double octahedron
def double_octahedron():
    T = nx.Graph()
    for u, v in it.combinations(range(6), 2):
        if {u, v} not in ({0, 3}, {1, 4}, {2, 5}):
            T.add_edge(u, v)
    for u, v in it.combinations(range(3, 9), 2):
        if {u, v} not in ({3, 6}, {4, 7}, {5, 8}):
            T.add_edge(u, v)
    faces = oriented_faces(T)
    check(len(faces) == 14, 'double octahedron has 14 faces')
    tally = Counter()
    for t0 in range(14):
        e0 = tuple(faces[t0][:2])
        m = Model(faces, t0, e0)
        ss = m.states()
        ps = m.pairs(ss)
        g = [s for s in ss if good(m, s)]
        tally[(len(ss), len(ps), len(g))] += 1
    say('[double octahedron] (states, pairs, good) over the 14 outer faces:', dict(tally))
    # the bad root (0,1,5) or its mirror: inner faces along 3,4,5 black
    t0 = next(i for i, f in enumerate(faces) if set(f) == {0, 1, 5})
    m = Model(faces, t0, (0, 1))
    S = (6, 7, 8)
    supply = sum(min(2, len(set(m.F[t]) & set(S))) for t in m.A)
    say('   root (0,1,5): states', len(m.states()), 'pairs', len(m.pairs()), '; S={6,7,8} needs 6, supply', supply)
    OUT['double_octahedron'] = dict(tally={str(k): v for k, v in tally.items()}, supply=supply)


# ---------------------------------------------------------------- 16-vertex example
def sixteen():
    faces = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (1, 4, 5), (1, 5, 2), (2, 5, 6), (2, 6, 7), (2, 7, 3), (3, 7, 8),
             (3, 8, 9), (3, 9, 4), (4, 9, 10), (4, 10, 5), (5, 10, 11), (5, 11, 6), (6, 11, 7), (7, 11, 12), (7, 12, 13),
             (7, 13, 14), (7, 14, 8), (8, 14, 9), (9, 13, 10), (9, 14, 13), (10, 13, 15), (10, 15, 11), (11, 15, 12),
             (12, 15, 13)]
    m = Model(faces, 8, (2, 7))
    ss, ps, goods, d = summary(m, '16-vertex class 158')
    K = kappa(m, face_paths(m))
    cv = covers(m, ps, K)
    for c in cv:
        say('   cover with', c['c'], 'cycles', [(x['h'], x['W']) for x in c['cycles']], 'good pairs',
            sum(p['good'] for p in c['pairs']), 'of', len(c['pairs']))
    OUT['sixteen'] = dict(summary=d, covers=[dict(c=c['c'], cycles=c['cycles'], good=sum(p['good'] for p in c['pairs']))
                                             for c in cv])


if __name__ == '__main__':
    running()
    cube()
    prism()
    double_octahedron()
    sixteen()
    o = Path(__file__).resolve().parents[1] / 'outputs'
    o.mkdir(exist_ok=True)

    def plain(v):
        if isinstance(v, dict):
            return {str(k): plain(x) for k, x in v.items()}
        if isinstance(v, (list, tuple, set, frozenset)):
            return [plain(x) for x in v]
        return v
    (o / 'recompute.json').write_text(json.dumps(plain(OUT), indent=1))
    say('ALL ASSERTIONS PASSED')
