"""Direction 1. Cutting an Eulerian triangulation along a cycle.

    python cuts.py glue NMAX [MMAX]   check the gluing formula on every cycle of length 3..MMAX
    python cuts.py three NMAX         boundary patterns of separating triangles (Theorem 2.2 as a functor)
    python cuts.py four NMAX          boundary patterns of 4-cycle cuts

A disk state is (word, partition): the labels of the boundary vertices (label of
position 0 is 0) and the partition of the boundary positions into the components
of the two label classes inside the disk.
"""
import sys
import json
from collections import Counter, defaultdict
from itertools import combinations

from common import corpus, Tri, UF, labellings_no_mono, HERE


def cycles_of_length(g, m):
    out = []
    nodes = sorted(g)

    def rec(path, start):
        if len(path) == m:
            if g.has_edge(path[-1], start) and path[1] < path[-1]:
                out.append(tuple(path))
            return
        for w in g[path[-1]]:
            if w > start and w not in path:
                path.append(w)
                rec(path, start)
                path.pop()

    for s in nodes:
        rec([s], s)
    return out


def sides(tri, cyc):
    """The two face sets cut out by the cycle."""
    cut = {frozenset((a, b)) for a, b in zip(cyc, cyc[1:] + cyc[:1])}
    comp = {}
    for start in range(tri.nf):
        if start in comp:
            continue
        comp[start] = start
        stack = [start]
        while stack:
            f = stack.pop()
            a = tri.faces[f]
            for u, v in zip(a, a[1:] + a[:1]):
                if frozenset((u, v)) in cut:
                    continue
                h = tri.sides[v, u]
                if h not in comp:
                    comp[h] = start
                    stack.append(h)
    reps = sorted(set(comp.values()))
    assert len(reps) == 2, reps
    return [[f for f in range(tri.nf) if comp[f] == r] for r in reps]


class Disk:
    def __init__(self, tri, cyc, fs):
        self.tri, self.cyc, self.fs = tri, cyc, fs
        vs = set()
        es = set()
        for f in fs:
            a = tri.faces[f]
            vs.update(a)
            for u, v in zip(a, a[1:] + a[:1]):
                es.add(frozenset((u, v)))
        self.verts = list(cyc) + sorted(vs - set(cyc))
        self.edges = [tuple(e) for e in es]
        self.interior = len(vs) - len(cyc)
        m = len(cyc)
        cyc_edges = {frozenset((a, b)) for a, b in zip(cyc, cyc[1:] + cyc[:1])}
        self.chords = sorted(tuple(sorted((cyc.index(u), cyc.index(v)))) for u, v in self.edges
                             if u in cyc and v in cyc and frozenset((u, v)) not in cyc_edges)
        fset = set(fs)
        word = []
        for a, b in zip(cyc, cyc[1:] + cyc[:1]):
            f = next(h for h in (tri.sides[a, b], tri.sides[b, a]) if h in fset)
            word.append('+' if tri.fcol[f] == 0 else '-')
        self.signs = ''.join(word)
        self._table = None

    def table(self):
        """(word, partition) -> Counter{number of interior components}."""
        if self._table is not None:
            return self._table
        tri, cyc = self.tri, self.cyc
        tab = defaultdict(Counter)
        cycset = set(cyc)
        for lab, c0, c1, rank in labellings_no_mono(tri, self.verts, self.fs, self.edges):
            uf = UF(self.verts)
            for u, v in self.edges:
                if lab[u] == lab[v]:
                    uf.union(u, v)
            blocks = defaultdict(list)
            for i, v in enumerate(cyc):
                blocks[uf.find(v)].append(i)
            part = frozenset(frozenset(b) for b in blocks.values())
            inner = (c0 + c1) - len(blocks)
            word = tuple(lab[v] for v in cyc)
            tab[word, part][inner] += 1
        self._table = dict(tab)
        return self._table

    def ham_states(self):
        return {key for key, cnt in self.table().items() if cnt[0] > 0}


def join_blocks(m, p1, p2):
    uf = UF(range(m))
    for b in list(p1) + list(p2):
        b = sorted(b)
        for x in b[1:]:
            uf.union(b[0], x)
    return len({uf.find(i) for i in range(m)})


def glue_poly(d1, d2):
    """Loop polynomial of the glued sphere: Counter{number of cycles of the 2-factor: count}."""
    m = len(d1.cyc)
    out = Counter()
    by_word = defaultdict(list)
    for (word, part), cnt in d2.table().items():
        by_word[word].append((part, cnt))
    for (word, part), cnt in d1.table().items():
        for part2, cnt2 in by_word.get(word, ()):
            j = join_blocks(m, part, part2)
            for i1, n1 in cnt.items():
                for i2, n2 in cnt2.items():
                    out[i1 + i2 + j - 1] += n1 * n2
    return out


