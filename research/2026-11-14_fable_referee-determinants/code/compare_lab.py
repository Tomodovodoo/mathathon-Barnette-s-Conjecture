"""Compare barnette_lab's exported data with the independent implementation.

Run from the repository root, after export_lab.py:
    python -B research/2026-11-14_fable_referee-determinants/code/compare_lab.py
Imports nothing from the lab. Writes compare_lab.json.
"""
import json
import sys
from fractions import Fraction
from itertools import permutations
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from etri import Tri, UF, perm_sign, det_int
from referee import pmul, padd


# ---------------------------------------------------------------- Q(zeta_12), zeta = exp(i pi / 6)
class Z12:
    """a0 + a1 x + a2 x^2 + a3 x^3 with x^4 = x^2 - 1."""
    __slots__ = ('c',)

    def __init__(self, c):
        self.c = tuple(Fraction(x) for x in c)

    @staticmethod
    def of(x):
        return x if isinstance(x, Z12) else Z12((x, 0, 0, 0))

    def __add__(self, o):
        o = Z12.of(o)
        return Z12(tuple(a + b for a, b in zip(self.c, o.c)))

    __radd__ = __add__

    def __neg__(self):
        return Z12(tuple(-a for a in self.c))

    def __sub__(self, o):
        return self + (-Z12.of(o))

    def __mul__(self, o):
        o = Z12.of(o)
        p = [Fraction(0)] * 7
        for i, a in enumerate(self.c):
            for j, b in enumerate(o.c):
                p[i + j] += a * b
        for k in (6, 5, 4):  # x^k = x^(k-2) - x^(k-4)
            p[k - 2] += p[k]
            p[k - 4] -= p[k]
            p[k] = 0
        return Z12(p[:4])

    __rmul__ = __mul__

    def __bool__(self):
        return any(self.c)

    def __eq__(self, o):
        return self.c == Z12.of(o).c

    def __hash__(self):
        return hash(self.c)

    def rational(self):
        assert not any(self.c[1:]), self.c
        return self.c[0]

    def __repr__(self):
        return f'Z12{tuple(str(x) for x in self.c)}'


Q = Z12((0, 1, 0, 0))            # exp(i pi/6)
QINV = Z12((0, 1, 0, -1))        # x^-1 = x - x^3
I = Z12((0, 0, 0, 1))            # x^3
assert Q * QINV == 1 and I * I == -1 and Q * Q * Q == I


def zpow(z, k):
    out = Z12.of(1)
    for _ in range(k):
        out = out * z
    return out


def ypoly_det(entries, n):
    """Leibniz determinant; entries[i][j] is a sparse polynomial in y_0..y_{n-1}."""
    total = {}
    one = {(0,) * n: 1}
    for p in permutations(range(n)):
        term = one
        for i in range(n):
            if not entries[i][p[i]]:
                term = {}
                break
            term = pmul(term, entries[i][p[i]])
        if term:
            total = padd(total, term, perm_sign(list(p)))
    return total


def fmt(poly):
    def mono(e):
        return '*'.join(f'y{i}' + (f'^{k}' if k > 1 else '') for i, k in enumerate(e) if k) or '1'
    return ' + '.join(f'({c})*{mono(e)}' for e, c in sorted(poly.items())) or '0'


