"""Claim-by-claim numerical audit with the independent implementation in etri.py.

Run from the repository root:
    python -B research/2026-11-14_fable_referee-determinants/code/referee.py
Writes results.json next to this file. Uses plantri.exe only as a source of
edge lists (orders 6..14, every face as root; 2^n polarization up to order 12).
"""
import json
import random
import subprocess
import sys
from fractions import Fraction
from itertools import permutations, product
from math import comb, prod
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
from etri import (Tri, UF, det_int, det_frac, perm_sign, octahedron, bipyramid, tetrakis_hexahedron,
                  disdyakis_dodecahedron, glue, parse_plantri)


def gbinom(k, m):
    """Generalized binomial coefficient k(k-1)...(k-m+1)/m!, any integer k."""
    num = 1
    for i in range(m):
        num *= k - i
    f = 1
    for i in range(2, m + 1):
        f *= i
    assert num % f == 0
    return num // f


# ---------------------------------------------------------------- small polynomial arithmetic
def pmul(p, q, cap=None):
    """Multiply sparse polynomials {exponent tuple: coeff}; drop monomials with an exponent > cap."""
    out = {}
    for e1, c1 in p.items():
        for e2, c2 in q.items():
            e = tuple(a + b for a, b in zip(e1, e2))
            if cap is not None and max(e) > cap:
                continue
            c = out.get(e, 0) + c1 * c2
            if c:
                out[e] = c
            else:
                out.pop(e, None)
    return out


def padd(p, q, s=1):
    out = dict(p)
    for e, c in q.items():
        c = out.get(e, 0) + s * c
        if c:
            out[e] = c
        else:
            out.pop(e, None)
    return out


def pdet(m, nvars, cap=None):
    """Leibniz determinant of a matrix of sparse polynomials (small sizes only)."""
    n = len(m)
    total = {}
    one = {(0,) * nvars: 1}
    for p in permutations(range(n)):
        term = one
        for i in range(n):
            if not m[i][p[i]]:
                term = {}
                break
            term = pmul(term, m[i][p[i]], cap)
            if not term:
                break
        if term:
            total = padd(total, term, perm_sign(list(p)))
    return total


