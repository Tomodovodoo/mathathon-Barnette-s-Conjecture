"""Shared setup for the atlas: the copied figure toolkit, the running example,
every computed object the pages draw, and the small layout helpers.

Nothing here writes outside digestions/atlas/. The toolkit in toolkit/ is a
copy of paper/figures/ (model.py, check.py, draw.py, layout.py, the style file
and the two stored examples), taken on 2026-11-14, so the atlas does not
depend on files another agent may change.
"""
import sys, json, math, itertools as it
from pathlib import Path
from collections import defaultdict, Counter
sys.dont_write_bytecode = True
O = Path(__file__).resolve().parent
ROOT = O.parents[1]
TK = O / 'toolkit'
sys.path[:0] = [str(TK), str(ROOT / 'workings' / 'barnette_lab')]
import numpy as np
import networkx as nx
import sympy as sp
import check, draw, layout
from model import Model, und, dual_of_cubic, oriented_faces
from draw import Panel, pt, ang

TW = 15.92          # text width in cm (A4, one-inch margins)
CERT = {}           # everything asserted, written to computed.json by build.py


def plain(x):
    if isinstance(x, dict): return {str(k): plain(v) for k, v in x.items()}
    if isinstance(x, (list, tuple, set, frozenset)): return [plain(v) for v in x]
    if isinstance(x, np.ndarray): return x.tolist()
    if isinstance(x, (np.integer,)): return int(x)
    if isinstance(x, (np.floating,)): return float(x)
    if isinstance(x, sp.Basic): return str(x)
    return x


# ---------------------------------------------------------------------------
# The running example and everything computed on it
run = check.running()
oc = check.octahedron()
gl = check.gluing()
m, xy, R = run['model'], run['xy'], run['R']
r, s, r2, rec = run['r'], run['s'], run['r2'], run['rec']
om, oxy, oR = oc['model'], oc['xy'], oc['R']
states = m.states()
pairs = m.pairs(states)
sid = {z: i for i, z in enumerate(states)}
n = len(m.A)


def eps(a, b, mod=m):
    return math.prod(mod.delta(u, v) for u, v in zip(a, b))


def is_tree_matching(mod, z):
    """Q_z plus the three root edges is a spanning tree of T."""
    Q = mod.Q_graph(z)
    return nx.is_forest(Q) and all(len(set(c) & set(mod.roots)) == 1 for c in nx.connected_components(Q))


mates = defaultdict(list)
for a_, b_ in pairs:
    mates[b_].append(a_)
tree_states = [z for z in states if m.Q_is_forest(z) and mates[z]]
assert all(is_tree_matching(m, z) for z in tree_states)
assert all(len(mates[z]) == 1 for z in tree_states)          # a good state has a unique mate
cyclic_pairs = [(a_, b_) for a_, b_ in pairs if not m.Q_is_forest(b_)]
assert (len(states), len(pairs), len(cyclic_pairs), len(tree_states)) == (12, 8, 2, 6)

# independent enumeration with the lab implementation
from barnette_lab.core import Instance
_b = Instance(m.T)
_b = Instance(m.T, next(i for i, f in enumerate(_b.faces) if set(f) == set(m.roots)))
_fid = {frozenset(f): i for i, f in enumerate(m.F)}


def _lab(z):
    ch = dict(zip(m.A, z))
    return tuple(ch[_fid[frozenset(_b.faces[t])]] for t in _b.A)


assert set(map(_lab, states)) == set(_b.states())
assert {(_lab(a_), _lab(b_)) for a_, b_ in pairs} == set(_b.pairs(list(_b.states())))
_lc = _b.recover(_lab(r), prescribed=m.e0)
assert set(map(tuple, rec['P'])) == set(map(tuple, _lc['P']))

# heights: integer potentials on the bounded faces of the spoke graph H0
spokes = [(t, v) for t in m.A for v in m.F[t]]
sindex = {e: i for i, e in enumerate(spokes)}
inner = [w for w in m.white if all(m.black_face(u, v) != m.t0 for u, v in zip(m.F[w], m.F[w][1:] + m.F[w][:1]))]
Cmat = sp.zeros(len(spokes), len(inner))
for j, w in enumerate(inner):
    f = m.F[w]
    for u, v in zip(f, f[1:] + f[:1]):
        t = m.black_face(u, v)
        Cmat[sindex[t, v], j] += 1
        Cmat[sindex[t, u], j] -= 1


