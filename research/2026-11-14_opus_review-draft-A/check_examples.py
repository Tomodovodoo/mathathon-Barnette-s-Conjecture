"""Independent recomputation of every number in draft A's worked examples.

Run from the repository root:
    python research/2026-11-14_opus_review-draft-A/check_examples.py

Inputs (read only): paper/figures/{octahedron,running}.json and the matching
layout-*.json (straight-line coordinates of the figure embedding).
Orientation-sensitive quantities (delta, J, cw/ccw, heights) are computed here
from the oriented face triples and the coordinates, NOT from barnette_lab,
because networkx may return the mirror embedding. barnette_lab is used only as a
cross-check for orientation-free objects (states, pairs, forest test, recovery).
Heights are computed literally from the draft's definition: a straight ray from
the centroid of each white face to infinity (inside t0), signed crossings with
the spokes c_t -> v, +1 when the spoke crosses from the ray's right to its left.
Output: check_examples.json next to this script.
"""
import json, math, sys, itertools
from pathlib import Path
from fractions import Fraction

ROOT = Path(__file__).resolve().parents[2]
FIG = ROOT / 'paper' / 'figures'
sys.path.insert(0, str(ROOT / 'workings' / 'barnette_lab'))
import networkx as nx
from barnette_lab.core import Instance

OUT = {}


def load(name):
    d = json.loads((FIG / f'{name}.json').read_text())
    lay = json.loads((FIG / f'layout-{name}.json').read_text())
    roots = {int(k): a for k, a in lay['root_angles'].items()}
    # Tutte barycentric embedding with the figure's root angles: a planar straight-line
    # drawing with the same orientation as the figure (the shared layout uses curved edges).
    import numpy as np
    V = sorted({v for f in d['faces'] for v in f}); idx = {v: i for i, v in enumerate(V)}
    nb = {v: set() for v in V}
    for f in d['faces']:
        for a, b in zip(f, f[1:] + f[:1]): nb[a].add(b); nb[b].add(a)
    M = np.zeros((len(V), len(V))); rhs = np.zeros((len(V), 2))
    for v in V:
        i = idx[v]
        if v in roots:
            M[i, i] = 1; a = math.radians(roots[v]); rhs[i] = (5 * math.cos(a), 5 * math.sin(a))
        else:
            M[i, i] = len(nb[v])
            for w in nb[v]: M[i, idx[w]] -= 1
    sol = np.linalg.solve(M, rhs)
    xy = {v: (float(sol[idx[v]][0]), float(sol[idx[v]][1])) for v in V}
    return d, xy


def area(xy, f):
    (ax, ay), (bx, by), (cx, cy) = (xy[v] for v in f)
    return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)