# ---------------------------------------------------------------- the audit of one rooted instance
def audit(name, edges, root, mirror=False, rng=None, heavy=True):
    rng = rng or random.Random(20261114)
    b = Tri(edges, root, mirror)
    n = b.n
    ss = b.states()
    row = {'name': name, 'vertices': len(b.V), 'n': n, 'root': sorted(root), 'mirror': mirror, 'states': len(ss)}
    ok = {}

    # --- (B1) states, determinant, common sign, weighted determinant
    ok['states == |det K|'] = abs(det_int(b.K())) == len(ss)
    ok['all states same permutation sign'] = len({b.state_sign(s) for s in ss}) <= 1
    w = {(t, v): rng.randint(2, 9) for t in b.A for v in b.faces[t]}
    sigma = b.state_sign(ss[0]) if ss else 1
    ok['det K(w) == sigma * sum of weighted states'] = det_int(b.K(w)) == sigma * sum(prod(w[t, v] for t, v in zip(b.A, s)) for s in ss)

    # --- pairs, J, eps
    pairs = b.pairs()
    row['pairs'] = len(pairs)
    Js = sorted(b.J(r, s) for r, s in pairs)
    row['J_multiset'] = {str(j): Js.count(j) for j in sorted(set(Js))}
    ok['J has the parity of n'] = all((j - n) % 2 == 0 for j in Js)
    ok['eps == (-1)^((n+J)/2)'] = all(b.eps(r, s) == (-1) ** ((n + b.J(r, s)) // 2) for r, s in pairs)

    # --- (A/B) disk identity on every D cycle, with the geometric orientation test
    disk_ok, odd_ok, ncyc, perm_even = True, True, 0, True
    for r, s in pairs:
        for cyc in b.dcycles(r, s):
            de = [(tl, h) for t, tl, h in cyc]
            hh, I, B, W, l = b.disk_data(de)
            ccw = b.is_ccw(de)
            dsum = sum(b.delta(u, v) for u, v in de)
            disk_ok &= (B + W == 2 * I + hh - 2) and (3 * (B - W) == 2 * l - hh) and (B == I + l)
            disk_ok &= dsum == (-3 if ccw else 3)
            odd_ok &= hh % 2 == 1
            ncyc += 1
    ok['disk identity on all D cycles'] = disk_ok
    ok['all D cycles odd'] = odd_ok
    row['d_cycles_checked'] = ncyc

    # --- Lemma 4.1 with every outgoing choice (small n only)
    if n <= 7:
        good, cnt = True, 0
        for r in ss:
            opts = [[v for v in b.faces[t] if v != r[i]] for i, t in enumerate(b.A)]
            for heads in product(*opts):
                out_of = dict(zip(r, heads))
                seen = set()
                for start in r:
                    path, v = [], start
                    while v in out_of and v not in seen:
                        seen.add(v)
                        path.append(v)
                        v = out_of[v]
                    if v in path:
                        cyc = path[path.index(v):]
                        de = [(x, out_of[x]) for x in cyc]
                        ccw = b.is_ccw(de)
                        good &= sum(b.delta(u, v2) for u, v2 in de) == (-3 if ccw else 3)
                        good &= not (set(cyc) & b.R)
                        cnt += 1
        ok['Lemma 4.1, all outgoing choices'] = good
        row['outgoing_cycles_checked'] = cnt

    # --- (B4) mates, tree states, forest support
    mates = {s: [] for s in ss}
    for r, s in pairs:
        mates[s].append(r)
    trees = [s for s in ss if b.is_tree_state(s)]
    row['tree_matchings'] = len(trees)
    ok['mate count == 2^k or 0 as predicted'] = all(len(mates[s]) == b.predicted_mates(s) for s in ss)
    ok['tree state <=> exactly one mate'] = all((len(mates[s]) == 1) == b.is_tree_state(s) for s in ss)
    ok['tree state <=> spoke duals form a white tree'] = all(b.white_tree(s) == b.is_tree_state(s) for s in ss)
    coeff = {s: sum(b.eps(r, s) for r in mates[s]) for s in ss}
    ok['coefficient of F at s is +-1 on trees, 0 elsewhere'] = all((abs(coeff[s]) == 1) if b.is_tree_state(s) else coeff[s] == 0 for s in ss)
    row['norm'] = sum(c * c for c in coeff.values())
    ok['coefficient norm == number of tree matchings'] = row['norm'] == len(trees)
    row['states_with_cyclic_Q_and_mates'] = sum(1 for s in ss if len(mates[s]) > 1)
    row['signed_tree_count'] = sum(coeff.values())

    # --- Q-cycle reversal flips eps because the cycle is odd (the real-sign form of Lemma 5.2)
    # checked implicitly by the zero coefficients above; record the lengths
    # --- (A, B2) determinant coefficient formula, raw determinant, doubling
    Fw = b.F_by_pairs(w)
    row['F_random_w'] = Fw
    if n <= 11 and heavy:
        ok['F == squarefree coefficient (polarization, Bareiss)'] = b.F_by_polarization(w) == Fw
        if n <= 8:
            ok['same with Fraction elimination'] = b.F_by_polarization(w, det=det_frac) == Fw
        one = {(t, v): 1 for t in b.A for v in b.faces[t]}
        ok['F_lambda(1) == lambda^n * states, lambda=1,2,3'] = all(b.F_by_polarization(one, lam) == lam ** n * len(ss) for lam in (1, 2, 3))
        row['raw_det_random_w'] = b.raw_det(w)
        row['raw_det_at_one'] = b.raw_det(one)
        row['F_at_one'] = b.F_by_pairs(one)

    # --- grouping by D
    groups = {}
    for r, s in pairs:
        key = frozenset(frozenset((x, y)) for x, y in zip(r, s))
        groups.setdefault(key, []).append((r, s))
    row['D_groups'] = len(groups)
    a = b.weights()
    tot, gaps_ok, group_size_ok = 0, True, True
    cyc_counts = []
    lead = {}
    for key, members in groups.items():
        r, s = members[0]
        cycs = b.dcycles(r, s)
        c = len(cycs)
        cyc_counts.append(c)
        group_size_ok &= len(members) == 2 ** c
        term = (-1) ** ((n - c) // 2)
        area = 1
        for cyc in cycs:
            de = [(tl, h) for t, tl, h in cyc]
            plus = prod(w[t, h] for t, tl, h in cyc)
            minus = prod(w[t, tl] for t, tl, h in cyc)
            if not b.is_ccw(de):
                plus, minus = minus, plus
            term *= plus - minus
            g = b.gap(cyc, a)
            gaps_ok &= g >= 1
            area *= g
        tot += term
        lead[c] = lead.get(c, 0) + area
    ok['each D group has 2^c pairs'] = group_size_ok
    ok['F == sum_D (-1)^((n-c)/2) prod_C (w^C+ - w^C-)'] = tot == Fw
    ok['L+ - L- >= 1 on every D cycle (own spoke weights)'] = gaps_ok
    m = min(cyc_counts) if cyc_counts else None
    row['cmin'] = m
    row['cycle_count_histogram'] = {str(c): cyc_counts.count(c) for c in sorted(set(cyc_counts))}

    # --- (B7) linear weights, (B4) binomial moments
    lin = [0] * (n + 1)
    qpoly = {}
    for r, s in pairs:
        e = b.eps(r, s)
        p = [1]
        for t, v in zip(b.A, s):
            q = [0] * (len(p) + 1)
            for j, c in enumerate(p):
                q[j] += c
                q[j + 1] += c * a[t, v]
            p = q
        for j, c in enumerate(p):
            lin[j] += e * c
        om = sum(a[t, v] for t, v in zip(b.A, s))
        qpoly[om] = qpoly.get(om, 0) + e
    qpoly = {k: v for k, v in sorted(qpoly.items()) if v}
    row['linear_polynomial'] = lin
    row['q_polynomial'] = {str(k): v for k, v in qpoly.items()}
    if m is not None:
        expected = (-1) ** ((n - m) // 2) * lead[m]
        ok['P(x)=F(1+xa) vanishes to order exactly cmin'] = all(c == 0 for c in lin[:m]) and lin[m] != 0
        ok['lowest coefficient == (-1)^((n-m)/2) sum prod A_C'] = lin[m] == expected
        ok['binomial moment of q-polynomial agrees'] = sum(v * gbinom(k, m) for k, v in qpoly.items()) == expected and \
            all(sum(v * gbinom(k, j) for k, v in qpoly.items()) == 0 for j in range(m))
        row['lowest_coefficient'] = lin[m]
        tree_side = sum(coeff[s] * sum(prod(a[t, v] for t, v in sub) for sub in subsets(list(zip(b.A, s)), m)) for s in trees) if comb(n, m) <= 5000 else None
        if tree_side is not None:
            ok['signed e_m over tree matchings == lowest coefficient'] = tree_side == lin[m]
    else:
        ok['no pair => F identically 0'] = all(c == 0 for c in lin) and Fw == 0

    # --- (B5) white Laplacians, (A) two-matroid relaxation
    wi = {y: i for i, y in enumerate(b.white)}

    def lap(spokes, weight=lambda t, v: 1):
        L = [[0] * len(wi) for _ in wi]
        for t, v in spokes:
            i, j = (wi[y] for y in b.spoke_sides(t, v))
            c = weight(t, v)
            L[i][i] += c
            L[j][j] += c
            L[i][j] -= c
            L[j][i] -= c
        return [r[:-1] for r in L[:-1]]

    all_spokes = [(t, v) for t in b.black for v in b.faces[t]]
    B_spokes = [(t, v) for t in b.A for v in b.corners[t]]
    row['white_tau_full'] = det_int(lap(all_spokes))
    row['white_tau_B'] = det_int(lap(B_spokes))
    if 3 ** n <= 200000:
        face_transversal, both = 0, 0
        for choice in product(*[b.corners[t] for t in b.A]):
            if b.white_tree(choice):
                face_transversal += 1
                both += len(set(choice)) == n
        row['white_trees_one_spoke_per_face'] = face_transversal
        ok['label-transversal white trees == tree matchings'] = both == len(trees)
        row['two_matroid_false_positives'] = face_transversal - both
    if n <= 5 and heavy:
        # coefficient of prod p_t prod z_v in det L_W with edge weight p_t z_v w_tv, by symbolic expansion
        nv = 2 * n
        pi = {t: i for i, t in enumerate(b.A)}
        zi = {v: n + i for i, v in enumerate(b.X)}
        L = [[{} for _ in wi] for _ in wi]
        for t, v in B_spokes:
            e = [0] * nv
            e[pi[t]] = 1
            e[zi[v]] = 1
            mono = {tuple(e): w[t, v]}
            i, j = (wi[y] for y in b.spoke_sides(t, v))
            L[i][i] = padd(L[i][i], mono)
            L[j][j] = padd(L[j][j], mono)
            L[i][j] = padd(L[i][j], mono, -1)
            L[j][i] = padd(L[j][i], mono, -1)
        d = pdet([r[:-1] for r in L[:-1]], nv, cap=1)
        got = d.get((1,) * nv, 0)
        ok['[prod p prod z] det L_W == sum of weighted tree matchings'] = got == sum(prod(w[t, v] for t, v in zip(b.A, s)) for s in trees)

    # --- (A) uniform sampling by determinant self-reduction: exact probabilities
    if len(ss) <= 400 and n <= 12:
        K = b.K()
        xi = {v: i for i, v in enumerate(b.X)}
        uniform = True
        for s in ss:
            p = Fraction(1)
            used = set()
            for i, t in enumerate(b.A):
                counts = {}
                for v in b.corners[t]:
                    if v in used:
                        continue
                    cols = [xi[x] for x in b.X if x not in used and x != v]
                    counts[v] = abs(det_int([[K[rr][c] for c in cols] for rr in range(i + 1, n)]))
                p *= Fraction(counts[s[i]], sum(counts.values()))
                used.add(s[i])
            uniform &= p == Fraction(1, len(ss))
        ok['self-reduction gives probability exactly 1/M to every state'] = uniform

    # --- recovery of the Hamiltonian cycle from every tree matching and every e0
    rec = 0
    rb = sorted(b.R)
    for s in trees:
        for e0 in ((rb[0], rb[1]), (rb[0], rb[2]), (rb[1], rb[2])):
            cert = b.recover(s, e0)
            cl = next(c for c in cert['classes'] if e0[0] in c)
            assert e0[1] in cl and not (b.R - set(e0)) & set(cl), 'prescription at t0 violated'
            rec += 1
    row['recoveries'] = rec
    ok['pair exists <=> tree matching exists'] = bool(pairs) == bool(trees)
    row['checks'] = ok
    row['all_ok'] = all(ok.values())
    return row


def subsets(items, m):
    from itertools import combinations
    return combinations(items, m)


def library():
    out = []
    octa = octahedron()
    out.append(('octahedron', octa, (0, 1, 2)))
    hb = bipyramid(6)
    out.append(('hexagonal_bipyramid', hb, (0, 1, 6)))
    out.append(('octagonal_bipyramid', bipyramid(8), (0, 1, 8)))
    out.append(('tetrakis_hexahedron', tetrakis_hexahedron(), None))
    out.append(('disdyakis_dodecahedron', disdyakis_dodecahedron(), None))
    cyc = json.loads((ROOT / 'research/2026-11-14_sol_route-constructive/data/hard_instance.json').read_text())
    out.append(('cyclic_12_sol', [tuple(e) for e in cyc['T_edges']], (0, 1, 6)))
    dbl = glue(octa, (0, 1, 2), octa, (0, 1, 2))
    out.append(('double_octahedron', dbl, 'all'))
    return out


def roots_of(edges, spec):
    t = Tri(edges, None) if False else None
    from etri import facial_triangles
    faces = facial_triangles(edges)
    if spec is None:
        return [faces[0]]
    if spec == 'all':
        return faces
    return [spec]


def main():
    rng = random.Random(20261114)
    rows = []
    for name, edges, spec in library():
        for root in roots_of(edges, spec):
            for mirror in (False, True):
                row = audit(f'{name}', edges, root, mirror, rng, heavy=len(edges) <= 40)
                rows.append(row)
                print(row['name'], row['root'], 'mirror' if mirror else 'plain', 'n', row['n'], 'states', row['states'], 'pairs', row['pairs'],
                      'trees', row['tree_matchings'], 'cmin', row['cmin'], 'ok' if row['all_ok'] else 'FAIL', flush=True)
                if not row['all_ok']:
                    print('   failed:', [k for k, v in row['checks'].items() if not v])
    plantri = ROOT / 'workings/barnette_lab/vendor/plantri.exe'
    census = []
    if plantri.exists():
        for order in range(6, 15):
            run = subprocess.run([str(plantri), '-ba', str(order)], capture_output=True, text=True, timeout=120)
            for i, line in enumerate(run.stdout.splitlines()):
                edges = parse_plantri(line)
                from etri import facial_triangles
                faces = facial_triangles(edges)
                roots = faces
                for root in roots:
                    row = audit(f'plantri_{order}_{i}', edges, root, False, rng, heavy=order <= 12)
                    rows.append(row)
                    census.append(row)
                    if not row['all_ok']:
                        print('FAIL', row['name'], row['root'], [k for k, v in row['checks'].items() if not v])
            print('plantri order', order, 'done;', sum(r['name'].startswith(f'plantri_{order}_') for r in census), 'rooted instances', flush=True)
    names = sorted({k for r in rows for k in r['checks']})
    summary = {k: [sum(1 for r in rows if k in r['checks']), sum(1 for r in rows if r['checks'].get(k) is False)] for k in names}
    print('\ncheck: [instances tested, failures]')
    for k, v in summary.items():
        print(f'  {k}: {v}')
    tot = {'rooted_instances': len(rows), 'states': sum(r['states'] for r in rows), 'pairs': sum(r['pairs'] for r in rows),
           'tree_matchings': sum(r['tree_matchings'] for r in rows), 'with_pairs': sum(1 for r in rows if r['pairs']),
           'with_cyclic_Q_states': sum(1 for r in rows if r['states_with_cyclic_Q_and_mates']),
           'cmin_histogram': {str(c): sum(1 for r in rows if r['cmin'] == c) for c in sorted({r['cmin'] for r in rows if r['cmin']})},
           'all_ok': all(r['all_ok'] for r in rows)}
    print(tot)
    (HERE / 'results.json').write_text(json.dumps({'totals': tot, 'summary': summary, 'rows': rows}, indent=1))


if __name__ == '__main__':
    main()
