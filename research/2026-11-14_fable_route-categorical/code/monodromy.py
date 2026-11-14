"""Direction 5. The permutation triple of an Eulerian triangulation.

    python monodromy.py NMAX

Black faces are the points 0..k-1. sigma_c rotates a black face about its corner of colour c.
Everything below is rebuilt from the triple alone and compared with the map:
  genus zero (cycle count k + 2), product one, the cubic graph G as the graph of three
  bijections black -> white, the states as transversals of cycles, the Hamiltonian cycles.
"""
import sys
from collections import Counter, defaultdict
from itertools import product

from common import corpus, Tri, hamiltonian_partitions
from trinity import states


def cycles(perm):
    seen, out = set(), []
    for x in perm:
        if x in seen:
            continue
        c = [x]
        seen.add(x)
        while perm[c[-1]] not in seen:
            seen.add(perm[c[-1]])
            c.append(perm[c[-1]])
        out.append(tuple(c))
    return out


def triple(tri):
    """sigma_c(t) = the next black face around the colour-c corner of t, in the stored face orientation."""
    sig = [dict(), dict(), dict()]
    pi = [dict(), dict(), dict()]      # pi_c(t) = white face across the edge of t opposite its colour-c corner
    for t in tri.black:
        a = tri.faces[t]
        for i in range(3):
            v, x, y = a[i], a[(i + 1) % 3], a[(i + 2) % 3]
            c = tri.col[v]
            pi[c][t] = tri.eface[frozenset((x, y)), 1]
            w = tri.eface[frozenset((v, x)), 1]            # white face across the side v x
            z = tri.third(w, (v, x))
            sig[c][t] = tri.eface[frozenset((v, z)), 0]     # black face across the next side at v
    return sig, pi


def ham_count_from_triple(k, pi):
    """Hamiltonian cycles of the cubic graph {t - pi_c(t)}: perfect matchings whose complement is one cycle."""
    blacks = sorted(pi[0])
    inv = [{w: t for t, w in p.items()} for p in pi]
    count = 0
    for choice in product(range(3), repeat=len(blacks)):
        m = {t: pi[c][t] for t, c in zip(blacks, choice)}
        if len(set(m.values())) != len(blacks):
            continue
        ch = dict(zip(blacks, choice))
        wch = {m[t]: ch[t] for t in blacks}
        # walk the complement 2-factor from the first black vertex
        t, c_in, steps = blacks[0], None, 0
        start = t
        while True:
            c_out = next(c for c in range(3) if c != ch[t] and c != c_in)
            w = pi[c_out][t]
            c_back = next(c for c in range(3) if c != wch[w] and c != c_out)
            t = inv[c_back][w]
            c_in = c_back
            steps += 1
            if t == start:
                break
        count += (steps == len(blacks))
    return count


def main(nmax):
    passport = defaultdict(set)
    for name, g in corpus(6, nmax):
        tri = Tri(g)
        k = tri.k
        sig, pi = triple(tri)
        cyc = [cycles(s) for s in sig]
        assert sum(map(len, cyc)) == k + 2                  # genus zero
        # cycles of sigma_c are the vertices of colour c, with length deg/2
        for c in range(3):
            lens = sorted(len(x) for x in cyc[c])
            assert lens == sorted(g.degree(v) // 2 for v in tri.V if tri.col[v] == c)
        prod_ok = any(all(sig[a][sig[b][sig[c][t]]] == t for t in tri.black)
                      for a, b, c in ((0, 1, 2), (0, 2, 1)))
        assert prod_ok
        # relation between the triple and the three matchings of G
        for c in range(3):
            a, b = (c + 1) % 3, (c + 2) % 3
            inv = {w: t for t, w in pi[b].items()}
            inv2 = {w: t for t, w in pi[a].items()}
            assert all(inv[pi[a][t]] == sig[c][t] for t in tri.black) or \
                all(inv2[pi[b][t]] == sig[c][t] for t in tri.black)
        # states as transversals: choose c(t) for t != t0 so that every cycle of sigma_c missing t0 is hit once
        t0 = tri.black[0]
        A = [t for t in tri.black if t != t0]
        cyc_of = [{t: i for i, cy in enumerate(cyc[c]) for t in cy} for c in range(3)]
        need = {(c, cyc_of[c][t]) for c in range(3) for t in A} - {(c, cyc_of[c][t0]) for c in range(3)}
        ntrans = 0

        def rec(i, used):
            nonlocal ntrans
            if i == len(A):
                ntrans += (len(used) == len(need))
                return
            for c in range(3):
                key = (c, cyc_of[c][A[i]])
                if key in need and key not in used:
                    rec(i + 1, used | {key})

        rec(0, frozenset())
        roots = set(tri.faces[t0])
        nstates = len(states(tri, A, [v for v in tri.V if v not in roots]))
        assert ntrans == nstates
        nham = len(hamiltonian_partitions(tri))
        nham2 = ham_count_from_triple(k, pi) if k <= 11 else None
        assert nham2 is None or nham2 == nham, (nham, nham2)
        pp = tuple(sorted(tuple(sorted(len(x) for x in cyc[c])) for c in range(3)))
        passport[pp].add((name, nham))
        print(name, 'k=%d' % k, 'cycle types', pp, 'states at t0=%d: %d' % (t0, nstates), 'Hamiltonian cycles', nham, flush=True)
    print('passports shared by triangulations with different numbers of Hamiltonian cycles:')
    for pp, items in passport.items():
        if len({h for _, h in items}) > 1:
            print(' ', pp, sorted(items))


if __name__ == '__main__':
    main(int(sys.argv[1]))