def svec(z):
    return sp.Matrix([int(z[m.A.index(t)] == v) for t, v in spokes])


def heights(v):
    h = list(Cmat.gauss_jordan_solve(v)[0])
    assert all(z.q == 1 for z in h)
    return tuple(map(int, h))


_hs = [heights(svec(z) - svec(states[0])) for z in states]
_min = tuple(min(h[j] for h in _hs) for j in range(len(inner)))
hs = [tuple(v - a for v, a in zip(h, _min)) for h in _hs]
vol = [sum(h) for h in hs]


def covers(hh):
    order = nx.DiGraph()
    order.add_nodes_from(range(len(hh)))
    for i, a in enumerate(hh):
        for j, z in enumerate(hh):
            if i != j and all(u <= v for u, v in zip(a, z)):
                order.add_edge(i, j)
    return nx.transitive_reduction(order)


state_order = covers(hs)
# every cover is one clock move: the two states differ by height one on one face
for i, j in state_order.edges():
    d = [b - a for a, b in zip(hs[i], hs[j])]
    assert sorted(d) == [0] * (len(inner) - 1) + [1]

# exact unit-circulation spoke weights and the exponents omega(s)
_a = run['spoke_weights']
aa = {e: sp.Rational(float(w)).limit_denominator(100000) for e, w in _a.items()}
assert all(sum(Cmat[i, j] * aa[e] for i, e in enumerate(spokes)) == 1 for j in range(len(inner)))
omega = [sum(aa[t, v] for t, v in zip(m.A, z)) for z in states]
# the exponent of a state is its volume, up to one additive constant
assert len({omega[i] - vol[i] for i in range(len(states))}) == 1

groups = {}
for a_, b_ in pairs:
    groups.setdefault(frozenset(und(u, v) for u, v in zip(a_, b_)), []).append((a_, b_))
groups = sorted(groups.values(), key=lambda g: -max(len(c) for c in m.directed_cycles(m.D(*g[0]))))
xs = sp.Symbol('x')
term = {(a_, b_): dict(r=sid[a_], s=sid[b_], J=m.J(a_, b_), sign=int((1j ** m.J(a_, b_)).real), eps=eps(a_, b_), vol=vol[sid[b_]])
        for a_, b_ in pairs}
assert all(d['eps'] == int((1j ** (n + d['J'])).real) for d in term.values())
Zred = sum(d['sign'] * sp.exp(xs * d['vol']) for d in term.values())
# fixed second state: cyclic states cancel
for z in states:
    tot = sum(term[a_, z]['sign'] for a_ in mates[z])
    assert tot == (0 if not m.Q_is_forest(z) else (term[mates[z][0], z]['sign'] if mates[z] else 0))
# grouped by D: a product over the cycles
group_data = []
for g in groups:
    cyc = [m.disk(c) for c in m.directed_cycles(m.D(*g[0]))]
    Ws = [k['W'] for k in cyc]
    base = min(term[p]['vol'] for p in g)
    lead = [p for p in g if term[p]['vol'] == base][0]
    prod = term[lead]['sign'] * sp.exp(xs * base) * math.prod((1 - sp.exp(xs * w)) for w in Ws)
    assert sp.simplify(sp.expand(prod) - sum(term[p]['sign'] * sp.exp(xs * term[p]['vol']) for p in g)) == 0
    group_data.append(dict(pairs=g, cycles=cyc, W=Ws, base=base, sign=term[lead]['sign'] * (-1) ** len(Ws)))
assert sp.simplify(Zred - sum(term[p]['sign'] * sp.exp(xs * term[p]['vol']) for g in groups for p in g)) == 0
lead_coeff = sum(d['sign'] * math.prod(d['W']) for d in group_data)
assert sp.series(Zred, xs, 0, 3).removeO().coeff(xs, 2) == lead_coeff and sp.series(Zred, xs, 0, 2).removeO() == 0

# the integer polynomial with linear weights w = 1 + x a
Fpoly = sp.expand(sum(eps(u, v) * sp.prod([1 + xs * aa[t, z] for t, z in zip(m.A, v)]) for u, v in pairs))
Fp = sp.Poly(Fpoly, xs)
assert Fp.nth(0) == 0 and Fp.nth(1) == 0 and abs(Fp.nth(2)) == abs(lead_coeff)
assert sum(eps(u, v) for u, v in pairs) == 0                 # F(1) = 0: the signs of the good states balance