def main():
    rows = json.loads((HERE / 'lab_export.json').read_text())
    report = []
    for row in rows:
        name = row['name']
        res = {'name': name}
        faces = [tuple(f) for f in row['faces']]
        lab_delta = {(u, v): d for u, v, d in row['delta']}
        b = Tri(row['T_edges'], row['root'])
        if any(b.delta(u, v) != d for (u, v), d in lab_delta.items()):
            b = Tri(row['T_edges'], row['root'], mirror=True)
            res['orientation'] = 'lab delta is the mirror of my default'
        else:
            res['orientation'] = 'lab delta equals my default'
        res['delta agrees with one orientation'] = all(b.delta(u, v) == d for (u, v), d in lab_delta.items())
        key = lambda t: frozenset(b.faces[t])
        mine_states = {frozenset((key(t), v) for t, v in zip(b.A, s)) for s in b.states()}
        lab_states = {frozenset((frozenset(faces[t]), v) for t, v in zip(row['A'], s)) for s in row['states']}
        res['states'] = [len(mine_states), len(lab_states)]
        res['state sets equal'] = mine_states == lab_states
        pairs = b.pairs()
        res['pairs'] = [len(pairs), row['n_pairs']]
        res['J multisets equal'] = sorted(b.J(r, s) for r, s in pairs) == row['pairs_J']
        mine_trees = {frozenset((key(t), v) for t, v in zip(b.A, s)) for s in b.states() if b.is_tree_state(s)}
        lab_trees = {frozenset((frozenset(faces[t]), v) for t, v in zip(row['A'], s)) for s in row['tree_states']}
        res['tree matchings'] = [len(mine_trees), len(lab_trees)]
        res['tree sets equal'] = mine_trees == lab_trees
        cyc_counts = [len(b.dcycles(r, s)) for r, s in pairs]
        res['cmin'] = [min(cyc_counts) if cyc_counts else None, row['cmin']]
        # the lab's spoke weights, read as data, checked by my own circulation routine
        lab_face = {frozenset(faces[t]): t for t in row['A']}
        mine_of = {lab_face[key(t)]: t for t in b.A}
        a = {(t, v): 0 for t in b.A for v in b.faces[t]}
        for t, v, wgt in row['weights']:
            if t in mine_of:
                a[mine_of[t], v] = wgt
        circ = b.circulations(a)
        bounded = {v for y, v in circ.items() if y != 'inf'}
        res['lab weights: circulation around bounded spoke faces'] = sorted(bounded)
        res['lab weights valid'] = len(bounded) <= 1 and (not bounded or abs(next(iter(bounded))) == 1)
        res['lab weights: all cycle gaps have one sign'] = len({b.gap(c, a) > 0 for r, s in pairs for c in b.dcycles(r, s)}) <= 1
        poly = {}
        for r, s in pairs:
            om = sum(a[t, v] for t, v in zip(b.A, s))
            poly[str(om)] = poly.get(str(om), 0) + b.eps(r, s)
        poly = {k: v for k, v in poly.items() if v}
        res['Z polynomial'] = [dict(sorted(poly.items(), key=lambda kv: int(kv[0]))), row['polynomial']]
        res['Z polynomial equal'] = poly == row['polynomial']
        # recovery from the lab's chosen tree state
        if 'recover' in row:
            s_lab = dict(zip(row['A'], row['recover']['state']))
            s = tuple(s_lab[lab_face[key(t)]] for t in b.A)
            e0 = tuple(row['root'][:2])
            cert = b.recover(s, e0)
            res['P equal'] = cert['P'] == sorted(tuple(sorted(e)) for e in row['recover']['P'])
            res['classes equal'] = sorted(map(sorted, row['recover']['classes'])) == cert['classes']
            # the lab's dual cycle, checked from scratch
            cf = [frozenset(f) for f in row['recover']['cycle_faces']]
            Pset = set(cert['P'])
            okc = len(cf) == len(b.faces) and len(set(cf)) == len(cf)
            for x, y in zip(cf, cf[1:] + cf[:1]):
                common = tuple(sorted(x & y))
                okc &= len(common) == 2 and common not in Pset and common in set(b.edges)
            res['lab dual cycle is Hamiltonian and avoids P'] = okc
        # the two-matroid candidate, checked from scratch
        sp = row['two_matroid']['spokes']
        uf = UF(b.white)
        tree_ok = True
        for t, v in sp:
            y, z = b.spoke_sides(mine_of[t], v)
            tree_ok &= uf.union(y, z)
        res['two-matroid candidate'] = {'size': len(sp), 'one spoke per face': len({t for t, v in sp}) == len(sp),
                                        'white forest': tree_ok, 'spanning': len(sp) == b.n,
                                        'distinct nonroots': len({v for t, v in sp}) == len(sp), 'lab says valid': row['two_matroid']['valid'],
                                        'repeated nonroots': sorted({v for t, v in sp if sum(1 for _, x in sp if x == v) > 1})}
        if 'sample_frequencies' in row:
            freq = list(row['sample_frequencies'].values())
            m = len(lab_states)
            exp = sum(freq) / m
            res['sampling'] = {'states hit': len(freq), 'of': m, 'chi2': round(sum((f - exp) ** 2 / exp for f in freq) + (m - len(freq)) * exp, 2), 'dof': m - 1}
        if 'primal_edges' in row:
            pe = {tuple(sorted(e)) for e in row['primal_edges']}
            verts = {v for e in pe for v in e}
            good = True
            for h in row['hamiltonian_cycles']:
                c = h['cycle']
                good &= len(c) == len(verts) and set(c) == verts
                good &= all(tuple(sorted((x, y))) in pe for x, y in zip(c, c[1:] + c[:1]))
                good &= all(tuple(sorted((x, y))) != tuple(sorted(h['forbidden'])) for x, y in zip(c, c[1:] + c[:1]))
            res['lab Hamiltonian cycles valid and avoid the forbidden edge'] = [good, len(row['hamiltonian_cycles'])]
        report.append(res)
        flags = {k: v for k, v in res.items() if isinstance(v, bool)}
        print(name, 'states', res['states'], 'pairs', res['pairs'], 'trees', res['tree matchings'], 'cmin', res['cmin'],
              'OK' if all(flags.values()) else 'MISMATCH ' + str([k for k, v in flags.items() if not v]))
        if name in ('truncated_octahedron', 'cube', 'hexagonal_prism', 'cyclic_12'):
            print('   two-matroid:', res['two-matroid candidate'])
            print('   sampling:', res.get('sampling'), '| cycles:', res.get('lab Hamiltonian cycles valid and avoid the forbidden edge'))

    # ------------------------------------------------------------ the hexagonal prism determinants
    row = next(r for r in rows if r['name'] == 'hexagonal_prism')
    faces = [tuple(f) for f in row['faces']]
    A, X = row['A'], row['X']
    n = len(A)
    delta = {(u, v): d for u, v, d in row['delta']}
    a = {(t, v): wgt for t, v, wgt in row['weights']}
    z = Fraction(5, 4)
    unit = lambda j: tuple(int(i == j) for i in range(n))
    sol = [[{} for _ in X] for _ in X]
    astra = [[{} for _ in X] for _ in X]
    astra2 = [[{} for _ in X] for _ in X]
    for j, t in enumerate(A):
        cs = [v for v in faces[t] if v in X]
        for u in cs:
            for v in cs:
                if u != v:
                    w = z ** a.get((t, v), 0)
                    ph = Q if delta[u, v] == 1 else QINV
                    sol[X.index(u)][X.index(v)] = padd(sol[X.index(u)][X.index(v)], {unit(j): ph * Z12.of(w)})
                    astra[X.index(u)][X.index(v)] = padd(astra[X.index(u)][X.index(v)], {unit(j): delta[u, v] * w})
                    astra2[X.index(u)][X.index(v)] = padd(astra2[X.index(u)][X.index(v)], {unit(j): delta[u, v] * 2 ** a.get((t, v), 0)})
    dsol = {e: (zpow(I, n) * c) for e, c in ypoly_det(sol, n).items()}
    dsol = {e: c.rational() for e, c in dsol.items() if c}
    dast = ypoly_det(astra, n)
    dast2 = ypoly_det(astra2, n)
    claimed = {}  # 5*y0*y1*y4*(-4*y0*y3 - 5*y1*y2 + 9*y2*y3)/64
    for coeff, mono in ((-4, (2, 1, 0, 1, 1)), (-5, (1, 2, 1, 0, 1)), (9, (1, 1, 1, 1, 1))):
        claimed[mono] = Fraction(5 * coeff, 64)
    hexres = {
        'sol: i^n det M at z=5/4': fmt(dsol),
        'sol polynomial reproduced exactly': dsol == claimed,
        'sol squarefree coefficient': str(dsol.get((1,) * n, 0)),
        'sol all-ones value': str(sum(dsol.values())),
        'astra: det N at z=5/4': fmt(dast),
        'astra squarefree coefficient at z=5/4': str(dast.get((1,) * n, 0)),
        'astra all-ones value at z=5/4': str(sum(dast.values())),
        'astra: det N at q=2': fmt(dast2),
        'astra squarefree coefficient at q=2': str(dast2.get((1,) * n, 0)),
        'astra all-ones value at q=2': str(sum(dast2.values())),
        'squarefree coefficients agree (i^n sol == astra)': dsol.get((1,) * n, 0) == dast.get((1,) * n, 0),
        'full y-polynomials agree': dsol == dast,
    }
    print('\nhexagonal prism (lab labels and weights, my arithmetic)')
    for k, v in hexres.items():
        print('  ', k, ':', v)
    (HERE / 'compare_lab.json').write_text(json.dumps({'instances': report, 'hexagonal_prism': hexres}, indent=1, default=str))


if __name__ == '__main__':
    main()
