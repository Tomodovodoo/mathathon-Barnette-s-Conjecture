"""Direction 3. Homological tests.

    python homology.py hall NMAX      topological Hall condition for the complex of partial tree matchings
    python homology.py bicomplex NMAX do the two cube differentials on pairs anticommute up to sign?

hall: vertices of the complex are incidences (t, v), t in A, v a nonroot corner of t.
A set of incidences is a simplex when its faces are distinct, its vertices are distinct and
the opposite edges form a forest in T with the three roots identified. A simplex with one
incidence in every face of A is a tree matching. The topological Hall theorem
(Aharoni-Haxell, Meshulam) gives such a simplex if, for every set S of faces, the subcomplex
on the incidences of S has vanishing reduced homology below dimension |S| - 1.
Homology is computed over GF(2).
"""
import sys
from collections import Counter, defaultdict
from itertools import combinations

from common import corpus, Tri, UF
from trinity import states


def rank_gf2(rows):
    """Rank of a list of integers read as GF(2) row vectors."""
    piv = {}
    r = 0
    for x in rows:
        while x:
            h = x.bit_length() - 1
            if h in piv:
                x ^= piv[h]
            else:
                piv[h] = x
                r += 1
                break
    return r


def simplices(tri, t0, mode):
    roots = set(tri.faces[t0])
    A = [t for t in tri.black if t != t0]
    rep = {v: ('R' if v in roots else v) for v in tri.V}
    out = [[] for _ in range(len(A) + 1)]

    def rec(i, cur, usedv):
        if cur:
            out[len(cur)].append(tuple(cur))
        for j in range(i, len(A)):
            t = A[j]
            for v in tri.faces[t]:
                if v in roots or v in usedv:
                    continue
                cur.append((t, v))
                if mode == 'matching' or forest(tri, cur, rep):
                    rec(j + 1, cur, usedv | {v})
                cur.pop()

    rec(0, [], frozenset())
    return A, out


def forest(tri, cur, rep):
    uf = UF(set(rep.values()))
    for t, v in cur:
        a, b = tri.opposite_edge(t, v)
        if not uf.union(rep[a], rep[b]):
            return False
    return True


def betti(simp_by_size, faces_allowed):
    """Reduced GF(2) Betti numbers of the subcomplex on the given faces."""
    levels = []
    for size, ss in enumerate(simp_by_size):
        if size == 0:
            continue
        levels.append([s for s in ss if all(t in faces_allowed for t, v in s)])
    while levels and not levels[-1]:
        levels.pop()
    if not levels:
        return None          # empty complex
    idx = [{s: i for i, s in enumerate(lv)} for lv in levels]
    ranks = [1]              # augmentation map C_0 -> Z has rank 1
    for d in range(1, len(levels)):
        rows = []
        for s in levels[d]:
            x = 0
            for j in range(len(s)):
                x |= 1 << idx[d - 1][s[:j] + s[j + 1:]]
            rows.append(x)
        ranks.append(rank_gf2(rows))
    ranks.append(0)
    return [len(levels[d]) - ranks[d] - ranks[d + 1] for d in range(len(levels))]


def run_hall(nmax, mode='tree'):
    summary = Counter()
    for name, g in corpus(6, nmax):
        tri = Tri(g)
        for t0 in tri.black:
            A, simp = simplices(tri, t0, mode)
            n = len(A)
            ntree = len(simp[n])
            ok = True
            worst = None
            for r in range(1, n + 1):
                for S in combinations(A, r):
                    b = betti(simp, set(S))
                    if b is None:
                        ok = False
                        worst = worst or (S, 'empty')
                        continue
                    low = [(d, x) for d, x in enumerate(b) if x and d < r - 1]
                    if low:
                        ok = False
                        worst = worst or (S, b)
            full = betti(simp, set(A))
            summary[(ntree > 0, ok)] += 1
            print(name, 't0=%d' % t0, 'n=%d' % n, 'top simplices=%d' % ntree, 'Betti of the whole complex', full,
                  'Hall condition holds' if ok else 'Hall condition FAILS at %s' % (worst,), flush=True)
    print('summary (has top simplex, Hall condition holds):', dict(summary))


def run_bicomplex(nmax):
    """Do the Q-cycle reversal and the D-cycle reversal commute as moves on pairs?"""
    from common import Instance
    tot = Counter()
    for name, g in corpus(6, nmax):
        for outer in range(2 * (len(g) - 2)):
            b = Instance(g, outer)
            ps = b.pairs()
            if not ps:
                continue
            for p in ps:
                dq = [b.reverse_q(p, c) for c in b.qcycles(p[1])]
                dd = [b.reverse_d(p, c) for c in b.dcycles(*p)]
                a = Counter(b.reverse_d(q, c) for q in dq for c in b.dcycles(*q))
                c2 = Counter(b.reverse_q(q, c) for q in dd for c in b.qcycles(q[1]))
                tot['pairs'] += 1
                tot['pairs where the two-step targets differ'] += (set(a) != set(c2))
    print(dict(tot))


if __name__ == '__main__':
    if sys.argv[1] == 'hall':
        run_hall(int(sys.argv[2]), sys.argv[3] if len(sys.argv) > 3 else 'tree')
    else:
        run_bicomplex(int(sys.argv[2]))