CERT['running'] = dict(counts=run['counts'], tree_matchings=len(tree_states), lab_agrees=True,
                       states=states, inner_white=inner, heights=hs, volume=vol,
                       state_covers=list(state_order.edges()),
                       terms=[dict(d) for d in term.values()],
                       groups=[dict(W=d['W'], base=d['base'], sign=d['sign'], pairs=[[sid[a_], sid[b_]] for a_, b_ in d['pairs']]) for d in group_data],
                       leading_coefficient=lead_coeff, F_series=str(sp.series(Fpoly, xs, 0, 4)),
                       r=sid[r], s=sid[s], r2=sid[r2])


# ---------------------------------------------------------------------------
# Layouts for the other triangulations (cached so pictures do not drift)
LAYFILE = O / 'layouts.json'
_lay = json.loads(LAYFILE.read_text()) if LAYFILE.exists() else {}


def rooted(faces, roots, e0=None):
    """A Model whose stored orientation agrees with the disk drawing."""
    for fs in (faces, [tuple(reversed(f)) for f in faces]):
        t0 = next(i for i, f in enumerate(fs) if set(f) == set(roots))
        mod = Model(fs, t0, e0)
        third = next(v for v in mod.roots if v not in mod.e0)
        a, b = mod.e0
        if mod.left[a, b] == mod.t0:
            a, b = b, a
        fixed = {v: layout.R * np.array([math.cos(math.radians(t)), math.sin(math.radians(t))])
                 for v, t in zip((a, b, third), layout.ROOT_ANGLES)}
        q = layout.tutte(mod, fixed)
        if all(layout.cross(q[f[1]] - q[f[0]], q[f[2]] - q[f[0]]) > 0 for i, f in enumerate(mod.F) if i != mod.t0):
            mod._tutte = q
            return mod
    raise AssertionError('no orientation gives a disk drawing')


def auto_layout(name, mod, rounds=150):
    if name in _lay:
        q = {int(k): np.array(v, float) for k, v in _lay[name].items()}
    else:
        q, _ = layout.relax(mod, mod._tutte, rounds=rounds)
        _lay[name] = {str(k): [round(float(v[0]), 3), round(float(v[1]), 3)] for k, v in q.items()}
        LAYFILE.write_text(json.dumps(_lay, indent=0))
        q = {int(k): np.array(v, float) for k, v in _lay[name].items()}
    check.check_layout(mod, q, layout.R)
    return q, layout.R


def aligned_layout(name, mod, start, frac=0.55):
    """Coordinates for `mod` that stay as close as possible (least squares) to the positions `start`
    of another drawing, with the roots fixed and every bounded face keeping at least `frac` of the
    smallest face area of a relaxed drawing. Cached like the other layouts."""
    if name not in _lay:
        from scipy.optimize import minimize
        free = list(mod.X)
        fixed = {v: np.array(start[v], float) for v in mod.roots}
        base = np.concatenate([start[v] for v in free])
        faces = [f for i, f in enumerate(mod.F) if i != mod.t0 and sum(v in mod.roots for v in f) < 2]   # a face on an outer arc is bounded by the arc
        unpack = lambda z: {**fixed, **{v: z[2 * i:2 * i + 2] for i, v in enumerate(free)}}

        def areas(z):
            q = unpack(z)
            return np.array([layout.cross(q[f[1]] - q[f[0]], q[f[2]] - q[f[0]]) / 2 for f in faces])
        q0, _ = layout.relax(mod, layout.tutte(mod, fixed), rounds=120)
        z0 = np.concatenate([q0[v] for v in free])
        sgn = 1 if areas(z0)[0] > 0 else -1
        assert min(sgn * areas(z0)) > 0
        amin = frac * min(sgn * areas(z0))
        sol = minimize(lambda z: float(np.sum((z - base) ** 2)), z0, jac=lambda z: 2 * (z - base),
                       constraints=[{'type': 'ineq', 'fun': lambda z: sgn * areas(z) - amin},
                                    {'type': 'ineq', 'fun': lambda z: (0.93 * layout.R) ** 2 - z[0::2] ** 2 - z[1::2] ** 2}], method='SLSQP', options={'maxiter': 800, 'ftol': 1e-10})
        assert sol.success and min(sgn * areas(sol.x)) > 0.98 * amin
        q = unpack(sol.x)
        _lay[name] = {str(k): [round(float(v[0]), 3), round(float(v[1]), 3)] for k, v in q.items()}
        LAYFILE.write_text(json.dumps(_lay, indent=0))
    q = {int(k): np.array(v, float) for k, v in _lay[name].items()}
    check.check_layout(mod, q, layout.R)
    return q, layout.R


