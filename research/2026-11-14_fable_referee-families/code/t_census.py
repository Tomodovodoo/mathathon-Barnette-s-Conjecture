"""Census over all Eulerian triangulations (plantri -b) and all facial roots.
Checks for REFEREE-algebra and REFEREE-probabilistic. Usage: python t_census.py MAXV"""
import json, sys, time
from collections import defaultdict
import numpy as np
import numpy.polynomial.polynomial as Pn
from core import *
from t_families_lib import det_states

MAXV = int(sys.argv[1]) if len(sys.argv) > 1 else 14


def gf2_inconsistent(rows, ncols):
    """rows: ints, bits 0..ncols-1 unknowns, bit ncols the right-hand side.
    True if the linear system over GF(2) has no solution."""
    piv = {}
    mask = (1 << ncols) - 1
    for r in rows:
        while True:
            low = r & mask
            if low == 0:
                if r >> ncols & 1:
                    return True
                break
            hb = low.bit_length() - 1
            if hb in piv:
                r ^= piv[hb]
            else:
                piv[hb] = r
                break
    return False


stats = defaultdict(int)
first = {}
res_first = {}                 # modulus -> first root with M>0 and M % q == 0
polys = defaultdict(set)
gauge_bad = []
M_by_graph = {}
t0 = time.time()
for V in range(6, MAXV + 1):
    graphs = plantri_eulerian(V)
    for gi, g in enumerate(graphs):
        faces = oriented_faces(g)
        name = f'plantri_{V}_{gi}'
        Ms = []
        for fi in range(len(faces)):
            inst = Inst(g, fi, faces=faces)
            stats['roots'] += 1
            S = sum(1 for _ in inst.states())
            assert S == det_states(inst), 'states do not all have one permutation sign'
            a, kappa, inner = inst.weights()
            good = []           # (r, s, eps)
            P = 0
            m = None
            tot = 0
            poly = defaultdict(int)
            mom1 = defaultdict(int)
            mom2 = defaultdict(int)
            covs = list(inst.covers())
            for d in covs:
                c = len(inst.cover_cycles(d))
                P += 1 << c
                m = c if m is None else min(m, c)
            for d in covs:
                for r, s, eps, js in inst.orientations(d):
                    tot += eps
                    poly[inst.omega(s)] += eps
                    if inst.is_good(s):
                        good.append((r, s, eps))
                    if m >= 2:
                        hs = {y: inst.height(y, s) for y in inner}
                        for y in inner:
                            mom1[y] += eps * hs[y]
                        if m >= 3:
                            for y in inner:
                                for y2 in inner:
                                    mom2[(y, y2)] += eps * hs[y] * hs[y2]
            M = sum(1 for _ in inst.good_states())
            Ms.append(M)
            assert tot == 0 and len(good) == M and M % 2 == 0
            assert sum(e for _, _, e in good) == 0
            assert len({tuple(sorted(s.items())) for _, s, _ in good}) == M
            if P:
                stats['roots_with_pair'] += 1
                if M == 0:
                    stats['pair_but_no_good'] += 1
                if M < 2 * m:
                    stats['M_below_2m'] += 1
                if M < 2 ** m:
                    stats['M_below_2^m'] += 1
                if P % (1 << m):
                    stats['P_not_div_2^m'] += 1
                if m >= 2:
                    stats['roots_m>=2'] += 1
                    assert all(v == 0 for v in mom1.values()), 'first moments differ'
                if m >= 3:
                    stats['roots_m>=3'] += 1
                    assert all(v == 0 for v in mom2.values())
            for q in (2, 3, 4, 5, 7, 11, 13):
                if M > 0 and M % q == 0 and q not in res_first:
                    res_first[q] = (name, sorted(inst.R), M)
            # gauges: sign per incidence of s (class 1), per incidence of r and of s (class 2)
            if M:
                inc = {}

                def col(key):
                    return inc.setdefault(key, len(inc))
                rows_s = []
                for r, s, eps in good:
                    b1 = 0
                    for t, v in s.items():
                        b1 |= 1 << col(('s', t, v))
                    rows_s.append((b1, eps))
                ns = len(inc)
                rows_rs = []
                for (b1, eps), (r, s, _) in zip(rows_s, good):
                    b2 = b1
                    for t, v in r.items():
                        b2 |= 1 << col(('r', t, v))
                    rows_rs.append((b2, eps))
                nall = len(inc)

                def build(rows, ncols):
                    # column ncols = global sign, bit ncols+1 = right-hand side
                    return [b | (1 << ncols) | ((1 if e < 0 else 0) << (ncols + 1)) for b, e in rows]
                if gf2_inconsistent(build(rows_s, ns), ns + 1):
                    stats['gauge_s_inconsistent'] += 1
                    gauge_bad.append((name, sorted(inst.R), M))
                if gf2_inconsistent(build(rows_rs, nall), nall + 1):
                    stats['gauge_rs_inconsistent'] += 1
            # polynomial roots
            pz = normalise({k: v for k, v in poly.items() if v})
            if pz:
                polys[V].add(pz)
                rts = np.roots(list(reversed(pz)))
                if any(abs(z.imag) > 1e-7 for z in rts) and 'nonreal' not in first:
                    first['nonreal'] = (name, sorted(inst.R), pz)
                if any(abs(abs(z) - 1) > 1e-6 for z in rts) and 'offcircle' not in first:
                    first['offcircle'] = (name, sorted(inst.R), pz)
            if V <= 12 and P:
                lin = defaultdict(int)
                for d in covs:
                    for r, s, eps, js in inst.orientations(d):
                        pl = [eps]
                        for t, v in s.items():
                            av = a[(t, v)]
                            nw = pl + [0]
                            for i, cf in enumerate(pl):
                                nw[i + 1] += cf * av
                            pl = nw
                        for i, cf in enumerate(pl):
                            lin[i] += cf
                co = [lin[i] for i in range(max(lin) + 1)]
                while co and co[-1] == 0:
                    co.pop()
                if co:
                    rts = np.roots(list(reversed(co)))
                    if any(abs(z.imag) > 1e-7 for z in rts) and 'lin_nonreal' not in first:
                        first['lin_nonreal'] = (name, sorted(inst.R), co)
        M_by_graph[name] = sorted(set(Ms))
    print(V, len(graphs), 'graphs', dict(stats), round(time.time() - t0, 1))
    sys.stdout.flush()
