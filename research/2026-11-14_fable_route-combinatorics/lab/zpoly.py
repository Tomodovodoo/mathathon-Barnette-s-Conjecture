"""The signed rank polynomial Z(q) = sum over tree matchings of eps(s) q^rank(s).

usage: python zpoly.py VMAX

Tests (per rooted triangulation with a pair, m = cmin):
  Z1  Z(q) / (q-1)^m has coefficients of one sign
  Z2  ... and Z(q) / (q-1)^m evaluated at 1 equals +- sum over minimal D of prod area
  Z3  the map Hamiltonian cycle avoiding e0 -> state is injective
Prints a few polynomials.
"""
import sys
from collections import defaultdict
from tri import enumerate_classes, from_code
from rooted import Rooted, dual_ham_cycles
from analyze import analyze, cycle_to_state


def divide_by_q_minus_1(p):
    """p: dict exponent -> coeff, with p(1) = 0.  Returns p / (q - 1)."""
    lo, hi = min(p), max(p)
    out = {}
    carry = 0
    for e in range(hi, lo, -1):
        carry += p.get(e, 0)
        if carry:
            out[e - 1] = carry
    assert carry + p.get(lo, 0) == 0
    return out


def main(vmax):
    L = enumerate_classes(vmax)
    tally = defaultdict(int)
    shown = 0
    first = {}
    for v in range(6, vmax + 1):
        for ci, code in enumerate(L[v]):
            T = from_code(code)
            hams = dual_ham_cycles(T)
            alledges = {frozenset(e) for e in T.de}
            for t0 in range(T.F):
                R = Rooted(T, t0)
                # Z3 does not need a pair
                a, b, c = T.faces[t0]
                for e0 in ((a, b), (b, c), (c, a)):
                    seen = {}
                    inj = True
                    for H in hams:
                        if frozenset(e0) in H:
                            continue
                        s = cycle_to_state(R, frozenset(alledges - H), e0)
                        assert s is not None
                        if s in seen:
                            inj = False
                        seen[s] = H
                    tally['Z3 cycle -> state injective:' + ('yes' if inj else 'no')] += 1
                    if not inj:
                        first.setdefault('Z3', (v, ci, t0, e0))
                res, ex = analyze(R, deep=False)
                if ex is None:
                    continue
                m = res['cmin']
                om, mu, trees = ex['om'], ex['mu'], ex['trees']
                base = min(om[s] for s in trees)
                Z = defaultdict(int)
                for s in trees:
                    Z[om[s] - base] += mu[s]
                Z = {e: c for e, c in Z.items() if c}
                Q = dict(Z)
                for _ in range(m):
                    Q = divide_by_q_minus_1(Q)
                signs = {1 if c > 0 else -1 for c in Q.values()}
                ok = len(signs) == 1
                tally['Z1 quotient has one sign:' + ('yes' if ok else 'no')] += 1
                if not ok:
                    first.setdefault('Z1', (v, ci, t0, sorted(Z.items()), sorted(Q.items())))
                assert abs(sum(Q.values())) == res['lead']
                tally['Z2 quotient(1) = lead: yes'] += 1
                # unsigned comparison: trees versus 2^m * |quotient|_1
                l1 = sum(abs(c) for c in Q.values())
                tally['Z4 trees == 2^m * sum|quotient coeffs|:' + ('yes' if res['trees'] == 2 ** m * l1 else 'no')] += 1
                if shown < 12 and res['trees'] > 2 ** m:
                    shown += 1
                    print(v, ci, t0, 'm=', m, 'trees=', res['trees'], 'Z=', sorted(Z.items()), 'Z/(q-1)^m=', sorted(Q.items()))
    for k in sorted(tally):
        print(f"{tally[k]:7d}  {k}")
    for k, x in first.items():
        print('first counterexample', k, x)


if __name__ == '__main__':
    main(int(sys.argv[1]))
