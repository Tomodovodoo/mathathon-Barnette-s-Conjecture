"""Numerical checks of the determinant and height identities of PROOF.md.

usage: python dets.py VMAX

For every rooted Eulerian triangulation with at most VMAX vertices:
  D1  det N_s = sigma * sum_r zeta^{sum delta(r(t), s(t))}; |det N_s| = 1 if s is a
      tree matching and 0 otherwise  (N_s = twisted incidence matrix of Q_s).
  D2  sum over pairs of i^J g(s) = coefficient of x_1...x_n in det(sum_t x_t M_t),
      M_t the 3x3 block zeta^{delta(v,w)} g_t(w), for g = q^{a(t,w)}, q = 1.3.
  D3  the same sum = 3^{-n/2} sum_S (-1)^{|S|} conj(chi_S) chi_S(g), the Fourier
      expansion over subsets S of A with the vertex 3-colouring.
  D4  for white faces w_1..w_j: sum over tree matchings of eps(s) prod h_s(w_i)
      is 0 for j < cmin and, for j = cmin, +-#{(D, bijection)} as in PROOF.md.
"""
import sys, cmath, math, itertools, random
from collections import defaultdict
import numpy as np
from tri import enumerate_classes, from_code
from rooted import Rooted
from analyze import analyze

ZETA = cmath.exp(1j * math.pi / 6)
OM = cmath.exp(2j * math.pi / 3)


def main(vmax):
    random.seed(1)
    L = enumerate_classes(vmax)
    cnt = defaultdict(int)
    for v in range(6, vmax + 1):
        for ci, code in enumerate(L[v]):
            T = from_code(code)
            col = T.vertex_colouring()
            for t0 in range(T.F):
                R = Rooted(T, t0)
                n = R.n
                st = R.states()
                if not st:
                    continue
                xi = {x: i for i, x in enumerate(R.X)}
                sigma = R.perm_sign(st[0])
                a = R.weights()[0]
                q = 1.3
                kappa = 1 if T.fcol[0] == R.bc else -1
                # ---- D1
                total = 0
                for s in st:
                    N = np.zeros((n, n), dtype=complex)
                    for i, (f, sv) in enumerate(zip(R.A, s)):
                        for x in T.faces[f]:
                            if x != sv and x in xi:
                                N[i, xi[x]] = ZETA ** R.delta(x, sv)
                    d = np.linalg.det(N)
                    ps = R.partners(s)
                    direct = sum(ZETA ** R.J3(r, s) for r in ps)
                    assert abs(d - sigma * direct) < 1e-7
                    valid, forced, cycles = R.Q_structure(s)
                    is_tree = valid and not cycles
                    assert abs(abs(d) - (1 if is_tree else 0)) < 1e-7
                    total += direct * q ** R.omega(s)
                    cnt['D1 states'] += 1
                # ---- D2 (inclusion-exclusion for the multilinear coefficient)
                if n <= 10:
                    Ms = []
                    for f in R.A:
                        M = np.zeros((n, n), dtype=complex)
                        for x in T.faces[f]:
                            for y in T.faces[f]:
                                if x != y and x in xi and y in xi:
                                    M[xi[x], xi[y]] = ZETA ** R.delta(x, y) * q ** a.get((f, y), 0)
                        Ms.append(M)
                    coeff = 0
                    for mask in range(1, 1 << n):
                        Msum = sum(Ms[i] for i in range(n) if (mask >> i) & 1)
                        coeff += (-1) ** (n - bin(mask).count('1')) * np.linalg.det(Msum)
                    assert abs(coeff - total) < 1e-6 * max(1, abs(total)), (coeff, total)
                    cnt['D2 rooted'] += 1
                # ---- D3
                if n <= 10:
                    tot3 = 0
                    cs = [[col[x] for x in s] for s in st]
                    gs = [q ** R.omega(s) for s in st]
                    for mask in range(1 << n):
                        idx = [i for i in range(n) if (mask >> i) & 1]
                        chi_r = sum(OM ** (kappa * sum(c[i] for i in idx)) for c in cs)
                        chi_s = sum(g * OM ** (-kappa * sum(c[i] for i in idx)) for c, g in zip(cs, gs))
                        tot3 += (-1) ** len(idx) * chi_r * chi_s
                    tot3 *= 3 ** (-n / 2)
                    assert abs(tot3 - total) < 1e-6 * max(1, abs(total)), (tot3, total)
                    cnt['D3 rooted'] += 1
                # ---- D4
                res, ex = analyze(R, deep=False)
                if ex is None:
                    continue
                m = res['cmin']
                aw = R.weights()[1]
                inner = list(aw)
                trees, mu, Dinfo = ex['trees'], ex['mu'], ex['Dinfo']
                mins = [cycs for cycs in Dinfo.values() if len(cycs) == m]
                encl = [[set(R.enclosed_white(c)) for c in cycs] for cycs in mins]
                sign = -1 if ((n - m) // 2) % 2 else 1
                for trial in range(6):
                    j = random.randint(0, m)
                    ws = [random.choice(inner) for _ in range(j)]
                    lhs = sum(mu[s] * math.prod(R.height(s, w) for w in ws) for s in trees)
                    if j < m:
                        assert lhs == 0
                    else:
                        rhs = 0
                        for E in encl:
                            for perm in itertools.permutations(range(m)):
                                if all(ws[i] in E[perm[i]] for i in range(m)):
                                    rhs += 1
                        assert lhs == sign * rhs, (lhs, sign, rhs)
                    cnt['D4 trials'] += 1
    for k in sorted(cnt):
        print(cnt[k], k, 'all passed')


if __name__ == '__main__':
    main(int(sys.argv[1]))