print('first witnesses', first)
print('residue witnesses', res_first)
print('gauge-inconsistent roots (s-gauge):', len(gauge_bad), gauge_bad[:5])
c13 = np.rint(Pn.polymul(Pn.polymul(Pn.polymul([-1, 1], [-1, 1]), [1, 1, 1]), [1, 1, 0, 1])).astype(int)
c16 = np.rint(Pn.polymul(Pn.polymul([-1, 1], [1, 1]), [1, 1, 1])).astype(int)


def present(V, co):
    co = tuple(int(x) for x in co)
    cands = set()
    for c in (co, tuple(reversed(co))):
        cands.add(normalise(dict(enumerate(c))))
        cands.add(normalise(dict(enumerate(tuple(-x for x in c)))))
    return bool(cands & polys.get(V, set()))


print('(z-1)(z^2+3) occurs at V=12:', present(12, (-3, 3, -1, 1)))
print('(z-1)^2(z^2+z+1)(z^3+z+1) occurs at V=13:', present(13, c13))
print('(z-1)(z+1)(z^2+z+1) occurs at V=16:', present(16, c16) if MAXV >= 16 else 'not run')
json.dump(dict(stats=dict(stats), first={k: [v[0], v[1], list(v[2])] for k, v in first.items()},
               residues={str(k): list(v) for k, v in res_first.items()}, gauge_bad=gauge_bad, M_by_graph=M_by_graph),
          open(f'out_census_{MAXV}.json', 'w'), indent=1)