# ---------------------------------------------------------------------------
# Drawing helpers
def P(unit=0.62, mod=None, pos=None, rad=None, **kw):
    if mod is None:
        return Panel(m, xy, R, unit=unit, **kw)
    return Panel(mod, pos, rad, unit=unit, **kw)


def small(tex):
    """Lighter marks for thumbnails under about 4.5 cm."""
    head, rest = tex.split('\n', 1)
    head = head.replace('[bf,', '[bf,bf small,')
    rest = (rest.replace('circle[radius=1.4pt]', 'circle[radius=.8pt]').replace('circle[radius=2.3pt]', 'circle[radius=1.4pt]')
            .replace('circle[radius=2.6pt]', 'circle[radius=1.7pt]').replace('+(-2.3pt,-2.3pt) $) rectangle ($', '+(-1.5pt,-1.5pt) $) rectangle ($')
            .replace('+(2.3pt,2.3pt) $)', '+(1.5pt,1.5pt) $)'))
    return head + '\n' + rest


def cell(tex, label=None, width=None):
    if label is None:
        return tex
    w = rf'\begin{{minipage}}[t]{{{width}cm}}\centering\footnotesize ' if width else r'{\footnotesize '
    e = r'\end{minipage}' if width else '}'
    return r'\begin{tabular}[t]{@{}c@{}}' + tex + r'\\[.6mm]' + w + label + e + r'\end{tabular}'


def vs(length):
    r'''Row break plus a real vertical skip. Inside a tabular, \\[len] only deepens the strut, so it adds
    nothing under a row that is already deeper than len (a nested tabular with a caption).'''
    return r'\\\noalign{\vskip ' + length + '}'


def grid(cells, ncols, colsep='3mm', rowsep='3mm'):
    rows = [cells[i:i + ncols] for i in range(0, len(cells), ncols)]
    cols = '@{}' + ('c@{\\hspace{' + colsep + '}}') * (ncols - 1) + 'c@{}'
    body = (vs(rowsep) + '\n').join(' &\n'.join(row) for row in rows)
    return rf'\begin{{tabular}}{{{cols}}}' + '\n' + body + '\n' + r'\end{tabular}'


def tikz(lines, unit=1, extra=''):
    return rf'\begin{{tikzpicture}}[bf,x={unit}cm,y={unit}cm{extra}]' + '\n' + '\n'.join(lines) + '\n' + r'\end{tikzpicture}'


def shade_faces(p, faces, style='af tint'):
    for f in faces:
        p.add(rf'\fill[{style}] {p.face_path(f)};')
    return p


def ring(p, v, rad='4.2pt', style='line width=.9pt'):
    p.add(rf'\draw[{style}] {pt(p.xy[v])} circle[radius={rad}];')
    return p


def facelabel(p, f, text, opts='af lab'):
    p.add(rf'\node[{opts}] at {pt(p.cen[f])} {{{text}}};')
    return p


def signtex(v):
    return '+' if v > 0 else '-'


WT_HEAVY = r'\tikzset{bf wtree/.append style={line width=1.5pt}}'      # greyscale: the green dash-dot curves need weight


def root_path(mod, z):
    """A path of opposite edges of z that joins two roots, or None."""
    Q = mod.Q_graph(z)
    for a_, b_ in it.combinations(mod.roots, 2):
        if nx.has_path(Q, a_, b_):
            pth = nx.shortest_path(Q, a_, b_)
            return list(zip(pth, pth[1:]))
    return None


FIGS = {}


def fig(slug):
    def deco(fn):
        FIGS[slug] = fn
        return fn
    return deco


# display names: states numbered by volume, s_0 the lowest
_order = sorted(range(len(states)), key=lambda i: (vol[i], i))
nm = {states[i]: k for k, i in enumerate(_order)}
by_name = {k: z for z, k in nm.items()}
CERT['running']['display_names'] = {str(sid[z]): k for z, k in nm.items()}
NUM = {}            # slug -> page number, filled by build.py before figures are drawn


def pg(slug):
    return str(NUM.get(slug, '?'))


def expo(sign, v):
    """TeX for a term  sign * e^{v x}."""
    e = '1' if v == 0 else ('e^{x}' if v == 1 else rf'e^{{{v}x}}')
    return ('+' if sign > 0 else '-') + e