class Tri:
    def __init__(self, d, xy):
        self.faces = [tuple(f) for f in d['faces']]
        self.t0 = int(d['t0'])
        self.e0 = tuple(sorted(d['e0']))
        self.xy = xy
        # orientation: bounded faces should be ccw in the layout
        signs = [area(xy, f) > 0 for i, f in enumerate(self.faces) if i != self.t0]
        assert all(signs) or not any(signs), 'inconsistent orientation'
        self.mirror = not all(signs)
        if self.mirror:  # make bounded faces ccw
            self.faces = [tuple(reversed(f)) for f in self.faces]
        self.left = {}
        for i, f in enumerate(self.faces):
            for a, b in zip(f, f[1:] + f[:1]):
                assert (a, b) not in self.left
                self.left[a, b] = i
        # 2-colouring of faces, t0 black
        g = nx.Graph()
        for (a, b), i in self.left.items():
            g.add_edge(i, self.left[b, a])
        col = nx.bipartite.color(g)
        self.black = {i for i in g if col[i] == col[self.t0]}
        self.white = set(g) - self.black
        self.R = set(self.faces[self.t0])
        self.V = sorted({v for f in self.faces for v in f})
        self.X = sorted(set(self.V) - self.R)
        self.A = sorted(self.black - {self.t0})
        self.n = len(self.A)
        self.T = nx.Graph([(a, b) for (a, b) in self.left])
        self.cent = {i: tuple(sum(xy[v][k] for v in self.faces[i]) / 3 for k in (0, 1)) for i in range(len(self.faces))}

    def delta(self, v, w):
        return 1 if self.left[v, w] in self.black else -1

    def states(self):
        def rec(i, used, st):
            if i == self.n:
                yield tuple(st); return
            for v in sorted(set(self.faces[self.A[i]]) - self.R - used):
                yield from rec(i + 1, used | {v}, st + [v])
        return list(rec(0, set(), []))

    def pairs(self):
        S = self.states()
        return [(r, s) for r in S for s in S if all(a != b for a, b in zip(r, s))]

    def Q(self, s):
        q = nx.Graph(); q.add_nodes_from(self.V)
        for t, v in zip(self.A, s):
            a, b = set(self.faces[t]) - {v}
            q.add_edge(a, b)
        return q

    def dcycles(self, r, s):
        succ = dict(zip(r, s)); face = {a: t for t, a in zip(self.A, r)}
        seen, out = set(), []
        for x in self.X:
            if x in seen: continue
            cyc = [x]; seen.add(x)
            while succ[cyc[-1]] != x:
                cyc.append(succ[cyc[-1]]); seen.add(cyc[-1])
            dsum = sum(self.delta(a, succ[a]) for a in cyc)
            out.append({'vertices': cyc, 'faces': sorted(face[a] for a in cyc), 'delta_sum': dsum,
                        'orientation': 'ccw' if dsum == -3 else 'cw' if dsum == 3 else 'BAD'})
        return out

    def J(self, r, s):
        j = sum(self.delta(a, b) for a, b in zip(r, s)); assert j % 3 == 0; return j // 3

    def eps(self, r, s):
        return (-1) ** ((self.n + self.J(r, s)) // 2)

    def eps_local(self, r, s):
        return math.prod(self.delta(a, b) for a, b in zip(r, s))

    # --- geometry for heights and enclosure
    def inside_polygon(self, p, poly):
        x, y = p; c = False
        for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
            if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
                c = not c
        return c

    def disk_data(self, cyc):
        poly = [self.xy[v] for v in cyc]
        inside_faces = [i for i in range(len(self.faces)) if i != self.t0 and self.inside_polygon(self.cent[i], poly)]
        B = sum(1 for i in inside_faces if i in self.black)
        W = sum(1 for i in inside_faces if i in self.white)
        I = [v for v in self.V if v not in cyc and self.inside_polygon(self.xy[v], poly)]
        h = len(cyc)
        ell = sum(1 for a, b in zip(cyc, cyc[1:] + cyc[:1])
                  if (self.left[a, b] in inside_faces and self.left[a, b] in self.black)
                  or (self.left[b, a] in inside_faces and self.left[b, a] in self.black))
        return {'B': B, 'W': W, 'I': len(I), 'interior_vertices': I, 'h': h, 'ell': ell,
                'white_inside': sorted(i for i in inside_faces if i in self.white)}

    def height(self, s, w, direction=(0.8191520442889918, 0.5735764363510461)):
        p0 = self.cent[w]; dx, dy = direction; far = (p0[0] + 1e3 * dx, p0[1] + 1e3 * dy)
        h = 0
        for t, v in zip(self.A, s):
            c = self.cent[t]; q = self.xy[v]
            hit = seg_cross(p0, far, c, q)
            if hit:
                cr = dx * (q[1] - c[1]) - dy * (q[0] - c[0])
                h += 1 if cr > 0 else -1
        return h


def seg_cross(p1, p2, q1, q2):
    def o(a, b, c):
        v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        assert abs(v) > 1e-12, 'degenerate crossing, change ray direction'
        return v > 0
    return o(p1, p2, q1) != o(p1, p2, q2) and o(q1, q2, p1) != o(q1, q2, p2)


def name(T, i):
    return ''.join(str(v) if v < 10 else f'·{v}' for v in sorted(T.faces[i]))


def run(label, d, xy, r=None, s=None):
    T = Tri(d, xy)
    res = {'mirrored_input': T.mirror, 'n': T.n, 'roots': sorted(T.R),
           'A': {f'a{t}': sorted(T.faces[t]) for t in T.A}}
    P = T.pairs(); S = T.states()
    res['num_states'] = len(S); res['num_pairs'] = len(P)
    forest = [p for p in P if nx.is_forest(T.Q(p[1]))]
    res['num_forest_pairs'] = len(forest)
    # local-sign simplification: eps == prod delta, on every pair
    res['eps_equals_prod_delta_all_pairs'] = all(T.eps(*p) == T.eps_local(*p) for p in P)
    # group by undirected D
    groups = {}
    for p in P:
        key = frozenset(frozenset((a, b)) for a, b in zip(*p))
        groups.setdefault(key, []).append(p)
    res['groups'] = [{'size': len(g), 'cycles': len(T.dcycles(*g[0])),
                      'forest_pairs': sum(nx.is_forest(T.Q(q[1])) for q in g)} for g in groups.values()]
    m = min(len(T.dcycles(*p)) for p in P)
    res['m'] = m
    # Lemma 4 check on every state with a partner
    ok4 = True
    for s_ in {p[1] for p in P}:
        Q = T.Q(s_)
        for comp in nx.connected_components(Q):
            sub = Q.subgraph(comp); a = len(comp & T.R)
            if not ((a == 1 and nx.is_tree(sub)) or (a == 0 and sub.number_of_edges() == len(comp))):
                ok4 = False
    res['lemma4_all_partnered_states'] = ok4
    if r is not None:
        res['pair_given_is_pair'] = (r, s) in P
        res['Q_s_cycles'] = [sorted(c) for c in nx.cycle_basis(T.Q(s))]
        res['Q_r_forest'] = nx.is_forest(T.Q(r))
        res['Q_r_components'] = [sorted(c) for c in nx.connected_components(T.Q(r))]
        res['Q_s_edges'] = sorted(tuple(sorted(e)) for e in T.Q(s).edges())
        dc = T.dcycles(r, s); res['D_rs'] = dc; res['J_rs'] = T.J(r, s); res['eps_rs'] = T.eps(r, s)
        res['disk'] = [T.disk_data(c['vertices']) for c in dc]
        # Q_s involution
        if res['Q_s_cycles']:
            K = res['Q_s_cycles'][0]
            r2 = list(r)
            for i, t in enumerate(T.A):
                a, b = set(T.faces[t]) - {s[i]}
                if a in K and b in K and r[i] in K:
                    r2[i] = (set(T.faces[t]) - {r[i], s[i]}).pop()
            r2 = tuple(r2)
            res['Q_involution'] = {'K': K, 'r_prime': r2, 'is_pair': (r2, s) in P,
                                   'changed': {f'a{T.A[i]}': [r[i], r2[i]] for i in range(T.n) if r[i] != r2[i]},
                                   'J': [T.J(r, s), T.J(r2, s)], 'eps': [T.eps(r, s), T.eps(r2, s)],
                                   'D_r2s': T.dcycles(r2, s)}
        # heights: verify (10) on the group of D(r,s) for every white face, two ray directions
        key = frozenset(frozenset((a, b)) for a, b in zip(r, s))
        g = groups[key]
        ok10 = True; detail = []
        for dirn in [(0.8191520442889918, 0.5735764363510461), (-0.2588190451, 0.9659258263)]:
            base = None
            for q in g:
                cyc = T.dcycles(*q)
                U = [c for c in cyc if c['orientation'] == 'ccw']
                if not U: base = q
            for q in g:
                cyc = T.dcycles(*q)
                U = [c for c in cyc if c['orientation'] == 'ccw']
                for w in T.white:
                    pred = T.height(base[1], w, dirn) + sum(w in T.disk_data(c['vertices'])['white_inside'] for c in U)
                    if T.height(q[1], w, dirn) != pred: ok10 = False
        res['height_change_eq10_holds_on_group'] = ok10
        # product of heights and group totals (needs m factors chosen in the minimiser D(r,s))
        if len(dc) == m:
            dd = [T.disk_data(c['vertices']) for c in dc]
            ws = res.get('_ws')
        res['white_faces'] = {f'a{w}': name(T, w) for w in sorted(T.white)}
    return T, res, P, groups


# ---------------- cube / octahedron
d, xy = load('octahedron')
T, res, P, groups = run('cube', d, xy)
# draft face order t1=135, t2=234, t3=045
order = {frozenset(map(int, k)): k for k in ['135', '234', '045']}
idx = [T.A.index(next(t for t in T.A if frozenset(T.faces[t]) == frozenset(map(int, k)))) for k in ['135', '234', '045']]
def from_draft(vals):
    st = [None] * T.n
    for i, v in zip(idx, vals): st[i] = v
    return tuple(st)
r_c, s_c = from_draft((3, 4, 5)), from_draft((5, 3, 4))
T, res, P, groups = run('cube', d, xy, r_c, s_c)
yc = next(w for w in T.white if set(T.faces[w]) == {3, 4, 5})
res['cube_height_y3'] = {'s_minus_and_reversed': None}
# pairs in group of D(r,s): reverse the single cycle
q2 = (s_c, r_c)
res['cube_height_y3'] = {'h_s(y3)': T.height(s_c, yc), 'h_r(y3)': T.height(r_c, yc),
                         'orientation_D_rs': T.dcycles(r_c, s_c)[0]['orientation']}
OUT['cube'] = res
# recovery via barnette_lab (orientation-free)
inst = Instance(nx.Graph([(a, b) for f in d['faces'] for a, b in zip(f, f[1:] + f[:1])]),
                outer=None or 0)
# find lab face ids matching t0 and translate state
lab_t0 = next(i for i, f in enumerate(inst.faces) if set(f) == set(d['faces'][int(d['t0'])]))
inst = Instance(inst.T, outer=lab_t0)
def to_lab(T, st):
    m = {frozenset(T.faces[t]): v for t, v in zip(T.A, st)}
    return tuple(m[frozenset(inst.faces[t])] for t in inst.A)
rec = inst.recover(to_lab(T, s_c), prescribed=d['e0'])
OUT['cube']['recovery_lab'] = {'P': [sorted(e) for e in rec['P']], 'classes': rec['classes'],
                               'cycle_len': len(rec['cycle'])}
# translate cycle into face names y_i / t_i of the draft
names = {frozenset(map(int, '012')): 't0', frozenset(map(int, '135')): 't1', frozenset(map(int, '234')): 't2',
         frozenset(map(int, '045')): 't3', frozenset(map(int, '015')): 'y0', frozenset(map(int, '123')): 'y1',
         frozenset(map(int, '024')): 'y2', frozenset(map(int, '345')): 'y3'}
OUT['cube']['recovery_lab']['cycle_named'] = [names[frozenset(inst.faces[i])] for i in rec['cycle']]

# ---------------- running 13-vertex example
d, xy = load('running')
T0 = Tri(d, xy)
tab = {0: (6, 1), 2: (2, 3), 7: (8, 7), 9: (1, 2), 11: (3, 9), 13: (10, 11), 15: (11, 6), 17: (7, 12), 19: (12, 8), 21: (9, 10)}
assert sorted(tab) == T0.A, (sorted(tab), T0.A)
r_run = tuple(tab[t][0] for t in T0.A); s_run = tuple(tab[t][1] for t in T0.A)
T, res, P, groups = run('running', d, xy, r_run, s_run)
# white faces w1 = 239, w2 = 7 8 12
w1 = next(w for w in T.white if set(T.faces[w]) == {2, 3, 9})
w2 = next(w for w in T.white if set(T.faces[w]) == {7, 8, 12})
dc = T.dcycles(r_run, s_run)
disks = [T.disk_data(c['vertices']) for c in dc]
res['w1_inside'] = [w1 in dd['white_inside'] for dd in disks]
res['w2_inside'] = [w2 in dd['white_inside'] for dd in disks]
F = lambda s_: T.height(s_, w1) * T.height(s_, w2)
tot = 0; per_group = []
for key, g in groups.items():
    gs = sum(T.eps(*q) * F(q[1]) for q in g)
    per_group.append({'cycles': len(T.dcycles(*g[0])), 'contains_rs': (r_run, s_run) in g, 'signed_sum': gs})
    tot += gs
forest_side = sum(T.eps(*q) * F(q[1]) for q in P if nx.is_forest(T.Q(q[1])))
res['F_groups'] = per_group; res['F_total'] = tot; res['F_forest_side'] = forest_side
res['sign_(-1)^((n-m)/2)'] = (-1) ** ((T.n - res['m']) // 2)
# four-term difference with the draft's u (long) v (small) indexing
g = next(g for g in groups.values() if (r_run, s_run) in g)
vals = {}
for q in g:
    cyc = T.dcycles(*q)
    u = int(any(c['orientation'] == 'ccw' and len(c['vertices']) == 7 for c in cyc))
    v = int(any(c['orientation'] == 'ccw' and len(c['vertices']) == 3 for c in cyc))
    vals[u, v] = (T.height(q[1], w1), T.height(q[1], w2), T.eps(*q), nx.is_forest(T.Q(q[1])))
b1, b2 = vals[0, 0][0], vals[0, 0][1]
res['four_term'] = {'b1': b1, 'b2': b2,
                    'table': {f'{u}{v}': vals[u, v] for (u, v) in vals},
                    'increments_match': all(vals[u, v][0] == b1 + u and vals[u, v][1] == b2 + u + v for (u, v) in vals),
                    'value': sum((-1) ** (u + v) * (b1 + u) * (b2 + u + v) for u in (0, 1) for v in (0, 1))}
# density inequality (4), with b(U) including t0, over all U containing R
worst = None; ok = True
for k in range(len(T.X) + 1):
    for S in itertools.combinations(T.X, k):
        U = set(T.V) - set(S)
        e = T.T.subgraph(U).number_of_edges()
        b = sum(1 for t in T.black if set(T.faces[t]) <= U)
        lhs3 = sum(min(2, len(set(T.faces[t]) & set(S))) for t in T.A)
        if (lhs3 >= 2 * len(S)) != (e - b <= 2 * len(U) - 4): ok = False
res['eq3_iff_eq4_all_S_with_t0_in_b'] = ok
OUT['running'] = res
# recovery using r as forest second state, via lab
inst = Instance(T.T)
lab_t0 = next(i for i, f in enumerate(inst.faces) if set(f) == set(T.faces[T.t0]))
inst = Instance(T.T, outer=lab_t0)
rec = inst.recover(to_lab(T, r_run), prescribed=d['e0'])
OUT['running']['recovery_lab_with_r'] = {'P': sorted(sorted(e) for e in rec['P']), 'classes': rec['classes'],
                                         'cycle_len': len(rec['cycle'])}

# ---------------- eps == prod delta on the lab's generated family (orientation-free statement)
from barnette_lab.core import generated
cnt = 0; bad = 0
for g in generated(12):
    try:
        b = Instance.from_primal(g) if all(dd == 3 for _, dd in g.degree()) else Instance(g)
    except Exception:
        continue
    for o in b.black:
        bi = Instance(b.T, outer=o)
        for r_, s_ in bi.pairs():
            cnt += 1
            if bi.sign(r_, s_) != math.prod(bi.delta(a, c) for a, c in zip(r_, s_)):
                bad += 1
OUT['eps_prod_delta_family'] = {'pairs_checked': cnt, 'mismatches': bad, 'source': 'barnette_lab.core.generated(12), every black outer face'}

def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items() if not str(k).startswith('_')}
    if isinstance(o, (list, tuple, set, frozenset)): return [clean(v) for v in o]
    return o
(Path(__file__).with_name('check_examples.json')).write_text(json.dumps(clean(OUT), indent=1))
print(json.dumps(clean(OUT), indent=1)[:6000])