def direct_poly(tri):
    out = Counter()
    for lab, c0, c1, rank in labellings_no_mono(tri, tri.V, range(tri.nf), list(tri.g.edges())):
        out[c0 + c1 - 1] += 1
    return out


def run_glue(nmax, mmax):
    total = Counter()
    states_seen = defaultdict(set)
    for name, g in corpus(6, nmax):
        tri = Tri(g)
        direct = direct_poly(tri)
        for m in range(3, mmax + 1):
            for cyc in cycles_of_length(g, m):
                a, b = sides(tri, cyc)
                d1, d2 = Disk(tri, cyc, a), Disk(tri, cyc, b)
                glued = glue_poly(d1, d2)
                assert glued == direct, (name, cyc, glued, direct)
                total[m] += 1
                for d in (d1, d2):
                    for (word, part) in d.ham_states():
                        states_seen[m].add((word, part))
        print(name, 'V=%d' % len(g), 'loop polynomial', dict(sorted(direct.items())), flush=True)
    print('cycles checked by length:', dict(total))
    from math import comb
    cat = [1, 1, 2, 5, 14]
    for m in sorted(states_seen):
        formula = sum(comb(m, 2 * j) * cat[j] for j in range(1, m // 2 + 1))
        # position 0 has label 0; a word and its complement are one pattern
        print('m=%d: distinct Hamiltonian boundary states seen %d, formula sum_j C(m,2j) Cat(j) = %d'
              % (m, len(states_seen[m]), formula))


def name4(word, part):
    w = ''.join(map(str, word))
    ones = [i for i in range(4) if word[i] != word[(i + 1) % 4] or True]
    lone = [i for i in range(4) if sum(1 for j in range(4) if word[j] == word[i]) == 1]
    if len(lone) == 1:
        return 'A%d' % lone[0]
    if w in ('0011', '0110'):
        return 'P01' if w == '0011' else 'P12'
    if w == '0101':
        if frozenset((0, 2)) in part:
            return 'X02'
        if frozenset((1, 3)) in part:
            return 'X13'
        return 'X??'
    return 'M' + w


def glue4(f1, f2):
    common = (f1 & f2) - {'X02', 'X13'}
    if common:
        return True
    return ('X02' in f1 and 'X13' in f2) or ('X13' in f1 and 'X02' in f2)


def run_three(nmax):
    """Every side of every separating triangle realises all three patterns."""
    n = 0
    hist = Counter()
    for name, g in corpus(6, nmax):
        tri = Tri(g)
        for cyc in cycles_of_length(g, 3):
            a, b = sides(tri, cyc)
            for fs in (a, b):
                d = Disk(tri, cyc, fs)
                if d.interior == 0:
                    continue
                words = sorted(''.join(map(str, w)) for w, p in d.ham_states())
                hist[tuple(words)] += 1
                n += 1
    print('sides of separating triangles with an interior vertex:', n)
    for k, v in hist.items():
        print('  realised label words', k, ':', v)


def run_four(nmax, out):
    fam = defaultdict(Counter)          # (signs, chords) -> Counter of frozenset of state names
    examples = {}
    pairs_ok = 0
    records = []
    for name, g in corpus(6, nmax):
        tri = Tri(g)
        nsep3 = len(tri.separating_triangles())
        for cyc in cycles_of_length(g, 4):
            a, b = sides(tri, cyc)
            d1, d2 = Disk(tri, cyc, a), Disk(tri, cyc, b)
            if d1.interior == 0 or d2.interior == 0:
                continue
            rev = (cyc[0],) + tuple(reversed(cyc[1:]))
            for base in (cyc, rev):
              for rot in range(4):
                c = base[rot:] + base[:rot]
                e1, e2 = Disk(tri, c, a), Disk(tri, c, b)
                # canonical rotations only: ++-- or +-+- on the first side
                for x, y in ((e1, e2), (e2, e1)):
                    if x.signs not in ('++--', '+-+-'):
                        continue
                    fx = frozenset(name4(*s) for s in x.ham_states())
                    fy = frozenset(name4(*s) for s in y.ham_states())
                    assert glue4(fx, fy), (name, c, fx, fy)
                    pairs_ok += 1
                    key = (x.signs, tuple(x.chords))
                    fam[key][fx] += 1
                    examples.setdefault((key, fx), (name, c, x.interior, nsep3))
                    records.append((x.signs, tuple(x.chords), tuple(sorted(fx)), y.signs, tuple(y.chords),
                                    tuple(sorted(fy)), nsep3, x.interior, y.interior))
        print(name, 'done', flush=True)
    print('rotated cut sides examined:', pairs_ok, '(every actual cut glues, as it must)')
    result = {}
    for key in sorted(fam):
        signs, chords = key
        print('\nsigns %s chords %s: %d distinct pattern sets' % (signs, list(chords), len(fam[key])))
        sets = list(fam[key])
        inter = frozenset.intersection(*sets)
        union = frozenset.union(*sets)
        print('  always achievable (intersection):', sorted(inter))
        print('  ever achievable (union):', sorted(union))
        minimal = [s for s in sets if not any(t < s for t in sets)]
        for s in sorted(minimal, key=lambda s: (len(s), sorted(s))):
            print('  minimal set', sorted(s), 'x%d' % fam[key][s], 'e.g.', examples[key, s])
        result['%s|%s' % (signs, list(chords))] = {
            'sets': {','.join(sorted(s)): c for s, c in fam[key].items()},
            'always': sorted(inter), 'ever': sorted(union)}
    # abstract gluing: any side with signs sigma against any side with the opposite signs
    print('\nabstract gluing test (sides from different triangulations):')
    flip = {'+': '-', '-': '+'}
    for signs in ('++--', '+-+-'):
        opp = ''.join(flip[c] for c in signs)
        left = [(k, s) for k in fam if k[0] == signs for s in fam[k]]
        # a side with the opposite signs is a canonical side read after a rotation
        bad = Counter()
        tot = 0
        for (k1, s1) in left:
            for (k2, s2) in left:
                # rotate s2 by two positions for ++--, by one for +-+-, to get signs opp
                shift = 2 if signs == '++--' else 1
                t2 = frozenset(rotate_name(x, shift) for x in s2)
                c2 = tuple(sorted(tuple(sorted(((i + shift) % 4, (j + shift) % 4))) for i, j in k2[1]))
                simple = not (set(k1[1]) & set(c2))
                tot += 1
                if not glue4(s1, t2):
                    bad[simple] += 1
                    if simple:
                        print('  NON-GLUABLE SIMPLE PAIR', signs, k1, sorted(s1), k2, sorted(s2))
        print('  signs %s: %d abstract pairs, non-gluable with a doubled chord %d, non-gluable simple %d'
              % (signs, tot, bad[False], bad[True]))
    with open(out, 'w') as fh:
        json.dump({'family': result, 'records': records}, fh)
    print('wrote', out)


def rotate_name(x, shift):
    """Name of the state after relabelling position i as i + shift."""
    if x[0] == 'A':
        return 'A%d' % ((int(x[1]) + shift) % 4)
    if x[0] == 'P':
        return x if shift % 2 == 0 else {'P01': 'P12', 'P12': 'P01'}[x]
    if x[0] == 'X':
        return x if shift % 2 == 0 else {'X02': 'X13', 'X13': 'X02'}[x]
    return x


if __name__ == '__main__':
    mode = sys.argv[1]
    nmax = int(sys.argv[2])
    if mode == 'glue':
        run_glue(nmax, int(sys.argv[3]) if len(sys.argv) > 3 else 6)
    elif mode == 'three':
        run_three(nmax)
    elif mode == 'four':
        import os
        run_four(nmax, os.path.join(HERE, '..', 'data', 'four_cuts_v%d.json' % nmax))


def rule_ok(signs, word):
    """Selection rule: mono boundary edges carry one third of the boundary sign sum."""
    m = len(signs)
    val = {'+': 1, '-': -1}
    tot = sum(val[c] for c in signs)
    mono = sum(val[signs[i]] for i in range(m) if word[i] == word[(i + 1) % m])
    return 3 * mono == tot


def run_full(nmax, m):
    """Is the set of realised patterns of a chordless disk a function of its sign word alone?"""
    universe = set()
    data = []
    for name, g in corpus(6, nmax):
        tri = Tri(g)
        nsep = len(tri.separating_triangles())
        for cyc in cycles_of_length(g, m):
            a, b = sides(tri, cyc)
            d1, d2 = Disk(tri, cyc, a), Disk(tri, cyc, b)
            for d in (d1, d2):
                universe.update(d.ham_states())
            if d1.interior == 0 or d2.interior == 0:
                continue
            for d in (d1, d2):
                if not d.chords:
                    data.append((name, cyc, d.signs, d.interior, nsep, d.ham_states()))
    print('m=%d: abstract states seen %d; chordless sides with interior vertices on both sides: %d'
          % (m, len(universe), len(data)))
    hist = Counter()
    worst = {}
    for name, cyc, signs, interior, nsep, fs in data:
        expected = {s for s in universe if rule_ok(signs, s[0])}
        assert fs <= expected, (name, cyc, signs)
        miss = len(expected) - len(fs)
        hist[len(expected), miss] += 1
        if miss:
            worst.setdefault((len(expected), miss), (name, cyc, signs, interior, nsep,
                             sorted((''.join(map(str, w)), sorted(map(sorted, p))) for w, p in expected - fs)))
    for (e, miss), c in sorted(hist.items()):
        print('  rule-compatible patterns %d, missing %d: %d sides' % (e, miss, c))
    for k, v in sorted(worst.items()):
        print('  example with', k, ':', v)


if __name__ == '__main__' and sys.argv[1] == 'full':
    run_full(int(sys.argv[2]), int(sys.argv[3]))
